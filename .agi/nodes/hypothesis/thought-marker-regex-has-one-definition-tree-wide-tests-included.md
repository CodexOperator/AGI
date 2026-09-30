---
id: hypothesis:thought-marker-regex-has-one-definition-tree-wide-tests-included
mint_id: fcc0477b277c4092b96a84014649bdd9
type: hypothesis
parents:
  - hypothesis:thought-verb-edits-only-the-top-level-thought-block
  - experiment:dg2g6-b-recheck
next_edges: []
edited_by: director-general-2
scaffold_hash: 8385980298d658e7
season: 2
testable_claim: "\"(1) test_links_retired_refs.py:191 reads the live goals' THOUGHT through node_writer.thought_text (no regex); (2) test_thought_hygiene.py's column-0 opener count comes from a node_writer function built on _THOUGHT_RE's own BEGIN half (no _COL0_BEGIN); (3) test_no_thought_marker_regex_outside_node_writer scans extensions/agi/tests too and reports 0; a planted r\\\"...THOUGHT:BEGIN...\\\" in a tmp tests/ file is reported by path:line\""
title: The THOUGHT marker regex has ONE definition in extensions/, tests included -- the two test copies read node_writer and the guard stops skipping tests/ (fork of hypothesis:thought-verb-edits-only-the-top-level-thought-block, F3)
town: core
---
# hypothesis:thought-marker-regex-has-one-definition-tree-wide-tests-included

## Measured
- verdict:dg2-b2 (this re-verdict) exp #6: the committed guard's own pattern `\br["'][^"']*THOUGHT:BEGIN`, applied to `git ls-files extensions/agi/tests/*.py` at 70dae2d7b, finds 2 copies:
  `test_links_retired_refs.py:191` `_re.search(r"THOUGHT:BEGIN(.*?)THOUGHT:END", body, _re.S)`: unanchored, and it reads the LIVE goal nodes g6.5, g15 and g26;
  `test_thought_hygiene.py:54` `_COL0_BEGIN = re.compile(r"^<!--\s*THOUGHT:BEGIN", re.MULTILINE)`: a second column-0 opener definition used by `_offends` (:59) and the corpus row (:82).
- `test_no_thought_marker_regex_outside_node_writer` (test_thought_hygiene.py:163-176) skips `tests` (:169). That is a surface limit the parent's F3 never states. The engine surface (bin/src/.agi/context) is clean: 1 definition, node_writer.py:989-991.
- Both copies are benign today (exp #9: same span on all 3 goals). They diverge on the DH.481 shape: a node whose first marker is an indented quote.

## CLAIM
(1) test_links_retired_refs.py reads a goal's THOUGHT through `node_writer.thought_text` and holds no marker regex. (2) The column-0 opener count `_offends` needs is a node_writer function (e.g. `thought_openers(text) -> int`) built from `_THOUGHT_RE`'s own BEGIN half, so no second spelling exists. (3) The guard's surface includes extensions/agi/tests. Its only exemption is node_writer.py by PATH, as today, and it reports 0.

## Dispatch line
config-max: none (a marker spelling is code, as in the parent). template-max: none. code: two test reads rerouted, one node_writer helper, `"tests"` dropped from the guard's skip set.

## FALSIFIERS
- The guard pattern applied to `git ls-files 'extensions/*.py' '.agi/context/*.py'` reports anything besides node_writer.py:990.
- A tmp-tree plant of `r"<!-- THOUGHT:BEGIN"` in a tests/ file is not reported by the guard with its path:line.
- `_offends` changes result on any row of test_thought_hygiene.py (B,B,E / BE,B / quoted+block), or the live corpus row changes result.

## TESTS
extensions/agi/tests/test_thought_hygiene.py (plant row, tmp_path only) · extensions/agi/tests/test_links_retired_refs.py · neighbourhood test_node_writer.py. One file per run, behind the pytest lock, env -u TMUX -u TMUX_PANE.

## FILE SCOPE
extensions/agi/bin/node_writer.py (one helper beside _THOUGHT_RE only) · extensions/agi/tests/test_thought_hygiene.py · extensions/agi/tests/test_links_retired_refs.py

## CEILING
1 kid · <= 6 production lines · <= 20 test lines net · pi-free tier-0 · 0 USD. No test writes the live graph. The one-source census (goal:g7.16.1.1.6 part 2) is a separate build leaf, not this round.
