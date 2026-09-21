---
id: experiment:a00-4d4910df-28be66
mint_id: aeaac8057bd94f0881e05653a75f798a
type: experiment
parents:
  - hypothesis:l2w15-write-guard
next_edges: []
confidence: 0.9
edited_by: ubuntu
evidence_runs:
  - experiment:a00-4d4910df-28be66
scaffold_hash: d986cf55d3427ff2
season: 1
title: "a00-4d4910df-28be66: log ensure_payload, filter .lock files, add pinning tests"
verdict: inconclusive_lean_proved:90
---
# experiment:a00-4d4910df-28be66

## Hypothesis

Every sanctioned node write is logged at the one engine function that writes a node file, and a write_guard.py check warns about any node or payload changed since HEAD whose bytes are not in that log.

## Experiment

Targeted the two remaining sanctioned-path gaps identified by parent review a00-554cbcdf (experiment:a00-e334f78a-bfc1e6):

### Gap 1: `ensure_payload` unlogged (write.py create --payload false-positive)

`node_writer.ensure_payload` (L448) creates an empty payload file with no log entry. `write_guard.py check` then flags this just-created payload as an unsanctioned write with a bogus `write.py payload` hint — a false positive on a sanctioned creation.

**Fix**: Added `_log_write(root, "ensure_payload", ...)` after `src.write_text("")` in `ensure_payload`, with explicit sha256 of the empty bytes since the text parameter is empty.

```
src.write_text("")
_log_write(root, "ensure_payload", ref, src,
           text="",
           extra={"sha256": hashlib.sha256(b"").hexdigest(),
                   "payload_ref": ref, "location": str(location)})
```

### Gap 2: `.lock` files from `_claim_node` flagged by the guard

`cli.py._claim_node` creates `<nodefile>.lock` files via `open(lock_file, "a")` for `fcntl.flock` inter-process mutual exclusion. These `.lock` files persist on disk and appear as untracked files under `.agi/nodes/`, causing `write_guard.py check` to print a WARN with a bogus `write.py <slug>.lock` hint.

**Fix**: Added a `.lock` suffix filter in `write_guard._git_changed_files`:

```python
if f.suffix == ".lock":
    continue
```

### Gap 3: Missing pinning tests

Added 3 new tests (total now 12):

| Test | What it covers |
|---|---|
| `test_ensure_payload_logs` | ensure_payload creates a log entry with operation=ensure_payload, correct payload_ref, and non-empty sha256 |
| `test_write_guard_silent_after_ensure_payload` | after ensure_payload + commit + write_node (build node with payload_ref), check is silent even under --strict — closes the sanctioned-payload false-positive gap |
| `test_write_guard_ignores_lock_files` | .lock file under nodes/ is not flagged; node edits are still detected |

### Verification

```
$ python3 -m pytest extensions/agi/tests/test_write_guard.py -v
12 passed in 0.52s
```

All 9 old tests still pass. All 3 new tests pass.

```
$ python3 -m pytest extensions/agi/tests/ -q --ignore=extensions/agi/tests/test_telemetry_rollup.py
2 failed, 1634 passed, 9 skipped in 85.50s
```

Failures are pre-existing/unrelated:
- `test_minted_node_stamps_loop_model_profile_from_env` — fails on clean HEAD
- `test_help_smoke[telemetry_rollup.py]` — other agent introduced syntax error in telemetry_rollup.py (triple-quote became quadruple-quote, reported but left untouched)

### Files changed

- `extensions/agi/bin/node_writer.py` — added `_log_write` call in `ensure_payload`
- `extensions/agi/bin/write_guard.py` — added `.lock` suffix filter in `_git_changed_files`
- `extensions/agi/tests/test_write_guard.py` — added 3 new tests (12 total)

## Evidence

### New test: ensure_payload logs

```
test_ensure_payload_logs ...
    entry["operation"] == "ensure_payload"  ✅
    entry["payload_ref"] == "ext/test/payload.sh"  ✅
    entry["sha256"]  # non-empty  ✅
```

### New test: check silent after ensure_payload

```
test_write_guard_silent_after_ensure_payload ...
    check (non-strict): exit 0  ✅
    check --strict: exit 0  ✅  # closes the sanctioned-payload false-positive
```

### New test: .lock files ignored

```
test_write_guard_ignores_lock_files ...
    .lock file: check exit 0  ✅
    .lock file: check --strict exit 0  ✅
    node edit WITH lock: --strict exit 1  ✅  # node monitoring still works
```

### Existing test suite (excluding broken telemetry_rollup)

```
1634 passed, 9 skipped, 2 failed
  (both failures pre-existing/unrelated)
```

## Verdict

**inconclusive_lean_proved:90** — closes the two remaining sanctioned-path gaps (ensure_payload logging, .lock filtering) and adds the pinning tests. The mechanism is now complete: every sanctioned write path (write_node, update_node, write_frontmatter, replace_payload, ensure_payload, claim_node) is logged; the guard correctly warns about unsanctioned node/payload edits while ignoring .lock files. The literal "one engine function" wording is still technically unmet (6 logged paths across 2 modules), but the owner brief anticipated logging in multiple locations. Confidence: 0.90.

## Agent Notes
Logged ensure_payload (node_writer.py), filtered .lock files in write_guard.py (_git_changed_files), added 3 pinning tests (12 total). Closes two sanctioned-path gaps from L2.12 review. Finds: other-agent syntax error in telemetry_rollup.py (pre-existing mod).

Parent review a00-0a4812a4 (L2.13): accepted as-is. Verified in code: ensure_payload log call present (node_writer.py, sha256 of empty bytes via extra), .lock suffix filter in write_guard._git_changed_files, 12/12 guard tests pass live, write_guard check silent on tree. Two items remain open for a later kid: (1) no explicit claim-path test (claim then check silent on node+lock) — claim uses flock, noted hard to isolate; (2) L2.03 item still open: test suite appending to the real write-log via snapshot_goals.PROJECT_ROOT. Suite is 2 red but both are not this kid: pre-existing env-stamp failure on clean HEAD, and another agent quadruple-quoted telemetry_rollup.py (correctly left untouched and reported).
