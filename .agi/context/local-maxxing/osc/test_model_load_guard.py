"""Falsifiers 1-3 of hypothesis:the-context-suite-refuses-a-model-load-by-construction.

Stand-in modules only -- no real library, no weights file, no network. The stand-ins
are installed at MODULE level, which is the falsifier's shape: a context test that
fakes `torch` and then calls `torch.load`. The conftest's per-test scan has to see
them before any test body runs.
"""

import importlib
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


class _AutoCausal:
    """The REAL shape: the loader class is held by a SUBMODULE, not by the root."""
    @classmethod
    def from_pretrained(cls, name, **kw):
        cls._calls.append((name, kw))
        return "RECORDED"


_AutoModel._calls, _AutoCausal._calls = [], []
_tfl = types.ModuleType("transformers.models.llama")
_tfl.AutoModelForCausalLM = _AutoCausal
STANDS = {
    "torch": _standin("torch", load=lambda *a, **k: "RECORDED"),
    "safetensors.torch": _standin("safetensors.torch", load_file=lambda *a, **k: "RECORDED"),
    "gguf": _standin("gguf", GGUFReader=lambda *a, **k: "RECORDED"),
    "llama_cpp": _standin("llama_cpp", Llama=lambda *a, **k: "RECORDED"),
}
_tf = _standin("transformers")
_tf.AutoModel = _AutoModel
STANDS["transformers"] = _tf
STANDS["transformers.models.llama"] = _tfl
STANDS["huggingface_hub"] = _standin(
    "huggingface_hub", hf_hub_download=lambda *a, **k: "RECORDED",
    snapshot_download=lambda *a, **k: "RECORDED")


@pytest.fixture(autouse=True)
def _standins(monkeypatch):
    """Install the stand-ins PER TEST and restore sys.modules after it. At import
    time (the old shape) they leaked into every module collected after this one:
    a real torch test got the stand-in ('module torch has no attribute
    set_num_threads', TMM.231). The conftest's pytest_runtest_call re-scan sees
    them before the body runs."""
    for name, mod in STANDS.items():
        monkeypatch.setitem(sys.modules, name, mod)
    yield


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


def test_submodule_held_transformers_class_is_refused(model_load_refusal):
    """Hole A: AutoModelForCausalLM lives on `transformers.models.llama`, a SUBMODULE
    of a refused root -- a root-only walk misses it, and it is the dominant real shape."""
    sub = sys.modules["transformers.models.llama"]
    with pytest.raises(model_load_refusal):
        sub.AutoModelForCausalLM.from_pretrained("qwen/qwen3-8b")
    assert _AutoCausal._calls == []


def test_hf_hub_download_is_refused(model_load_refusal):
    """Hole B: the hub fetch is a weights read too, and was absent from the table."""
    hub = sys.modules["huggingface_hub"]
    for call in (lambda: hub.hf_hub_download("Qwen/Qwen3-8B", "qwen3.safetensors"),
                 lambda: hub.snapshot_download("Qwen/Qwen3-8B")):
        with pytest.raises(model_load_refusal):
            call()
    assert hub._calls == []


def test_a_module_imported_inside_the_body_is_refused_not_recorded(
        tmp_path, monkeypatch, model_load_refusal):
    """Hole C, the import half -- CLOSED by the sys.meta_path hook in the conftest.
    A refused root is imported from a real path (FileFinder + SourceFileLoader, so
    the loader wrapping is exercised, not just a dict stand-in), INSIDE the body:
    `import` itself consults the hook, so there is no re-scan to outrun. This is
    the shape of osc_lowpeak_test.py:46, which imports transformers in a body."""
    (tmp_path / "vllm.py").write_text(
        "CALLS = []\n"
        "def LLM(*a, **k):\n"
        "    CALLS.append(a)\n"
        "    return 'RECORDED'\n")
    monkeypatch.syspath_prepend(str(tmp_path))
    monkeypatch.delitem(sys.modules, "vllm", raising=False)
    try:
        import vllm  # noqa: PLC0415 -- the import IS the falsifier
        assert vllm.__name__ == "vllm"       # the inner loader still ran in full
        with pytest.raises(model_load_refusal):
            vllm.LLM(model="/models/8b.gguf")
        assert vllm.CALLS == []               # the REAL function was never reached
    finally:
        sys.modules.pop("vllm", None)


def test_the_hook_does_not_invent_an_absent_refused_module():
    """A refused root that is not installed must still raise the ImportError the
    interpreter would raise -- the hook must not answer for a module it cannot find."""
    with pytest.raises(ImportError):
        importlib.import_module("vllm")


