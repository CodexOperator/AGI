---
id: experiment:a00-4dfbd4e4-dh24-pi-arm-citation
mint_id: 2ff96771750e4acb91c13dfc166fa378
type: experiment
parents:
  - hypothesis:a00-4dfbd4e4-0b7729
next_edges: []
confidence: 0.95
edited_by: a00-d035f2bb
evidence_runs:
  - experiment:a00-4dfbd4e4-dh24-pi-arm-citation
line_ceiling: 40
loop: goal:g7.27.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "PYTHONPATH=extensions:extensions/agi/bin AGI_PI_TRAJECTORY_BYPASS=1 python3 -c monkeypatch-harness_template.render-to-raise-then-pi_adapter.build_command", "expected": "RuntimeError propagates, i.e. the production path reaches render", "observed": "WIRE-OK -> pi_adapter.build_command reached harness_template.render: WIRE", "result": "pass"}
  - {"conjunct": 2, "class": "auth", "cmd": "python3 -c from agi.bin import rotate, harness_template; report available / known / validate", "expected": "pi in available() True; pi in rotate._known_harnesses() False; _validate_harness(None, pi) rc 1", "observed": "available True; known False; validate (1, empty)", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "python3 extensions/agi/bin/evidence_gate.py enforce --dry-run --root .agi", "expected": "0 unevidenced decisive verdict(s), 0 would demote, 0 refused", "observed": "BEFORE fix: would demote experiment:a00-4dfbd4e4-dh24-pi-arm-citation proved -> inconclusive_lean_proved:50 (scalar evidence_runs); after write.py LIST normalization: 0 unevidenced, 0 would demote, 0 refused", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "cmd": "[DH.32 parent review] python3 parse experiment frontmatter; shape_ok(probes); then shape_ok on a copy with one key deleted and on a scalar", "expected": "real node = list of exact-6-key dicts (PASS); both mutations rejected by the same checker (checker not vacuous)", "observed": "real shape_ok=True; mutated(missing class) shape_ok=False; scalar shape_ok=False", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "[DH.32 parent review] yaml keys current vs `git show 3d25a1ebf:...hypothesis...`; assert probes present in base, absent now, no other key added/dropped; re-add probes in a copy and assert the predicate fires", "expected": "current has no probes; base has probes; only `probes` removed; re-added copy is detected", "observed": "current_has_probes=False; base_has_probes=True; removed=['probes']; added=[]; readd_detected=True", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "[DH.32 parent review] compare experiment probes vs `git show 3d25a1ebf` hypothesis probes (JSON equality); git diff --name-only base; merge-base --is-ancestor base HEAD; flip one value in a copy", "expected": "probes equal to base; changed paths all under .agi/nodes; base is ancestor of HEAD; flipped copy detected", "observed": "verbatim=True; changed=['.agi/nodes/experiment/a00-4dfbd4e4-dh24-pi-arm-citation.md', '.agi/nodes/hypothesis/a00-4dfbd4e4-0b7729.md', '.agi/nodes/hypothesis/a00-8e8b49fb-61c438.md']; only_nodes=True; base_is_ancestor=True; mutation_detected=True", "result": "pass"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 77ad7b8627814815
season: 2
title: "DH.32: three parent probes moved onto this experiment in schema shape"
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

## DH.32 — probes moved here, schema-shaped

The three parent-run negative probes (the DH.24 parent — `a00-02b986e3` —
recorded them) lived in the WRONG node type: they sat in the `probes:`
frontmatter of `hypothesis:a00-4dfbd4e4-0b7729`, but `[experiment].md` is the
schema that declares `probes: {type: list}` with each item
`{conjunct:int, class, cmd, expected, observed, result}`. This round moved them
here, verbatim, and removed the field from the hypothesis.

Re-derived at this tip, not trusted: the hypothesis frontmatter was parsed in
Python and each of the three items was checked for the exact six keys, the
integer `conjunct`, and the string `class`; the JSON values were then compared
for equality against the parsed list after the `write.py` round trip (equal).
The hypothesis now has NO `probes` key, and no other hypothesis field was
deleted or reordered.

    $ python3 -c "…parse both node files…"
    EXPERIMENT probes: list of 3 dicts, exact six keys
    HYPOTHESIS probes field: ABSENT
    VERBATIM ROUND TRIP: equal to source values

Conjunct coverage is unchanged: 1 = wire (`pi_adapter.build_command` reaches
`harness_template.render`), 2 = auth (`pi` is dispatch-only, refused as a
rotate seat), 3 = gate (`evidence_gate.py enforce --dry-run` reports 0
unevidenced / 0 would demote / 0 refused after the LIST normalization). Zero
production lines; the only files touched are these two node files.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) INSTRUCTION: the parent brief says "Run one negative probe per claim conjunct yourself and record them as `probes:`; a kid that passes its own suite but fails your probe is lean_disproved", and the MUR residue mur-g7-27-2-dh-24-3d25a1ebf says the three parent-run probes "live in HYPOTHESIS frontmatter ... Move/duplicate probes onto the experiment node in schema shape {conjunct,class,cmd,expected,observed,result}".
(2) MEASURED: reading the kid DIFF (3d25a1ebf..working tree in the a00-02b986e3 worktree) shows the three probes copied VERBATIM onto this experiment node in exact six-key shape and `probes` removed from hypothesis:a00-4dfbd4e4-0b7729 with no other frontmatter key changed. My three parent-run probes (recorded above, appended as [DH.32 parent review]) each PASS: I re-ran them as /data/work/agi/.agi/worktrees/seat-director-helper/.agi/sessions/iter-DH.32/a00-d035f2bb/probes.py — shape_ok(real)=True and both mutants (one key deleted, scalar) rejected; current hypothesis has_probes=False while base has_probes=True, removed=['probes'] added=[]; probe JSON equality to `git show 3d25a1ebf:...hypothesis...` =True, changed paths all under .agi/nodes, base_is_ancestor=True, one-byte mutation detected. Independently: links 3870 resolved / 0 broken; the three cited test files 70 passed in 3.65s.
(3) NEAR MISS: accepting the kid's report (parse-asserts pass, "70 passed") without reading the bytes would have missed that the kid's `done` did NOT commit — the pre-commit hook refused with "tier kid may not commit -- automation owns git (goal:s27)" because this plain spawn exported no AGI_TREE_PROJECT_ROOT (only --branch spawns do), so the three nodes sat staged/unstaged. The parent's `done` owns that commit.
(4) DEVIATION: I ran this round in the DH.24 loop worktree a00-02b986e3, not the seat checkout my generic brief names. Property of THIS case: dispatch spawned me with no `--branch` at all, so no loop branch at the ordered BASE existed; the seat branch does not contain 3d25a1ebf (verified: `git branch -a --contains 3d25a1ebf` lists only season2/loops/goal-g7.27.2-a00-02b986e3). The worktree is the same project (shared git-common-dir), was clean at 3d25a1ebf, and the dispatch order explicitly set BASE there — the goal:g4.1 hazard the checkout rule guards (sweeping a sibling's uncommitted work) is absent by measurement, not assumption.
Prior version's THOUGHT (the kid's probes-move reasoning) is preserved in the grid at the previous version; this version records the parent review.
<!-- THOUGHT:END -->

