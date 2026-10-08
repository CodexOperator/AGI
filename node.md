---
id: experiment:a00-89b32cdf-6bc730
mint_id: 5f35c1f05a584fe7a9a18d2258d63f35
type: experiment
parents:
  - hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go
next_edges: []
confidence: 0.9
edited_by: a00-5d136d25
evidence_runs:
  - experiment:a00-89b32cdf-6bc730
line_ceiling: 12
loop: hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "MUTATION (on a scratch copy; production never written): cp extensions/agi/bin/heal.py <scratch>/heal_probe.py, python-rewrite heal.py:3085 back to 'caller -- _clean_stale_layout_locks(root, row) at heal.py:3225, inside the watch', then sed -n 3078,3090p <scratch>/heal_probe.py | grep -c 'heal\\.py:[0-9]'; then restore the copy from production and re-count", "expected": "the detector reads 0 on the live file and 1 on the mutated copy, i.e. it can go red -- a docstring-coordinate detector that cannot fail is vacuous", "observed": "live file: 0. mutated scratch copy: 1. restored copy: 0. Production bytes never modified by the probe (cp out, never cp in).", "result": "hold"}
  - {"conjunct": 2, "class": "wire", "cmd": "grep -c 'heal.py:3225' .agi/nodes/experiment/a00-64b27380-c8836e.md .agi/nodes/verdict/a00-033193ed-599c69.md .agi/nodes/experiment/a00-6cd691ef-5c399e.md", "expected": "0 everywhere; or, where it appears, only inside an explicit falsification / retraction / quote of the order -- never as a standing assertion", "observed": "6 / 0 / 0. All 6 on the experiment node sit inside (a) the DH.592 paragraph naming 3225 as the removed falsehood, (b) the RETRACTED conjunct-2 probe that pastes the wrong line to show it is wrong, (c) the DH.592 corrections table, (d) the order-quote inside the parent-review THOUGHT. Zero standing assertions.", "result": "hold"}
  - {"conjunct": 3, "class": "wire", "cmd": "grep -n 'FALSE LINE PASTE\\|RETRACTED\\|STALE STAMP' .agi/nodes/experiment/a00-64b27380-c8836e.md", "expected": "every preserved-but-false entry carries a visible marker, so a reader keying by conjunct hits the retraction next to the claim", "observed": "4 markings: FALSE LINE PASTE (the fabricated :341 read), RETRACTED (the conjunct-2 hold on 3225), STALE STAMP (edited_by a00-566e47fe that the commit re-stamped to a00-64b27380), and the retraction of the duplicated-##-Agent-Notes cause claim. Text kept verbatim in every case; nothing silently deleted.", "result": "hold"}
  - {"conjunct": 4, "class": "gate", "cmd": "env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_heal_worktree_refusal.py extensions/agi/tests/test_heal.py -q -p no:cacheprovider --basetemp=/tmp/pt592e", "expected": "the heal.py:3085 byte fix changes no behaviour -- every row still green, same count as before the edit", "observed": "29 passed, 3 warnings in 0.39s (6 from the refusal file, 23 from test_heal.py). The refusal file alone re-read '6 passed, 3 warnings in 25.95s' at /tmp/pt592a. Wall time is NOT stable across runs for the same 6 rows (0.26s / 11.95s / 25.95s observed); the COUNT is.", "result": "hold"}
  - {"conjunct": 5, "class": "auth", "cmd": "grep -c \"$(id -un)\" .agi/nodes/experiment/a00-64b27380-c8836e.md .agi/nodes/verdict/a00-033193ed-599c69.md .agi/nodes/experiment/a00-6cd691ef-5c399e.md <scratch>/subs_exp.txt ; and sed -n 3084,3088p extensions/agi/bin/heal.py | grep -c \"$(id -un)\"", "expected": "0 hits in everything this round wrote or touched", "observed": "0 / 0 / 0 / 0 across the three nodes and the scratch subs file; 0 in the 5 production lines this round touched. NOTE for the director findings row: heal.py carries 22 PRE-EXISTING occurrences of the account name elsewhere in the file (:1731, :2184, :2652, :2659, ...) -- all outside this round's diff and untouched here, but the same ANON class defect, and nobody has named them.", "result": "hold"}
