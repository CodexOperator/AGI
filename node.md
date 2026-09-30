---
id: goal:g7.16.1.10
mint_id: 95bbfbf4fd084c8faf999e30ec82fa9c
type: goal
parents:
  - goal:g7.16.1
next_edges: []
confidence: 0.7
edited_by: self-perpetuating
goal_id: G7.16.1.10
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 447eb127019929ec
season: 2
seeds: []
status: active
tags:
  - council-loop
  - merge-up-review
  - review-once
  - b4
  - prime-freed
title: "G7.16.1.10: a change is reviewed ONCE, as it lands -- rounds polled from the trunk, reuse proven per commit by patch-id against a recorded sm_clean mur, one council report row per round, residues to their owner, and the Prime gives only the final merge word"
town: core
---
# goal:g7.16.1.10

## OWNER 2026-09-30 05:1xZ, verbatim (Prime pane)
"It's weird you're still running chunk reviews it feels like that's also the councils job or something that should be automated as merges roll in. So you can keep the most zoomed out view and properly ground yourself way up high right up into the morals"

## OWNER 2026-09-30 02:5xZ, verbatim (Prime pane)
"Remember the council IS prime to everyone else."

## Why this exists
goal:g7.16.1 (the council loop): in this formation every bundle is already reviewed once, by sanctuary-master's mur before the council's lens pass. The Prime's PASS (skill agi-merge-pass §2, steps 2-4) then builds rounds over BASE...TIP and launches chunk reviews of the SAME changes a second time before merging the town trunk into season2/main. PASS B3 (gen 20, merged 13c3a3e8c: 608 commits, 40 sampled rounds) ran under that procedure, and its residues went to a Prime-minted leaf (goal:g1.31), as B2's (goal:g1.30) and 12's (goal:g1.28) did.
Measured 05:2xZ 09-30 (read-only feasibility review): reuse cannot be decided mechanically today. A mur verdict records no base/tip (merge-up-review.json:141,250; the shas go only into the prompt, :16), the tracked run row has no args or shas (workflow.py:1192-1235), SM's bundle-3 murs ran as Claude Code wf_* runs with 0 tracked rows, and "SM-clean tip" exists only as a room line that moved (9966e3050 -> ddea3a61f). There is no discrete "a round lands" event either: directors commit straight to the trunk (B3: 11 merges, 1 a director merge-up).

## Target end-state
```
poll rev-list <last_reviewed>..trunk (the CHECK cadence; trunk-sync merges excluded)
   └─ rounds = one commit, or a run of consecutive commits by the same post + hypothesis (never across a foreign commit)
        ├─ every commit's patch-id already sits under an sm_clean mur record, context unchanged ─▶ REUSED(run key)
        └─ otherwise ─▶ ONE queued launcher (PER x CAP <= 6, the memory guard) ─▶ agi-merge-up-review ─▶ REVIEWED(run key)
every round is a row on ONE council report node (via write.py, committed by exact path, suite-lock aware):
   round · base..tip · REUSED | REVIEWED | unreviewed:budget (run key) · verdict · residues · reds
   residues (from verify verdicts[] + missed[], never the review list alone) ─▶ the owner: the hypothesis's assigned post,
            else the commit-subject post, else director-engine ─▶ that owner's residue leaf (never a Prime-minted PASS leaf)
   RED (a config cell: secrets · node deletion by mint_id · broken link · protocol regression) ─▶ hard stop, ONE [red]
PASS = the Prime reads the report ─▶ ONE word: merge | hold ─▶ merge + verify + push, which stay mechanical
```
- **A review has a recorded identity.** At launch, `workflow.py` persists `runs/<key>/round_<label>.json = {base, tip, tip_tree, paths, patch_ids[], launched_by, sm_clean}`, and the report row copies it. Reuse is keyed by content through git's own machinery: per commit `git patch-id --stable`, plus the touched files' base blob ids, so the context the reviewer read is part of the key (all-is-one lens). "SM-clean" is a field on that record, never a room line.
- **Reuse PROVES coverage, never assumes it** (alive lens). A round is REUSED only when EVERY commit in it has its patch-id under an sm_clean record with the same base context. A tip sha never stands for the commits below it.
- **Mechanical REDs are checked mechanically first.** Secrets (anonymize, counts only), a node deletion (resolved by mint_id; a move into deprecated/ is not one) and a broken link are checked before any model runs. Only a protocol regression needs judgment.
- **Budget stays honest.** Under the credits floor (a config cell), unreviewed rounds show as `unreviewed:budget` rows. A merge over them needs the Prime's word naming the count. Only a RED or a round with NO row blocks by name.
- **The council keeps its lens.** The council still reviews each bundle through its lenses. The report is the PASS input, and the Prime stands above it on the morals.
- **The reviewer is a self-healing loop,** so it is a row of the liveness census (goal:g7.16.1.5 C / goal:g7.16.1.1.6.1). A reviewer that stops is ONE [red], never a silent backlog.
- **Model:** a config cell. It stays pi-free until the headless claude-code stage route lands in workflow.py (today that harness only prints a Workflow() call, workflow.py:2590-2606); after that, Sonnet 5.5.
- Absorbs BY NAME: skill agi-merge-pass §2 steps 2-4 (build rounds, launch chunks, verdicts) and step 6 (the Prime-minted residue leaf). Steps 0, 1, 5 and 7 stay as the mechanical merge.

