"""A research stage that declared a `result_file` and wrote it complete on
disk returns that file as its structured result -- the run does not fail at
the structured return when the work is there.

hypothesis:l4-a-research-stage-whose-digest-file-is-complete-returns-it-as-its-
structured-result-never-fails-the-run-at-the-structured-return. The six
conjuncts: (1) unstructured stdout + complete digest -> resolved-from-digest
and downstream runs; (2) wall-cut stage + complete digest -> same; (3)
unstructured + INCOMPLETE digest -> the stage fails and its dependent is
skipped BY NAME; (4) a valid structured block still wins over the file; (5) a
stage with no `result_file` key is byte-for-byte today's behaviour; (6) the run
status names the stages that resolved from a digest.

All subprocess is a fixture: no pi binary, no network, no real sleep.
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

import pytest
from unittest import mock

REPO = Path(__file__).resolve().parents[3]
BIN = REPO / "extensions" / "agi" / "bin"
sys.path.insert(0, str(BIN))

import subprocess as _sp  # noqa: E402

import workflow as _wf  # noqa: E402
from workflow import RunView, _run_stage_pi, run_workflow  # noqa: E402


@pytest.fixture(autouse=True)
def _no_ambient_pi_bin(monkeypatch):
    """`$PI_BIN` now WINS over the config cell (the ONE shared resolver), so
    a suite run from a pi seat would otherwise dispatch these fake-bin tests
    at the real pi. (hypothesis:harness-bin-paths-resolve-per-box round 3)"""
    monkeypatch.delenv("PI_BIN", raising=False)

SCHEMA = {"type": "object", "properties": {"a": {"type": "string"}},
          "required": ["a"]}
VALID = {"a": "from-digest"}
def _fake_pi_bin() -> str:
    """A REAL, never-spawned `harnesses.pi.bin` cell.

    A path-shaped `bin` cell that does not exist REFUSES by name
    (`hypothesis:harness-bin-absolute-token-free-bins-refused-by-name`), so the
    `/bin/fakepi` literal these tests used as a stand-in can no longer be
    resolved. `subprocess.run` is mocked throughout; the file exists only to
    satisfy the resolver.
    """
    import tempfile
    p = Path(tempfile.mkdtemp(prefix="fakebin-")) / "fakepi"
    p.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    p.chmod(0o755)
    return str(p)


CFG = {"harnesses": {"pi": {"bin": _fake_pi_bin(), "provider": "openrouter"}}}
KNOBS = {"read:x": {"model": "m", "effort": "low"}}


def _cp(cmd, rc=0, stdout=""):
    return _sp.CompletedProcess(cmd, rc, stdout=stdout, stderr="")


def _stage(tmp_path, result_file=True):
    st = {"label": "read:x", "role": "kid", "prompt": "p",
          "_repeat_item": {"key": "x"}, "schema": SCHEMA}
    if result_file:
        st["result_file"] = str(tmp_path / "read-x.json")
    return st


def _digest(tmp_path, value):
    (tmp_path / "read-x.json").write_text(json.dumps(value), encoding="utf-8")


# -- (1) unstructured stdout + complete digest ------------------------------

def test_unstructured_stdout_resolves_from_complete_digest(tmp_path):
    _digest(tmp_path, VALID)
    view = RunView("k", [_stage(tmp_path)], "pi", out=io.StringIO())
    with mock.patch("subprocess.run",
                    side_effect=lambda c, **k: _cp(c, 0, "prose, no JSON { oops")):
        rc, value = _run_stage_pi(CFG, _stage(tmp_path), KNOBS,
                                  {"scratch": str(tmp_path)}, view=view)
    assert rc == 0, rc
    assert value == VALID, value
    assert view.state["read:x"]["status"] == "resolved", view.state["read:x"]
    assert "resolved-from-digest" in view.state["read:x"]["detail"]


# -- (2) wall-cut stage + complete digest -----------------------------------

def test_wall_cut_stage_resolves_from_complete_digest(tmp_path):
    _digest(tmp_path, VALID)
    st = _stage(tmp_path)

    def boom(cmd, **kw):
        raise _sp.TimeoutExpired(cmd, kw.get("timeout") or 1)

    with mock.patch("subprocess.run", side_effect=boom):
        rc, value = _run_stage_pi(CFG, st, KNOBS, {"scratch": str(tmp_path)},
                                  timeout_s=1)
    assert rc == 0, rc
    assert value == VALID, value


# -- (3) incomplete digest -> fail (the file is never accepted as a result) --

def test_incomplete_or_absent_digest_fails_the_stage(tmp_path):
    _digest(tmp_path, {"a": 123})  # parses, fails the schema
    st = _stage(tmp_path)
    view = RunView("k", [st], "pi", out=io.StringIO())
    with mock.patch("subprocess.run",
                    side_effect=lambda c, **k: _cp(c, 0, "prose, no JSON")):
        rc, value = _run_stage_pi(CFG, st, KNOBS, {"scratch": str(tmp_path)},
                                  view=view)
    assert rc != 0 and value is None, (rc, value)
    assert view.state["read:x"]["status"] == "failed", view.state["read:x"]
    (tmp_path / "read-x.json").unlink()  # absent is the same failure
    with mock.patch("subprocess.run",
                    side_effect=lambda c, **k: _cp(c, 0, "prose, no JSON")):
        rc2, value2 = _run_stage_pi(CFG, st, KNOBS, {"scratch": str(tmp_path)})
    assert rc2 != 0 and value2 is None, (rc2, value2)


# -- (4) a valid structured block still wins over the file ------------------

def test_valid_structured_block_wins_over_digest(tmp_path):
    _digest(tmp_path, {"a": "from-file"})
    with mock.patch("subprocess.run",
                    side_effect=lambda c, **k: _cp(c, 0, '{"a": "from-stdout"}')):
        rc, value = _run_stage_pi(CFG, _stage(tmp_path), KNOBS,
                                  {"scratch": str(tmp_path)})
    assert rc == 0 and value == {"a": "from-stdout"}, value


# -- (5) no result_file key -> today's behaviour byte-for-byte --------------

def test_no_result_file_key_is_unchanged(tmp_path):
    with mock.patch("subprocess.run",
                    side_effect=lambda c, **k: _cp(c, 0, "prose, no JSON")):
        rc, value = _run_stage_pi(CFG, _stage(tmp_path, result_file=False),
                                  KNOBS, {"scratch": str(tmp_path)})
    assert rc == 0, rc
    assert value == {"unstructured": "prose, no JSON"}, value


# -- (6) full run: resolved-from-digest named; a failed digest skips its dep -

_FAKE = """#!/usr/bin/env python3
import json, os, sys
prompt = sys.argv[-1]
if 'prior text follows' in prompt:
    sys.stdout.write(json.dumps({"ok": True}))
    sys.exit(0)
