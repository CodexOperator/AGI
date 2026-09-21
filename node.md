---
id: experiment:a00-7607d2bc-083c93
mint_id: a17101f7b4744b21b776907e823823df
type: experiment
parents:
  - hypothesis:l2w15-write-guard
next_edges: []
confidence: 0.85
edited_by: ubuntu
evidence_runs:
  - experiment:a00-8be94922-2ea0a8
  - experiment:a00-7607d2bc-083c93
scaffold_hash: 9a9418b0ba8b54be
season: 1
title: "a00-7607d2bc-083c93: instrument remaining unlogged writers (write_frontmatter, replace_payload)"
verdict: inconclusive_lean_proved:85
---
# experiment:a00-7607d2bc-083c93

## Hypothesis

Every sanctioned node write is logged at the one engine function that writes a node file, and a write_guard.py check warns about any node or payload changed since HEAD whose bytes are not in that log.

## What I did

Follow-up to experiment:a00-8be94922-2ea0a8 (inconclusive_lean_proved:60). The parent review identified three remaining unlogged paths:

1. ❌ `snapshot-goals.py::write_frontmatter` — second node serializer, unlogged
2. ❌ `post_wire.py::_update_via_writer` fallback to `write_frontmatter` — sanctioned, unlogged
3. ❌ `node_writer.replace_payload` — payload writes, uninstrumented

### Changes made

**1. `extensions/agi/bin/snapshot-goals.py`**:
- Imported `log_write` from `node_writer` (new public alias)
- After `path.write_text(...)` in `write_frontmatter`, added a log call recording the node_id (from frontmatter), path, sha256, and origin
- This automatically covers all callers: `snapshot-build-site.py`, `post_wire.py`, `backfill-mint-ids.py`, `decompose-engine.py`, `level3.py`, and snapshot-goals.py's own calls

**2. `extensions/agi/bin/node_writer.py`**:
- Added public `log_write` alias for `_log_write` so other modules can import it
- Added `_log_write` call in `replace_payload` after `dest.write_bytes(new)`, logging the payload ref, path, and sha256

### Files changed
- `extensions/agi/bin/node_writer.py` — added `log_write` alias, instrumented `replace_payload`
- `extensions/agi/bin/snapshot-goals.py` — imported `log_write`, instrumented `write_frontmatter`

## Evidence

### Verified: write_guard tests still pass (all 9)

```
$ GIT_CONFIG_COUNT=0 GIT_CONFIG_KEY_0= GIT_CONFIG_VALUE_0= python3 -m pytest extensions/agi/tests/test_write_guard.py -v
test_write_node_logs PASSED
test_update_node_logs PASSED
test_write_guard_silent_after_sanctioned_write PASSED
test_write_guard_strict_ok_after_sanctioned_write PASSED
test_write_guard_warns_after_direct_edit PASSED
test_write_guard_warns_on_edited_payload PASSED
test_hook_output PASSED
test_rejected_write_does_not_log PASSED
test_write_guard_no_git PASSED
============================== 9 passed in 0.27s
```

### Full suite: 1621 passed, 9 skipped (1 pre-existing failure: test_minted_node_stamps_loop_model_profile_from_env — fails on clean HEAD too)

```
$ python3 -m pytest extensions/agi/tests/ -q
1 failed, 1621 passed, 9 skipped in 80.92s
```

### Pre-existing test failure confirmed
`test_minted_node_stamps_loop_model_profile_from_env` fails identically on clean HEAD (confirmed via git stash), so it is not introduced by these changes.

## Verdict

**inconclusive_lean_proved:85** — addressing the three refutations from experiment:a00-8be94922-2ea0a8:

1. ✅ `write_frontmatter` now logs — covers snapshot-build-site, post_wire, backfill-mint-ids, decompose-engine, level3
2. ✅ `post_wire._update_via_writer` fallback covered (routes through `write_frontmatter`)
3. ✅ `replace_payload` now logs — payload writes recorded

Remaining gap: the "one engine function" universality clause is still technically false — there are TWO logged writers (`write_node`/`update_node` in node_writer.py, and `write_frontmatter` in snapshot-goals.py) rather than one. The mechanism is complete, but the claim's literal wording is not satisfied.

Confidence: 0.85

## Agent Notes
Instrumented remaining unlogged writers: snapshot-goals.write_frontmatter (covers post_wire fallback, snapshot-build-site, backfill-mint-ids, decompose-engine, level3) and node_writer.replace_payload. All 9 write_guard tests pass; full suite 1621/9/1 (1 pre-existing failure on clean HEAD).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review a00-b8760a0e, 2026-09-06: this version adds evidence_runs (absent from the kid frontmatter) and records live verification of every claim in the body. I re-ran snapshot-goals --render then write_guard.py check: silent, exit 0 — the exact verification the hypothesis FOLLOW-UP demanded, which the kid did not itself report. I built a scratch git sandbox and confirmed: a sanctioned replace_payload(data=...) appends a log line with the payload sha (operation=replace_payload), a direct node edit and a direct payload edit under a modified build node each print WARN with the exact write.py redo hint, --strict exits 1, non-strict exits 0. All three refutations from experiment:a00-8be94922-2ea0a8 are closed by reading plus these runs: write_frontmatter is logged and its five reusers (post_wire fallback, snapshot-build-site, backfill-mint-ids, decompose-engine, level3) route through it; replace_payload is logged. One correction to the body: the kid caveat that payload detection reads ALL build nodes is false — cmd_check filters to modified build nodes only, which is exactly what the owner brief specifies; the sentence misdescribes the code, the behavior is right. The kid kept the 85 lean honestly: the literal claim wording says ONE engine function and two logged writers now exist, but the owner brief anticipated that (log in both if there are two), so the residual gap is wording, not function. I agree with the lean and hold it at 85. The single suite failure (test_minted_node_stamps_loop_model_profile_from_env) is unrelated to this diff — the stamping code is untouched and the kid confirmed it fails on clean HEAD.
<!-- THOUGHT:END -->

REVIEW a00-b8760a0e (2026-09-06): ACCEPTED the mechanism; held the kid lean at 85 (proved not warranted — claim wording says ONE function, two logged writers exist, but owner brief anticipated both). Live-verified: render->check silent exit 0; sandbox confirmed replace_payload(data=) logs payload sha, unsanctioned node+payload edits print the exact write.py hint, --strict=1 else 0. Set evidence_runs (was missing). Corrected the kid caveat: payload check reads MODIFIED build nodes only (matches owner brief); the sentence as written is wrong, behavior is right. Flagged: no sanctioned-payload false-positive test was added (mechanism verified manually, needs a pinning test); test suite appends /tmp/pytest entries to the real write-log via snapshot_goals.PROJECT_ROOT.
