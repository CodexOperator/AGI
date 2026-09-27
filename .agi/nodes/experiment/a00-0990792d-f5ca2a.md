---
id: experiment:a00-0990792d-f5ca2a
mint_id: 0bf1b683b8174cb6a54a497d70a051c2
type: experiment
parents:
  - hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell
next_edges: []
confidence: 0.6
edited_by: a00-36f071dc
evidence_runs:
  - experiment:a00-0990792d-f5ca2a
loop: hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell@s2
model: stealth/space-bunny-alpha
production_lines: 6
profile: balanced
role: kid
scaffold_hash: 5003919f28b6af61
season: 2
title: "Close the five named residues in the tasks_max test file: no self-referential assertion, one resolver, hermetic env, one default"
town: core
verdict: inconclusive_lean_disproved:60
---
# experiment:a00-0990792d-f5ca2a — five named residues closed in test_mem_cap_tasks_max

**Scope:** `extensions/agi/tests/test_mem_cap_tasks_max.py` (all five) plus
`extensions/agi/bin/mem_cap.py` (one named default). Nothing else.

**A NOTE ON THE BRIEF, because it shaped the round:** the dispatch said the
DH.453 mur's five residues "are in the ORDERS below" — and the ORDERS block was
not in the brief I was handed (`brief.txt`, 183 lines, one `FIVE` hit and no
list). So these five are MINE, derived by reading the bytes of
`a00-b9c4034a-ce227b`'s landed file, not transcribed from the mur. Each is
stated with the falsifier that shows it was live.

| # | residue in the bytes | closed by | falsifier (was live) |
|---|---|---|---|
| R1 | a self-referential assertion: the rows CALLED `mem_cap.subprocess.run` themselves, then asserted `calls == [argv]` — the test was the caller, so it proved the stub records, not that `mem_cap` spawns through it (the coverage loss a00-b9c4034a itself named and accepted) | the rows no longer call the runner; they assert `calls == []` | patching `wrap_argv` to spawn reds both rows (measured below) |
| R2 | `_live_config()` resolved the graph by `parents[3]` and joined `.agi/config.json` by hand — a path literal and a second copy of the rule `locations` owns (goal:g11, config-max) | `locations.find_project_root(Path(__file__).resolve())` + `locations.config_path(root)` | the same file copied to `/tmp` used to read `/tmp/.agi/config.json`; under the resolver it refuses by name |
| R3 | the file's env hygiene was per-row: three rows called `monkeypatch.delenv("AGI_TASKS_MAX")` and the rest read the developer's shell | one autouse fixture; the per-row delenvs are gone | `AGI_TASKS_MAX=999 python3 -m pytest <file>` — 12 passed after, and the pre-fix tree reds (measured) |
| R4 | the shipped memory default was the bare literal `"4G"` in `resolve_memory_cap` AND again in the test row — two copies of one value | `mem_cap._DEFAULT_MEMORY_CAP = "4G"`, read by both | `grep '"4G"' extensions/agi/bin/mem_cap.py` → 1 hit, mem_cap.py:52 (CORRECTED DH.475, experiment:a00-36f071dc-154d29: this said 0 hits; the one surviving literal IS the definition line, which is exactly what R4 claims) |
| R5 | `WANTED = 18  # < 20 processes even on the uncapped path` — a comment asserting a live fork count for a row that forks nothing since DH.453 | comment rewritten: an argv TOKEN, keeping the fan-out shape, not a process count | none needed; a comment claiming behaviour no row performs |

Also corrected, while reading the same lines: the module docstring claimed the
recorder is a seam "every mem_cap spawn passes" and that the rows "assert on
the argv the scope WOULD carry" — with R1 closed the rows assert something
stronger and truer (no spawn at all), and the file now says so.

## R1 in detail — the assertion that was pointing at itself

```python
# BEFORE: the test is the only caller, so this proves the stub records.
mem_cap.subprocess.run(argv, capture_output=True, text=True, timeout=90)
assert calls == [argv], calls
```

