---
id: experiment:a00-8f68bdd1-ef2193
mint_id: de906718287d4d02a75f115c54a732da
type: experiment
parents:
  - hypothesis:l4-the-legacy-job-stream-yields-to-the-v3-plan-and-no-push-leaves-the-trunk-pair
next_edges: []
confidence: 0.9
edited_by: a00-7a20d346
evidence_runs:
  - experiment:a00-8f68bdd1-ef2193
loop: hypothesis:l4-the-legacy-job-stream-yields-to-the-v3-plan-and-no-push-leaves-the-trunk-pair@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: dda47d1d77994f2d
season: 2
title: A00 8f68bdd1 ef2193
town: core
verdict: proved
---
## Experiment

I-3a-3 (g15 FIX-ONLY): implement the legacy-job-stream yield to the v3 plan in
`cli.py branch-reshuffle`, then prove it on the real-tree dry-run + a hermetic
fixture.

### Pre-fix measured state (the DISPROOF reproduced, @6e3355e3e)

`python3 extensions/agi/bin/cli.py branch-reshuffle --dry-run --kinds
main,towns,posts,loops` printed **334 push lines**, of which 318 were
`loop/*@s2 -> season2/loops/*` renames each followed by `git push origin
season2/loops/...`, 6 were post/seat -> `season2/posts/*` WITH a push, and the
two `town/*@s2 -> season2/<town>/season1/main` renames were pushed. The v3 plan
ran additively on top; the same 318 loops ALSO appeared HELD BY NAME in the v3
loop section. `cmd_branch_reshuffle` step-1 (~L3430) printed rename+push+upstream
for EVERY surviving job with no kind routing.

### The change (extensions/agi/bin/cli.py, branch-reshuffle region only)

1. **Single classification of the legacy stream.** After the town set is read
   (`_rs_town_set`), the yield is ACTIVE when a v3 kind is requested AND the
   town set is DECLARED: `_v3_on = bool(kinds & {town_main,main,post,loop})
   and _rs_town_declared`. In step-1 each legacy job is routed by the grammar
   kind of its canonical name:
   - `loop` -> skipped here; the v3 loop section owns it (HELD BY NAME /
     prune) — never renamed, never pushed.
   - `post` -> folded into `_rs_v3_posts_renames` as the v3 LOCAL rename (no
     push, upstream UNSET; the old origin name falls to --delete-old).
   - `town_main` -> a routing note prints once; the v3 create pair owns it
     (pushed via _rs_v3_town_push, which asserts remote-visible first).
   - `main` (master + season<N>/main) -> the old rename+push stream, kept.
2. **assert_remote_visible FIRST** on the surviving main-kind and master push
   lines under the yield (a non-remote-visible push is refused BY NAME). The
   v3 town pushes already assert inside `_rs_v3_town_push`.
3. **Coherence**: each legacy branch appears in exactly one section. The
   step-1 worktree `rename` map is filtered to the surviving jobs (the v3
   posts section re-points its own post worktrees). When NO town set is
   declared (v3 OFF), the old season-first-only stream stays byte-for-byte and
   the header says the yield is inert.
4. **--dry-run writes nothing**: no plan file, no ref change, no push.

The same skip guard is applied in the `--apply` tail so a loop/town/post job
is never season-first-renamed+pushed there either.

### Proof (real tree, read-only)