## Invariants
- The Prime never runs a chunk review.
- A merge never lands over a RED, or over a round in BASE...TIP with no row. `unreviewed:budget` rows merge only on the Prime's word naming their count.
- Every residue lands on a named owner, never on the Prime.
- The cost cap holds: every review goes through the one queued launcher (PER x CAP <= 6).

## Falsifier
1. The next PASS (B4): 0 tracked run rows with `launched_by=belam` since `last_pass_at`, and the council report's rows cover every commit in BASE..TIP.
2. A commit whose patch-id already sits under an sm_clean record, with unchanged base context, shows REUSED and starts 0 review runs. A rebase of it onto a new sha is also REUSED, and a record whose span does not cover the commit never shows as REUSED.
3. Negative: a scratch round with a planted fake secret is RED before any model runs, and a commit with no report row blocks the merge by name.

## Out of scope
goal:g5.33 (workflows retire into the unified dispatch route: the queued launcher rides whichever route is live) · goal:g1.31 (PASS B3's own residues) · goal:g7.16.1.6 (the write form) · the headless claude-code stage route itself (sanctuary-master's first engine item; this goal depends on it only for the Sonnet model cell).

## Agent Notes
Assigned to **the council** (placement).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by self-perpetuating (council item 3 on belam resume, alive convening) on the owner 05:1xZ 09-30 line, verbatim: "It is weird you are still running chunk reviews it feels like that is also the councils job or something that should be automated as merges roll in" (full quote in the OWNER section). Lens (vision:self-perpetuating): the change is not only moving reviews off the Prime; in the council loop SM already murs every bundle and the PASS re-reviews it, so the goal is ONE review per change. Lens lines taken whole: all-is-one (key by content through git patch-id --stable + the touched files base blobs, never a new hash, never the tip sha), alive gen 3 (reuse PROVES coverage; the report shows REUSED vs REVIEWED with the run key). An Opus read-only feasibility review (05:2xZ) found the draft identity and trigger did not exist in the tooling; its five amendments were folded in: a persisted round record written by workflow.py, rounds polled per commit from rev-list (no discrete landing event exists), ONE queued launcher that keeps the paid-for PER x CAP <= 6 trap, residues from verify verdicts[] + missed[] with a named owner rule, unreviewed:budget rows so a sampled PASS can still merge on the Prime naming the count, a launched_by cell that makes falsifier 1 measurable, and pi-free until the headless claude-code stage route lands.
<!-- THOUGHT:END -->
