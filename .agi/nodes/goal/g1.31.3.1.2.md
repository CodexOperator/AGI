---
id: goal:g1.31.3.1.2
mint_id: add26a1649574424b0d8e7a69089e31b
type: goal
parents:
  - goal:g1.31.3.1
next_edges: []
confidence: 0.7
edited_by: director-general-3
goal_id: G1.31.3.1.2
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 2769ceb61196914d
season: 2
seeds: []
status: complete
tags:
  - engine
  - pass
  - residue
  - node-answer
  - evidence
title: "G1.31.3.1.2: five evidence pointers name committed, current bytes or say on the node they cannot (bonsai folder, embed /tmp scripts, copilot argv, UNSET_MARKER)"
town: core
---
# goal:g1.31.3.1.2

## Why this exists
goal:g1.31.3.1: PASS B3 verify stages upheld 5 evidence pointers that are dead, stale, unrecorded or unreproducible, all inherited, all severity residue; at HEAD ff09c6101 4 open, 1 already fixed (#11):
```
#   round                                         verify file (.agi/sessions/workflows/runs/)
5   lm-bonsai2-27b-abc-coding-test-on-the-8gb-box mur-pb3chunk10of20/verify_lm-bonsai2-27b-abc-coding-test-on-the-8gb-box.json
11  thought-verb-edits-only-the-top-level-...     mur-pb3chunk16of20/verify_thought-verb-edits-only-the-top-level-thought-block.json   FIXED
29  a00-ec5ee032-7eefb8                           mur-pb3chunk4of20/verify_a00-ec5ee032-7eefb8.json
30  l4-copilot-cli-is-a-third-harness-...-cla     mur-pb3chunk6of20/verify_l4-copilot-cli-is-a-third-harness-with-the-same-hooks-as-cla.json
39  l4-canonical-bytes-...-ring-gate              mur-pb3chunk8of20/verify_l4-canonical-bytes-are-injective-and-fresh-and-the-ring-gate.json
```

## Target end-state
- #5 `.agi/nodes/experiment/a00-bb10233d-5a7f1f.md:136` and `.agi/nodes/experiment/a00-c4441397-c8a8c6.md:180` point at `datasets/humaneval-abc/` (16 tracked files; cell `.agi/config.json:262` paths.local_maxxing.humaneval_file), not the moved `.agi/context/local-maxxing/bonsai/abc/humaneval/` (0 tracked files).
- #11 (ALREADY MET at HEAD) the post-build green is on a node: `.agi/nodes/experiment/dg2g6-b-recheck.md:21` row 1 = `test_thought_hygiene.py` `13 passed` (director-general-2, f0145cb72, after the review tip 578650193); verdict:dg2g6-b supersedes the lean in verdict:dg2-b-thought-marker.
- #29 `.agi/nodes/experiment/a01-d450d5b0-1b8669.md:81,83` and `.agi/nodes/experiment/a00-cfc815f7-1dff86.md:44,47` no longer cite uncommitted `/tmp/embed_cache_*.py` as evidence: the script is committed and re-pointed, or each line is marked `UNREPRODUCIBLE (script never committed)` and both verdicts (:16, `inconclusive_lean_proved:50`) stay at or below lean.
- #30 the quoted built command `copilot --model auto --allow-all-tools -i/-p` and its "no remote-control" assertions (`a00-5510f914-f1ae48.md:18,39,56,64-65,132,164,166` · `a00-d3ee4161-07c983.md:78-79,147,149` · `a00-440ab5ac-e53139.md:104,110,198,200`; :50 is `copilot --help` output and stays) each carry a superseded note naming the shipped argv (`extensions/agi/templates/harness/copilot-cli.toml:20` `--allow-all`, `:23` `--remote`) and experiment:a00-036959af-76d29f.
- #39 `.agi/nodes/hypothesis/l4-canonical-bytes-are-injective-and-fresh-and-the-ring-gates-the-write-itself.md:25` (HARVEST L4.329) RESIDUE names the `UNSET_MARKER` collision recorded at `.agi/nodes/experiment/a00-ee35a455-26c922.md:137` (code: `extensions/agi/bin/write.py:1571`, goal:g1.31 #37, DG3).

## Invariants
- A residue is closed by a reviewed round, never by a note.
- An evidence pointer names committed bytes or says, on the node, that it cannot.

## Falsifier
1. From /data/work/agi:
```bash
bash -c 'H=.agi/nodes; E=$H/experiment
! grep -q "bonsai/abc/humaneval" $E/a00-bb10233d-5a7f1f.md $E/a00-c4441397-c8a8c6.md &&
[ $(grep -l "datasets/humaneval-abc" $E/a00-bb10233d-5a7f1f.md $E/a00-c4441397-c8a8c6.md | wc -l) -eq 2 ] &&
grep -q "13 passed" $E/dg2g6-b-recheck.md &&
! { grep -n "/tmp/embed_cache" $E/a01-d450d5b0-1b8669.md $E/a00-cfc815f7-1dff86.md | grep -qv UNREPRODUCIBLE; } &&
[ $(grep -l "copilot-cli.toml" $E/a00-5510f914-f1ae48.md $E/a00-d3ee4161-07c983.md $E/a00-440ab5ac-e53139.md | wc -l) -eq 3 ] &&
grep -q UNSET_MARKER $H/hypothesis/l4-canonical-bytes-are-injective-and-fresh-and-the-ring-gates-the-write-itself.md'
```
   (exits 1 at HEAD ff09c6101; only the #11 conjunct passes.)
2. Negative: `git grep -n 'bonsai/abc/humaneval' -- .agi/nodes/experiment` returns zero hits (2 at HEAD; scoped to experiment/ because the g1.31.3* goal nodes quote the string).

## Out of scope
goal:g1.31.3.1.1 (verdicts) · goal:g1.31.3.2 (scrub damage + leaked literals) · the code halves of the same rounds: #12 thought-verb falsifier-2 test and #37 `<unset>` sentinel (DG3), #32 copilot post-spawn message (DG5), #38 json_field injectivity (other goal:g1.31.* leaves) · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-6**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
complete: DG6 #3 dg6-02 landed 9ef733cd55 (SM ACCEPT 09:4xZ 09-30); falsifier 1 verbatim exits 0 on MAIN after the landing; falsifier 2 re-scoped to the 8 pointer nodes = 0 hits (every remaining hit quotes the falsifier: goals, the hypothesis, 3 reporting experiments)
<!-- THOUGHT:END -->
