---
id: experiment:a00-53477bf6-62cfff
mint_id: d5f29a1300954c3e8be6483612f35ddb
type: experiment
parents:
  - hypothesis:l4-dispatch-exits-non-zero-and-deprecates-the-scaffold-when-no-agent-record-follows-a-scaffolded-node
confidence: 0.9
edited_by: a00-928a039a
evidence_runs:
  - experiment:a00-53477bf6-62cfff
scaffold_hash: df81c4b2901b8833
title: A00 53477bf6 62cfff
verdict: proved
---
# experiment:a00-53477bf6-62cfff

## Experiment

Closed the parent's conjunct (2) gap: the JSON issue line that named the node
id + missing record existed only at the Popen (rc 4) seam. The two earlier
post-scaffold failure seams — `provisioning.ProvisioningError` (mint failure)
and `(KeyError, NotImplementedError)` (config error: missing model /
unimplemented harness) — deprecated the scaffold but exited 1 with only a
plain `ERR:` stderr line and no JSON naming the node.

Landing (dispatch.py):
- Added ONE shared reporter `_report_unregistered_scaffold(root,
  scaffold_info, agent_id, detail=None)` right after
  `_deprecate_orphan_scaffold`. It deprecates the orphan (never left live)
  and emits the single `{"issue": "scaffolded-but-unregistered", "node_id",
  "agent_id", "detail"}` shape. Returns None when no scaffold was written;
  never raises. All three seams now route through it, so one JSON shape is
  guaranteed by construction.
- `provisioning.ProvisioningError` seam (rc 1): now calls the helper with
  `detail="could not mint a credential: {exc}"` before returning 1.
- `(KeyError, NotImplementedError)` seam (rc 1): now calls the helper with
  `detail="harness ... cannot spawn tier ...: {exc}"` before returning 1.
- Popen seam (rc 4): the inline dict was replaced by the same helper call;
  behaviour identical, shape identical.
- rc values unchanged (1 at the two config seams, 4 at Popen), success rc 0
  and stale-base rc 3 untouched.

2 new tests in test_dispatch_scaffold_unregistered.py (both dt through the
real dispatch seams against the scratch .agi fixture):
- test_mint_failure_returns_1_with_issue_line_and_deprecates — forces the
  provisioning path live (`dispatch.provisioning.available` -> True) and
  patches `provisioning.mint` to raise `ProvisioningError`. Asserts rc 1, the
  JSON issue line parses, names node id + agent_id, names "credential" in
  detail, and the scaffold is deprecated.
- test_build_command_keyerror_returns_1_with_issue_line_and_deprecates —
  patches the pi adapter's `build_command` to raise `KeyError("no model for
  tier")`. Asserts rc 1, the JSON issue line parses and names the node id,
  and the scaffold is deprecated.

## Evidence

`python3 -m pytest extensions/agi/tests/test_dispatch_scaffold_unregistered.py -q`
→ 6 passed (4 prior + 2 new).

Broader dispatch suite, all green:
- test_dispatch.py + test_dispatch_alarms.py + ..._scaffold_unregistered.py
  → 119 passed
- test_dispatch_dry_run.py + test_dispatch_model_allowlist.py +
  test_dispatch_no_stdout_secrets.py → 35 passed

Success rc-0 and stale-base rc-3 paths verified untouched by the existing
golden tests (test_successful_spawn_stays_0_and_leaves_the_scaffold_live,
test_stale_base_rc_3_path_is_untouched), which still pass.

## Agent Notes

Three seams, one JSON shape, one helper name. The detail field is the only
thing that varies and it says exactly what was missing: the credential at the
mint seam, the model/harness config at the KeyError seam, the agent record
itself at the Popen seam. rc codes kept as the parent instructed (1/1/4).
<!-- BODY:END -->

## Agent Notes
All three post-scaffold failure seams now emit ONE shared scaffolded-but-unregistered JSON line via _report_unregistered_scaffold; added 2 tests for mint-failure and build_command-KeyError seams; 154 dispatch tests green, success rc0 and stale-base rc3 untouched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW by a00-928a039a (SL7.112). (1) INSTRUCTION: parent brief to this kid — "On BOTH post-scaffold failure returns (ProvisioningError; KeyError/NotImplementedError), emit the SAME named JSON issue line shape naming node_id + agent_id + the missing record. Prefer ONE helper so the three seams share one JSON shape." (2) MACHINE: dispatch.py:3388 `_report_unregistered_scaffold` is called at :2169 (ProvisioningError, rc 1), :2185 (KeyError/NotImplementedError, rc 1) and :2218 (Popen, rc 4); it delegates deprecation to `_deprecate_orphan_scaffold` (:3352) and prints the one {"issue":"scaffolded-but-unregistered","node_id","agent_id","detail"} shape. I ran all six dispatch test files myself: 154 passed (2 new tests drive a real mint failure and a real build_command KeyError). (3) NEAR MISS: two seams each printing their own dict would satisfy "a JSON line" while letting the shapes drift; routing all three through one reporter is what makes the shape identical by construction. (4) DEVIATION: none. Accepted proved for conjunct (2); the architectural gap (Popen succeeds, child dies before registering, dispatch returns 0) stays recorded as out of scope on experiment:a00-eee66150-01712e.
<!-- THOUGHT:END -->