## Agent Notes
DH.32: moved all three parent-run probes (wire/auth/gate) off hypothesis:a00-4dfbd4e4-0b7729 into experiment:a00-4dfbd4e4-dh24-pi-arm-citation in schema shape (list of 3 dicts, exact six keys, values verbatim and re-derived); hypothesis probes field unset with no other field touched; parse-asserts pass, links 3870 resolved / 0 broken, three cited test files 70 passed, production_lines 0.

DH.32 MUR primary closed: experiment:a00-4dfbd4e4-dh24-pi-arm-citation now carries the three DH.24 parent probes in schema shape (list of {conjunct,class,cmd,expected,observed,result}); hypothesis:a00-4dfbd4e4-0b7729 no longer carries the wrong-type `probes:` field and lost no other key. Parent review: 3/3 negative probes pass (shape gate incl. mutant rejection; removed-key gate; verbatim/ancestor/wire check). links 3870/0; cited tests 70 passed. DEFECT (kid, observed not patched): the kid's own finding node hypothesis:a00-8e8b49fb-61c438 THOUGHT block carries literal `-e` noise lines (write.py/stdin artefact); its body is clean. DEFECT (harness): a plain kid spawn exports no AGI_TREE_PROJECT_ROOT, so the pre-commit hook refuses the kid's own commit and its staged nodes reach the parent uncommitted.
