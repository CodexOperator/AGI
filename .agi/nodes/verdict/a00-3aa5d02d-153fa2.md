---
id: verdict:a00-3aa5d02d-153fa2
mint_id: a6cc1b69693748758aba617a8f15dd42
type: verdict
parents:
  - experiment:a00-17ab468d-05e2a2
next_edges: []
confidence: 0.85
edited_by: a00-3aa5d02d
evidence_runs:
  - experiment:a00-17ab468d-05e2a2
loop: experiment:a00-17ab468d-05e2a2@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 952d39a3738b82a3
season: 2
title: "DH.478: the DH.474 probes on a00-17ab468d did not reproduce, so they were replaced with two that do"
town: core
verdict: proved
---
# verdict:a00-3aa5d02d-153fa2 — the DH.474 probes on this node did not reproduce; replaced with two that do

## What was judged

`experiment:a00-17ab468d-05e2a2` was cut for a corrective, node-wording-only slice. The engine
review (mur-director-engine-12, review+verify DH.474-k1, accept_with_residue) named four
residues. This round claims the four, on that one node, by `write.py` only.

| # | residue | what the bytes said before | what they say now |
|---|---|---|---|
| 1 | probes do not reproduce | four bullets citing `grep -cE` over a node id as if it were a path, and outputs describing a different file than the command | two probes, each with the exact command, each re-run after the last edit and pasted raw |
| 2 | THOUGHT duplicated the review | the DH.474 THOUGHT was a verbatim second copy of the review paragraph below it, with line numbers measured pre-edit | rewritten from scratch; the ONE review copy outside the block is untouched; no line numbers cited |
| 3 | rebrief unanswered | `rebrief_request` OPEN | `rebrief_answer: resolved: landed 2d648bf26; no new kid needed` |
| 4 | production_lines | `2` on a node-only round | `0`, and the Evidence line no longer calls a node diff production lines |

## Evidence (measured on the final bytes, not asserted)

| probe | command | result |
|---|---|---|
| (a) user name, three nodes | `for f in …; do grep -niF "$(id -un)" .agi/nodes/experiment/$f.md; echo "exit=$?"; done` | 0 hits, `exit=1` ×3 |
| (b) home-directory prefix | `grep -n "/home/" <the same three paths>` | 8 hits, exit 0, each listed `file:line` in the node's own table with its classification |
| suite | `python3 -m pytest extensions/agi/tests/test_boxkit_probe.py extensions/agi/tests/test_mem_cap_tasks_max.py -q --basetemp /tmp/a00-dh478` | `35 passed in 23.59s` (no code changed; `--timeout` is not installed here, so it was dropped) |

**No real home path value survives in any of the three nodes.** Every `/home/` hit is the
literal second half of a quoted grep pattern or a sentence describing it. Nothing needed
redaction; no line was deleted. The user name is written only as the shell expansion
`$(id -un)`.

## What this proves, and what it does not

Proved: the node's recorded probes now follow from their recorded commands, the THOUGHT is
this version's own reasoning, the rebrief is answered, and the round's line accounting says
NODE edit / 0 production lines. Disproved: that the DH.474 probe block, as recorded, was
evidence — a `grep -cE` over a node id is not a runnable command, so its "0 hits, exit 1" was
unbacked even though the underlying conclusion happened to hold.

Not established, and out of scope: anything about the rest of the graph, the history-rewrite
residue (director's), or whether `anonymize.py check` would ever catch a user name — it does
not look for one.

## Caveat carried upward

A self-matching gate is still a defect in the ORDERS, not in any node: a node that documents
its own grep pattern can never return exit 1 for that pattern. The next slice should stop
recording the pattern literally in the node that is being scanned.

## Agent Notes
DH.478 corrective slice on a00-17ab468d-05e2a2: replaced the four non-reproducing DH.474 probes with two re-run probes (user name 0 hits exit 1 on each of the three nodes; 8 /home/ hits each classified, no real path value), rewrote the duplicated THOUGHT, answered the rebrief (2d648bf26), production_lines 0; suite 35 passed.
