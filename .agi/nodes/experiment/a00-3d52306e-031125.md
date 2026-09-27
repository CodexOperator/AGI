---
id: experiment:a00-3d52306e-031125
mint_id: afe7f210372741c6bd550dc167ed6712
type: experiment
parents:
  - hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write
next_edges: []
confidence: 0.7
edited_by: a00-3d52306e
evidence_runs:
  - experiment:a00-3d52306e-031125
  - experiment:a00-6cb920d2-f30271
  - experiment:a00-a022ddab-5727e8
loop: hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 65c57c93599f1a7a
season: 2
title: make the payload-rename chain prose agree with its bytes, and find one more hard defect
town: core
verdict: inconclusive_lean_disproved:70
---
# experiment:a00-3d52306e-031125 — make the chain's prose agree with the chain's bytes

## What this round was

A node-text round: the parent measured the subtree and found the chain's
NODES disagreeing with its BYTES, which is the defect that makes a merge-pass
land the wrong code. Zero production lines, zero test lines — everything below
is measured against the bytes in this checkout, or it is not in the node.

| item | what I did | where |
|---|---|---|
| 1 | named the open broken case as a falsifier a future run must kill | hypothesis FALSIFIERS |
| 2 | narrowed CLAIM conjunct 3 to the checkout-honest shape, in the CLAIM | hypothesis CLAIM |
| 3 | retracted the DH.497 PARENT REVIEW in place, verbatim kept, tabled | experiment:a00-a022ddab-5727e8 |
| 4 | corrected the residue ledger against the bytes (2 of 3 claims were wrong) | experiment:a00-a022ddab-5727e8 Caveats |
| 5 | measured `set location` + a payload verb: CORRECT, recorded as a note | hypothesis FALSIFIERS |
| 6 | named the link_ref/payload_ref ORDER disagreement + its one-line fix | hypothesis FALSIFIERS |
| 7 | hunted further — and found a NEW hard defect (below) | hypothesis FALSIFIERS |

## Probes run (all on temp graphs under /tmp, no live pane, no real mint)

**P-A — `set payload_ref X` in the SAME write as a `payload` verb LOSES the
bytes.** The only new measurement of the round, and it is a hard failure, not a
style point.

```
$ python3 /tmp/probe579/p1.py       # submit() a set payload_ref + payload <file>
RAISED FileNotFoundError payload /tmp/probe579-xxx/lib/mod.py does not exist
      — `payload` replaces bytes, it never creates.
row payload_ref: lib/renamed.py
lib/mod.py      False
lib/renamed.py  True # original bytes
```

Read the code and the shape is inevitable: `submit()` takes the old
`payload_ref`/`location` pair once at write.py:2169 and never re-reads
`payload_ref` from `set_fm`; the mover runs at :2271-2276 and
`replace_payload` runs AFTER it at :2278-2290, still aimed at the OLD path. So
the row lands, the file is renamed, and the caller's new bytes are written
nowhere — the call raises out of `submit()`. Three commitments broken in one
command: the write is not atomic, the bytes are lost, and the mover is supposed
to be the LAST thing before the row.

The fix is the shape submit already uses elsewhere: resolve the payload target
from the EFFECTIVE pair (`set_fm` over on-disk), the same `_effective` helper
the outside-ref gate is built on at :2085-2096.

**P-B — verb ledger, read from the bytes** (this is item 4, and two of the
three claims in the old caveat were wrong):

| verb | reaches the mover's trigger? | read at |
|---|---|---|
| `set payload_ref` / `set location` | YES — the named path | write.py:274-284 |
| `sub` on the node | YES — a changed non-protected frontmatter value lands in `edit.set_fm` | write.py:2407-2418 |
| `body_patch` | NO — `edit.sub_body` / `body_patch_diff` only | write.py:2136-2143 |
| `unset payload_ref` | NO — appends to `unset_fm` only | write.py:288-293 |

against a trigger that reads `set_fm` alone (write.py:2257). So `sub` IS
covered by the mover and the consent gate; `body_patch` cannot reach it at all;
`unset payload_ref` is the only genuine hole, and it is now a named falsifier.

