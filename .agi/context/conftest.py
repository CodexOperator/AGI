"""No model load by construction: every weights-loading entry point REFUSES, by name.

The box is memory-guarded (belam 04:29Z). A stand-in `torch` that only RECORDS its
`load` calls still trips this; no library is imported to install the guard.
"""
import importlib.util
import inspect
import json
import os
import pathlib
import sys

import pytest

_CFG = json.loads((pathlib.Path(__file__).resolve().parents[1] / "config.json").read_text())
# The byte budget a DECLARED dir may hold and still be read. A config cell, not a
# literal: the allow-list is only as safe as this number (falsifier 3, > ~200 MiB).
MAX_ALLOWED_LOAD_BYTES = _CFG["values"]["core"]["model_load_allowed_max_bytes"]
_ALLOWED: set = set()   # realpaths a test declared for THIS test, cleared per test

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


def _stub(owner, attr, real, bound=False):
    """Refuse, unless the call names a dir THIS test DECLARED (allow_model_load)
    whose bytes are still under the cap -- then delegate to the real loader, so a
    test that built a tiny config-built checkpoint in its own tmp dir can read it
    back (osc_lowpeak_test.py:46-51). Declaration, not tmp-ness, is the key: a
    from_pretrained on a dir under tmp_path that the test did not declare is
    still refused, so the allow-list is not a general tmp_path hole.

    `bound=True` is a CLASSMETHOD loader (`AutoModel*.from_pretrained`): the call
    arrives as (cls, path, ...), so the path is a[1], and `real` is the raw
    function, re-bound to the CALLING class -- never the class it was found on,
    which would drop the subclass (DH.413 harvest: a[0] was the class, so a
    declared tmp checkpoint was refused)."""
    def _refuse(*a, **kw):
        path = a[1] if bound and len(a) > 1 else (a[0] if a and not bound else None)
        if path is None:
            path = kw.get("pretrained_model_name_or_path")
        if _declared_ok(path):
            return real(*a, **kw)
        raise ModelLoadRefused(_why(owner, attr))
    _refuse.__name__, _refuse._model_load_stub = attr, True
    _refuse._real_loader = real
    return classmethod(_refuse) if bound else _refuse


def _declared_ok(obj):
    """True only for a declared, existing-or-empty, under-cap directory path."""
    if not isinstance(obj, (str, os.PathLike)):
        return False
    try:
        real = os.path.realpath(obj)
        # the declared dir OR a file under it: a from_pretrained on the dir opens
        # <dir>/model.safetensors through safe_open (DH.413 harvest); the cap is
        # measured on the DECLARED root, so a file cannot dodge it
        root = next((d for d in _ALLOWED
                     if real == d or real.startswith(d.rstrip(os.sep) + os.sep)), None)
        if root is None:
            return False
        return sum(os.path.getsize(os.path.join(r, f))
                   for r, _, fs in os.walk(root) for f in fs) <= MAX_ALLOWED_LOAD_BYTES
    except (OSError, TypeError, ValueError):
        return False


def _safe_get(obj, attr):
    """`getattr` that never raises: a real install holds PROXIES whose attribute
    access raises something other than AttributeError -- `torch.classes` (a
    `_ClassNamespace`) raises RuntimeError("Tried to instantiate class ..."),
    which `getattr`'s default does not catch, and the autouse scan errored EVERY
    test on a torch python (TMM.231, director-engine gen 24)."""
    try:
        return getattr(obj, attr, None)
    except Exception:  # noqa: BLE001 -- an unreadable attr is not a loader
        return None


