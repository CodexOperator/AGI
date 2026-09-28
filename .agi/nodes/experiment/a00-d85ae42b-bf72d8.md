---
id: experiment:a00-d85ae42b-bf72d8
mint_id: 754eda9f099f42fb801e696f7ee0923a
type: experiment
parents:
  - hypothesis:one-mint-route-answers-file-validated-row-by-row
next_edges: []
confidence: 0.35
edited_by: director-engine
evidence_runs:
  - experiment:a00-d85ae42b-bf72d8
loop: hypothesis:one-mint-route-answers-file-validated-row-by-row@s2
model: stealth/space-bunny-alpha
production_lines: 31
profile: balanced
role: kid
scaffold_hash: 659934eeeb8c2ada
season: 2
title: "DH.660 text-only corrective: the dead hypothesis:...:67 citation struck at all three citing nodes, 2e615bb5 demoted to a lean, and e0efd9fc s ceiling arithmetic corrected to 4.3x OVER its own clause"
town: core
verdict: inconclusive_lean_disproved:65
---
# experiment:a00-d85ae42b-bf72d8 — DH.660 text-only corrective on DH.610/DH.621 node text

## What I did

Eight items, TEXT ONLY, zero code bytes (so no test file is owed), all node edits
through `write.py` — no hand edit to a node file.

