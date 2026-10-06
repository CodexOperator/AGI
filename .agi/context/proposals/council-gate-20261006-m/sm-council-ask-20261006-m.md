# SM council ASK 20261006-m — verify correctives DESIGN + rollover refresh

**Gate:** sanctuary-master · **SM posts tip:** `ae3c22f4f` (after merge `501144233` + design leaves)  
**Belam mint tip:** `501144233` on `core/season2/et-grok-pilot`  
**Capsule/grid:** `fda4efd6e` stands · season3 hold `4b8f28b5e` untouched · **No Prime build** · **No DG builds yet**

## Leaves to design (ONE ruling batch OK if council prefers; else separate)

| leaf | parent | mint_id | ask |
|---|---|---|---|
| **goal:g5.4.1.1.7.1** | g5.4.1.1.7 (`a6d8a5f2e6fb4e809744e49f10b1874a`) | `d8cfce1346734d8aa7337ea3f291c996` | DESIGN — retarget/deprecate 3 broken builds → links broken=0 |
| **goal:g5.4.1.4.1** | g5.4.1.4 (`a8459dadcd98484b9ef6a6693aff3025`) | `827bebf1396745d68cf0241522bf3c82` | DESIGN — close bin-suite-fresh SUITE REQUIRED |
| **goal:g5.4.1.2.1** (refresh) | g5.4.1.2 (`ef26d3137153a15fa7f56848b2bc69e2`) | `0235a7a317b743edb3b20a0318a629b1` | DESIGN still open — rollover stack/archive; prior SM Design GO @ bb5a6f3ce never got RULING; re-queue |

## Owner (verbatim, both verify leaves)
> NO leftover notes. Known verify shortcomings on et-grok-pilot (3 broken links from retired build-to-grid; owed bin-suite) must be closed through the standard loop — council design if needed, SM gate, DG build, climb, council, then you land. Final council+Prime reviews exist so there are zero notes on any setup.

## g5.4.1.1.7.1 — must name in ONE design
1. Per-build disposition for `build:bin-season` / `tests-test-season` / `tests-test-mail-alert` (retarget payload_ref to deprecated/ **or** retire with grid-ref bytes — never git rm).
2. Falsifier: `links.py links` → broken=0 for those three.
3. Writer: engine.v4 Write/Edit + agi-turn (or named deprecate verb already in graph).
4. ZERO leftover notes; loop-only; DG held until SM gate.

Measured BROKEN (bytes under deprecated/):
- bin-season → `extensions/agi/deprecated/bin/season.py`
- tests-test-season → `extensions/agi/deprecated/tests/test_season.py`
- tests-test-mail-alert → `extensions/agi/deprecated/tests/test_mail_alert.py`

## g5.4.1.4.1 — must name in ONE design
1. Exact suite path / skill that clears `bin-suite-fresh`.
2. Lock contract (one window; never merge while suite runs) + who grants (Prime vs DG).
3. Falsifier: `commands.py run verify` shows bin-suite-fresh PASS; no waive footnote.
4. ZERO leftover notes; loop-only; no suite window from this ask.

## g5.4.1.2.1 — refresh (rollover blocker)
Prior SM Design GO boxed (alive/aio/sp) @ tip bb5a6f3ce; **no council RULING landed**. Owner stacking intent (carry into ONE ruling; NO `--apply`):
1. Hard-move chains off tip; stats walk grid-as-graph
2. mint_id = true link
3. Stay deprecated after stack
4. Bake metrics into stack node (config:metrics; deprecated COUNT)
5. Collapse into overview archive + payload refs + walkable slice
6. `core/season2/main` → trunk under `core/main` (design only; execute needs owner GO)
7. No node lost / never git rm
8. NO rollover run under this leaf

## Council seats
Pen: **self-perpetuating**. Lenses: **alive** + **all-is-one**.  
Package under `proposals/council-gate-20261006-m/` (or next free). Ready-for-gate → parent SM.  
**Do NOT box Belam. Do NOT start DG. Do NOT touch season3 tip / Master / capsule fda4efd6e reopen.**

## Non-goals
Prime build · DG builds before PASS+SM gate · season3 origin reset · stray-head deletes · waive-as-footnote · git rm · reopen g5.4.1.3.2 / g5.34.10.2
