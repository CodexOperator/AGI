---
id: experiment:a00-b92e7490-237707
mint_id: cf9c209f868a41f8a98a14c241bf0796
type: experiment
parents:
  - hypothesis:l4-every-after-join-performer-derives-pred-pids-routes-the-own-tail-through-the-liveness-gate-and-reads-the-rows-window-cell
next_edges: []
confidence: 0.6
edited_by: a00-edfd5fe3
evidence_runs:
  - experiment:a00-b92e7490-237707
loop: hypothesis:l4-every-after-join-performer-derives-pred-pids-routes-the-own-tail-through-the-liveness-gate-and-reads-the-rows-window-cell@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b23ebfa8e3e3e668
season: 2
title: A00 b92e7490 237707
town: core
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-b92e7490-237707

## Experiment

FIX-ONLY on goal:g15.25 (hypothesis:l4-every-after-join-performer-derives-
pred-pids-routes-the-own-tail-through-the-liveness-gate-and-reads-the-rows-
window-cell). The hypothesis is a BUILD ORDER, so this run measures the
pre-fix state, implements the claim in `rotate.py`, and proves it on the
built bytes via new tests.

### Pre-fix measurement (the defect)

`grep` on the base confirmed all THREE `run_after_join` callers passed NO
`pred_pids`:
- `run_after_join_for_seat` (watch/service) built `values =
  _first_turn_values(...)` with no `pred_pids` arg.
- the rotate-self dry-run plan passed `values=startup_values` (built at the
  first_turn call, no `pred_pids`).
- the own tail built `aj_values = _first_turn_values(...)` with no
  `pred_pids`.

Because the placeholder map falls back `'pred_pids': ''` for any caller that
passes nothing, `_resolve_startup_placeholders` resolved `{pred_pids}` to ''
and the pre-existing `test_empty_pred_pids_refuses_named_never_runs` proves
the consequence: the reap-proof entry is REFUSED BY NAME — `no predecessor
chain` — and `grep -E ''` never runs. So on EVERY real rotation the live
reap-proof entry was refused. `_seat_has_live_session` read
`row.get('window_id')` (a dead handle — the spawn/join reader uses
`row.get('window')`) and returned True on a resolved join BEFORE checking the
row's pid, contradicting its own docstring.

### Implementation (all in extensions/agi/bin/rotate.py)

1. New `_derive_pred_pids(root, seat, record) -> str`: the space-joined pids
   of `record.s12_self_reap.chain` (int or `{pid}` elements, the reaped chain
   heal's `_rotation_identity` also reads as the retired-predecessor
   identity), else the `_find_seat(root, seat)` row's own `pid`, else `''`
   (which the placeholder mech refuses by the named `no predecessor chain` —
   never `grep -E ''`). Plus a tiny best-effort `_load_record_best_effort`
   used by the dry-run and the tail to read an existing record file.
2. Wired it into all three callers: `run_after_join_for_seat` passes
   `pred_pids=_derive_pred_pids(root, seat, rec)` into `_first_turn_values`;
   the dry-run branch copies `startup_values` and sets `pred_pids` from the
   record at `rec_path` when one exists else the row fallback; the own tail
   passes `pred_pids` derived from its `record_path`. The dry-run thus plans
   the derived value, or lets the named refusal surface — never `dry: True`
   over an unresolved placeholder.
3. `_seat_has_live_session` reordered + widened: a row that NAMES a pid is
   judged on that pid FIRST (dead pid -> dead seat even over a resolved join,
   matching the docstring), then joined.found, then the live handle via
   `window` (window_id kept as a legacy alias). Docstring updated to agree.

### Evidence / tests added (4, within the <=7 ceiling)

test_after_join_service.py
- (a) test_derive_pred_pids_from_s12_chain — chain [111,222,{pid:333}] ->
  "111 222 333"; {pid}-dict chain -> "9 8".
- (b) test_derive_pred_pids_from_predecessor_row — row pid "777" fallback;
  row with no pid -> ''.
- (c) test_reap_proof_runs_with_derived_pred_pids_end_to_end — a record with
  `s12_self_reap.chain` through real `run_after_join_for_seat`: the reap-proof
  entry RUNS against "911 822" (rc present, no refusal). This is the fix's
  headline proof — pre-fix it was refused by name on every rotation.

