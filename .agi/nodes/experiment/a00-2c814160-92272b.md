---
id: experiment:a00-2c814160-92272b
mint_id: fd1614eb5f6c4614aba1777633592454
type: experiment
parents:
  - hypothesis:the-agent-named-clis-join-the-choice-surface
next_edges: []
confidence: 0.9
edited_by: a00-bb479eab
evidence_runs:
  - experiment:a00-2c814160-92272b
loop: hypothesis:the-agent-named-clis-join-the-choice-surface@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - "gate: introspected all 19 EF.48 CLIs and compared verb sets to command:commands -- every set exact; node_writer.py and metrics.py have no parser and are declared in excluded: by name"
  - "auth: commands.propose on sensei.py:apply, unify.py:, benchmark.py:, post_wire.py:, handoff.py:claim/release/write, anonymize.py:install-hook, node_writer.py:, metrics.py: each refused by name as not proposable and named its reason"
  - "wire: commands.propose(commands.py:propose, ...) returned an argv with argparse.parse_args monkeypatched to raise and zero CLI modules imported during propose"
  - "gate: render_manifest twice byte-identical; no token starts with /; no home or root value; no box label"
  - "gate: test_commands_manifest.py 97 passed; test_commands.py + test_graphweb.py + test_bin_help_smoke.py 124 passed 11 skipped, only known red harness_template --help"
production_lines: 55
profile: balanced
role: kid
scaffold_hash: e8839f306bae28fe
season: 2
title: "CLI GROUP B: nine engine CLIs join the command:commands choice surface"
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-2c814160-92272b

## Experiment

CLI GROUP B of the EF.48 engine-CLI choice-surface survey: declare all nine
engine CLIs (sensei, post_wire, node_writer, metrics, unify, hierarchy,
handoff, benchmark, anonymize) in `command:commands` and extend the coverage
test to include them. Same contract as GROUP A: every verb declared in
`manifest:` or `excluded:` with typed args, placement data, side_effects and
proposable.

### What landed (measured)

| item | before | after |
|---|---|---|
| GROUP B verbs declared | 0 | 20 entries: 18 manifest + 2 excluded |
| placement overrides | 5 (GROUP A) | +3 (`sensei.py:propose.target`, `sensei.py:calls.from_`, `handoff.py:read.section`) |
| test CLI list | GROUP A 10 | +9 GROUP B (`_LISTED_CLIS`) |
| parserless handling | none | `_PARSERLESS_CLIS` + `require_parser` knob on `_introspect_cli` |
| GROUP A backfill | 9 entries with `args: []` | typed args read from each CLI's argparse |

`node_writer.py:` (library, no `main`) and `metrics.py:` (manual argv) are
excluded by name -- no argparse to introspect. Non-proposable with a reason:
`sensei.py:apply`, `post_wire.py:`, `unify.py:` (destructive), `benchmark.py:`
(spend), `handoff.py:claim/release/write` (shared scratchpad),
`anonymize.py:install-hook` (writes a git hook). Every other entry is
proposable with typed args; the read audits are proposable read.

### Commands and results

```
python3 -m pytest extensions/agi/tests/test_commands_manifest.py -q
  -> 97 passed
python3 -m pytest extensions/agi/tests/test_commands.py \
  extensions/agi/tests/test_graphweb.py \
  extensions/agi/tests/test_bin_help_smoke.py -q
  -> 124 passed, 11 skipped, 1 failed (KNOWN RED: harness_template.py --help
     produces empty stdout -- not GROUP B)
```

`git diff --numstat` over the production node file:
`55  1  .agi/nodes/.geometry/commands.md` (ceiling 40, 2x = 80; within).

### Deviation (disclosed)

`write.py <node> 'sub ...'` on a frontmatter key does not preserve bytes:
`_resolve_sub` parses the changed file and re-dumps ALL frontmatter
canonically, expanding every inline flow map into block YAML. A one-line
insertion produced a 2171-line diff. GROUP A had already hand-written the
inline form for the same reason (its note says so). I restored the node to
HEAD and re-applied the block with a direct splice, preserving the inline
form and keeping the diff at 55 lines. Recorded here, never silent.

## Evidence

- `test_commands_manifest.py` 97 passed: every GROUP B verb introspected from
  its own argparse equals its declared key, every declared arg is still
  accepted, and every proposable entry places every supplied value.
- `node_writer.py`/`metrics.py` are never imported by the test: the
  `require_parser=False` knob returns `{"": set()}` without running `main`,
  while every parser CLI still asserts its parser was captured.
- The other named suites show only the pre-existing `harness_template.py` red.
Raw output, screenshots, logs.

## Agent Notes
GROUP B: 20 entries for 9 CLIs (18 manifest + 2 excluded parserless), 3 placement overrides; _LISTED_CLIS +=GROUP B and require_parser knob added; GROUP A's 9 args:[] entries backfilled from argparse; test_commands_manifest.py 97 passed, other named suites 124 passed 11 skipped with only the known harness_template.py --help red; production_lines 55

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review EF.48 (a00-bb479eab). Instruction: GROUP B joins the choice surface, every verb declared or excluded by name, destructive/live-seat/spend/owner-ops never proposable, coverage+drift green, propose data-only, manifest deterministic with no box value. What the machine does, cited to artifacts I ran: probeB.py introspected all 19 CLIs and every GROUP B verb set matched the manifest exactly; probeB2.py refused all ten GROUP B operator verbs by name with their reasons; the manifest rendered 177 entries byte-equal twice with no absolute path, home or root value; test_commands_manifest.py 97 passed and the other three named files 124 passed with only the known red. Near miss I checked for: a parserless module quietly dropped from the list -- both are named in excluded: and in _LISTED_CLIS, and the require_parser knob defaults True so the parser assertion still fires for the other 17. Weakness left in the node, not hidden: the GROUP B comment blocks are glued to the tail of the preceding entry line (valid YAML, ugly bytes), and _PARSERLESS_CLIS is keyed by filename so a future argparse on metrics.py would not be noticed. GROUP A args backfill landed here and my all-19 probe confirmed it. No deviation from a standing rule.
<!-- THOUGHT:END -->

Parent accepted GROUP B proved: all 9 CLIs introspected == declared (19/19 with GROUP A); ten operator verbs refused by name; parserless two excluded by name; propose data-only; suite green bar known red. Caveat: GROUP B comment lines glued to prior entries; _PARSERLESS_CLIS filename-keyed.
