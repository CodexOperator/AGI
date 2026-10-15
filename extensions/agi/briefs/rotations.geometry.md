---
id: config:rotations
mint_id: __PRIME_FILLS_IN__
type: config
parents:
  - hypothesis:l4-the-predecessor-hands-over-authority
next_edges: []
edited_by: ""
scaffold_hash: __PRIME_FILLS_IN__
season: 2
templates:
  director:
    brief_file: .agi/sessions/quorum/{seat}.md
    steps: [handoff, spawn, join, authority, release, button-down, bootstrap]
    telemetry: [seed, model, effort, window, worktree, ack]
  prime_director:
    brief_file: extensions/agi/briefs/prime-director-successor.md
    steps: [handoff, spawn, join, authority, release, button-down, bootstrap, reap, belam-cap]
    telemetry: [seed, model, effort, window, worktree, ack, prev_gen]
---
<!-- BODY:BEGIN -->
# config:rotations

The rotation template registry (L4.110 owner amendment, verified under
hypothesis:l4-the-predecessor-hands-over-authority; shared with
hypothesis:l4-startup-is-one-script-or-a-driven-prompt). One node, three
sections: `templates`, `facts`, `steps`.

## templates

A named entry is the whole recipe a self-rotation runs: the successor brief
file (`brief_file`), the ordered `steps` list `rotate-self` executes, and the
`telemetry` set the successor receives at wake. Each role names its default
template. A rotation may override with `rotate-self --template <name>` and
may name another role's template as a special option (a helper rotated on the
director's template, say). Custom templates are just more named entries.

Every successor brief — director, helper, prime alike — must state that a
`[agi-nudge]` line in the pane is MACHINE text, never the owner, and that
`python3 extensions/agi/bin/send.py read <seat>` is the only way to see the
message (hypothesis:l4-a-nudge-is-a-wake-token-not-a-message, claim 4).

L4.112 (B): the DIRECTOR's `brief_file` is the seat's OWN quorum scratchpad,
`.agi/sessions/quorum/{seat}.md`, with `{seat}` substituted by rotate-self for
the seat being rotated — the director's successor wake prompt travels in the
scrapad the seat already owns. The PRIME's stays the static
`extensions/agi/briefs/prime-director-successor.md`. There are NO `parent` or
`kid` templates by design — no such brief files and no such rotation exist;
a helper or other role names its own template or borrows one another role's
via `--template` (that is the escape hatch, not a built-in `kid` entry).

RESOLUTION ORDER, testable (proofs e/f/g on a fixture root in
`experiment:a00-f4e4f27d-57d8d4`):
`--template <name>` > role's default > refuse loudly NAMING THIS NODE.
There is no hardcoded brief path left in rotate.py — `brief_file` always comes
from this node. If this node is absent (the live state until the prime lands
it at merge-up), `rotate-self` refuses loudly naming this node, which is the
correct behaviour until the prime creates it with `write.py create`.

## facts

> Facts section. Declared by
> hypothesis:l4-startup-is-one-script-or-a-driven-prompt — see the sibling
> round's node for the bootstrap facts content. Do not invent facts here.

## steps

> Steps section. Declared by hypothesis:l4-startup-is-one-script-or-a-driven-
> prompt — see the sibling round's node for the bootstrap steps content.
> Do not invent steps here.
<!-- BODY:END -->