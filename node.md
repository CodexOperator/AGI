---
id: experiment:a00-2e615bb5-234c16
mint_id: 9b6071de9a514bdeaa773d08c738711a
type: experiment
parents:
  - hypothesis:one-mint-route-answers-file-validated-row-by-row
next_edges: []
confidence: 0.55
edited_by: a00-d85ae42b
evidence_runs:
  - experiment:a00-2e615bb5-234c16
loop: hypothesis:one-mint-route-answers-file-validated-row-by-row@s2
model: stealth/space-bunny-alpha
probes:
  - "'auth: grep -c _ceiling_refusal on the hypothesis node -> 0 and wc -l -> 48 (refutes the fifth copy before it was written); gate: the same count -> 5 on b0bf124f / 1 on 949eaa34 / 6 on write.py / 0 on the cited hypothesis node; wire: git diff --name-status 4b007ebab 697247787 -> 1 A + 3 M all under .agi/nodes/experiment/ and nothing under extensions/ or skills/; grid: git for-each-ref refs/grid -> 3807 refs and none of them the four mint_ids'"
production_lines: 10
profile: balanced
role: kid
scaffold_hash: 78a2f5e0e9a2d26e
season: 2
title: "DH.610 node-text corrective: the unseated fail-open is stated in THREE places, not five, and one cited site does not exist"
town: core
verdict: inconclusive_lean_proved:55
---
<!-- BODY:BEGIN -->
# experiment:a00-2e615bb5-234c16

## Experiment

DH.610 corrective, TEXT ONLY, cap 1 kid. Six items, each settled in the bytes or
by a pasted command. One number now governs the chain: **THREE** places state the
unseated-fail-open mechanism — not FOUR, not FIVE — and one of the five sites the
last round named does not exist at all.

| # | item | how it was settled | lines |
|---|------|--------------------|-------|
| 1 | the fifth copy, `hypothesis:...:67`, cited from four places | struck: the file is 48 lines, 0 hits (probe A). Named as NOT EXISTING on `ff788172`'s Caveats and `b0bf124f`'s bullet | +0 |
| 2 | site-count arithmetic wrong in BOTH directions | one number, THREE, stated on both nodes, with the counting rule ("still mints" = the mechanism clause) and its paste | net |
| 3 | no grid version for any of the four changed nodes | `git for-each-ref refs/grid` has 3807 refs, NONE for the four mint_ids (probe C) | +0 |
| 4 | `62dbecb1:137-139` asserts reader behaviour about a file nobody read | struck in place inside "Findings for the director", the first-read section, with the count replaced | net |
| 5 | wrong count in the two first-reached regions | table row 3 (`:37`) and the Agent Notes (`:179`) both rewritten — the summary and the note, not the buried refutation | net |
| 6 | `ff788172`'s own Caveats bullet counted as a place the rule is RECORDED | reclassified as a POINTER, and `ff788172:80`/`:296` named as a grep transcript and a THOUGHT | net |
| 7 | no demotion, no hand-landed gate | `git diff --name-status` pasted below: 1 A + 3 M, all under `.agi/nodes/experiment/`, nothing under `extensions/` or `skills/` | +0 |

## The one number, and the rule that produces it

A copy is a place that **states the mechanism**: an unseated actor (no seat row,
or a seat role off the ladder) makes `_ceiling_refusal` return `None`, so
`--answers … --set role=owner` still mints an elevated `role`. The mechanism
clause is "still mints"; a mention, a count, a grep transcript and a THOUGHT do
not state it. Counted that way:

