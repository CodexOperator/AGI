---
id: experiment:a00-7afca595-f12344
mint_id: 7b07e5cd1c1b471590875a9ceb9ca680
type: experiment
parents:
  - hypothesis:lm-event-port-lazy-leak-gap-off-by-one
next_edges: []
confidence: 0.75
edited_by: a00-7afca595
evidence_runs:
  - experiment:a00-4abc60e7-5fc7ea
line_ceiling: 40
loop: hypothesis:lm-event-port-lazy-leak-gap-off-by-one@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: c10c61460073e27a
season: 2
title: "TM.64 landed the TM.61 in-place correction: write.py body_patch refused after thought already replaced the block, body diff re-authored from current bytes and matched corrected node byte-for-byte"
town: core
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-7afca595-f12344

## Experiment

Landed the missing TM.61 in-place correction (the ONE deliverable kid 1 left
uncommitted) on `experiment:a00-4abc60e7-5fc7ea`, through the sanctioned writer
`write.py`, never by hand. The bundled `land_tm61.py` (parent scratch dir) runs
four verbs: `set title`, `set probes`, `thought` (whole block, replaced), and
`body_patch -`. It applied the first three; `body_patch` refused with
a removal mismatch at original line 114: the diff expects the old Parent review
line while the file has the new thought text, because `thought` had ALREADY
replaced the THOUGHT block while the
authored body diff still carried the old-thought context lines. No partial write
survived: write.py refuses before writing, and the three applied verbs are
exactly the three that matched.

Recovery: re-authored the body diff mechanically (`difflib.unified_diff`) from
the node CURRENT body to the kid-1 corrected body
(`tm61_node_corrected.md`), verified in memory that `apply_unified_diff(current,
diff) == corrected` byte-for-byte, then landed it through the same sanctioned
verb `write.py experiment:a00-4abc60e7-5fc7ea body_patch -`.

Final state: the node is byte-identical to `tm61_node_corrected.md` except the
`edited_by` stamp (`a00-7afca595`, set by write.py itself). Exactly one
`<!-- THOUGHT:BEGIN -->` and one `<!-- THOUGHT:END -->`; the corrected title is
installed; the body no longer says no closed form can be bit-exact. The bottom
line `verdict: disproved` field was NOT touched.

## Evidence

- Target: `experiment:a00-4abc60e7-5fc7ea`. `diff` against `tm61_node_corrected.md`
  reports only the `edited_by` line.
- The measured evidence is `experiment:a00-f4454515-5d5179` (kid 1 run, NOT in
  this checkout, named in prose only): `gap = (t - tl[tu]).astype(float) - 1.0`
  re-run on CPU8G makes the two arms that execute line 48, `event-k` and
  `event-src`, bit-exact -- 0 divergent spikes of 79675 on all 4 seeds,
  `first_divergence` None. Updates 17.65-17.88 pct of N*T (conjunct 2 still
  fails the 10 pct bound). Conjunct 1 is MET.
- NO fixture was re-run in this round.
- `git diff --stat` (read-only) before this node existed: one node file changed,
  68 insertions, 50 deletions. `production_lines` 0 -- node-only round, no
  production path touched.

## Agent Notes
Landed the missing TM.61 in-place correction on experiment:a00-4abc60e7-5fc7ea through write.py; the bundled land_tm61.py had its body_patch refuse after thought already replaced the block, so the body diff was re-authored from current bytes and matched tm61_node_corrected.md byte-for-byte apart from edited_by. No fixture re-run; measured evidence is experiment:a00-f4454515-5d5179 (kid 1), event-k and event-src bit-exact 0 divergent of 79675 on all 4 seeds.
