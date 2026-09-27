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

## CORRECTIVE DH.568 -- closes mur-director-engine-26 DH.551-k1 demote
BASE      CUT FROM season2/loops/hypothesis-round-stages-gate-on--a00-9d1f795c tip e97ef01cb (branch de-base-568; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. FIRST, MUST CLOSE (a paid-lane regression, the round never merges while open): COST DIRECTION of the fix, undisclosed anywhere: threading the admitted row onto argv (workflow.py:2205-2206) makes an explicit --harness BEAT a ladder row naming a different harness (dispatch.py:2058-2074, with the notice printed at :2072), and the live ladder row for the round parent's (tier 0, parent) is pi-free (.agi/nodes/.geometry/ladder.md:43). So any round whose harness resolves to `pi` now forces the detached parent onto the PAID pi harness, where the pre-fix code let the ladder's free pi-free row win (explicit_harness=False path, dispatch.py:2058-2065). The branch's round-research-review.json:5 keeps `provider: "pi"`, and provider IS the default harness when no --harness is passed (workflow.py:351-356; no config row and no geometry per-workflow override exists for round-research-review) - so the item-4 merge resolution is cost-load-bearing, not merely wording. UNVERIFIED live impact: I did not run a round (that would dispatch a real parent). The probe I WOULD run, on a copied manifest, never this tree: `workflow.py run round-research-review --harness pi --dry-run` to read the resolved harness, and a dispatch.py argv capture showing the ladder-override notice. -- the fix leaves every round parent on the ladder tier-0 0-USD row (pi-free): prefer the config cell (round-research-review.json provider) over code; a committed test pins the resolved parent harness == pi-free without spawning.
2. 1. CEILING breach: 93 test lines against a hard 40-line cap (test_workflow_round_findings_and_seam_refusal.py:240)
3. 2. Verdict bookkeeping: frontmatter verdict: proved vs the node's own PARENT REVIEW inconclusive_lean_proved:80 (a00-da20f480-c3438e.md:16)
4. 3. Docstring near-miss unsupported by the bytes (workflow.py:2195) - 'the dry-run print had --harness' but no such print exists
5. 4. Negative test leaves a real-process path open (test_workflow_round_findings_and_seam_refusal.py:309)
6. The false near-miss story has a SECOND and a THIRD durable site the first reviewer did not cite: the node's own THOUGHT (a00-da20f480-c3438e.md:125, 'the dry-run print already carried --harness before this round') and the new test's own docstring (test:275, 'never a printed dry-run line'). Both are permanent graph/test text resting on a print that exists nowhere in base or tip; correcting only workflow.py:2195 leaves the false claim in the memory.
7. The <= 40 test-line cap the round breached has NO home cell: .agi/context/schemas/[hypothesis].md:49 (the CEILING template line) names only 'kids / 10-12 production lines per conjunct / pi parents / a USD cap'. A per-round budget that lives only in brief prose is a template-max candidate for the brief's author; a cap that no template line carries is also why it had to be quoted onto the node twice.
8. Merge context the first reviewer did not state, which changes the risk picture: 'git merge-tree' shows exactly TWO conflict hunks in the entire merge of this branch into local-maxxing/season2/main (workflow.py's adapter gate, round-research-review.json's provider+description). .agi/config.json, GOALS.md, skills/agi-verify/SKILL.md are 'changed in both' but auto-merge with zero conflict markers, and the test file merges clean. The merge is therefore cheap; only the two named resolutions need judgement.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_workflow_round_findings_and_seam_refusal.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/workflow.py · extensions/agi/tests/test_workflow_round_findings_and_seam_refusal.py · extensions/agi/workflows/round-research-review.json · .agi/nodes/experiment/a00-da20f480-c3438e.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over e97ef01cb · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.568: mur-director-engine-26 DH.551-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
