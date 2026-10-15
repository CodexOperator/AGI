---
id: verdict:dg2-g1-send-unreadable
mint_id: 44638387ee8540cda8dce8d745036f28
type: verdict
parents:
  - experiment:a00-a8672dc3-9f1b27
  - hypothesis:g1-send-says-cannot-list-windows-never-window-gone
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:a00-a8672dc3-9f1b27
model: claude-sonnet-5-5
role: director
scaffold_hash: e12cc44bef88eb68
season: 2
title: "G1 send re-verdict: PROVED -- unreadable tmux listing says cannot list windows, never gone; readable absence still says gone; red on base, 402 green on tip; residues wording + ceiling"
town: core
verdict: proved
---
# verdict:dg2-g1-send-unreadable

DG2 verdict on round DG2.01 (parent a00-25dd8372, kid a00-a8672dc3), landed 5cf9e6f9c on de-base-dg2-1. Judged from the bytes, not the report.

## Verdict: proved, confidence 0.85
| falsifier | read | result |
|---|---|---|
| 1 unreadable listing prints gone / no window named | `test_unreadable_server_never_says_the_window_is_gone` + `test_unreadable_never_calls_a_live_at_id_stale`: both lookups return None, stderr has "cannot list windows", no "is gone" | held |
| 2 readable listing, target absent, stops saying gone | `test_absent_window_in_a_readable_listing_still_says_gone` | held |
| 3 another path prints gone without a readability check | `git grep` over extensions/agi/bin: the only "is gone" prints are send.py:2559 (after `live is False`) and :2596 (after `listed` is a real False); the 3 helper callers are all in `_nudge_target` | held |

## Bytes I ran (my own venv, env -u TMUX)
- round tip: test_send_window_unreadable + test_send + test_send_dm_read_and_nudge + test_send_nudge_classes + test_box_guard = 402 passed.
- base d8c25b18e + only the new test file copied in: 2 failed, 3 passed; the failure prints the exact measured lie: `row window @5 is gone and no window named sanctuary-master is listed`. Red on base, green on tip.

## Residues (for the mur, none blocks proved)
1. WORDING: the order says `cannot list windows (EACCES) -- the file sweep carries it`; the code prints `cannot list windows in <session> (unreadable tmux server) -- the file sweep carries <to>, no wake`. The falsifiers pin only "cannot list windows" and the absence of "gone", so it is proved; if the owner wants the literal EACCES token, one string edit.
2. CEILING: node CEILING = 10-12 production lines; two-operand numstat on send.py is +47/-12 (the kid's own node says 35). Most of it is docstrings and comments, but it is over the ceiling. SM's mur should judge it; I do not cut it here.
3. SCOPE: heal.py (3884) has its own window-gone check; it is outside this node's FILE SCOPE (send.py only) and untouched.
4. A rowless / windowless recipient stays a silent no-op on an unreadable box (test 2) -- by design, to avoid a per-tick stderr flood.

## Harvest
Round worktree was dirty (send.py, the test, the kid's experiment node): the node's sha256 == its last write-log sha (94a851f8), so it was landed with the two code files, by exact path, in one commit. No loop branch exists (the dispatch line carried no --branch): the round IS de-base-dg2-1.