path = os.environ.get('FAKE_RESULT_FILE')
mode = os.environ.get('FAKE_RESULT_MODE', 'complete')
if path and mode == 'complete':
    open(path, 'w', encoding='utf-8').write(json.dumps({"a": "digest"}))
elif path and mode == 'incomplete':
    open(path, 'w', encoding='utf-8').write(json.dumps({"a": 123}))
sys.stdout.write('prose with no schema-valid JSON')
"""


def _manifest(tmp_path):
    return {
        "name": "review", "type": "review", "script": "agi-round-review.js",
        "stages": [
            {"label": "find", "role": "kid", "model_hint": "sonnet",
             "effort_hint": "low",
             "repeat": {"of": "targets", "label_template": "find:{window}"},
             "prompt": "find things", "schema": SCHEMA,
             "result_file": str(tmp_path / "find-{window}.json")},
            {"label": "refute", "role": "reviewer", "model_hint": "sonnet",
             "effort_hint": "medium", "chained_from": "find",
             "repeat": {"of": "targets", "label_template": "refute:{window}"},
             "prompt": "prior text follows:\n{unstructured}\nend prior",
             "schema": {"type": "object",
                        "properties": {"ok": {"type": "boolean"}},
                        "required": ["ok"]}},
        ],
    }


def _run_full(tmp_path_factory, tmp_path, monkeypatch, mode):
    fake = tmp_path / "fakepi"
    fake.write_text(_FAKE, encoding="utf-8")
    fake.chmod(0o755)
    saved_manifest, saved_cfg = _wf._load_manifest, _wf._load_config
    saved_root = _wf._loc.shared_project_root

    def cfg(root):
        c = json.loads(json.dumps(saved_cfg(root)))
        c.setdefault("harnesses", {}).setdefault("pi", {})["bin"] = str(fake)
        return c

    sessions = tmp_path_factory.mktemp("wf-sessions")
    _wf._loc.shared_project_root = lambda root: sessions
    monkeypatch.setenv("FAKE_RESULT_FILE", str(tmp_path / "find-t1.json"))
    monkeypatch.setenv("FAKE_RESULT_MODE", mode)
    _wf._load_manifest = lambda repo, key: _manifest(tmp_path)
    _wf._load_config = cfg
    try:
        buf = io.StringIO()
        rc = run_workflow(REPO / ".agi", "review", "pi",
                          {"targets": [{"window": "t1"}]}, False, out=buf)
        text = buf.getvalue()
        path = sessions / "sessions" / "workflows" / "review.jsonl"
        rows = ([json.loads(l) for l in
                 path.read_text(encoding="utf-8").splitlines()]
                if path.exists() else [])
        return rc, text, rows
    finally:
        _wf._load_manifest, _wf._load_config = saved_manifest, saved_cfg
        _wf._loc.shared_project_root = saved_root


def test_full_run_resolves_from_digest_and_names_it(tmp_path_factory, tmp_path,
                                                    monkeypatch):
    rc, text, rows = _run_full(tmp_path_factory, tmp_path, monkeypatch,
                               "complete")
    assert rc == 0, text
    assert "[·] find:t1" in text, text
    assert "resolved-from-digest" in text, text
    assert "[✓] refute:t1" in text, "the dependent must still run"
    assert rows and "find:t1" in rows[0]["resolved_from_digest"], rows


def test_full_run_incomplete_digest_fails_and_skips_dependent(
        tmp_path_factory, tmp_path, monkeypatch):
    rc, text, rows = _run_full(tmp_path_factory, tmp_path, monkeypatch,
                               "incomplete")
    assert rc != 0, text
    assert "[✗] find:t1" in text, text
    assert "skipped" in text and "dependency 'find'" in text, text
    assert rows and rows[0]["stages"]["find:t1"] == "failed", rows


# -- trove-survey: panel and judge declare a result_file --------------------

def test_trove_survey_panel_and_judge_declare_result_file():
    """hypothesis:lm-pi-stage-never-sees-its-schema...: panel and judge were
    handed neither a result_file nor a closing schema sentence, unlike read
    and critique. Both must now declare a rendered result_file whose parent
    dir is the run scratch."""
    import json as _json
    from pathlib import Path as _Path
    manifest = _json.loads(
        (REPO / "extensions" / "agi" / "workflows" / "trove-survey.json")
        .read_text(encoding="utf-8"))
    by_label = {s["label"]: s for s in manifest["stages"]}
    for label in ("panel", "judge"):
        st = by_label[label]
        assert st.get("result_file"), f"{label} declares no result_file"
        assert "{scratch}" in st["result_file"], st["result_file"]
        tail = st["prompt"][-400:]
        assert "JSON object" in tail and "schema" in tail, \
            f"{label} prompt names no required schema: {tail!r}"