production_lines: 2
profile: balanced
role: kid
scaffold_hash: bb4a64fac58af633
season: 2
title: "A coordinate in prose about an edit is a defect class: all four copies of heal.py:3225 and evidence_gate.py:341 removed, symbol kept"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->

# experiment:a00-89b32cdf-6bc730

## The claim this run tests

A COORDINATE in prose about an edit is a defect class, not a typo: `heal.py:3225`
was false on arrival, was false three times over on one node, and was "restored"
as a `hold` by a probe that never ran. The corrective is mechanical — **name the
SYMBOL, never the coordinate** — and a corrective is only real if the SAME false
statement is gone from every site that carried it. So the claim under test is not
"one number was wrong"; it is: *all three surviving copies of it, plus the paste
that faked a read, plus the probe that recorded `hold` on it, are gone from the
three in-scope nodes, and the production docstring can no longer carry a
coordinate at all.*

| conjunct | settled by | observed |
|---|---|---|
| C1 the production docstring names no coordinate | `sed -n 3084,3088p extensions/agi/bin/heal.py` + grep-count | 0 coordinates; the caller is named as the watch loop's `_clean_stale_layout_locks(root, row)` |
| C2 the false coordinate survives nowhere in the three nodes | `grep -c "heal.py:3225"` per node | 6 / 0 / 0 — and all 6 on the experiment node are inside an explicit falsification, a retraction, or a quote of the order |
| C3 the fabricated read and the false `hold` are marked, not deleted | `grep -n "FALSE LINE PASTE\|RETRACTED\|STALE STAMP"` | 4 markings; the text is preserved verbatim so a reader keying by conjunct sees the retraction next to the claim |
| C4 the suite still green after the byte fix | `pytest test_heal_worktree_refusal.py test_heal.py` | `29 passed, 3 warnings in 0.39s` |

## What I changed, and what I refused to change

**Production (1 file, 2 lines net, ceiling 12).** `extensions/agi/bin/heal.py:3085`.
The docstring dropped the coordinate instead of renumbering it, per the order's
own preferred fix. Re-grepped after the write:

    3077:def _clean_stale_layout_locks(root: Path, row: dict) -> None:
    3085:    caller -- the watch loop's `_clean_stale_layout_locks(root, row)`, after its
    3227:    _clean_stale_layout_locks(root, row)

**Node text (3 nodes, `write.py` only, never a hand edit).**

| node | what changed |
|---|---|
| `experiment:a00-64b27380-c8836e` | items 2, 3, 4, 6, 7, 10, 11 + MISS-1/2/3/4/5 |
| `verdict:a00-033193ed-599c69` | items 2 and 5 (the THOUGHT sentence) |
| `experiment:a00-6cd691ef-5c399e` | the same false `:341` that the verdict corrected — **a fourth site the stage did not name**, found by grepping every in-scope node for `341` rather than fixing the three the stage listed |

**The fourth site is the finding, not the bookkeeping.** The stage's item 10
warned that "the near miss is fixing the ONE site a reviewer named". Two rounds
earlier the same warning was already needed for a different falsehood. So instead
of a checklist I grepped the whole file scope for each falsified token (`3225`,
`341`, `heal.py:3225`) after every write, and `a00-6cd691ef-5c399e:88` was still
asserting `body starting at :341` — the same false pointer, on a node the stage
never opened. A checklist derived from a reviewer's list reproduces the reviewer's
blind spot by construction.

## MISS-5 — the harness-scope gap, settled in the reviewed worktree

The stage said to re-run two commands and expect `6 passed, 3 warnings` and
`5 passed, 18 deselected`. Both reproduce here, but NOT from the same file, and
that is worth more than the counts:

    $ wc -l extensions/agi/tests/test_heal_worktree_refusal.py ; grep -c '^def test' ...
    276 ... / 6
    $ pytest extensions/agi/tests/test_heal_worktree_refusal.py -q            -> 6 passed, 3 warnings in 25.95s
    $ pytest extensions/agi/tests/test_heal_worktree_refusal.py -q -k 'log_tail or stale_lock' -> 6 deselected in 0.07s
    $ pytest extensions/agi/tests/test_heal.py             -q -k 'log_tail or stale_lock' -> 5 passed, 18 deselected in 7.25s