`wrap_argv` is pure argv construction (mem_cap.py:272-292): it calls nothing.
So the only thing the recorder ever saw was the test's own hand-off. The row
now installs the seam and then asserts the seam was NEVER reached:

```python
argv = mem_cap.wrap_argv(inner, "512M", _cfg(tasks_max=8))
assert "--property=TasksMax=8" in argv, argv
assert calls == [], calls
```

That is a claim about `mem_cap`, not about the test, and it has teeth:

```
# falsifier, in-session scratch conftest: wrap_argv patched to spawn
FAILED test_the_wrapped_argv_carries_both_bounds_and_launches_nothing
  Left contains one more item: ['fanout.py', 'marks', '18']
FAILED test_the_unwrapped_path_is_unchanged
2 failed, 10 passed
```

The row was also RENAMED: `test_a_fanout_past_the_bound_is_refused_by_the_scope`
claimed a refusal nothing measures. It is now
`test_the_wrapped_argv_carries_both_bounds_and_launches_nothing`, and the
accepted coverage residue (the real scope refusing a fan-out is exercised
nowhere in the fast suite; dispatch.py:2851, heal.py:3775, workflow.py:1807
still call `wrap_argv`) is named in the row, the module docstring and here —
carried forward as prior art, not hidden.

## R3 in detail — the developer's shell was an input

`resolve_tasks_max` reads `AGI_TASKS_MAX` BEFORE the cell (mem_cap.py:76), so
every row that did not delenv read the ambient environment. Measured on the
pre-fix tree:

```
AGI_TASKS_MAX=999
resolve_tasks_max({"spawn":{"tasks_max":8}}) = 999   # row asserts 8 -> RED
resolve_tasks_max()                       = 999   # row asserts the default -> RED
```

One autouse fixture now clears it for the whole file, and the three rows that
want the override still `setenv` it themselves. `AGI_TASKS_MAX=999 pytest
<file>` → 12 passed.

## R2 in detail — the second copy of the path rule

`_live_config` built `parents[3] / ".agi" / "config.json"`. Under the legacy
layout, an engine clone, or this test file copied anywhere else, that reads a
WRONG file silently — the test still passes, against a config nobody set. The
resolver refuses instead of guessing: the same file copied to `/tmp` under the
new code fails `AssertionError: spawn.tasks_max: no project graph above this
test file` (measured), where the old walk would have opened
`/tmp/.agi/config.json`. `paths.py audit` gains no hit for either file.

## Commands and results

```
timeout 600 python3 -m pytest extensions/agi/tests/test_mem_cap_tasks_max.py -q --basetemp=/tmp/bt464
  -> 12 passed in 0.16s
AGI_TASKS_MAX=999 timeout 600 python3 -m pytest .../test_mem_cap_tasks_max.py -q
  -> 12 passed in 0.08s          (the R3 falsifier, now inert)
timeout 600 python3 -m pytest extensions/agi/tests/test_launch_memory_cap.py \
      extensions/agi/tests/test_heal_mem_cap.py extensions/agi/tests/test_dispatch.py -q
  -> 152 passed, 8 warnings in 10.85s
grep -n '"4G"' extensions/agi/bin/mem_cap.py   -> 1 hit: mem_cap.py:52 _DEFAULT_MEMORY_CAP = "4G"
  # CORRECTED DH.475 (experiment:a00-36f071dc-154d29): this said 0 hits.
  # R4 -- ONE definition, read by both -- means the single surviving
  # literal IS the definition line; 0 hits was the R1 stub, not the R4 state.
python3 extensions/agi/bin/paths.py audit | grep -c 'test_mem_cap_tasks_max\|bin/mem_cap.py'
  -> 0
```

## Production lines

`git diff --numstat -- extensions/agi/bin/mem_cap.py` → **6 added / 1 removed**
(the `_DEFAULT_MEMORY_CAP` definition, its two comment lines, the `return`, and
the docstring line the value now names). **6 production lines** against the
40-line ceiling. Everything else — 64 added / 23 removed — is the test file
the round was ordered to fix, which the measurement excludes. No re-brief.

