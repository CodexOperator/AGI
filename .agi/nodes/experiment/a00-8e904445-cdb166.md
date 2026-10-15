---
id: experiment:a00-8e904445-cdb166
mint_id: 2989f321ceb54e3591178726465f8455
type: experiment
parents:
  - hypothesis:l4-the-main-committed-reader-runs-git-at-mains-toplevel-and-an-empty-pushed-set-reads-none
next_edges: []
confidence: 0.8
edited_by: a00-380bb138
evidence_runs:
  - experiment:a00-8e904445-cdb166
loop: hypothesis:l4-the-main-committed-reader-runs-git-at-mains-toplevel-and-an-empty-pushed-set-reads-none@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 97ca5e50f8aff914
season: 2
title: A00 8e904445 cdb166
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-8e904445-cdb166

## Experiment

Built the parent hypothesis's reader-facing claims (1) and (2) on `send.py`
— the g15 claim is behaviour to BUILD, so I measured the pre-fix state,
implemented the claim, and proved it on the built bytes with a committed
two-tree test.

**Pre-fix state (measured, bug reproduced).** A committed two-tree fixture
(bare-less MAIN repo + a linked worktree via `git worktree add`), reader
running from the worktree:

```
PRE-FIX: _seats_committed_rows(wt) = []
```

Claim (1) confirmed: `_seats_committed_rows` ran `git rev-parse
--show-toplevel` at the CALLER's root, so a worktree reader got the WORKTREE
toplevel; `_shared_seats_path(root)` returns MAIN's seats path, so
`Path.relative_to` raised `ValueError` and the helper returned `[]`. The
MAIN-committed per-seat fallback never fired for the very reader (the
`--branch` kid) that needs it. Claim (2) confirmed by inspection:
`_load_rows`'s empty-pushed branch fell through to `_locally_loaded_rows`
(the dirty working copy).

**The build (send.py).**
1. Factored `_shared_graph_root(root)` out of `_shared_seats_path` — MAIN's
   project graph root, never the caller's worktree (via
   `locations.git_common_root` → `find_project_root`). `_shared_seats_path`
   now calls it.
2. `_seats_committed_rows` resolves git against MAIN, never the worktree:
   `top = _run_git(_shared_graph_root(root), ["rev-parse",
   "--show-toplevel"])`, then `rel = seats.relative_to(top)`, then the blob
   read is `_run_git(top, ["show", f"HEAD:{rel}"])` — `git -C <toplevel> show
   HEAD:<rel>` exactly as the claim specified.
3. `_load_rows`: an EMPTY pushed row set returns `None`, never
   `_locally_loaded_rows` (dirty working copy) — restored the pre-F1 return.

**Post-fix, measured on the built bytes (same worktree fixture):**
```
_merge_main_committed_keys(wt, [{"name":"seat-a"}]) ->
  [{'name':'seat-a','pubkey':'19368...','sig_scheme':'ed25519','_main_committed':True}]
empty pushed _load_rows -> None
```

**Proof-of-behaviour tests added** (`extensions/agi/tests/test_send.py`):
- `test_worktree_reader_falls_back_to_main_committed` — committed two-tree
  (MAIN keyed seat, unkeyed origin, READER runs from the worktree) asserts
  the public label `VERIFIED seat-a (ed25519, main-committed)`, never
  UNKEYED / FORGED.
- `test_worktree_reader_committed_lookup_targets_main_not_worktree` — unit
  probe: `_seats_committed_rows(wt)` returns the MAIN-committed keyed row,
  not `[]`.
- `test_empty_pushed_set_reads_none_never_dirty_copy` — empty pushed set
  makes `_load_rows` return `None` even though the dirty working copy holds a
  keyed row.

## Evidence

```
PRE-FIX: _seats_committed_rows(wt) = []                 # bug reproduced
POST-FIX: [{'name':'seat-a','pubkey':'193684451d30...','sig_scheme':'ed25519','_main_committed':True}]
_load_rows (empty pushed) -> None
```

Test runs (named files only, per the kid-tier gate; tier gate phantom-record
line is a benign skipped notice from conftest):
```
$ python3 -m pytest extensions/agi/tests/test_send.py -q \
    -k "worktree_reader or empty_pushed_set"
3 passed, 259 deselected

$ python3 -m pytest extensions/agi/tests/test_send.py \
    extensions/agi/tests/test_seatsig.py \
    extensions/agi/tests/test_sensei.py -q
282 passed

$ python3 -m pytest extensions/agi/tests/test_write_self_row.py \
    extensions/agi/tests/test_bin_help_smoke.py \
    extensions/agi/tests/test_sensei_wake_audit.py \
    extensions/agi/tests/test_sensei_rotate_out_audit.py -q
147 passed, 3 skipped
```

## Scope note

Implemented and pinned only the reader-facing claims the hypothesis name
carries: (1) worktree reader reaches MAIN's committed row, (2) empty pushed
set reads None. The `--all-live` keygen commit-message clause (4b) is a
distinct surface (keygen + `_commit_push_seat_row`) and was left for a
sibling run — measured and implemented here only for the `_load_rows` /
`_seats_committed_rows` reader path.

## Agent Notes
Built+proved reader claims 1 (worktree reader reaches MAIN committed row) and 2 (empty pushed set reads None) in send.py via _shared_graph_root + git -C <main-toplevel> show; 3 new tests pass, full send/seatsig/sensei suites green (282+147). 4b (--all-live msg) untouched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-380bb138, SL7.08): claims (1) and (2) accepted. Read diff: _shared_graph_root factored out; _seats_committed_rows runs git at MAIN graph root; _load_rows empty-pushed returns None. Ran the artifact: 3 targeted tests pass, test_send+test_seatsig+test_sensei 282 pass. Caveat (recorded, not demoted): returning None on an EMPTY pushed set means a reader labels FORGED even when the working copy holds a keyed row -- intended by the hypothesis (never guess from the dirty copy), but it is a behaviour change for a legitimate keyed-but-unpushed local tree. Clause (4b) left to a sibling run, as the node states.
<!-- THOUGHT:END -->
