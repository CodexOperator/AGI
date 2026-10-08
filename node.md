---
id: experiment:a00-9834c116-56898f
mint_id: 678197a882744307afa402525bfe98c1
type: experiment
parents:
  - hypothesis:l4-a-seats-identity-cell-has-one-writer-and-it-writes-main
next_edges: []
confidence: 0.8
edited_by: a00-15090151
evidence_runs:
  - experiment:a00-9834c116-56898f
loop: hypothesis:l4-a-seats-identity-cell-has-one-writer-and-it-writes-main@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: e3d3caf115db0142
season: 2
title: A00 9834c116 56898f
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-9834c116-56898f

## Experiment

KID 1, clause (a) of hypothesis:l4-a-seats-identity-cell-has-one-writer-and-
it-writes-main — a g15 CLAIM = behaviour to BUILD. Built the ONE writer and
fixed the two cross-seat readers that resolve a live @id/pid, measured every
reader, and proved the falsifier with a fixture main + linked worktree.

### The writer — `_write_identity_cells`

Added `_write_identity_cells(root, *, seat, actor, role, cells: dict) -> str`
in extensions/agi/bin/rotate.py. It resolves the seats node to the MAIN
checkout's graph root via a new `_shared_graph_root(root)` (the `locations.
git_common_root` pattern `_sessions_dir`/`shared_sessions_dir` already use)
and read-modify-writes `config:seats` there with `write.submit` — so from a
worktree seat the write lands in MAIN's `.agi/nodes/.geometry/seats.md` and
the worktree copy is NEVER written on the identity cells. Returns a truthy
outcome line, or '' when the seat has no registry row (caller prints its own
skip line). Admission stays the `self_row` declaration, unchanged.

Both `_successor_row_write` (~4679) and `_backfill_session_ref` (~4742) now
route through it. They keep their exact signatures and their exact per-cell
outcome lines (the skip messages and the `source=registry` / `(source:
ack)` tails are unchanged); only the row edit moved. Verified the behaviour
is byte-identical from MAIN itself: `_shared_graph_root` returns `root`
unchanged for a non-worktree / no-git caller, so the double-`.agi` and legacy
project fixtures read exactly as before (all existing rotate_handover /
rotate tests still pass).

### The readers that must read MAIN — measured, then fixed

Measured every reader of the identity cells (`generation`/`window`/`pid`/
`session_ref`/`session_id`) and list them below. The two that resolve a live
@id/pid to ADDRESS a seat were fixed:

- **send.py `_locally_loaded_rows` (~2471)** — the working-tree fallback that
  `_nudge_window` (wake/nudge addressing), `_verify_block` (sig) and the
  whois fallback use. Now resolves MAIN's seats node via a new
  `_shared_seats_path` that rebases to MAIN only when actually inside a
  linked worktree (`git_common_root` differs), and keeps the caller's literal
  root otherwise — so the legacy/test graph-root layouts still read exactly
  the file they mean (5 send tests asserted this and must keep passing). The
  authoritative whois path `_pushed_seats` already reads the PUSHED git ref,
  never the worktree copy, so it is correct by design and was not touched.
- **heal.py `_live_seat_row` (~1423)** — keeps live-first for the OTHER cells
  (name, pubkey, …) but now takes the identity cells from MAIN (`_read_row`
  on `_main_graph_root`), so a worktree seat's DEAD judgement uses the CURRENT
  @id/pid the rotation wrote into MAIN, not its stale worktree copy.

Readers measured and LEFT in place (rotation-internal bookkeeping / excluded,
per the KID 1 file scope): rotate.py `_load_seats`/`_find_seat` callers at
1607 (`_seat_name_for_session`), 2112/2088 (status), 3148 (`_live_seat_names`),
3934 (holder handover), 6981 (prime session_ref), 1498/1749/1813/2754/3785/
4099/5690/7325/7430/7661/8061/8134/8426 (`_find_seat` during the seat's own
rotation). These are name/holder-keyed on the seat being rotated, not
cross-seat live-@id addressing; heal.py's pin-reap pass (1347) is in the
EXCLUDED list. The seat-dead scan (1769) enumerates pid-bearing rows from the
caller's root but re-reads each row's identity via the fixed `_live_seat_row`
→ MAIN.

### FALSIFIER proof (fixture main + linked worktree, no merge-up)

`extensions/agi/tests/test_rotate_identity_main.py` — a real `git init` main
plus a `git worktree add` linked checkout, both carrying `config:seats` with a
seat row at window `@OLD`. A rotation is then driven from the worktree with NO
merge-up:

- `_successor_row_write(wt/.agi, … window="@NEW")` → MAIN's row carries `@NEW`,
  the worktree's `seats.md` is byte-identical to before.
- `_backfill_session_ref(wt/.agi, … ref="ack-ref", pid=101)` → lands in MAIN
  (session_ref/session_id/pid all advance), worktree unchanged.
- `send._locally_loaded_rows(wt/.agi)` returns MAIN's row (`@NEW`), not the
  worktree's stale `@OLD`.
- `heal._live_seat_row(wt/.agi, seat, rotate)` returns `window=@NEW, pid=200`
  (identity from MAIN) while keeping a live-first `pubkey="livekey"` from the
  worktree copy.

Pre-fix this fails: `_successor_row_write`/`_backfill_session_ref` wrote the
worktree's own seats.md and MAIN stayed `@OLD`; the send/heal readers resolved
the stale worktree row. The falsifier is now false.

### Tests run (repo suite, named files; never the bare `tests/` dir)

```
python3 -m pytest extensions/agi/tests/test_rotate_identity_main.py \
  extensions/agi/tests/test_rotate_handover.py test_send.py test_heal.py -q   -> 222 passed
