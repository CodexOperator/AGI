---
id: config:rotations
mint_id: ee0148fe1f4d4244aa2527dc961bdd20
type: config
parents:
  - hypothesis:l4-the-predecessor-hands-over-authority
next_edges: []
edited_by: belam-S1-L4-VI
locations: {}
scaffold_hash: c15eeda9b6db679a
season: 2
spawn_check: unverified
spawn_check_reason: no active schema for type 'config'
templates:
  director:
    brief_file: .agi/sessions/quorum/{seat}.md
    steps:
      - handoff
      - spawn
      - join
      - authority
      - release
      - button-down
      - bootstrap
    telemetry:
      - seed
      - model
      - effort
      - window
      - worktree
      - ack
  prime_director:
    brief_file: extensions/agi/briefs/prime-director-successor.md
    steps:
      - handoff
      - spawn
      - join
      - authority
      - release
      - button-down
      - bootstrap
      - reap
      - belam-cap
    telemetry:
      - seed
      - model
      - effort
      - window
      - worktree
      - ack
      - prev_gen
thought_session: belam-S1-L4-VI
title: "Rotation templates — one node, three sections: templates, facts, steps"
---
<!-- BODY:BEGIN -->
# config:rotations

The rotation template registry (owner amendment 2026-09-10, verbatim in
`doc:l4-owner-decisions`: "rotations should be config maxxed so you can choose
templates"; built under `hypothesis:l4-the-predecessor-hands-over-authority`
(L4.110), shared with `hypothesis:l4-startup-is-one-script-or-a-driven-prompt`).
One node, three sections: `templates` (frontmatter), `facts`, `steps`.
Type `config`, written by the owner or the prime only — a template drives every
successor's wake brief, which is authority, the same class as `config:seats`.
Created by the Prime L4-VI at merge-up 19 from the body L4.110 shipped, with the
point's two measured corrections: the director template's `brief_file` is the
seat's quorum scratchpad `.agi/sessions/quorum/{seat}.md` (`{seat}` substituted
by `rotate-self`; the shipped `briefs/director-successor.md` did not exist), and
the `parent` / `kid` entries were dropped (no such rotation exists and their
briefs did not exist either).

## templates

A named entry is the whole recipe a self-rotation runs: the successor brief
file (`brief_file` — a path under the repo root; `{seat}` is the rotating
seat's name), the ordered `steps` list `rotate-self` executes, and the
`telemetry` set the successor receives at wake. Each role names its default
template. A rotation may override with `rotate-self --template <name>` and may
name another role's template as a special option (a helper rotated on the
director's template, say). Custom templates are just more named entries.

RESOLUTION ORDER, testable (proofs on a fixture root in the L4.110 experiment
node): `--template <name>` > the role's default > refuse loudly NAMING THIS
NODE. There is no hardcoded brief path left in `rotate.py` — `brief_file`
always comes from this node. If this node is absent, `rotate-self` refuses
loudly naming this node; from the moment L4.110's code is on `season/s2` this
node must exist there too, which is why the Prime created it BEFORE merge-up 19
rather than in the same window. The resolution must run BEFORE any side effect
(handoff write, window rename) — L4.112 moves it there.

## facts

> Declared by `hypothesis:l4-startup-is-one-script-or-a-driven-prompt` (0b) —
> the bootstrap facts a successor is handed instead of reading the handoff.
> Empty until 0b lands; do not invent facts here.

## steps

> Declared by `hypothesis:l4-startup-is-one-script-or-a-driven-prompt` (0b) —
> the bootstrap steps. Empty until 0b lands; do not invent steps here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Created by the Prime L4-VI on 2026-09-10 (date -u 22:5xZ) ahead of merge-up 19, because L4.110's rotate.py refuses every rotate-self while this node is absent: creating it before the code lands decouples the two and keeps every seat rotatable in between. Body and templates are L4.110's shipped extensions/agi/briefs/rotations.geometry.md with the point gen VIII's two measured corrections (director brief_file = the quorum scratchpad with {seat}; parent and kid entries dropped). The file was moved from nodes/config/ to nodes/.geometry/ because that is the address rotate.py resolves (same as config:seats); the mint id is unchanged. spawn_check unverified is the gate's honest stamp: it found no active spawn rule for type config.
<!-- THOUGHT:END -->
