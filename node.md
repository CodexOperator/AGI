---
id: experiment:a00-508820d2-b37c0e
mint_id: 814a251466b04d1cbbf6dc44536cc7ec
type: experiment
parents:
  - hypothesis:l3-write-payload-unchanged-unlogged
next_edges: []
confidence: 0.9
edited_by: a00-bc10a761
evidence_runs:
  - experiment:a00-508820d2-b37c0e
loop: hypothesis:l3-write-payload-unchanged-unlogged@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: df276449f5bb4d86
season: 2
title: A00 508820d2 b37c0e
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-508820d2-b37c0e

## Experiment

Tested `hypothesis:l3-write-payload-unchanged-unlogged`: an explicit
`write.py <build-id> "payload <same path>"` on a payload whose bytes are
UNCHANGED must still record a write-log sanction entry carrying the node's
`mint_id` and the payload `sha256`, clearing write_guard — the L3.27 defect
where 5 identical re-logs left 5 WARNs because `replace_payload` returned
with no log entry when bytes matched.

**Red first.** Added
`test_write_guard_silent_after_same_bytes_payload_relog` to
`extensions/agi/tests/test_write_guard.py`:
- build an mvp node with a payload (`payload_ref`/`link_ref`/`location`),
  git-commit baseline;
- kid writes payload bytes AND the node file directly (unsanctioned);
- assert write_guard `--strict` warns (rc 1);
- `write.submit(..., payload_from=<same file>)` — bytes unchanged;
- assert write_guard now silent (rc 0) and the newest `replace_payload` log
  entry carries `mint_id == <node frontmatter mint_id>` and a non-empty
  `sha256`.

Before the fix this failed: `payload_entries[-1]` IndexError — NO
`replace_payload` entry existed after a same-bytes re-log, exactly L3.27's
"changed skip".

**Fix (two files):**

1. `extensions/agi/bin/node_writer.py` — `replace_payload` gained a
   `mint_id` param. The unchanged-bytes branch now calls `_log_write(...
   "replace_payload" ... mint_id=..., "changed": False)` instead of returning
   bare. The changed branch now also passes `mint_id` (was previously empty;
   the guard's sha256-only fallback masked it — this makes the payload log
   honest). Still returns `(dest, False)` so the CLI's `unchanged` message and
   `res.payload_changed` semantics are untouched.

2. `extensions/agi/bin/write.py` — `submit()` now resolves the target node's
   `mint_id` via a new read-only `_node_mint_id()` helper and threads it into
   `replace_payload`. Reading frontmatter only; no file write, so
   `test_edit_py_contains_no_file_write` still holds.

No `update_node` (node-body) entry is added by this path — only the
`replace_payload` payload-write entry — so the node-body update log is
unchanged, as the hypothesis required.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_write_guard.py::test_write_guard_silent_after_same_bytes_payload_relog -q
BEFORE fix: FAILED 1 failed   (IndexError: list index out of range — no
                               replace_payload entry after same-bytes re-log)
AFTER  fix: . [100%] 1 passed

$ python3 -m pytest extensions/agi/tests/ -q
1935 passed, 1 skipped, 1 failed in 109.49s
  (the 1 failure: tests/test_seat_status.py — pre-existing, unrelated:
   literal `assert "rollup" in human` vs the code's "roll-up", plus an
   environment `ModuleNotFoundError: No module named 'frontmatter'` in the
   captured stderr. Touch nothing in write.py/node_writer.py.)
```

The new test asserts, after a same-bytes re-log:
- `res.payload_changed is False` (it is still a no-op write);
- newest log entry `operation == "replace_payload"`;
- `entry["mint_id"] == node frontmatter mint_id`;
- `entry["sha256"]` non-empty;
- `write_guard check --strict` returns 0 (silent).

All four hold after the fix and the first three fail on the un-fixed code.

## Agent Notes
Same-bytes payload re-log is now a sanction: replace_payload logs (mint_id, sha256) even on unchanged bytes (added mint_id param, threaded from write.py submit). Red-first test wrote+passed. write_guard --strict silent after re-log; node-body update log unchanged. Repo suite 1935 passed; 1 pre-existing unrelated seat_status failure (rollup/roll-up literal + missing frontmatter module on box).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Red-first: test_write_guard_silent_after_same_bytes_payload_relog reproduced the L3.27 same-bytes skip (IndexError — no replace_payload entry) and fails on un-fixed code. Fix reviewed and confirmed: replace_payload gains mint_id param and logs (mint_id, sha256, changed:False) on the unchanged branch; write.py submit threads the real mint_id via read-only _node_mint_id (no file write, invariant holds). Parent re-ran the new test independently: passes. Node-body update log untouched as claimed. Verdict proved accepted — evidence_runs names this experiment, which is the run.
<!-- THOUGHT:END -->

Parent review (a00-bc10a761, L3.28): artifact read, fix verified in node_writer.py L456-513, new guard test re-run independently and passes. Red-first claim accepted (test asserts replace_payload entry absent pre-fix). 1 pre-existing unrelated failure (test_seat_status.py) noted as caveat, not blocking. Verdict proved upheld.

## Agent Notes
Same-bytes payload re-log is now a write-log sanction (write.py payload verb); red-first guard test added; verdict proved upheld after parent re-run of the test.
