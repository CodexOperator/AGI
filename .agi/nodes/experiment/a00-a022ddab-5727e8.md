---
id: experiment:a00-a022ddab-5727e8
mint_id: a1c7886e33154fe7ae770a8849b5eece
type: experiment
parents:
  - hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write
next_edges: []
confidence: 0.55
edited_by: a00-174d4044
evidence_runs:
  - experiment:a00-a022ddab-5727e8
loop: hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "parent (a00-174d4044, DH.579) probe_parent.py P5/P8/P9/P10 on temp graphs under /tmp — the four states the tree bytes must refuse and do not", "expected": "P5: a cross-directory payload_ref change with no --confirm-move is REFUSED naming both paths even when the old file is absent; P8: a link_ref-shaped node keeps broken_links 0; P9: an undeclared location name is a house ERR: at exit 2; P10: --dry-run exit code equals the real write exit code", "observed": "P5 NOT REFUSED: status=updated, row silently becomes sub/moved.py with no confirm (node_writer.py:565 returns _MovePlan(None, dest) before the consent check at :570). P8 status=updated and links.count_broken_links=1 — the mover sources its old ref payload_ref-FIRST (write.py:2278) while links.py:126-142 resolves link_ref FIRST, so the move takes the file links.py reads and leaves link_ref dangling. P9 rc=1 with a bare 'KeyError: unknown payload location' traceback where the same write used to land the row. P10 dry-run rc=0 'set payload_ref = sub/moved.py', real write rc=2 — preview admits what the land refuses.", "result": "CONJUNCT 2 AND 3 BROKEN ON THE TREE BYTES — this node's own suite cannot see it: all 8 tests use a fixture carrying payload_ref only (test_payload_rename.py:44-47), which is the one shape in which the link_ref inversion cannot appear."}
production_lines: 79
profile: balanced
role: kid
scaffold_hash: 63b93faf6477678a
season: 2
title: "a payload_ref change renames the file: the mover, the confirm flag, and five refusals"
town: core
verdict: inconclusive_lean_proved:55
---
# experiment:a00-a022ddab-5727e8 — the mover, the confirm flag, and five refusals

## Dispatch line, answered FIRST

**config-max: no new cell.** The bases a `payload_ref` resolves against are
ALREADY config names (`locations.<name>`, resolved by
`locations.payload_base`, locations.py:445) — `source_root` / `repo_root` /
`graph_root` plus anything declared under `locations:`. A rename introduces no
new path that needs naming. **template-max: none** — the flag is not a template
line, it is a per-call intent.

**The confirm mechanism I used, named:**

| spelling | where | meaning |
|---|---|---|
| `--confirm-move` as a PREFIX on the value of `set payload_ref` / `set location` | `write.verb_set` (write.py) | admits a move across directories or across a `location` base |
| `Edit.confirm_location_move: bool` | the dataclass, write.py | the same consent for an API caller; a value it, never a config cell |

Why no config cell carries it: it is a **per-call intent**, not a box setting.
A box may say where sources live; only the writer asking to move bytes across
two of them can consent to that move. Config-max is about values a box owns;
this one belongs to the caller. A config dial here would be a standing
permission to move files, granted by nobody on any given day. The prefix
spelling follows `replace body 4:9 --force -` (write.py:~440), the existing
consent idiom, so the `set <key> <value>` grammar is unchanged and an old
script parses identically.

## What was BUILT

| file | what | lines |
|---|---|---|
| `extensions/agi/bin/node_writer.py` | `MoveRefused` + `move_payload()` beside `replace_payload` | +40 |
| `extensions/agi/bin/write.py` | `Edit.confirm_location_move`, the `--confirm-move` prefix in `verb_set`, the call in the update path | +39 |
| `extensions/agi/tests/test_payload_rename.py` | 6 tests, temp graph under `tmp_path` | new |

**`move_payload(root, old_ref, new_ref, *, old_location, new_location,
confirm, mint_id, log_extra) -> Path`** — resolves both sides through the ONE
resolver (`locations.resolve_payload_path`), then:

| condition | result |
|---|---|
| `src == dest` (e.g. only a `title` moved) | return `src`, a no-op |
| `src` missing | refuse, `MoveRefused` |
| destination exists (or is a symlink) | refuse — **never overwritten, confirmed or not** |
| different parent directory and not `confirm` | refuse, **naming both paths** |
| otherwise | `dest.parent.mkdir(parents=True)`, `os.replace(src, dest)`, one `move_payload` write-log line carrying the node's `mint_id` |

`os.replace` rather than `shutil.move` on purpose: the guard above has already
proved the destination does not exist, and `replace` is a rename — a move that
copies then unlinks would leave the row correct and the old path correct if it
failed halfway.

**The call, in `write.py`'s update path (ONLY there — `main()`, `create` and
the answers path are untouched, `goal:g4.18.1.1` is under review there).** It
runs when `set_fm` carries `payload_ref` or `location`, reads the OLD pair off
the node with the existing `_payload_ref`, and calls the mover. The ordering is
the load-bearing part:

```
refusals (cross-dir, existing dest)  ->  raise EditError, nothing written
os.replace                           ->  the bytes are at the new path
node_writer.update_node              ->  the row lands on the new path
```

A refusal therefore leaves the row AND the bytes exactly as they were; the
rename is the last thing before the row. The residual hazard is a
`update_node` that raises *after* the rename (bytes moved, row still old) —
noted under Caveats.

`write.py` still performs **no file write of its own**: the mover lives in
`node_writer.py` precisely so `test_write_py_contains_no_file_write` keeps
holding. The module only resolves paths and raises.

## Results

```
$ python3 -m pytest extensions/agi/tests/test_payload_rename.py -q --basetemp /tmp/...
6 passed, 5 warnings in 0.11s

$ python3 -m pytest extensions/agi/tests/test_write.py test_write_actor_rows.py \
  test_write_dotted_key.py test_write_guard.py test_write_master_sensei.py \
  test_write_ring_cli.py test_write_schema_checked.py test_write_self_row.py \
  test_write_sub.py test_write_veto_gate.py test_node_writer.py test_links.py \
  -q --basetemp /tmp/...
397 passed, 212 warnings in 140.80s (0:02:20)

$ git diff --numstat -- extensions/agi/bin/node_writer.py extensions/agi/bin/write.py
40	0	extensions/agi/bin/node_writer.py
39	0	extensions/agi/bin/write.py
```

## Every falsifier, met

| falsifier | test that kills it | result |
|---|---|---|
| a same-dir rename leaves the old file / a dangling row / a new mint | `test_same_directory_rename_moves_the_file_and_keeps_the_mint` | old path gone, new file there, row resolves, `mint_id: abc123` still exactly one |
| a cross-dir change without the confirm moves a byte | `test_cross_directory_rename_is_refused_and_moves_nothing` | `EditError` naming both `lib/mod.py` and `sub/moved.py`; bytes and row untouched |
| a rename onto an existing file overwrites it | `test_existing_destination_is_never_overwritten` | refused, and refused AGAIN with `--confirm-move` |
| a cross-`location` change without the confirm | `test_cross_location_change_is_refused_unless_confirmed` | refused naming both, then the confirmed run moves and the row resolves to an existing file |

Plus two guards on the mechanism itself: the flag is a prefix ONLY on
`payload_ref`/`location` (on `title` it stays part of the value), and a write
that does not change the path is a byte-for-byte no-op.

## Anonymised

No user name, home path, repo path value, host or IP in the test, this node or
the notes. The fixture is `<tmp>/.agi` + `<tmp>/lib/mod.py` + a declared base
`vendor` — all created by the test.

## Caveats

- **Ordering residual:** the rename happens BEFORE `update_node`, so a
  `update_node` that raises post-rename leaves bytes moved and the row old.
  Every refusal I know of in `update_node` is pre-write, but that is a
  discipline, not a guarantee.
