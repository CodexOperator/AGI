---
id: goal:g1.31.5.4.3
mint_id: e0ae28a398d843ec93a8c0ff72b26f16
type: goal
parents:
  - goal:g1.31.5.4
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.5.4.3
goal_kind: subgoal
origin: goals-doc
scaffold_hash: dc5afc877a8e096b
season: 2
seeds: []
status: retired
tags:
  - engine
  - pass
  - pass-b3
  - missed
  - one-source
title: "G1.31.5.4.3: drift rule has one source (drift_check.py called by driver.sh), brief._strip_thought pinned by a test, copilot flags probed vs copilot --help"
town: core
---
# goal:g1.31.5.4.3

## Why this exists
goal:g1.31.5.4: 3 PASS B3 `missed` rows (all residue): a rule written twice, a behaviour change no test pins, and harness flags never probed. Verify files are under `.agi/sessions/workflows/runs/`. Re-read at HEAD d4b7ead17:
```
n    round (verify file)                                                                              HEAD cite
2    a00-4d063889-c4e95d (mur-pb3chunk10of20)                                                         driver.sh:138-181 · bin/drift_check.py
75   engine-delta-2 (mur-pb3chunk1of20)                                                               brief.py:2354-2361 -> node_writer.py:1077 (:1014)
104  l4-copilot-cli-is-a-third-harness-with-the-same-hooks-as-claude-code-and-pi (mur-pb3chunk6of20)  templates/harness/copilot-cli.toml:16-17 · :23 · :38
```
```
n2   driver.sh:138 if SKIP_ENGINE_DRIFT_CHECK unset -> :139 python3 -c "...drift..." (inline copy)
     drift_check.py: the same rule, no SKIP_ENGINE_DRIFT_CHECK, 0 callers (listed only in commands.md / test_commands_manifest)
n75  brief._strip_thought -> node_writer.strip_thought (^-anchored, MULTILINE): an indented or quoted pair is no longer stripped
     0 tests name brief._strip_thought    (snapshot-goals.py:192 now delegates to node_writer: that "third copy" half is FIXED)
n104 toml renders --effort (:16) and --remote (:23 seat, :38 dispatch); the one quoted `copilot --help`
     (experiment a00-5510f914-f1ae48.md:32-37) lists neither; test_rotate_copilot_harness.py compares builder to template only
     copilot binary absent on this box -> probe owed on a box that has it
```

## Target end-state
- n2: the drift rule has one source. `driver.sh` calls `extensions/agi/bin/drift_check.py`, and `drift_check.py` honours `SKIP_ENGINE_DRIFT_CHECK` itself. driver.sh holds no inline `python3 -c` copy.
- n75: a committed test pins `brief._strip_thought`. A top-level THOUGHT region is stripped, while an indented or quoted `THOUGHT:BEGIN … END` pair survives, which is the anchored narrowing that node_writer.py:1014 defines.
- n104: every flag and const that `copilot-cli.toml` renders (`--model`, `--effort`, `--allow-all`, `--remote`, `-i`, `-p`) is checked against a verbatim `copilot --help` captured on a box that has the binary. The capture is quoted into a node and committed as a test fixture, and `test_rotate_copilot_harness.py` asserts each rendered flag appears in it. Any flag that is absent is removed from the toml.

## Invariants
- A residue is closed by a reviewed round, never by a note.
- One source per rule (diagram B). A wrapper that delegates is not a copy.
- A probe run on another box is quoted verbatim, with no host name, user or path.

## Falsifier
1. From /data/work/agi (rc 1 at HEAD d4b7ead17, measured: the first 2 conjuncts fail):
```bash
bash -c '! sed -n "/SKIP_ENGINE_DRIFT_CHECK/,/^fi/p" extensions/agi/driver.sh | grep -q "python3 -c" &&
grep -q "drift_check.py" extensions/agi/driver.sh && grep -q SKIP_ENGINE_DRIFT_CHECK extensions/agi/bin/drift_check.py &&
git grep -q "brief._strip_thought" -- extensions/agi/tests &&
python3 -m pytest extensions/agi/tests/test_rotate_copilot_harness.py -q -k help_text --basetemp /tmp/g13154c'
```
2. Negative: `git grep -n 'python3 -c' -- extensions/agi/driver.sh` returns zero hits (1 at HEAD: :139).

## Out of scope
goal:g1.31.4.5 (the bogus `engine_commit` drift) · goal:g1.31.4.6.1 (the behavioural drift test) · goal:g1.31.4.2.1 (copilot hooks and meter) · goal:g1.31.5.4.1 · goal:g1.31.5.4.2 · goal:g1.31.5.1-.3 · goal:g1.31.5.5 · goal:g1.31.1-.3 · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-6**.
n104's probe needs a box with the copilot binary, and there is none here. Route the capture to a post on such a box, and never print its host name.

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
