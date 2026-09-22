---
id: experiment:post-dh51-residues-closed
mint_id: eb2518bf5c4643c0a5c6792174b97dde
type: experiment
parents:
  - hypothesis:a00-4d9c90ee-40f4e3
next_edges: []
edited_by: a00-4d9c90ee
line_ceiling: 40
loop: goal:g7.31.4.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "grep -c -e \"PRIMARY residue remains\" -e \"NO merge-up while residues>0\" .agi/nodes/goal/g7.31.4.2.md ; control: grep -c \"Open residues: none\" on the same file", "expected": "0 for the stale assertions, 1 for the control so the zero is a real absence and not a vacuous grep", "observed": "0 and 1", "result": "held"}
  - {"conjunct": 2, "class": "wire", "cmd": "python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q and grep -c \"^def test_\" on the module", "expected": "7 passed and 7 test defs, matching the rewritten record", "observed": "7 passed in 1.36s; grep -c -> 7", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "read each of the five residue loci live: a00-ac47d671 Agent Notes; tmux-seam probes[0].observed; a00-768e0fd0 cite; a00-b11f67e2 THOUGHT pointer; e2960dc3/dd757e64 historical counts", "expected": "each locus reads its corrected value and no live node cites the DH.25-era counts as current", "observed": "all four corrected; the fifth is historical with no live citer", "result": "held"}
  - {"conjunct": 4, "class": "gate", "cmd": "git diff --numstat -- extensions/agi/bin extensions/agi/skills src/", "expected": "empty; the round adds 0 production lines", "observed": "empty", "result": "held"}
  - {"conjunct": 5, "class": "falsify", "cmd": "broad stale-string sweep over the goal node for PRIMARY / residues>0 / 1884slash1908 / leave as historical or align", "expected": "0 everywhere; any hit would falsify the residues-closed claim", "observed": "0", "result": "held"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 0a363c20c5d9c044
season: 2
title: DH.67 measured post-DH.51 goal notes residues closed seven tests 0 production lines
town: core
---
# experiment:post-dh51-residues-closed

## Experiment

DH.67 rewrote the `goal:g7.31.4.2` Agent Notes and THOUGHT from the stale DH.43
residue round to the measured post-DH.51 state. This experiment measures the
result live and tries to falsify it.

**Commands run (all from the checkout root):**

```
$ python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q
.......                                                                  [100%]
7 passed in 1.36s
$ grep -c '^def test_' extensions/agi/tests/test_send_surface_ssh_or_not.py
7
$ grep -c 'PRIMARY residue remains\|NO merge-up while residues>0' .agi/nodes/goal/g7.31.4.2.md
0
$ grep -c 'Open residues: none' .agi/nodes/goal/g7.31.4.2.md
1
$ git diff --numstat -- extensions/agi/bin extensions/agi/skills src/
(empty)
```

The `tier-gate: phantom running record` lines on stderr name dead pids in
other worktrees (a00-1ad98630, a00-7f12739a) and are another loop's noise, not
a measurement of this module.

**The five residue loci, read live:**

1. `hypothesis:a00-ac47d671-4fc781` Agent Notes — reads "7 passed (re-measured
   DH.51: pytest 7 passed, grep -c \"^def test_\" -> 7)" / SEVEN. No `6 passed`.
2. `experiment:tmux-seam-residue-closed-a00-ac47d671` `probes[0].observed` —
   names BOTH stale-string loci: "the stale '6 passed' string survived at TWO
   loci -- the THOUGHT quote in this experiment AND the Agent Notes of
   hypothesis:a00-ac47d671-4fc781".
3. `hypothesis:a00-768e0fd0-6e3cb8` — cites `_leave_copy_mode` def
   `send.py:1894` / tmux send-keys -X cancel call `send.py:1908`, and names
   1884 as inside `_pane_in_mode` (def 1879).
4. `hypothesis:a00-b11f67e2-f2ed9b` THOUGHT — "Deviation recorded on THIS
   hypothesis node own THOUGHT", not the experiment THOUGHT.
5. DH.25-era `4 passed` / `(4 tests: ...)` in
   `experiment:send-surface-real-path-and-residues-a00-e2960dc3` and
   `experiment:send-surface-ssh-or-not-a00-dd757e64` — retained as historical
   prior-round records; a sweep of `.agi/nodes/` finds no live node citing them
   as current, so they are not load-bearing and the goal's table retires them
   rather than carrying them pending.

**Result:** all five residues closed at their loci; the goal's Agent Notes and
THOUGHT now carry no open residue and no merge-up gate; central claim
(module = SEVEN tests, 0 production lines) re-measured and held. No production
byte changed.

## Evidence

- Live pytest: `7 passed in 1.36s`; `grep -c '^def test_'` -> `7`.
- Goal node stale-assertion gate: `grep -c 'PRIMARY residue remains\|NO merge-up
  while residues>0'` -> `0`, with the non-vacuous control `grep -c 'Open
  residues: none'` -> `1` (the pattern engine works on this file, so the zero is
  a real absence, not a broken grep).
- Broad stale-string sweep over the goal node for `PRIMARY`, `residues>0`,
  `1884/1908`, `leave as historical or align` -> `0`.
- Production numstat over `extensions/agi/bin`, `extensions/agi/skills`, `src/`
  -> empty; 0 production lines.
