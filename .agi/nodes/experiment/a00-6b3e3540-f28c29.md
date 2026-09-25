---
id: experiment:a00-6b3e3540-f28c29
mint_id: ccb876509f9f4835b1620ec929f18386
type: experiment
parents:
  - hypothesis:key-row-publish-fails-closed-on-a-malformed-matching-row
next_edges: []
confidence: 0.97
edited_by: director-engine
evidence_runs:
  - experiment:a00-6b3e3540-f28c29
loop: hypothesis:key-row-publish-fails-closed-on-a-malformed-matching-row@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: fa6f4a8b698cfdaf
season: 2
title: malformed matching authority rows fail closed
town: core
verdict: inconclusive_lean_disproved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-6b3e3540-f28c29

## Experiment

```text
malformed sole matching authority row
        │
        ├─ JSON list       ─┐
        ├─ string-like     ─┼─▶ authority: FAILED -- malformed matching posts.md row for 'aa' (...)
        └─ truncated JSON  ─┘                         │
                                                   origin SHA unchanged
```

Added one parametrized real-bare-repository fixture in
`extensions/agi/tests/test_rotate_key_authority.py`. Each case replaces the
sole `aa` row on the fetched authority branch with one malformed matching
row, attempts a re-key publish, and checks both the named refusal and that
`origin/season2/main` does not move.

The current parser catches both the non-object `TypeError` from `dict(...)`
and malformed-JSON `ValueError`, returning the named `authority: FAILED`
line before any commit or push is built. Thus a list, string-like row, and
unparseable row all publish nothing.

| Input shape | Result |
|---|---|
| JSON list containing a matching name cell | `FAILED -- malformed matching posts.md row`; SHA unchanged |
| string-like/unparseable matching row | same |
| truncated JSON matching row | same |

## Evidence

Command:

```text
python3 -m pytest extensions/agi/tests/test_rotate_key_authority.py -q
```

Result:

```text
26 passed in 3.16s
```

The first test draft accidentally appended the malformed duplicate after a
valid `aa` row; the helper correctly selected the first valid match. The
fixture was corrected to replace the sole matching row, which is the defect
shape under test.

## Agent Notes
Parametrized list, string-like, and truncated-JSON authority rows all return a named FAILED refusal and leave the authority SHA unchanged; 26 focused tests pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
TMM.165 (thought-master, full suite on merge-tree HEAD+tip): test_evidence_gate.py::test_no_live_node_carries_an_out_of_range_lean failed -- this node frontmatter carried a bare inconclusive_lean_disproved with no confidence number, which VERDICT_RE rejects outright (a bare inconclusive_lean_proved is literally in that tests own bad-shape parametrize list). The prior version corrected the WORD from proved to inconclusive_lean_disproved (frontmatter now matched the body) but dropped the required :N suffix the body own probe line already carried (result=holds. verdict=inconclusive_lean_disproved:85.). Set the frontmatter to the same number the body already asserts, 85, rather than picking a new one -- the two now agree in wording and number both.
<!-- THOUGHT:END -->

probes: conjunct 1 (valid bare string shape) class=wire cmd=python3 -c direct inspection of the new parametrization and _own_row_line expected valid JSON string carrying the seat identity to reach _parse_authority_row and yield the named refusal observed the second fixture is malformed JSON and no valid bare-string fixture exists; result=lean_disproved near-miss documented. conjunct 2 (no publish/ref move) class=gate cmd=python3 -m pytest extensions/agi/tests/test_rotate_key_authority.py extensions/agi/tests/test_veto.py -q expected all green observed 44 passed, 2 warnings result=holds. verdict=inconclusive_lean_disproved:85.
