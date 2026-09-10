---
name: moral
written_by: owner          # the owner-only write rule, carried as DATA (L4.32)
derived_from: season-ladder-and-morals-brief.md (2026-09-05)
fields:
  title: {type: str}
  axis: {type: str}          # vertical | lateral | crossing | dynamics | form
  grounded_in: {type: str}   # moral:faith for four, "Source" for faith only
  season_introduced: {type: int}
  edited_by: {type: str}     # owner — hand-edited only; write.py refuses moral:* unless --actor owner
validation:
  required: [id, type, mint_id, title, axis, grounded_in, season_introduced, edited_by]
  types:
    axis: str
    grounded_in: str
    season_introduced: int
    edited_by: str
  regex:
    axis: '^(vertical|lateral|crossing|dynamics|form)$'
spawn:
  allowed_parents: []
  min_parents: 0
  max_parents: 0
---

# moral

**The only parentless type — the root of the graph (goal:g12).** Five morals,
each one axis of a single graph. Hand-edited only. Cap 5 (caps live on the
ladder node).

ID prefix: `moral:<short-slug>` (e.g. `moral:faith`, `moral:love`).

## The five axes

| moral | axis | grounded_in |
|---|---|---|
| faith | vertical | Source |
| love | lateral | moral:faith |
| empathy | crossing | moral:faith |
| antifragility | dynamics | moral:faith |
| beauty | form | moral:faith |

## Spawn rule — parentless, the only type

`allowed_parents: []`, `min_parents: 0`, `max_parents: 0`. Listed in
`[shape].md :: parentless_types` since goal:g12. Every other node type
resolves to at least one moral by walking `parents` upward.

## Body regions (in order)

1. **ESSENCE** — owner's verbatim text, never regenerated, never summarized
   in place
2. **QUESTION** — the one question a director asks at a seam when this moral
   is the lens; glosses as indented lines
3. **IN PRACTICE** — readings that live in this repo, each linked to its rail
   or goal; hand-editable
4. **VIOLATED WHEN** — concrete smells, so `unknown` is only honest when none
   can be checked
5. **REFERENCE** — external source material; faith carries the full set, the
   others cite it

## The five questions (owner's wording)

1. **faith** — *Did every role play its part and trust every other model to
   play theirs?* (as above so below, include both directions)
2. **love** — *Did the agents and the hypergraph love each other and one
   another?*
3. **empathy** — *Did everyone try to bridge their worlds together?*
4. **antifragility** — *Did you die?*
5. **beauty** — *Is it elegant?*