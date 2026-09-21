---
id: experiment:dh51-residue-closure-a00-e1e6807b
mint_id: 769aab3d132e40ee9d34ec1feb9c77c4
type: experiment
parents:
  - hypothesis:a00-e1e6807b-4c2526
next_edges: []
edited_by: a00-64ee01a6
line_ceiling: 40
loop: goal:g7.31.4.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "grep -c '6 passed, 0 production lines' and grep -n '7 passed' on .agi/nodes/hypothesis/a00-ac47d671-4fc781.md", "expected": "the stale claim phrase is absent (0) and the re-measured 7-passed line is present", "observed": "grep -c '6 passed, 0 production lines' -> 0; Agent Notes now reads '; 7 passed (re-measured DH.51: pytest 7 passed, grep -c \"^def test_\" -> 7), 0 production lines.'; surviving literal '6 passed' mentions are explicitly labelled DH.31-era historical", "result": "held"}
  - {"conjunct": 2, "class": "wire", "cmd": "parse probes[0].observed from .agi/nodes/experiment/tmux-seam-residue-closed-a00-ac47d671.md", "expected": "observed names BOTH stale-string loci: this experiment's THOUGHT quote AND the Agent Notes of hypothesis:a00-ac47d671-4fc781", "observed": "DH.51 amendment. corrected Evidence tail: 7 passed in 6.08s; the stale '6 passed' string survived at TWO loci -- the THOUGHT quote in this experiment AND the Agent Notes of hypothesis:a00-ac47d671-4fc781 -- while the stale 'Six tests' string lived only in the THOUGHT quote. hypothesis:a00-ac47d671-4fc781 was closed in DH.51 ...", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "sed -n '1894p;1908p' extensions/agi/bin/send.py (with 1879p/1884p context)", "expected": "1894 is 'def _leave_copy_mode', 1908 is the tmux send-keys -X cancel call; 1884 is inside _pane_in_mode (def 1879)", "observed": "1894: def _leave_copy_mode(target: str) -> bool: ; 1908: [\"tmux\", \"send-keys\", \"-t\", target, \"-X\", \"cancel\"], ; 1879: def _pane_in_mode(target: str) -> bool: with the display-message call at 1884", "result": "held"}
  - {"conjunct": 4, "class": "gate", "cmd": "grep -c 'Deviation recorded in the experiment node' and grep -c 'Deviation recorded on THIS hypothesis node' on .agi/nodes/hypothesis/a00-b11f67e2-f2ed9b.md", "expected": "old pointer absent (0); corrected pointer present (1)", "observed": "0 and 1", "result": "held"}
  - {"conjunct": 5, "class": "wire", "cmd": "grep the DH.25-era counts and their inbound references across .agi/nodes", "expected": "counts remain as historical records and no live node cites them as the current count", "observed": "send-surface-real-path-and-residues-a00-e2960dc3.md:53 '4 passed in 0.74s'; send-surface-ssh-or-not-a00-dd757e64.md:120 '(4 tests: ...)'; referenced only by their own hypothesis parents and goal:g7.31.4.2's residue table", "result": "held"}
  - {"conjunct": 6, "class": "gate", "cmd": "git diff --numstat -- extensions/agi/bin extensions/agi/skills src", "expected": "empty; the round changes node files only, 0 production lines", "observed": "empty", "result": "held"}
  - {"by": "parent", "conjunct": "residue-1 PRIMARY", "class": "gate", "cmd": "grep -c '6 passed, 0 production lines' .agi/nodes/hypothesis/a00-ac47d671-4fc781.md; grep -n '7 passed' on the same file", "expected": "stale phrase absent (0) and the live Agent Notes line carries the measured 7", "observed": "0; line 56 now reads '... 7 passed (re-measured DH.51: pytest 7 passed, grep -c \"^def test_\" -> 7), 0 production lines.'", "result": "held"}
  - {"by": "parent", "conjunct": "residue-1 PRIMARY", "class": "wire", "cmd": "python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q; grep -c '^def test_' on the module", "expected": "live re-measure agrees with the written 7", "observed": "7 passed in 2.81s; grep -c -> 7", "result": "held"}
  - {"by": "parent", "conjunct": "residue-2 NOTE", "class": "wire", "cmd": "parse probes[0].observed from experiment:tmux-seam-residue-closed-a00-ac47d671", "expected": "amended observed names BOTH stale-string loci (experiment THOUGHT and hypothesis:a00-ac47d671-4fc781 Agent Notes)", "observed": "names 'a00-ac47d671-4fc781' and 'THOUGHT' both true; result held", "result": "held"}
  - {"by": "parent", "conjunct": "residue-3 NOTE", "class": "wire", "cmd": "sed -n '1879p;1884p;1894p;1908p;1915p;1931p;2112p;2127p;2131p;2138p;2852p;2860p' extensions/agi/bin/send.py", "expected": "1894 is def _leave_copy_mode, 1908 the send-keys -X cancel call, 1884 inside _pane_in_mode def 1879; every added def/call pair resolves", "observed": "all live: 1879 def _pane_in_mode; 1884 display-message; 1894 def _leave_copy_mode; 1908 send-keys -X cancel; 1915/1931 _capture_pane; 2131/2138 _window_id_listed list-windows; 2852/2860 _send_keys; 2112 _list_windows; 2127 _window_listed", "result": "held"}
  - {"by": "parent", "conjunct": "residue-4 NOTE", "class": "gate", "cmd": "grep -c 'Deviation recorded in the experiment node' and grep -c 'Deviation recorded on THIS hypothesis node' on .agi/nodes/hypothesis/a00-b11f67e2-f2ed9b.md", "expected": "old pointer absent; corrected pointer present", "observed": "0 and 1", "result": "held"}
  - {"by": "parent", "conjunct": "residue-5 NOTE", "class": "wire", "cmd": "read the DH.25-era counts and grep their inbound references across .agi/nodes", "expected": "counts are prior-round records, no live node treats them as the current count", "observed": "e2960dc3 '4 passed in 0.74s', dd757e64 '(4 tests: ...'; references only the goal residue table, their own hypothesis parents, sibling experiments and the DH.51 nodes", "result": "held"}
  - {"by": "parent", "conjunct": "round constraint", "class": "gate", "cmd": "git diff --numstat -- extensions/agi/bin extensions/agi/skills src; git status --porcelain", "expected": "no production bytes changed; only the four target nodes plus the kid's two new nodes", "observed": "numstat empty; porcelain shows exactly the 4 target node files modified (kid's 2 nodes committed at 479386d26)", "result": "held"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 2f475f402f14826d
season: 2
testable_claim: "Each of the five MUR residues on goal:g7.31.4.2 is closed: the old stale text is gone from its locus and the new text carries a re-measured value or a corrected citation, with 0 production lines changed."
title: "DH.51 residue closure: five MUR residues on goal:g7.31.4.2 re-measured and closed"
town: core
---
<!-- BODY:BEGIN -->
# experiment:dh51-residue-closure-a00-e1e6807b

## Experiment

Residue-closure round DH.51 on `goal:g7.31.4.2`, closing the five residues left
by MUR `mur-g7-31-4-2-dh-43-5ef0dc14b-3` (`accept_with_residue` @19:42Z).
Node edits only, via `write.py`; zero production lines. The central claim
(committed test module carries SEVEN tests, 0 production lines) is untouched
and re-measured here, not re-litigated.

### 1 PRIMARY — `hypothesis:a00-ac47d671-4fc781`, Agent Notes (was "6 passed")

Re-measured FIRST, then wrote the measurement:

```
$ python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q
.......                                                                  [100%]
7 passed in 3.49s
$ grep -c '^def test_' extensions/agi/tests/test_send_surface_ssh_or_not.py
7
```

The Agent Notes line was rewritten with `write.py replace body 34:34 -` to
`7 passed (re-measured DH.51: pytest 7 passed, grep -c "^def test_" -> 7)`. The
old claim phrase `6 passed, 0 production lines` is gone; the two surviving
literal `"6 passed"` mentions are explicitly labelled DH.31-era historical (the
node THOUGHT and the corrected Agent Notes), not live claims.

### 2 NOTE — `experiment:tmux-seam-residue-closed-a00-ac47d671` probes[0]

`probes[0].observed` claimed the stale strings "survive only inside the
THOUGHT". False: the hypothesis Agent Notes also carried `6 passed` (residue 1).
Amended with `write.py set probes <json>`; `observed` now names BOTH loci and
states the post-close state.

```
$ python3 -c "parse probes[0].observed"
DH.51 amendment. corrected Evidence tail: 7 passed in 6.08s; the stale '6 passed'
string survived at TWO loci -- the THOUGHT quote in this experiment AND the Agent
Notes of hypothesis:a00-ac47d671-4fc781 -- while the stale 'Six tests' string lived
only in the THOUGHT quote. hypothesis:a00-ac47d671-4fc781 was closed in DH.51 ...
```

### 3 NOTE — `hypothesis:a00-768e0fd0-6e3cb8` mis-cite

Live read of `extensions/agi/bin/send.py`:

```
$ sed -n '1879p;1884p;1894p;1908p' extensions/agi/bin/send.py
1879:def _pane_in_mode(target: str) -> bool:
1884:            ["tmux", "display-message", "-p", "-t", target,
1894:def _leave_copy_mode(target: str) -> bool:
1908:            ["tmux", "send-keys", "-t", target, "-X", "cancel"],
```

So `1884` is inside `_pane_in_mode` (def 1879), NOT `_leave_copy_mode`. The
line was corrected to `_leave_copy_mode (def send.py:1894, tmux send-keys -X
cancel call send.py:1908)`, and the sibling tmux call sites were re-read live
and are also stated as def/call pairs: `_capture_pane` def 1915 call 1931,
`_window_id_listed` def 2131 call 2138, `_send_keys` def 2852 call 2860,
`_list_windows` def 2112, `_window_listed` def 2127.

### 4 NOTE — `hypothesis:a00-b11f67e2-f2ed9b` wrong pointer

The body said `Deviation recorded in the experiment node:`. The deviation (the
`replace body N:M` workaround for the missing body verb) is recorded on this
hypothesis node's OWN THOUGHT. The pointer wording was corrected to
`Deviation recorded on THIS hypothesis node own THOUGHT`. No claim changed.

### 5 NOTE — broader historical counts (DH.25-era)

`experiment:send-surface-real-path-and-residues-a00-e2960dc3.md:53` carries
`4 passed in 0.74s`; `experiment:send-surface-ssh-or-not-a00-dd757e64.md:120`
carries `(4 tests: ...)`. Both are CORRECT records of the module as it stood in
DH.25/DH.21 (before later rounds added tests). They are **not load-bearing**:
no live node cites them as the current count, only their own hypothesis parents
and this goal's residue table reference the two experiments. Left untouched as
historical, per the brief. (The current count is carried by
`experiment:tmux-seam-residue-closed-a00-ac47d671` and
`experiment:module-wide-no-real-tmux-guard-a00-768e0fd0`, both reading SEVEN.)

## Evidence

Raw command tails:

```
$ python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q
.......                                                                  [100%]
7 passed in 3.49s

$ grep -c '^def test_' extensions/agi/tests/test_send_surface_ssh_or_not.py
7

$ grep -c '6 passed, 0 production lines' .agi/nodes/hypothesis/a00-ac47d671-4fc781.md
0
$ grep -n '7 passed' .agi/nodes/hypothesis/a00-ac47d671-4fc781.md
56:...; 7 passed (re-measured DH.51: pytest 7 passed, grep -c "^def test_" -> 7), 0 production lines.

$ grep -c 'Deviation recorded in the experiment node' .agi/nodes/hypothesis/a00-b11f67e2-f2ed9b.md
0
$ grep -c 'Deviation recorded on THIS hypothesis node' .agi/nodes/hypothesis/a00-b11f67e2-f2ed9b.md
1

$ git diff --numstat -- extensions/agi/bin extensions/agi/skills src
(empty)
```

Production lines: 0 (only `.agi/nodes/*.md` changed). Ceiling 40.

## Residue table (post-close)

| # | locus | old | new | state |
|---|-------|-----|-----|-------|
| 1 | hypothesis:a00-ac47d671-4fc781 | `6 passed` claim | measured `7 passed` / SEVEN | CLOSED |
| 2 | experiment:tmux-seam-residue-closed-a00-ac47d671 probes[0] | "only the THOUGHT" | names both loci | CLOSED |
| 3 | hypothesis:a00-768e0fd0-6e3cb8 | `1884/1908` | def@1894 call@1908 (+live siblings) | CLOSED |
| 4 | hypothesis:a00-b11f67e2-f2ed9b | "in the experiment node" | "on THIS hypothesis node own THOUGHT" | CLOSED |
| 5 | experiment:e2960dc3 / experiment:dd757e64 | DH.25-era `4` | left historical, declared in this node | CLOSED (historical) |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-64ee01a6, DH.51 corrective round on goal:g7.31.4.2). WHAT THE INSTRUCTION SAID: close the five MUR mur-g7-31-4-2-dh-43-5ef0dc14b-3 residues; the PRIMARY is hypothesis:a00-ac47d671-4fc781 Agent Notes still reading 6 passed while the module measures SEVEN. WHAT THE MACHINE ACTUALLY DOES: I re-ran the live measurement myself (python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q -> 7 passed in 2.81s; grep -c ^def test_ -> 7), read the four changed node files byte-for-byte, and diffed the working tree -- exactly 4 target nodes modified, 9 insertions and 9 deletions, zero production bytes. I then ran one negative probe per residue and appended all thirteen probes (the six the kid wrote plus my seven) to this node list; every one held. THE NEAR MISS: the kid could have satisfied rewrite-to-7 by swapping the digit without re-measuring, and could have satisfied remove-the-stale-string by deleting the historical mention outright; the committed bytes do neither -- they re-measure and they label the surviving mention DH.31-era historical, so the live claim and the historical record do not disagree. Residue 5 I accepted as left-historical because the DH.25 counts (4 passed) are correct for their own round and no live node cites them as the current count. No demotion: hypothesis:a00-e1e6807b-4c2526 proved holds. DEVIATION: the standing guidance that a kid authored THOUGHT is the kid to land does not apply here -- it forbids a director landing a kid uncommitted authored bytes, not a parent recording the review the parent contract requires, and this kid already committed its own node (479386d26).
<!-- THOUGHT:END -->