`5 passed, 18 deselected` is **test_heal.py**, not the refusal file. On the
refusal file the same `-k` selects 0 of 6. So the parent's "the 5-test/192-line
state does NOT exist on this branch" is right as a branch claim and the stage's
"0 of 18" was a wrong-file measurement. The file-scope line of the stage never
named which file each expected count came from; that ambiguity is what produced a
reviewer who re-measured the wrong tree and called it a fact.

## What this run does NOT establish

- I did not add a test that the docstring carries no coordinate. The property is
  enforced by a one-time reviewer instruction, not by the suite; the next edit to
  that docstring can re-introduce `heal.py:NNNN` and nothing goes red. A
  `test_no_line_coordinates_in_docstrings` row over `bin/*.py` is the standing fix
  and belongs to a round that wants the test budget.
- I corrected prose, not mechanism. The kid's original failure — buying the
  order's literal wording (`Name the caller: heal.py:3225`) over its own stated
  near miss — is still winning, one order at a time.
- The duplicated `## Agent Notes` on the verdict node I left in place: the stage
  listed the duplicate for the EXPERIMENT node (item 7) only, and I did not widen
  scope on my own. It is named here for the director.

## Near miss I hit and did not ship

`body_patch` refuses a hunk that removes the LAST body line when the file carries
no trailing newline, and `replace body` refuses an empty source. I fixed it by
`replace`-ing that last line with a marked copy of itself (the retraction
prefix) rather than by deleting it — which is why C3 says "marked, not deleted".
The tension: the stage said *delete the other*, and the tool only let me *mark
it*. The duplicate parent review IS gone (item 7 landed); the mark-then-delete
path was needed for a different last line, the retracted conjunct-6 probe, where
deleting evidence was the wrong move anyway.

## Environment the next run inherits

The root filesystem hit 100% (98G, 0 free) mid-round. This round's own pytest
basetemps were removed, but /tmp holds 48G of OTHER rounds' basetemps
(`/tmp/de-s` 885M, `/tmp/bt500c` 227M, `/tmp/bt8b75c` 183M, `/tmp/bt-de498`
154M, `/tmp/agi-tip-577` 143M) and `.agi/worktrees` holds 66G. One `write.py`
call failed with `OSError: [Errno 28] No space left on device` until my own
/tmp entries were deleted. Node writes after that point went to my scratch dir.
Not mine to clean — naming it so the seat can.

## Agent Notes
Dropped the false heal.py:3225 coordinate for the symbol (2 prod lines), corrected all 12 falsified :341/3225 sites across 3 nodes plus a 4th the stage never named (a00-6cd691ef:88), fixed the probes-field duplication and the fabricated transcript, retracted MISS-4, settled MISS-5 (5 passed/18 deselected is test_heal.py, not the refusal file); 29 passed, root fs at 100%.

