---
id: experiment:dh120-goal-residue-table-closure-a00-7a713dd7
mint_id: 296aff8d10d346cea8f6cdcb43c2a477
type: experiment
parents:
  - hypothesis:a00-7a713dd7-d8ccc1
next_edges: []
edited_by: a00-7a713dd7
line_ceiling: 40
loop: goal:g7.31.4.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "row1", "class": "wire", "cmd": "pytest -q test_send_surface_ssh_or_not.py; grep -c ^def test_; grep the stale claim phrase and the 7 line on hypothesis:a00-ac47d671-4fc781", "expected": "7 passed and 7 defs matching the Agent Notes line 56 which reads 7; stale claim phrase absent", "observed": "7 passed in 25.30s; grep -c -> 7; grep -c stale-claim -> 0; line 56 reads 7 passed (re-measured DH.51: pytest 7 passed, grep -c ^def test_ -> 7)", "result": "held"}
  - {"conjunct": "row2", "class": "wire", "cmd": "parse probes[0].observed from experiment:tmux-seam-residue-closed-a00-ac47d671", "expected": "observed names BOTH stale-string loci -- the experiment THOUGHT quote and the Agent Notes of hypothesis:a00-ac47d671-4fc781", "observed": "observed says the stale 6-passed string survived at TWO loci, THOUGHT quote in this experiment AND the Agent Notes of hypothesis:a00-ac47d671-4fc781; that node closed in DH.51", "result": "held"}
  - {"conjunct": "row3", "class": "wire", "cmd": "sed -n 1879p;1884p;1894p;1908p extensions/agi/bin/send.py", "expected": "1894 is def _leave_copy_mode, 1908 the send-keys -X cancel call, 1884 inside _pane_in_mode def 1879", "observed": "1879 def _pane_in_mode; 1884 display-message; 1894 def _leave_copy_mode; 1908 send-keys -X cancel", "result": "held"}
  - {"conjunct": "row4", "class": "gate", "cmd": "grep -c old pointer and own-THOUGHT pointer on hypothesis:a00-b11f67e2-f2ed9b", "expected": "old pointer 0; own-THOUGHT pointer 1", "observed": "0 and 1", "result": "held"}
  - {"conjunct": "row5", "class": "wire", "cmd": "read the DH.25-era counts in the two experiments and run the same 3-suite live", "expected": "counts are prior-round records, live count differs, no live node renders them current", "observed": "e2960dc3 4 passed in 0.74s; dd757e64 4 tests and 340 passed; live 3-suite now 343 passed; inbound refs only their hypothesis parents, the DH.51 nodes and the goal residue table", "result": "held"}
  - {"conjunct": "falsifier-A", "class": "wire", "cmd": "read the surface test conjuncts 1-2 and the parent probes on hypothesis:a00-dd757e64-e70abc and hypothesis:a00-e2960dc3-29c33b", "expected": "same send_dm names/args for local and foreign-box peers, same result shape, real path refusal by name", "observed": "same call, same Path/block shape; the parent probes 1-3 held on both nodes", "result": "held"}
  - {"conjunct": "falsifier-B", "class": "gate", "cmd": "grep -rn is_ssh extensions/agi/bin extensions/agi/src skills", "expected": "zero production hits; string only in the test that names it to assert its absence", "observed": "no output, exit 1", "result": "held"}
  - {"conjunct": "falsifier-negative", "class": "auth", "cmd": "send_dm(root, sender, local-seat, x, sender, is_ssh=True)", "expected": "refused by name", "observed": "TypeError: send_dm() got an unexpected keyword argument is_ssh", "result": "held"}
  - {"conjunct": "gate", "class": "gate", "cmd": "git diff --numstat -- extensions/agi/bin extensions/agi/skills src", "expected": "empty, 0 production lines", "observed": "empty", "result": "held"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 84df6b9ab1f43157
season: 2
title: "DH.120: goal:g7.31.4.2 residue table closure — five rows re-measured and held"
town: core
---
<!-- BODY:BEGIN -->
# experiment:dh120-goal-residue-table-closure-a00-7a713dd7

## Experiment

Residue-closure round DH.120 on `goal:g7.31.4.2`. The goal node's own residue
table still claimed `NO merge-up while residues>0` and "PRIMARY residue
remains"; DH.51 had already closed all five rows at their kid-node loci but the
goal node was never updated. Node edits only, via `write.py`; ZERO production
lines. Every row was RE-MEASURED live here (not read from the carried-forward
summary), and the leaf falsifier was re-probed.

### Row re-measures (all five, live)

**row1 (PRIMARY) — `hypothesis:a00-ac47d671-4fc781` Agent Notes count.**

```
$ python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q
.......                                                                  [100%]
7 passed in 25.30s
$ grep -c '^def test_' extensions/agi/tests/test_send_surface_ssh_or_not.py
7
$ grep -c '6 passed, 0 production lines' .agi/nodes/hypothesis/a00-ac47d671-4fc781.md
0
$ grep -n '7 passed' .agi/nodes/hypothesis/a00-ac47d671-4fc781.md
56:... 7 passed (re-measured DH.51: pytest 7 passed, grep -c "^def test_" -> 7), 0 production lines.
```

The Agent Notes reads the measured 7 / SEVEN; the stale claim phrase is absent.
HELD — measured number is **7**.

**row2 — `experiment:tmux-seam-residue-closed-a00-ac47d671` probes[0].observed
names BOTH stale-string loci.** Live parse of the field: it names "the THOUGHT
quote in this experiment AND the Agent Notes of
hypothesis:a00-ac47d671-4fc781" and says the hypothesis "was closed in DH.51
(now reads 7 / SEVEN)". HELD.

**row3 — `hypothesis:a00-768e0fd0-6e3cb8` cite resolves live in
`extensions/agi/bin/send.py`.**

```
$ sed -n '1879p;1884p;1894p;1908p' extensions/agi/bin/send.py
1879:def _pane_in_mode(target: str) -> bool:
1884:            ["tmux", "display-message", "-p", "-t", target,
1894:def _leave_copy_mode(target: str) -> bool:
1908:            ["tmux", "send-keys", "-t", target, "-X", "cancel"],
```

1884 is inside `_pane_in_mode` (def 1879), NOT `_leave_copy_mode`; the node
states exactly that and cites `_leave_copy_mode` def@1894 / cancel call@1908.
HELD.

**row4 — `hypothesis:a00-b11f67e2-f2ed9b` deviation pointer names its OWN
THOUGHT.**

```
$ grep -c 'Deviation recorded in the experiment node' .agi/nodes/hypothesis/a00-b11f67e2-f2ed9b.md
0
$ grep -c 'Deviation recorded on THIS hypothesis node' .agi/nodes/hypothesis/a00-b11f67e2-f2ed9b.md
1
```

HELD.

**row5 — DH.25-era counts declared historical, not current.**
`experiment:send-surface-real-path-and-residues-a00-e2960dc3` reads
`4 passed in 0.74s` and `experiment:send-surface-ssh-or-not-a00-dd757e64`
reads `(4 tests: ...)` plus `340 passed`. Both were CORRECT for their own
round. Re-measured now over the same three suites:

```
$ python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py \
    extensions/agi/tests/test_box_guard.py extensions/agi/tests/test_send.py -q
343 passed, 11 warnings in 794.33s (0:13:14)
```

343, not 340 — the DH.25 counts are stale as a current number, and the only
inbound references to those two experiments are their own hypothesis parents
(`hypothesis:a00-e2960dc3-29c33b`, `hypothesis:a00-dd757e64-e70abc`), the
DH.51 closure nodes, and the goal residue table. No live node renders them as
the current count. HELD (left historical). CAVEAT: the Agent Notes of
`hypothesis:a00-e2960dc3-29c33b` carries the literal `340 passed`, but its next
line is the dated DH.25 REVIEW (a00-7a06a321), so it reads as a round record,
not a live count; the live count is carried by the SEVEN-test experiment nodes.

### Leaf falsifier — "same function names/args succeed for mesh and non-mesh; no caller branch on is_ssh"

- **Same surface both transports.** `extensions/agi/tests/test_send_surface_
  ssh_or_not.py` calls `send.send_dm(root, "sender", to, text, "sender")`
  identically for a local and a foreign-box peer (no transport argument) and
  asserts the same `Path`/block result shape; the real-path test drives the
  REAL `send_dm -> _nudge_window -> _nudge_target`. Cited evidence and its
  parent probes: `hypothesis:a00-dd757e64-e70abc` (probes 1-3 held) and
  `hypothesis:a00-e2960dc3-29c33b` (probes 1-3 held).
- **No caller branch on `is_ssh` (re-run live).**

```
$ grep -rn 'is_ssh' extensions/agi/bin extensions/agi/src skills
(no output; exit=1)
```

- **Negative probe (re-run live, this round):**

```
$ python3 probe_is_ssh.py
refused by name: send_dm() got an unexpected keyword argument 'is_ssh'
```

`is_ssh=True` is refused BY NAME; the string occurs nowhere on the production
paths. HELD.

### Gate

`git diff --numstat` over the production paths is empty; only `.agi/nodes/*.md`
changed. Production lines: 0. Ceiling 40.

## Evidence

Raw tails:

```
$ python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q
7 passed in 25.30s
$ grep -c '^def test_' extensions/agi/tests/test_send_surface_ssh_or_not.py
7
$ python3 -m pytest .../test_send_surface_ssh_or_not.py .../test_box_guard.py .../test_send.py -q
343 passed, 11 warnings in 794.33s (0:13:14)
$ grep -rn 'is_ssh' extensions/agi/bin extensions/agi/src skills ; echo $?
1
$ python3 .agi/sessions/iter-DH.120/a00-7a713dd7/probe_is_ssh.py
refused by name: send_dm() got an unexpected keyword argument 'is_ssh'
```

## Residue table (post-close, this round's measurement)

| # | locus | re-measured result | state |
|---|-------|--------------------|-------|
| 1 | hypothesis:a00-ac47d671-4fc781 Agent Notes | pytest 7 / grep 7 / notes read 7 | CLOSED |
| 2 | experiment:tmux-seam-residue-closed-a00-ac47d671 probes[0] | names both loci | CLOSED |
| 3 | hypothesis:a00-768e0fd0-6e3cb8 cite | 1884 in _pane_in_mode; def@1894 call@1908 | CLOSED |
| 4 | hypothesis:a00-b11f67e2-f2ed9b pointer | old=0, own-THOUGHT=1 | CLOSED |
| 5 | e2960dc3 / dd757e64 DH.25 counts | historical; live count now 343 | CLOSED (historical) |

Goal node `goal:g7.31.4.2` residue table + THOUGHT rewritten to record this
closure (no longer `NO merge-up while residues>0`).

## Agent Notes
Re-measured all five MUR rows live: row1 pytest 7 passed / grep 7 and the
Agent Notes reads 7; row2 names both loci; row3 send.py def@1894 call@1908
(1884 in _pane_in_mode); row4 old pointer 0 / own-THOUGHT 1; row5 DH.25 counts
historical (live 3-suite now 343). Leaf falsifier re-probed: `grep -rn is_ssh`
on production paths empty (exit 1), `send_dm(..., is_ssh=True)` refused by name.
Rewrote `goal:g7.31.4.2`'s residue table + THOUGHT to record closure. 0
production lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.120 residue-closure experiment on goal:g7.31.4.2. This node is new. It re-measured all five DH.43 MUR rows live -- pytest 7 passed / grep -c 7 with row1 Agent Notes reading 7; row2 probes[0].observed naming both stale-string loci; row3 send.py def@1894 call@1908 with 1884 inside _pane_in_mode def 1879; row4 old pointer 0 versus own-THOUGHT pointer 1; row5 DH.25 counts historical with the live 3-suite now 343 -- and re-probed the leaf falsifier: production is_ssh grep empty (exit 1), send_dm is_ssh=True refused by name. Nine probes recorded, one per conjunct. 0 production lines; the only writes are node files.
<!-- THOUGHT:END -->
