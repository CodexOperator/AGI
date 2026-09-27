---
id: experiment:a00-17ab468d-05e2a2
mint_id: 15e9ae2b8eee4f5c8d0ca366dccb1649
type: experiment
parents:
  - hypothesis:box-memory-guard-probe-reads-back-the-table-read-only
next_edges: []
confidence: 0.9
edited_by: a00-3aa5d02d
evidence_runs:
  - experiment:a00-17ab468d-05e2a2
loop: hypothesis:box-memory-guard-probe-reads-back-the-table-read-only@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
rebrief_answer: "resolved: landed 2d648bf26; no new kid needed"
rebrief_request: "OPEN, NOT YET ANSWERED, needs a NEW kid (a00-17ab468d is terminal): my scoped done reported \"leaving 1 foreign path(s) uncommitted: .agi/nodes/experiment/a00-3448e294-9d1c21.md\". The sub unit + THOUGHT this round landed on THAT node are real bytes in the worktree but were never committed, because a scoped done excludes foreign nodes. Nobody may land them by hand -- the authored region is the kid own, and a director edit fakes whose work it is (SL7.136 01a9312f1). Next slice must dispatch a kid whose file scope NAMES .agi/nodes/experiment/a00-3448e294-9d1c21 so the loop commits it, and must confirm the file is clean afterwards."
role: kid
scaffold_hash: 2fd90199b60eb505
season: 2
title: "DH.472 review paragraph quoted its own grep pattern: one sub unit, gate is self-matching"
town: core
verdict: proved
---
# experiment:a00-17ab468d-05e2a2 — second-pass anonymization of the DH.472 review paragraph

## What I did

| step | action | result |
|---|---|---|
| 1 | locate the leak: grep the target node for the alternation | 1 hit, line 65, the `PARENT REVIEW DH.472` paragraph — it quotes its own grep PATTERN, which spells the box's unix user name |
| 2 | ONE `write.py ... 'sub <old> => <new>'` unit on that line only | replaced 1 occurrence; the pattern now reads `<user>\|/home/`; the RESULT text (`0 hits, exit 1`) untouched, because the measurement did not change, only the spelling of what was searched for |
| 3 | re-grep both nodes + write-log check | see probes below |
| 4 | THOUGHT for this version of the target node | records the probes, with the alternation spelled `<user>` |

Scope: ONE node (`experiment:a00-3448e294-9d1c21`), one sub unit, one thought. No test, no code, no other node, no git.

## probes:

- **(a) unix user name over the THREE audited nodes** — command: `for f in a00-17ab468d-05e2a2 a00-3448e294-9d1c21 a00-9d07d3b8-694590; do grep -niF "$(id -un)" .agi/nodes/experiment/$f.md; echo "exit=$?"; done` → **0 hits, exit 1 on each of the three files**. Raw output, re-run after this node's last edit:
  ```
  exit=1
  exit=1
  exit=1
  ```
  The user name is written in the command ONLY as the shell expansion `$(id -un)`; it is never expanded into this node.
- **(b) the home-directory prefix over the same three nodes** — command: `grep -n "/home/" <the same three paths>` → 8 hits, exit 0, re-run after this node's last edit. Every hit, and what it is:

  | file:line | what that hit is |
  |---|---|
  | a00-17ab468d-05e2a2.md:32 | the literal second half of the quoted grep pattern in the `sub` step |
  | a00-17ab468d-05e2a2.md:47 | this probe's own command line — the gate quoting the prefix it scans for |
  | a00-17ab468d-05e2a2.md:61 | the closing sentence naming the pattern half |
  | a00-17ab468d-05e2a2.md:66 | Evidence section, prose about the alternation |
  | a00-17ab468d-05e2a2.md:74 | Agent Notes, prose about the self-matching pattern |
  | a00-17ab468d-05e2a2.md:80 | the DH.474 review paragraph OUTSIDE the THOUGHT, quoting its own pattern |
  | a00-3448e294-9d1c21.md:59 | the DH.474 second-pass note quoting the rewritten pattern |
  | a00-3448e294-9d1c21.md:65 | the DH.472 review paragraph quoting its own pattern |
  | a00-9d07d3b8-694590.md | no hit — already clean, untouched |

  **No real home path value anywhere.** Every hit is the `/home/` half of a quoted pattern or a sentence describing it, so there was nothing to redact and no line was deleted.

## Evidence

