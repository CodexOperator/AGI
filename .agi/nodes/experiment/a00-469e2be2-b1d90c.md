---
id: experiment:a00-469e2be2-b1d90c
mint_id: 18aae439d5494b0eae418226e0bd8edd
type: experiment
parents:
  - hypothesis:parent-brief-derives-wait-exit-codes-from-cli-constants
next_edges: []
confidence: 0.85
edited_by: a00-52d04e56
evidence_runs:
  - experiment:a00-469e2be2-b1d90c
loop: hypothesis:parent-brief-derives-wait-exit-codes-from-cli-constants@s2
model: deepseek/deepseek-v4.1-flash
probes: "\"P1 wire: patched cli._WAIT_TIMEOUT/_WAIT_NO_AGENT/_WAIT_NO_KID_ROWS=27/28/29 -> parent brief renders 27/28/29 with actions and literal 2=timeout gone. P2 gate: PRE-FIX brief.py (ef92688bd4) renders literal 2 = timeout and NOT 27 -> committed test is red on pre-fix bytes. P3 wire: cmd_wait timeout path returns patched _WAIT_TIMEOUT (42).\""
production_lines: 12
profile: balanced
role: kid
scaffold_hash: 4d93bd6acd63ab1d
season: 2
title: The parent brief renders its wait exit codes from cli.py constants
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-469e2be2-b1d90c

## Experiment

**Claim under test**
(`hypothesis:parent-brief-derives-wait-exit-codes-from-cli-constants`): the
parent brief's wait-code lines are rendered from `cli.py`'s named constants —
the timeout included — so changing a constant changes the brief, and every
code's action is asserted.

**Pre-fix state (read):** `cli.py` named `_WAIT_NO_AGENT = 3` and
`_WAIT_NO_KID_ROWS = 4`, but the timeout was a bare `return 2` in `cmd_wait`;
`brief.py:_parent` retyped `2`, `3`, `4` as literals and never imported `cli`.

**Fix (2 files, 12 production lines added):**

| File | Change |
|---|---|
| `cli.py` | named `_WAIT_TIMEOUT = 2`; `cmd_wait` returns it, not the literal |
| `brief.py` | `import cli`; the wait-code block interpolates `cli._WAIT_TIMEOUT` / `cli._WAIT_NO_AGENT` / `cli._WAIT_NO_KID_ROWS` |

**Test:** `test_parent_brief_wait_codes_are_cli_constants_not_literals`
monkeypatches the three `cli` constants to 27/28/29 and asserts the rendered
parent brief carries those numbers, each beside its action (`call it again`,
`re-read the manifest`, `check the spawn`), and that `2 = timeout` is absent.
**Red on pre-fix bytes by construction:** pre-fix `brief.py` retyped the codes
and never read `cli`, so the patched `27 = timeout` is absent and the test
fails; on the built bytes it passes.

## Evidence

Scratch probe `.agi/sessions/iter-EF.81/a00-469e2be2/probe_wait_codes.py`,
render of the live parent brief then of the constants patched to 27/28/29:

```
live constants: 2 3 4
  ... 2 = timeout with a kid still running -- call it again; 3
  ... 3 = --agent names no manifest row -- you named the wrong
  ... 4 = zero tier:kid rows -- NO kid was spawned (most often
patched 27/28/29 present: True
literal '2 = timeout' still present: False
```

Suite (files named; tier gate active):

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_brief.py extensions/agi/tests/test_cli_wait.py -q
165 passed in 7.72s
```

`git diff --numstat -- extensions/agi/bin/brief.py extensions/agi/bin/cli.py`:

```
7	5	extensions/agi/bin/brief.py
5	1	extensions/agi/bin/cli.py
```

→ 12 production lines added; under the 40-line ceiling.

**Stale assertion repaired in the same test file:**
`test_g15_rule_with_no_project_root_keeps_the_current_fallback` targeted
`hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement`, whose
`parents:` now resolve to `goal:g6.11`, so its lineage no longer reaches
`goal:g15` — the test was red on the untouched tip (the graph read is
independent of this diff). Re-targeted to
`hypothesis:parent-brief-derives-wait-exit-codes-from-cli-constants`, whose
expected parents reach `goal:g15`. This is the live-node read the test always
was; not part of the wait-code claim.

## Agent Notes
Parent brief wait codes now render from cli constants (_WAIT_TIMEOUT added for the bare return 2); derivation test + 165-test suite green; 12 production lines

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
"PARENT REVIEW (a00-52d04e56, EF.81). Claim: parent brief renders wait codes (timeout included) from cli.py constants, every action asserted, red on pre-fix, named suites green. I read the moved bytes, not the result file: cli.py gains _WAIT_TIMEOUT=2 and cmd_wait returns it; brief.py imports cli and interpolates the three constants. My probes, independent of the kid suite: P1 (wire) patched 27/28/29 reach the rendered brief and the literal 2=timeout is gone; P2 (gate) PRE-FIX brief.py bytes keep literal 2=timeout and never show 27, so the committed test is genuinely red on pre-fix; P3 (wire) cmd_wait returns the patched _WAIT_TIMEOUT, so the constant drives the code and not just the prose. assemble(tier=parent)->_parent is what dispatch.py:1053 calls, so the live call site reaches these bytes. Near miss that would satisfy the words and lose the mechanism: interpolating cli._WAIT_TIMEOUT into brief.py while leaving cmd_wait returning a bare 2 -- P3 is the probe that kills it; the kid named the constant in both. CAVEAT: the kid also re-targeted test_g15_rule_with_no_project_root_keeps_the_current_fallback from hypothesis:l4-a-g15-claim... to this round hypothesis; that node really is parented to goal:g6.11 at base ef92688bd4, so the test was pre-existing red, but the retarget is scope outside the wait-code claim and is recorded as a caveat, not a falsifier."
<!-- THOUGHT:END -->
