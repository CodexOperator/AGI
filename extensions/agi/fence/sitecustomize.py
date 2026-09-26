"""The inherited-env fence: this file is the `sitecustomize` a no-model round puts
on PYTHONPATH, so EVERY python process the round starts installs the refusal at
interpreter start -- the parent, a kid, a grandchild -- before it can import a
loader. It reads the SAME table module as the pytest conftest
(`extensions/agi/model_fence.py`), resolved in this order:

1. `import model_fence` -- the fence dir and `extensions/agi` are on PYTHONPATH;
2. `AGI_MODEL_FENCE_SRC` (set by dispatch; the file, or the dir holding it) --
   loaded by path, so a fenced process whose PYTHONPATH was rewritten still
   refuses. Degradation is a file-load, NEVER a second table: two tables is
   falsifier 3.

Fails SILENT and never raises: a sitecustomize that throws breaks the
interpreter it was meant to protect.
"""
import importlib.util
import os
import sys


def _fence_module():
    """The one shared table, by import or by the env var that names its file."""
    try:
        import model_fence  # noqa: PLC0415 -- the import IS the resolution
        return model_fence
    except ImportError:
        pass
    src = os.environ.get("AGI_MODEL_FENCE_SRC")
    if not src:
        return None
    src = os.path.join(src, "model_fence.py") if os.path.isdir(src) else src
    if not os.path.isfile(src):
        return None
    spec = importlib.util.spec_from_file_location("model_fence", src)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["model_fence"] = mod       # the same object for any later import
    spec.loader.exec_module(mod)
    return mod


try:
    _fence = _fence_module()
    if _fence is not None:
        _fence.install()       # the import-time barrier, consulted by `import` itself
        _fence.patch_all()     # and a sampler over whatever is ALREADY in sys.modules
except Exception:  # noqa: BLE001 -- a fence that cannot install must not break python
    pass
