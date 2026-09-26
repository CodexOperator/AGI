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
    "huggingface_hub": ("hf_hub_download", "snapshot_download"),
}


def _attrs_for(name):
    """Refused attrs for a module name: its OWN row plus its refused ROOT's.
    `transformers.models.llama.AutoModelForCausalLM` is the dominant real shape and
    the class lives on a SUBMODULE, so the root's row has to reach it."""
    return frozenset(REFUSED.get(name, ())) | frozenset(REFUSED.get(name.split(".")[0], ()))


class ModelLoadRefused(RuntimeError):
    """A test in this suite tried to load model weights."""


def _why(owner, attr):
    return (f"model load refused by construction: {owner}.{attr}() may read "
            "weights; this suite asserts on bytes, never on a model")


def _stub(owner, attr):
    def _refuse(*_a, **_kw):
        raise ModelLoadRefused(_why(owner, attr))
    _refuse.__name__, _refuse._model_load_stub = attr, True
    return _refuse


def _patch_one(name, module):
    """Patch a loader's refused attrs on the module AND on the classes it holds:
    AutoModel.from_pretrained is a method on the class, not a module attribute."""
    attrs = _attrs_for(name)
    if module is None or not attrs:
        return 0
    owners = [module] + [o for o in vars(module).values() if isinstance(o, type)]
    n = 0
    for owner in owners:
        for attr in attrs:
            cur = getattr(owner, attr, None)
            # Only an attr the owner HAS is a loader; adding one to every class
            # is noise, and a real install holds immutable C types (torch.dtype,
            # torch.Size) where setattr raises TypeError -- which errored EVERY
            # test on a python with torch (DH.392 harvest, director-engine gen 24).
            if cur is None or getattr(cur, "_model_load_stub", False) is True:
                continue
            try:
                setattr(owner, attr, _stub(owner.__name__, attr))
            except (TypeError, AttributeError):
                continue
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
