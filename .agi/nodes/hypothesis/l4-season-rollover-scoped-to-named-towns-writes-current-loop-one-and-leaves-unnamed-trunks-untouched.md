---
id: hypothesis:l4-season-rollover-scoped-to-named-towns-writes-current-loop-one-and-leaves-unnamed-trunks-untouched
mint_id: 28f1fc8b2477491899cc0bf5df8696e8
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 0a431e3c89eb366c
season: 2
testable_claim: "(1) season.py rollover --global accepts --towns <slug,...>: the alignment check applies to the named towns only (a named misaligned town still refuses by name), the unnamed towns' trunks, cells and season_history are untouched byte-for-byte, and the global trunk + master fold happen exactly as the unscoped mode does. (2) the rollover writes current_loop: 1 in the same deferred cell pass that writes current_season: 3 (owner 15:0xZ: a fresh season restarts the loop count), so the first Prime rotation after it names belam-S3-L1-I (SM.118's resolver). (3) --dry-run prints every ref cut/fold/archive and every cell it WOULD write, and writes nothing: refs and nodes byte-identical before/after, measured. (4) the real run is ONE command the Prime names on his [decision] line; the kid never runs it with --apply against origin -- the apply proof runs in a throwaway clone (tmp) of the live repo, and the experiment records the exact command, the refs it created there, and the cells it wrote."
title: "SM.119 (owner 14:5xZ + 15:0xZ, Prime 19:39Z/19:49Z, doc:s3-plan PRE-S3 \"SM.115\"): SEASON ROLLOVER 2 -> 3 scoped to the Prime's and the core-town branches -- season.py rollover --global --towns core,sanctuary cuts season3/main and the two town trunks, folds, archives, writes current_season 3 AND current_loop 1, and leaves local-maxxing / streaming-suite / web-app-suite trunks and cells byte-identical; PREPARED now (dry-run + tests), EXECUTED only on the Prime's [decision] line after SM.117 + SM.118 land"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-season-rollover-scoped-to-named-towns-writes-current-loop-one-and-leaves-unnamed-trunks-untouched

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.119 BRIEF (sanctuary-master 20:0xZ 09-18). MEASURED NOW: season.py rollover --global --dry-run REFUSES on this tree: "town(s) local-maxxing, streaming-suite, web-app-suite not at global season 2 -- align first" (cmd_rollover_global L1275-1330: --town with --global refused, a town never rolls alone; trunks = ladder + every declared town; cells written in a deferred pass after every trunk verifies). Town cells today: core 2, sanctuary 2, local-maxxing 1, streaming-suite 1, web-app-suite 1; ladder current_season 2, current_loop 5. DEVIATION recorded here: owner 02:2xZ ruled "a town NEVER rolls alone"; owner 14:5xZ ruled the rollover "can just be for your branch and sanctuary master, let thought master work on his branch independently until tomorrow's check in" -- the newer ruling wins; --towns is the scoping the newer ruling needs, and the unscoped mode stays the default. SHAPE: --towns parsing + subset in cmd_rollover_global (~10 lines), current_loop in the ladder cell pass (~3), dry-run print of refs + cells (~5). CEILING 25 production lines. TESTS (test_season_rollover_scoped.py, throwaway git repos): (1) --towns subset proceeds while an unnamed town is misaligned; (2) unnamed town trunk + cell + history byte-identical; (3) current_loop -> 1 with current_season -> 3; (4) a named misaligned town refuses by name; (5) dry-run writes nothing. EXECUTION: NOT in this round -- the Prime runs the one command on his word after SM.117 + SM.118 land; the experiment ships the exact command line. FILE SCOPE: season.py + one test file; never the ladder or town nodes on a live branch. Deliver batch + review in ONE line; foreground-wait every kid.
