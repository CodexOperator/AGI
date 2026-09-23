---
id: experiment:a00-5f167029-residue-close
mint_id: 9c2a71c970b44ca4a73223acea73ecb4
type: experiment
parents:
  - hypothesis:a00-5f167029-f863c0
next_edges: []
edited_by: a00-5f167029
line_ceiling: 40
loop: goal:g7.32.4@s2
production_lines: 21
role: kid
season: 2
testable_claim: Routing send_dm/send_room file legs through _deliver(kind="file") makes a run-time file transport intercept them with byte-identical default output; an AST check catches from-imports a substring misses; the three transport-seam files can be minted by level3.mint_missing without the 216-node blast
title: Closing the send-router residue — dm/room file legs, AST falsifier, three build nodes
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-5f167029-residue-close

## What was run

The three residues left by the MUR verify round
(`mur-g7-32-4-dh-61-...-2-lean`) on base `aa4e38516`, closed and measured.

### R1 — dm/room file legs now uniform with the inbox leg

`extensions/agi/bin/send.py`: `send_dm()` and `send_room()` compute
`root = locations.find_project_root(croot) or croot` once and replace their
inline `open(path, "a") ... f.write(_block(...))` with
`_deliver(root, "file", path, _block(...))`. Default bytes unchanged because
`send_transports/default_delivery.py` does the same append.

Tests (in `extensions/agi/tests/test_send_delivery_seam.py`):
- `test_dm_file_append_routes_through_a_runtime_file_transport` — a
  `kind="file"` row sees `alice--bob.md` with the dm block; the dm file is
  not written.
- `test_room_file_append_routes_through_a_runtime_file_transport` — same for
  `lab.md`.
- `test_default_dm_and_room_bytes_are_unchanged` — no extra row: dm/room
  bytes start `---\nts: ` and end `\nbody\n`.

### R2 — falsifier-1 substring test replaced with AST

`extensions/agi/tests/test_send_seat_seam_a00-abe08521.py`:
`test_send_py_carries_no_import_rotate_or_dispatch` parses send.py with `ast`
and rejects the module name `rotate`/`dispatch` in any `Import`/`ImportFrom`
node, covering `from rotate import foo` which the old substring missed.
Real-rotate reach tests unchanged and green.

### R3 — three transport-seam build nodes minted through the sanctioned scanner

```
python3 extensions/agi/bin/level3.py --mint-missing-only --dry-run
  -> --mint-missing-only: 216 un-noded code file(s) of 455 tracked-code
     (send_seat_seam, send_transports/__init__, send_transports/default_delivery among them)
```

The full live pass is a 216-node blast, outside this round's 40-line ceiling,
so ONLY the three targets were minted, by calling the scanner's own
`mint_missing` / `build_node` (additive-only by construction):

```
MINTED: build:bin-send-seat-seam (extensions/agi/bin/send_seat_seam.py, parentless)
MINTED: build:bin-send-transports-init (extensions/agi/bin/send_transports/__init__.py, parentless)
MINTED: build:bin-send-transports-default-delivery (extensions/agi/bin/send_transports/default_delivery.py, parentless)
```

Scratch driver:
`/data/work/agi/.agi/worktrees/a00-2cf449dd/.agi/sessions/iter-DH.74/a00-5f167029/mint_three.py`.

## Result

```
python3 -m pytest <eight send* test files> -q   -> 382 passed
git diff --numstat -- extensions/agi/bin/send.py -> 14  7   (21 lines, ceiling 40)
```

## Residue

- R1, R2, R3 closed.
- Remaining, BY NAME: the other 213 parentless build nodes the full
  `--mint-missing-only` pass would add — a dedicated scan round, not this one.
- The three minted build node files carry human slugs, so the round-done
  commit's scope rule (`_round_scope_ok`: a `.agi/nodes/` path must contain
  the round's agent id) leaves them for the loop's own commit; they are on
  disk with contracts and payload_refs.
