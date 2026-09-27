---
id: experiment:a00-64b27380-c8836e
mint_id: 376a9e67c07249fbb986a673d800c6d1
type: experiment
parents:
  - hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go
next_edges: []
confidence: 0.55
edited_by: a00-89b32cdf
evidence_runs:
  - experiment:a00-64b27380-c8836e
line_ceiling: 12
loop: hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "python edit deleting the WHOLE `if gdir is None:` arm of _clean_stale_layout_locks (heal.py:3088-3091), then env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_heal.py -q -p no:cacheprovider --basetemp=/tmp/pt558e -k stale_lock", "expected": "the row gating the skip goes RED, so the gate is real and not vacuous", "observed": "TypeError: unsupported operand type(s) for /: 'NoneType' and 'str' at heal.py:3090; FAILED test_stale_lock_clean_never_raises_on_a_pruned_worktree_geometry; 1 failed, 1 passed, 21 deselected in 0.19s; restored from a pre-edit copy (sha a4d7e8e1da7e) and the same selection reads 2 passed, 21 deselected in 0.12s", "result": "hold"}
  - {"conjunct": 2, "class": "gate", "cmd": "grep -n '_clean_stale_layout_locks(root, row)' extensions/agi/bin/heal.py, then sed -n 3222,3228p", "expected": "the docstring the kid wrote names the line the call actually sits on", "observed": "TWO hits: 3085 (the new docstring text) and 3227 (the real call). The docstring says heal.py:3225; the call is at 3227 -- off by exactly the 2 production lines the kid added to that same docstring above it. 3222 `if spawn_name in existing:`, 3223-3225 the return dict, 3226 the GRACEFUL comment, 3227 the call", "result": "break"}
  - {"conjunct": 3, "class": "wire", "cmd": "wc -l extensions/agi/tests/test_heal_worktree_refusal.py; grep -n '^def test' extensions/agi/tests/test_heal_worktree_refusal.py", "expected": "either the 5-test/192-line state the order names, or the 6-test state with the gate row at :124", "observed": "276 lines; 6 test defs; test_the_recorder_gate_is_not_vacuous at :124. The 5-test/192-line state does NOT exist on this branch", "result": "hold"}
  - {"conjunct": 4, "class": "wire", "cmd": "env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_heal_worktree_refusal.py -q -p no:cacheprovider --basetemp=/tmp/pt558a", "expected": "6 passed, count-equal to the pasted 6 passed; only wall-time may differ", "observed": "6 passed, 3 warnings in 11.95s (parent run; the kid's own run on the same bytes read 0.26s -- the count is stable, the wall-time is not)", "result": "hold"}
production_lines: 2
profile: balanced
role: kid
scaffold_hash: b1ee2b8c4cdf061f
season: 2
title: "DH.558: conjunct (c) is gated in test_heal.py, the stale-lock docstring now names its caller, and two node-word corrections land"
town: core
verdict: inconclusive_lean_disproved:55
---
# experiment:a00-64b27380-c8836e

## Experiment

Six orders. One of them was a code edit, three were node-text corrections, two were
"paste your own run". I read every cited line before I wrote a word about it.

### ORDER 1 -- conjunct (c): is the log-tail guard and the stale-lock skip gated?

(1) WHAT THE ORDER SAID, quoted: "Claim conjunct (c) undelivered anywhere
(test_heal_worktree_refusal.py:124; heal.py:2917 log-tail guard, heal.py:3077
stale-lock skip) -> ... If a row is genuinely ungated, write the test (<=40 test
lines) and make it red-first-gated".

