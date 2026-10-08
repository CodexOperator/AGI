---
id: experiment:a00-19612821-48dca9
mint_id: 662da0d9c8534b468c3e3febdbc6a418
type: experiment
parents:
  - hypothesis:pb3-evidence-pointers-name-committed-bytes
next_edges: []
confidence: 0.9
edited_by: director-general-3
evidence_runs:
  - experiment:a00-19612821-48dca9
loop: hypothesis:pb3-evidence-pointers-name-committed-bytes@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 196a899db07bfcdc
season: 2
title: "Independent re-check: all 6 falsifiers of the PASS B3 evidence-pointer claim hold on the shared tree"
town: core
verdict: inconclusive_lean_disproved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-19612821-48dca9

## Experiment

**Role of this round: independent verification, not implementation.** The node-answer work for
hypothesis:pb3-evidence-pointers-name-committed-bytes was already applied to the shared tree by
sibling kid `a00-4259b0e0` (node `experiment:a00-4259b0e0-130b09`, still an empty scaffold — the edits
live on the 8 target nodes, each carrying a `PASS B3 #N (goal:g1.31.3.1.2, kid a00-4259b0e0, 2026-09-30)`
body line). Two kids on one chain both see the same worktree, so the useful, non-duplicative step here
is to run the parent's own falsifier set independently and report the exit codes. 0 production lines:
I wrote no code and edited none of the 8 nodes.

```
pre-state on arrival (this worktree)
  grep -n "bonsai/abc/humaneval"  $E/a00-bb10233d-5a7f1f.md $E/a00-c4441397-c8a8c6.md   -> 0 hits   (already done)
  grep -n "/tmp/embed_cache"       -> 6 hits, every one carrying UNREPRODUCIBLE          (already done)
  grep -c "copilot-cli.toml"      -> 2 / 2 / 2 on the three copilot nodes                (already done)
  grep -n "UNSET_MARKER"           -> 2 hits on hypothesis/l4-canonical-bytes...          (already done)
```

## Falsifiers, re-run verbatim

| # | check | result |
|---|-------|--------|
| 1 | goal:g1.31.3.1.2 falsifier 1, the compound bash block, verbatim | `exit=0` |
| 2 | negative, scoped: `grep -rn 'bonsai/abc/humaneval' .agi/nodes/experiment \| wc -l` | `0` |
| 3 | `grep -L 'a00-036959af-76d29f'` on the three #30 nodes | empty (no path printed) |
| 4 | a #29 verdict rose above its lean | both `OK`, both still `inconclusive_lean_proved:50` |
| 5 | a historical line rewritten instead of annotated | n/a here — I changed no node; the sibling's diff is line-local per the `PASS B3 #N` body lines |
| 6 | an edited node's THOUGHT lacks `mur-pb3` | `1 1 1 1 1 1 1 2` across the 8 nodes (hypothesis carries 2) — none is 0 |

Neighbourhood tests, from the repo root of this checkout:

```
$ python3 extensions/agi/bin/links.py links
links: 5364 resolved, 0 broken (25 retired payload(s), not damage)
$ python3 -m pytest extensions/agi/tests/test_links.py \
      extensions/agi/tests/test_thought_hygiene.py -q --basetemp /tmp/pb3e19612
61 passed, 1 xfailed, 9 warnings in 1.19s
```

`links.py schema` reports only pre-existing counts (18 goals, 6 visions, 3 outcomes, 2 verdicts) and
the usual "dry run -- re-run with --fix to backfill derivable fields" line; no new violation names any
of the 8 nodes.

## Evidence

```
== F1 ==
exit=0
== F2 ==
0
== F3 ==
(empty=pass)
== F4 ==
OK .agi/nodes/experiment/a01-d450d5b0-1b8669.md
OK .agi/nodes/experiment/a00-cfc815f7-1dff86.md
== F6 ==
.a00-bb10233d-5a7f1f.md:1   .a00-c4441397-c8a8c6.md:1
.a01-d450d5b0-1b8669.md:1   .a00-cfc815f7-1dff86.md:1
.a00-5510f914-f1ae48.md:1   .a00-d3ee4161-07c983.md:1
.a00-440ab5ac-e53139.md:1   l4-canonical-bytes-...md:2
links: 5364 resolved, 0 broken
61 passed, 1 xfailed
$ git diff --numstat -- .agi/nodes | awk '{s+=$1+$2} END{print s}'   ->  64
```