**P-C — the link_ref/payload_ref order disagreement (item 6), confirmed in the
source, not in a report.** `links.link_ref` (links.py:124-142) reads
`link_ref:` first and falls back to `payload_ref:`; `write._payload_ref`
(write.py:2783) does the opposite — `fm.get("payload_ref") or
fm.get(links.LINK_FIELD)`. A node carrying BOTH fields is renamed after one
file and linked as another. One line (`_payload_ref` reads `link_ref` first)
makes both readers share one order, and `goal:g4.18.1.4` requires
`broken_links` 0, so this is a broken link, not a preference.

**P-D — `set location` + a payload verb (item 5) is CORRECT.** The rebinding at
write.py:2237 happens before both the plan and `replace_payload`, and the mover
refuses the cross-base move without `--confirm-move`; with it, the diff taken
on the old base's bytes lands in the moved file. Recorded as a note so the next
run does not spend a kid re-measuring it as a bug.

## Test state (re-measured, not copied)

```
$ python3 -m pytest extensions/agi/tests/test_payload_rename.py -q --basetemp /tmp/pt579
8 passed, 6 warnings in 0.17s
```

8 tests, unchanged: the test file has no case for `unset payload_ref`, for the
`link_ref`/`payload_ref` order, or for P-A, which is why those are named
falsifiers and not closed ones.

## What this round did NOT do, and why

- **No code.** The parent's re-brief answer on the sibling closed this chain's
  production-line budget "at the bytes now on disk" (108-vs-40 accounting, cut).
  P-A and P5 and the `_payload_ref` order are all small fixes; none of them is
  mine to land under a closed ceiling, so they are recorded as falsifiers with
  their probes.
- **No `verdict` on the hypothesis's frontmatter.** `cli.py done` owns that
  field; a kid that edits it by hand is a second source of truth about a chain
  whose whole defect is a second source of truth.

## Caveats

- The brief warned that a third kid's bytes had moved again; **they are not in
  this checkout.** No `a00-cee48ba1` node exists under `.agi/nodes/` here and
  `_link_ref_only` is absent from `extensions/`, so every line number here is
  read off the bytes in THIS worktree at this moment. Re-read before trusting
  them on another branch.
- P-A is a measurement, not a diagnosis of the fix; the `_effective` shape is a
  proposal, and the alternative (move the rename after `replace_payload`, or
  aim `replace_payload` at `_plan.dest`) may be cheaper.
- I did not run the neighbourhood suite; no code changed, so the only claim I
  make about it is the 8 payload-rename tests above.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.579 (a00-3d52306e) — a node-text round with ONE new measurement behind it. The brief said a third kid had moved the bytes again; they are not in this checkout (no a00-cee48ba1 node, no _link_ref_only in extensions/), so every line number I wrote is read off the bytes in this worktree, and I say so in the node rather than citing a line number I did not read. What the round found that no report had: set payload_ref X in the same write as a payload verb LOSES the caller's bytes. submit() reads the payload target once at write.py:2169 and never re-reads it from set_fm, the mover renames at :2271, and replace_payload runs after it at :2278 still aimed at the old path — the call raises FileNotFoundError with the row written, the file moved, and the new bytes nowhere. That is the sharpest thing left against "naming a file is ONE intention", and it is a defect in the ORDER, which is exactly what the previous two kids were already fighting over. Everything else I did was reconciliation: the CLAIM narrowed against its own contradicting test, the DH.497 review retracted in place, the verb ledger corrected (sub IS covered, body_patch never reaches the mover, only unset payload_ref is a hole), the link_ref/payload_ref order disagreement named with its one-line fix, and the set location shape recorded as correct so nobody spends a kid on it again. I fixed no code: the sibling's answered re-brief closed this chain's production-line budget at the bytes on disk, and a fix landed over a closed ceiling is the round being cut.
<!-- THOUGHT:END -->

## Agent Notes
node-text reconciliation + one new hard probe: set payload_ref X with a payload verb raises FileNotFoundError after the row and the rename, losing the caller's bytes (write.py:2169 reads the old ref, :2271 moves, :2278 writes to the old path); CLAIM narrowed against its contradicting test, DH.497 review retracted in place, verb ledger corrected (only unset payload_ref is a hole), link_ref/payload_ref order disagreement named, 0 production lines