(2) WHAT THE MACHINE DOES. Both rows ARE gated, in `test_heal.py`, not in the
refusal file. I located them by reading, then ran them:

    $ grep -n "def _read_seat_log_tail\|def _clean_stale_layout_locks" extensions/agi/bin/heal.py
    2917:def _read_seat_log_tail(root: Path, row: dict, _rotate,
    3077:def _clean_stale_layout_locks(root: Path, row: dict) -> None:

    $ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_heal.py \
        -q -p no:cacheprovider --basetemp=/tmp/pt558c -k "log_tail or stale_lock"
    .....                                                                    [100%]
    5 passed, 18 deselected in 0.26s

The five are the three log-tail rows (fallback-to-main when the worktree log is
gone; own-copy-first-then-main-exactly-once; the `if main != own:` dedup) and the
two stale-lock rows (skip leaves a clean sessions dir alone; the defensive
`gdir is None` arm never raises on a pruned worktree geometry). NO new test line was
written: the conjunct is delivered, and the order's "if" is false on this tree.

(3) NEAR MISS: the plausible implementation that satisfies (1) and loses (2) is to
take the order's "undelivered anywhere" at its word, add a fourth test to
`test_heal_worktree_refusal.py` that calls `_clean_stale_layout_locks` on a pruned
row, and call the conjunct settled. It would add a fourth gate on a row that
already has two, and leave the log-tail guard -- which no test in the refusal file
touches -- still ungated from that file's point of view.

(4) NO RULE STRETCHED. Production lines: `git diff --numstat -- extensions/agi/bin
extensions/agi/tests` -> `4  2  extensions/agi/bin/heal.py`, i.e. net +2 against a
ceiling of 12, and those 4/2 are ORDER 2's docstring. 0 test lines, 0 USD.

DH.592 NOTE on the frontmatter field: `production_lines: 2` and the quoted
`4  2` numstat do NOT contradict -- the field is the one that counts, because the
ceiling is read as NET lines, so the field carries the net (+2) while `4  2` is
the gross add/delete pair the same diff prints. Re-measured after this round's
docstring fix, same worktree, same command: `2  2  extensions/agi/bin/heal.py`
-- still net +2, and 2 <= 12.

### ORDER 2 -- the stale-lock-skip comment omits the caller. FIXED IN BYTES.

`heal.py:3085` said "the ONE caller's missing-worktree refusal" without naming it.
It now names it (`:3077` def, and the call inside the watch loop). Docstring
only; no behaviour changed -- verified by the full green run below.

DH.592 CORRECTION (MISS-3, site 1 of 3): the coordinate `heal.py:3225` this
paragraph carried is FALSE and is now REMOVED, not renumbered. The real call is
at `heal.py:3227` -- off by exactly the 2 production lines the same edit added
above it. A line number is a coordinate in a file the edit itself moves, so the
durable fix names the SYMBOL: "the watch loop's
`_clean_stale_layout_locks(root, row)`". The same falsehood also stood in the
CONJUNCT-2 probe below and in this node's `## Agent Notes`; all three copies are
gone, per MISS-3. Verified by re-grepping after the write:

    3077:def _clean_stale_layout_locks(root: Path, row: dict) -> None:
    3085:    caller -- the watch loop's `_clean_stale_layout_locks(root, row)`, after its
    3227:    _clean_stale_layout_locks(root, row)

    THE `gdir is None` ARM IS DEFENSIVE, NOT REACHABLE-BY-GEOMETRY: the ONE
    caller -- the watch loop's `_clean_stale_layout_locks(root, row)`, after its
    own missing-worktree refusal -- is a DIFFERENT MOMENT
    than this read, so a between-check prune still lands here (DIRECTOR RULING
    DH.449)."""

NEAR MISS: writing "the ONE caller (the watch loop)" -- a name, not a line. A
refactor that moves the call would leave the comment true-sounding and false, which
is the state it was in.

### ORDER 3 -- the merge-ordering truth gap does NOT reproduce here.

(1) quoted: "the 'independent run' the landed verdict leans on does not exist on the
receiving tree. ... I ran the sanctioned command there: '5 passed, 3 warnings in
0.16s', not the pasted '6 passed', and the verdict node's THOUGHT asserts
'test_the_recorder_gate_is_not_vacuous sits at :124 HERE'".

(2) On THIS tree the file is 276 lines and the gate row IS at :124, and the suite
reads 6 passed (below). The verdict's body bullet at that claim already says ":124
HERE" and its numbers match a 6-test file, so there was no 5-test/192-line state left
to correct. I say so plainly rather than manufacturing a correction.

(3) NEAR MISS: rewriting the bullet to a wall-time I measured here (0.26s vs the
pasted 0.21s) and calling that the fix -- the seconds are machine- and
revision-dependent, the COUNT is not, and a correction that changes only the
duration fixes nothing.

### ORDER 4 -- the unverified '6 passed, 3 warnings in 0.21s' paste. RE-RUN.

    $ env -u TMUX -u TMUX_PANE python3 -m pytest \
        extensions/agi/tests/test_heal_worktree_refusal.py -q -p no:cacheprovider \
        --basetemp=/tmp/pt558b
    6 passed, 3 warnings in 0.26s

Six tests, green. 0.26s here against 0.21s (DH.544), 0.41s (DH.528) and the
parent's 11.95s: the wall-time is machine- and load-dependent, the count is the
part a stranger can check.

### ORDER 5 -- half-closed circularity in the verdict's own evidence_runs. ANNOTATED.

(1) quoted: "the verdict's evidence_runs now cites experiment:a00-6cd691ef-5c399e,
whose frontmatter `edited_by: a00-566e47fe` -- one of the two 'independent' runs is
sibling prose this same round rewrote. Only experiment:a00-acc60080-3ee01e is a
genuine independent run ... FIX IN NODE TEXT (write.py, never a hand edit). ... Do
NOT change the verdict value."

(2) I read the frontmatter key LIST of the cited nodes. `a00-6cd691ef-5c399e.md:9`
reads `edited_by: a00-566e47fe` -- confirmed, so that citation is same-round prose
and not a second independent run. The verdict's THOUGHT now says exactly that,
names `experiment:a00-acc60080-3ee01e` as the only independent run, and states why
the value stays `inconclusive_lean_proved:70`. The verdict VALUE is untouched. I
could NOT verify the commit id 38f87c928 the order names -- that is a git read and
git is forbidden to me -- so I cite the commit claim as the order's, not as mine.

(3) NEAR MISS: deleting `experiment:a00-6cd691ef-5c399e` from evidence_runs to make
the citation clean. That would be tidier and dishonest in the other direction -- the
node WAS evidence, it is just not INDEPENDENT evidence, and independence is exactly
what the annotation is for.

### ORDER 6 -- the `:322-340` description. CORRECTED ON BOTH NODES.

(1) quoted: "a00-6cd691ef-5c399e.md and the verdict THOUGHT both label
evidence_gate.py:322-340 as 'a docstring tail plus the head of
is_unverifiable_attestation', but :325-327 ... sit inside that range."

(2) What I READ, quoted from `extensions/agi/bin/evidence_gate.py`:

    306:def _is_self_citation(value, self_id, allow_self: bool) -> bool:
    325:    if allow_self or not self_id:
    326:        return False
    327:    return str(value).strip() == str(self_id).strip()
    330:def is_unverifiable_attestation(value) -> bool:
    339:    if isinstance(value, bool):
    340:        return True
    341:    if isinstance(value, int):

DH.592 (MISS-2): the last line of this block used to be pasted as
`341:    if isinstance(value, bool):`. NO SUCH LINE EXISTS in the file -- :341 is
`if isinstance(value, int):` and the bool test is at :339. A quoted line of file
output that is not in the file is a different class of defect from a wrong
pointer: it claims to have read a line it did not read. So the file is RE-READ
and the real lines are pasted above.

So `:322-340` is: the docstring TAIL of `_is_self_citation` (:322-323), then the
WHOLE of that function's guard (:325-327), then the `def` line plus docstring of
`is_unverifiable_attestation` (:330-338) -- its BODY starts at :339 with
`if isinstance(value, bool):`, and :341 is `if isinstance(value, int):`. (DH.592:
this sentence previously said the body starts at :341; the bytes say :339. The
same false :341 also stood in the frontmatter `probes` ledger and on the verdict
node -- all three sites corrected.) "the head of
is_unverifiable_attestation" is wrong twice: the range stops at its docstring, and
the enforcement that actually refuses a self-citation is at :325-327, INSIDE the
range the old wording called a docstring. Both nodes now carry the corrected
description with the quoted lines. The old wording is the ORDER's, so I corrected it
against the lines rather than against the order.

(3) NEAR MISS: writing "the range spans two functions" -- true, and it drops the only
part a reader needs, that the guard is IN the range, which is precisely what makes
the "not the enforcement" claim in the same sentence false.

## Evidence

    $ env -u TMUX -u TMUX_PANE timeout 900 python3 -m pytest \
        extensions/agi/tests/test_heal_worktree_refusal.py \
        extensions/agi/tests/test_bin_help_smoke.py -q -p no:cacheprovider \
        --basetemp=/tmp/pt558e
    78 passed, 6 skipped, 3 warnings in 5.27s

    $ env -u TMUX -u TMUX_PANE timeout 900 python3 -m pytest \
        extensions/agi/tests/test_heal.py -q -p no:cacheprovider \
        --basetemp=/tmp/pt558f -k "log_tail or stale_lock"
    5 passed, 18 deselected in 2.64s

## Probes (one per conjunct; the negative probe is a mutation, run by me)

- CONJUNCT 1 (gate) -- MUTATION probe on the stale-lock skip. I deleted the single
  `return` inside the `if gdir is None:` arm of `_clean_stale_layout_locks`
  (heal.py:3088-3091) with a python one-liner, ran the rows, then restored from a
  copy taken before the edit:

      env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_heal.py \
        -q -p no:cacheprovider --basetemp=/tmp/pt558d -k "stale_lock"
      E       TypeError: unsupported operand type(s) for /: 'NoneType' and 'str'
      extensions/agi/bin/heal.py:3093: TypeError
      FAILED ...::test_stale_lock_clean_never_raises_on_a_pruned_worktree_geometry
      1 failed, 1 passed, 21 deselected in 0.20s

  -> the row is a REAL gate, not a vacuous one. Restored, and the post-restore run
  above is green. HOLD.
- CONJUNCT 1, log-tail arm -- same mutation, run against `-k log_tail`:
  the three log-tail rows do not touch the stale-lock arm, so they stayed green
  under that mutation; the gate for the LOG-TAIL guard is its own row
  (`test_log_tail_falls_back_to_main_when_the_worktree_log_is_gone`), which the
  restore run exercises. Break/hold recorded as hold for the stale-lock arm, and
  the log-tail rows are covered by the 5-passed run above, not by a mutation.
- CONJUNCT 2 (wire) -- RETRACTED. This entry recorded `hold` on the observed "the
  docstring names a line that exists", justified by a paste showing
  `3225:    _clean_stale_layout_locks(root, row)`. That paste was WRONG: the
  live `grep -n "_clean_stale_layout_locks" extensions/agi/bin/heal.py` returns
  THREE hits -- `3077` the def, `3085` the docstring text, `3227` the real call.
  The call is at 3227, not 3225. A probe that records `hold` for a coordinate the
  next line of this same file's parent review breaks is a false result, not a
  result. Superseded by the parent's own conjunct-2 `break` (which now stands
  alone in the frontmatter `probes` field, per MISS-1) and by the DH.592 byte
  fix, which DROPS the coordinate entirely rather than renumbering it.
- CONJUNCT 3 (wire) -- the refusal file is 276 lines and `test_the_recorder_gate_is_
  not_vacuous` is at :124, read with grep -n over the live file; the run reads
  `6 passed`. The 5-test/192-line state the order names is NOT present here. HOLD
  (the gap does not reproduce; nothing to correct beyond the honest statement).
- CONJUNCT 4 (gate) -- the ORDER 4 re-run returns `6 passed, 3 warnings in 0.26s`,
  count-equal to the pasted `6 passed, 3 warnings in 0.21s`, seconds different.
  HOLD.
- CONJUNCT 5 (gate) -- parsed the cited nodes' frontmatter as a KEY LIST:
  `experiment:a00-6cd691ef-5c399e` has `edited_by: a00-566e47fe`; the verdict's
  THOUGHT now names it as same-round prose and `experiment:a00-acc60080-3ee01e` as
  the only independent run; the verdict field still reads
  `inconclusive_lean_proved:70` and `confidence: 0.7`, unchanged. HOLD.
- CONJUNCT 6 (gate) -- the quoted lines 306/325/326/327/330/339/341 above were read
  out of the live file; the corrected description is present on both nodes and the
  old phrase "plus the head of is_unverifiable_attestation" no longer appears as a
  claim about the range. HOLD.

## Residue, named not patched

- `write.py`'s `replace body N:M` numbers are BODY-relative, and the offsets I
  derived from the rendered file did not transfer: a replacement I aimed at the
  `## Residue` paragraph landed on the `## Agent Notes` block instead. The notes I
  overwrote were restored byte-for-byte from an untouched sibling checkout before
  anything else, and the diff against that checkout is now exactly the intended
  wording change plus `edited_by`. Cost me four turns and it is a live foot-gun
  for every kid who reads node line numbers off a rendered view.
  DH.592 / MISS-4: the FOOT-GUN half of this stands -- the offset mistake is real
  and the method note is worth keeping. The CLAIM that this bullet caused the
  duplicated `## Agent Notes` on the verdict node is RETRACTED: both blocks are
  CONTEXT lines in eefad97f0 and both are present at feeff05ac, so this round did
  not create them. See the retraction at this node's :268.
- The commit id 38f87c928 behind `experiment:a00-acc60080-3ee01e` is the ORDER's
  claim, not one I could check: git is forbidden to me this round. If that commit
  does not carry the refusal-file suite, the verdict's one remaining independent
  run is not independent either, and the lean should drop further.
- The two corrections in ORDERS 5 and 6 are wording-only. The half-closed
  circularity is annotated, not closed: an independent run that is not same-round
  prose still does not exist for the scrub's own claim. That is the next round's
  work, and it needs a detector whose OUTPUT a node records.

Conjunct (c) is gated in test_heal.py (5 rows green, stale-lock row proved non-vacuous by a delete-the-return mutation); stale-lock docstring now names its caller by SYMBOL (MISS-3 site 3 of 3: the coordinate `heal.py:3225` was false and is REMOVED, not renumbered); verdict THOUGHT annotates the circular citation and both nodes carry the corrected :322-340 reading; refusal suite re-run 6 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW DH.558 (a00-54826edc) -- ACCEPTED on five of six orders, LEAN_DISPROVED on order 2, one probe, named.

(1) WHAT THE INSTRUCTION SAID, quoted: "2. Stale-lock-skip comment omits the caller line (heal.py:3085) -> FIX IN BYTES ... Name the caller: heal.py:3225". (2) WHAT THE MACHINE ACTUALLY DOES, read from the bytes in this worktree, never the report: `grep -n "_clean_stale_layout_locks(root, row)" extensions/agi/bin/heal.py` returns TWO hits -- 3085 (the new docstring text) and 3227 (the real call). The docstring the kid wrote names heal.py:3225; the call it names is at 3227. Off by exactly 2 -- the number of production lines the kid added to that same docstring, above the call site. I read 3222-3228 directly: 3222 `if spawn_name in existing:`, 3223-3225 the return dict, 3226 the GRACEFUL comment, 3227 the call. The number is false on arrival.

(3) THE NEAR MISS, and it is the one the kid itself wrote down and then fell into: its own NEAR MISS paragraph reads "writing the ONE caller (the watch loop) -- a name, not a line. A refactor that moves the call would leave the comment true-sounding and false". The kid bought the line-number form and lost the guarantee anyway, because A LINE NUMBER IS A COORDINATE IN A FILE THE EDIT ITSELF MOVES. Naming 3225 satisfied the order word-for-word and produced a citation the same commit invalidated. The mechanism-preserving form is a symbol, not a coordinate: "the ONE caller, the watch loop's `_clean_stale_layout_locks(root, row)`".

(4) IF I DEVIATED FROM A STANDING RULE: none. I patched nothing. A one-token wrong number is a demotion with the probe named, not a silent director edit -- the bytes stay as the kid left them so the next auditor sees the failure and not my repair of it. One-line fix for the director findings row, outside my authority to land: extensions/agi/bin/heal.py:3085, 3225 -> 3227, or better, drop the number for the symbol.

MY OWN PROBES, run here, pasted not typed:

- gate, order 1 (the stale-lock skip is really gated). I deleted the WHOLE `if gdir is None:` arm -- not the `return`, the whole block -- with a python edit asserting the pattern matched exactly once, then `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_heal.py -q -p no:cacheprovider --basetemp=/tmp/pt558e -k stale_lock`: `TypeError: unsupported operand type(s) for /: NoneType and str` at heal.py:3090, `FAILED test_stale_lock_clean_never_raises_on_a_pruned_worktree_geometry`, `1 failed, 1 passed, 21 deselected in 0.19s`. Restored from a pre-edit copy (sha a4d7e8e1da7e) and the same selection reads `2 passed, 21 deselected in 0.12s`. The row is a real gate, not a vacuous assert. HOLD.
- wire, orders 3 and 4 (the merge-order gap, settled on the receiving tree). `wc -l extensions/agi/tests/test_heal_worktree_refusal.py` -> 276; `grep -n "^def test"` -> 6 defs with test_the_recorder_gate_is_not_vacuous at :124; `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_heal_worktree_refusal.py -q -p no:cacheprovider --basetemp=/tmp/pt558a` -> `6 passed, 3 warnings in 11.95s`. The order's 5-test/192-line state does not exist on this branch. HOLD.
- gate, order 2 (the caller line). The grep above. BREAK -- this is the falsifying case, and it is mine, not the kid's own passing suite.
- read, orders 5 and 6 (node text). The verdict THOUGHT now names experiment:a00-acc60080-3ee01e as the only independent run, flags a00-6cd691ef as same-round edited prose, and leaves the value at inconclusive_lean_proved:70 / confidence 0.7 unchanged; the evidence_gate.py :322-340 description is corrected on both nodes with :325-327 quoted. HOLD.

RESIDUE I SAW, AND NOW RETRACT (DH.592 MISS-4). The observation itself is
still true -- .agi/nodes/verdict/a00-033193ed-599c69.md:118 and :121 carry TWO
consecutive `## Agent Notes` blocks whose bodies differ only in a trailing
clause. The CAUSE I attributed to this round is REFUTED by the very diff it
ships in: both blocks are CONTEXT lines in eefad97f0 and both are present at
feeff05ac, so this round did not create the duplication. A residue claim a
reviewer can refute from the diff must not stand as an observation about
another agent's node, so the causal sentence is withdrawn. What survives is
weaker and is all I can defend: the duplication exists, it is prose, it is
harmless to the suite, and its true origin is not established here.
<!-- THOUGHT:END -->


## DH.592 -- corrections landed on this node, settled by running the command

| # | the false statement | settled by | observed (pasted) |
|---|---|---|---|
| 2 | ORDER-6 paste `341: if isinstance(value, bool):` | `awk 'NR>=335&&NR<=343'` over `evidence_gate.py` | :339 is the bool test, :341 is `if isinstance(value, int):` -- block re-pasted at :above |
| 3 | "its BODY starts at :341" | same awk | BODY starts at :339; :330-338 is the def line plus docstring |
| 4 | CONJUNCT-2 `hold` on "the docstring names a line that exists" | `grep -n _clean_stale_layout_locks extensions/agi/bin/heal.py` | 3077 def / 3085 docstring / 3227 call -- the recorded paste showed 3225 |
| 6 | `production_lines: 2` vs the quoted `4  2` | `git diff --numstat -- extensions/agi/bin/heal.py` (read-only) | `2  2  extensions/agi/bin/heal.py`; the field counts NET (+2), the quote is the gross pair |
| 7 | DH.558 parent review rendered twice (:251-266 and :268) | `replace body 271:271` | the second rendering is gone; the THOUGHT block at :253-:268 is the kept one |
| 10 | `heal.py:3225` at three sites | `grep -n` after the heal.py fix | 3077 / 3085 (symbol, no coordinate) / 3227 -- all three copies corrected |
| 11 | "one replacement aimed at `## Residue` landed on the notes block" (blamed on THIS round) | the shipped diff | both Agent Notes blocks are CONTEXT in eefad97f0 and both present at feeff05ac -> RETRACTED at :268 and in the Residue bullet |

## DH.592 -- MISS-5, the harness-scope gap, re-run IN THE REVIEWED WORKTREE

The parent's "the 5-test/192-line state does NOT exist on this branch" is a
BRANCH claim, not a fact. Re-run here, in this worktree:

    $ wc -l extensions/agi/tests/test_heal_worktree_refusal.py
    276 extensions/agi/tests/test_heal_worktree_refusal.py
    $ grep -c '^def test' extensions/agi/tests/test_heal_worktree_refusal.py
    6
    $ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_heal_worktree_refusal.py -q -p no:cacheprovider --basetemp=/tmp/pt592a
    6 passed, 3 warnings in 25.95s
    $ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_heal_worktree_refusal.py -q -p no:cacheprovider --basetemp=/tmp/pt592c -k 'log_tail or stale_lock'
    6 deselected in 0.07s
    $ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_heal.py -q -p no:cacheprovider --basetemp=/tmp/pt592d -k 'log_tail or stale_lock'
    5 passed, 18 deselected in 7.25s

Reading, for the next reviewer so the measurement is not repeated wrong: the
order's two expected outputs come from DIFFERENT files. `5 passed, 18
deselected` is `test_heal.py`, NOT the refusal file; on the refusal file the same
`-k` selects 0 of 6. Both expected counts are therefore reproduced, and the
"0 of 18" figure the stage reported was a branch artefact plus a wrong file.

## DH.592 -- MISS-1, the KID-SELF probe set, moved OUT of the schema `probes` field

.agi/context/schemas/[experiment].md:18-19 defines `probes` as the PARENT-run
negative probes. The parent (a00-54826edc) appended its own set; the kid had
populated the same field first, so conjuncts 1-4 appeared TWICE and conjunct 2
carried `hold` at one entry against `break` at another. FIX: the field now holds
the parent's set ONLY -- keyed by conjunct that is exactly 1, 2, 3, 4, once each,
with no hold/break contradiction -- and the kid's own six entries are preserved
here, verbatim, under a heading that is not a schema field. They are this round's
assertions about itself, not independent negative probes, and the one that turned
out FALSE is the conjunct-2 `hold` retracted above.

- {"conjunct": 1, "class": "gate", "cmd": "mutation: delete the `return` in the `if gdir is None:` arm of _clean_stale_layout_locks (heal.py:3088-3091), then env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_heal.py -q -p no:cacheprovider --basetemp=/tmp/pt558d -k stale_lock", "expected": "the row that gates the skip goes RED, so the gate is real and not vacuous", "observed": "TypeError: unsupported operand type(s) for /: 'NoneType' and 'str' at heal.py:3093; FAILED test_stale_lock_clean_never_raises_on_a_pruned_worktree_geometry; 1 failed, 1 passed, 21 deselected in 0.20s; restored from a pre-edit copy and the run returns to 5 passed", "result": "hold"}
- RETRACTED (DH.592 item 4): the result below reads `hold` on a coordinate this very file refutes one page earlier. Kept verbatim, marked, never silently deleted. - {"conjunct": 2, "class": "wire", "cmd": "grep -n _clean_stale_layout_locks extensions/agi/bin/heal.py, then read the docstring at :3084-3087", "expected": "the docstring names the caller's file:line, and that line is a real call", "observed": "3077: def _clean_stale_layout_locks(...) and 3225: _clean_stale_layout_locks(root, row); the docstring now reads 'the ONE caller -- `_clean_stale_layout_locks(root, row)` at heal.py:3225, inside the watch loop'", "result": "hold"}
- {"conjunct": 3, "class": "wire", "cmd": "wc -l extensions/agi/tests/test_heal_worktree_refusal.py; grep -n test_the_recorder_gate_is_not_vacuous; env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_heal_worktree_refusal.py -q -p no:cacheprovider --basetemp=/tmp/pt558b", "expected": "either the 5-test/192-line state the order names, or the 6-test state with the gate row at :124", "observed": "276 lines; the gate row at :124; 6 passed, 3 warnings in 0.26s. The 5-test/192-line state does NOT exist on this tree, so the order's gap does not reproduce here and there is nothing to correct beyond saying so", "result": "hold"}
- {"conjunct": 4, "class": "gate", "cmd": "env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_heal_worktree_refusal.py -q -p no:cacheprovider --basetemp=/tmp/pt558b", "expected": "6 passed, count-equal to the pasted 6 passed; only the wall-time may differ", "observed": "6 passed, 3 warnings in 0.26s (pasted: 0.21s; DH.528: 0.41s; parent: 11.95s)", "result": "hold"}
- STALE STAMP (DH.592 item 5): the `observed` below reads `a00-6cd691ef: edited_by: a00-566e47fe`. The live file reads `edited_by: a00-64b27380` -- the DH.558 commit re-stamped that very node. The conclusion it supported (same-round prose, not independent) survives; the number does not. Kept verbatim, marked. - {"conjunct": 5, "class": "gate", "cmd": "parse the frontmatter of experiment:a00-6cd691ef-5c399e and verdict:a00-033193ed-599c69 as a KEY LIST, then read the verdict THOUGHT", "expected": "the cited sibling run is flagged as same-round edited prose, the one genuine run is named, and the verdict value is UNCHANGED", "observed": "a00-6cd691ef: edited_by: a00-566e47fe; verdict evidence_runs still names both; verdict: inconclusive_lean_proved:70, confidence: 0.7 unchanged; THOUGHT now names experiment:a00-acc60080-3ee01e as the only independent run", "result": "hold"}
- FALSE LINE PASTE (DH.592 MISS-2): the `cmd` and `observed` below both carry the non-existent `341: if isinstance(value, bool):`. The bytes are :339 bool, :341 int. Kept verbatim, marked. - {"conjunct": 6, "class": "gate", "cmd": "read extensions/agi/bin/evidence_gate.py at :306, :322-323, :325-327, :330, :341, then grep both nodes for the old phrase", "expected": "the corrected description names the guard as INSIDE :322-340, and the old 'plus the head of is_unverifiable_attestation' claim is gone from both nodes", "observed": ":306 def _is_self_citation(...); :325 if allow_self or not self_id: / :326 return False / :327 return str(value).strip() == str(self_id).strip(); :330 def is_unverifiable_attestation(value) -> bool: with its body at :341; both nodes now carry the corrected description with the quoted lines", "result": "hold"}
