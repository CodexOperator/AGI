---
id: outcome:g7-16-1-4-1-w-g-goals-md-retired-closed
mint_id: 350eaead7498443bb714c9652d5862ee
type: outcome
parents:
  - goal:g7.16.1.4.1
next_edges: []
alignment: aligned
confidence: 0.9
edited_by: director-general-1
evidence_runs:
  - mvp:dg3b4-wg1-goals-md-retired
  - mvp:dg3b4-wg2-dead-renderer-retired
  - verdict:dg2mvp-wgR
  - verdict:dg2mvp-l2a
  - verdict:dg2mvp-g7-16-1-4-1-2
judged_against: goal:g7.16.1.4.1
scaffold_hash: 54a2b04ef17a90d4
season: 2
status: closed
title: "OUTCOME goal:g7.16.1.4.1 -- W-G closed: GOALS.md retired with all 6 callers, --from-doc, the migration tools and every stale live mention; smoke rc 0, a clean rotation closeout, SM clean"
town: core
---
# outcome:g7-16-1-4-1-w-g-goals-md-retired-closed

# outcome:g7-16-1-4-1-w-g-goals-md-retired-closed

## Outcome
goal:g7.16.1.4.1 (bundle 4 row W-G, the owner's 17:3xZ 09-29 order to retire GOALS.md) is CLOSED. Every falsifier holds on the bytes. sanctuary-master's re-review is clean, and all three leaves are complete.

| clause | outcome |
|---|---|
| no live code path renders or checks GOALS.md (6 callers) | MET: `git ls-files GOALS.md` empty; `snapshot-goals.py --render` outside tests 0; driver.sh --smoke keeps snapshot + metrics |
| --from-doc and its unlink retire; the goals_file cell and DEFAULT_GOALS_FILE go | MET: --from-doc / from_doc in snapshot-goals.py 0 |
| GOALS.md leaves by git rm of the derived file only; no goal node touched | MET: W-G.1 41107692f + W-G.2 254f58ef7 |
| every reader line names the ONE goal read | MET: 17 GOALS.md mentions in CLAUDE.md, QUICKSTART.md, skills, bin and driver.sh, all retirement pointers (F2 now runs with no exclusion, 3c5abfdc0) |
| node-type schemas name a reader that exists (corrective) | MET: verdict:dg2mvp-wgR PROVED 0.9 |
| the one-repo migration tools (goal:g7.16.1.4.1.1) | MET: unify.py + verify_unified.py (b8d232fc6) and publish-engine.sh (de5507a17) retired with their rows and tests; verdict:dg2mvp-l2a PROVED 0.9 |
| config prose names no retired tool as live (goal:g7.16.1.4.1.2) | MET: DG4 701e9c16c + 1274ad15b; verdict:dg2mvp-g7-16-1-4-1-2 PROVED 0.95 |

## Measures
F1 smoke (DG1, 00:5xZ 09-30): rc 0, node_count 5283 (5045 active + 238 deprecated), broken_links 0 · one clean rotation closeout: the Prime's rotate-self at 02:27Z (belam.20260930T022735Z: success, every step; rotate-out b986a293f touched only the card) and 00:56Z, both after W-G landed · links 5306/0 at close.

## What the loop changed
Retiring GOALS.md surfaced two slower-burning copies of the same fault: a schema and two config nodes naming a retired reader or writer as live. Each became its own leaf, not a note. The rule the bundle leaves behind: when a tool retires, every node naming it as live retires the mention in the same row.
