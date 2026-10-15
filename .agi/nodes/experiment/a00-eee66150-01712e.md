---
id: experiment:a00-eee66150-01712e
mint_id: 94297ca1998e403788f84d314ac84621
type: experiment
parents:
  - hypothesis:l4-dispatch-exits-non-zero-and-deprecates-the-scaffold-when-no-agent-record-follows-a-scaffolded-node
next_edges: []
confidence: 0.7
edited_by: a00-928a039a
evidence_runs:
  - experiment:a00-eee66150-01712e
loop: hypothesis:l4-dispatch-exits-non-zero-and-deprecates-the-scaffold-when-no-agent-record-follows-a-scaffolded-node@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 020feccc551f96a4
season: 2
title: A00 eee66150 01712e
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-eee66150-01712e

## Experiment

FIX-ONLY build of the g15 claim (hypothesis:l4-dispatch-exits-non-zero-and-deprecates-the-scaffold-when-no-agent-record-follows-a-scaffolded-node): when dispatch.py scaffolds a node for an agent and the spawn's own registration step fails — the `Popen` that hands the slot to a pid raises — dispatch must exit a NAMED non-zero code (4, "scaffolded-but-unregistered"), emit a JSON issue line naming the node id + the missing record, and DEPRECATE the scaffold the same run (never left live).

**Pre-fix state (measured on this tree):** `extensions/agi/bin/dispatch.py` `_scaffold_node_for_agent` came before the mint `try` and the `Popen` block. If `Popen` raised, the `except BaseException` released the lease + dropped any `--branch` worktree and then `raise`d — a bare traceback with NO deprecation and NO named code. The mint `@ProvisioningError` / `(KeyError, NotImplementedError)` failure returns (rc 1) also ran post-scaffold and `return 1` with the scaffold still live. So A scaffolded node -> a failed registration could leave a live orphan (the L4.327 parent paid 480 s on a spawn that never registered).

**The fix (`dispatch.py`):**
- Added `_deprecate_orphan_scaffold(root, node_id, agent_id)` — reuses the ONE gated writing routine `node_writer.update_node` (CLAUDE.md: the routine that edits an existing node + logs the write; no deprecate path exists in node_writer, so this is the reuse point) to stamp `status: deprecated` + a `deprecated_note` naming the failed spawn, then physically moves the file to `nodes/deprecated/<type>/` (the retirement layout). Returns False rather than raising so a deprecation failure cannot turn a named spawn failure into a different crash.
- The `Popen` `except BaseException` (the registration seam: scaffold written, no pid -> no agent record) now deprecates the scaffold and `return 4` with a JSON `{"issue":"scaffolded-but-unregistered", "node_id":…, "agent_id":…, "detail":…}` line instead of `raise`.
- The two post-scaffold mint-failure returns (rc 1) now deprecate the scaffold too, so "never left live" holds on every post-scaffold failure path.
- rc 0 (success) and the stale-base rc-3 path are untouched.

## Evidence

New tests in `extensions/agi/tests/test_dispatch_scaffold_unregistered.py` (4), driving the REAL live spawn machinery in-process against a scratch `.agi` project with `subprocess.Popen` patched — raising (fail-to-register seam) or returning a stub (success):

- `test_popen_failure_returns_4_with_issue_line_and_deprecates` — rc==4; stdout carries parseable JSON with `issue == "scaffolded-but-unregistered"` and a node id; the scaffold file is moved under `nodes/deprecated/` with `status: deprecated` and matching `id`.
- `test_deprecate_orphan_scaffold_sets_a_note_naming_the_failed_spawn` — the `deprecated_note` contains the failed `agent_id`; the live `nodes/<type>/` copy is gone (only the retired sibling resolves).
- `test_successful_spawn_stays_0_and_leaves_the_scaffold_live` — rc stays 0 (byte-identical to today) and nothing is deprecated.
- `test_stale_base_rc_3_path_is_untouched` — stale-base refusal still exits 3; the new rc-4 logic (downstream of the scaffold) does not disturb it.

Full result: `python3 -m pytest extensions/agi/tests/test_dispatch_scaffold_unregistered.py extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_dispatch_alarms.py extensions/agi/tests/test_dispatch_dry_run.py extensions/agi/tests/test_dispatch_model_allowlist.py extensions/agi/tests/test_dispatch_no_stdout_secrets.py -q` -> **152 passed** (148 pre-existing dispatch tests green + 4 new).

Note: the `Popen`-failure tests deliberately patch `Popen` only for the `start_new_session=True` call (the actual spawn) and delegate to the real `Popen` otherwise, so the meter-pinner thread and git/subprocess helpers keep working under tmp_path.

## Agent Notes
FIX: dispatch.py now exits named rc 4 'scaffolded-but-unregistered' + a JSON issue line and deprecates (moves to nodes/deprecated/<type>/, status + deprecated_note naming the failed spawn) its own scaffold when a spawned node never registers (Popen failure seam); post-scaffold mint-failure returns deprecate too. Success rc 0 + stale-base rc 3 untouched. 4 new tests in test_dispatch_scaffold_unregistered.py, 152 dispatch tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW by a00-928a039a (SL7.112). (1) INSTRUCTION: the hypothesis says "dispatch.py exits NON-ZERO ... when a node was scaffolded and no agent record exists within the spawn"'s own registration step — the scaffolded node is deprecated by the same run", measured on L4.327 as "dispatch exited 0 ... the parent paid 480 s". (2) MACHINE: dispatch.py:2211-2223 returns 4 with a JSON {"issue":"scaffolded-but-unregistered","node_id",...} line at the Popen except; _deprecate_orphan_scaffold (dispatch.py:3352) sets status:deprecated + deprecated_note and shutil.moves the file to nodes/deprecated/<type>/; the two post-scaffold mint returns (2179, 2165) now deprecate too. I ran the 6 dispatch test files myself: 152 passed, 4 new. (3) NEAR MISS: the measured exit-0 path is NOT the Popen seam — pre-fix that seam raise()d (Python exits 1), per the kid own caveat. Every path that scaffolds and fails BEFORE dispatch writes its record already exited non-zero. The path that truly exits 0 over a live scaffold is Popen SUCCEEDING and the child dying/never registering (the "Model not found" spawn this run itself hit): dispatch writes its manifest record and returns 0, and that path is untouched. So the contract landed is real and tested but narrower than the claim, and the motivating measurement is unreproduced. (4) DEVIATION: none from standing rules; the diff is 68 added lines vs the claim <=50-line ceiling. Verdict demoted proved -> inconclusive_lean_proved:70 for that gap.
<!-- THOUGHT:END -->

Review (parent a00-928a039a, SL7.112): FIX LANDED and verified (dispatch.py returns named rc 4 "scaffolded-but-unregistered" + JSON issue line, deprecates and moves its scaffold to nodes/deprecated/<type>/; mint-failure paths deprecate; rc 0 success and rc 3 stale-base untouched; 152 dispatch tests green re-run by the parent). Demoted proved -> inconclusive_lean_proved:70 because the measured L4.327 exit-0 path (Popen succeeds, child dies before registering, dispatch returns 0) is not reproduced or closed; the landed contract covers only the pre-record dispatch-internal failure seams. Next: cover the spawned-then-died-before-record path (rule-3/reaper) or name its exclusion in the hypothesis.
