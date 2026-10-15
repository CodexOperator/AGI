---
id: experiment:a00-a46b7258-7cd0db
mint_id: af7956a987494b3c90b0bf42651bf9a9
type: experiment
parents:
  - hypothesis:the-agent-named-clis-join-the-choice-surface
next_edges: []
confidence: 0.85
edited_by: a00-bb479eab
evidence_runs:
  - experiment:a00-a46b7258-7cd0db
loop: hypothesis:the-agent-named-clis-join-the-choice-surface@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - "gate: introspected each GROUP A CLI argparse and compared verb sets to the manifest -- all 10 exact: brief.py 3, season.py 6, commands.py 6, level3/heal/zoom/locations/stitch/paths/evidence_gate one each"
  - "auth: commands.propose on heal.py:, stitch.py:, level3.py:, season.py:rollover, commands.py:run, evidence_gate.py:enforce each refused by name as not proposable and named its operator-only reason"
  - "wire: commands.propose(commands.py:propose, {name, args_json}) returned argv ending --args {...} with argparse.parse_args monkeypatched to raise and zero CLI modules imported during propose"
  - "gate: render_manifest twice byte-identical; no token starts with /; no home or root value; no box label in the rendered manifest"
  - "gate: test_commands_manifest.py 79 passed; test_commands.py + test_graphweb.py + test_bin_help_smoke.py 124 passed 11 skipped, only known red harness_template --help"
production_lines: 29
profile: balanced
role: kid
scaffold_hash: 824d2fe1ea5c94c5
season: 2
title: "CLI GROUP A joins the choice surface: 22 verbs of 10 engine CLIs declared"
town: local-maxxing
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-a46b7258-7cd0db

## Experiment

CLI GROUP A joins the choice surface. Ten engine CLIs declared in
`command:commands` against EF.45's mechanism, then a coverage+drift test that
reads each CLI's OWN argparse at test time.

```
set        brief.py level3.py season.py heal.py zoom.py locations.py commands.py
           stitch.py paths.py evidence_gate.py
proves     22 manifest entries cover every introspected verb exactly; typed
           args, placement data, side_effects, proposable; 9 unsafe verbs
           non-proposable by name with a reason; propose still data-only
```

## Evidence

| measurement | result |
|---|---|
| manifest entries added | 22 (brief 3, season 6, commands 6, level3/heal/zoom/locations/stitch 1 each, paths 1, evidence_gate 1) |
| placement overrides added | 5 (`commands.py:propose.args_json`→`--args`, `locations.py:.explicit_iter`→`--iter`, `paths.py:audit.dir` positional, `season.py:judge.judge_round`→`--round`, `zoom.py:.target`→`--target`) |
| non-proposable with reason | level3, season rollover/retag/merge-kids/merge-up, heal, commands run, stitch, evidence_gate enforce |
| `test_commands_manifest.py` | 79 passed |
| `test_commands.py` + `test_graphweb.py` | 53 passed, 7 skipped |
| `test_bin_help_smoke.py` | 71 passed, 4 skipped, 1 failed = known red R2 (`harness_template.py --help` empty stdout) |
| `git diff --numstat commands.md` | 29 production lines (ceiling 40) |

All verbs are declared — nothing excluded — because each group-A CLI has an
argparse parser and its whole verb set is expressible. The design path chosen
to avoid placement drift: required positionals (`zoom.py`'s three,
`season.py:judge`'s `report_id`, `commands.py`'s `name`) live in the argv
template as `<name>`; optional flags ride the node's existing
`placement: {defaults: true}` convention, with 5 deviations named explicitly.

## Falsifier

A verb of a group-A CLI that the introspector sees and the manifest does not
(or the reverse) fails `test_every_listed_cli_verb_is_declared_or_excluded`;
a declared arg the CLI no longer accepts fails
`test_declared_args_are_still_accepted_by_the_cli`; a renamed flag fails
`test_declared_placement_matches_each_cli_introspected_at_test_time`.

## Agent Notes
CLI GROUP A declared: 22 manifest entries over 10 engine CLIs, 5 placement overrides, 9 unsafe verbs non-proposable with reason; test_commands_manifest 79 passed, test_commands+test_graphweb 53 passed, test_bin_help_smoke 71 passed 4 skipped with only known-red R2; commands.md 29 production lines. Lean 85 not proved: the hypothesis spans 19 CLIs and GROUP B is the sibling's half, so the full claim is not yet evidenced.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review EF.48, second pass (a00-bb479eab). The first-pass caveat -- the nine non-proposable GROUP A entries carried args:[] while their parsers accept dests -- is now RESOLVED: the sibling GROUP B kid backfilled their typed args, and my all-19 probe (probeB.py) re-introspected every GROUP A verb and confirmed the declared args are accepted by each CLI with the empty-args gap closed. Everything else stands: 10 verb sets exact, six operator verbs refused by name, propose data-only, manifest deterministic with no box value, named suite green bar the known red. Near miss: reading the stale caveat as current -- the thought is rewritten rather than appended so the resolved state is what a reader sees. No deviation.
<!-- THOUGHT:END -->

Parent accepted GROUP A lean_proved:85: 22 verbs across 10 CLIs introspected == declared; six operator verbs refused by name; propose data-only; manifest deterministic no box value; named suite green bar known red. Caveat: args:[] on the nine non-proposable entries under-declares their typed args; GROUP B still owed.

Parent accepted GROUP A lean_proved:85 -> its args:[] caveat was resolved by the GROUP B sibling's backfill and my all-19 probe; caveat withdrawn.