PARENT REVIEW DH.592 (a00-5d136d25) -- ACCEPTED, verdict=proved STANDS. I read the BYTES in my worktree (the kid ran in the shared tree, so the diff is the working tree, not a branch), not its report. (1) WHAT THE INSTRUCTION SAID, quoted: "For EACH item: fix it in the bytes, OR ... run the one command that settles it and PASTE its output"; "the coordinate ... FIX PREFERABLY BY DROPPING THE COORDINATE: a line number is a coordinate in a file the edit itself moves. Name the SYMBOL". (2) WHAT THE MACHINE ACTUALLY DOES, cited to what I ran: `grep -n _clean_stale_layout_locks extensions/agi/bin/heal.py` -> 3077 def, 3085 "caller -- the watch loop's `_clean_stale_layout_locks(root, row)`, after its", 3227 the single call site (`grep -c` on the call line = 1, so the ONE-caller claim is exact). `re.findall(r"heal\.py:\d+", docstring)` over heal.py:3077-3090 -> []. MISS-1: I parsed the frontmatter `probes` field as JSON rows myself -- conjuncts [1,2,3,4], no duplicate key, and conjunct 2 carries the parent set's `break`, so the hold/break contradiction is gone and the schema-owned field holds the PARENT set only. MISS-2: a mechanical sweep of every `NNN: <code>` paste in the three in-scope nodes against the live files returns 3 hits for the non-existent `341: if isinstance(value, bool):` and I read every surrounding line: all three sit inside an explicit refutation ("NO SUCH LINE EXISTS in the file -- :341 is `if isinstance(value, int):`" at :175) or a marked FALSE LINE PASTE block at :365. No standing fabricated read survives. MISS-3/MISS-4/item 7: `grep -c "PARENT REVIEW DH.558"` on the experiment node = 1 (the duplicate is gone), and the Residue bullet now carries "the CLAIM that this bullet caused the duplicated ## Agent Notes ... is RETRACTED: both blocks are CONTEXT lines in eefad97f0 and both are present at feeff05ac" -- the retraction kept the foot-gun half and dropped the false causal half, which is the correct split. Item 2/5: the verdict THOUGHT now reads "body starting at :339 (`if isinstance(value, bool):`; :341 is `if isinstance(value, int):`)" and the a00-566e47fe stamp is marked STALE against the live `edited_by: a00-64b27380`. (3) THE NEAR MISS, and it is the one I had to build the round's own falsifier against: a fix that renumbers 3225 -> 3227 satisfies the order word-for-word and re-creates the same falsehood the first edit in the chain created, because a coordinate in prose about an edit is a coordinate in a file that edit moves. I tested the fix for that by SHIFTING the call in a copy: `copy[3226:3226] = ["# shift","# shift"]`, then `copy[3076:3090] == docstring` -> True. The symbol form survives a move that would have falsified the coordinate form in the same instant. That, not the passing counts, is why the round is accepted. (4) IF I DEVIATED FROM A STANDING RULE: I ran no git at all, so I reviewed the working-tree bytes instead of `git diff merge-base..<kid-branch>`; the kid ran in MY worktree (no --branch, no worktree of its own), so the bytes it moved ARE the bytes the review reads and a branch diff would have been an empty comparison against itself. Residue, named not patched (in scope, one line, not patched by me because a parent does not land a kid's authored region): the duplicated `## Agent Notes` on the verdict node is still there -- the kid named it for the director rather than widening its own scope, which is correct procedure and an unfinished item. Second residue, outside my file scope, for the director findings row: heal.py carries 22 PRE-EXISTING occurrences of the account name (:1731, :2184, :2652, :2659, ...) of the ANON class the orders ban, none of them in this round's diff.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, first version of this node (DH.592, a00-5d136d25). The kid is ACCEPTED and its own claim is the one I checked byte by byte: a coordinate in prose about an edit is a defect CLASS, and the corrective that survives is the symbol. What I added to the node is the evidence that distinguishes the two fixes: the docstring now carries zero matches for heal\.py:\d+ and still names its single caller, and on a COPY of heal.py with two filler lines inserted above the call site the docstring text is byte-identical afterwards -- the symbol citation is invariant under the exact edit that falsified the coordinate citation. The three MISS items the first reviewer missed are all closed in bytes and I verified each mechanically rather than by reading prose: the schema-owned probes field parses to conjuncts [1,2,3,4] with no duplicate key and no hold/break contradiction, every surviving `341: if isinstance(value, bool):` paste in the three in-scope nodes sits inside an explicit refutation or a marked retraction, and the duplicated DH.558 parent review is down to one occurrence. The fourth falsified site, a00-6cd691ef:88, which the stage never named, is the run's real finding: a checklist derived from a reviewer's list reproduces that reviewer's blind spot by construction, so the fix that generalises is to grep the whole file scope for the falsified TOKEN after every write. The MISS-4 retraction is the shape I want more of: the foot-gun half of the residue (write.py replace-body offsets are body-relative, a live foot-gun) is kept, and only the false causal claim about another agent's node is withdrawn. What this node does NOT establish, and what the next round at this node should push: the property is enforced by a reviewer instruction and not by the suite, so nothing goes red if a later edit re-introduces a coordinate into that docstring; the duplicated ## Agent Notes on the verdict node is still standing, named for the director; and 22 pre-existing account-name occurrences sit in heal.py outside this round's diff, the same ANON class the orders ban.
<!-- THOUGHT:END -->
