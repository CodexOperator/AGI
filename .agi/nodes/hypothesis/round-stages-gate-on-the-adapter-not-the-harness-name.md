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

## CORRECTIVE DH.585 -- closes mur-director-engine-29 DH.568-k1 demote
BASE      CUT FROM season2/loops/hypothesis-round-stages-gate-on--a00-000aa7b3 tip 9c175b3ae (branch de-base-585; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
0. FIRST, MUST CLOSE (paid lane, the chain never merges while open): round-mur.json still resolves provider pi and threads it onto the round parent's argv (the billed lane). Set it to pi-free like round-research-review, and replace the literal asserts (test_workflow_round_manifests.py:265 'pi', the new test's 'pi-free') with ONE assert that EVERY round manifest's provider EQUALS the ladder tier-0 parent row's harness, read from the tmp fixture, never the live graph.
1. 1 · round-mur still resolves the paid pi harness and threads it onto the round-parent argv; the round never mentions round-mur, so the Prime's item 1 is not met tree-wide
2. 2 · the round knowingly leaves a committed test red that its own cell change caused (test_workflow_round_manifests.py:265, `assert harness == "pi"`); pytest -q is a declared verify command
3. 3 · node ledger row 3 claims a verdict reconciliation that is not in the merge (experiment:a00-da20f480-c3438e absent from the diff, still `verdict: proved`)
4. 4 · node ledger row 6 claims a THOUGHT rewrite in a node that is byte-identical across the diff (a00-205b79d3-a08b8e.md:37)
5. 5 · the 'threaded value must EQUAL the ladder row' rule is prose plus one single-manifest test, and is already violated in-tree by round-mur
6. The cell change is WORKFLOW-WIDE, not round-parent-only, and the round never says so: workflow.py:352-356 resolves the manifest `provider` for the whole run, so all six stages of round-research-review moved to pi-free. The node's own probe shows it (a00-205b79d3-a08b8e.md:70-71, `[dispatch] review :: role=kid model=stealth/space-bunny-alpha effort=high`) but the ledger and Agent Notes describe the change as the round parent only. An undisclosed widening of scope with no evidence the free lane was intended for the five review stages. RESIDUE.
7. The new cost assertion makes a tmp-dir unit test read the LIVE graph and hard-code an owner-owned value: test file:272-274 asserts `man['provider'] == row['harness'] == 'pi-free'` against REPO/.agi/nodes and the committed manifest. Any legitimate edit of the tier-0 parent ladder row (ladder.md:43) turns the suite red with no code defect, and the round itself asks for a cell-level test budget in its own findings (item 7). A test should pin the RULE, not the owner's current value. RESIDUE.
8. workflow.py:2204-2205 re-states a config value in code prose (`round-research-review.json` keeps `provider: pi-free`); the invariant is the EQUALITY between the cell and the ladder row, not the literal `pi-free`, so the copy is the part that will drift. config_max RESIDUE.
9. a00-205b79d3-a08b8e.md:10-12 lists experiment:a00-da20f480-c3438e in `evidence_runs` although the round ran nothing against it and that node is byte-identical across the merge (md5 92e72a51…): the evidence list overstates what this round measured. RESIDUE (same root as #3/#4).
10. Ownership template check (fresh, mine): the round's own hypothesis states its claim over BOTH round manifests (round-stages-gate-on-the-adapter-not-the-harness-name.md:10, 'round-mur/round-research-review run under --harness pi-free'), and the round closed it on one; the flow template that authors round manifests (skills/agi-workflow/SKILL.md:36-38) still has no line about the `provider` cell or the ladder equality, which is where an authoring rule belongs. RESIDUE.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_workflow_round_findings_and_seam_refusal.py test_workflow_round_manifests.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/workflow.py · extensions/agi/tests/test_workflow_round_findings_and_seam_refusal.py · extensions/agi/tests/test_workflow_round_manifests.py · extensions/agi/workflows/round-mur.json · extensions/agi/workflows/round-research-review.json · .agi/nodes/experiment/a00-205b79d3-a08b8e.md · .agi/nodes/experiment/a00-da20f480-c3438e.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 9c175b3ae · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.614 -- closes mur-director-engine-34 DH.585-k1 demote
BASE      CUT FROM season2/loops/hypothesis-round-stages-gate-on--a00-eaa8fcfc tip 2b73f2d84 (branch de-base-614; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1 · Ledger row 3 asserts a verdict reconciliation the bytes contradict (a00-205b79d3-a08b8e.md:34 vs a00-da20f480-c3438e.md:21)
2. 3 · The new rule test compares the manifest against a fixture value it chose itself (test_workflow_round_manifests.py:300), so a live-ladder paid-lane regression stays green
3. M1 (demote-class, the first reviewer missed it) — a00-205b79d3-a08b8e.md:86-88 still reads 'A committed test pins it without spawning anything: it reads the live ladder row for (tier 0, parent) and the manifest `provider` and asserts they are the same value, `pi-free`.' That test is DELETED by this very diff (the `man['provider'] == row['harness'] == 'pi-free'` assert and the `import spawn_gate` removed from test_workflow_round_findings_and_seam_refusal.py), and the round's own child node says so at a00-2588e527-e1653e.md:61-72 ('deleted; the file no longer imports spawn_gate at all'). The node the round rewrote still points a reader at a test that does not exist — the same false-reader class as ledger row 3, and the corrective fixed row 6 for exactly this while leaving this line.
4. M2 (residue, and this is where the reviewer's '12 vs 8' actually lives) — a00-2588e527-e1653e.md:248 claims `pytest extensions/agi/tests/test_workflow_round_findings_and_seam_refusal.py -k "seam or admitted or pi_adapter"` -> 12 passed. That filter selects 8 test ids at 2b73f2d84 (4 from the seam refusal × 2 seam × 2 dry_run, 1 named-pi-seam, 1 admitted, 2 pi_adapter), not 12. UNVERIFIED by execution and reported as static collection: the worktree HEAD is 7abfb6460, whose copy of that file differs from 2b73f2d84 by 97 deleted lines, so running it here would measure HEAD, not the reviewed tip. Probe I would run, not run: `git worktree`-free — extract 2b73f2d84's file into a checkout of the same tree and `env -u TMUX -u TMUX_PANE python3 -m pytest <file> -k "seam or admitted or pi_adapter" -q -p no:cacheprovider --collect-only | tail -1`.
5. M3 (residue, one source per rule) — the rule now lives in three prose copies: round-mur.json:7 (added by this diff, ~1.4 kB in a single JSON line), round-research-review.json:7 (pre-existing, the same rule), and workflow.py:2200-2210 (rewritten by this diff to name the equality). No home cell exists: .agi/context/schemas/ has no [workflow].md at 2b73f2d84, and .agi/nodes/.geometry/workflows.md:17-28 owns only the type rows, not the round-manifest provider constraint. The equality belongs in the resolver's docstring plus one schema/geometry constraint, not in three manifest descriptions that no test reads.
6. M4 (note, UNVERIFIED — the widening is argued, not measured) — a00-2588e527-e1653e.md:118-133 justifies moving all five inherited review stages onto pi-free by citing ladder.md:44 (CONFIRMED: tier-0 kid = pi-free) and per-stage role hints, but the only measurement quoted is `_resolve_default_harness` per manifest, which resolves the WHOLE run (workflow.py:349-356), not per stage. Probe I would run, not run: `python3 extensions/agi/bin/workflow.py run round-mur --args '{"target":"hypothesis:x","iteration":"L1.01","rounds":[]}' --dry-run` and compare the per-stage `[dispatch]` lines against the same command with the `provider` cell removed in memory — dry-run only, nothing spawned. Already disclosed as argued in the node, so it is residue, not a hidden claim.
7. NEGATIVE FINDINGS, checked and clean (so the round is not demoted on them): no test in scope touches a real resource — test_workflow_round_findings_and_seam_refusal.py:252 patches _wf.subprocess.run, the ladder fixture is written to tmp_path only (test_workflow_round_manifests.py:276-286), and the spawn_gate import removal is clean (no remaining reference in that file, grep rc=1). No deletion under .agi/nodes. The round did not edit the gate it passes through: workflow.py changed 9/4 and only inside the _run_round_stage docstring (:2199-2210); the adapter gate itself is untouched.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_workflow_round_findings_and_seam_refusal.py test_workflow_round_manifests.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/workflow.py · extensions/agi/tests/test_workflow_round_findings_and_seam_refusal.py · extensions/agi/tests/test_workflow_round_manifests.py · extensions/agi/workflows/round-mur.json · .agi/nodes/experiment/a00-205b79d3-a08b8e.md · .agi/nodes/experiment/a00-2588e527-e1653e.md · .agi/nodes/experiment/a00-da20f480-c3438e.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 2b73f2d84 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.631 -- lands DH.614's two node edits its round left UNLOGGED (never hand-landed, TMM.268)
BASE      CUT FROM season2/loops/hypothesis-round-stages-gate-on--a00-8a82adaf tip ace2a3f5a (branch de-base-631). No merge. Never rebase.
NOTE      DH.614's kid edited two experiment nodes with no write-log entry; the parent exited leaving them uncommitted in worktree .agi/worktrees/a00-8a82adaf. Read them with: git -C .agi/worktrees/a00-8a82adaf diff -- .agi/nodes/experiment/a00-205b79d3-a08b8e.md .agi/nodes/experiment/a00-2588e527-e1653e.md (READ ONLY: never write, stage or commit in that worktree).
1. Re-apply the a00-205b79d3-a08b8e.md hunks (row 3 STRIKE (DH.614) + the rewritten committed-test paragraph) THROUGH write.py on this branch; for each claim the hunk makes, re-run the command it names and paste the output (never type a number).
2. Re-apply the a00-2588e527-e1653e.md section "6b · the widening is now MEASURED (DH.614, a00-ee817424)" THROUGH write.py; re-run its dry-run measurement here and paste this branch's output, not the copied one.
3. Paste git -C <this worktree> status -s (empty) and git log --oneline -3 on your node after the commit.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_workflow_round_manifests.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE .agi/nodes/experiment/a00-205b79d3-a08b8e.md · .agi/nodes/experiment/a00-2588e527-e1653e.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · 0 production lines · 0 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.631: mur-director-engine-35 DH.614-harvest residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