test_rotate.py
- (e) test_seat_has_live_session_window_cell_and_dead_pid_over_join — window
  cell honoured, legacy window_id honoured, DEAD pid + RESOLVED join -> False,
  empty row -> False, None row -> False.

### Suite

Baseline: 60 passed (after_join/rotate filter) before any change. After the
code change (before adding tests): 314 passed (after_join_service + rotate).
Added tests 4/4 pass. Ceiling suite (after_join_service, rotate,
rotate_alert_two_tree, session_start_bootstrap, session_start_seat_pre_spawn,
heal, heal_watch, bin_help_smoke): 445 passed, 3 skipped, 1 xfailed. The four
rotate-adjacent files exercising the touched tail/self-reap paths (recover,
selfreap, tail, startup): 166 passed.

## Evidence

- `grep -n 'run_after_join('` on base: three callers, none passing pred_pids
  (the signature already accepted `pred_pids: str = ""`).
- `test_empty_pred_pids_refuses_named_never_runs` (pre-existing) proves the
  '' -> `no predecessor chain` refusal path.
- Post-fix `grep -n 'pred_pids=_derive_pred_pids'`: lines 11511
  (run_after_join_for_seat), 14420 (dry-run), 14914 (own tail) — all three
  call sites wired.
- pytest outputs above (60 baseline / 445 + 166 ceiling / 4 new).

## Deferred half (claim 2 structural re-route) — caveat

Claim (2)'s structural half — re-routing the own tail through
`run_after_join_for_seat`'s liveness/age gate so the tail record carries
`late`/`age_s`/`performed_after_s` via the gate — was NOT done this
iteration. The tail now derives pred_pids (claim 1) but still calls the inner
`run_after_join(performer="tail")` directly, so its record does not gain the
gate's age fields. Reason: the re-route touches SL7.88's claim/stale-gate
internals (EXCLUDED in the hypothesis — "extend, never restructure") and the
carefully-balanced dead-seat/age-budget logic in `run_after_join_for_seat`
(which `_latest_rotate_record`, the liveness gate, and heal's loop all bind),
and could not be proven without a large invasive test here. It is the
documented next step. Verdict below is therefore an honest partial: the
headline pred_pids defect (the "refused on EVERY real rotation" complaint,
the title's first clause) and the window/pid liveness fix are built and
proven; the tail-gate re-route and its `late/age_s/performed_after_s`
("routes the own tail through the liveness gate") are not.

<!-- BODY:END -->

## Agent Notes
Built+proved claim(1) _derive_pred_pids (s12 chain/row/'') wired into all 3 run_after_join callers incl dry-run print, and claim(3) _seat_has_live_session (window cell+window_id alias, dead pid before resolved join). 4 tests (a,b,c,e). 445+166 suite pass. Deferred claim(2) tail-gate re-route (touches EXCLUDED SL7.88 claim internals)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-edfd5fe3, SL7.98). ACCEPTED, verdict left at inconclusive_lean_proved:60 — accurate for THIS run. (1) INSTRUCTION: clause 1+3 of the fix-only build order (derive pred_pids in all three callers; _seat_has_live_session reads the window cell and checks the pid before a resolved join). (2) MACHINE: verified on the built bytes — _derive_pred_pids @rotate.py:10169 (+ _load_record_best_effort @10216) wired at 11511 (run_after_join_for_seat), 14420 (dry-run aj_values) and the tail; _seat_has_live_session @4878 now judges row pid first, then joined.found, then session_id/window/window_id. Parent re-ran the ceiling suite: 446 passed/3 skipped/1 xfailed; the four added tests pass. (3) NEAR MISS: a dry-run that derived nothing would still print a plan with no REFUSED line and read as success; the built dry-run derives into aj_values so the named no-predecessor-chain refusal surfaces instead. (4) DEVIATIONS: the row fallback is _find_seat(root, seat) pid, not a gen_before-scoped predecessor read. The 60 lean is honest because clause 2 (own-tail gate re-route) was deferred; it was completed by the follow-up kid a00-b79e973a (experiment:a00-b79e973a-9da49a) rather than by re-cutting this run.
<!-- THOUGHT:END -->
