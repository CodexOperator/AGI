---
id: hypothesis:l3w4-push-further-loops
mint_id: 8244d4b5b1f549c793021ba5d65e304a
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: belam-S1-L3-XI
scaffold_hash: a89f65b899623a39
season: 2
testable_claim: "cli.py done accepts an optional --push-further TEXT that stamps push_further: TEXT on the target node through the same write --next-edge uses for next_edges, zoom.py's shared completion_contract() reports push_further as one more optional DONE-contract line on both harnesses, and dispatch.py's new --push-further flag refuses to spawn (exit 2, no spawn_budget lease, no session dir) whenever --target names a node of type overview, vision, or moral, but otherwise threads the flag into zoom_command so _compose_small prepends the target's push_further text to the continuation kid's context and stamps the newly scaffolded node's frontmatter pushed_from: <target> — so a push-further chain can re-dispatch at the same target id through kid/parent/director tiers but is mechanically refused the instant it would auto-continue into quorum-judged territory."
thought_session: belam-S1-L3-XI
title: Push further, stop at the quorum
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-push-further-loops

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## CLAIM

`zoom.py::completion_contract()` gains one DONE-contract line,
`push_further: <text>`; `cli.py done` gains `--push-further TEXT`, stamping
`push_further: TEXT` via the write `--next-edge` uses for `next_edges`;
`dispatch.py --push-further --target <id>` refuses to spawn
(exit 2, no lease, no session dir) when `<id>`'s type is
`overview`/`vision`/`moral`, else passes it to `zoom_command` so
`_compose_small` prepends `<id>`'s `push_further` text to the continuation
kid's context and stamps the scaffolded child `pushed_from: <id>`.

## WHY

Owner (7): "each successive hypothesis and experiment... push it as far as
possible, rather than just far enough to prove a verdict"; "...if it can be
pushed further, loop it again"; "...stopping at
quorum unless it needs Belam's input." `idea:push-further`: "a push-further
field... the layer above answers continue or stop." Owner (8): work is
"atomic, recursive, reusable" — `pushed_from` is that trace.

## FILES

- extensions/agi/bin/zoom.py :: completion_contract L89, _compose_small L566
- extensions/agi/bin/cli.py :: cmd_done L312, _append_verdict_to_node L685, "--next-edge" L805
- extensions/agi/bin/dispatch.py :: argparse L542, zoom_command L96, _scaffold_node_for_agent L1642
- extensions/agi/bin/brief.py :: _parent L839 (review step 3)
- .agi/context/schemas/[hypothesis].md :: fields:
- .agi/nodes/idea/push-further.md — source
- extensions/agi/tests/test_dispatch.py — one new test

## DESIGN (director proposal)

- `[hypothesis].md` `fields:` += `push_further: {type: str}`, optional —
  `dsl.py::validate` only checks `required`/`types`/`regex`, never rejects an
  undeclared field, so `write.py <id> set push_further ...` works on any
  type; hypothesis is the one documented.
- `cli.py done --push-further TEXT` (default None) → `_append_verdict_to_node`
  gains `if push_further: set_fm["push_further"] = push_further`, same
  `node_writer.update_node` call as `--next-edge`; `completion_contract()`
  reports it as one optional line after `struggles:`, and pi's branch shows
  the flag on its done command.
- `zoom.py --push-further` (default off): `_compose_small` inserts `"PUSH
  FURTHER (left on {target}): {text}"` above "Extend or fork from `{target}`"
  when the target's frontmatter carries it.
- `dispatch.py --push-further` (default off), checked before the per-slot
  loop: target type in `{overview,vision,moral}` → ERR, exit 2, no
  lease, no session dir; else appended to `zoom_command`, and
  `_scaffold_node_for_agent` gets `extra_fm={"pushed_from": target}`,
  printing `push-further: {target} -> {node_id}`.
- `brief.py::_parent()` step 3 gains one sentence: read a kid's
  `push_further`; continue by re-dispatching `--target <same-id>
  --push-further`; stop by leaving the field as the record.

## TESTS (red-first)

One: `test_dispatch_push_further_refuses_overview_continues_below` —
`--push-further --target overview:fixture` exits 2, no lease, no session dir;
`--push-further --target hypothesis:fixture` (frontmatter `push_further:
"widen the retry window"`) scaffolds a child stamped `pushed_from:
hypothesis:fixture` and prints the `push-further:` line.

## GATE

Test green. Manual: `cli.py done ... --push-further "text"` stamps the field;
`zoom.py --target hypothesis:x --level small --push-further` prints `PUSH
FURTHER` above "Extend or fork from". Suite green; no live spawn.

## NOT IN SCOPE

Quorum vote tally (`l3w4-quorum-reviews`); rotation alarms
(`l3w4-seat-rotation-loops`); rendering push counts
(`l3w4-telemetry-seat-status`); the Bug Master seat
(`l3w4-bug-master-seat`); `--next-edge`'s replace-not-append gap
(pre-existing, untouched).

## SOURCE

`.agi/context/l3-command-ladder-brief.md`, owner verbatim (7)/(7b) (Belam III)
and (8) (Belam IV). `idea:push-further`.

YOU HOLD A BRANCH — READ THIS BEFORE ANYTHING ELSE (Belam XI, L3.43, 2026-09-08). You were dispatched with `--branch`, so you are in your own git worktree on your own `loop/...@s2` branch. **COMMIT YOUR KID'S WORK TO THAT BRANCH BEFORE YOU EXIT.** From inside your worktree:

    git add -A
    git commit -m "L3.43 <your agent id>: <what landed>"

MEASURED TWICE NOW, INCLUDING THE ROUND IMMEDIATELY BEFORE THIS ONE: every `--branch` parent so far has exited with its branch at ZERO commits ahead, `season.py merge-up` then merged an empty branch and REPORTED GREEN, and a human had to harvest the work by hand from inside the worktree. A round that ends with your branch empty has produced nothing as far as every automated reader is concerned. You are the live proof that this can work — see `hypothesis:l3-parent-brief-forbids-the-only-commit`.

Do NOT push. Do NOT merge. Do NOT touch `season/s2`. The director merges. Commit locally on your own branch, that is all.

Run on pi/OpenRouter. Your kid: `python3 extensions/agi/bin/dispatch.py . L3.43 --target <this node> --level small --tier kid --harness pi`. Do NOT run `workflow.py run` for any reason this round.
