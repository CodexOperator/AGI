"""No model load by construction: every weights-loading entry point REFUSES, by name.

A thin pytest shell around ONE shared fence, `extensions/agi/model_fence.py` --
the same table the inherited-env `sitecustomize` installs in a non-pytest process
of a no-model round (falsifier 3: one definition, never two). The box is
memory-guarded (belam 04:29Z): a stand-in `torch` that only RECORDS its `load`
calls still trips this; no library is imported to install the guard.

This file keeps only what pytest needs: the re-exported names the guard tests
reach through `sys.modules[conftest]`, the import-time hook's lifetime, and the
per-test declaration clear.
"""
import importlib.util
import os
import pathlib
import sys

import pytest

# `AGI_MODEL_FENCE_SRC` names the file (or the dir holding it) so the guard
# resolves from an env, not from a literal path; the sibling of this conftest
# under `extensions/agi/` is the default.
_SRC = os.environ.get("AGI_MODEL_FENCE_SRC") or str(
    pathlib.Path(__file__).resolve().parents[2] / "extensions" / "agi" / "model_fence.py")
_spec = importlib.util.spec_from_file_location("model_fence", _SRC)
# NOT registered in sys.modules: a guard test finds "the module that owns the
# guard" by scanning sys.modules for ModelLoadRefused/_patch_one, and it must
# land on this conftest, not on the shared module it imported.
model_fence = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(model_fence)

# One table, re-exported (NOT copied) so a test that reaches it through
# `sys.modules[conftest]` sees the same objects the fence installed.
REFUSED = model_fence.REFUSED
_ALLOWED = model_fence._ALLOWED
ModelLoadRefused = model_fence.ModelLoadRefused
_patch_one = model_fence._patch_one
_patch_all = model_fence.patch_all

# The pytest-visible cap cell. `_cap` below reads THIS global, so
# `monkeypatch.setattr(conftest, "MAX_ALLOWED_LOAD_BYTES", 0)` still bites
# without the shared module keeping a second copy of the number.
MAX_ALLOWED_LOAD_BYTES = model_fence.MAX_ALLOWED_LOAD_BYTES
model_fence.set_cap_source(lambda: globals()["MAX_ALLOWED_LOAD_BYTES"])

_LOAD_HOOK = model_fence.install()   # hole C, the import half: `import` itself


def pytest_sessionfinish(session, exitstatus):
    """Removed at session end: the hook outlives neither the run nor the process."""
    model_fence.uninstall(_LOAD_HOOK)


@pytest.fixture
def allow_model_load():
    """Declare the one dir this test BUILT itself, so it may be read back."""
    return model_fence.allow_model_load


@pytest.fixture(autouse=True)
def _no_model_load():
    """Re-scan per test: a module imported since the last scan is caught too."""
    _patch_all()
    yield
    model_fence.clear_allowed()   # a declaration never outlives its test


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_call(item):
    """Scan AGAIN after every fixture ran, right before the body: a stand-in a
    test's own fixture installs (monkeypatch.setitem on sys.modules) is seen."""
    _patch_all()


@pytest.fixture
def model_load_refusal():
    return ModelLoadRefused
