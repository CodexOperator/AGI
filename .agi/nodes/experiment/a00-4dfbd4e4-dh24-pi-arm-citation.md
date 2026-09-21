---
id: experiment:a00-4dfbd4e4-dh24-pi-arm-citation
mint_id: 2ff96771750e4acb91c13dfc166fa378
type: experiment
parents:
  - hypothesis:a00-4dfbd4e4-0b7729
next_edges: []
edited_by: a00-4dfbd4e4
evidence_runs: experiment:a00-4dfbd4e4-dh24-pi-arm-citation
line_ceiling: 40
loop: goal:g7.27.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 77ad7b8627814815
season: 2
title: "DH.24 pi-arm citation closed: pi template + adapter tests name the F1 arm at tip 5d8d4c914"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-4dfbd4e4-dh24-pi-arm-citation
DH.24 residue lane under `goal:g7.27.2` — close the F1 **pi-arm** citation gap
in `verdict:g7.27-harness-templates-falsifiers-hold`. Measured on checkout HEAD
`5d8d4c914` (`5d8d4c9141aff5c75369e03e6d22dbee20e3341f`).

## What was measured

Parent falsifier 1 covers "each of pi, claude-code, copilot-cli builds its argv
from a template with no flag construction inside rotate.py", but the verdict
never named the pi arm (`grep -nw pi` on it was empty). The pi tests exist and
pass, so the completion claim is not false — this round closes the citation gap.
All line numbers below were re-derived with `grep -n` at this tip, not copied.

Command 1:

    PYTHONPATH=/tmp/pt python3 -m pytest \
      extensions/agi/tests/test_harness_template.py \
      extensions/agi/tests/test_harness_dispatch_shapes.py \
      extensions/agi/tests/test_rotate_copilot_harness.py -q

Tail observed (at this tip):

    70 passed in 1.15s

Command 2:

    PYTHONPATH=/tmp/pt python3 -m pytest \
      extensions/agi/tests/test_harness_template.py -k pi -q

Tail observed (at this tip):

    15 passed, 26 deselected in 0.23s

Both counts are what this run printed (raw tails saved under
`.agi/sessions/iter-DH.24/a00-4dfbd4e4/`), not copied from the brief.

### pi file:line + test-name evidence

- `extensions/agi/tests/test_harness_template.py:223`
  `::test_pi_template_renders_the_flag_shape` freezes pi's headless argv
  `["/x/pi","--provider",...,"--model",...,"--thinking",...,"-p","--mode",
  "json",...,"CARD"]` and pins that absent keys emit NO flag (pi's own
  settings keep winning).
- `:238` `::test_pi_adapter_production_path_reaches_render` monkeypatches
  `pi_adapter.harness_template.render` with a sentinel and asserts
  `pi_adapter.build_command(...)` returns it with `seen["id"] == "pi"` — the
  pi DISPATCH path goes THROUGH the template renderer, not an inline argv.
- `:258` `::test_pi_template_is_dispatch_only_not_a_rotate_seat` asserts
  `"pi" in harness_template.available()`, `load("pi").get("rotate") is False`,
  `"pi" not in rotate._known_harnesses()`, and
  `rotate._validate_harness(None, "pi")[0] == 1`.
- `extensions/agi/templates/harness/pi.toml` is pi's only argv source
  (`argv = [--provider, --model, --thinking, "-p","--mode","json",
  spread extra_args, slot prompt]`, `rotate = false`).

### What is NOT covered (same caveat class as claude/copilot)

`grep -nw pi extensions/agi/bin/rotate.py` returns 4 hits, and ALL FOUR are
comments or strings (`:943`, `:990`, `:1746`, `:20956`) — no live code.
`grep -rn "_build_pi\|build_pi_args" extensions/agi/bin/rotate.py` is EMPTY.
So rotate.py carries no pi argv builder; pi is dispatch-only, exactly the F1
"zero hits for that harness's flag construction inside rotate.py" clause.

## Effect on the verdict

`verdict:g7.27-harness-templates-falsifiers-hold` F1 now names the pi arm with
the citations above, at the same quality as the claude/copilot citations; its
state stays `proved` and this experiment node is added to its `evidence_runs`
(LIST form). Zero production code edits.

## Evidence

    $ git rev-parse HEAD
    5d8d4c9141aff5c75369e03e6d22dbee20e3341f

    $ PYTHONPATH=/tmp/pt python3 -m pytest \
        extensions/agi/tests/test_harness_template.py \
        extensions/agi/tests/test_harness_dispatch_shapes.py \
        extensions/agi/tests/test_rotate_copilot_harness.py -q
    70 passed in 1.15s

    $ PYTHONPATH=/tmp/pt python3 -m pytest \
        extensions/agi/tests/test_harness_template.py -k pi -q
    15 passed, 26 deselected in 0.23s

    $ grep -nw pi extensions/agi/bin/rotate.py
    943:# opts a template out of the seat set (pi is headless, not a rotate seat).
    990:        # Declared but not buildable here: `pi` is a dispatch.py harness with
    1746:  hooks-as-claude-code-and-pi, conjunct 6): the config.json harness id the
    20956:                             "claude-code-and-pi)")

    $ grep -rn "_build_pi\|build_pi_args" extensions/agi/bin/rotate.py
    (no output, exit 1)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This node exists because the DH.24 dispatch found a citation gap, not a code
defect: `verdict:g7.27-harness-templates-falsifiers-hold` claimed all three
G7.27 falsifiers hold, but its F1 section named only claude-code and
copilot-cli even though parent falsifier 1 explicitly covers `pi` too. The pi
tests already existed and passed, so the completion claim was true but
under-cited (falsifier 2 only partially evidenced). WHAT THE MEASUREMENT
FOUND: the pi evidence is real and at this tip — frozen-argv test at
`test_harness_template.py:223`, production-render sentinel at `:238`,
dispatch-only assertion at `:258`; `templates/harness/pi.toml` is pi's only
argv source; `grep -nw pi rotate.py` returns four COMMENT/string hits and
`_build_pi`/`build_pi_args` is EMPTY, so there is no pi argv builder in
`rotate.py`. Fresh tails: `70 passed in 1.15s` (three files) and
`15 passed, 26 deselected in 0.23s` (`-k pi`), both re-measured rather than
copied. The verdict's F1 now carries the pi bullets, its `evidence_runs` lists
this node, and its Confidence paragraph cites the new tip. ZERO production
lines — the whole fix is in graph nodes, which is what a citation gap calls
for; had any pi test failed that would have been a behaviour defect to stop on
instead.
<!-- THOUGHT:END -->
