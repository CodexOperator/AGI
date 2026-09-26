"""No model load by construction: every weights-loading entry point REFUSES, by name.

The box is memory-guarded (belam 04:29Z). A stand-in `torch` that only RECORDS its
`load` calls still trips this; no library is imported to install the guard.
"""
import sys

import pytest

# loader module -> the attributes that would read weights off disk or the hub
REFUSED = {
    "torch": ("load", "jit_load", "load_file", "safe_open", "from_pretrained"),
    "torch.jit": ("load",), "safetensors": ("safe_open",),
    "safetensors.torch": ("load_file", "load"), "gguf": ("GGUFReader",),
    "transformers": ("from_pretrained",), "llama_cpp": ("Llama", "LlamaModel"),
    "vllm": ("LLM",),
}
ROOTS = frozenset(n.split(".")[0] for n in REFUSED)


class ModelLoadRefused(RuntimeError):
    """A test in this suite tried to load model weights."""


def _stub(owner, attr):
    def _refuse(*_a, **_kw):
        raise ModelLoadRefused(
            f"model load refused by construction: {owner}.{attr}() may read "
            "weights; this suite asserts on bytes, never on a model")
    _refuse.__name__, _refuse._model_load_stub = attr, True
    return _refuse


def _patch_one(name, module):
    """Patch a loader's refused attrs on the module AND on the classes it holds:
    AutoModel.from_pretrained is a method on the class, not a module attribute."""
    if module is None or name.split(".")[0] not in ROOTS:
        return 0
    owners = [module] + [o for o in vars(module).values() if isinstance(o, type)]
    n = 0
    for owner in owners:
        for attr in REFUSED.get(name, ()):
            if getattr(getattr(owner, attr, None), "_model_load_stub", False) is not True:
                setattr(owner, attr, _stub(owner.__name__, attr))
                n += 1
    return n


def _patch_all():
    return sum(_patch_one(n, m) for n, m in list(sys.modules.items()))


@pytest.fixture(autouse=True)
def _no_model_load():
    """Re-scan per test: a module imported since the last scan is caught too."""
    _patch_all()
    yield


@pytest.fixture
def model_load_refusal():
    return ModelLoadRefused
