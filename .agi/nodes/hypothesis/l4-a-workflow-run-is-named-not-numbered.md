---
id: hypothesis:l4-a-workflow-run-is-named-not-numbered
mint_id: ac7249ce82be4b7c9aa8479246fe660e
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 25fa7be9c3391147
season: 2
spawn_check: unverified
spawn_check_reason: "parent id(s) resolve to no node: ['build:bin-workflow']"
testable_claim: "OWNER 2026-09-11 18:1xZ (via prime XI, verbatim): 'consolidate g15.19 + g15.20 into a wave or two and hand off to sanctuary-director'. Minted by sanctuary-director 163547Z 18:2xZ from the prime's WAVE 1 order; the prime's measurement is the claim's mechanism. OWNER 18:1xZ: 'make sure workflow IDs are more descriptive instead of random letters, easy to type, fewer tokens'. CLAIM: (1) `workflow.py run` mints a descriptive run KEY from the type + args (merge-up review of merge-up 39 = mur-39; of SL1#2 = mur-sl1-2; author/validate keep their names), prints it FIRST, records the harness run id (wf_xxxx) BESIDE it in the tracked run; `workflow.py list`/`status` resolve the key; every handoff/note/dm cites the key, never wf_xxxx (the harness id stays harness-minted; we stop typing it); a key collision appends -2, -3. (2) PRIME XI g15 line 18:2xZ, same file: `workflow.py author`, re-authoring an EXISTING manifest, DROPS the type cell and REPLACES description with the --note text (measured re-authoring merge-up-review: validate went 7 -> 8 violations; restored by hand at 07bae9ea8) — fix = carry type + description through and APPEND the note; test on a fixture manifest. TESTS: key minting for the three shapes, list/status by key, the author round-trip on a fixture manifest keeping type + description with the note appended. FALSIFIER: a run whose key is not derivable from its type + args, or an author re-run that loses type/description. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/workflow.py + extensions/agi/tests/test_workflow*.py. EXCLUDED: config:workflows (prime-owned), every other file."
title: "A workflow run is named, not numbered: workflow.py mints a descriptive run key from type + args (mur-39), prints it first, keeps the harness id beside it; author re-authoring keeps type + description and appends the note"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-workflow-run-is-named-not-numbered

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
HARVEST L4.282 (sanctuary-director 182119Z, 2026-09-11 18:37:20Z): merged a00-47db504f (1 kid a00-90c8724a; parent held 85 lean-proved). Real tree on the merged bytes: `workflow.py run merge-up-review --args '{"n":39}' --dry-run` prints `[run-key] mur-39` as its FIRST line, before any [dispatch] line; `workflow.py list` unchanged (7 workflows); `status mur-39` says no runs match because a dry-run tracks nothing (expected — the tests pin the tracked path: 44 passed under env -u TMUX). The six deleted lines are the _track_run signature + the author description overwrite, nothing global. RESIDUE, accepted as the parent found it: the claim's 'records the harness wf_… id beside it' is unmet because workflow.py mints no harness id — the `wf_` ids the prime cites (wf_ba530baa-dab) are minted by the claude-code harness when IT runs the .js script. FIX-ONLY (queued behind L4.283, not re-dispatched now): on the claude-code harness path capture the `wf_` id from the harness output when one appears and record it beside run_key; `-` when the harness mints none (pi). Everything else in the claim is landed and verified — a fix-only kid re-derives none of it.
