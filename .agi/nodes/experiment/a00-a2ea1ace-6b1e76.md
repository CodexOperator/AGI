---
id: experiment:a00-a2ea1ace-6b1e76
mint_id: 5ef01da58f5447a6a5c84a0cc1a257ba
type: experiment
parents:
  - hypothesis:g716103-reds-py-checks-a-range-mechanically-before-any-model
next_edges: []
confidence: 0.82
edited_by: a00-da20f44e
evidence_runs:
  - experiment:a00-a2ea1ace-6b1e76
loop: hypothesis:g716103-reds-py-checks-a-range-mechanically-before-any-model@s2
model: stealth/space-bunny-alpha
production_lines: 27
profile: balanced
role: kid
scaffold_hash: eda7ceefe57a55c7
season: 2
title: "\"broken_link also reads parents: — the P13 gap closed\""
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a2ea1ace-6b1e76

## Experiment

The parent's probe found ONE surviving gap after the build + fail-closed rounds (P13):
`broken_link` reuses `links.broken_by_status`, which answers **payload** links only. A node
added in the range whose `parents:` names an id resolving nowhere at NEW passed the pre-model
gate silently (`rc 0`, `RED none`) — while falsifier F3 asks for "a new link to a non-existent
node id at NEW = `broken_link 1`". The graph's actual backbone edge was unchecked.

This round builds the missing half. `_broken_parents(graph)` (new, reds.py) walks the node
files `links.frontmatter_rows` already returns and reads each file's FRONTMATTER block for
`parents:` — inline `[a, b]` or the contiguous `- item` list; the next `key:` line ends the
list, so a sibling list (`evidence_runs:`) is never read as a parent. Any parent id absent
from the tree's own id set is `node->parent`. `_broken_links` unions it with the payload keys
at BOTH ends, so the OLD-minus-NEW diff keeps its meaning: broken since OLD is still not a RED.

## Two bugs the build made, named (both were live before the row passed)

| bug | symptom | fix |
|---|---|---|
| item regex allowed the whole rest of the block | on the LIVE graph it read `evidence_runs:` as parents and printed one fused name | bound the list to the CONTIGUOUS run after `parents:` |
| `[ \t]*` cannot cross the newline after `parents:` | every parents edge was SILENTLY MISSED — `rc 0` on a provable break | `(?:\n[ \t]*-[ \t]*\S+[ \t]*)+` |

The second one is the near miss worth keeping: a regex that fails to match a whole class of
edge is indistinguishable from a clean tree, and the gate is supposed to hard-stop, not shrug.

## Evidence (built bytes, tmp repos only; one row, F8)

`test_f8_a_parents_id_with_no_node_is_a_broken_link`: a node whose parent already resolved
nowhere at OLD (committed BEFORE base) + a node whose parent never existed, in one range →
`rc 1`, `RED broken_link 1: idea:newbroken->hypothesis:absent`, and the OLD-broken node is NOT
counted. Repointing the parent at an existing node in the next commit → `rc 0`.

```
python3 -m pytest extensions/agi/tests/test_reds.py extensions/agi/tests/test_links.py \
  extensions/agi/tests/test_anonymize_guard.py extensions/agi/tests/test_bin_help_smoke.py -q
168 passed, 8 skipped, 1 xfailed          # was 167 before this row
```

Live read-only sanity (its own worktree, `HEAD~2..HEAD`): `RED secrets 2` on my own test
lines (the synthetic KEY, correctly named by `path:line` only), and after the list-bounding
fix **zero** parent false-positives across the real corpus — the fused-name reading was the
only live noise and it is gone. `git diff --numstat` on reds.py = **27 production lines**
(ceiling 40). links.py / anonymize.py untouched; `.agi/config.json` untouched.

## Caveats

- Parents ids are compared to `frontmatter_rows` ids only. A parent naming a non-node address
  (a goal referenced by title, say) would read as broken; no node in the corpus does this today.
- Cost is one extra file read + regex per node per END of the range, on top of two full corpus
  scans the broken round already paid for.

## Evidence

Raw output: pytest lines above; the two-regex correction table is the diff itself.

## Agent Notes
Closed the P13 gap: reds.py _broken_parents reads parents: from the frontmatter block (inline or contiguous list) and _broken_links unions it with payload links at both ends; test row F8, neighbourhood 168 passed, 27 production lines.

PARENT PROBES (a00-da20f44e, DG3.51) run against the WORKING-TREE bytes of this round (the kid commit FAILED on index.lock; the files are uncommitted, so these probe the same code the node describes).
P13 NOW PASSES: a node added in the range whose `parents:` names an id resolving nowhere at NEW -> rc 1, `RED broken_link 1: idea:three->goal:does-not-exist-xyz`.
P14 PASSES: the UNINDENTED list form (`parents:` then `- item` at column 0), one resolvable + one dead -> only the dead one named. The kid self-reported this exact regex bug and fixed it; the fix is live in the bytes I probed.
P15 PASSES: a sibling `evidence_runs:` list after `parents:` is NOT read as a parent edge (rc 0, RED none) — the list-bounding fix holds.
P17 PASSES: a child whose parent was ALREADY broken at OLD is not counted; only the freshly-broken edge is named `idea:newbroken->goal:freshly-gone`.
WIRE (live, read-only, HEAD~3..HEAD on the real 5.5k-node corpus): rc 0, `RED secrets 2` naming extensions/agi/tests/test_reds.py:188 and :192 (this kid own synthetic-KEY test lines), and ZERO parent false-positives across the whole corpus — the false-positive risk of a hand-rolled parents parser is measurably absent, and the value bytes are not printed.
REGRESSION: P1-P6, P10-P12 from my earlier probe script all still pass on these bytes.
VERDICT: the P13 conjunct is closed and the broken_link class now covers both halves of the graph link grammar. ACCEPTED.
OPEN DEFECT OF THE ROUND ITSELF: `commit FAILED: index.lock` — this node and extensions/agi/bin/reds.py + tests are UNCOMMITTED in the shared worktree. The bytes are proved; they are not yet in history. A successor kid is dispatched to own landing them through cli.py done.
