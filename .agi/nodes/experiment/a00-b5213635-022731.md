---
id: experiment:a00-b5213635-022731
mint_id: b644bf9d0ecf44a3b3821f7dde5e50c1
type: experiment
parents:
  - hypothesis:the-choice-surface-takes-optional-args-and-offers-no-operator-verb
next_edges: []
confidence: 0.8
edited_by: a00-aba90604
evidence_runs:
  - experiment:a00-b5213635-022731
loop: hypothesis:the-choice-surface-takes-optional-args-and-offers-no-operator-verb@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "multi-value placement", "class": "wire", "cmd": "propose synthetic x.py:go with arity many and owns=[a,b,c]", "expected": "argv ends --owns a b c as three tokens", "observed": "--owns a b c", "result": "pass"}
  - {"conjunct": "append arity", "class": "wire", "cmd": "propose synthetic arity append owns=[a,b]", "expected": "--owns a --owns b", "observed": "--owns a --owns b", "result": "pass"}
  - {"conjunct": "fixed nargs arity", "class": "gate", "cmd": "propose synthetic arity 2 owns=[a,b,c]", "expected": "refuse by name, not one truncated token", "observed": "arg needs 2 values, got 3", "result": "pass"}
  - {"conjunct": "no silent drop", "class": "gate", "cmd": "propose synthetic default placement owns=[a,b]", "expected": "refuse by name naming the arg and arity", "observed": "arg got 2 values but its placement declares one", "result": "pass"}
  - {"conjunct": "drift pins arity", "class": "gate", "cmd": "drift_problems over synthetic CLI nargs=+ with declared arity 2", "expected": "reports arity 2 != many", "observed": "arity mismatch reported", "result": "pass"}
  - {"conjunct": "propose stays pure", "class": "gate", "cmd": "test_propose_never_imports_a_cli_or_touches_argparse", "expected": "no import, no parse_args", "observed": "pass", "result": "pass"}
  - {"conjunct": "multi-value places every value", "class": "wire", "cmd": "parent_probes.py PROBE A/A2/A3: propose with arity many/append/append:2", "expected": "every value its own token, flag repeated for append", "observed": "many -> --owns a b c; append -> --owns a --owns b; append:2 -> --owns a b --owns c d", "result": "pass"}
  - {"conjunct": "no silent drop / wrong count", "class": "gate", "cmd": "parent_probes.py PROBE G1/G2: list with no declared arity and arity 2 with 3 values", "expected": "CommandError naming arg and arity", "observed": "arg 'owns' got 2 values but its placement declares one; arg 'owns' needs 2 values, got 3", "result": "pass"}
  - {"conjunct": "live data still unmigrated", "class": "gate", "cmd": "parent propose(<checkout>/.agi, cli.py:done, owns=[a,b])", "expected": "refusal naming the missing arity (data not applied)", "observed": "'cli.py:done': arg 'owns' got 2 values but its placement declares one", "result": "pass -- confirms the named YAML is the remaining gap"}
  - {"conjunct": "drift pins arity once data lands", "class": "gate", "cmd": "parent_probes.py PROBE G4: _drift_problems with the 9 named YAML keys merged, then owns corrupted to arity 2", "expected": "[] with data; a named arity mismatch when corrupted", "observed": "drift with named YAML applied: []; corrupted: [('cli.py:done','owns','arity 2 != many',...)]", "result": "pass"}
  - {"conjunct": "placement + reason declared in [command].md schema", "class": "gate", "cmd": "parent_probes.py PROBE S1: parse [command].md frontmatter", "expected": "fields.placement {type: dict}, manifest comment carries reason, validation.types.placement: dict", "observed": "present", "result": "pass"}
production_lines: 59
profile: balanced
role: kid
scaffold_hash: 8cd4ac5d44e517da
season: 2
title: "multi-value placement: propose places every value from a declared arity, or refuses by name"
town: local-maxxing
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-b5213635-022731

## Experiment

ROUND 3 of the choice surface: the F2 verify on EF.45 demoted three items — (a)
`grid.py:cron proposable` (fixed in the data by the director, untouched here),
(b) multi-value options placed with a single token, producing an INCOMPLETE
argv, and (c) the `placement` field undeclared in the `[command]` schema.
This round builds (b) and (c).

**Built (b): arity in the placement data.** `_resolve_placement` now returns a
fifth element, the declared `arity` (None when undeclared). `propose` parses it
with `_split_arity` into a mode and size and places every value:

| `arity` | CLI shape | placement |
|---|---|---|
| `many` | `nargs='+'/'*'` | one flag, every value: `--owns a b c` |
| `append` | `action='append'` | flag repeated: `--owns a --owns b` |
| `append:N` | append + `nargs=N` | flag repeated, N values each |
| `"N"` | `nargs=N` | one flag and exactly N values |
| absent | one value | a single `[flag, value]` |

A list handed to an arg whose placement declares NO arity now REFUSES BY NAME
(`arg got N values but its placement declares one`), instead of the pre-fix
`str(list)` collapsing them into one token. A `"N"` or `append:N` arity that
the supplied count cannot satisfy also refuses by name. `propose` still never
imports, execs or patches a CLI — the arity is node DATA.

**Built (c): schema.** `[command].md` declares the top-level `placement` field
(and its `kind`/`flag`/`const`/`consts`/`arity` shape) and the `reason` field on
manifest/excluded entries, in `fields:` and `validation.types`.

