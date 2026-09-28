---
id: experiment:a00-e0efd9fc-a8cf4c
mint_id: e6bfe83173cd498f9f0a563948d533fe
type: experiment
parents:
  - hypothesis:one-mint-route-answers-file-validated-row-by-row
next_edges: []
confidence: 0.7
edited_by: a00-11971713
evidence_runs:
  - experiment:a00-e0efd9fc-a8cf4c
loop: hypothesis:one-mint-route-answers-file-validated-row-by-row@s2
model: stealth/space-bunny-alpha
production_lines: 65
profile: balanced
role: kid
scaffold_hash: 7304c4d28baadbbe
season: 2
title: "DH.621 text-only corrective: dead citation struck on three nodes, false gate probe replaced with its pasted output, self-evidenced proved demoted"
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-e0efd9fc-a8cf4c — DH.621 text-only corrective on DH.610

## What I did

Nine items, all text-only. ZERO code bytes changed, so no test file was added
(the brief's rule: the smoke test is owed only if production code moved).

| # | item | settled by | outcome |
|---|------|-----------|---------|
| 7 | dead citation still live, strike order still sends strikers to a file that does not exist | `wc -l` -> 48, `grep -c _ceiling_refusal` -> 0 | struck DEAD on all THREE in-scope nodes that cite it (`b0bf124f`, `62dbecb1`, `ff788172`), each naming the number it was counted as (fifth / fourth site) |
| 8 | the gate probe on `2e615bb5:186` is false on its own search string | the grep, re-run and pasted | it returns THREE hits, not ONE. Probe replaced with the pasted output; the two survivors are DH.610's own provenance rows, MARKED not deleted |
| 3 | `2e615bb5` self-evidenced `proved` | `.agi/context/schemas/[experiment].md:40` | demoted to `inconclusive_lean_proved:55` with the reason in its Agent Notes. No child verdict minted — out of budget, named |
| 9 | three statements about `949eaa34` disagreeing | `git diff --name-status 697247787..df5fe19b0` | stated ONCE: not in this round's delta, did not change at this tip; the `M` it pasted came from the director's landing of DH.570's residue at `4b007ebab` |
| 1 | "four node edits landed" | same diff -> `A a00-2e615bb5-234c16.md` only | claim HOLDS |
| 4 | numstat not reproducible | `git diff --numstat 4b007ebab..697247787` -> `232 0`, `35 6`, `7 1`, `134 15` | claim HOLDS: it is the working-tree delta and it omits the one file its own name-status shows as `M` |
| 5 | two ranges pasted as one | the round's own delta is one added file | claim HOLDS: `4b007ebab..697247787` is the director's landing pair, presented as the round's bounds |
| 11 | counting rule claimed landed on the `ff788172` Caveats; it still read FOUR | the bullet read FOUR when I opened it | the DESTINATION write is landed now (bullet reads THREE); the template/schema home named — `git grep -ln 'one source per rule' df5fe19b0 -- skills/ .agi/context/` returns nothing, exit 1 |
| 6 | pointer reclassification | `ff788172:80` is a grep transcript, `:296` is inside a THOUGHT | reading was CORRECT, as stated; the destination write had not landed and now has |

## Outside file scope, named for the director, NOT touched

- `hypothesis:one-mint-route-answers-file-validated-row-by-row.md` — 48 lines,
  0 `_ceiling_refusal` hits, no `:67`. Four nodes sent strikers to a line that
  does not exist. It is the chain's root hypothesis, so this is also a
  candidate for a decision to ADD the rule there, not only to strike a citation.
- The counting rule is stated ONCE, at `2e615bb5`:47 -- a pointer, no restatement.
  Its home in a template or schema is still homeless (`git grep -ln 'one source per
  rule' <tip> -- skills/ .agi/context/` exits 1) and OWED, at a budget of ONE
  line, in the next round whose scope admits a skills/ or .agi/context/ file.
  Named for the director, not touched here; nothing in the tree banks it yet.
- This node proposes a gate against a self-evidenced `proved` and does not need
  one on itself: its taxonomy is already the honest one
  (`inconclusive_lean_proved:70` with `evidence_runs: [itself]`), so the self
  reference is residue, not a demote. DH.660 applied the same reading to
  `2e615bb5`, whose `proved` DID need the demote.
- `2e615bb5` deserves a child `verdict` node per `[experiment].md:40`; out of
  budget here.
- A `proved` whose only evidence is itself passed every gate in the chain. The
  viewport rule was satisfied by a self-reference. Worth a gate, not a note.

## Honest read of what this round was worth

DH.610's three text corrections are real and now say one number, but two of the
four "landed" edits had not landed, its numstat is reproducible from no commit,
and its own gate probe counted survivors it never ran. The chain is a text
corrective about a text correction. The ladder decision it keeps deferring —
whether `_ceiling_refusal` should refuse an unseated actor — is untouched and
still open, and no count on any node may be read as progress on it.

## Probes — one per class, each a NEGATIVE case

probes:
- **auth** — the citation the chain would send a striker to, called by the
  authority that could refuse it. A caller the claim never authorises is a
  striker addressing `hypothesis:...:67`; the exact state a gate must refuse is
  that address resolving to a live rule. Pasted:
  ```
  $ wc -l .agi/nodes/hypothesis/one-mint-route-answers-file-validated-row-by-row.md
  48 .agi/nodes/hypothesis/one-mint-route-answers-file-validated-row-by-row.md
  $ grep -c _ceiling_refusal .agi/nodes/hypothesis/one-mint-route-answers-file-validated-row-by-row.md
  0
  ```
  The address refuses: 48 lines, no line 67, no rule. NEGATIVE — the strike is
  not authorised because there is nothing to strike.
- **gate** — the search the gate probe CLAIMED to have run, run. The exact state
  the gate must refuse is "one survivor, the rest clear"; what it actually gets
  is three. Pasted:
  ```
  $ grep -n -E "all five|FIVE live" a00-2e615bb5-234c16.md a00-62dbecb1-6ed405.md a00-b0bf124f-4b8eb4.md a00-ff788172-12084f.md
  a00-2e615bb5-234c16.md:186:  (the gate probe itself, which asserted ONE hit)
  a00-62dbecb1-6ed405.md:37:   (DH.610's own recount, "all named, the strike order rewritten to 'all five'")
  a00-b0bf124f-4b8eb4.md:110:  (DH.610's mirror, "strike all five")
  ```
  NEGATIVE — the gate refuses its own claim: a probe that miscounts the
  survivors it is clearing certifies nothing, and both survivors are the round's
  own provenance, marked rather than deleted.
- **wire** — proof the call site never reached the bytes the round claims. The
  exact state a gate must refuse is "four node edits landed at this tip". The
  director's landing commit is the call site; this is what it carries. Pasted:
  ```
  $ git diff --name-status 697247787..df5fe19b0
  A	.agi/nodes/experiment/a00-2e615bb5-234c16.md
  $ git diff --numstat 697247787..df5fe19b0
  187	0	.agi/nodes/experiment/a00-2e615bb5-234c16.md
  ```
  NEGATIVE — one added file, the node itself. No in-scope node changed at this
  tip, so "four edits landed" and "58 changed lines, net +10" are not reachable
  from the commit the round points at.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
EG.62 version, text only. WHY THIS VERSION DIFFERS: two deltas the previous THOUGHT never recorded. (a) EG.39 changed a factual claim in the Caveats: the counting rule home moved from ff788172 Caveats (which never held it; grep for "a copy is a place" on ff788172 exits 1) to 2e615bb5:47. (b) EG.62 strikes the EG.39 aside "the director BANKED it as a [rule]": at eef31410a no rule line exists in the director card, skills/ or .agi/context/ (git grep exits 1), so the bullet now says OWED and names nothing as banked. Verdict unchanged at inconclusive_lean_proved:70. Prior DH.621 reasoning has NO grid version: `git for-each-ref refs/grid/` holds 0 refs for mint e6bfe831, because neither 056aac2ce nor 11a2fd3ce ran `grid.py commit`; it is readable at `git show eef31410a:.agi/nodes/experiment/a00-e0efd9fc-a8cf4c.md`. EG.89 (corrective DH.EG.89, text only): this pointer corrected; it named a grid version that does not exist.
<!-- THOUGHT:END -->

## Agent Notes
DH.621 text-only: dead hypothesis:...:67 citation struck DEAD on all three citing nodes (48 lines, 0 hits), 2e615bb5's gate probe replaced with its own pasted three-hit grep, 2e615bb5 demoted proved->inconclusive_lean_proved:55 (self-evidenced), 949eaa34 delta status stated once, items 1/4/5 settled by pasted diffs, ff788172 bullet landed at THREE, counting rule's template home named; zero code bytes.
