"""Pre/post-fix probe: what does a pi stage timeout PRINT?

A stage whose pi process exceeds timeout_s raises subprocess.TimeoutExpired,
a subclass of SubprocessError, so the lone `except (OSError,
SubprocessError)` branch reported it as 'could not start pi: <exc>' with the
whole command -- prompt and all -- buried inside the exception text.
"""
import io, sys, subprocess
from unittest import mock
sys.path.insert(0, "extensions/agi/bin")
import workflow as _wf

STAGE = {"label": "refute:a", "kind": "pi", "prompt": "REFUTE THIS", "schema": {}}
CFG = {"harnesses": {"pi": {}}}


def fake_run(cmd, **kw):
    raise subprocess.TimeoutExpired(cmd, 600)


err = io.StringIO()
with mock.patch("subprocess.run", side_effect=fake_run), \
     mock.patch.object(sys, "stderr", err):
    rc, value = _wf._run_stage_pi(
        CFG, STAGE, {"refute:a": {"model": "m", "effort": "x"}}, {},
        timeout_s=600)
print("rc=", rc, "value=", value)
print("stderr:", err.getvalue().strip())
