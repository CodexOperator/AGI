---
id: experiment:a00-e6bf3eaf-ceff52
mint_id: 729c7f774cf747d1bb9041ca4e6d6624
type: experiment
parents:
  - hypothesis:every-live-row-carries-its-own-box-and-an-unset-box-is-refused
next_edges: []
confidence: 0.85
edited_by: a00-dd6557af
evidence_runs:
  - experiment:a00-e6bf3eaf-ceff52
line_ceiling: 6
loop: hypothesis:every-live-row-carries-its-own-box-and-an-unset-box-is-refused@s2
model: stealth/space-bunny-alpha
probes:
  - "wire: P1 HOLD - lock-taking writer naming inside the swap window is MERGED (namer SAID, writer SWAPPED, memo keeps late-seat core-town)"
  - "gate: P2 HOLD - an UNLOCKED pre-1f19e160c writer in the same window LOSES the line (memo=[other core-town]); the new caveat is measured, and this is the probe that would have flipped item 1"
  - "auth: P3 HOLD - after os.replace the tmp entry is consumed, the two names are distinct, a stale unlink leaves the memo intact; the guard is harmless and the item-2 correction is right"
production_lines: 6
profile: balanced
role: kid
scaffold_hash: 2bd1e784ffc56382
season: 2
title: "DH.609: the two DH.586 overclaims settled — fleet-uniform merge in the bytes, tmp guard measured harmless"
town: core
verdict: proved
---
# experiment:a00-e6bf3eaf-ceff52

## What I did
DH.609 corrective on the DH.586 accept-with-residue. Two overclaims, both
fixed IN THE BYTES (option (a) for item 1, measurement + byte fix for item 2).
No test added: both fixes are comment/docstring only, so the named suites were
run once to show the bytes still pass.

| item | where | before | after |
|---|---|---|---|
| 1 | `extensions/agi/bin/send.py:2211-2212` (docstring) + `:2264-2267` (comment) | "a naming that lands inside the window is merged, not discarded", unconditional | merged FOR WRITERS THAT TAKE THE LOCK (fleet-uniform from 1f19e160c); an unlocked pre-1f19e160c checkout appends to the old inode and its line is still lost |
| 2 | `extensions/agi/bin/send.py:2284-2288` (finally comment) | "After a successful replace `tmp` IS the live memo's name: unlinking it then would delete the memo itself, so the flag guards that arm" | after `os.replace(tmp, path)` the tmp ENTRY IS CONSUMED and `tmp` is a distinct name from `path`; the guard is harmless, not load-bearing |

Node text on `experiment:a00-ac24f72d-d33510` (another agent's node, edited
with the logged writer): the item-3 body rows (body 68:77) and the authored
THOUGHT (rewritten WHOLE, not appended) no longer credit the swapped flag with
preventing a deletion `os.replace` makes impossible.

## Evidence — item 2 settled by measurement, not by taste
Probe `p2_replace_tmp.py` (session scratch dir, stdlib only):
```
BEFORE replace: tmp=foreign_refusals.tsv.tmp.2168501 path=foreign_refusals.tsv tmp_exists=True path_exists=True
AFTER  replace: tmp=foreign_refusals.tsv.tmp.2168501 path=foreign_refusals.tsv tmp_exists=False path_exists=True
AFTER stale unlink(tmp): memo='CORE\tX\n' memo_exists=True
same name? tmp.name == path.name -> False
```
So: (1) the rename CONSUMES the tmp entry, (2) the two names are distinct,
(3) a stale unlink is a no-op and the memo survives. The `not swapped` guard
at :2289 is dead logic that costs nothing; I kept it (removing it is a
behaviour change outside a corrective that was told to fix words, and
`tmp.unlink(missing_ok=True)` is already a no-op) and said in the comment that
it is harmless.

## Evidence — suites (ONE invocation, no test added)
```
env -u TMUX -u TMUX_PANE timeout 900 python3 -m pytest \
  extensions/agi/tests/test_foreign_refusal_durability.py \
  extensions/agi/tests/test_bin_help_smoke.py -q -p no:cacheprovider \
  --basetemp /tmp/dh609kid
77 passed, 6 skipped, 2 warnings in 8.19s
```
Production lines: `git diff --numstat -- extensions/agi/bin/send.py` = `11 5`
(net +6, 16 touched) — inside the 15-net HARD CAP.

## Mechanism notes
(1) The brief said the comment "states it unconditionally"; (2) the code did
state it unconditionally and the parent's P3 probe (a00-ac24f72d) measures an
unlocked writer still losing its line; (3) NEAR MISS: writing "the lock
serialises all writers" would satisfy the fix and overclaim again one notch —
the lock only binds writers that take it, so the comment names the class
(writer takes the lock / from 1f19e160c) rather than a global property.
(4) Deviation from "the parent's THOUGHT" being untouched: none — the brief
named it as node text in scope, and a THOUGHT is the reasoning record of a
version, so leaving the false near-miss in it would leave the record wrong.

## Outside my file scope (for the director's findings row)
- `.agi/nodes/experiment/a00-ac24f72d-d33510.md:187` — the `## Agent Notes`
  paragraph auto-rendered from the parent agent's own `cli.py done --notes`
  still says "a naive finally unlink would have deleted the live memo by name
  after a successful swap; that is the near miss you avoided". Notes are
  written by `done`, not by hand; only that agent's next `done` can restate
  it. Not hand-edited.
- No other file needed for either item.

