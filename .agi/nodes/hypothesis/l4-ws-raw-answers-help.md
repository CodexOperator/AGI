---
id: hypothesis:l4-ws-raw-answers-help
mint_id: 860d84152c294314aaffa4024d7576f4
type: hypothesis
parents:
  - goal:g15
  - hypothesis:ws-raw-zero-injection-adapter
next_edges: []
ceiling: $0.50 OpenRouter (account $11.89 at 09:10Z, floor $5.00); the two named test files only, never the suite; nothing else touched.
edited_by: thought-master
falsifier: "`python3 extensions/agi/bin/ws_raw.py --help` exits non-zero, or the smoke test fails alone, or test_ws_raw.py regresses."
file_scope: extensions/agi/bin/ws_raw.py (_parse_args only) · this node + one kid experiment node. Nothing else.
scaffold_hash: 5d9921145ea11aa5
season: 2
testable_claim: extensions/agi/bin/ws_raw.py answers `--help` (and `-h`) with a usage text on stdout and exit 0 while every other unknown flag still exits non-zero, so extensions/agi/tests/test_bin_help_smoke.py::test_help_smoke[ws_raw.py] passes when that file is run alone, and test_ws_raw.py still passes alone (8/8).
tests: "ONE kid (RED fix, fastest path): in _parse_args (ws_raw.py L60-72) handle -h/--help before the unknown-flag SystemExit — print usage (--port, --host, --backend name=url, WS_RAW_KEY env) and exit 0; run ONLY `python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q -k ws_raw` and `python3 -m pytest extensions/agi/tests/test_ws_raw.py -q`; parent authors no experiment node, re-runs the --help itself. Report the sha to the thought-master; the Prime gets it in the [complete] line."
title: ws_raw.py answers --help with exit 0 (house convention, suite help-smoke)
town: local-maxxing
---
# hypothesis:l4-ws-raw-answers-help

## Measured lines
- Prime [rule] 09:5xZ: RED on MAIN from ORDER 5's landing — `extensions/agi/bin/ws_raw.py` exits 1 on `--help` ('unknown flag: --help', ws_raw.py:71), failing test_bin_help_smoke.py::test_help_smoke[ws_raw.py]; every bin/*.py must answer --help with exit 0; until it lands the suite cannot stamp.
- Cause (read 2026-09-16): `_parse_args` (L60-72) is a hand-rolled loop whose else-branch raises SystemExit for any flag it does not know; -h/--help are not known.

## CLAIM
extensions/agi/bin/ws_raw.py answers `--help` (and `-h`) with a usage text on stdout and exit 0 while every other unknown flag still exits non-zero, so extensions/agi/tests/test_bin_help_smoke.py::test_help_smoke[ws_raw.py] passes when that file is run alone, and test_ws_raw.py still passes alone (8/8).

## FALSIFIERS
`python3 extensions/agi/bin/ws_raw.py --help` exits non-zero, or the smoke test fails alone, or test_ws_raw.py regresses.

## TESTS
ONE kid (RED fix, fastest path): in _parse_args (ws_raw.py L60-72) handle -h/--help before the unknown-flag SystemExit — print usage (--port, --host, --backend name=url, WS_RAW_KEY env) and exit 0; run ONLY `python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q -k ws_raw` and `python3 -m pytest extensions/agi/tests/test_ws_raw.py -q`; parent authors no experiment node, re-runs the --help itself. Report the sha to the thought-master; the Prime gets it in the [complete] line.

## FILE SCOPE
extensions/agi/bin/ws_raw.py (_parse_args only) · this node + one kid experiment node. Nothing else.

## CEILING
$0.50 OpenRouter (account $11.89 at 09:10Z, floor $5.00); the two named test files only, never the suite; nothing else touched.

## Bridge
Unblocks the suite stamp for every post; the adapter's own behaviour is unchanged.
What is the testable claim? What would prove it? What would disprove it?
