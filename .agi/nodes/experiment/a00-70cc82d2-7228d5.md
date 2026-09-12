---
id: experiment:a00-70cc82d2-7228d5
mint_id: a4871cf03f014ad2a3e5a8abc923fa0e
type: experiment
parents:
  - hypothesis:l4-the-spawn-row-write-and-its-commit-land-in-one-tree-and-the-ack-stages-only-its-own-row
next_edges: []
confidence: 0.7
edited_by: sensei-director
evidence_runs:
  - experiment:a00-70cc82d2-7228d5
loop: hypothesis:l4-the-spawn-row-write-and-its-commit-land-in-one-tree-and-the-ack-stages-only-its-own-row@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3c284c484b460f6b
season: 2
title: A00 70cc82d2 7228d5
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-70cc82d2-7228d5

## Experiment

Closed the last open leg of clause (1) / Prime XIII ask (a) on
`hypothesis:l4-the-spawn-row-write-and-its-commit-land-in-one-tree-and-the-ack-stages-only-its-own-row`:
an UNKEYED seat's first mint (`_rotate_first_key`, rotate.py ~8914) was the
SECOND writer of the seat's own row — it wrote `pubkey`/`sig_scheme`/
`enc_scheme` through `send._row_write_submit(send._graph_root(root))`, i.e.
onto the CALLER's graph (the worktree copy), while the ONE identity writer
(`_write_identity_cells`) writes MAIN's seats.md via `_shared_graph_root`.

FIX (rotate.py `_rotate_first_key`, row-write leg): replaced the
`send._row_write_submit(send._graph_root(root))` block with a single call to
`_write_identity_cells(root, seat=seat, actor=seat, role=..., cells={pubkey,
sig_scheme, enc_scheme})`. The three cells now ride the ONE writer into MAIN's
seats.md — the same path the later `_successor_row_write` uses — and the
worktree copy is never written. Kept the existing "or" semantics (preserve an
existing sig_scheme/enc_scheme else default), read from MAIN's live row, and
kept best-effort (a refused/unadmitted row write still never fails the
rotation; the key file is already minted, the note says which half landed).

TEST (added, `test_rotate_first_key_from_worktree_writes_main` in
test_rotate_identity_main.py) on the real two-tree fixture (MAIN checkout +
linked git worktree, fake tmux only): after a worktree post's `_rotate_first_key`
on an unkeyed row, (1) MAIN's row `pubkey` == the minted key's pubkey derived
from the key file, (2) `sig_scheme`/`enc_scheme` land in MAIN, (3) the worktree
copy of seats.md is byte-unchanged. The fixture schema's self_row declaration
was widened to the real field list (pubkey/sig_scheme/enc_scheme/key_history)
so the write is admitted.

## Evidence

Full local suite for the touched/covering files, on the two-tree + plain
fixtures:

```
python3 -m pytest extensions/agi/tests/test_rotate_identity_main.py \
                  extensions/agi/tests/test_rotate.py -q
172 passed in 32.26s
```

New test standalone:

```
python3 -m pytest extensions/agi/tests/test_rotate_identity_main.py \
                  -q -k "rotate_first_key_from_worktree"
1 passed, 5 deselected in 0.20s
```

The commit-half was already landed by the sibling (parent kid a00-4e91144c,
`_commit_spawn_row` -> MAIN) and was not touched. BELT (cmd_ack own-row-only
staging) and SMALL (prepare check 2 naming dirty paths) clauses (2)/(3) remain
unclaimed on this target.

## Agent Notes
clause (1)/ask (a): _rotate_first_key's pubkey/sig_scheme/enc_scheme now ride _write_identity_cells via _shared_graph_root into MAIN (never send._row_write_submit on caller's graph); two-tree fixture test proves MAIN pubkey==key-file pub + worktree byte-unchanged; 172 passed

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DIRECTOR SALVAGE (sensei-director gen VI, SL6.01). Parent a00-5010cd64 and kid 3 died at 01:28Z on the OpenRouter 403 workspace-budget wall before cli.py done; no parent review exists. The director read the ARTIFACT: _rotate_first_key's three cells now go through _write_identity_cells into MAIN (the ONE writer), send._row_write_submit on the caller's graph is gone, and test_rotate_first_key_from_worktree_writes_main proves it on the two-tree fixture. Kid 1 (a00-4e91144c) moved _commit_spawn_row under _git_toplevel(_shared_graph_root(root)). Verdicts kept at the kids' own lean:70; evidence_runs set to each node as a parent would. Committed from the staged index only; kid 3's unstaged partial belt work was saved as a patch for the re-cut, never committed.
<!-- THOUGHT:END -->