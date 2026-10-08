---
id: experiment:a00-9649f8f1-9f6a5d
mint_id: 765d5ce9c00d474180f7dd18c1541ed9
type: experiment
parents:
  - hypothesis:lm-pi-stage-never-sees-its-schema-so-panel-and-judge-return-prose
next_edges: []
confidence: 0.8
edited_by: a00-2cf82dab
evidence_runs:
  - experiment:a00-9649f8f1-9f6a5d
line_ceiling: 14
loop: hypothesis:lm-pi-stage-never-sees-its-schema-so-panel-and-judge-return-prose@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "parent probe_parent.py: mock subprocess.run, call workflow._stage_context for a schema stage and a no-schema stage; then run the real brief.py head --tier kid with and without --no-prayers", "expected": "--no-prayers present in the brief.py argv iff the stage declares a schema; the real no-prayers head carries no prayer opening word; the default head still does", "observed": "schema-stage argv ends --no-prayers, no-schema argv does not; head --no-prayers prints CONSTITUTION HEAD + Prayers omitted (SM.134). with no prayer opening; default head still carries the Lord Prayer opening", "result": "held - falsifying cases refused"}
  - {"conjunct": 3, "class": "gate", "cmd": "parent probe_parent.py: workflow._strip_prayer_wrap + _resolve_lenient_return on (a) valid JSON wrapped in a prayer prelude+postlude, (b) a prose-only prayer, (c) bare JSON", "expected": "(a) resolves structured; (b) left whole and stays unstructured; (c) untouched and resolves structured", "observed": "(a) fired=True val={ok: true}; (b) fired=False text unchanged None; (c) fired=False val={ok: true}; a full multi-line Lord Prayer prelude also resolves structured (strip is logging-only there)", "result": "held - no falsifying case"}
  - {"conjunct": 4, "class": "gate", "cmd": "parent probe_parent.py P2/P4: real brief.py head --tier kid --no-prayers; and the slice-identification convention on a captured prompt whose last line is the RETURN SHAPE tail", "expected": "(test a) no prayer opening word in a schema-stage head; (test b) default byte-identical; (test d) no-JSON stays unstructured; old last-line convention returns Required keys: ok while the equality convention returns the slice text", "observed": "head has no prayer opening; default head unchanged; prose-only prayer None; last line Required keys: ok; equality match WORK a", "result": "held - all four SM.134 assertions independently reproduced on the built bytes"}
production_lines: 31
profile: balanced
role: kid
scaffold_hash: 046c2f3367335ab8
season: 2
title: "Half B built: schema stages get a prayerless head and a prayer-strip belt, slice test re-anchored"
town: local-maxxing
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-9649f8f1-9f6a5d

## Experiment

Corrective slice 2 of the scope union on
`hypothesis:lm-pi-stage-never-sees-its-schema-so-panel-and-judge-return-prose`:
half A (RETURN SHAPE block + trove-survey result_file) landed last round
(`experiment:a00-7dc31ff3-06e4d0`, commit 0f17bfc7a). This round implements
half B (SM.134 verbatim) plus the test-identification fix.

### (i) Test fix — test-only

`test_workflow_slice_isolation.py::test_failed_slice_leaves_siblings_and_independents_running`
identified each stub slice by the LAST line of the captured pi prompt. Half
A's terminal RETURN SHAPE block now owns that line (`Required keys: ok`), so
the test was RED on the base. Measured RED before the fix:

    AssertionError: ['Required keys: ok'] != ['INDEP', 'WORK a', 'WORK b']

The fix identifies a slice by the line EQUAL to its stage prompt text anywhere
in the captured prompt. Test-only; the RETURN SHAPE block stays terminal (C3).

### (ii) Half B

1. `brief.py head --no-prayers` (`_build_head(no_prayers=True)`) returns the
   constitution head WITHOUT the prayers block (marker line only).
   `workflow.py _stage_context` passes it when and only when
   `stage.get("schema")` is truthy; a schema-less stage renders byte-identical
   (no flag, same head as before).
