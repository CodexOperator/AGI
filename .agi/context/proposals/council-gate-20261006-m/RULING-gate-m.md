# ONE ruling — gate-m (council-gate-20261006-m) — DESIGN batch

**Pen:** self-perpetuating · **Lenses:** alive · all-is-one  
**Designs:**  
- `DESIGN-g5.4.1.1.7.1-links.md` (mint `d8cfce1346734d8aa7337ea3f291c996`)  
- `DESIGN-g5.4.1.4.1-bin-suite.md` (mint `827bebf1396745d68cf0241522bf3c82`)  
- `DESIGN-g5.4.1.2.1-stack.md` (mint `0235a7a317b743edb3b20a0318a629b1`)  
**Lens note:** `LENS-all-is-one.md`  
**SM tip:** posts/sanctuary-master `db3597c32` (design leaves @ `ae3c22f4f`) · Belam mint tip `501144233`  
**Ask:** `sm-council-ask-20261006-m.md`

## Verdict

**PASS** — all three designs sufficient for later DG / suite-grant leaves. **DG held** until parent SM gate. **Do not box Belam.** No suite window from this ruling. No rollover `--apply`. Season3 tip untouched. Capsule `fda4efd6e` stands.

## Must-carry (short) — all three leaves

### g5.4.1.1.7.1 — links
1. Retarget `payload_ref` (not full retire) for all three builds → deprecated/ paths where bytes sit:  
   - `build:bin-season` `2e990ee…` → `extensions/agi/deprecated/bin/season.py`  
   - `build:tests-test-season` `e84b2e52…` → `extensions/agi/deprecated/tests/test_season.py`  
   - `build:tests-test-mail-alert` `e4d37e3c…` → `extensions/agi/deprecated/tests/test_mail_alert.py`
2. Writer: engine.v4 Write/Edit + agi-turn (or named deprecate/repoint if already in graph).
3. Falsifier: `links.py links` — those three not BROKEN; ZERO leftover notes; never git rm.

### g5.4.1.4.1 — bin-suite
1. Suite path: `verification.py window` then `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/<file>.py -q` (one committed file); clear via `commands.py run verify` → bin-suite-fresh PASS.
2. Lock: `.agi/sessions/<values.core.suite_lock.file>` (today `verify-suite.lock`); free = absent in MAIN and every post worktree; never merge while suite runs.
3. **Prime grants ONE suite window**; DG may operate pytest under that grant; probe never rotate/heal/send/dispatch.
4. NO suite window from this ask; ZERO leftover notes; no waive footnote.

### g5.4.1.2.1 — stack (refresh)
1. Carry owner 8-point intent verbatim: hard-move off tip + grid-as-graph stats; mint_id = true link; stay deprecated; bake metrics (config:metrics; deprecated COUNT; retired do not); overview archive + payload refs + `slice_ref: refs/slice/season-N-archive`; `core/season2/main` → trunk under `core/main` (design only; owner GO to execute); no node lost / never git rm; **NO --apply**.
2. Vertical procedure named in `DESIGN-g5.4.1.2.1-stack.md` (per-node grid branches; hard-move; overview shape).
3. Align metrics with g5.36.1; slice hook with g5.4.1.3.1 — do not reopen those PASS leaves.

## Residues (non-blocking)

- agi-all-is-one verify PermissionError on smoke/budget/anonymize (`.env` / spawn-budget) — post ACL, not these leaves.
- Non-BROKEN “→ none” experiment/hypothesis link lines outside the three builds — out of scope.
- Exact operator for post-land suite catch-up (Prime grant vs Belam ops) → parent SM gate / land notes.
- `core/season2/main` archive cut remains separate owner GO.

## Ready-for-gate

Council PASS complete for gate-m batch. **Parent runs SM gate next.** This package does **not** mint DG leaves, does **not** wake Belam, does **not** open a suite window, does **not** run rollover, does **not** touch season3 tip `4b8f28b5e` / capsule `fda4efd6e` / g5.4.1.3.2 / g5.34.10.2.

## Out of scope

Prime build · DG builds before PASS+SM gate · season3 origin reset · stray-head deletes · waive-as-footnote · git rm · reopen g5.4.1.3.2 / g5.34.10.2 · `--apply` rollover
