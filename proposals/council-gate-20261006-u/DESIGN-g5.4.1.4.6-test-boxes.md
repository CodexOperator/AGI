# Council design — goal:g5.4.1.4.6 — committed test_boxes.py

**Leaf mint:** `594456f7bb7e44a0817448278714699c` · parent `goal:g5.4.1.4.2` · **status:** active (DESIGN)  
**SoT (mint / SM):** `04aedac1d` (`04aedac1d248f6fd35bba4f16c5bc57ea1c83a5d`) · climb parent PASS tip `1617aff10` (**do not reopen**)  
**Pen:** self-perpetuating · **Lenses:** alive (PASS lean) · all-is-one (pending)  
**DG held** · **No Belam box** · gate-t / write-path g5.4.1.6 / land binsuite `04aedac1d` land-stream **OOS**  
**Capsule** `fda4efd6e` · season3 `4b8f28b5e` · writer: **Write+agi-turn — never write.py** · **OWNER pytest ALLOWED — never strip**

## Problem (measured)

| object | measured (ET 2026-10-06 ~17:53) |
|---|---|
| `extensions/agi/tests/test_boxes.py` | **MISSING** on MAIN / climb `1617aff10` / SM tip lineage |
| boxes freshness under Belam ONE grant | greened only via `test_bin_help_smoke.py -k boxes` → **1 passed** |
| `extensions/agi/bin/boxes.py` | PRESENT · **377 lines / 13315 B** · owns box identity / posts `box` cell / `AGI_BOX` / `graph_root` |
| parent `g5.4.1.4.2` | bin-suite-fresh **PASS** @ `1617aff10` (`status: complete` on climb); residue is **test debt**, not product-fail |

Owner zero-notes: missing `test_boxes.py` is a **real DESIGN leaf**, not a MUR footnote on `.4.2`.

## Standing path (ONE lean — ACCEPT)

**Add committed `extensions/agi/tests/test_boxes.py` covering `extensions/agi/bin/boxes.py`.**

### Scope (binding)
1. **File path:** `extensions/agi/tests/test_boxes.py` only (never replace/strip `test_bin_help_smoke.py` or other tests).
2. **Coverage floor (must-carry):**
   - Help / CLI smoke for `boxes.py` (may overlap bin_help_smoke; overlap OK — this file is the named owe).
   - **Behavioral** coverage of core readers: at least `graph_root`, default-box / `AGI_BOX` resolution, and posts-row `box` cell membership (happy path + one schema/error path using existing fixtures or temp graph — no live MAIN mutate).
3. **Suite rules:** one committed file at a time under Prime suite-window (`verification.py window` → `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_boxes.py -q`).
4. **Never strip** existing tests (Owner pin). Never `git rm`. Never waive by footnote on `.4.2`.

### Rejected
- Closing U1 by citing bin_help_smoke alone forever.
- Expanding scope into rotate `_box_fact` / unrelated box-* tests.
- Reopening `.4.2` PASS or mixing gate-t MOVE.

### Loop / writer
```
council DESIGN → SM gate → DG BUILD (Write+agi-turn) → climb/MUR → council → land
```
**DG held now.** This package does not add the test file.

## Must-carry
1. Committed `test_boxes.py` present on tip after BUILD.
2. One-file pytest green under suite-window rules.
3. `bin-suite-fresh` still PASS independently.
4. ZERO leftover notes on `.4.2` about missing test_boxes.
5. Write+agi-turn; never write.py; never strip pytest; never git rm.

## Falsifiers (for later BUILD / land)
1. `extensions/agi/tests/test_boxes.py` **PRESENT** on cited tip.
2. `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_boxes.py -q` → green (under suite grant/window).
3. `commands.py run verify` → `bin-suite-fresh` still PASS.
4. **Negative:** strip/delete other tests; waive-as-footnote on `.4.2`; write.py; git rm; Belam wake from this package; DG before SM PASS; mix gate-t / land-binsuite stream; season3/capsule/Master touch.

## Out of scope
Reopen `g5.4.1.4.2` · U2/U3 · gate-t send.py · write-path g5.4.1.6 · Belam land · season3 rewrite · Master · invent heads
