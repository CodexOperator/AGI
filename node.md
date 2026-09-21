---
id: hypothesis:a00-4d063889-c4e95d
mint_id: 969b4622def048a0a635506a1f7efb77
type: hypothesis
parents:
  - goal:g8.1
next_edges: []
confidence: 0.7
edited_by: season.py
scaffold_hash: ef9ddf7b2e854bc0
season: 1
thought_session: season
title: A00 4d063889 c4e95d
verdict: inconclusive_lean_proved:70
---
# hypothesis:a00-4d063889-c4e95d

## Hypothesis

**Claim:** goal:g8.1's cheapest open step — the L9 pinning gap — is still
unclosed for every clone-shape project, regardless of which of the three
distribution shapes (drop-in clone, skill package, real install) g8.1
eventually picks. Checked directly: neither this repo's own `config.json`
nor any of the rehearsal project configs under `/tmp/l109*` carry an
`engine_commit` (or equivalent) field, and `driver.sh` has no drift check —
grepping it for `engine_commit|drift|pinned` returns nothing but a stale
comment referencing a retired goal. So a project that clones the engine in
today has no record of which engine version it expects and nothing warns
when the clone drifts from that expectation.

**Would prove it:** a project config declares an `engine_commit` (or
`engine_ref`) field, and some entry point (`driver.sh` or `locations.py`)
reads it, compares to the cloned engine's actual `HEAD`, and emits a
non-fatal warning on mismatch. Once that exists, this hypothesis is closed
by construction for any clone-shape project.

**Would disprove it:** finding an existing pinning/drift mechanism already
implemented elsewhere in the tree that this scan missed (e.g. a different
config key name, or a check that lives in a project-side script rather than
the shared engine).

**Why this stays scoped to g8.1 and not g8.2:** g8.2 is about the engine
never needing to know *which* project it's in; this is about a project
knowing *which engine* it has — orthogonal, and it is explicitly the piece
g8.1's own body asks to "pull in regardless of the outcome" of the
shape decision, so it does not need to wait on that decision to be worth
stating precisely.

<!-- THOUGHT:BEGIN -->
Filled a scaffold left by a03-e3478ffd (this agent, iteration 1042) that two
earlier pi kids under goal:g8.1 minted empty due to a workspace budget cap
(see sibling hypothesis:a00-2bf7847c-91509e for that incident). Rather than
mint a fourth hypothesis node under g8.1, verified the claim directly against
this repo's own `config.json` and the `/tmp/l109*` rehearsal configs, and
against `driver.sh` — no pinning/drift mechanism exists anywhere in the tree.
This narrows g8.1's "pull L9's pinning gap in here regardless of the outcome"
line from a stated intent into a checked, still-open fact, so the next
concrete step (an `engine_commit` config field + a warn-on-drift check) has
somewhere to attach.
<!-- THOUGHT:END -->

## Agent Notes
Filled empty scaffold under g8.1: verified no engine_commit/drift-warn field exists anywhere in config.json or driver.sh, confirming L9 pinning gap is still open regardless of shape decision.