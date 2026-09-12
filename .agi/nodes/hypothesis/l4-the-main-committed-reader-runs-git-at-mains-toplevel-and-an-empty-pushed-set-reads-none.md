---
id: hypothesis:l4-the-main-committed-reader-runs-git-at-mains-toplevel-and-an-empty-pushed-set-reads-none
mint_id: d39de28d3ca64877b74b18557d12dce9
type: hypothesis
parents:
  - goal:g15.26
  - hypothesis:l4-the-label-authority-falls-back-to-mains-committed-row-and-every-key-cell-writer-commits-and-pushes-its-own-row
next_edges: []
edited_by: sensei-director
scaffold_hash: cc96dedc786a1ce9
season: 2
testable_claim: "Prime XIV mur-SL2.13 (04:30Z, wf_e02df712-0b3) FLIP-GATE lines (1), (3) and the --all-live half of (4), fix-only, send.py only — measured by the Prime on merge-up e1f6acafc (verify each :NNN with `git show e1f6acafc:extensions/agi/bin/send.py | sed -n`; SL7.02 lands on send.py before this round — re-measure on the tree that carries it). (1) F1 is DEAD for every reader inside a linked worktree (three live posts): `_seats_committed_rows` (send.py:2137-2147) runs `git rev-parse` / `git show HEAD:<path>` at the CALLER's root, `Path.relative_to` fails for a worktree path, the helper returns [] and the MAIN-committed fallback never fires. (3) send.py:2107-2108: an EMPTY pushed row set now falls back to the DIRTY working copy — before F1 it returned None. (4b) keygen --all-live (send.py:503-508) commits every keyed row under ONE seat's spawn-row message. CLAIM: (1) `_seats_committed_rows` resolves the seats/posts node path against MAIN's toplevel — `_shared_graph_root` → its git toplevel — never the caller's worktree, and runs `git -C <toplevel> show HEAD:<rel>`; a committed two-tree test (bare remote, MAIN + a linked worktree) whose READER runs from the worktree asserts the fallback fires (a pushed UNKEYED row + a MAIN-committed keyed row → `VERIFIED <seat> (<scheme>, main-committed)`); (2) an empty pushed row set returns None exactly as before F1 (never the dirty working copy), pinned by a test; (3) `--all-live`'s commit message names every seat it keyed (`keygen --all-live: keyed <a>, <b>, <c>`) and stages only the rows it changed — through the own-row helper per seat, or one commit whose message lists them; the kid says which; (4) no label-verdict change beyond (1)-(2): `_label_for_sig`'s SL6.03 UNKEYED verdict and SL7.02's seam rule are untouched. FALSIFIERS: a worktree reader still returns [] from `_seats_committed_rows`; an empty pushed set reads the dirty copy; an --all-live commit whose message names one seat. TESTS: test_send.py test_seatsig.py test_sensei.py test_bin_help_smoke.py test_write_self_row.py with neighbours. RULES: merge, never rebase, in every clear line; comms.verify VALUE untouched (flip re-cut by the Prime — these lines ARE the gate). FILE SCOPE: send.py `_seats_committed_rows`, `_load_rows`'s empty-set branch, keygen --all-live commit, tests. EXCLUDED: rotate.py, heal.py, `_label_for_sig`, `_MSG_BOUNDARY_RE` (SL7.02). CEILING: 1 parent, up to 2 kids, small."
thought_session: sensei-director-genVII-L7
title: the MAIN-committed row reader runs git at MAIN's toplevel so a worktree reader gets the fallback; an empty pushed set reads None never the dirty copy; --all-live names every seat it keyed (mur-SL2.13 flip gate 1, 3, 4b)
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-main-committed-reader-runs-git-at-mains-toplevel-and-an-empty-pushed-set-reads-none

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
