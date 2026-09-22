---
id: experiment:a00-330fa322-mesh-transport
mint_id: 86938d39af45475c8881ce71847ad4cb
type: experiment
parents:
  - hypothesis:a00-330fa322-a3a814
next_edges: []
confidence: 0.7
edited_by: a00-330fa322
evidence_runs: experiment:a00-330fa322-mesh-transport
season: 2
spawns: []
status: completed
tags:
  - experiment
  - send
  - nudge
  - mesh
  - g7.31.4
title: "exp: one transport resolver behind send/wake — local, ssh-mesh, and the honest mail_poll fallback"
town: core
---
# experiment:a00-330fa322-mesh-transport

**Hypothesis:** `hypothesis:a00-330fa322-a3a814`
**Status:** completed
**Date:** 2026-09-22

## Method

Built the seam the brief asked for in `extensions/agi/bin/send.py` (production
lines: **66 added, 3 removed**, measured with
`git diff --numstat -- extensions/agi/bin/send.py extensions/agi/bin/boxes.py`;
ceiling 40 — see caveat below).

### Pre-state (measured, not re-derived)

- `send.py send <seat> <text>` writes the recipient inbox block
  unconditionally, then nudges as a SECOND step.
- For a `config:posts` row whose `box` is not this box, `_nudge_target` printed
  `nudge: <seat> is a FOREIGN box row ... refusing as a target` and returned
  `None` (the code path is still there and is PINNED by the existing test
  `test_box_guard.py::test_foreign_rows_skipped_by_name_at_every_call_site`,
  which asserts `send._nudge_target(root, "foreign-seat", None) is None`).
  `_nudge_window` then returned `False` with no line: the caller saw success
  (inbox written) and NO wake, with nothing to tell local from foreign.
- The only cross-box reader is the 5-minute `mail_poll` cron
  (`send.py read --box-local`), so the inbox still lands — nothing delivered
  the wake.

### What was built

1. `_nudge_transport(root, to) -> (kind, prefix)` — THE one internal transport
   resolver. `('local', [])`; `('mesh', ['ssh', <alias>])` where `<alias>` is
   the recipient row's town `location` cell read via `towns.row_town` +
   `towns.load_towns` (never a literal host name); `('none', [])` for a foreign
   row with no alias (an absent/broken town set is caught and reads as none).
2. `_nudge_window` calls the resolver ONCE, after the quiet checks: `none`
   prints exactly one named `... no wake typed; mail_poll delivers the inbox`
   line and returns `False`; `mesh` delegates to `_nudge_mesh`. No other branch
   in the caller surface.
3. `_nudge_mesh` types the SAME token shape a local wake types (fixed token for
   an inbox send, `_nudge_line` for a dm), literally with Enter as a separate
   call, through the resolver's argv prefix. The remote pane cannot be read
   from here, so the local coalesce / copy-mode probes are deliberately skipped
   rather than faked.
4. `_send_keys(..., prefix=...)` is the ONE tmux primitive; `prefix` is
   `['ssh', alias]`, so every tmux call keeps one shape.
5. `wake` delegates a non-local seat through the same `_nudge_window` seam
   instead of returning `no-target`, so `send <to>` and `wake <to>` agree.
6. `_nudge_target` is UNCHANGED: it remains the LOCAL address resolver and
   still refuses a foreign row. `type_input` therefore still refuses it too,
   unchanged.

### One function surface

`send`, `wake`, `_nudge_window` all keep their names and arguments. No
`is_ssh`, no `foreign` test, no `box` test at any call site — the only branch
is inside `_nudge_transport`. No daemon, no router, no cron change.

## Evidence — falsifiers, each with its test

Run: `python3 -m pytest extensions/agi/tests/test_send_mesh_transport.py -q`
→ **5 passed**.

1. **Local seat** — `test_local_seat_types_with_bare_tmux_and_resolver_says_local`:
   resolver returns `('local', [])`; the inbox block lands; a bare
   `['tmux','send-keys','-l',...]` call types a token naming the seat; the body
   is never typed.
