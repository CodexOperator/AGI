---
id: experiment:a00-620bf49d-ac1ffb
mint_id: 2f58598da4764c4e9aab23cf2a31f3bc
type: experiment
parents:
  - hypothesis:every-live-row-carries-its-own-box-and-an-unset-box-is-refused
next_edges: []
confidence: 0.85
edited_by: a00-620bf49d
evidence_runs:
  - experiment:a00-620bf49d-ac1ffb
loop: hypothesis:every-live-row-carries-its-own-box-and-an-unset-box-is-refused@s2
model: claude-opus-5-5
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 25218bf2ef0d29f5
season: 2
title: "EG.52 corrective: EOF deletion claim restated to the measured rule (empty file refused, empty stdin deletes), DH.669 verdict demoted, numstat and residue recounted, quoted THOUGHT de-marked"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-620bf49d-ac1ffb

## What this run did
EG.52 corrective for the DH.669 demote (mur-eg-16). Six items, text only, each fixed
through write.py or settled by a pasted run. 0 production lines, 0 test lines.

| # | item | disposition |
|---|---|---|
| 1 | a00-dd6557af THOUGHT: "replacement AND deletion both land" | **FIXED** — THOUGHT restated to the measured rule below |
| 2 | a00-13835534 body (:65) + THOUGHT carry the same claim | **FIXED** — body sentence and THOUGHT restated |
| 3 | a00-13835534 `verdict: proved` vs its own review's lean_disproved | **FIXED** — `inconclusive_lean_disproved:60`, confidence 0.6 |
| 4 | a00-13835534 numstat lists 3 files, landed 4 | **FIXED** — landed-range numstat pasted beside the old block |
| 5 | own Agent Notes (:202) missing from residue list | **FIXED** — list names it, count "two" → THREE (body + THOUGHT) |
| 6 | a00-939e9e6a quoted THOUGHT pair = its authored region | **FIXED** — markers as text + own THOUGHT; new hazard found |

## Item 1/2 settler — the real rule (the parent review was half right too)
`/dev/shm` throwaway agi project, script + paste in my session dir
(`probe-delete.sh`, `probe-delete.txt`):
```
$ write.py goal:d-file "replace body 1:4 empty.txt"   # empty FILE source, range reaches EOF
ERR: replace source 'empty.txt' is empty — refusing to replace a range with an empty source (it would delete the range). Nothing written. A deliberate deletion needs an explicit signal, not an empty file.
rc=2
$ write.py goal:d-stdin "replace body 1:4 -" </dev/null   # empty STDIN source, range reaches EOF
updated: goal:d-stdin
rc=0
$ write.py goal:r-file "replace body 1:4 new.txt"     # non-empty replacement, range reaches EOF
updated: goal:r-file
rc=0
$ write.py goal:i-file "replace body 1:2 empty.txt"   # empty FILE source, INTERIOR range (1:2 of 5)
ERR: replace source 'empty.txt' is empty — ... Nothing written. ...
rc=2
== d-file.md   body: B1 / B2 / (blank) / TAILY   (unchanged)
== d-stdin.md  body: (none — all 4 body lines deleted)
== r-file.md   body: NEWTAIL
```
| shape | result |
|---|---|
| EOF replacement, non-empty text | lands rc=0 |
| deletion, empty FILE source, any range | refused rc=2 (write.py:1996-2001) |
| deletion, `-` with EMPTY stdin | **lands rc=0** — stdin branch write.py:1984-1988 returns before the check |

So the source kind decides, never the range end. The DH.669 review's "a deletion cannot
be made this way" holds for a file source only. The nodes now say this.

## Item 6 — measured hazard, worse than named
Rendering the quoted markers as text (`replace body 33:33` / `35:35` on a00-939e9e6a)
made `_carry_thought` (node_writer.py:932-935) APPEND the quote's content as a NEW
authored block at the end of the body — the old body's first `_THOUGHT_RE` match was the
quote, the new body had none. Captured before overwrite (`carry-observed.txt`):
```
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS ver
DH.645 (a00-939e9e6a) — this block was destroyed to a literal dash by `write.py <id> 'thought -'`, a verb th
<!-- THOUGHT:END -->
```
Replaced via the `thought` verb with the node's own reasoning. After: one marker pair
(:277/:279), the quoted paragraph appears once (inside the fence), `extract_thought`
returns the EG.52 text. **De-marking a quote promotes it to the node's own thought** —
every de-mark must be followed by a `thought` write.

## Tests
```
$ env -u TMUX -u TMUX_PANE -u AGI_POST -u AGI_SEAT TMPDIR=/dev/shm/... timeout 900 \
    python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q -p no:cacheprovider --basetemp /dev/shm/...
72 passed, 6 skipped in 8.48s
```

## Lines — against the CUT tip (the working tree; this node is untracked, so it is absent)
```
$ git diff --numstat 1e7dbd6d5
37	11	.agi/nodes/experiment/a00-13835534-fb0948.md
7	3	.agi/nodes/experiment/a00-939e9e6a-b4a5fb.md
2	2	.agi/nodes/experiment/a00-dd6557af-ffda28.md
```
+ this node (new). Production 0, test 0, 1 kid, 0 USD. Also run, to settle item 4:
`git diff --numstat 1300bd8c9 1e7dbd6d5` (pasted on a00-13835534).

## For the director's findings row (named, not touched)
- `extensions/agi/bin/write.py:1984-1988` — empty stdin to `replace <t> N:M -` deletes the
  range at rc=0 while an empty file is refused; the guard is asymmetric.
- `extensions/agi/bin/node_writer.py:918-935` — unanchored `_THOUGHT_RE` + `_carry_thought`
  promote a body-quoted THOUGHT to the node's authored thought on any body replace.
- Three `done`-rendered Agent Notes lines still carry the EOF claim (a00-dd6557af:151-155,
  a00-939e9e6a ENGINE BEHAVIOUR bullet, a00-13835534's own summary); next `done` restates.
Every measurement above is pasted from a run; nothing is typed from memory.

## Agent Notes
EG.52 corrective: 6 items fixed via write.py; measured rule = EOF replacement lands, empty FILE source refused rc=2 range-independently, empty STDIN deletes rc=0; a00-13835534 demoted to lean_disproved:60, numstat 3->4 pasted, residue 2->3; a00-939e9e6a quote de-marked, which made _carry_thought promote the quote to authored thought (overwritten with own thought); 0 prod/0 test lines, smoke 72 passed 6 skipped
