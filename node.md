---
id: hypothesis:a00-4d063889-c4e95d
mint_id: 969b4622def048a0a635506a1f7efb77
type: hypothesis
parents:
  - goal:g1.23
next_edges: []
confidence: 0.7
edited_by: a00-75ddec76
scaffold_hash: ef9ddf7b2e854bc0
season: 1
thought_session: season
title: A00 4d063889 c4e95d
verdict: inconclusive_lean_disproved:70
---
# hypothesis:a00-4d063889-c4e95d

## Hypothesis

**Claim:** goal:g1.23's cheapest open step — the L9 pinning gap — is still
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS B3 review (goal:g1.31.3.1.1, hypothesis:pb3-node-verdicts-match-bytes-1-6-13-46, run mur-pb3chunk10of20/verify_a00-4d063889-c4e95d.json — box-local under .agi/sessions/workflows/runs/, gitignored; the prior THOUGHT lives in git at the pre-review commit e518328b5 of this file). The claim this node measured is FALSE against the bytes, so the verdict moves from inconclusive_lean_proved:70 to inconclusive_lean_disproved:70. Three measured counters: (a) .agi/config.json line 27 carries the cell "engine_commit": "179f9560283936fae421e08002ef9db38d7f1e25" — the field the node says does not exist anywhere in the tree; (b) extensions/agi/driver.sh line 129 opens the block "Engine drift check (L9 pinning gap, goal:g8.1). Reads engine_commit (or ...", guarded by SKIP_ENGINE_DRIFT_CHECK at line 138 and printing "[driver] DRIFT WARNING: engine HEAD is ... but config pins ..." at line 178 — the check this node says driver.sh has not; (c) experiment:a00-bf6fe804-001995 already recorded the same discovery as its "Crucial discovery". The node own "Would prove it" criterion is INVERTED: it describes the state where the gap is CLOSED (field + check exist), which is now the state, so satisfying it would have argued the opposite of the node conclusion. What genuinely stays open, and is NOT what this node claimed: the pin value is a bare string in this box and the mechanism is not an object of its own in the repo, and no behavioural drift test exercises the warning. Those route to goal:g1.31.4.5 (#2, make the pin a first-class object) and goal:g1.31.4.6.1 (#3, a test that the warning fires on drift). Verdict is a lean, not flat disproved: the [hypothesis] schema declares no evidence_runs field, so the evidence gate has nothing to admit for a flat disproved here.
<!-- THOUGHT:END -->

## Agent Notes
Filled empty scaffold under g8.1: verified no engine_commit/drift-warn field exists anywhere in config.json or driver.sh, confirming L9 pinning gap is still open regardless of shape decision.