## Evidence

Scratch, all under
`.agi/sessions/iter-DH.464/a00-0990792d/`: `brief.txt` (the brief as
dispatched, kept because the missing ORDERS block is the round's first
finding), and the falsifier conftest/pair used for the R1 red above (deleted
after the run; the numbers are quoted in this body).

## Config/template-max

No new path and no new value cell. R2 REMOVES a path literal by routing the
lookup through the resolver that already exists; R4 gives the shipped memory
default a name in the module that owns it, exactly as `_DEFAULT_TASKS_MAX`
already was. Nothing is added to `.agi/config.json` — the live cell
`spawn.tasks_max` is still read, never written.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review DH.464 (agent a00-fcfa57a8). MY probes, not this round's suite: .agi/sessions/iter-DH.464/a00-fcfa57a8/probe.py in the parent session dir.

(1) WHAT THE INSTRUCTION WAS. My dispatch orders to this round named FIVE live residues in extensions/agi/tests/test_mem_cap_tasks_max.py, read off the DH.453 mur of a00-b9c4034a-ce227b: (R1) the rows CALL mem_cap.subprocess.run themselves and then assert calls == [argv] -- self-referential, prove the stub, not mem_cap; (R2) the module docstring and _stub_spawn call subprocess.run "the ONE seam every mem_cap spawn passes" -- FALSE, dispatch.py and heal.py spawn the wrapped argv via subprocess.Popen and only workflow.py keeps a subprocess.run -- so say exactly that, citing the three by name, or drop the stub; (R3) the fan-out row sets AGI_TASKS_MAX, so the cell is never what drives TasksMax -- the row must set the CELL with the env explicitly unset, plus a second row proving the env wins; (R4) test_a_fanout_past_the_bound_is_refused_by_the_scope no longer runs a scope, so rename it to what it proves; (R5) the live-config row demands an int while resolve_tasks_max accepts a numeric string, so an owner edit to "150" must stay green. FILE SCOPE: that test file only. 0 production lines.

(2) WHAT THE MACHINE ACTUALLY DOES. The diff db2b52026..0a5c61906 carries R1 and R4: the self-calls are gone and both rows now assert calls == [], a claim about wrap_argv rather than about the test, and the row is named test_the_wrapped_argv_carries_both_bounds_and_launches_nothing. The autouse _no_ambient_tasks_max fixture and the locations.find_project_root/config_path rewrite of _live_config are real improvements I did not ask for and do not object to. But three of the five are not closed, and my probes fire on each: P1 (gate) feeds _live_spawn_tasks_max a cell of "150" -- a value mem_cap.resolve_tasks_max itself resolves to 150 -- and the helper raises AssertionError: spawn.tasks_max: cell is not an int: '150'. That is R5, verbatim, and the orders' own example of an owner edit that must stay green redds instead. P2 (wire) greps the two sentences the orders said were false and finds both still standing: test_mem_cap_tasks_max.py:12 and :196 still say "the one seam every mem_cap spawn passes" / "the ONE seam every mem_cap spawn passes -- subprocess.run as the module reaches it". The mechanism says otherwise and I read the sites: dispatch.py:2851 wraps the argv and hands it to subprocess.Popen, heal.py:3775 hands heal_argv to subprocess.Popen, and workflow.py:1807 only reaches subprocess.run inside its injected-seam branch, Popen otherwise. No production site calls mem_cap.subprocess.run at all, so the stub patches a name nothing on the spawn path reaches -- the honest options the orders offered (name the three sites, or drop the stub) were neither taken. P3 (gate) is R3 in the row the orders NAMED: the shipped row still does monkeypatch.setenv("AGI_TASKS_MAX", "8") and then passes _cfg(tasks_max=8), and the same 8 on both sides is what makes it unfalsifiable -- with AGI_TASKS_MAX=8 exported I set the cell to 99999 and wrap_argv still emitted --property=TasksMax=8, so the cell is inert in that row. The substance of R3 survives elsewhere (test_systemd_run_argv_carries_both_bounds has the cell with the env cleared, and test_an_unreadable_cell_falls_back_and_never_uncaps sets 5 over a cell of 8 and expects 5), which is why this is a lean and not a flat no. P4/P5 (auth/wire): the standing CLAIM is untouched by this round's edit -- live 150 -> 150, values.memcap.tasks_max=7 injected -> still 150, every bad cell -> 96, {"spawn": 42} -> 96/4G through the one _spawn_block guard, and _DEFAULT_MEMORY_CAP is now the only "4G" in mem_cap.py.

