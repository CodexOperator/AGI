---
id: hypothesis:a-draft-mints-one-checked-row-per-call
mint_id: 434328e116764436a8ecc0064d83001f
type: hypothesis
parents:
  - goal:g4.18.1.2
next_edges: []
edited_by: director-engine
scaffold_hash: 064f3bc3a3479845
season: 2
testable_claim: write.py draft open|set|mint fills one schema-checked row per call from stdin or a file and mints through the same code as create --answers; a refused row leaves the draft unchanged
title: "A draft mints one checked row per call: open / set <row> - / mint over one answers file (EG.4, assigned: director-engine)"
town: core
---
# hypothesis:a-draft-mints-one-checked-row-per-call

## Why this exists
belam [decision] 00:0xZ 09-28 (owner, verbatim on town:local-maxxing): "NEXT, in dependency order: g4.18.1.2 captive mint flow -> the send pipeline core (g7.32.6) -> rotate core (g7.31.3.3)". goal:g4.18.1.2 (owner 09-26): "Why can't minting just use the write function one step at a time as a captive flow the models follow? Each row filled out and format checked."

## Measured
- The g4.18.1.1 chain tip 1e74cea4b (season2/loops/hypothesis-one-mint-route-answer-a00-31004c15; corrective DH.660 queued) already has `write.py create --answers PATH` (write.py:3123) and a per-row refusal `_answers_row_refusal` (write.py:1947-1965): the validator exists; no step-by-step DRAFT flow does.
- A model composing one long `create` argv makes quoting errors (goal:g4.18.1 Evidence 09-26).

## CLAIM
`write.py draft` is a captive, resumable flow over ONE draft file: `draft open <type> <slug> --parent <id>...` writes the draft and prints the first row to fill with its legal shape; `draft set <draft> <row> -` (value from stdin, or `--from FILE`) validates that ONE row through the same row validator `create --answers` uses and, on success, writes it and prints the next row; `draft mint <draft>` mints through the SAME code path as `create --answers` (the draft IS an answers file). No step reads a row value from a shell-quoted argv position.

## Dispatch line
config-max: the row order and each row's legal shape come from the type's schema (.agi/context/schemas/[<type>].md), never a code literal · template-max: the "next row" prompt text is one template line · code: the three verbs over the existing answers path.

## FALSIFIERS
1. A scripted run of open + one set per row + mint mints a hypothesis whose bytes equal the same mint from a hand-written answers file (exit 0 both).
2. A `set` with a value the schema regex refuses exits non-zero and leaves the draft byte-identical.
3. An abandoned draft mints nothing and blocks no other mint of the same slug.

## TESTS
New extensions/agi/tests/test_write_draft_flow.py (falsifiers 1-3, tmp graphs only) + the g4.18.1.1 answers tests on that tip + test_bin_help_smoke.py (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE).

## FILE SCOPE
extensions/agi/bin/write.py (the draft verbs, reusing the answers path) · the new test file · the kid's own node

## CEILING
HARD CAP: 1 kid · <= 60 production lines net · <= 80 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut.
BASE: cut from the g4.18.1.1 chain tip AFTER DH.660's mur clears (dependency: this flow calls that validator), never from the post branch.
PARENT: paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit.
