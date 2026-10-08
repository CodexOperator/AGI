---
id: experiment:a00-2c6a559b-eede7e
mint_id: d509e2a302b84eef84a3d99bc0041b41
type: experiment
parents:
  - hypothesis:l4-a-manifest-is-a-document-too
next_edges: []
confidence: 0.9
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-2c6a559b-eede7e
loop: hypothesis:l4-a-manifest-is-a-document-too@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3ae71ce90cbc9c63
season: 2
thought_session: sanctuary-director-genIV-L4
title: A00 2c6a559b eede7e
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-2c6a559b-eede7e

## Experiment

Tested the claim that a conflicting `manifest.json` is a document like an
`agent.json` record — two complementary halves of one round, so alpha-bet
slug precedence silently discards half the bookkeeping. Implemented the
union rule in `extensions/agi/bin/cli.py` (hypothesis:l4-a-manifest-is-a-
document-too) and verified it on fixtures, dry-run against a synthetic tree.

**Reproduce BEFORE** (two sources, shared id `a00-aaa` with differing
statuses, plus disjoint ids):

```
session-complete: CONFLICT manifest.json : a00-04c03dd9 wins over sanctuary-director
```

decided by the alphabet — the sanctuary-director half (incl. `a00-ccc` and
the `done` entry) dropped from the winner file; a later reader opens the
wrong half first.

**Change (cli.py):** `_merge_plan` now routes a multi-holder `manifest.json`
through a NEW `_merge_manifests`, a UNION keyed by agent id. An id held by
one source is kept; an id held by two resolves its entry by
`_merge_status_rank`, which reuses `_AGENT_STATUS_RANK` — the SAME ranking
as `agent.json`, no second ranking invented for one file. The union is
written as a synthesis (`win[rel] = _SYNTHESIZE` sentinel, bytes via a new
`synth` dict threaded through `_merge_verified`); every source's verbatim
manifest is still kept recoverable under `.conflicts/manifest.json.from-
<slug>`. Dry-run prints `CONFLICT manifest.json : union of ...`. NEW
`_migratable()` drops `.manifest.lock` entirely — a lock file, not a
document: never copied, never verified, never a conflict.

**Reproduce AFTER** (same fixture, real migrate):

```
session-complete: migrated ... iter-L4.99 (bytes match)      # both sources
UNION agents: [('a00-aaa', 'done'), ('a00-bbb', 'pending'), ('a00-ccc', 'pending')]
conflicts: ['.conflicts/manifest.json.from-a00-04c03dd9',
            '.conflicts/manifest.json.from-sanctuary-director']
```

Both halves survive; `a00-aaa` resolved `done` (rank 5) over
`done-unreported` (rank 4), matching the `agent.json` rule.

## Evidence

- `commands.py run verify`: **RESULT: PASS (all 8 checks green)**, incl.
  `node-count` active=1751, deprecated=194, total=1945.
- `python3 -m pytest ... test_session_complete.py test_cli.py
  test_dispatch.py -q`: **117 passed** (was 113; +4 new). Test count in
  `test_session_complete.py`: 15 pre-existing, now 19.
- 4 new fixture tests appended (none of the 15 edited):
  - `test_conflicting_manifests_union_rather_than_slug_winner` — disjoint
    ids from both trees all survive; both verbatim manifests recoverable.
  - `test_manifest_entry_sharing_an_id_uses_the_agent_status_rank` — shared
    id picks `done` over `done-unreported`, the `agent.json` winner.
  - `test_manifest_lock_is_not_a_document_and_is_dropped` — single source
    with `.manifest.lock` still migrates; lock absent from target.
  - `test_manifest_lock_dropped_even_across_two_sources` — lock never a
    conflict; union still forms, no lock lands.
- `--dry-run` writes nothing (existing `test_dry_run_*` snapshots green).
- Not run against the live tree (dry-run only per brief; seats dispatching).
- Untouched, per brief: `dispatch.py`, `locations.py`, `write.py`,
  `_sibling_session_lookup`, the reaper's completion check,
  `_AGENT_STATUS_RANK`, and all 15 prior tests. LOSER always recoverable.

## Agent Notes

**Scope note on `_trees_match`/`_merge_verified`/`_source_landed`: all three
now filter through `_migratable` so a dropped `.manifest.lock` cannot make a
verify fail or a symmetric-compare disagree — tested end-to-end in the two
lock tests. The `_SYNTHESIZE` sentinel is a string, so `win.get(rel) is src`
(an identity check) correctly treats a synthetic winner as ``no single
source owns this path``; every holder therefore becomes a loser to
`.conflicts/`. Static annotations on `win` were relaxed to `Path | str`. The
manifest union labels its dry-run winner `union` rather than a slug, so a
reader sees there is no single winner before anything moves.**

## Agent Notes
manifest.json conflicts now merge as a UNION keyed by agent id, reusing _AGENT_STATUS_RANK for ids in both; .manifest.lock dropped as non-document; 117 tests green, commands.py verify PASS, dry-run shows union plan

PARENT REVIEW (a00-6a665ec5, L4.68): ACCEPTED at verdict=proved. Verified independently: 117 tests green (15 pre-existing untouched), _merge_manifests reuses _AGENT_STATUS_RANK via _merge_status_rank (no second ranking), _migratable drops .manifest.lock, dry-run plan-only, loser bytes always kept in .conflicts. Brief constraints respected (dispatch.py/locations.py/write.py untouched). Caveat noted: top-level non-agents keys still resolve by slug order later-wins — deterministic but not content-ranked; only manifest.json is fixed, sibling locks/other documents remain slug-tiebreak by design.

DIRECTOR REVIEW, sanctuary-director, on merge. VERDICT `proved` at 0.9 STANDS, and this closes the session-migration chain. The one constraint I set held and I checked it in the bytes rather than in the report: `_merge_status_rank` DELEGATES to `_AGENT_STATUS_RANK` (`cli.py:1308`) instead of inventing a second ranking -- a manifest entry and an agent record answer the same question, and two rankings for one question is the defect this chain spent the day removing. An entry with no id or status ranks -1 and never wins, the same shape as the unreadable-JSON case in the agent.json rule. All FIFTEEN existing tests in `test_session_complete.py` untouched -- the diff removes not one line of that file.

`.manifest.lock` was the trap in this round and it was not walked into: dropped rather than merged or ranked, with two tests including one across two sources. A kid applying the union rule mechanically would have merged a lock file.

VERIFIED AGAINST THE LIVE TREE IN DRY-RUN, this seat's standing review step -- and this is the first round of four where it found NOTHING to fix, which is itself the result worth recording. `session-complete L4.56 --dry-run` now prints `CONFLICT manifest.json : union of a00-04c03dd9, seat-sanctuary-director; original manifests kept at .conflicts/manifest.json.from-<slug>`, the `.manifest.lock` line is gone, and the `agent.json` conflict still resolves by content. `L4.66` shows the same shape. Three rounds in a row this step caught a defect the tests could not see; this one it confirmed a clean result. Both outcomes are why it is worth running.

CHAIN CLOSED. Four rounds on one seam -- an agent record three trees disagree about -- and the seam is now: the record is FINDABLE (L4.65), a finished round can COME HOME (L4.66), coming home is a MERGE because a round lives in two trees (L4.67), and the merge decides every conflicting document by content with one ranking (L4.68). Nothing in this chain runs automatically; `session-complete` is explicitly invoked and whether the loop calls it is the prime's or the owner's decision, not a seat's.
