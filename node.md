---
id: goal:g1.41
mint_id: 34dab5846bce46c88ac3ddc9051bd6e7
type: goal
parents:
  - goal:g1
next_edges: []
confidence: 0.7
edited_by: belam
goal_id: G1.41
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 81793048f2615a81
season: 2
status: active
tags:
  - engine
  - pass
title: "G1.41: PASS B4 residues -- every finding of the 6 reviewers merged at cd981237cd is fixed at its line or answered on its node"
town: core
---
# goal:g1.41

## Why this exists
goal:g1: PASS B4 (owner 18:0xZ 10-07: "We can start working on the merge pass now. A lot of it likely can be skipped since we retired so much stuff but whatever isn't deprecated can be merged now") reviewed the trunk BASE 1f2b49ffc9 -> TIP bcdb15f10f (5,242 commits, 1,165 live files, retired nodes skipped) with 6 adversarial reviewers and merged it into season2/main at cd981237cd (season2/main recreated at b0608a1f3 on the owner's choice: it had vanished from origin). Every finding below names file:line at TIP.

## Target end-state
- Every residue below is fixed at its line or answered on its node; the two demotes are corrected on their nodes.
- The boot hole is closed by the DG lane (owner 19:0xZ 10-07, verbatim: "Leave it, fix via DG only").
- SM places the lanes (one owner per file); DG1 writes the hypotheses; DG2 falsifies; DG3 builds; SM gates.

```
FIXED BEFORE MERGE  heal.py:1905 sweep discarded git status rc -> force-remove of uncommitted bytes  = 28b5d9cd95 (SM 19:38Z)
                    aa3-lanes.t.sh lane 3j red since the thought-master rename                      = fe8d111821 (belam)
RED -> DG (owner)   engine-root.md:61-63,71,74 + engine.md:91 agi-boot.service (root) runs HEAD:engine-root.md while
                    .git + refs/heads carry group agi rwx (14 users): boot chain must read a root-held pinned sha (carry.env AGI_TRUNK pattern)
DEMOTE              goal:g7.16.1.5.5.6 complete, ram-recharge half unmet (child .1 active)
                    outcome:g4-18-5-5-suite-lock-refusal-exits-3-closed:35 cites dg2mvp-g41855 as PROVED (inconclusive_lean_proved:70); add dg2mvp-g1315131
                    outcome:council-bundle-1-g7-16-1-1:57 "one source per rule holds" vs dg2g6-b (test_thought_hygiene.py:54) + dg2g6-a
ROOT PIECES         engine-root.md:142-146,104 agi-carry@ restarts unbounded every 5 s for a post absent at the pinned T
                    engine-grow.md:41,60 engine*.md has no ring: cell; agi-gate runs a candidate's agi-project as root (close BEFORE agi-land installs)
                    engine.md:90 agi-project uses posts.md .name unvalidated (path traversal, sysusers field injection, quote break)
                    engine-root.md:73,76 jq "null" -> awk string compare opens the load gate (claims fail-closed)
                    guard-init.sh:181 eval of guard.env as root before validation (+ ram-main.sh:19, ram-tier.sh:21, session-sweep.sh:14)
                    engine-root.md:39,43 agi-run missing -> exit 127 loop every 30 s, root agi-signers each cycle
                    engine-post.md:144 polkit lets any agi user start ANY agi-post@ (restarts a downed post)
                    engine.md:41-79 stated piece sizes stale (agi-project 1841 -> 2242 B, agi-wt 688 -> 1077 B, ...)
ENGINE PYTHON       write.py:2079 ring gate fail-open on a load error · anonymize.py:306 no denylist -> rc 0 'skipped'
                    grid.py:895 extra ls-tree per node per tick; a malformed nest tip is skipped forever
                    metrics_cell.py:138 commits by path while the suite lock is held
                    reds.py:100 a deleted node file with no id: row is never a node_deletion · reds.py:51 scan without root (no user class)
                    verification.py:1409-1412 check_formation blind to a 2nd formations cell / a repeated active: key
                    council_report.py:138 tip guard accepts ?, *, ranges
GRID (owner Q)      grid.py:1240-1280 --all writes ONE ref twice per tick when two files share a mint (c89ca4b1: hypothesis a00-66d002ad-8cee33 +
                    experiment osc-band-call-run-a00-66d002ad; v6918) = 30% of all grid versions · cron vs post card ping-pong (grid.py:911-913:
                    MAIN's older card re-versioned over the post's newer one) · experiments a00-da06914d-branch-dry-run + a00-829ed05f-dry-refuses-target
                    have no mint_id (error every tick) · AA1.V capsule per-node commits designed, NOT installed (every live agi-turn = 269 B v4)
TESTS + SKILLS      skills/agi/SKILL.md:59, agi-workflow:4-41, agi-corrective:103-105, agi-dispatch:48 still route workflow.py (owner 10-02 14:01Z: retire it)
                    agi-goal:13, agi-dispatch:16,61, agi-corrective:71-81 write.py as the only writer (owner 10-01 23:3xZ: v5 = plain Write/Edit)
                    test_anonymize_guard.py:867-871 always skipped · test_heal_sweep.py:53-57 + test_heal_watch.py:51 stub _sweep_pressure_ok (heal.py:1603-1619 untested)
                    test_boxkit_templates.py:1199-1201 email-only hit = skip · test_node_writer.py:1796 tautological or
NODES               g4.6.1:44 falsifier hits a comment · g7.16.1.11.3:33 falsifier unreachable (9 MISSING frozen) + 55 vs 51 rows
                    g7.16.1.11.1:34 + .11.2 minted complete with no measurement · doc:council-report table 0 rows
                    experiment dg2mvp-g7165332-check:16 + verdict dg2mvp-g7165332:20 cite old id goal:g7.16.1.5.3.2
                    g7.16.1.5.3:47 owner quote "we're" vs first appearance "we are" · verdict dg2g6-d:24 cites a never-existing experiment
                    verdict dg2-aa1m-m3b overlap row contradicts itself · 38 listed nodes miss schema fields (links.py schema: 246 graph-wide)
                    lm-kv-slot-save-beats-reprefill:14 write.py round-trip wraps testable_claim in quotes (930e65687c)
RESEARCH            datasets/osc-band/2026-10-01-neuron-period-2/*.npz 45.8 MB + model*.pt 3.6 MB pickles + acts.npz 1.5 MB in history, no LFS/ignore
                    dt1-self-poke-toy-dh1-1001:19 malformed key carries the corrected title (:18 overclaims) · tm-neuron-period-pc-1001:55 no link to p4fair
                    L4 run 2 thin margins unrecorded (run 4 wins 2/3) · self-poke-toy-dh1 dataset lacks summary.md
ANONYMIZE           a00-9e756108-2218a8:40 + a00-b5e5622d-9bd19f:108 quote /tmp/pytest-of-<user>: write the segment as <user>
```

## Falsifier
- Negative: any line above still reads as quoted at the season2/main tip after its lane closes.
