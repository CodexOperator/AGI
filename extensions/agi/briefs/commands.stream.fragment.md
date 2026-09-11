---
id: command:commands
type: frag
parents:
  - hypothesis:l4-towns-each-app-is-a-vision-with-its-own-council
edited_by: a00-7f9e3d95
season: 2
frag_kind: commands.stream
title: "The stream command group — sb-status, brb, back, panic — resolved from locations.streamer_stub"
---
<!-- BODY:BEGIN -->
# commands.stream.fragment — the stream commands become our commands

A **Prime-landed** fragment for `command:commands`
(`.agi/nodes/.geometry/commands.md`). This round does not edit the geometry
node; the Prime folds this `commands:` group in at merge-up. The
`argv`/`about`/`workflow` shape is copied from the live commands block in
`.agi/nodes/.geometry/commands.md` (frontmatter `commands:` entries, read at
iteration L4.117); every entry here matches it cell for cell.

## The `stream` group to add under `commands:`

Each command's argv resolves its stub path from a configurable
`locations.streamer_stub` (default `~/work/streamer-stub`, resolved by the
test that reads this fragment to `/home/ubuntu/work/streamer-stub`); the
`<stub>` token is substituted at resolve time the way `<root>` and `<engine>`
already are in `commands.py`. `<stub>` is the stub DIRECTORY, so the argv
that reaches a mode is `<stub>/bin/<script> <flag>` — never `<stub>` alone
(that is a directory, not an executable) and never `<stub>/bin/hold.sh brb`
(hold.sh dispatches on `argv[0]`'s basename via `case "${0##*/}"`, so a bare
`hold.sh` basename falls through to the usage error instead of pausing). The
four commands pass the measured explicit flags: `sb-status`
=`hold.sh --status`, `brb`=`hold.sh --pause`, `back`=`hold.sh --off`,
`panic`=`panic.sh` (no flag = the hard cut). None of them is ever executed
by these fragments; they are declarations for the operator table and
`commands.py run`.

```yaml
  sb-status:
    argv:
      - <stub>/bin/hold.sh
      - --status
    about: the streamer stub's live status (the stream is LIVE; read-only status reporting)
    workflow: read
    owner_only: false
  brb:
    argv:
      - <stub>/bin/hold.sh
      - --pause
    about: pause the streamer — operator sets the stub to be-right-back
    workflow: see
    owner_only: false
  back:
    argv:
      - <stub>/bin/hold.sh
      - --off
    about: resume the streamer after brb — operator brings the stub back to live
    workflow: see
    owner_only: false
  panic:
    argv:
      - <stub>/bin/panic.sh
    about: OWNER-ONLY — full emergency stop of the streamer
    workflow: see
    owner_only: true
```

## `panic` is owner-only and is REFUSED for every other actor

`panic` is marked owner-only in the node and must be **refused** for any
other actor. This is a declaration, stated here so it is true at the config
layer even before the runner enforces it:

> **REFUSAL: any actor who is not the owner requesting `panic` is refused.**
> The stream is LIVE; `panic` halts it and is never executed by a kid, a
> test, or a non-owner operator. `commands.py run` gates `panic` on the
> caller being the owner because the entry declares `owner_only: true` — any
> other actor gets a machine-readable `REFUSED: ... owner_only` message and a
> non-zero exit, with nothing executed (the refusal happens before any
> subprocess call). These fragments never run it either — not even a dry run.

`sb-status` reads stream health; `brb` and `back` are the operator's
pause/resume pair. They are the two "hands" the stub exposes that are not
destructive. `panic` is the one that is.

## What the Prime must run to land this (and its residue)

Land `config:seats` with the council rows and `town` cells from
`seats.councils.fragment.md`, and fold this `stream` group into
`command:commands`. The exact `write.py` create/set lines are in
`experiment:a00-7f9e3d95-7b55f6`.

**Code residue landed after this round, plainly named:** the commands.py
runner change that (a) resolves `<stub>` from `locations.streamer_stub` and
(b) gates `panic` on owner (`owner_only: true` field, refused before any
subprocess call for a non-owner actor) — landed in this round.
<!-- BODY:END -->
