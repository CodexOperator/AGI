---
id: experiment:g7-31-4-2-dh51-closure-reremeasure
mint_id: 89454d3e72d94280af94486e57bd0db9
type: experiment
parents:
  - hypothesis:a00-722277f3-a7148a
next_edges: []
edited_by: a00-722277f3
evidence_runs:
  - experiment:g7-31-4-2-dh51-closure-reremeasure
line_ceiling: 40
loop: goal:g7.31.4.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q; grep -c '^def test_' on the module", "expected": "7 passed and 7 test defs, matching the DH.51 rewritten record", "observed": "7 passed in 16.69s; grep -c -> 7", "result": "held"}
  - {"conjunct": 2, "class": "wire", "cmd": "grep -c '6 passed, 0 production lines' and grep -n '7 passed' on hypothesis:a00-ac47d671-4fc781", "expected": "0 hits for the stale string; the node reads the measured 7 / SEVEN", "observed": "0; lines 52 and 56 read DH.51 re-measured pytest 7 passed and 7 / SEVEN", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "parse probes[0].observed of experiment:tmux-seam-residue-closed-a00-ac47d671", "expected": "names BOTH stale-string loci (that experiment THOUGHT AND hypothesis:a00-ac47d671-4fc781 Agent Notes)", "observed": "DH.51 amendment ... the stale 6 passed string survived at TWO loci -- the THOUGHT quote in this experiment AND the Agent Notes of hypothesis:a00-ac47d671-4fc781 ... hypothesis:a00-ac47d671-4fc781 was closed in DH.51 (now reads 7 / SEVEN)", "result": "held"}
  - {"conjunct": 4, "class": "gate", "cmd": "sed -n '1884p;1894p;1908p' extensions/agi/bin/send.py", "expected": "1884 inside _pane_in_mode; 1894 def _leave_copy_mode; 1908 the tmux send-keys -X cancel call", "observed": "1884 tmux display-message -p -t target (inside _pane_in_mode); 1894 def _leave_copy_mode(target: str) -> bool; 1908 tmux send-keys -t target -X cancel", "result": "held"}
  - {"conjunct": 5, "class": "wire", "cmd": "grep -c 'Deviation recorded in the experiment node' and grep -c 'on THIS hypothesis node' on hypothesis:a00-b11f67e2-f2ed9b", "expected": "0 and 1 -- the deviation pointer names the hypothesis node, not the experiment THOUGHT", "observed": "0; 1", "result": "held"}
  - {"conjunct": 6, "class": "wire", "cmd": "grep the DH.25-era counts and their inbound references across .agi/nodes", "expected": "counts remain historical records; no live node cites them as the current count", "observed": "send-surface-real-path-and-residues-a00-e2960dc3.md:53 '4 passed in 0.74s'; send-surface-ssh-or-not-a00-dd757e64.md:120 '(4 tests: ...)'; referenced only by their own hypothesis parents and the goal node stale residue table", "result": "held"}
  - {"conjunct": 7, "class": "auth", "cmd": "grep -rn is_ssh extensions/agi/bin; git diff --numstat -- extensions/agi/bin src", "expected": "0; empty -- no caller branch on is_ssh and 0 production lines", "observed": "0; empty", "result": "held"}
  - {"conjunct": 8, "class": "gate", "cmd": "on the BUILT goal node: grep -c 'Next parent: DH.51'; grep -c 'Residues closed (DH.51 harvest'; grep -c 'DH.51-closure delta'", "expected": "0; 1; 1 -- the stale queued-parent sentence and residue table are gone, the closure table and THOUGHT delta are present", "observed": "0; 1; 1", "result": "held"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: adbf1d7f859b79e9
season: 2
testable_claim: With the five DH.43 residues already closed in DH.51 (harvest 9f15ab27c), the five closure claims re-measure TRUE on the live bytes and goal:g7.31.4.2's own Agent Notes and THOUGHT whole-replaced to the closed state carry no stale queued-parent record and 0 production lines.
title: Re-measure all five DH.51 residue closures on live bytes, then whole-replace the stale goal:g7.31.4.2 Agent Notes and THOUGHT
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:g7-31-4-2-dh51-closure-reremeasure


## Experiment

**Build-order round on `goal:g7.31.4.2`.** The residue is a stale record inside
the goal node's own authored regions, not a production defect: `## Agent Notes`
still listed the five DH.43 residues as open, and the `THOUGHT` still queued a
"DH.51 corrective parent" that had already run (kid `a00-e1e6807b`, harvest
`9f15ab27c`, an ancestor of this tip). This round measured the pre-fix state,
whole-replaced both regions with the measured closed state, and proved on the
built bytes.

### Pre-fix measurement — all seven checks confirmed, none falsified

```
$ python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q
7 passed in 16.69s
$ grep -c '^def test_' extensions/agi/tests/test_send_surface_ssh_or_not.py
7
$ grep -c '6 passed, 0 production lines' .agi/nodes/hypothesis/a00-ac47d671-4fc781.md
0
$ grep -n '7 passed' .agi/nodes/hypothesis/a00-ac47d671-4fc781.md
52:... re-measured DH.51: pytest 7 passed, grep -c "^def test_" -> 7 ...
56:... 7 passed (re-measured DH.51: ...), 0 production lines. Prior "6 passed" ...
$ sed -n '1884p;1894p;1908p' extensions/agi/bin/send.py
            ["tmux", "display-message", "-p", "-t", target,
def _leave_copy_mode(target: str) -> bool:
            ["tmux", "send-keys", "-t", target, "-X", "cancel"],
$ grep -c 'Deviation recorded in the experiment node' .agi/nodes/hypothesis/a00-b11f67e2-f2ed9b.md
0
$ grep -c 'on THIS hypothesis node' .agi/nodes/hypothesis/a00-b11f67e2-f2ed9b.md
1
$ grep -rn is_ssh extensions/agi/bin | wc -l
0
$ git diff --numstat -- extensions/agi/bin src
(empty)
```

`probes[0].observed` of `experiment:tmux-seam-residue-closed-a00-ac47d671`
names BOTH stale loci explicitly (its own THOUGHT and the Agent Notes of
`hypothesis:a00-ac47d671-4fc781`). The DH.25-era `4 passed` counts at
`send-surface-real-path-and-residues-a00-e2960dc3.md:53` and
`send-surface-ssh-or-not-a00-dd757e64.md:120` sit inside those nodes' own
Evidence/THOUGHT history; no live node cites them as the current count.

### The fix — two whole-replaces, through `write.py`, no hand edit

1. `write.py goal:g7.31.4.2 'replace body 35:45 -'` — the five-row DH.43
   residue table and the `Next parent: DH.51` sentence replaced by the
   `### Residues closed (DH.51 harvest 9f15ab27c)` table ending "no corrective
   parent is queued".
2. `write.py goal:g7.31.4.2 'thought ...'` — the queued-DH.51 THOUGHT
   replaced by the DH.51-closure delta.

Whole-replace, not append: an accumulating Agent Notes file would leave two
tables that disagree — the residue being closed. The duplicate heading
`# goal:g7.31.4.2` at body line 33 is pre-existing and left alone.

## Evidence

Post-fix, measured on the live node:

```
$ grep -c 'Next parent: DH.51' .agi/nodes/goal/g7.31.4.2.md
0
$ grep -c 'sev | defect | locus | close' .agi/nodes/goal/g7.31.4.2.md
0
$ grep -c 'Residues closed (DH.51 harvest' .agi/nodes/goal/g7.31.4.2.md
1
$ grep -c 'DH.51-closure delta' .agi/nodes/goal/g7.31.4.2.md
1
$ git diff --numstat -- extensions/agi/bin src
(empty)
$ git status --porcelain -- .agi/nodes
 M .agi/nodes/goal/g7.31.4.2.md
?? .agi/nodes/experiment/g7-31-4-2-dh51-closure-reremeasure.md
?? .agi/nodes/hypothesis/a00-722277f3-a7148a.md
```

Only the goal node plus this round's two nodes changed; **0 production lines**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.51-closure re-measure plus build. This version differs from the DH.51 records because it re-measures all five closures on THIS tip's live bytes instead of trusting the DH.51 result files, and then BUILDS the fix the goal node still needed: exercise p05 of DH.51 asserted the residue table had no inbound reference problem, but goal:g7.31.4.2's own Agent Notes still listed the five defects as open and its THOUGHT still queued a DH.51 corrective parent that had already run. Whole-replaced body 35:45 with the closure table and rewrote the THOUGHT via write.py. 0 production lines, .agi/nodes/*.md only.
<!-- THOUGHT:END -->
