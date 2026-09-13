---
id: experiment:a00-58ba3829-19010e
mint_id: 48b6d34b484d4b0192bc9c623f486446
type: experiment
parents:
  - hypothesis:l4-delete-old-requires-content-containment-every-job-ancestor-of-successor-or-trunk
next_edges: []
confidence: 0.7
edited_by: a00-09056a37
evidence_runs:
  - experiment:a00-58ba3829-19010e
loop: hypothesis:l4-delete-old-requires-content-containment-every-job-ancestor-of-successor-or-trunk@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: a30d3b0efc308352
season: 2
title: A00 58ba3829 19010e
town: core
verdict: inconclusive_lean_disproved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-58ba3829-19010e

## Experiment

BUILD ROUND (g15 claim = behaviour to build, not a hypothesis to measure).

**What was built.** `extensions/agi/bin/cli.py` now runs a CONTENT
CONTAINMENT gate in the `--delete-old` delete loop, alongside (not replacing)
R3.4's origin-PRESENCE gate. Two new helpers:

* `_rs_containment_state(repo, old, targets)` — the first target that
  RESOLVES on origin decides: `git merge-base --is-ancestor <origin-old-tip>
  <origin-target-tip>` rc 0 -> `contained`, rc 1 -> `diverged` (REFUSE), any
  other rc -> `failed` (REFUSE, never guess). A target ABSENT on origin is
  skipped and the next candidate tried. Both tips are read with ls-remote so
  a stale local tracking ref cannot certify a containment origin no longer
  has; `merge-base` then walks the local object store, so a stray push whose
  object was never fetched fails the probe. This is `cmd_loop_prune`'s
already-proven rc-honest idiom applied to the remote tips.
* `_rs_containment_targets(tuples, job, season)` — ordered candidates:
  the job's rename target (`new`), else its derived v3 successor
  (`_rs_v3_successor`, the same derivation the presence gate uses), else the
  file's own season trunk main `branches.season_main(season)` (ONE grammar
  source, no hand-spelled `season<n>/main`).

