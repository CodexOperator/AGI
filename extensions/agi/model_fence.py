"""THE one loader table and the one refusal, shared by both fences.

Two consumers, ONE definition (falsifier 3 of
hypothesis:a-no-model-round-refuses-a-model-load-in-every-process-it-spawns):
`.agi/context/conftest.py` (the pytest guard, DH.392/413) and
`extensions/agi/fence/sitecustomize.py` (the inherited-env guard every python
process of a no-model round installs at import time). Moved VERBATIM out of the
conftest, harvest comments included -- a second table is the defect, not a
faster edit. No library is imported to install the guard, and nothing here ever
opens a weights dir.
"""
import importlib.util
import inspect
import json
import os
import pathlib
import sys

# loader module -> the attributes that would read weights off disk or the hub
REFUSED = {
    "torch": ("load", "jit_load", "load_file", "safe_open", "from_pretrained"),
    "torch.jit": ("load",), "safetensors": ("safe_open",),
    "safetensors.torch": ("load_file", "load"), "gguf": ("GGUFReader",),
    "transformers": ("from_pretrained",), "llama_cpp": ("Llama", "LlamaModel"),
    "vllm": ("LLM",),
    "huggingface_hub": ("hf_hub_download", "snapshot_download"),
}
_ALLOWED: set = set()   # realpaths a test declared for THIS test, cleared per test


def _cap_from_config():
    """`values.core.model_load_allowed_max_bytes`, found by walking up from this
    file. A config cell, not a literal -- and if the cell cannot be found the
    cap is 0: the allow-list earns nothing and every declared dir is refused."""
    for parent in pathlib.Path(__file__).resolve().parents:
        for name in (".agi/config.json", "agi-tree.config.json"):
            cfg = parent / name
            if cfg.is_file():
                return json.loads(cfg.read_text())["values"]["core"]["model_load_allowed_max_bytes"]
    return 0


# The cap is read THROUGH `_cap`, never bound at patch time: the conftest
# re-points it at its own module global, which its tests monkeypatch to 0.
MAX_ALLOWED_LOAD_BYTES = int(os.environ.get("AGI_MODEL_FENCE_MAX_BYTES")
                             or _cap_from_config())


def _cap():
    return MAX_ALLOWED_LOAD_BYTES


def set_cap_source(fn):
    """The conftest owns the pytest-visible cap cell and re-points the shared
    `_cap` at it, so `monkeypatch.setattr(conftest, "MAX_ALLOWED_LOAD_BYTES", 0)`
    still bites -- one table, one cap, no second copy of either."""
    global _cap
    _cap = fn


def _attrs_for(name):
    """Refused attrs for a module name: its OWN row plus its refused ROOT's.
    `transformers.models.llama.AutoModelForCausalLM` is the dominant real shape and
    the class lives on a SUBMODULE, so the root's row has to reach it."""
    return frozenset(REFUSED.get(name, ())) | frozenset(REFUSED.get(name.split(".")[0], ()))


class ModelLoadRefused(RuntimeError):
    """A process in a no-model round tried to load model weights."""


def _why(owner, attr):
    return (f"model load refused by construction: {owner}.{attr}() may read "
            "weights; this suite asserts on bytes, never on a model")


def allow_model_load(*paths):
    """Declare the one dir a test BUILT itself, so it may be read back."""
    for p in paths:
        _ALLOWED.add(os.path.realpath(p))


def clear_allowed():
    """A declaration never outlives the test that made it."""
    _ALLOWED.clear()


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
                   for r, _, fs in os.walk(root) for f in fs) <= _cap()
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


def patch_all():
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


def install():
    """Put the import-time guard in THIS process's meta_path and return the hook,
    so a caller that owns a lifetime (pytest session, or a forked child) can
    `uninstall` it. Idempotent-ish: the hook is one object per call."""
    hook = _RefuseOnLoad()
    sys.meta_path.insert(0, hook)
    return hook


def uninstall(hook):
    if hook in sys.meta_path:
        sys.meta_path.remove(hook)