**Tests.** A synthetic-graph falsifier supplies N values and asserts all N
appear (red pre-fix: one stringified token); append and fixed-N variants; a
refusal when no arity is declared; the drift helper `_drift_problems` now pins
arity against the CLI's own argparse, but only where the node DECLARES one; and
`test_drift_catches_a_declared_arity_the_cli_does_not_have` proves the pin is
real by introspecting a synthetic `nargs='+'` CLI and reporting a declared
`arity: "2"`. The no-import/no-argparse guard stays green.

## Evidence

Live multi-value args re-derived on this checkout (argparse -> entry.arg):

| entry | arg | CLI arity | declared |
|---|---|---|---|
| write.py:create | parent | append:1 | none |
| cli.py:scaffold | parents | append:1 | none |
| cli.py:done | owns | many | none |
| cli.py:done | evidence_runs | many | none |
| cli.py:scope-check | own | append:1 | none |
| cli.py:wait | agent | append:1 | none |
| grid.py:commit | session | "2" | none |
| rotate.py:handoff | field | append:2 | none |
| sensei.py:pick_worst | rows | many | none |

Pre-fix simulation (from the captured bytes, scratch `prefix_sim.py`): every
`arity` yields `['x.py', 'go', '--owns', "['a', 'b', 'c']"]` — ONE token, the
list stringified. Shipped bytes yield `--owns a b c` as three tokens, red
turned green.

```
python3 -m pytest extensions/agi/tests/test_commands_manifest.py \
  extensions/agi/tests/test_commands.py \
  extensions/agi/tests/test_graphweb.py -q
155 passed, 7 skipped
```

Second run including test_bin_help_smoke.py is unaffected.

## DATA I could not write (director applies to `.geometry/commands.md`)

`.geometry/commands.md` is EF.54's file. Add these entry-qualified keys under
its existing top-level `placement:` map — entry-qualified because `parent`
(collides with `cli.py:done --parent`, single) and `parents`/`session`/`rows`
differ per entry. Simulated with these merged: `_drift_problems` = `[]` and the
full-supply falsifiers stay green.

```yaml
  write.py:create.parent:
    kind: option
    flag: "--parent"
    arity: append
  cli.py:scaffold.parents:
    kind: option
    flag: "--parent"
    arity: append
  cli.py:done.owns:
    kind: option
    flag: "--owns"
    arity: many
  cli.py:done.evidence_runs:
    kind: option
    flag: "--evidence-runs"
    arity: many
  cli.py:scope-check.own:
    kind: option
    flag: "--own"
    arity: append
  cli.py:wait.agent:
    kind: option
    flag: "--agent"
    arity: append
  grid.py:commit.session:
    kind: option
    flag: "--session"
    arity: "2"
  rotate.py:handoff.field:
    kind: option
    flag: "--field"
    arity: append:2
  sensei.py:pick_worst.rows:
    kind: option
    flag: "--rows"
    arity: many
```

Until that lands the live entries still place one value per call and the drift
pin for them is scoped out (no declared arity). The mechanism, the refusal, and
the pin are all committed and green.

## Agent Notes

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, EF.55 a00-aba90604. WHAT THE INSTRUCTION SAID: "read the kid diff bytes, not its result file; run one negative probe per claim conjunct and record them as probes"; F2 item (2): "a multi-value option places every value ... or refuses by name; the placement data carries the arity; the drift test pins it". WHAT THE MACHINE ACTUALLY DOES: commit 164c35ff71 carries commands.py (_split_arity, a 5-tuple placement, per-arity chunking), test_commands_manifest.py (_cli_arity, _drift_problems, synthetic multi-value falsifiers), and [command].md (placement + reason). I ran 8 probes from my scratch (parent_probes.py): many/append/append:2 each place every token; a wrong fixed count and a list with no declared arity each refuse by name; _drift_problems is [] with the 9 named YAML keys merged and names the mismatch when owns is corrupted to arity 2; the LIVE cli.py:done.owns list refuses -- proving the arity data is not yet applied. NEAR MISS: the obvious way to learn arity is to introspect each CLI's argparse at PROPOSE time; that is round 1's stranded bug (it executes the CLI and races a concurrent parse). The kid keeps arity as node DATA and does the introspection only in the TEST, which keeps propose pure while a wrong declared arity still fails the suite. DEVIATION: the arity DATA could not be written because .geometry/commands.md is EF.54's concurrent file; the kid names the exact 9-key YAML and I verified _drift_problems is [] with it merged, so the mechanism is proved and the live multi-value entries stay single-token UNTIL that data lands. That is why the verdict is inconclusive_lean_proved:80, not proved, and I accept it as written rather than demoting: the deliverable the order asked for is complete, and the residue is named with the exact patch.
<!-- THOUGHT:END -->

## Agent Notes
arity in placement data: propose places every value (many/append/append:N/nargs=N) or refuses by name; [command].md declares placement+reason; synthetic falsifiers red-prefix/green; drift pins arity only where declared (synthetic nargs=+ CLI proves catchability); 155 passed 7 skipped; live arity YAML for 9 multi-value args named for director since .geometry/commands.md is EF.54's

parent a00-aba90604 EF.55: ACCEPTED inconclusive_lean_proved:80. Diff 164c35ff71: commands.py arity-aware placement (many/append/append:N/nargs=N), [command].md declares placement+reason, test_commands_manifest.py drift pins arity at test time. 8 parent probes pass (many/append/append:2 place every token; wrong count and no-arity list refuse by name; drift catches a corrupted arity once the 9 named YAML keys are merged; live cli.py:done.owns list still refuses -> arity data unmigrated). Residue: director must apply the 9-key placement YAML to .geometry/commands.md (EF.54 has the file).