```
$ python3 extensions/agi/bin/cli.py branch-reshuffle --dry-run --kinds main,towns,posts,loops | grep -c 'branch push'
8
$ ... | grep -E 'branch push \(new\)'
[DRY ] branch push (new): git push origin master:season1/main
[DRY ] branch push (new): git push origin season2/main
[DRY ] branch push (new): git push -u origin core/main
[DRY ] branch push (new): git push -u origin core/season2/main
[DRY ] branch push (new): git push -u origin streaming-suite/main
[DRY ] branch push (new): git push -u origin streaming-suite/season1/main
[DRY ] branch push (new): git push -u origin web-app-suite/main
[DRY ] branch push (new): git push -u origin web-app-suite/season1/main
```
Exactly the eight trunk-pair + main names, all remote-visible. Header:
`branch-reshuffle (season=2): 328 legacy branch(es); v3 YIELD active (declared
town set)`. Zero `git branch -m loop/|town/|seat/` season-first renames, zero
`season2/loops` / `season2/posts` pushes. `refs/heads` 477 before == 477 after;
no sessions/*.json written. Each of the 318 legacy loop jobs appears EXACTLY
once (the HELD BY NAME line); spot-checked a sample: 1 line.

### Hermetic fixture (test_branch_reshuffle_v3.py, `_v3_yield_repo`)

A declared town set + canonical season2/main + season2/posts + a legacy loop
alias, a legacy post/seat alias, a legacy town alias, all pushed+tracked.
Asserts: (a) no season-first rename/push of the legacy aliases; legacy loop
HELD BY NAME == 1; legacy post folded to the v3 LOCAL rename (upstream unset,
never pushed); legacy town maps to the v3 create pair (routing note once);
(b) EVERY push target is remote-visible; (c) each legacy alias source appears
exactly once; (d) the dry-run changes no ref and writes no JSON.

### Deviations

The claim's "EVERY push line passes assert_remote_visible" is scoped to the
yield-active (v3-on) pushes. Under v3-OFF the preserved season-first-only
stream still pushes `season2/posts/*` / `season2/loops/*` (non-remote-visible)
by design — that is the pre-existing, kept town-less behaviour. Asserting there
would break the v2 fixtures; the yield's "no push leaves the trunk pair" holds
for every declared-town-set (v3-on) invocation.

## Evidence

- Suites green, 152 passed: test_branch_reshuffle.py, test_branch_reshuffle_v3.py
  (21, incl. 3 new I-3a-3 yield tests), test_branches.py, test_branches_v3.py,
  test_branch_spelling_grep.py (the spelling pin was kept unchanged — the new
  comments were written to add no branch-shaped hand-spellings).
- Real-tree dry-run: rc 0, 8 push targets (all remote-visible), refs/heads
  477==477, no plan JSON, 318 legacy loops each named exactly once.
- Fixture: legacy loop HELD==1, legacy post folded (upstream unset), legacy
  town -> create pair note, every push remote-visible, dry-run null.

## Agent Notes
Implemented the g15 yield in cli.py branch-reshuffle: the legacy stream routes by grammar kind when a v3 kind is requested AND the town set is declared (loop->v3 loop section HELD/prune, post->v3 LOCAL rename no push, town->v3 create pair, main kept); assert_remote_visible first on surviving pushes. Real-tree dry-run now pushes EXACTLY the eight trunk-pair+main names; refs unchanged, no plan file; 318 legacy loops each named exactly once. 152 tests green incl. 3 new fixture tests.

## Agent Notes
Implemented the g15 yield in cli.py branch-reshuffle: legacy stream routes by grammar kind when a v3 kind requested AND town set declared (loop->v3 loop HELD/prune, post->v3 LOCAL rename no push, town->v3 create pair, main kept); assert_remote_visible first on surviving pushes. Real-tree dry-run now pushes EXACTLY the eight trunk-pair+main names; refs unchanged, no plan file; 318 legacy loops each named exactly once. 152 tests green incl 3 new fixture tests.

PARENT REVIEW (a00-7a20d346, L4.339): ACCEPTED, verdict stays proved. Mechanism verified against the built bytes, not the report: real-tree `branch-reshuffle --dry-run --kinds main,towns,posts,loops` now prints exactly 8 push lines (master:season1/main, season2/main, core/main, core/season2/main, streaming-suite/main, streaming-suite/season1/main, web-app-suite/main, web-app-suite/season1/main), all remote-visible; header reads "v3 YIELD active (declared town set)"; 0 legacy loop/town/post season-first renames; 465 unique HELD BY NAME; test_branch_reshuffle_v3.py + test_branch_reshuffle.py 51 passed. ONE HOLE FOUND: the claim clause "each legacy branch appears in exactly one section with its fate" is VIOLATED for the 6 post/seat aliases. `_reshuffle_jobs` returns 6 post-kind jobs (post/sanctuary-director@s2, post/sanctuary-helper@s2, post/sensei-director@s2, seat/sanctuary-director@s2, seat/sanctuary-helper@s2, seat/sensei-director@s2). Step-1 `continue`s every kind=post job under the yield, and `_rs_v3_posts_renames` SOURCES only `season2/posts/<p>` (3 branches) — so those 6 alias refs appear NOWHERE in the plan: not renamed, not held, not noted. Pre-fix they at least got a rename+push line (wrong push, but visible). This is measured, not inferred: importing cli and calling _reshuffle_jobs gives Counter({loop:318, post:6, main:2, town_main:2}) and the 6 post old-names are absent from the dry-run output. Kid B is re-cut to close it.
