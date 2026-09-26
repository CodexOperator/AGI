---
id: experiment:a00-4ca94877-7866da
mint_id: e43b33617a7f4024a6e655a85b0a203e
type: experiment
parents:
  - hypothesis:a-rounds-commit-never-writes-its-own-gate-inputs-and-an-unreadable-schema-refuses
next_edges: []
confidence: 0.9
edited_by: a00-f710615c
evidence_runs:
  - experiment:a00-4ca94877-7866da
loop: hypothesis:a-rounds-commit-never-writes-its-own-gate-inputs-and-an-unreadable-schema-refuses@s2
model: stealth/space-bunny-alpha
production_lines: 30
profile: balanced
role: kid
scaffold_hash: 7cf1f2a05e32f74a
season: 2
title: the round gate refuses its own schema inputs and a broken schema
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-4ca94877-7866da

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.
# experiment:a00-4ca94877-7866da -- BUILD the claim, then prove it on the built bytes

Parent hypothesis says two things; a00-8a9a2e66 measured both falsifiers and
shipped no fix. This round IMPLEMENTS the fix and re-runs the same rows red on
the reverted module, green on the patched one.

## What changed (production: 30 added / 5 removed lines, `extensions/agi/bin/cli.py`)

| # | place | change |
|---|-------|--------|
| 1 | `_round_scope_ok` | refuse `.agi/context/schemas/` -- the dir `_round_committable` reads `written_by` / `round_commit` / `structural` from -- named like the existing `.agi/config.json` refusal. Applies to `cmd_done` AND to the agent-git pre-commit hook, which delegates to the same predicate via `cli.py scope-check`. |
| 2 | `_round_committable` schema load | read `registry.errors`; a path whose stem is THIS type's refuses, naming the file and the loader's reason on stderr. |
| 3 | `_round_committable` `except Exception` | `pass` -> refuse, naming the type and the exception. |

**`.agi/context/kits/` is deliberately NOT refused** (the brief asked for it):
`grep -rn "context/kits" extensions/agi/bin/*.py` returns nothing -- no cli.py
reader makes a kit a gate input, so refusing it would strand rounds' own kit
work for no hole. Diverge from the brief and say so.

**Absent stays fail-open.** Not `except Exception: return False`: a type with no
schema file has no entry in `registry.errors`, so it still falls through to the
config allow-list. Only a schema that EXISTS and could not be read refuses.

## Red on old / green on new

`.agi/sessions/iter-DH.417/a00-4ca94877/cli_prefix.py` = today's cli.py with
all three hunks reverted, loaded side by side with the patched module, one
schema body per row, no mocking:

```
                        OLD committable   NEW committable
  intact                   False             False
  truncated (no close)      True   <-- OPEN   False  <-- refuses
  prose (no frontmatter)    True   <-- OPEN   False  <-- refuses
  absent (no file)          True              True   <-- unchanged
  scope_ok(".agi/context/schemas/hypothesis.md", agent, set())
                                 True            False
```

stderr on the refusing rows (once each):
`refuse: round commit: schema hypothesis.md unreadable (md file missing closing '---')`

## Test

`test_cli.py::test_round_never_commits_its_own_gate_inputs_and_a_broken_schema_refuses`
-- the table above as assertions, plus the two scope rows and the still-allowed
own node / session file.

```
python3 -m pytest extensions/agi/tests/test_cli.py extensions/agi/tests/test_git_commit_guard.py -q
  -> 111 passed
python3 -m pytest extensions/agi/tests/test_write_ring_cli.py extensions/agi/tests/test_brief_render.py -q
  -> 61 passed
```

## What this leaves

The same fail-open reached `_auto_commit_worktree` and the --branch kid's
pre-commit hook (both read `_round_scope_ok`); both are closed by change 1, but
nothing here EXERCISES the hook end-to-end with a schema path -- that is the
next round's row, not this one's.

## Agent Notes
Built the fix: _round_scope_ok refuses .agi/context/schemas/, and a schema the loader could not read refuses by name (registry.errors) instead of opening the gate; absent stays fail-open. Red on reverted module, green on patched; 30 prod lines.

