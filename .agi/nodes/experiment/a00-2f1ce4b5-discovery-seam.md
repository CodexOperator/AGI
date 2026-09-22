---
id: experiment:a00-2f1ce4b5-discovery-seam
mint_id: 4dcdd760224e4533be31cdc57d1d78df
type: experiment
parents:
  - hypothesis:a00-2f1ce4b5-36077e
next_edges: []
edited_by: a00-2f1ce4b5
line_ceiling: 40
loop: goal:g7.32.4@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 74
profile: balanced
role: kid
scaffold_hash: 7cbd83c9d39978fb
season: 2
title: Transport discovery seam — a dropped module is the whole registration
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-2f1ce4b5-discovery-seam

## What was built

**goal:g7.32.4 falsifier 2, module+discovery leg** — a transport module is now
sufficient ON ITS OWN: dropping a file that defines
`register(register_delivery, helpers)` into the transport directory registers
it. No edit to send.py's selection loop and no import added to send.py.

New package `extensions/agi/bin/send_transports/`:

```
send_transports/
  __init__.py           # discover(register_delivery, helpers, directory=None)
  default_delivery.py   # the built-in file-append / pane-nudge transports
```

- `discover(...)` scans the dir (default: its own) for non-underscore `*.py`,
  loads each by file path via `importlib.util.spec_from_file_location`, and
  calls `register(register_delivery, helpers)`. Idempotent per registry:
  paths already seen by *this* `register_delivery` are skipped, so a re-import
  or reload cannot double-register. `directory=` is overridable so a test can
  point it at a throwaway dir.
- `default_delivery.py` is `_deliver_default` MOVED VERBATIM out of send.py:
  `kind="file"` appends the block; `kind="nudge"` wakes the pane.
- send.py now calls (once, where the old `register_delivery("default", ...)`
  was):

```python
import send_transports  # noqa: E402

send_transports.discover(register_delivery, {
    "nudge_window": lambda *a, **k: _nudge_window(*a, **k),
    "announce_nudge": lambda *a, **k: _announce_nudge(*a, **k)})
```

The helpers are **late-bound lambdas**, not frozen function references: the
built-in nudge handler resolves `send._nudge_window` at CALL time, so
monkeypatching the symbol still reaches it. (A direct reference broke
`test_send_surface_ssh_or_not.py` — a real regression, fixed and named as a
struggle.)

## Falsifier 2, module+discovery half — PROVED

New test
`extensions/agi/tests/test_send_transport_discovery_a00-2f1ce4b5.py` (3 tests):

1. **dropped module registers with no edit to send** — writes a NEW
   `carrier_pigeon.py` into a tmp dir, calls
   `send_transports.discover(send_mod.register_delivery, helpers, directory=tmp)`,
   and asserts it is the FIRST row and that `send()` writes through it
   (`INTERCEPTED`), with the inbox never getting the normal block; plus
   `"carrier_pigeon"` / `"carrier-pigeon"` do not appear in send.py's source.
2. **idempotent per registry** — a second `discover()` over the same dir loads
   nothing and registers one row, not two.
3. **built-in delivery lives in its own module** — `default` is registered at
   import, `def _deliver_default` no longer appears in send.py, and with only
   the real dir discovered the bytes are the old append verbatim.

```
$ python3 -m pytest extensions/agi/tests/test_send_transport_discovery_a00-2f1ce4b5.py -q
3 passed
```

## Behaviour preservation

send.py no longer defines `_deliver_default`; a census shows the built-in
file/nudge transports defined only in `send_transports/default_delivery.py`.
With only the built-ins discovered, every byte written is unchanged and every
existing send test stays green:

```
$ python3 -m pytest extensions/agi/tests/test_send.py \
    test_send_nudge_classes.py test_send_quiet.py test_send_rewind.py \
    test_send_surface_ssh_or_not.py test_send_undelivered.py \
    test_send_seat_seam_a00-abe08521.py test_send_transport_seam.py \
    test_send_delivery_seam.py test_send_transport_discovery_a00-2f1ce4b5.py -q
386 passed, 11 warnings in 36.69s
```

Live CLI sanity: `send.py --help` exits 0; at import
`DELIVERY_TRANSPORTS == ['default']`, `SEND_TRANSPORTS == ['room', 'dm', 'inbox']`.

## Residue (named, not hidden)

- The CLI-addressing `SEND_TRANSPORTS` rows (room/dm/inbox) are still defined
  in send.py; only the DELIVERY leg is module+discovery this round.
- Falsifier 1 is untouched: send.py still reaches rotate through
  `send_seat_seam.py` (kid a00-abe08521's named boundary), and the four
  orchestration symbols remain.
- Falsifier 3 (g7.32.2 magic-pane) still DEFERRED.

## Budget

```
$ git diff --numstat -- extensions/agi/bin/send.py
9       14      extensions/agi/bin/send.py
$ wc -l extensions/agi/bin/send_transports/__init__.py \
        extensions/agi/bin/send_transports/default_delivery.py
44 + 21 = 65
```
production_lines = 9 + 65 = 74, line_ceiling = 40 (under 2x; the loader's
docstring and the moved handler are the bulk — no new behaviour).

Raw output, screenshots, logs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Why this version: falsifier 2 module half built as a directory-scan discovery seam rather than another table row. send_transports.discover() loads each module by file path and calls its register(register_delivery, helpers); idempotency is tracked on the register function object, not a module global, so a fresh send module in each test process still discovers the built-ins. The built-in _deliver_default moved verbatim into send_transports/default_delivery.py. First cut passed frozen function references as helpers and broke monkeypatch visibility (test_send_surface_ssh_or_not.py), so the helpers are late-bound lambdas resolving send._nudge_window / _announce_nudge at call time.
<!-- THOUGHT:END -->
