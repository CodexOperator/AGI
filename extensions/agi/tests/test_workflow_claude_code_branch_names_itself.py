"""SM.120: a claude-code workflow run NAMES ITSELF on stderr.

hypothesis:l4-a-workflow-run-on-the-claude-code-harness-says-it-executed-
nothing-and-names-the-two-real-routes. The claude-code branch of
`run_workflow` resolves and describes every stage (the .js is the runner
there) and used to do so in total silence -- a live run read as if it had
executed the two stages. Lock: exactly ONE named stderr line on the
claude-code path, stdout byte-identical, and the pi path silent.
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BIN))

import workflow  # noqa: E402
from workflow import run_workflow  # noqa: E402


def _tmp_session_root(tmp_path_factory, wf_mod):
    """Same throwaway seam test_workflow.py uses: redirect workflow's
    `<project>/sessions/` resolution under tmp (no phantom production row)."""
    tmp = tmp_path_factory.mktemp("wf-sessions")
    saved = wf_mod._loc.shared_project_root
    wf_mod._loc.shared_project_root = lambda root: tmp
    return tmp, lambda: setattr(wf_mod._loc, "shared_project_root", saved)


def test_claude_code_branch_names_itself_and_pi_path_is_silent(
        tmp_path_factory, capsys):
    tmp, restore = _tmp_session_root(tmp_path_factory, workflow)
    try:
        # claude-code run: exits 0, resolves both "review" stages, tracks
        # exactly one row under the tmp seam -- exactly as today.
        buf = io.StringIO()
        rc = run_workflow(REPO / ".agi", "review", "claude-code",
                          {"targets": [{"window": "t1"}]}, False, out=buf)
        assert rc == 0
        rows = (tmp / "sessions" / "workflows" / "review.jsonl")\
            .read_text(encoding="utf-8").splitlines()
        assert len(rows) == 1, rows
        assert json.loads(rows[0])["harness"] == "claude-code"

        # stdout unchanged: same view, same terminal summary.
        text = buf.getvalue()
        assert "workflow review (harness=claude-code)" in text
        tail = [l for l in text.splitlines()
                if l.startswith(("[stage]", "[summary]"))]
        assert tail[-1] == ("[summary] workflow=review stages=2 "
                            "ok=0 unstructured=0 failed=0"), tail

        # exactly one stderr line, naming all three facts.
        err = [l for l in capsys.readouterr().err.splitlines() if l.strip()]
        assert len(err) == 1, err
        line = err[0]
        assert line.startswith("workflow.py: "), line
        assert "agi-round-review.js" in line, line
        assert "--harness pi" in line, line
        assert "no stage" in line, line

        # the pi path never prints it (dry-run is enough).
        buf2 = io.StringIO()
        rc2 = run_workflow(REPO / ".agi", "review", "pi", {}, True, out=buf2)
        assert rc2 == 0, buf2.getvalue()
        err2 = [l for l in capsys.readouterr().err.splitlines() if l.strip()]
        assert err2 == [], err2
    finally:
        restore()
