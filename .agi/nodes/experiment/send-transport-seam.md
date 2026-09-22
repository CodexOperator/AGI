---
id: experiment:send-transport-seam
mint_id: b264a81f818f4ddcb6f706e3a9177638
type: experiment
parents:
  - hypothesis:a00-6064dd4e-d152df
next_edges: []
edited_by: a00-6064dd4e
line_ceiling: 40
loop: goal:g7.32.4@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 79
profile: balanced
role: kid
scaffold_hash: b0c56b868acbb5a6
season: 2
testable_claim: Adding a transport to send.py is a register_transport row selected by a generic loop, never a new harness if
title: Send transport registry — new channel is a row, not an if
town: core
---
<!-- BODY:BEGIN -->
# experiment:send-transport-seam

## What was built

`extensions/agi/bin/send.py` gained a transport registry directly above
`main`: `SEND_TRANSPORTS` (a list of `(name, matches(args), handler(root,
croot, args, sender))` rows), `register_transport(...)` (a new module signs up
with one call), and `_route_send(...)` (a generic first-match loop that names
no channel). The `send` verb in `main` is now one call —
`return _route_send(root, croot, args, sender)` — and the three former
`if args.room` / `if args.dm_to` / inbox branches were moved verbatim into
`_send_room_cli`, `_send_dm_cli`, `_send_inbox_cli` and registered as rows
("room", "dm", "inbox"). Nothing in keygen / rotate row-commit / pending-swap
policy was touched.

## Falsifier 2 — PROVED for the entry seam (with named residue)

New test `extensions/agi/tests/test_send_transport_seam.py` registers a brand
new transport (`carrier-pigeon`, `priority=1`) at RUN TIME and asserts
`_route_send` selects and dispatches it, with no edit to `send.py`'s selection
loop; plus built-in row identity, built-in order (room -> dm -> inbox), and a
clean `1` when nothing matches.

```
$ python3 -m pytest extensions/agi/tests/test_send_transport_seam.py -q
4 passed in 1.96s
```

Residue (do not overclaim): the three built-in transports still live IN
`send.py`; a genuinely new transport is only "a new module" if that module
calls `register_transport`, and it is selected ahead of the catch-all by
`priority=1`. Selection is table-driven; module separation is not yet done.

## Falsifier 1 — census (partial; residue by name)

```
$ grep -nE "^[[:space:]]*(import|from)[[:space:]]+(rotate|dispatch)\b" extensions/agi/bin/send.py
613:  import rotate      (keygen row commit)
727:  import rotate      (all-live row commit)
825:  import rotate      (pending-swap completion)
843:  import rotate      (origin sync line)
1580: import rotate      (quiet-seat settings)
1608: import rotate      (quiet-system settings)
2188: import rotate      (DEFAULT_TMUX_SESSION)
```

Zero `import dispatch` in send.py (the only "dispatch" hit is the word inside a
comment/docstring). Seven local `import rotate`s remain.

Rotate symbols used, classified:

- ORCHESTRATION (residue): `_commit_spawn_row`, `_persist_pending_key`,
  `_finish_pending_swap_on_push`, `_push_season_branch`.
- PLUMBING/PRESENTATION (not policy): `_git_toplevel`, `_normalize_settings`
  (x2), `DEFAULT_TMUX_SESSION`, `_find_seat`, `_own_row_line`,
  `_seats_ownrow_content`.

So falsifier 1 is NOT met on this tip: `send.py` still imports rotate
row-commit / pending-key / pending-swap / push orchestration. Deliberately NOT
restructured this round (dispatch constraint).

## Falsifier 3 — DEFER (with trace)

```
$ ls extensions/agi/bin | grep -iE "messag|magic|pane"
(no messaging/magic-pane module)
```

`goal:g7.32.2` (magic-pane messaging) is not built on this tip: no
messaging/magic-pane module exists. What DOES exist is the cross-harness nudge
path inside `send.py`: `send_dm` (line ~3895) calls
`_nudge_window(root, other, sender=..., body=text)` then
`_announce_nudge(croot, other, ok)`; the inbox path calls `_announce_nudge` via
`send` (line ~2960). So the nudge bridge already lands through this router's
`dm` transport (and the inbox transport), but native grok<->grok messaging is
DEFERRED, not claimed.

## Behaviour preservation

```
$ python3 -m pytest extensions/agi/tests/test_send.py \
    test_send_nudge_classes.py test_send_quiet.py test_send_rewind.py \
    test_send_surface_ssh_or_not.py test_send_undelivered.py -q
372 passed, 11 warnings in 142.94s
```

## Budget

```
$ git diff --numstat -- extensions/agi/bin/send.py
79      61      extensions/agi/bin/send.py
```
production_lines=79, line_ceiling=40 (under 2x; a refactor of three moved
branches, not new behaviour).
Raw output, screenshots, logs.
