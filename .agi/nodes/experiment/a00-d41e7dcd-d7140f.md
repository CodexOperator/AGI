---
id: experiment:a00-d41e7dcd-d7140f
mint_id: bf552c9006de4ec7a439f089f1875f5f
type: experiment
parents:
  - hypothesis:migrate-transcript-copy-survives-sftp-mode-scp
next_edges: []
confidence: 0.95
edited_by: a00-d41e7dcd
evidence_runs:
  - experiment:a00-d41e7dcd-d7140f
loop: hypothesis:migrate-transcript-copy-survives-sftp-mode-scp@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 07778b6b99148289
season: 2
title: "Test isolation: scp argv test must not mkdir under real ~/.claude/projects"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d41e7dcd-d7140f
# experiment:a00-d41e7dcd-d7140f

## Experiment

TEST HYGIENE for `test_transcript_scp_argv_is_tilde_relative_never_literal_dollar_home`
(`extensions/agi/tests/test_migrate_channel.py`). The EF.35 `~` fix in
`rotate._migrate_copy_transcript` is sound and was NOT touched; only the test's
isolation was fixed.

Defect: the test called the LIVE `rotate._migrate_copy_transcript` without
redirecting `rotate.CC_PROJECTS_DIR` (`rotate.py` L94,
`Path.home() / ".claude" / "projects"`). `_migrate_transcript_dest` ->
`transcript_from_registry_dict` (rotate.py L6734-6747) derives `dest` under the
real home, and `_migrate_copy_transcript` runs
`dest.parent.mkdir(parents=True, exist_ok=True)` (~L20921), creating a REAL
directory under `~/.claude/projects` on every run. The stubbed
`subprocess.run` never stopped the mkdir; the director removed 7 empty
leftovers.

Fix (added hygiene, existing assertions kept intact):

1. `monkeypatch.setattr(rotate, "CC_PROJECTS_DIR", tmp_path / ".claude" / "projects")`
   BEFORE the call. `CC_PROJECTS_DIR` is the module global both the dest
   derivation and (transitively) the mkdir read, so this is the load-bearing
   redirect. The exact-argv assertions are unchanged and still pass:
   `argv[2] == boxA:~/.claude/projects/<slug>/sess-1.jsonl`, ends
   `/sess-1.jsonl`, `$HOME` nowhere in argv. (`dest.parent.name` is the slug,
   which the redirect does not alter.)
2. Positive non-touch assertion: snapshot the real
   `Path.home() / ".claude" / "projects"` top-level entry names before the
   call and assert `_snapshot() == before` after it (None when it does not
   exist). Also `assert str(dest).startswith(str(tmp_path / ".claude" / "projects"))`.

## Evidence

Probe (offline, scratch, no real-home write) showing the redirect is live and
the mkdir follows the global -- run with `rotate.subprocess.run` stubbed and
`rotate.CC_PROJECTS_DIR` pointed at a scratch fake home:

    dest      = /tmp/ef41_probe/fakehome/.claude/projects/-tmp-ef41_probe-fork-wt/sess-1.jsonl
    dest.parent exists = True
    under fakehome = True

So removing the monkeypatch leaves `dest` under `Path.home()` and the
`_snapshot() == before` assertion fails: the new check is non-vacuous.

Test run (the two named files only, never the suite):

    python3 -m pytest extensions/agi/tests/test_migrate_channel.py -q
    35 passed, 2 warnings in 1.08s

    python3 -m pytest extensions/agi/tests/test_rotate*.py -q
    949 passed, 1 xfailed, 1115 warnings in 568.99s (0:09:28)

Live `~/.claude/projects` holds 5 entries before and after; the fixed test adds
none. Production lines changed: 0 (test file only; 22 insertions, 1 deletion in
`test_migrate_channel.py`).

## Agent Notes
Redirect rotate.CC_PROJECTS_DIR to tmp_path and assert real ~/.claude/projects is unchanged; exact scp argv assertions kept. test_migrate_channel.py 35 passed, test_rotate*.py 949 passed 1 xfailed; production lines 0.