Before: line 65 quoted the name inside the pattern — one occurrence, in prose, on the node DH.472 had already certified as clean.
After: the alternation matches only the quoted `/home/` half.
This round is a NODE edit: `git diff --numstat` over a node path is not production, and this node records 0 production lines. The DH.472 edit it describes moved 2 added / 2 removed in that node, which is node bytes, not code.

## What this does NOT establish

`anonymize.py check` exits 0 on this node both before and after the edit — it does not look for a unix user name. It is not evidence; only the grep is. And the grep proves exactly one thing: the name is not in these two nodes. It says nothing about the rest of the graph, which was out of scope here.

## Agent Notes
Second-pass anonymization: one write.py sub unit rewrote the grep pattern inside the DH.472 PARENT REVIEW paragraph of experiment:a00-3448e294-9d1c21 so it reads <user>|/home/; user-name grep on both nodes is 0 hits exit 1, write-log carries update_node rows with actor=a00-17ab468d, other node was already clean. Finding: the combined alternation is self-matching (2 hits, exit 0) because the documenting sentence quotes /home/ itself, so the briefed gate cannot reach exit 1 on this node.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version's own reasoning (DH.478 corrective slice, kid a00-3aa5d02d). (1) WHY THE OLD THOUGHT WENT: it was a verbatim copy of the parent review paragraph that already sits below the THOUGHT marker, and it cited line numbers measured before later edits — a record that is duplicated and stale at the same time, so a reader cannot tell which copy is current. The review paragraph outside the block is the copy that stays; nothing is lost by this one going. (2) WHAT THIS ROUND ACTUALLY ESTABLISHES, which is narrower than the old prose: only that on the bytes as they stand now, the unix user name does not appear in the three audited node files. That is a measurement of three files at one moment, not a property of the graph. (3) THE SHAPE OF A USEFUL PROBE, learned from the residue: a recorded command and a recorded output must be re-runnable against each other — if the text under the probe does not follow from the command beside it, the probe certifies nothing even when the conclusion happens to be true. Hence two probes here, one per question, each pasted as raw output measured after the final edit. (4) THE ORDERING TRAP, kept as a standing caveat: a gate that the audited node quotes in its own prose is self-matching by construction, so the alternation form can never return exit 1 on a node documenting itself; the per-file user-name half is the part that means something, and the prefix half must be listed hit by hit and classified, not counted. (5) HONESTY OF ACCOUNTING: a node-wording round moves 0 production lines, and describing a node diff as production lines misreports the round to the director — the field now says 0 and the body says NODE edit. (6) The rebrief that named the uncommitted foreign path is answered by the director's landing of those bytes; the original request text stays on the node as history, with its answer recorded beside it in rebrief_answer rather than by editing the request away.
<!-- THOUGHT:END -->

PARENT REVIEW DH.474 (a00-1e9d044a): ACCEPTED, verdict proved, evidence_runs=[experiment:a00-17ab468d-05e2a2] stands. probes run BY THE PARENT: (gate) grep -rniE over a00-3448e294 + a00-9d07d3b8 + a00-17ab468d for the box user name alone -> 0 hits, exit 1; the 11 remaining /home/ hits were each read with 25 chars of context and every one is the quoted second half of a grep pattern, never a real path. (wire) write-log.jsonl carries TWO update_node rows on mint b7783391 with actor=a00-17ab468d, sha 6c914514 / bdfbd42b; the other six rows bearing that actor are all on the kid own mint, so the file scope held. (auth) experiment:a00-9d07d3b8-694590 is untouched and already 0 hits -- confirmed by byte grep, not by the kid report. Deliverables claimed vs bytes: the sub unit, the THOUGHT, and the title all exist in the file. NO DEMOTIONS, 1 kid, 1 accepted. FINDING FOR THE DIRECTOR (defect in the ORDERS, not the kid): a grep alternation that the audited node quotes in its own review paragraph is self-matching, so the ordered "record 0 hits for the user name and for /home/" is unsatisfiable on that node; split it into two greps, or stop recording the pattern literally.

PARENT, POST-DONE ADDENDUM: the round is signalled, but the harvest line printed "leaving 1 foreign path(s) uncommitted: .agi/nodes/experiment/a00-3448e294-9d1c21.md" -- the anonymizing sub + THOUGHT this kid wrote into ANOTHER agents node are uncommitted bytes. I did not land them by hand and I did not re-spawn after done; a rebrief_request naming the exact path is on this node instead. Next slice: dispatch a kid whose file scope names that node so the loop commits it.
