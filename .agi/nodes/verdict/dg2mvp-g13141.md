---
id: verdict:dg2mvp-g13141
mint_id: 6f0c8a56756147648041a937eae5a210
type: verdict
parents:
  - experiment:dg2mvp-g13141-check
  - hypothesis:g1314-dg5-01-corrective-one-load-one-check-one-resolver
next_edges: []
confidence: 0.84
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-g13141-check
scaffold_hash: 094c47d3abc5d07c
season: 2
title: "goal:g1.31.4.1 post-build as re-scoped (88ddd2ca08): proved 0.84 -- one graph load + one target check per render and dry-dispatch path, dry == live target on an 18-cell matrix, --branch dry resolves inside a linked worktree, ZoomUnavailable = rc 1 + one ERR block at 4 sites; dropped conjunct routed to g1.31.4.1.1; ceiling over (recorded DH.DG3.56); 1 inherited red (advisor row)"
town: core
verdict: proved
---
# verdict:dg2mvp-g13141

## g13141 verdict: goal:g1.31.4.1 build satisfies its hypothesis (as re-scoped)

Every measured conjunct holds at HEAD and no falsifier fires (F1 1 load per small/parent render; F2 auto+bogus rc 1; F3 one has_node(target) inside target_resolves; F4 no caveat module or test; F5 no dry nonce, no line cite). One graph load and one target check per dry dispatch and per render path (call counters, probe1.py); dry == live target refusal on a 18-cell tier x level x target matrix with the live side driven through zoom_command up to the spawn, every target cell agreeing; `--branch --dry-run` from inside a linked worktree resolves branch, base and main-rooted worktree path correctly and reads the dispatcher's own checkout both ways; ZoomUnavailable surfaces as rc 1 + an ERR block, 0 tracebacks, at all four sites.
The one conjunct not judged is the dropped one, ROUTED to goal:g1.31.4.1.1 (horizon): "a --branch dry run reads the graph a live --branch spawn renders from". That is a routing, not a disproof; it is why the round's own verdict read lean_disproved:80.
CEILING: over as a chain, known and recorded. adb1bd23fd..e22a38df4c production NET +38 vs +10, tests added 138 vs 70 (hypothesis node DH.DG3.56 already states "the chain was +40 vs +10"); the corrective slice itself held its cap (production -2 vs <= 0, tests net +19 vs <= +20).
Tests: 7 of 8 files green; the one red (advisor-row in test_dispatch_dry_run) is identical on the base tree, INHERITED, already named in DH.DG3.56 item 6. The "1 inherited red in test_dispatch.py" on the DG3 card did not reproduce: test_dispatch.py 139 passed here.
Observations, not conjunct gaps and not raised as correctives (none is an SM/DG3 card residue, all are outside the claim): (a) dry exits 0 for `--tier parent` with a big draw / `--level big`, where live zoom.py refuses ("--tier parent has no shape at --level big"), a tier/level refusal that predates the build; (b) dry `--branch` on a detached HEAD prints `base=NONE (...)` and exits 0, live exits 1; (c) live branch_worktree_for_spawn resolves git_common_root twice at base and at HEAD (second via guard_cell in ram_worktrees_dir, g7.16.1.5.4 code), so "one per spawn" holds for the dry --branch run (DH.DG3.56 item 3) and is unchanged for live; (d) a malformed config.json gives a JSONDecodeError traceback in zoom and dry (not a ZoomUnavailable). If the owner wants them closed, (a) and (b) fit under goal:g1.31.4.1.1.
No strict-xfail rows exist for this row (none in git history of the two files).