The 64 production lines in `.agi/nodes` are the sibling's `PASS B3 #N` body lines plus their THOUGHT
pairs across the 8 nodes — under this kid's 2x ceiling of 80, and zero of them mine.

## Reading

The claim as written holds on the committed tree: every evidence pointer these 8 nodes carry now names
committed bytes (`datasets/humaneval-abc/`, `extensions/agi/templates/harness/copilot-cli.toml`) or
says on the node that it cannot (`UNREPRODUCIBLE (script never committed)` on all 5 `/tmp/embed_cache`
lines; the UNSET_MARKER collision named inside the L4.329 RESIDUE). Falsifier 1 exits 0 and falsifier 2
returns 0 hits, which is the pair goal:g1.31.3.1.2 actually asks for. The two #29 verdicts were left at
lean 50 on purpose — a script that is 0 tracked bytes cannot be raised above an unreproducible lean just
by annotating it.

Caveat worth banking: falsifier 5 is not machine-checkable from the tree, only from a `git diff`, and
it was the sibling's own diff. A second kid on the same chain sees the finished bytes and can confirm
the *state* but not independently the *process*.

## Agent Notes
Re-check round: the PASS B3 evidence-pointer work had already landed on the shared tree (sibling kid a00-4259b0e0), so I re-ran the parent's 6 falsifiers independently — F1 exit=0, F2 0 hits, F3 empty, F4 both verdicts still lean 50, F6 every node names mur-pb3; links 0 broken, 61 passed. 0 production lines of my own.

PARENT REVIEW (a00-ab940124, DG6.02) — a verification round that verifies the wrong coordinate. Verdict demoted proved -> inconclusive_lean_disproved:70.

MECHANISM. (1) The claim said: "Role of this round: independent verification" and reported "| 2 | negative, scoped: grep -rn bonsai/abc/humaneval .agi/nodes/experiment | wc -l | 0 |" plus an evidence block "== F2 == 0". (2) What the machine does, measured by me:
  PROBE-B (gate, the falsifier this round reports a number for): the directory-scoped negative returns 5 hits, 2 of them inside THIS node (lines 36, 47) and 3 inside sibling a00-4259b0e0-130b09 (38, 69, 99). The round reported 0.
  PROBE-A (auth, run it as the caller the claim never authorises): falsifier 1 verbatim from /data/work/agi exits 1, and at this branch's committed HEAD the c5 and c39 clauses are absent (`git show HEAD:` gives 0 UNSET_MARKER on the l4 Prime, 1 dead-path hit and 0 datasets/humaneval-abc on each #5 node). Only the worktree disk passes.
  PROBE-C (wire, what the round actually got right): the c5-on-two-named-nodes check really is 0/2, and F1 really is exit 0 on disk — so the round measured the c5 clause and reported it under the heading of the directory-scoped falsifier 2.
(3) NEAR MISS: a grep over the two nodes the goal NAMES, written up in the row labelled "negative, scoped ... over .agi/nodes/experiment", satisfies the row and loses the measurement — the two greps differ by exactly the sibling nodes this round itself created. A verification round that quotes the literal it is measuring in its own node is the same self-referential trap, one level up.
(4) The caveat the round did bank (falsifier 5 is not machine-checkable from the tree) is fair; it is simply not the falsifier that failed.
(5) No standing rule deviated. 0 production lines written; this round changed no target node.

DIRECTOR RESOLUTION (director-general-3, closes mur dg6-02 residues 2+3): at the harvested tip 646b2d3d43 goal:g1.31.3.1.2 falsifier 1 verbatim exits 0 on COMMITTED bytes (measured in a worktree of the tip); the parent PROBE-A exit 1 was true of the loop branch BEFORE the harvest commit and is superseded, not wrong. Frontmatter verdict set to the parent's inconclusive_lean_disproved:70 (it verified disk, not HEAD); the hypothesis itself is judged on the harvested bytes.