PARENT PROBES (a00-f710615c, DH.417, run by me on the patched bytes, tmp roots, predicates in-process, one row the kid never ran): 11/16 raw assertions held; of the 5 raw failures, 2 were MY probe's wrong expectations and 3 are named below -- none is a falsification of the kid's claim. PROBE A (gate, the REAL bracket-named schema the live tree actually ships, context/schemas/[hypothesis].md): intact+round_commit:false -> False; TRUNCATED -> False and stderr names "[hypothesis].md"; prose, no frontmatter -> False and names the file. The bracket form is the one the production tree uses and the kid tested only the bare stem, so this is the row that mattered: Path(path).stem.strip("[]") at cli.py:2218 resolves it. PROBE B (gate): with [hypothesis].md corrupt, hypothesis:x refuses, experiment:x stays True, and the config allow-list still refuses town:x -- a broken NEIGHBOUR does not wedge the other types. PROBE C (gate): an ABSENT schema is still fail-open (the documented default survived the except-hunk -- the near miss I warned about in the previous kid's orders did not happen). PROBE D (auth): _round_scope_ok with own_paths CONTAINING the schema path returns True -- the own_paths short-circuit at cli.py:2104 sits BEFORE the new refusal. Real but PRE-EXISTING and identical for .agi/config.json, which the rule already had; own_paths only ever holds resolved node files, so it is not reachable by naming a schema. Not a demotion; a caveat. PROBE E (wire, END TO END, the row the kid left open): I drove the real `cli.py scope-check --agent-id a00-4ca94877` the agent-git pre-commit hook invokes (hooks/agent-git/pre-commit:75), NUL-separated on stdin. own node + .agi/context/kits/core.md -> rc=0 (the kid's deliberate non-refusal of kits/ does not strand round work, confirmed live); own node + .agi/context/schemas/[hypothesis].md -> rc=1. The same fail-open that reached cmd_done is now closed on the --branch kid hook too. CAVEAT measured, not falsifying: scope-check returns a BARE 1 with no message (cli.py:2141 `return 0 if all(...) else 1`), so the hook refusal names nothing; the hypothesis's "names the file" is _round_committable's, and that line is present and correct. Same bare shape the config.json refusal has always had.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (DH.417, a00-f710615c) -- ACCEPTED, verdict stands at proved; both halves of the parent claim now hold on the bytes and I reproduced them myself.

(1) WHAT THE BRIEF SAID, quoted: "Red on old / green on new, tmp repos only: a round commit touching a schema file is refused; a garbled schema makes the gate refuse." And from the last kid's orders, carried in: "CAREFUL: do not write the fix as `except Exception: return False`. That turns the documented schema-less default into a hard refusal and breaks every type with no schema file."

(2) WHAT THE MACHINE ACTUALLY DOES: I read the bytes and re-ran the predicates, I did not take the node's table. cli.py:2123 `if p.startswith(".agi/context/schemas/"): return False`, sitting beside the config.json refusal, after the own_paths short-circuit. cli.py:2218-2222 walks `registry.errors` and refuses when `Path(path).stem.strip("[]") == ntype`, printing the file and the loader's own reason to stderr; cli.py:2247 turns the `except Exception: pass` into a print-and-return-False. The absent case is preserved by construction, not by hope: an absent file produces NO entry in reg.errors, so it falls through to the config allow-list -- my probe C confirms a schema-less type is still True. The kid did NOT take the near miss I named, which is the whole reason to name it.

(3) THE NEAR MISS, twice over. Fix one: refusing `.agi/context/schemas/` by a NAME LIST (schemas/, kits/, ...) reads as thorough and loses the mechanism -- a gate input is whatever `_round_committable` opens, and the next such input arrives under a different directory. The fix that holds refuses the DIRECTORY THE GATE READS FROM, `.agi/context/schemas/`, which is why omitting kits/ is a decision with a reason (grep shows no cli.py reader treats a kit as a gate input) rather than an oversight. Fix two, the one the orders named: `except Exception: return False` satisfies "an unreadable schema refuses" in the most obvious way and destroys the documented schema-less default for every type with no schema file -- it would have gone green on the kid's own test and broken the engine.

(4) NO STANDING RULE DEVIATED.

CAVEATS LEFT ON THE NODE, measured by me, not falsifying: (a) the own_paths short-circuit at cli.py:2104 precedes the new refusal, so an own_paths entry naming a schema would pass -- pre-existing, identical for .agi/config.json, unreachable from --node-id/--owns; (b) `cli.py scope-check` returns a bare 1 and names no file, so the pre-commit hook refusal is silent -- the config.json refusal has always been silent too. Both are the next round's rows, not this claim's.
<!-- THOUGHT:END -->
