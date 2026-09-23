"""A `workflow.py run <unknown>` must refuse BY NAME at exit 2, never traceback.

The runner's own docstring (top of bin/workflow.py, "RUN exit codes") says
`2  resolve failure (bad --args, unknown workflow, harness/model refused)`,
and `main()` catches `(WorkflowsNodeError, ValueError, adapters.AdapterError)`
-> exit 2. `_load_manifest` used to raise a bare `FileNotFoundError`, which is
none of those, so an unknown name escaped as an uncaught traceback at exit 1
(hypothesis:a00-66151f1a-c8cc6d). This test drives the REAL CLI as a subprocess.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
WF = REPO / "extensions" / "agi" / "bin" / "workflow.py"


def test_unknown_workflow_name_is_refused_by_name_exit_2():
    proc = subprocess.run(
        [sys.executable, str(WF), "run", "definitely-not-a-workflow",
         "--dry-run"],
        cwd=REPO, capture_output=True, text=True)
    both = proc.stdout + proc.stderr
    assert proc.returncode == 2, (proc.returncode, both)
    assert "definitely-not-a-workflow" in both, both
    assert "Traceback" not in both, both
    assert "FileNotFoundError" not in both, both