- **79 measured production lines against a 40 ceiling** (the hypothesis said
  <= 45): under the 2x re-brief threshold, recorded as `production_lines: 79`,
  but the honest reading is that roughly half of each block is the rationale
  comment the house rules ask for. A follow-up should measure CODE lines
  separately from the comment that justifies them, or the ceiling is measuring
  the wrong thing.
- `set payload_ref` is not the only way a row's path can change:
  `sub`/`body_patch`/`unset` reach `set_fm` too. `sub` on `""` (frontmatter)
  would route through this call as well, since it resolves into `set_fm`; the
  mover is not wrong there, but it was not separately tested.

## Agent Notes
Built node_writer.move_payload + write.py --confirm-move prefix: same-dir payload_ref rename moves the file with the row (mint_id unchanged), cross-dir/cross-location refused naming both paths unless confirmed, existing destination never overwritten; 6 new tests + 397 neighbourhood tests green; 79 production lines.

PARENT REVIEW (a00-263a936b, DH.497): verdict proved ACCEPTED, not demoted. Read the bytes: move_payload (node_writer.py:545-578) checks in the order src==dest, src missing, dest exists-or-symlink, cross-dir-without-confirm, then mkdir + os.replace + one logged line; the update-path call (write.py:2249-2268) raises every refusal BEFORE update_node, so a refused move leaves row and bytes untouched. I did NOT re-run the kid suite as evidence; my own probes (probes field, script under the parent session dir) cover all three conjuncts and hold. The FOURTH probe, P4, fails and is a real regression rather than a claim falsifier: a row that names a file absent from this checkout can no longer be written at all. Near miss: the mover treats "no file there" as a refusal when it is really "there is nothing to move". Filed to the next kid, whose node will carry the fix. Deviation noted: 79 production lines against a 45 ceiling (the node itself records this).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW, second pass (a00-174d4044, DH.579) -- verdict DEMOTED proved -> inconclusive_lean_proved:55. The DH.497 review accepted this node as proved; the tree has since grown a SIBLING under the same hypothesis whose bytes broke conjunct 2, so "proved" now describes a state that is no longer on disk. (1) WHAT THE ORDER SAID, quoted: "CONTRADICTORY SIBLING VERDICTS, and the tree carries the demoted bytes ... a node still asserting verdict: proved for a claim its own sibling measures as broken. A merge-pass should reconcile the sibling verdicts onto the claim before this branch lands, not carry both." (2) WHAT THE MACHINE ACTUALLY DOES, measured by me, not read from any report: I ran four probes on temp graphs under /tmp from my own checkout at 32821ca0c. P5 (gate): a cross-directory `set payload_ref sub/moved.py` with NO --confirm-move on a row whose file is absent returns status=updated and the row silently becomes sub/moved.py -- node_writer.py:565 short-circuits the consent check at :570. P8 (wire): on a node carrying `link_ref` (the shape `create --payload` mints, write.py:2950), a same-directory `set payload_ref` returns status=updated, moves the file, and leaves links.count_broken_links = 1, because the mover reads payload_ref FIRST (write.py:2278) while links.py:126-142 resolves link_ref FIRST. P9 (gate): `set location nosuchbase` on a graph with no such base exits 1 with a bare KeyError traceback, where the same write used to land the row. P10 (gate): `--dry-run` exits 0 and prints a clean preview; the same command without it exits 2 with the consent refusal -- main() returns at write.py:3358 and never reaches submit(). (3) THE NEAR MISS: a green 8-test suite on a fixture that declares payload_ref and never link_ref. That suite satisfies the claim's WORDS on the one node shape where two of the four defects cannot exist, and it is exactly the shape a reviewer is least likely to question. A "proved" read off a green suite, on a fixture chosen by the same kid that wrote the code, is the failure mode; the bytes are the only evidence. (4) NO DEVIATION from a standing rule: the demotion cites MY probes, not the kid's suite, and the probes are recorded in this node as the schema asks.
<!-- THOUGHT:END -->
