---
id: experiment:a00-fddbb8b0-ad821d
mint_id: 2fe084877a064f6495b49b19ab050404
type: experiment
parents:
  - hypothesis:l4-trimguard-never-reads-a-closing-quote-as-an-open-span
next_edges: []
confidence: 0.95
edited_by: a00-4d8ade12
evidence_runs:
  - experiment:a00-fddbb8b0-ad821d
loop: hypothesis:l4-trimguard-never-reads-a-closing-quote-as-an-open-span@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d2ac75150bdf486e
season: 2
title: A00 fddbb8b0 ad821d
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-fddbb8b0-ad821d

## Experiment

hypothesis:l4-trimguard-never-reads-a-closing-quote-as-an-open-span —
a g15 BUILD order, not a measurement. Two fixes landed:

(1) `_collect_owner_spans` (extensions/agi/bin/cli.py) now distinguishes
    OPEN from CLOSE. Only `"` and `“` OPEN a span; only `"` and `”` CLOSE
    one. A stray closing curly `”` outside a span is skipped, never an
    opener. Pre-fix the code tested `line[i] in '"“”'` for the opener and
    scanned to any of `'"“”'` for the close, so a stray `”` minted a phantom
    span (or, on a short intervening run, consumed the real closing quote and
    LOST the real span entirely — the walk re-opened on the closing `"` and
    fell into the empty open-ended branch).

(2) `test_real_handoff_section_has_no_open_spans` now reads a FIXTURE §6
    section written under `tmp_path` (a copy of the item-106 shape), never
    the live HANDOFF.md — the hermetic suite no longer pins the live bytes.

## Evidence

Test suite: `env -u TMUX -u TMUX_PANE python3 -m pytest
.extensions/agi/tests/test_cli_trimguard.py -q`

    5 passed in 0.08s

New acceptance test (`foo” bar "this is a real owner quote of twenty-five
plus"`):

    ACCEPT spans: {'this is a real owner quote of twenty-five plus'}

Simulated PRE-FIX code on the same line (OPEN==CLOSE==`"“”`, both scans
`'"“”'`):

    PRE-FIX spans: set()   # real span LOST — closing `"` re-opened a
                           # zero-content open-ended span

So the fix both kills the phantom AND restores the real span on this shape.

Guard against the LIVE HANDOFF.md at HEAD:

    §6 lines 133-149  bytes=2557  real quoted spans: 1
    OK: all 1 owner quotes resolve in .agi/nodes/ — safe to collapse.


<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-4d8ade12, L4.303) — kept at proved.

WHAT THE INSTRUCTION SAID. The hypothesis testable_claim's L4.303 BUILD ORDER: "(1) in `_collect_owner_spans` only `\"` and `“` OPEN a span and only `\"` and `”` CLOSE one -- a stray `”` outside a span is skipped, never an opener (the L4.297 harvest residue: a stray `”` before a straight-quoted span minted a phantom closed span and could drop the real one); test: `foo” bar \"this is a real owner quote of twenty-five plus\"` yields exactly the real span; (2) `test_real_handoff_section_has_no_open_spans` reads a FIXTURE section ... never the live HANDOFF.md." Ceiling 1 kid, and the landed quote-parity walk was NOT to be re-derived.

WHAT THE MACHINE ACTUALLY DOES. Not the report — the artifact. cli.py:1898-1901 now declares `OPEN = '\"“'` and `CLOSE = '\"”'`; cli.py:1903 opens only on `line[i] in OPEN`; the close scan cli.py:1907 stops at `line[j] in CLOSE`. I loaded the helper myself and ran the four acceptance shapes: the mandated line yields exactly `{'this is a real owner quote of twenty-five plus'}` (stray `”` skipped); item-106 yields only its real span; a true unclosed 25+ quote still reports; two closed spans yield two; a `“...”` curly pair yields one. `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_cli_trimguard.py extensions/agi/tests/test_cli.py -q` -> 24 passed. `python3 extensions/agi/bin/cli.py trimguard` on the REAL HANDOFF.md at HEAD -> `§6 lines 133-149 bytes=2557 real quoted spans: 1` then `OK: all 1 owner quotes resolve in .agi/nodes/ — safe to collapse.` exit 0. The live-HANDOFF test is now a `tmp_path` fixture (test_cli_trimguard.py:82-100), as demanded.

NEAR MISS. Keeping ONE set `'\"“”'` for the opener and only excluding `”` from the close scan satisfies the exact acceptance string yet still mints a phantom closed span beginning at a stray `”` whenever the stray-to-next-quote run is >= 25 chars — the same class of bug the round exists to kill. The kid split BOTH sets, which is the general mechanism the claim named. Second near miss: the fixture line the kid appended is itself a 25+ non-quoted line, so if a phantom could open on the fixture's trailing text the `len(spans) == 1` assert would catch it — the fixture is not decoration.

DEVIATION. None from a standing rule. No engine behaviour outside `_collect_owner_spans` changed; file scope is exactly cli.py + test_cli_trimguard.py.

CAVEAT RECORDED, NOT PENALISED. The `_collect_owner_spans` docstring still says "A quote opens a span; the next quote closes it", which is now narrower than the code (only `\"`/`“` open). Prose-only drift in the same function; the behaviour and all five tests are correct on bytes I ran.
<!-- THOUGHT:END -->

## Agent Notes
Split OPEN/CLOSE quote sets in _collect_owner_spans so a stray closing curly quote is skipped, never an opener; real span no longer lost nor phantom-minted. Handoff test now reads a tmp_path fixture, not live HANDOFF. 5/5 tests pass; live HANDOFF trimguard passes with 1 real span.