def test_the_hook_is_removed_at_session_end():
    """The conftest is a guard on THIS run's interpreter, not on the process: the
    hook is uninstalled by pytest_sessionfinish, so a caller outside the suite
    (a build script, a REPL) keeps its own import semantics."""
    conftest = sys.modules[_no_model_load_owner()]
    assert conftest._LOAD_HOOK in sys.meta_path
    try:
        conftest.pytest_sessionfinish(None, 0)
        assert conftest._LOAD_HOOK not in sys.meta_path
    finally:
        sys.meta_path.insert(0, conftest._LOAD_HOOK)   # restore for the rest of the run


@pytest.mark.xfail(strict=False, reason="RESIDUAL HOLE, named not closed: a module written DIRECTLY "
                                       "into sys.modules by the body (`sys.modules['vllm'] = mod`) "
                                       "bypasses `import` entirely, so the meta_path hook never sees "
                                       "it. Unclosable without wrapping the dict: CPython caches it "
                                       "(the swap broke collection with KeyError: zoneinfo._tzpath) and "
                                       "types.ModuleType is immutable. The import half of hole C is "
                                       "closed by experiment:a00-18859cb2-820ca3; this half is not.")
def test_body_written_into_sys_modules_directly_is_still_unseen(model_load_refusal):
    """Hole C, the dict half: still open. A body that ASSIGNS sys.modules is not
    importing anything. The canary, not a proof."""
    late = types.ModuleType("vllm")
    late.LLM = lambda *a, **k: "RECORDED"
    sys.modules["vllm"] = late
    try:
        with pytest.raises(model_load_refusal):
            sys.modules["vllm"].LLM(model="/models/8b.gguf")
    finally:
        sys.modules.pop("vllm", None)


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


def test_a_real_install_shape_with_c_types_does_not_error_the_guard():
    """DH.392 harvest: a real torch holds immutable C types (torch.dtype,
    torch.Size). The guard set the refused attrs on EVERY class the module held,
    so setattr raised TypeError and the autouse fixture errored every test on a
    python with torch installed. Only an attr the owner HAS is patched, and an
    immutable owner is skipped -- the module's own loader is still refused."""
    conftest = sys.modules[_no_model_load_owner()]
    mod = _standin("torch_ctypes_shape", load=None)
    mod.dtype, mod.Size = int, tuple

    class Tensor:
        pass

    mod.Tensor = Tensor
    conftest._patch_one("torch", mod)          # must not raise
    assert not hasattr(Tensor, "load")         # nothing added to a non-loader
    with pytest.raises(conftest.ModelLoadRefused):
        mod.load("w.pt")


def _no_model_load_owner():
    """The loaded .agi/context conftest module, found by the guard it defines."""
    for name, m in list(sys.modules.items()):
        # __dict__, never getattr: torch.ops (an _OpNamespace) answers ANY
        # attribute, so a getattr probe picked it on a torch python (TMM.231)
        d = m.__dict__ if isinstance(m, types.ModuleType) else {}
        if "ModelLoadRefused" in d and "_patch_one" in d:
            return name
    pytest.skip("the .agi/context conftest is not loaded in this run")


def test_a_proxy_whose_attribute_access_raises_is_skipped_not_fatal(monkeypatch):
    """TMM.231 defect 1, without torch: `torch.classes` is a _ClassNamespace whose
    getattr raises RuntimeError (not AttributeError), so getattr's default never
    caught it and the autouse scan errored every test on a torch python."""
    class _Namespace(types.ModuleType):
        def __getattr__(self, attr):
            raise RuntimeError(f"Tried to instantiate class {attr}")
    monkeypatch.setitem(sys.modules, "torch.classes", _Namespace("torch.classes"))
    conftest = sys.modules[_no_model_load_owner()]
    conftest._patch_all()   # must not raise


def test_standins_never_leak_into_a_later_module(tmp_path):
    """TMM.231 defect 2: run this file, then a module collected AFTER it, in one
    session; the later module must not see a stand-in torch."""
    import os
    import subprocess
    if os.environ.get("AGI_GUARD_LEAK_CHILD"):
        pytest.skip("inside the leak probe's own child run")
    later = tmp_path / "test_zz_later.py"
    later.write_text(
        "import sys\n"
        "def test_no_standin():\n"
        "    t = sys.modules.get('torch')\n"
        "    assert t is None or not hasattr(t, '_calls'), t\n")
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                        __file__, str(later)], capture_output=True, text=True, timeout=120,
                       env=dict(os.environ, AGI_GUARD_LEAK_CHILD="1"))
    assert r.returncode == 0, r.stdout[-2000:]