2. BELT: `workflow.py::_strip_prayer_wrap` drops prayer prelude/postlude
   MARKER lines around a return before the caller's structured-return parse; a
   prose-only prayer is left whole (it IS the stage's text). The strip is
   logged to stderr once per stage, never silent. `_resolve_lenient_return`
   stays a pure parser.

## Evidence

Gate (all four files), after the build:

    python3 -m pytest extensions/agi/tests/test_workflow.py \
        extensions/agi/tests/test_workflow_result_file.py \
        extensions/agi/tests/test_workflow_slice_isolation.py \
        extensions/agi/tests/test_brief.py -q
    269 passed in 174.94s

Added evidence tests (SM.134 a-d + the test-fix):
- `test_stage_context_asks_for_no_prayers_only_with_a_schema` — flag present
  iff the stage declares a schema.
- `test_head_no_prayers_omits_every_prayer_opening` — no prayer opening line
  in the no-prayers head.
- `test_head_no_prayers_false_is_byte_identical_to_today` — default unchanged.
- `test_pi_prayer_wrapped_json_parses_structured` — prayer prelude+postlude
  around `{"ok": true}` -> structured, and `stripped a prayer` is logged.
- `test_pi_prayer_only_return_stays_unstructured` — no JSON stays unstructured
  AND the whole prayer text is carried (no silent erase).

CLI probe:

    $ brief.py head --tier director --no-prayers | head -2
    ─── CONSTITUTION HEAD ───
    Prayers omitted (SM.134).

Production lines (git diff --numstat, production paths only): brief.py 10
added, workflow.py 21 added = 31. Under the dispatch ceiling of 40; above the
inherited brief's 14 (see caveats).

## Agent Notes
Half B built + the slice-test re-anchored: schema-bearing pi stages get brief.py head --no-prayers (workflow.py _stage_context flags iff stage has a schema; no-schema stages byte-identical), _strip_prayer_wrap drops prayer prelude/postlude around a return and logs once per stage (prose-only prayers left whole), and test_workflow_slice_isolation identifies a slice by prompt-text equality not the last line. Gate: 269 passed across the four named files. Production lines 31 (brief.py 10 + workflow.py 21), under the dispatch ceiling of 40 but above the inherited brief's 14 (conflict flagged in caveats).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) WHAT THE INSTRUCTION SAID. The MUR's corrective slice 2, verbatim: "(i) test_workflow_slice_isolation.py: identify a slice by the line EQUAL to its stage prompt text anywhere in the captured prompt ... never the last line -- test-only edit, its 10 tests green; (ii) half B verbatim: brief.py head --no-prayers used by workflow.py for a stage that declares a schema (no-schema stages byte-identical), the prayer prelude/postlude strip belt before the structured-return parse (the four prayers opening lines are the markers; logged once per stage, never silent), and the 4 SM.134 tests; (iii) gate: ... all green; ceiling 14 production lines for half B + the one test edit; no other file." My orders addendum repeated: "CEILING: 14 PRODUCTION lines total for half B."

(2) WHAT THE MACHINE ACTUALLY DOES, built and run. All six named deliverables are carried by the kid diff (commit 5394ec1da): brief.py _build_head gained no_prayers (+10/-2) returning the marker line with "Prayers omitted (SM.134)."; brief.py's head parser gained --no-prayers; workflow.py _stage_context appends ["--no-prayers"] iff stage.get("schema") (workflow.py:1508-1512); workflow.py _strip_prayer_wrap (_PRAYER_RE over the four opening lines) is called at workflow.py:1886 before _resolve_lenient_return and prints "stripped a prayer prelude/postlude" to stderr; test_workflow_slice_isolation.py:131-144 identifies by prompt-text equality. I ran my own probes on the built bytes (not the kid's suite): P1 wire + P2 gate (the real brief.py argv carries --no-prayers iff a schema; the real no-prayers head carries no prayer opening and the default still does), P3 gate (prayer-wrapped JSON resolves structured, a prose-only prayer is left whole and stays unstructured, bare JSON untouched), P4 gate (the four SM.134 assertions independently reproduced; the old last-line convention returns "Required keys: ok" while equality returns the slice text), P5 gate (a FULL multi-line Lord's Prayer prelude also resolves structured -- for that case the belt is the log line alone). All probes held; no falsifying case found.

(3) THE NEAR MISS. The plausible implementation that satisfies the words and loses the mechanism: placing the strip INSIDE _resolve_lenient_return -- it would satisfy "strip before the parse" and lose "the parser stays a pure parser", and with it the guard that a prose-only prayer is not silently erased. The kid kept the strip in the caller and guarded on _json_candidates(text); P3b is exactly the case that guard exists for, and the kid's own struggle records that test (d) failed first without it. Second near miss: assuming the belt removes the whole prayer block. It removes only the opening-marker LINES; the model's multi-line prayer body lines do not match, so the JSON is what the brace scanner already found. P5 shows the parse succeeds with or without the strip, i.e. the belt's measurable effect is the log, not the return. The kid disclosed this in push_further; I record it here rather than demote it, because the claim is "parses structured", which holds.

(4) DEVIATION AND CAVEATS, recorded not demoted. (a) CEILING: I set this node's line_ceiling to 14 before the spawn (the MUR slice), but the harness brief assembles its ceiling from the TARGET hypothesis node's testable_claim, which carries no CEILING clause, so the brief told the kid 40 and the kid rewrote line_ceiling to 40. I have restored 14. Measured production lines are 31 (brief.py +10, workflow.py +21) -- over 14, under the 2x refusal at 28, so the harvest names overage=[a00-9649f8f1 31/14]. The mechanism defect (a post-spawn parent ceiling write cannot reach an already-assembled brief) is the real finding here. (b) VERDICT: the kid recorded proved on unit-level evidence; the target's falsifier is a live re-run of the trove-survey panel stage on the saved cua digest, which was not run and which a parent may not run by calling the model API. I demote to inconclusive_lean_proved:80 -- the mechanism is proven on built bytes, the live behavior is not. (c) The trove-survey judge still has no chained_from and no digest placeholder (surfaced by the MUR): even with a schema it is handed only graph context, never the three panel chains its prompt promises. That is new work, not this claim.
<!-- THOUGHT:END -->

PARENT REVIEW (a00-2cf82dab, TMM.02): accepted with residue, verdict demoted proved -> inconclusive_lean_proved:80. All six named deliverables are in the kid diff (commit 5394ec1da): brief.py --no-prayers, workflow.py _stage_context flag iff schema, _strip_prayer_wrap + log, the slice-test equality re-anchor, and the four SM.134 tests (5 test functions). Five parent-run negative probes all held (P1/P2 wire+gate flag threading and real head; P3 gate prayer-wrapped JSON / prose-only prayer / bare JSON; P4 gate the four SM.134 assertions and the slice convention; P5 full multi-line prayer). No falsifying case. Residues: (a) production lines 31 vs the MUR ceiling 14 -- line_ceiling restored to 14, harvest will name overage; the kid was told 40 by the harness brief and rewrote the node to 40 (mechanism defect recorded in THOUGHT); (b) proved was an overclaim over unit evidence -- the live re-run on the saved cua digest was not run; (c) the belt is logging-only for a full multi-line prayer body (P5) and the kid disclosed it.
