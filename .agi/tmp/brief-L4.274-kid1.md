# L4.274 kid brief — hypothesis:l4-the-dry-run-chain-line-is-tested-hermetically

You are the ONLY kid. Implement the amended build order on the target node.
THIS IS A BUILD ROUND, NOT A MEASUREMENT ROUND: ship the code change AND the
tests. A round that only reproduces the defect and reports `disproved` is a
FAILED round.

## What is already true on this tree (measured by the parent, 2026-09-11)

- `extensions/agi/bin/rotate.py` cmd_rotate_self: the LIVE Belam cap is gated
  `if role == "prime_director" or getattr(args, "belam_prefix", None):`
  (line ~5606) and reaps at ~5794 (`handover["belam_cap"]["oldest_to_reap"]`).
- The DRY-RUN (r5) Belam cap plan is INSIDE `if is_chain_seat:` (line ~5389).
- `is_chain_seat = (role == "prime_director")` (line ~5172).
- Therefore a PLAIN seat run with `--belam-prefix <pfx>` reaps live but its
  `--dry-run` prints NO (r5) plan. That is the defect.
- `_descendant_chain` (line ~3048) returns the chain SHALLOW->DEEP (deepest
  LAST; BFS). `_reap_chain` (line ~3204) TERMs `reversed(pids)` =
  deepest-first. The dry-run currently prints `chain!r` as returned, i.e.
  shallow->deep, while the same line says `TERM'd DEEPEST-FIRST`. Order
  printed != order executed.
- `extensions/agi/tests/test_rotate_selfreap.py` already has
  `test_plain_seat_dry_run_resolves_own_id_touches_nothing` (~525) and
  `test_chain_seat_dry_run_prints_fifo_plan_touches_nothing` (~564), and
  `test_dry_run_enumerates_s2_s12` (~235) asserts HEADINGS ONLY — it never
  asserts the pids/chain lines. Existing hermetic seams in the file:
  `_ps_table(monkeypatch, table)` (~61), `monkeypatch.setattr(rotate,
  "_pane_pid", ...)` (~421), and the `windows.txt` file passed as
  `window_path` (tmux display/list are read from it).

## Clauses to IMPLEMENT (all three)

1. **Hermetic exact-line tests.** In `test_rotate_selfreap.py`, add hermetic
   tests (same `_ps_table` / `_pane_pid` monkeypatch / `windows.txt` seam)
   that assert the EXACT dry-run lines, not headings:
   - PLAIN seat: own `@id` (resolved from the CURRENT `<seat>` window, never
     from the `.genN` rename target) + the pane pid + the derived chain.
   - CHAIN seat (`role="prime_director"`): the OLDEST predecessor + its `@id`
     + the derived chain.
   Deriving from a real `_ps_table` is fine; monkeypatching `_pane_pid` and
   `_descendant_chain` is fine. The test MUST be hermetic: no tmux, no real
   `ps`, no real kill.
2. **Plain seat with `--belam-prefix` prints the (r5) cap-reap plan it WOULD
   run.** Mirror the LIVE gate, not `is_chain_seat`: print the (r5) plan
   whenever `role == "prime_director" or getattr(args, "belam_prefix", None)`,
   derived read-only through the SAME `_belam_oldest(...)` call path the live
   path uses (~5606 → ~5794). Touches nothing (no window write, no kill, no
   rotation record — the existing dry-run tests assert exactly this; keep
   that property for the new case too). Assert it hermetically, with a
   `_pane_pid` + `_descendant_chain` (or `_ps_table`) that yields a real
   chain so the printed line carries pids, not the named skip.
3. **Print the chain in the order it would be TERM'd.** The printed chain
   must be DEEPEST-FIRST under the `DEEPEST-FIRST` label (the order
   `_reap_chain` actually signals: `reversed(chain)`). Pick one and make it
   coherent: print `list(reversed(chain))` and keep the label, OR print the
   chain with an explicit "shallow->deep" label. Prefer deepest-first print,
   because the label already claims it. The hermetic test must PIN the order
   so that a `_descendant_chain` patched to return the chain reversed makes
   the test FAIL (that is the node's stated falsifier).

## Falsifiers you must make the tests catch

- a plain-seat `--belam-prefix` dry-run that prints no (r5) plan while the
  live path would reap;
- a test that passes with `_descendant_chain` patched to return the chain
  reversed (i.e. an order-blind assertion).

## FILE SCOPE (hard)

- `extensions/agi/bin/rotate.py` — ONLY the dry-run r4/r5 block of
  `cmd_rotate_self` (today ~5385-5475) and, if the plain-seat r5 print needs
  it, nothing else. Do NOT re-indent, do NOT touch first_turn/bootstrap/
  spawn/handoff/prepare/status: those regions are being edited live by the
  sensei-director's SL1.02/SL1.04 rounds. Do NOT touch the live r5 block.
- `extensions/agi/tests/test_rotate_selfreap.py` — only added/extended tests.

EXCLUDED: every other file, every other region of rotate.py, clause (4)
(`_restore_shield_signals` in a `finally`) — deferred by the parent, do NOT
do it.

## Evidence

- Run `python3 -m pytest extensions/agi/tests/test_rotate_selfreap.py -q` and
  paste the real count + your new test names in the node.
- Prove the falsifier: mutate `_descendant_chain`'s return (or patch it
  reversed) and show your order assertion goes RED; then restore. Report both
  the red and the green run.
- The node's verdict must be one of
  `proved | disproved | inconclusive_lean_proved:N | inconclusive_lean_disproved:N | pending`.
  `proved` REQUIRES `evidence_runs` to be a LIST of node ids that exist.
- Report `DONE <node-id>` with `caveats:` and `struggles:` lines.
- Do NOT git commit / push / sync. The loop owns git.
