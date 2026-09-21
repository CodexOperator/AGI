---
id: experiment:a00-67444ebf-8bc24f
mint_id: bc460fda18b44bc8a795616159943e6b
type: experiment
parents:
  - hypothesis:l4-the-dry-run-chain-line-is-tested-hermetically
next_edges: []
confidence: 0.9
edited_by: a00-8512520d
evidence_runs:
  - experiment:a00-67444ebf-8bc24f
loop: hypothesis:l4-the-dry-run-chain-line-is-tested-hermetically@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 959cf5a51d89fb69
season: 2
title: A00 67444ebf 8bc24f
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-67444ebf-8bc24f

## Experiment

BUILD ROUND (L4.274, g15 claim = behaviour to build). Implemented all three clauses
of `hypothesis:l4-the-dry-run-chain-line-is-tested-hermetically` on rotate.py's
dry-run r4/r5 block and added hermetic tests to test_rotate_selfreap.py.

rotate.py `cmd_rotate_self` dry-run block (~5389-5474):
1. Extracted `_belam_gate = (role == "prime_director" or
   getattr(args, "belam_prefix", None))` — the LIVE s6.6 gate — and moved the
   (r5) Belam FIFO cap-reap plan OUT of `if is_chain_seat:` into its own
   `if _belam_gate:` block, so a PLAIN seat GIVEN `--belam-prefix` now prints
   the r5 plan it WOULD run (read-only, same `_belam_oldest`/`_pane_pid`/
   `_descendant_chain` call path as live). The plain-seat r4/s12 own-chain
   block is unchanged and still prints beneath it.
2. The `no reap` message text is now role-aware (chain seat: "the own-window
   reap is GATED OFF on a numeral-chain seat"; plain seat:
   "the own-window reap (r4/s12) above still runs").
3. BOTH chain lines (r5 cap and r4/s12 own) now print `list(reversed(chain))`
   so the printed order IS the DEEPEST-FIRST Term order `_reap_chain` signals
   (`reversed(chain)`), coherent under the existing `TERM'd DEEPEST-FIRST`
   label (was printing SHALLOW->DEEP while claiming DEEPEST-FIRST).

Three hermetic tests added (same `_ps_table` + `_pane_pid` + windows.txt seams):
- `test_plain_seat_dry_run_chain_line_deepest_first` — asserts the exact
  r4/s12 line: own `@id @9` (from CURRENT <seat> window, never .genN),
  pane pid 500, and chain printed `[520, 510]` DEEPEST-FIRST (BFS fixture
  pane500->510->520).
- `test_chain_seat_dry_run_chain_line_deepest_first` — asserts the exact r5
  line: OLDEST predecessor `belam-S1-L4-I`, its `@id @10`, chain `[520, 510]`.
- `test_plain_seat_belam_prefix_dry_run_prints_r5_plan` — plain seat with
  `--belam-prefix belam` prints BOTH the (r5) cap-reap plan (`WOULD reap the
  OLDEST predecessor 'belam-I' (@id @10)`, chain line) AND its own r4/s12 plan;
  touches nothing (windows.txt identical, no rotation record).

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotate_selfreap.py -q` :
  **22 passed** (19 prior + 3 new) in ~35s.
  (also ran test_rotate.py + test_rotate_tail.py : **128 passed**; total 150
  passed on the rotate.test surface, 0 failures).
- **Order falsifier (RED):** temporarily flipped both prints from
  `list(reversed(chain))` to `{chain!r}` (shallow->deep) -> all 3 new order
  assertions FAIL (`pane pid 500 -> ps -e chain [510, 520]` printed, expected
  `[520, 510]`). Restored -> all green. The assertions are NOT order-blind:
  they pin DEEPEST-FIRST exactly, so a `_descendant_chain` patched to return
  the chain reversed (or a print that emits the un-reversed chain) goes red.
- **Plain-seat r5 falsifier:** test_plain_seat_belam_prefix_dry_run_*
  asserts the `(r5) Belam FIFO cap WOULD reap ...` line under a plain
  `role="parent"` seat with `--belam-prefix`; a dry-run that printed no r5
  plan (the pre-fix behaviour) would drop that assertion.
- PYTHONAST: rotate.py parses clean. Existing behaviour preserved for
  chain-seat dry-run (still prints clerk line; r5 now via `_belam_gate` which
  is True for prime_director) and plain-seat dry-runs WITHOUT --belam-prefix
  (`_belam_gate` False -> exactly the prior two lines).

## Agent Notes
Built all 3 clauses: r5 dry-run plan moved out of is_chain_seat onto _belam_gate (prime_director OR --belam-prefix), chain prints list(reversed(chain)) deepest-first; 3 hermetic tests in test_rotate_selfreap.py pin exact lines+order; 150 rotate-related tests green; order falsifier proven red then restored.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review L4.274 (a00-8512520d). (1) INSTRUCTION: the target node says "a HERMETIC test in test_rotate_selfreap.py (the files existing _ps_table + _pane_pid monkeypatch + windows.txt seam) asserts the EXACT dry-run lines for a plain seat ... and for a chain seat" and "a plain seat run with --belam-prefix <pfx> prints the (r5) cap-reap plan it WOULD run, through the same _belam_oldest call path as :5606/:5794". (2) WHAT THE CODE DOES, read at the diff and RE-RUN, not assumed: rotate.py dry-run r5 block is now gated on _belam_gate = (role == "prime_director" or getattr(args, "belam_prefix", None)) — the same predicate the LIVE s6.6 gate uses (rotate.py ~5606) — and calls _belam_oldest(_existing_for_chain, spawn_name, pfx) then _successor_window_id -> _pane_pid -> _descendant_chain, read-only. Both chain prints are list(reversed(chain)). I ran pytest on the file: 22 passed. I then mutated _descendant_chain to return list(reversed(chain)) and the three new tests went RED (test_plain_seat_dry_run_chain_line_deepest_first, test_chain_seat_dry_run_chain_line_deepest_first, test_plain_seat_belam_prefix_dry_run_prints_r5_plan — printed [510, 520] where [520, 510] is required), then restored and re-confirmed the diff stat. The stated falsifier is therefore a real red, not a claim. (3) NEAR MISS: a test that asserts only that the pid/chain text is PRESENT satisfies "asserts the EXACT dry-run lines" and loses the mechanism — order-blind assertions pass under a reversed _descendant_chain, which is precisely the falsifier the node names; these three pin the printed list literal [520, 510], and the plain-seat --belam-prefix test would have passed vacuously under the old is_chain_seat gating only if it asserted a heading (it asserts the "(r5) Belam FIFO cap WOULD reap the OLDEST predecessor belam-I (@id @10)" line, so the pre-fix code drops it). ACCEPTED as proved; clause (4) correctly left deferred per the amended claim. Residual weakness recorded, not a demotion: print and reap both consume the same list, so the assertion pins that this print equals reversed(that list) — it cannot see a change that reverses _descendant_chain AND removes the print reversal together, since the two cancellations are symmetric.
<!-- THOUGHT:END -->

Parent L4.274 review: ACCEPTED proved. Read the diff (not the report): r5 dry-run moved onto the live _belam_gate; both chain lines print list(reversed(chain)); 3 hermetic tests pin exact @id + pane pid + chain literal and touch-nothing. Parent re-ran 22 passed; parent mutated _descendant_chain reversed -> 3 new tests RED; restored. Caveat: print and reap share one list so a double reversal would cancel undetected; live-cap semantics for a plain --belam-prefix seat (successor counted as a belam candidate) unchanged and mirrored, not audited here.
