---
id: experiment:dh154-goal-record-truth-closure
mint_id: c30b100154ff47b1bcc6d4bf3ac76248
type: experiment
parents:
  - hypothesis:a00-6ff315cb-75c51c
next_edges: []
confidence: 0.9
edited_by: a00-6ff315cb
evidence_runs:
  - experiment:dh154-goal-record-truth-closure
line_ceiling: 40
loop: goal:g7.31.4.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "grep -c '6 passed, 0 production lines' .agi/nodes/hypothesis/a00-ac47d671-4fc781.md; grep -n '7 passed' on the same file; python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q", "expected": "stale claim phrase absent (0); the live Agent Notes line carries the measured 7; live pytest still measures 7 passed", "observed": "0; line reads '... 7 passed (re-measured DH.51: pytest 7 passed, grep -c \"^def test_\" -> 7), 0 production lines.'; live DH.154 re-run: 7 passed in 24.65s", "result": "held"}
  - {"conjunct": 2, "class": "wire", "cmd": "parse probes[0].observed from .agi/nodes/experiment/tmux-seam-residue-closed-a00-ac47d671.md", "expected": "observed names BOTH stale-string loci: this experiment THOUGHT quote AND the Agent Notes of hypothesis:a00-ac47d671-4fc781", "observed": "DH.51 amendment. corrected Evidence tail: the stale '6 passed' string survived at TWO loci -- the THOUGHT quote in this experiment AND the Agent Notes of hypothesis:a00-ac47d671-4fc781 -- while the stale 'Six tests' string lived only in the THOUGHT quote. hypothesis:a00-ac47d671-4fc781 was closed in DH.51 ...", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "sed -n '1879p;1884p;1894p;1908p' extensions/agi/bin/send.py", "expected": "1894 is 'def _leave_copy_mode', 1908 is the tmux send-keys -X cancel call; 1884 is inside _pane_in_mode (def 1879)", "observed": "1879: def _pane_in_mode(target: str) -> bool: ; 1884: [\"tmux\", \"display-message\", \"-p\", \"-t\", target, ; 1894: def _leave_copy_mode(target: str) -> bool: ; 1908: [\"tmux\", \"send-keys\", \"-t\", target, \"-X\", \"cancel\"],", "result": "held"}
  - {"conjunct": 4, "class": "gate", "cmd": "grep -c 'Deviation recorded in the experiment node' and grep -c 'Deviation recorded on THIS hypothesis node' on .agi/nodes/hypothesis/a00-b11f67e2-f2ed9b.md", "expected": "old pointer absent (0); corrected pointer present (1)", "observed": "grep -c 'Deviation recorded in the experiment node' -> 0; grep -c 'Deviation recorded on THIS hypothesis node' -> 1", "result": "held"}
  - {"conjunct": 5, "class": "wire", "cmd": "read the DH.25-era counts and grep their inbound references across .agi/nodes", "expected": "counts remain as historical records and no live node cites them as the current count", "observed": "send-surface-real-path-and-residues-a00-e2960dc3.md:53 '4 passed in 0.74s'; send-surface-ssh-or-not-a00-dd757e64.md:120 '(4 tests: ...)'; referenced only by their own hypothesis parents and goal:g7.31.4.2 residue table", "result": "held"}
  - {"conjunct": 6, "class": "gate", "cmd": "grep -c 'Queue DH.51' .agi/nodes/goal/g7.31.4.2.md (before and after the rewrite)", "expected": "1 before the rewrite; 0 after -- the stale queue line is replaced by the DH.154 close-out", "observed": "1 before; 0 after the write.py goal:g7.31.4.2 replace body 33:49 -", "result": "held"}
  - {"conjunct": 7, "class": "gate", "cmd": "grep -rn is_ssh extensions/agi/bin extensions/agi/src skills ; echo exit=$?", "expected": "exit 1, zero hits -- the central claim's no-caller-branch-on-is_ssh invariant still holds", "observed": "no output; exit=1", "result": "held"}
  - {"conjunct": 8, "class": "gate", "cmd": "git diff --numstat -- extensions/agi/bin extensions/agi/src skills", "expected": "empty; the round changes node files only, 0 production lines", "observed": "empty", "result": "held"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 6d4b8997babf3393
season: 2
testable_claim: The five MUR residues on goal:g7.31.4.2 are closed and the goal-level Agent Notes no longer presents any as open or queues DH.51 as future work; 0 production lines.
title: "DH.154 goal-record truth closure: five residues re-measured, none open"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:dh154-goal-record-truth-closure

## Experiment

DH.154 residue/record round on `goal:g7.31.4.2`. The five MUR residues from
`mur-g7-31-4-2-dh-43-5ef0dc14b-3` were landed by DH.51
(`experiment:dh51-residue-closure-a00-e1e6807b`) but the goal node's own Agent
Notes still presented all five as OPEN and queued DH.51 as future work. This
round re-measured every figure live FIRST, ran one negative probe per residue,
then whole-replaced the goal-level residue table and the stale queue line. Node
files only; zero production lines.

### Re-measurements (live, before any write)

```
$ python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q
.......                                                                  [100%]
7 passed in 24.65s

$ grep -c '^def test_' extensions/agi/tests/test_send_surface_ssh_or_not.py
7

$ grep -rn is_ssh extensions/agi/bin extensions/agi/src skills
(no output; exit 1, zero hits)

$ sed -n '1879p;1884p;1894p;1908p' extensions/agi/bin/send.py
def _pane_in_mode(target: str) -> bool:
            ["tmux", "display-message", "-p", "-t", target,
def _leave_copy_mode(target: str) -> bool:
            ["tmux", "send-keys", "-t", target, "-X", "cancel"],

$ grep -c 'Queue DH.51' .agi/nodes/goal/g7.31.4.2.md
1        # before this round's rewrite; -> 0 after

$ git diff --numstat -- extensions/agi/bin extensions/agi/src skills
(empty)
```

### Negative probes, one per residue

| # | residue | negative probe (would fail if the claim were false) | result |
|---|---------|-----------------------------------------------------|--------|
| 1 | hyp a00-ac47d671 read "6 passed" | grep the stale phrase AND re-run pytest live: stale phrase absent (0) while live pytest still measures 7, and the node reads "measured 7 / SEVEN" | held |
| 2 | probe overstated "only THOUGHT" | parse `experiment:tmux-seam-residue-closed-a00-ac47d671` probes[0].observed and require BOTH loci named: the experiment THOUGHT AND hyp a00-ac47d671 Agent Notes | held |
| 3 | `_leave_copy_mode` mis-cite | read live `send.py`: 1884 must be inside `_pane_in_mode` (def 1879), 1894 must be `def _leave_copy_mode`, 1908 the cancel call | held |
| 4 | deviation pointer names experiment THOUGHT | grep `hypothesis:a00-b11f67e2-f2ed9b`: old pointer absent (0), "on THIS hypothesis node own THOUGHT" present (1) | held |
| 5 | DH.25-era `4` counts | read the two experiments and grep inbound references: counts are correct for their own round and no live node cites them as the current count | held |

### Goal-level rewrite

`write.py goal:g7.31.4.2 'replace body 33:49 -'` whole-replaced the stale
`### Residue round` table + central-claim line + THOUGHT with the DH.154
close-out: every row marked CLOSED with its closing measurement/citation, and
the `Next parent: DH.51 ...` line replaced by a DH.154 line stating DH.51 is
DONE (not queued) and the round closed the goal-level record with 0 production
lines. The base Agent Notes line (`Assigned to **director-helper**. ...`) was
kept intact.

## Evidence

Raw command tails:

```
$ python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q
7 passed in 24.65s
$ grep -c '^def test_' extensions/agi/tests/test_send_surface_ssh_or_not.py
7
$ grep -rn is_ssh extensions/agi/bin extensions/agi/src skills ; echo "exit=$?"
exit=1
$ grep -c 'Queue DH.51' .agi/nodes/goal/g7.31.4.2.md
0        # after the rewrite
$ git diff --numstat -- extensions/agi/bin extensions/agi/src skills
(empty)
```

Production lines: 0 (only `.agi/nodes/*.md` changed). Ceiling 40.

## Residue table (post-close, goal-level)

| # | locus | old | new | state |
|---|-------|-----|-----|-------|
| 1 | hypothesis:a00-ac47d671-4fc781 | `6 passed` claim | measured `7 passed` / SEVEN | CLOSED |
| 2 | experiment:tmux-seam-residue-closed-a00-ac47d671 probes[0] | "only the THOUGHT" | names both loci | CLOSED |
| 3 | hypothesis:a00-768e0fd0-6e3cb8 | `1884/1908` | def@1894 call@1908 (+live siblings) | CLOSED |
| 4 | hypothesis:a00-b11f67e2-f2ed9b | "in the experiment node" | "on THIS hypothesis node own THOUGHT" | CLOSED |
| 5 | experiment:e2960dc3 / experiment:dd757e64 | DH.25-era `4` | left historical, declared in this node | CLOSED (historical) |

## Agent Notes
DH.154 closed the goal-level residue record on goal:g7.31.4.2: re-measured all five MUR mur-g7-31-4-2-dh-43-5ef0dc14b-3 figures live (pytest 7 passed, grep -c '^def test_' 7, is_ssh sweep exit 1, send.py 1884 inside _pane_in_mode def 1879 / _leave_copy_mode def 1894 / cancel call 1908), rewrote the Agent Notes table every row CLOSED with its closing measurement, replaced the stale DH.51 queue line with the DH.154 close-out; 0 production lines.
