---
id: goal:g7.5
mint_id: 116872160ca44aafadd6c8d1eab645a2
type: goal
parents:
  - goal:g7
confidence: 1.0
edited_by: season.py
goal_id: G7.5
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G7.5: Parse failures are swallowed with zero signal"
---
> **Corpus repaired 2026-08-25; the code fix is still open, which is why this
> stays `active`.** The malformed file below now parses, carries a `mint_id`,
> and has a grid ref. **The loaders still swallow parse failures silently** —
> that is the actual goal and nothing about it has changed. What has changed is
> that the corpus no longer supplies a free fixture, so the fix needs the
> synthetic one preserved here. Verbatim, the frontmatter as it stood:
>
> ```yaml
> ---
> id: "hyp:a00-1467544f-chain-600hop"
>   - "exp:a00-1467544f-chain-600hop"     # <- stray: `spawns:` key was missing
> parents:
>   - idea:domain-bootstrap-discovery
> subgraph: false
> ...
> ```
>
> A list item at indent level 1 directly after a scalar mapping entry, with no
> key introducing it. PyYAML raises; both loaders catch and drop the file. The
> repair was to restore the one missing line — `spawns:` — which is what the
> orphaned item plainly belonged to. **Nothing else in the file was touched, and
> no node was created or deleted.** Regression test: feed the block above to
> `load_directory` and `load_existing_nodes` and require both to warn with the
> path and the exception rather than continue.

`load_directory`'s `except Exception: continue` and `load_existing_nodes`'s
`except Exception: pass` both silently drop any file that raises while its
frontmatter is parsed. **No caller learns anything.**

On the live corpus this hides exactly one file:
`nodes/hypothesis/a00-1467544f-chain-600hop.md`, whose frontmatter carries a
stray `- "exp:a00-1467544f-chain-600hop"` list line between `id:` and
`parents:`, breaking YAML block-mapping parsing. That file is invisible to the
renderer, the metrics, the chain finder and the dashboard alike — the same
failure mode as G7.1 and G7.2, reached through a hard parse error instead of a
bad reference or an id collision.

Fix: both sites warn with the file path and the exception, following the
warn-by-default / strict-to-fail pattern G7.1 and G7.2 already established.
**Do not repair the malformed node.** Fixing the corpus is a separate,
deliberate decision — the G7.2 rule. This goal is about making the failure
visible, not about making it go away.

**This goal also owns one of G7.1's "dangling" references, which is not
dangling.** `nodes/experiment/a00-1467544f-chain-600hop.md` references
`hyp:a00-1467544f-chain-600hop`, and the integrity check reports it as an
unknown parent. **The target exists on disk, with exactly that id** — it is the
malformed file above, and it is absent from the loader's index only because
parsing it raised. So the reference is sound and the *index* is incomplete;
the reported defect is in the wrong place.

Left unfixed on 2026-08-25 for that reason. Repairing the stray list line would
clear the INTEGRITY line and simultaneously destroy the only live evidence this
goal has — the corpus stops demonstrating the defect the moment it is tidied.
**Repair it as part of landing the warn, never before**, and re-run G7.1's sweep
afterwards to confirm the reference resolves rather than disappears. Until then
the count of genuinely unresolvable references is **2**, not 3: this one is a
G7.5 symptom wearing a G7.1 costume.

**Third consequence, found 2026-08-25, and like G7.2's it breaks the backup
rather than the render: this node had no grid ref and was therefore not backed
up at all.** *(Closed by the repair above — it now has a `mint_id` and a ref.
Kept here because it is the argument for why a parse failure is never cosmetic.)* `grid.py commit --all` refuses to write a node-id-keyed ref for a
file with no `mint_id`, and `backfill-mint-ids.py` — the only assigner (S14) —
skips it with `SKIP (unparseable frontmatter)`. The parse failure that hides the
node from the renderer also denies it the one mechanism G7 exists to guarantee.
Every `commit --all` since the mint-id migration has reported it as an error
line among successful ref writes, which is the same shape of silence G7.2 was
escalated for.

That raises this goal's priority the same way. G7.5 was "one file is invisible
to readers", which is bad but static. It is also **an ongoing hole in the
backup**, and unlike G7.2's forked ref it cannot be repaired by resolving an id
collision — the file has to parse before anything else can key on it. Note the
resolution order this forces: **repair the frontmatter, then backfill the
mint_id, then grid-commit** — and take a copy of the malformed file into the
goal's own record first, since repairing it is what destroys the fixture.