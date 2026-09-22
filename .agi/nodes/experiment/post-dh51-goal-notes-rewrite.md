---
id: experiment:post-dh51-goal-notes-rewrite
mint_id: 30a210725bc747e6a46b44c30c7919b3
type: experiment
parents:
  - hypothesis:a00-d476be80-b65dbe
next_edges: []
edited_by: a00-d476be80
line_ceiling: 40
loop: goal:g7.31.4.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 1f91b0afc9701fa3
season: 2
testable_claim: "The goal:g7.31.4.2 Agent Notes and THOUGHT, rewritten on this base, describe the measured post-DH.51 state: five residues closed, module SEVEN, 0 production lines, DH.67 duplicate absent."
title: Rewrite goal:g7.31.4.2 notes to measured post-DH.51 state
town: core
---
<!-- BODY:BEGIN -->
# experiment:post-dh51-goal-notes-rewrite

## Experiment

DH.71 corrective residue round on `goal:g7.31.4.2`. The deliverable is the
goal node's own prose: its Agent Notes and THOUGHT still carried the DH.43
wording ("PRIMARY residue remains", "NO merge-up while residues>0") although
DH.51 had closed every residue. This round rewrites both to the measured
state and records what was measured, live, in THIS checkout.

No production byte changed. `git diff --numstat` over `extensions/agi/bin`,
`src`, `skills` is empty; `git status --porcelain -- extensions/agi/bin/send.py`
is empty. 0 production lines (ceiling 40).

## Commands and real output

Re-measurement of the central claim:

```
$ python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q
.......                                                                  [100%]
7 passed in 6.00s
$ grep -c '^def test_' extensions/agi/tests/test_send_surface_ssh_or_not.py
7
```

(The leading `tier-gate: phantom running record .../a00-7f12739a/... (dead)`
line is another loop's noise, not this run's result.)

The five residue loci, verified live (not trusted from the brief):

1. `grep -c '6 passed, 0 production lines' .agi/nodes/hypothesis/a00-ac47d671-4fc781.md` -> **0**; line 56 reads the measured `7 passed (re-measured DH.51: pytest 7 passed, grep -c "^def test_" -> 7), 0 production lines`. CLOSED.
2. `experiment:tmux-seam-residue-closed-a00-ac47d671` `probes[0].observed` reads: "the stale '6 passed' string survived at TWO loci -- the THOUGHT quote in this experiment AND the Agent Notes of hypothesis:a00-ac47d671-4fc781"; both named. CLOSED.
3. `grep -n '1894\|1908\|1884\|_leave_copy_mode\|_pane_in_mode' .agi/nodes/hypothesis/a00-768e0fd0-6e3cb8.md` -> line 83 cites `_leave_copy_mode (def send.py:1894, tmux send-keys -X cancel call send.py:1908)` and states "1884 is inside _pane_in_mode (def 1879), not _leave_copy_mode". CLOSED.
4. `grep -n THOUGHT .agi/nodes/hypothesis/a00-b11f67e2-f2ed9b.md` -> line 53 says "Deviation recorded on THIS hypothesis node own THOUGHT". CLOSED.
5. `grep -n '4 passed\|4 tests' .../send-surface-real-path-and-residues-a00-e2960dc3.md .../send-surface-ssh-or-not-a00-dd757e64.md` -> historical transcript lines only (a DH.25 `pytest ... 4 passed in 0.74s` code block and a "(4 tests: ...)" evidence sentence). No live node presents them as current; not an open item on the goal. CLOSED as historical.

## Base divergence (measured, not assumed)

This checkout is cut from `seat/director-helper@s2` @ `1837c9ae`, which does NOT
carry the DH.67 commits:

```
$ ls .agi/nodes/hypothesis/ | grep -i 'post-dh51' || echo ABSENT
ABSENT
$ ls .agi/nodes/deprecated/hypothesis/ | grep -i 'post-dh51' || echo ABSENT
ABSENT
$ ls .agi/nodes/hypothesis/ | grep 4d9c90ee || echo ABSENT
ABSENT
$ ls .agi/nodes/experiment/ | grep -i post-dh51 || echo ABSENT
ABSENT
```

So residue #1 (retire the deprecated duplicate) has nothing to act on in THIS
checkout: a status-blind live-dir globber finds no duplicate. The absence is
recorded; no `post-dh51-residues-closed` file was invented and no DH.67 node
was brought forward. Base reconciliation is the parent/director's.

## What landed

`goal:g7.31.4.2` — Agent Notes and THOUGHT whole-replaced (`replace body
31:49` + `thought`) to the measured post-DH.51 state: five residues closed at
their loci, module SEVEN, 0 production lines, no open residue, merge-up no
longer gated by residues, DH.67 duplicate absent on this base.

## Deviation from the brief

The brief named `write.py note` for the goal Agent Notes. `note` APPENDS under
`## Agent Notes`; that append-to-a-section shape is exactly what left the
DH.43 stale table in the goal body (and the duplicate `# goal:g7.31.4.2`
heading). I used the sanctioned whole-body `replace body 31:49` round trip
instead, plus the `thought` verb — whole replacement, never append, as the
brief's own deliverable sentence requires.

## Evidence

Raw output, screenshots, logs.