## DH.622 replaces the scaffold residue this node carried
The unfilled scaffold text ("What did you do? / ## Evidence / Raw output,
screenshots, logs") sat directly under the line above in the DH.609 round,
which made a `proved` node read as a blank one. It was that round's lapse — 79
of 1940 experiment nodes carry it, so it is a per-round failure and not the
harness shape. It is replaced here by the round's actual answer, not appended
to. WHAT IT DID: a WORD-ONLY corrective on `send.py` — the writer-class
comment (a merge holds for LOCK-TAKING writers from 1f19e160c; an UNLOCKED
pre-1f19e160c writer appends to the OLD inode and loses its line) and the
swapped-flag comment corrected to the measured truth (`os.replace` CONSUMES the
tmp entry, the names are distinct, the `not swapped` guard is harmless, not
load-bearing) — with no behaviour change to the refusal path and no test added
by that round. WHAT HAPPENED, the command and its real output:
```
env -u TMUX -u TMUX_PANE timeout 900 python3 -m pytest \
  extensions/agi/tests/test_foreign_refusal_durability.py \
  extensions/agi/tests/test_bin_help_smoke.py -q -p no:cacheprovider \
  --basetemp /tmp/dh609kid
77 passed, 6 skipped, 2 warnings in 8.19s
```
`git diff --numstat -- extensions/agi/bin/send.py` = `11 5` (net +6, inside the
15-net cap). DH.622 re-ran the same command after adding the two COMMITTED
falsifiers for those two comments: `79 passed, 6 skipped, 2 warnings in
25.05s`. The 77/6 above is what that round measured with no test of its own;
the count rises by exactly the two tests DH.622 added, so the two numbers are
consistent, not contradictory.

## Agent Notes
DH.609 corrective landed: send.py comments now say the merge holds for LOCK-TAKING writers from 1f19e160c (an unlocked pre-1f19e160c writer still loses its line), and the swapped-flag comment is corrected to the measured truth (os.replace consumes the tmp entry, names distinct, guard harmless); a00-ac24f72d item-3 rows + THOUGHT rewritten whole; 77 passed 6 skipped; send.py numstat 11/5.

PARENT REVIEW a00-83fd305f (DH.609) — read the BYTES in the checkout, not the report. (1) DELIVERABLES ALL PRESENT: send.py:2210-2212 docstring and :2262-2268 comment now name the class (lock-taking writers, every checkout from 1f19e160c) and say an UNLOCKED pre-1f19e160c writer appends to the OLD inode and loses its line; :2284-2289 finally comment says the tmp entry is CONSUMED, the names are distinct, the guard is harmless not load-bearing, with the measurement in the comment. a00-ac24f72d body 94-102 (item 3) and the authored THOUGHT (rewritten whole, not appended) no longer credit the flag with preventing an impossible deletion. numstat 11/5 = +6 net production, inside the 15 cap; no test added, as the brief allowed for a comment-only fix. (2) MY PROBES, 3, run by me against these bytes, independent of the kid suite (scratch p_dh609.py, temp graphs only): P1 wire HOLD — a lock-taking writer naming inside the swap window is MERGED (memo=[other core-town, late-seat core-town], namer SAID, writer SWAPPED), so the positive half of the corrected comment is live code, not a dead branch; P2 gate HOLD — the SAME race fired by an UNLOCKED pre-1f19e160c writer LOSES the line (memo=[other core-town]), so the caveat the kid added is MEASURED, not a face-saving hedge, and P2 is the probe that would have flipped the item the other way; P3 auth HOLD — after os.replace the tmp entry is consumed (tmp.exists False), the names differ, and a stale unlink leaves the memo intact, so the guard is harmless dead logic and the item-2 correction is right. Each probe was built to falsify and none did. (3) RESIDUE, not a demotion: a00-ac24f72d:187 still carries the false near-miss in its ## Agent Notes, which is auto-rendered from that agent's own done --notes and is not hand-editable by anyone; the kid named it instead of editing it, which is correct. (4) NEAR MISS the kid avoided: writing "the lock serialises all writers" would have satisfied item 1 and re-overclaimed one notch; the comment names the WRITER CLASS, not a global property — the same shape of error as the sentence it replaced, one level down.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW, re-derived from the checkout bytes and from three probes I built and ran, not from the kid report. (1) WHAT THE KID WAS TOLD: two overclaims in the DH.586 residue must be fixed in the bytes or settled with one pasted command, inside 15 net production lines, 1 kid, 0 USD -- the flock mechanism itself accepted, not to be re-argued. (2) WHAT THE MACHINE ACTUALLY DOES: send.py:2210-2212 and :2262-2268 now scope the merge to the WRITER CLASS (lock-taking, every checkout from 1f19e160c) and state the counter-case in the comment itself; :2284-2289 states the measured reason for the guard -- os.replace CONSUMES the tmp entry, the two names are distinct, so the guard is harmless dead logic and not a saver. a00-ac24f72d body 94-102 and its THOUGHT (rewritten whole) match those bytes. My three probes each had a way to FAIL: P1 could have shown the lock is never taken on the append path (dead branch), P2 could have shown the unlocked mixed-fleet writer MERGING, which would make the new caveat false in the other direction and re-open item 1, and P3 could have shown a stale unlink deleting the memo, which would make the kid item-2 correction the lie and the original comment right. Measured: merged / lost / intact respectively -- the comments now match the machine in all three arms. (3) NEAR MISS: the fix could have been to write "the lock serialises all writers" -- same shape of error as the sentence it replaced, one notch more comfortable to read. The kid named the class of writer instead, which is the only claim the bytes support. (4) RESIDUE left standing and named, not hidden: a00-ac24f72d:187 keeps the false near-miss in an auto-rendered ## Agent Notes that only that agent own next done can restate, and the zero-byte .lock sibling is still never pruned. The round closes on the two items it was given; the flock is now documented at the strength it actually has, which is fleet-uniform and no more.
<!-- THOUGHT:END -->