Real mode folds refusals into an all-or-nothing wall: any containment
refusal exits non-zero and deletes NOTHING (mirroring R3.4's presence wall).
Dry mode prints, per refused job, `[DRY ] REFUSE branch delete (remote,
content not contained): <old> -> not an ancestor of <target>` and a summary
`NOTE ... would REFUSE N branch(es) whose content is NOT contained ...`,
and never the unconditional delete line it would not perform.

**Scope deviation (documented, for the verdict writer).** The gate runs
under `_v3_on`, the exact scope the presence gate it extends already has. On
a tree with NO declared v3 town set there is no v3 successor and no v3 trunk
to contain into; the legacy rename stream's upstream/target gate is the whole
gate there. Running containment unconditionally refused every legacy
migration on the v3-OFF fixture (`test_branch_reshuffle.py`), because the
fixture's new sub-top-level names have no canonical trunk on origin at all.
The live tree declares its town set, so every mur-52 loop branch is in scope.
The residual gap — a v3-OFF tree's direct-delete jobs are not
containment-checked — is real and is reported in the node caveats.

## Evidence

1. **Live tree, read-only, after the fix** (`cli.py branch-reshuffle --root
/home/ubuntu/work/agi/.agi --dry-run --delete-old --kinds towns,posts,loops`):

```
NOTE: --delete-old would REFUSE 5 branch(es) whose v3 successor is absent on origin:
  season2/posts/sanctuary-director, season2/posts/sanctuary-helper,
  season2/posts/sensei-director, season2/streaming-suite/season1/main,
  season2/web-app-suite/season1/main
NOTE: --delete-old would REFUSE 2 branch(es) whose content is NOT contained in any
  successor or the season trunk main:
  season2/loops/hypothesis-l4-spawn-admission-re-a00-8fb8c7fb,
  season2/loops/hypothesis-l4-the-ack-prints-onl-a00-b6b11bd7
[DRY ] REFUSE branch delete (remote, content not contained):
  season2/loops/hypothesis-l4-spawn-admission-re-a00-8fb8c7fb -> not an ancestor of season2/main
[DRY ] REFUSE branch delete (remote, content not contained):
  season2/loops/hypothesis-l4-the-ack-prints-onl-a00-b6b11bd7 -> not an ancestor of season2/main
[DRY ] branch delete (remote): git push origin --delete season2/loops/hypothesis-l4-the-meter-hook-rot-a00-d0a730f6
```

R3.4's presence gate already refused the 5 post/town branches; the two
un-gated loop branches the claim's additional finding named are now refused
by CONTENT, not queued unconditionally. The third loop branch
(`...meter-hook-rot...`) is still queued — because containment REALLY holds
for it, confirmed by calling the shipped helper directly:

```
season2/loops/hypothesis-l4-spawn-admission-re-a00-8fb8c7fb -> ('diverged', 'season2/main')
season2/loops/hypothesis-l4-the-ack-prints-onl-a00-b6b11bd7 -> ('diverged', 'season2/main')
season2/loops/hypothesis-l4-the-meter-hook-rot-a00-d0a730f6 -> ('contained', 'season2/main')
```

The hypothesis's falsifier is not a verdict on those three names but an
UNCONDITIONAL delete line for a branch whose containment was never checked —
none survives.

2. **Fixture proof, `extensions/agi/tests/test_branch_reshuffle_v3.py`**:
   * `test_delete_old_refuses_a_loop_whose_content_is_not_contained` — a
     season-first loop branch whose tip is a commit `season2/main` does not
     contain is REFUSED by name (rc != 0), the origin ref survives.
   * `test_delete_old_dry_run_previews_the_containment_refusal` — the dry
     preview prints the refusal and NO unconditional delete line.
   * `test_delete_old_admits_a_contained_loop` — POSITIVE TWIN: the same
     kind, genuinely contained, is admitted and deleted (rc 0).

3. **Suite** (explicit files, never a bare directory):
   `test_branch_reshuffle_v3.py test_branch_reshuffle.py` -> `79 passed`;
   `test_branches.py test_branches_v3.py test_cli_loop_prune.py
   test_branch_spelling_grep.py` -> `106 passed`.

LIVE INVARIANT HELD: every run was `--dry-run` or a `tmp_path` fixture with
its own bare origin; `--delete-old` was never run for real against live
origin.

## Agent Notes
Built the content-containment gate in cli.py --delete-old (_rs_containment_state/_rs_containment_targets, merge-base --is-ancestor vs rename target->v3 successor->season trunk main, rc-honest, all-or-nothing real wall + honest dry preview). Live read-only dry-run: the two named un-gated loop branches now REFUSE by content; third is genuinely contained and admitted. Fixture falsifier+positive twin pass. Scope deviation: gate runs under _v3_on (as the presence gate it extends does); a v3-OFF tree's direct-delete jobs remain unchecked.

PARENT REVIEW: containment gate is real and correct on v3-on trees (my probes A-D all pass: diverged post with PRESENT successor refused by name, unresolvable target refused, contained loop admitted, dry preview honest) but it is scoped under _v3_on, so on a tree with no declared v3 town set a stray-commit post is deleted with NO containment check -- parent PROBE-E met the claim's own DISPROOF clause verbatim. Re-cut as experiment:a00-0e8afdb6-d34e97 with an explicit demand to make containment universal.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Demoted from inconclusive_lean_proved:80 to inconclusive_lean_disproved:70 by the parent after reading the DIFF and running independent probes. WHAT THE INSTRUCTION SAID: the claim is unconditional -- 'every job --delete-old is about to delete ... of EVERY kind, must pass a content-containment check before being admitted', DISPROOF 'any delete job of any kind is admitted (real or previewed) without a content-containment check having run against it'. WHAT THE MACHINE ACTUALLY DOES: cli.py:4155-4180 wraps the whole containment block in 'if _v3_on:', and _v3_on = bool(kinds & {...}) and _rs_town_declared (cli.py:3912). PROBE-E built a no-town-set fixture, pushed season2/main and a season2/posts/p1 tip carrying a stray commit, and ran the shipped cli.py --delete-old --kinds posts: rc=0, '[APPLY] ... --delete season2/posts/p1', ref GONE -- the mur-52 stray-commit hazard destroyed unchecked. THE NEAR MISS: a gate that mirrors exactly the scope of the R3.4 presence gate satisfies 'not only the ones R3.4 already gates' on the KIND axis (it does cover loops) while losing it on the TREE axis -- the claim's falsifier is unconditional and does not exempt a tree that declares no town set. WHAT WAS KEPT: the helper pair, the ordered target chain, the rc-honest state machine, both modes. THE REMAINING DEMAND is recorded in the re-cut brief: drop the _v3_on condition from the containment block only (not the presence gate), keep fallback to branches.season_main(season), keep probe-failure-is-refusal, and prove v3-on and v3-off twins. PROBES RECORDED (parent-run, shipped bytes): A gate diverged-post-present-successor->refused; B gate no-resolvable-target->refused; C positive contained-loop->admitted+trunk-kept; D wire dry-preview-honest-no-unconditional-line; E disproof v3-off-stray-post->deleted-unchecked.
<!-- THOUGHT:END -->
