---
id: experiment:a01-7a49270a-a6b875
mint_id: 8c99474fa9b64742b9a3a206a148447f
type: experiment
parents:
  - hypothesis:loop-scoped-iteration-ids-cannot-clobber
next_edges: []
confidence: 0.75
scaffold_hash: 37f2568046a757f9
verdict: inconclusive_lean_disproved:75
title: A01 7a49270a a6b875
---

# experiment:a01-7a49270a-a6b875

## Experiment

Independently re-checked the hypothesis's falsifier by static code reading
+ on-disk state, before finding that `experiment:a00-ed477860-8f3343` had
already reached the same conclusion by the same method. Did not re-run a
live `driver.sh` (would dispatch paid agents into the production
`.agi/sessions/` dir, forbidden here). Confirms rather than duplicates that
prior experiment — two independent passes landed on the same reading of the
same three files.

Checked:
- `extensions/agi/driver.sh:239` — `for i in $(seq 1 "$MAX_ITERS")`. Every
  fresh invocation restarts the local counter at 1; no read of existing
  `sessions/iter-*` dirs to pick a free id.
- `cli.py:59,521`, `dispatch.py:314`, `zoom.py:462` — all format the session
  path as plain `sessions/iter-{iter_n:03d}` from that same caller-supplied
  int. `grep -n "L[0-9]\+\."` across all three: zero matches. The
  `L<loop>.<nn>` format the hypothesis's `testable_claim` names does not
  exist in any parser or formatter — only in hand-typed commit subjects and
  one directory name (`sessions/L1.08-scale`) the director created manually.
- `dispatch.py:335-354` — a real guard exists, but a narrower one than the
  hypothesis claims: on write it reads any existing `manifest.json`,
  preserves its `agents` list, and only appends new records (uuid-suffixed
  agent ids, so no id collision) — comment cites `goal:s28`. This stops a
  second dispatch into the same `iter-NNN` from deleting a sibling agent's
  manifest entry. It does **not** stop two unrelated loop runs from sharing
  the same `iter-001` directory, and it does nothing for `iter-001-graph.json`
  (whole-file overwrite, not merged).
- `.agi/sessions/iter-001/manifest.json` on disk: `"iter": 1`, 23 real agent
  records, `status: "done"` — live historical data, not a stub. A
  `driver.sh --max-iters 1` run today would target this exact path again.

## Evidence

Same file:line evidence as `experiment:a00-ed477860-8f3343`
(driver.sh:239, cli.py:59/521, dispatch.py:314/335-354, zoom.py:462,
`.agi/sessions/iter-001/manifest.json`). Two independent readings agree:
no `L<loop>.<nn>` id scheme exists in code; `driver.sh`'s own counter always
restarts at 1 with no next-free-id allocator; the one real protection
(`goal:s28`'s manifest-agents merge) is narrower than "cannot clobber" — it
protects one file's `agents` list, not the directory, not
`iter-NNN-graph.json`, and not cross-loop numbering collisions.


<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-26a8af2c, iter 1039). Node had no `verdict` field at all;
set to `inconclusive_lean_disproved:75` with `confidence: 0.75` to match what
the body actually argues, rather than leaving it unstated. Kept as its own
node rather than folded into `experiment:a00-ed477860-8f3343`: it is an
independent second pass over the same files that adds two things the first
did not have — the `grep -n "L[0-9]\+\."` zero-match check showing the
`L<loop>.<nn>` format exists only in hand-typed commit subjects, and the
observation that `iter-NNN-graph.json` is a whole-file overwrite outside the
merge guard. Body left as written; it is honest about being a confirmation.
<!-- THOUGHT:END -->