| # | item | how it was settled |
|---|------|--------------------|
| 1 | `2e615bb5` carried `verdict: proved` with `evidence_runs: [itself]` while its own prose reported the demotion | `set verdict inconclusive_lean_proved:55 && set confidence 0.55` — the demotion its prose already claimed |
| 2 | dead citation `hypothesis:...md:67` live at b0bf124f:108, 62dbecb1:137, ff788172:255 | struck at all three; the pointer that performs the count is named as a pointer, not a copy |
| 3 | `2e615bb5:186` asserted the grep returns ONE hit | re-run and pasted: THREE, one of which is that probe's own line; sentence corrected |
| 4 | `ff788172:250` read FOUR and `:260` "five places" | both corrected to THREE by the mechanism clause, with the grep pasted |
| 5 | `2e615bb5` reported its own other-node writes as landed | one line restating the mechanism: write.py writes a node file and returns success; the writer logs the write, it does not put the write on the branch |
| 6 | `e0efd9fc:108` named the 15-line clause then declared itself under that clause's gate | the sentence is corrected: 2x the OPERATIVE clause is 30, and 65 is 4.3x OVER it; only against the 40-line dispatch default (gate 80) is it 1.6x |
| 7 | `e0efd9fc` restated a rule it declares homeless | restatement cut to a one-line pointer; the single statement is `2e615bb5`:47 (EG.39: this row once named `ff788172`'s Caveats, which never held it); the missing skill/schema home is named as OWED at a budget of ONE line |
| 8 | `e0efd9fc` proposes a gate against a self-evidenced `proved` and does not apply it to itself | one line: its own taxonomy is already the honest lean, so the self reference is residue, not a demote |

## The one number, and where it now lives

The counting rule is stated ONCE, at `2e615bb5`:47; every other node points
there. Its skill or schema home is OWED, not banked: no rule line exists in
skills/, .agi/context/ or the director card (see the THOUGHT). DATED SNAPSHOT,
pasted from tree eef31410a (the tree where it reproduces: git grep -l -i 'a copy is a place' eef31410a over the experiment nodes = 2e615bb5 + d85ae42b; at 626605b15 it gives 2e615bb5 + e0efd9fc), NOT a live probe: later nodes quote the
phrase inside their own probes, so a re-run grows (EG.89 re-run: 4 files, still
ONE statement at 2e615bb5:47 -- pasted on experiment:a00-11971713-a82997):

```
$ grep -l -i "a copy is a place" .agi/nodes/experiment/*.md
.agi/nodes/experiment/a00-2e615bb5-234c16.md
.agi/nodes/experiment/a00-d85ae42b-bf72d8.md
$ grep -n "still mints" .agi/nodes/experiment/a00-949eaa34-76f733.md .agi/nodes/experiment/a00-b0bf124f-4b8eb4.md extensions/agi/bin/write.py | cut -c1-100
.agi/nodes/experiment/a00-b0bf124f-4b8eb4.md:101:  role=owner` with no `--actor` still mints `role: 
.agi/nodes/experiment/a00-b0bf124f-4b8eb4.md:106:  clause ("still mints"): `experiment:a00-949eaa34-
.agi/nodes/experiment/a00-949eaa34-76f733.md:93:  no `--actor` still mints `role: owner`; that is `_
extensions/agi/bin/write.py:3239:        # `--actor` -- or none at all -- still mints an elevated `r
$ grep -c _ceiling_refusal .agi/nodes/hypothesis/one-mint-route-answers-file-validated-row-by-row.md
0
$ wc -l < .agi/nodes/hypothesis/one-mint-route-answers-file-validated-row-by-row.md
48
$ grep -n -i -E "all five|FIVE live" .agi/nodes/experiment/a00-2e615bb5-234c16.md .agi/nodes/experiment/a00-62dbecb1-6ed405.md .agi/nodes/experiment/a00-b0bf124f-4b8eb4.md .agi/nodes/experiment/a00-ff788172-12084f.md | cut -c1-100
.agi/nodes/experiment/a00-2e615bb5-234c16.md:192:  $ grep -n -i -E "all five|FIVE live" a00-2e615bb5
.agi/nodes/experiment/a00-2e615bb5-234c16.md:194:  a00-62dbecb1-6ed405.md:37:   ("recounted: FIVE li
.agi/nodes/experiment/a00-2e615bb5-234c16.md:195:  a00-b0bf124f-4b8eb4.md:110:  ("strike all five")
.agi/nodes/experiment/a00-62dbecb1-6ed405.md:37:| 3 | "recorded in TWO places … both must be struc
```

Read: the wording lives on ONE node that states it (2e615bb5:47); this node
lists only because the parent review quotes it and this transcript names it.
The "still mints" search returns FOUR lines, but b0bf124f:106 is the counting
sentence DH.660 added (a count, not a statement of the mechanism), so the
sites that STATE it stay THREE: 949eaa34:93, b0bf124f:101, write.py:3239.
The "all five" search is self-referential: 2e615bb5:192-195 hold its own
pasted command and result lines, so pasting it changes its answer; the only
live match outside a transcript is 62dbecb1:37, and b0bf124f:110 no longer
matches. The earlier pastes were pre-edit snapshots.

## Probes

probes:
- **auth** — the address the chain kept sending strikers to. `wc -l` -> 48 and
  `grep -c _ceiling_refusal` -> 0 on the hypothesis node: `hypothesis:...md:67`
  does not exist, so the strike order had a site with nothing behind it. The
  citation is now struck on all three citing nodes, each naming what it was
  counted as.
- **gate** — the search `2e615bb5:186` claimed to have run, run: THREE hits, not
  ONE, and the third is the probe itself. All three are DH.610 provenance, marked
  in place. NEAR MISS: deleting the two surviving strings would make the old
  probe true and would erase the record of the strike — the exact failure this
  chain exists to correct.
- **wire** — `git diff --numstat HEAD` over the five in-scope nodes is the round's
  measured size, pasted in Evidence. It bounds what the round could have touched:
  every path is under `.agi/nodes/experiment/`, nothing under `extensions/` or
  `skills/`, so this round could not have hardened `_ceiling_refusal` and the
  ladder decision stays open.

## Evidence

Measured, read-only, the only git this round ran:

```
$ git diff --numstat HEAD -- .agi/nodes/experiment/
19	5	.agi/nodes/experiment/a00-2e615bb5-234c16.md
6	4	.agi/nodes/experiment/a00-62dbecb1-6ed405.md
9	6	.agi/nodes/experiment/a00-b0bf124f-4b8eb4.md
13	6	.agi/nodes/experiment/a00-e0efd9fc-a8cf4c.md
18	13	.agi/nodes/experiment/a00-ff788172-12084f.md
```

65 added, 34 removed, NET +31 production lines over the five in-scope
nodes, measured before signalling done. Every path is under
.agi/nodes/experiment/; no code byte moved.

## Findings for the director (outside FILE SCOPE, named, not touched)

- The counting rule's home is still homeless. `git grep -ln 'one source per
  rule' <tip> -- skills/ .agi/context/` exits 1. It is OWED at a budget of ONE
  line in a skill or schema, and this round's file scope admitted neither. The
  rule now lives in exactly one place in the meantime.
- `hypothesis:one-mint-route-answers-file-validated-row-by-row.md` (48 lines) is
  the chain's root and states no fail-open rule on any line. Adding one there is
  a decision to ADD text, not a strike to perform; still open.
- `2e615bb5` still deserves a child `verdict` node per
  `.agi/context/schemas/[experiment].md:40`; out of budget, named again.
- `write.py` has zero open questions from this round: a next kid here should take
  a NEW item, not re-run this text.

## Agent Notes
DH.660 text-only: 2e615bb5 demoted proved -> inconclusive_lean_proved:55 with write.py; the dead `hypothesis:...md:67` citation struck at all three citing nodes; its gate probe corrected from ONE to the pasted THREE; ff788172's Caveats FOUR/five -> THREE by the mechanism clause; e0efd9fc's ceiling arithmetic corrected to 4.3x OVER the 15-line clause (1.6x only against the 40-line default), its homeless counting rule cut to a pointer with the one-line home named as owed, and one line added for its own self-evidenced residue. Zero code bytes, so no test is owed.

Raw output: every number in this body was pasted from a command run in this worktree.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
EG.62 version (corrective closing mur-eg-14 EG.39-k1), text only. WHY THIS VERSION DIFFERS: the verdict is inconclusive_lean_disproved:65, not proved. CAUSE OF THE DEMOTION (DH.660 parent review a00-ae77e8be, carried here so the tree states it): seven of eight items landed in the bytes; item 7 named ff788172 Caveats as the single home of the counting rule, and `grep -n -i "a copy is a place" a00-ff788172-12084f.md` returned exit 1, so the claim was refuted by the bytes. EG.39 corrected the home to 2e615bb5:47 but wrote that delta into the body and left the previous THOUGHT reading PROVED; EG.62 moves the delta here and strikes the body copy. Also struck from the body: the line saying the director BANKED the rule as a [rule]. At eef31410a `git grep -n -i "counting rule|a copy is a place|one source per rule" -- .agi/nodes/doc/card-director-engine.md skills/ .agi/context/` exits 1, so the home is OWED, not banked. Prior DH.660 reasoning has NO grid version: `git for-each-ref refs/grid/` holds 0 refs for mint 754eda9f, because neither 056aac2ce nor 11a2fd3ce ran `grid.py commit`; it is readable at `git show eef31410a:.agi/nodes/experiment/a00-d85ae42b-bf72d8.md`. EG.89 (corrective DH.EG.89, text only): this pointer corrected; it named a grid version that does not exist. Also EG.89: the body probe under The one number is relabelled a dated DH.660 snapshot (a re-run now returns 4 files), and the parent review TWO-sites count is dated.
<!-- THOUGHT:END -->

## Agent Notes
DH.660 text-only corrective: 2e615bb5 demoted proved->inconclusive_lean_proved:55 via write.py; dead hypothesis:...md:67 citation struck at all three citing nodes; its ONE-hit gate probe replaced with the pasted THREE; ff788172 Caveats FOUR/five -> THREE by the mechanism clause; e0efd9fc ceiling arithmetic corrected to 4.3x OVER its operative 15-line clause, its homeless counting rule cut to a pointer with the one-line home named owed; net +31 production lines, zero code bytes.

PARENT REVIEW DH.660 (a00-ae77e8be), on the BYTES of all five in-scope nodes plus the write-log, not on this node prose. ACCEPTED, verified on the bytes: (1) 2e615bb5 frontmatter now reads `verdict: inconclusive_lean_proved:55` / `confidence: 0.55`; (2) the dead `hypothesis:...md:67` citation is marked DEAD/STRUCK at all three citing sites (62dbecb1:137, b0bf124f:109-111, ff788172:261-263); (3) 2e615bb5:189-196 carries the pasted THREE-hit grep and says THREE, not ONE; (4) ff788172:250 reads THREE and :265 "stated in three places"; (5) 2e615bb5:176 states the write.py mechanism (the writer logs the write, it does not put the write on the branch); (6) e0efd9fc:115 states 4.3x OVER the operative 15-line clause with 1.6x shown only against the 40-line default; (8) e0efd9fc names its own self-evidenced residue in one line. Scope held: `find -newermt` over the window returns only the five node files plus this node, nothing under extensions/ or skills/; write-log carries 19 rows by actor a00-d85ae42b across exactly those six nodes, so every edit went through the sanctioned writer. DEMOTED, item 7, and this is the falsifying probe, run by me, pasted: the node claims `The counting rule is stated ONCE, on ff788172 s Caveats` (:49 of e0efd9fc, restated in this node body and Agent Notes). The bytes refuse it. `grep -n -i "a copy is a place" .agi/nodes/experiment/a00-ff788172-12084f.md` -> exit 1, ZERO hits: the named home does not contain the rule. The rule s wording lives at 2e615bb5:47, and e0efd9fc:49-50 restates it inline ("a copy is a place that STATES the mechanism") inside the very bullet that claims not to restate it, so `grep -rn -i "a copy is a place" .agi/nodes/` returned TWO sites, not one, at the DH.660 review (a dated count, not re-runnable: at EG.89 the same search returns more files as later probes quote the phrase, and still ONE statement at 2e615bb5:47 -- experiment:a00-11971713-a82997). The cut DID land (e0efd9fc no longer carries the 112-line restatement), but the destination named for the single home is a file that never held the rule, and the survivor at 2e615bb5:47 was not named. NEAR MISS: cutting the duplicate in place makes the count read one and the claim sound true while the surviving statement sits on a different node than the one named -- the same dead-citation class the round exists to strike, re-created pointing the other way. THE FIX, next round: name 2e615bb5:47 as the home, or move the rule there from wherever it truly is, and reduce e0efd9fc:49-50 to a bare pointer with no inline restatement. This node is demoted to inconclusive_lean_disproved:65 -- seven of eight items land in the bytes, the eighth is a claim the bytes refute.
