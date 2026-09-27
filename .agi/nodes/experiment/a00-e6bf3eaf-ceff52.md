---
id: experiment:a00-e6bf3eaf-ceff52
mint_id: 729c7f774cf747d1bb9041ca4e6d6624
type: experiment
parents:
  - hypothesis:every-live-row-carries-its-own-box-and-an-unset-box-is-refused
next_edges: []
confidence: 0.85
edited_by: a00-e6bf3eaf
evidence_runs:
  - experiment:a00-e6bf3eaf-ceff52
loop: hypothesis:every-live-row-carries-its-own-box-and-an-unset-box-is-refused@s2
model: stealth/space-bunny-alpha
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
What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Agent Notes
DH.609 corrective landed: send.py comments now say the merge holds for LOCK-TAKING writers from 1f19e160c (an unlocked pre-1f19e160c writer still loses its line), and the swapped-flag comment is corrected to the measured truth (os.replace consumes the tmp entry, names distinct, guard harmless); a00-ac24f72d item-3 rows + THOUGHT rewritten whole; 77 passed 6 skipped; send.py numstat 11/5.