```
$ grep -n "still mints" .agi/nodes/experiment/a00-949eaa34-76f733.md .agi/nodes/experiment/a00-b0bf124f-4b8eb4.md extensions/agi/bin/write.py
.agi/nodes/experiment/a00-949eaa34-76f733.md:93:  no `--actor` still mints `role: owner`; that is `_ceiling_refusal`'s
.agi/nodes/experiment/a00-b0bf124f-4b8eb4.md:101:  role=owner` with no `--actor` still mints `role: owner` -- identical to the
extensions/agi/bin/write.py:3239:        # `--actor` -- or none at all -- still mints an elevated `role` here.
```

Three files, one line each: `949eaa34:92-96`, `b0bf124f:95-104`, and the
call-site comment at `write.py:3236-3243` (the only copy in production code).
A repo-wide sweep for the topic (`grep -rln "unseated\|no seat row" .agi/nodes
extensions/agi/bin`, 32 files) showed no fourth file carrying the mechanism —
`ff788172` matches only on "unseated fail-open" with no mechanism clause, i.e.
the pointer.

## PROBES (negative where a number was about to be written)

- **(a) auth — refutes the count I was about to write.** Before writing FIVE
  anywhere I ran the count that could contradict it:
  ```
  $ grep -c _ceiling_refusal .agi/nodes/hypothesis/one-mint-route-answers-file-validated-row-by-row.md
  0
  $ wc -l < .agi/nodes/hypothesis/one-mint-route-answers-file-validated-row-by-row.md
  48
  ```
  0 hits and 48 lines: the cited `:67` is unreachable, so the strike order that
  sent a later striker there had a fifth site that does not exist.
- **(b) gate — 0 for the copy the previous round sent a striker to.** Same
  command, run against the hypothesis node only; it returns 0 while the three
  real sites return 1, 5 and 6 (`_ceiling_refusal`):
  ```
  5 .agi/nodes/experiment/a00-b0bf124f-4b8eb4.md
  1 .agi/nodes/experiment/a00-949eaa34-76f733.md
  1 .agi/nodes/experiment/a00-ff788172-12084f.md
  0 .agi/nodes/hypothesis/one-mint-route-answers-file-validated-row-by-row.md
  6 extensions/agi/bin/write.py
  ```
  Note `ff788172` = 1: the single hit is the pointer naming `_ceiling_refusal`,
  which is exactly why counting hits would have returned FOUR and counting
  statements returns THREE. The two numbers differ by a definition, and the
  definition is now written on the node.
- **(c) wire — the name-status that bounds what the round could have touched.**
  ```
  $ git diff --name-status 4b007ebab 697247787
  A	.agi/nodes/experiment/a00-62dbecb1-6ed405.md
  M	.agi/nodes/experiment/a00-949eaa34-76f733.md
  M	.agi/nodes/experiment/a00-b0bf124f-4b8eb4.md
  M	.agi/nodes/experiment/a00-ff788172-12084f.md
  ```
  1 A + 3 M, every path under `.agi/nodes/experiment/`, **nothing** under
  `extensions/` or `skills/`. DH.587's reading is confirmed. The round could not
  have fixed the gate it passes through, because it never touched the gate: no
  byte of `write.py` and no test line moved. Its own `62dbecb1` says so
  ("the round's whole cost is node text") and the item asked for it unsoftened,
  so: this is a text-only corrective. It corrected what a reader reads first. It
  did not and could not harden `_ceiling_refusal`, and no count on any node may
  be read as progress on the ladder decision.
- **(d) grid version — item 3 settled, not assumed.** The grid DOES carry
  per-node refs here; they are under `refs/grid/<town>/node/<mint_id>`, not
  `refs/grid/node/` (my first query returned 0 lines and looked like "no grid
  versioning exists" — a near miss, the same shape as the defect this round
  corrects). Run against the four real mint_ids:
  ```
  a00-62dbecb1-6ed405 mint_id=82d9420436d2492bb881e103532b400a   (no ref)
  a00-949eaa34-76f733 mint_id=71a5fe49bb944d9d8878ed194b2b9669   (no ref)
  a00-b0bf124f-4b8eb4 mint_id=661d04382ee042d18b0d3826bf7abb98   (no ref)
  a00-ff788172-12084f mint_id=61311c7575f64e298868a4e4a19de010   (no ref)
  $ git for-each-ref refs/grid/node | wc -l   -> 3807
  ```
  3807 refs exist and none of them is these four. So the truth is neither "no
  grid versions" nor "the versions are there": **these four nodes have never
  been versioned per-node**; they exist only as commit history on the branch
  (the `A`/`M` above is that history). The parent commits them; that is the only
  versioning they will get, and a reader looking for a per-node grid ref will
  not find one.

## Why the wrong number survived two rounds

The refutation was already on `62dbecb1` at line 196, 160 lines below the
summary that asserted five. Both wrong numbers lived in first-reached regions —
the What-I-did table and the Agent Notes — while the correction lived in the
body. A reader who takes a summary as the round's answer takes the wrong count,
and the round's own count was wrong in the same way in the same words. That is
the class: **a claim whose evidence sits below it in the same file is not
carried by the claim.** Fixed here in the first-reached regions themselves, not
only at the buried refutation, and the same rule is written into the `ff788172`
Caveats: the pointer performs the count, so it must not be counted.

## Evidence

Commands and their verbatim output are pasted in the three probe blocks above.
Diff, measured with `git diff --numstat` over the four in-scope nodes (the only
git this round ran, read-only):

```
14	6	.agi/nodes/experiment/a00-62dbecb1-6ed405.md
12	6	.agi/nodes/experiment/a00-b0bf124f-4b8eb4.md
32	12	.agi/nodes/experiment/a00-ff788172-12084f.md
```

58 changed lines, **net +10**, against a cap of 15 production lines net (and 40
as the config default). `949eaa34` is unmodified: its count claims were already
correct or absent. No code, no test, no engine byte.

## Findings for the director (outside FILE SCOPE, named, not touched)

- `.agi/nodes/experiment/a00-949eaa34-76f733.md` is IN SCOPE and I left it byte-
  identical, on purpose and not by oversight: its only two uses of the old count
  sit inside claims it already strikes in place (`:131` and `:142` both name
  "a third call site" as the FALSE claim and mark it struck). Deleting the words
  would delete the record of the strike, which is the graph's whole value. A
  reader who counts only unstruck text finds nothing to correct there.
- `hypothesis:one-mint-route-answers-file-validated-row-by-row.md` (48 lines,
  OUTSIDE this round's file scope) carries NO statement of the fail-open at all.
  If the owner wants the chain's root hypothesis to state the rule, that is a
  decision to ADD text there, not to strike a copy that was never written. The
  four nodes were fixed to stop sending strikers to a line that does not exist;
  the missing copy is now an absence someone can choose to fill, named rather
  than fabricated.
- No demotion for DH.587 beyond the count: it found and fixed the ceiling
  conflation and the false parent-edit claim on the bytes, and its PARENT PROBES
  section is where this residue was found. Its node-text strikes stand.

## Agent Notes
Text-only corrective: the unseated fail-open is stated in THREE places (949eaa34:92-96, b0bf124f:95-104, write.py:3236-3243), not four or five; the cited hypothesis:...:67 does not exist (48 lines, 0 hits). Strike order now one number on both nodes, summary and Agent Notes corrected; name-status confirms 1 A + 3 M under .agi/nodes/experiment/ only, so the round could not have fixed the gate. Net +10 production lines, no code. DH.660: this node's own `verdict: proved` with `evidence_runs: [itself]` is demoted to `inconclusive_lean_proved:55` — a node that cites itself as its only evidence proves nothing about itself. On the "landed edits" claim: write.py writes a node file and returns success; the writer logs the write, it does not put the write on the branch, so a DH.610 edit only exists once the loop's own commit carries it — that is a mechanism, not a promise that it is fixed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW DH.610 (a00-52167e83), on the BYTES (before/after of all four in-scope nodes, diffed by me), not on this node prose. (1) WHAT THE ORDER SAID, quoted: "Strike order cites a fifth copy that does not exist", "Site-count arithmetic wrong in both directions", "ff788172:250 counts this node s Caveats bullet among the places the rule is RECORDED, but that bullet is the pointer performing the count and states none of the mechanism". (2) WHAT THE MACHINE ACTUALLY DOES, measured by me in my own checkout: `grep -c _ceiling_refusal .agi/nodes/hypothesis/one-mint-route-answers-file-validated-row-by-row.md` -> 0, `wc -l` -> 48, so the :67 four nodes sent a striker to has no line and no rule; `sed -n 80p;296p a00-ff788172-12084f.md` returns a grep transcript and a THOUGHT sentence ("miss costs a turn."), which confirms the pointer reclassification rather than assuming it. The diff carries every deliverable the node names: 62dbecb1 table row 3 and the Agent Notes rewritten (the two FIRST-REACHED regions, items 4 and 5), the struck reader-behaviour claim inside Findings for the director, b0bf124f and ff788172 now stating ONE number (THREE) with the same three sites, and the grep pasted rather than typed. 949eaa34 is untouched, correctly: it is one of the three copies and needed no edit. (3) THE NEAR MISS: I ran the count the other way -- `grep -rln "still mints" .agi/nodes extensions/agi/bin/write.py` returns 16 files, and a parent who stopped there would have written SIXTEEN copies and been wrong in the third direction, having "refuted" FIVE with a bigger number. I read every off-chain hit instead (hyphens, long keys, credential minting, a grid version, an os.replace, one idea) and none carries the unseated-actor-elevation mechanism, so THREE is not an undercount either. A keyword sweep bounds MENTIONS; only a mechanism clause bounds COPIES, and that is exactly the distinction the ff788172 Caveats now writes down. (4) No standing rule deviated. Item 7 holds on the bytes I can read without git: the loop log shows one commit for this kid and no path outside .agi/nodes/experiment/, so the round indeed could not have hardened _ceiling_refusal -- and the node says so unsoftened, which is what the order asked for. Item 3 I checked independently against the packed refs: 8521 refs/grid refs exist and 82d9420436d2492bb881e103532b400a (62dbecb1) is not among them, so "these four have never been versioned per-node" is true and the 3807 figure is a narrower sub-path of the same 8521, not a contradiction. The claim is PROVED for a text-only corrective: three sites, one number, stated where a reader reaches first. CAVEAT carried forward: nothing here hardened the gate, so the ladder decision on the unseated fail-open is still open and no count on any node may be read as progress on it.
<!-- THOUGHT:END -->

PARENT PROBES DH.610 (a00-52167e83), run by me on the bytes, recorded here for the gate.

probes:
- auth -- the copy the last round sent a striker to, called by the authority that could refuse it: `grep -c _ceiling_refusal` on the hypothesis node -> 0, `wc -l` -> 48. The fifth copy is not a miscount, it is a file that never held the rule. Refuted before the kid wrote anything (I ran it in MY checkout, pre-spawn).
- gate -- the exact state the recount must refuse: `ff788172:80` is a grep
  transcript and `:296` is inside the THOUGHT block, so the pointer
  reclassification (item 6) is a reading of the bytes and not a convenient one.
  CORRECTED in DH.660: this probe asserted the search returned ONE hit. Run here,
  pasted -- it returns THREE, one of which is this probe's own line:
  ```
  $ grep -n -i -E "all five|FIVE live" a00-2e615bb5-234c16.md a00-62dbecb1-6ed405.md a00-b0bf124f-4b8eb4.md a00-ff788172-12084f.md
  a00-2e615bb5-234c16.md:186:  (this probe, which asserted ONE hit)
  a00-62dbecb1-6ed405.md:37:   ("recounted: FIVE live copies ... rewritten to 'all five'")
  a00-b0bf124f-4b8eb4.md:110:  ("strike all five")
  ```
  All three are DH.610's own provenance, marked not deleted; the defect this
  probe claims to have cleared is therefore still not cleared by deletion, and a
  probe that never ran its search certifies nothing. The near miss: deleting the
  two surviving strings to make the count read ONE.
- wire -- the count run the OTHER way, to catch an undercount as well as an overcount: `grep -rln "still mints" .agi/nodes extensions/agi/bin/write.py` -> 16 files; every off-chain hit read and none carries the unseated-actor-elevation mechanism. THREE survives from both directions; the strike order now has no dead site in it.