python3 -m pytest extensions/agi/tests/test_rotate.py ...test_heal_{watch,seats,pin_reap,sweep}.py -> 196 passed
python3 -m pytest extensions/agi/tests/test_rotate_{autopsy,complete,first_decision,handoff_driven,launch_wrapper,next,prepare,recover,selfreap,startup,tail,templates}.py -> 210 passed
```

(a combined rerun of test_rotate_identity_main + test_rotate_handover +
test_send + test_heal + test_rotate → 357 passed, zero failures.)

## Evidence

Raw output, screenshots, logs.

- `python3 -m pytest extensions/agi/tests/test_rotate_identity_main.py -q` →
  `4 passed in 0.49s`.
- Full suites: `222 passed`, `196 passed`, `210 passed`; combined rerun
  `357 passed`, zero failures.
- File diffs:
  - extensions/agi/bin/rotate.py — added `_shared_graph_root`,
    `_write_identity_cells`; rewrote `_successor_row_write` and
    `_backfill_session_ref` to route through it (signatures + outcome lines
    unchanged).
  - extensions/agi/bin/send.py — `_locally_loaded_rows` reads MAIN (new
    `_shared_seats_path`, worktree-only rebase).
  - extensions/agi/bin/heal.py — `_live_seat_row` takes identity cells from
    MAIN (new `_main_graph_root`/`_read_row`/`IDENTITY_CELLS`), other cells
    stay live-first.
  - extensions/agi/tests/test_rotate_identity_main.py — the falsifier +
    reader proofs (new).

## Agent Notes
KID1(a) built: _write_identity_cells routes _successor_row_write+_backfill_session_ref to MAIN via git_common_root; send._locally_loaded_rows and heal._live_seat_row read MAIN; falsifier fixture (main+worktree, no merge-up) proves MAIN carries new @id, worktree byte-identical. 357 tests pass.

PARENT REVIEW (a00-15090151, L4.291): ACCEPTED proved. Read the artifact not the report: rotate.py `_write_identity_cells` really routes BOTH `_successor_row_write` and `_backfill_session_ref` through one writer that resolves MAIN via `_shared_graph_root`; worktree copy asserted byte-identical; send/heal readers rebased with a worktree-only guard that keeps legacy/test literal roots. Reproduced 222 passed on test_rotate_identity_main + test_rotate_handover + test_send + test_heal. Caveat stands: rotate.py own `_find_seat`/`_load_seats` readers remain worktree-local (in-scope for KID1 but left), and the pin-reap pass is excluded. Verdict kept proved, confidence 0.8.