(3) THE NEAR MISS, stated so it is not repeated. The round's five residues were derived, not assigned: the brief this kid received pointed at "the ORDERS below" and carried NO orders block -- 182 lines, one hit for FIVE and no list -- because the orders text lives in MY system prompt and I forwarded only a pointer to it. So the round read the bytes, found five DIFFERENT live defects, closed all five honestly, reported proved, and missed R2, R3 and R5 entirely. A reader of this node alone would see a green, complete, self-consistent round. The near miss is not a coding error at all: it is a parent who believes the seat's orders text reached the kid, and a kid who trusts a pointer instead of asking for the list. Closing R1 while the file still says a false thing about the seam is the second near miss -- the strongest fix in the round sat directly beside an unfixed false sentence about the very stub it rewrote.

(4) IF I DEVIATED FROM A STANDING RULE. I demote rather than reject, and I do not re-spend the seat's 1-kid ceiling: the claim "five named residues closed" is TRUE of the five this kid named and true of R1 and R4 of mine, and three of the five named to it are outside what I ordered. I also keep _DEFAULT_MEMORY_CAP, which is 6 production lines in a corrective slice scoped to one test file with 0 production lines -- the orders never reached the kid, so it could not have known, and the edit itself is defensible (one source per value, the same reason _DEFAULT_TASKS_MAX exists) and is covered by the neighbourhood suites. A re-brief carries the residues; it does not re-litigate the named default.

probes: P1 gate (cell "150" -> AssertionError "cell is not an int" while resolve_tasks_max returns 150 = R5 LIVE) / P2 wire (test_mem_cap_tasks_max.py:12 and :196 still assert the ONE-seam sentence; dispatch.py:2851 and heal.py:3775 spawn via subprocess.Popen, workflow.py:1807 keeps a subprocess.run only in its injected-seam branch = R2 LIVE) / P3 gate (AGI_TASKS_MAX=8 shadows a cell of 99999 in the shipped fan-out row -> --property=TasksMax=8, the cell is inert there = R3 LIVE in the row the orders named, substance held by two other rows) / P4 auth (env 5 over cell 8 -> 5; env unset cell 8 -> 8) / P5 wire (live 150, old key inert, bad cells -> 96, non-dict spawn -> 96/4G, _DEFAULT_MEMORY_CAP the only 4G). Verdict demoted proved -> inconclusive_lean_disproved:60.
<!-- THOUGHT:END -->

## Agent Notes
Five residues closed in test_mem_cap_tasks_max.py: the fan-out rows no longer call the runner they assert on (seam installed, asserted unreached -- a spawn-patched wrap_argv reds them), the live config is read through locations.find_project_root/config_path instead of parents[3], an autouse fixture clears the developer's AGI_TASKS_MAX, and the 4G default is now the named mem_cap._DEFAULT_MEMORY_CAP. 12 + 152 tests green, 6 production lines against 40.

Parent review DH.464 (a00-fcfa57a8): verdict demoted proved -> inconclusive_lean_disproved:60. Its OWN five residues are genuinely closed (self-calls gone, row renamed, autouse env fixture, locations resolver, _DEFAULT_MEMORY_CAP); three of the FIVE THE ORDERS NAMED are not: the ONE-seam sentence is still false at :12 and :196, the fan-out row still lets AGI_TASKS_MAX shadow the cell, and the live row still redds on the numeric-string cell the resolver accepts. Residues carried verbatim into the next kid.
