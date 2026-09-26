"""Falsifiers 1-3 of hypothesis:the-context-suite-refuses-a-model-load-by-construction.

Stand-in modules only -- no real library, no weights file, no network. The stand-ins
are installed at MODULE level, which is the falsifier's shape: a context test that
fakes `torch` and then calls `torch.load`. The conftest's per-test scan has to see
them before any test body runs.
"""

import sys
import types

import pytest


def _standin(name, **attrs):
    mod = types.ModuleType(name)
    mod._calls = []
    for attr in attrs:
        def recorder(*a, _name=attr, **kw):
            mod._calls.append((_name, a, kw))
            return "RECORDED"

        recorder.__name__ = attr
        setattr(mod, attr, recorder)
    return mod


class _AutoModel:
    @classmethod
    def from_pretrained(cls, name, **kw):
        cls._calls.append((name, kw))
        return "RECORDED"


_AutoModel._calls = []
STANDS = {
    "torch": _standin("torch", load=lambda *a, **k: "RECORDED"),
    "safetensors.torch": _standin("safetensors.torch", load_file=lambda *a, **k: "RECORDED"),
    "gguf": _standin("gguf", GGUFReader=lambda *a, **k: "RECORDED"),
    "llama_cpp": _standin("llama_cpp", Llama=lambda *a, **k: "RECORDED"),
}
_tf = _standin("transformers")
_tf.AutoModel = _AutoModel
STANDS["transformers"] = _tf
sys.modules.update(STANDS)


@pytest.fixture(scope="session", autouse=True)
def _drop_standins():
    yield
    for name in STANDS:
        sys.modules.pop(name, None)


def test_standin_torch_load_is_refused_not_recorded(model_load_refusal):
    """Falsifier 1: the stand-in's `load` must never be reached."""
    with pytest.raises(model_load_refusal):
        sys.modules["torch"].load("qwen3-8b.safetensors")
    assert sys.modules["torch"]._calls == []


def test_standin_safetensors_load_file(model_load_refusal):
    """Falsifier 2: safetensors."""
    with pytest.raises(model_load_refusal):
        sys.modules["safetensors.torch"].load_file("w.bin")
    assert sys.modules["safetensors.torch"]._calls == []


def test_standin_transformers_from_pretrained(model_load_refusal):
    """Falsifier 2: a classmethod on a stand-in class, the transformers shape."""
    with pytest.raises(model_load_refusal):
        _AutoModel.from_pretrained("qwen/qwen3-8b")
    assert _AutoModel._calls == []


def test_standin_gguf_reader_and_llama_construction(model_load_refusal):
    """Falsifier 2: gguf reader + llama.cpp model construction."""
    for name, call in (("gguf", lambda m: m.GGUFReader("model.gguf")),
                       ("llama_cpp", lambda m: m.Llama("/models/8b.gguf"))):
        with pytest.raises(model_load_refusal):
            call(sys.modules[name])
        assert sys.modules[name]._calls == []


def test_guard_needs_no_library_installed(model_load_refusal):
    """Falsifier 3: the guard is bytes on stand-ins -- nothing heavy is imported."""
    assert getattr(sys.modules["torch"], "__file__", None) is None
    assert issubclass(model_load_refusal, RuntimeError)


def test_ordinary_suite_work_is_unaffected():
    """The guard refuses model loads ONLY -- ordinary calls still run."""
    plain = types.ModuleType("plainmod")
    plain.value = 41
    assert plain.value + 1 == 42