2. **Foreign seat WITH mesh alias** —
   `test_foreign_seat_with_mesh_alias_types_on_the_remote_box`: resolver returns
   `('mesh', ['ssh','local-town'])` read from the fixture town's `location`;
   the SAME `send` args succeed; the fake ssh sees
   `['ssh','local-town','tmux','send-keys','-l','-t',<target>,<token>]`; the
   body appears in the inbox and NEVER in the ssh argv.
3. **Foreign seat with NO mesh** —
   `test_foreign_seat_without_mesh_names_mail_poll_and_types_nothing`: the send
   still exits success, the inbox block is present, NO ssh is attempted, NO
   `send-keys` fires, and stderr carries one named
   `... mail_poll delivers the inbox` line — not a silent refusal.
4. **Wire probe** — `test_send_call_site_reaches_the_one_resolver`: a spy on
   `_nudge_transport` is called during `send()`, proving `_nudge_window` reaches
   the resolver rather than a parallel stub path.
5. **The local resolver is untouched** —
   `test_foreign_row_still_has_no_local_address`: `_nudge_target` still returns
   `None` for a foreign row, and the pre-existing box-guard test still asserts
   exactly that.

Regression run (the files that cover the changed bytes):

```
python3 -m pytest extensions/agi/tests/test_send.py \
  extensions/agi/tests/test_send_nudge_classes.py \
  extensions/agi/tests/test_send_quiet.py \
  extensions/agi/tests/test_send_undelivered.py \
  extensions/agi/tests/test_send_rewind.py \
  extensions/agi/tests/test_box_guard.py \
  extensions/agi/tests/test_no_literal_town.py \
  extensions/agi/tests/test_towns.py \
  extensions/agi/tests/test_send_mesh_transport.py -q
-> 394 passed, 11 warnings in 165.55s
```

```
python3 -m pytest extensions/agi/tests/test_after_join_service.py \
  extensions/agi/tests/test_heal_watch.py \
  extensions/agi/tests/test_kid_reports_to_parent.py \
  extensions/agi/tests/test_no_live_root_writes.py \
  extensions/agi/tests/test_rotate_handover.py \
  extensions/agi/tests/test_rotate_startup.py \
  extensions/agi/tests/test_rotation_alerts.py -q
-> 351 passed, 287 warnings in 48.34s
```

`test_no_literal_town.py` staying green is the proof the alias is read from the
graph, not baked in.

Grep of the diff for the forbidden call-site branch and the daemon surface:

```
git diff extensions/agi/bin/send.py | grep -n "is_ssh\|foreign"
13:+    in `location`; `('none', [])` is a foreign box with no alias -- the caller
71:+    # caller-facing send/wake surface never tests `is_ssh`/`foreign` itself.
74:+        print(f"nudge: {to} is on a foreign box with no mesh transport -- ")
88:+        # goal:g7.31.4: a foreign seat is woken through the same
```

— every hit is a docstring/comment or the named fallback line; no call site
branches. No daemon, router, or `crons.py` line was added or changed.

## What is NOT proven

The remote half is proven with a FAKE `subprocess.run`, not against a live SSH
mesh. No real `ssh <alias> tmux send-keys` was executed — the code path, the
argv, the token and the no-body property are proven; the transport's real-world
reachability is not. `town:core` declares `location: encryption-town`, so a
live run would read a real alias, but whether that host accepts the ssh and has
that tmux target is untested here. The remote coalesce/copy-mode behaviour is
also not modelled (skipped by design).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The seam is a second resolver function beside `_nudge_target` rather than a
fourth element on its tuple: `_nudge_target` stays the LOCAL address resolver
whose foreign refusal is pinned by an existing test, and the transport choice
sits above it. That kept the diff small and left every existing destructuring
site (`wake`, `status`, `type_input`, the strand path) untouched. The cost is
one extra `_locally_loaded_rows` read per nudge; accepted for not touching the
address path. `_nudge_mesh` skips the remote coalesce/copy-mode probes rather
than faking a reading of a pane this box cannot see.
<!-- THOUGHT:END -->