def _patch_one(name, module):
    """Patch a loader's refused attrs on the module AND on the classes it holds:
    AutoModel.from_pretrained is a method on the class, not a module attribute."""
    attrs = _attrs_for(name)
    if module is None or not attrs:
        return 0
    try:
        held = list(vars(module).values())
    except TypeError:  # a sys.modules entry with no __dict__ (a proxy)
        held = []
    owners = [module] + [o for o in held if isinstance(o, type)]
    n = 0
    for owner in owners:
        for attr in attrs:
            cur = _safe_get(owner, attr)
            # Only an attr the owner HAS is a loader; adding one to every class
            # is noise, and a real install holds immutable C types (torch.dtype,
            # torch.Size) where setattr raises TypeError (DH.392 harvest).
            if cur is None or _safe_get(cur, "_model_load_stub") is True:
                continue
            try:
                # the real loader is kept for the declared-dir delegation, and the
                # stub is never wrapped by itself if the module is patched twice
                raw = vars(owner).get(attr) if isinstance(owner, type) else None
                if isinstance(raw, classmethod):
                    # a classmethod DEFINED here: patch it as one, delegating to
                    # its raw function so the calling subclass stays `cls`
                    setattr(owner, attr, _stub(_safe_get(owner, "__name__") or name,
                                               attr, raw.__func__, bound=True))
                elif isinstance(owner, type) and inspect.ismethod(cur):
                    continue   # an INHERITED classmethod: its defining class is patched
                else:
                    setattr(owner, attr, _stub(_safe_get(owner, "__name__") or name, attr,
                                               _safe_get(cur, "_real_loader") or cur))
            except Exception:  # noqa: BLE001 -- immutable / proxy owner: skip
                continue
            n += 1
    return n


def _patch_all():
    return sum(_patch_one(n, m) for n, m in list(sys.modules.items()))


class _Patching:
    """Delegates every loader call to the real loader; patches the module the
    INSTANT it is exec'd. `create_module` is reached only when the inner loader
    has one (importlib getattr-swallows the AttributeError otherwise), so the
    module-creation path is byte-for-byte the inner loader's."""

    def __init__(self, inner, name):
        self._inner, self._name = inner, name

    def create_module(self, spec):
        return self._inner.create_module(spec)

    def exec_module(self, module):
        self._inner.exec_module(module)
        _patch_one(self._name, module)

    def __getattr__(self, attr):
        return getattr(self._inner, attr)


class _RefuseOnLoad:
    """Hole C, the import half: a refused module is guarded the moment it is
    exec'd, so a module imported INSIDE a test body cannot outrun the guard. The
    per-test re-scan is a SAMPLER, not a barrier -- the body's next line can run
    before it. This hook is the barrier: it is consulted by `import` itself.
    Delegates to the real finders via importlib.util.find_spec with itself
    removed, so no finder's find_spec signature is ever guessed at."""

    def find_spec(self, fullname, path=None, target=None):
        if not _attrs_for(fullname):
            return None                      # the common case: not a refused root
        try:
            sys.meta_path.remove(self)
        except ValueError:
            return None
        try:
            spec = importlib.util.find_spec(fullname)
        except (ImportError, AttributeError, ValueError):
            return None                      # absent: leave the ImportError to the caller
        finally:
            sys.meta_path.insert(0, self)
        if spec is not None and spec.loader is not None:
            spec.loader = _Patching(spec.loader, fullname)
        return spec


_LOAD_HOOK = _RefuseOnLoad()
sys.meta_path.insert(0, _LOAD_HOOK)


def pytest_sessionfinish(session, exitstatus):
    """Removed at session end: the hook outlives neither the run nor the process."""
    if _LOAD_HOOK in sys.meta_path:
        sys.meta_path.remove(_LOAD_HOOK)


@pytest.fixture
def allow_model_load():
    """Declare the one dir this test BUILT itself, so it may be read back."""
    def _declare(*paths):
        for p in paths:
            _ALLOWED.add(os.path.realpath(p))
    return _declare


@pytest.fixture(autouse=True)
def _no_model_load():
    """Re-scan per test: a module imported since the last scan is caught too."""
    _patch_all()
    yield
    _ALLOWED.clear()   # a declaration never outlives its test


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_call(item):
    """Scan AGAIN after every fixture ran, right before the body: a stand-in a
    test's own fixture installs (monkeypatch.setitem on sys.modules) is seen."""
    _patch_all()


@pytest.fixture
def model_load_refusal():
    return ModelLoadRefused
