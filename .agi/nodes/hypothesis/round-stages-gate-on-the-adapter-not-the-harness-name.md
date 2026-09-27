---
id: hypothesis:round-stages-gate-on-the-adapter-not-the-harness-name
mint_id: 302bbb6500a5433fbd5618b54e9f485a
type: hypothesis
parents:
  - goal:g1.26
next_edges: []
edited_by: director-engine
scaffold_hash: b2723fffc940da7a
season: 2
testable_claim: round-mur/round-research-review run under --harness pi-free; a claude-code seam still refuses by name; the gate reads harnesses.<h>.adapter; a test fails on 6c403aeb4b
title: "A kind:round stage is gated on the harness ADAPTER cell, not the name pi (assigned: director-engine)"
town: core
---
# hypothesis:round-stages-gate-on-the-adapter-not-the-harness-name

# hypothesis: A kind:round stage is gated on the harness ADAPTER cell, not the name pi (assigned: director-engine)

## Why this exists
**Parent `goal:g1`** (PASS residues; g15 -> g20 -> g1). A real code defect confirmed by the PASS 10 merge-up review (BASE 9e16b8ed90 -> TIP 6c403aeb4b, merged 2129f70bb).

## Measured
workflow.py:2417 (range :2409-2421) `if harness != "pi"` refuses every kind:round stage with rc 6 for --harness pi-free / pi-local although harnesses.<h>.adapter = pi runs the identical _run_round_stage path (PASS 10 c3 verify missed[], c10 template_max YES)

## Testable claim
round-mur/round-research-review run under --harness pi-free; a claude-code seam still refuses by name; the gate reads harnesses.<h>.adapter; a test fails on 6c403aeb4b

## CORRECTIVE DH.551 -- closes mur-director-engine-23 DH.512-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-round-stages-gate-on--a00-256e7631 tip 577a6ab6d (branch de-base-551; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. The round's dispatch ignores the harness the gate just admitted (workflow.py:2191 spawns dispatch.py with no --harness, so the parent always uses spawn.harness)
2. 2. The merge target already carries a second, divergent copy of this gate with no falsifier; git merge-tree reports CONFLICT in workflow.py and round-research-review.json
3. No new demote-severity defect found beyond the two residues re-derived above; the falsifier, the claude_code refusal, the pi-free/pi-local admission and the real-manifest dry runs all reproduce on the tip bytes.
4. MERGE-RESOLUTION REQUIREMENT (missed as an instruction, not just a conflict): the tip's round-research-review.json description edit collides with 56c1156ab, which already changed that manifest's provider/harness pi -> pi-free. Resolving the conflict by taking the tip's side wholesale would re-state a harness requirement on a manifest the target already moved to pi-free; the merged description must keep the target's pi-free resolution AND the adapter phrasing.
5. SCOPE: the round edited extensions/agi/workflows/round-mur.json and round-research-review.json (description strings only) outside the parent's stated FILE SCOPE; disclosed in the node and in the parent's note, and in this repo manifests are hand-edited artifacts, so it is a named deviation rather than an unsanctioned write.
6. UNVERIFIED (not run, per the no-whole-suite / no-own-probe constraint): the node's '154 passed, 2 skipped' over three test files — I ran only the two single committed test files (10 passed and 23 passed/2 skipped).
7. UNVERIFIED (not run): the parent's P1/P2/P3 probes (a harness NAMED pi with adapter claude_code must still refuse rc 6). No committed test covers that conjunct. The probe I WOULD run, and did not: a read-only call to workflow.run_workflow with a fixture config declaring harnesses.pi = {adapter: 'claude_code', models: {...}} and a manifest carrying one kind=round stage, with _run_round_stage, _run_stage_pi, _load_manifest, _load_config, _repo_root, _mint_run_key, _track_run and _claude_code_seam_present monkeypatched, asserting rc == 6. Mechanism evidence only: the gate at workflow.py:2437 reads harness_cfg.get('adapter') and never consults the name, so the conjunct is satisfied by construction.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_workflow_round_findings_and_seam_refusal.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_workflow_round_findings_and_seam_refusal.py · extensions/agi/workflows/round-mur.json · extensions/agi/workflows/round-research-review.json · .agi/nodes/experiment/a00-50e8cf71-343d6c.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 577a6ab6d · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.551: mur-director-engine-23 DH.512-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
