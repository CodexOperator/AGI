---
id: goal:g1.31.4.3
mint_id: 8c1dac5ae4ea44079e568100983bf0b4
type: goal
parents:
  - goal:g1.31.4
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.4.3
goal_kind: subgoal
origin: goals-doc
scaffold_hash: f5120ecb39e76131
season: 2
seeds: []
status: active
tags:
  - engine
  - pass
  - pass-b3
  - write.py
  - canonical-bytes
  - thought
title: "G1.31.4.3: set-to-'<unset>' and unset sign distinct bytes, a blind mint grep is a named rc 2, the thought verb's quoted-only append is tested"
town: core
---
# goal:g1.31.4.3

## Why this exists
goal:g1.31.4: 3 PASS B3 items whose fix lands in write.py / node_writer.py (+ their tests), from 3 rounds:
- `l4-canonical-bytes-are-injective-and-fresh-and-the-ring-gate` (#37, `.agi/sessions/workflows/runs/mur-pb3chunk8of20/verify_l4-canonical-bytes-are-injective-and-fresh-and-the-ring-gate.json`) — OPEN at HEAD ff09c6101 (probe: `_config_write_fields(w,{'k':'<unset>'},None,ts='T',nonce='n') == _config_write_fields(w,None,['k'],ts='T',nonce='n')` → True).
- `engine-delta-5` item 1 (#24, `.agi/sessions/workflows/runs/mur-pb3chunk3of20/verify_engine-delta-5.json`) — FIXED after the tip at 59032171c (DG3, SM residue 102).
- `thought-verb-edits-only-the-top-level-thought-block` falsifier 2 second half (#12, `.agi/sessions/workflows/runs/mur-pb3chunk16of20/verify_thought-verb-edits-only-the-top-level-thought-block.json`) — OPEN.

## Target end-state
- A config-row write that SETS a key to the literal `'<unset>'` and one that UNSETS the key yield different canonical bytes: the unset arm (write.py:1627 `fields[k] = _rings.json_field(UNSET_MARKER)`, marker write.py:1571) no longer shares an encoder and an input with the set arm (write.py:1614) — or a set of the literal is refused by name like the set/unset overlap refusal (write.py:1598-1604). (#37)
- A mint-id target whose grep cannot look exits rc 2 with `ERR: mint lookup could not look: ...`, never a traceback: write.py:3699 `except rotation_record.GrepError`, pinned by `test_w2a_mint_exits_found_unknown_two_carriers_and_a_blind_grep` (extensions/agi/tests/test_links.py:858-874). ALREADY TRUE at HEAD (59032171c). (#24)
- The `thought` verb on a body holding ONLY an indented quoted pair ADDS one column-0 THOUGHT block and leaves the quote byte-identical — the append branch `node_writer.py:1088-1089` (via write.py:3292) is pinned by a committed row in `extensions/agi/tests/test_thought_hygiene.py` (today only :153-154 `extract_thought` → None and :187-190 the splice branch). (#12; hypothesis FALSIFIERS :40-42)

## Invariants
- A residue is closed by a reviewed round, never by a note.
- Every WRITTEN config value is covered by the quorum's signed bytes; distinct decisions never share canonical bytes.
- Tests for these rows are pure-function (no process, no pane).

## Falsifier
1. `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_write_ring_cli.py extensions/agi/tests/test_thought_hygiene.py extensions/agi/tests/test_links.py -q -k "unset_literal or quoted_only_body or blind_grep"` passes with >= 3 tests (1 today: blind_grep), and the pure probe exits 0: `cd extensions/agi/bin && python3 -c "import sys;sys.path.insert(0,'../src');import write as w
try: a=w._config_write_fields('config:seats',{'k':'<unset>'},None,ts='T',nonce='n')
except w.EditError: sys.exit(0)
sys.exit(a==w._config_write_fields('config:seats',None,['k'],ts='T',nonce='n'))"` (exit 1 today: the two decisions are equal).
2. Negative: `git grep -nF 'fields[k] = _rings.json_field(UNSET_MARKER)' -- extensions/agi/bin/write.py` returns zero hits (a str marker through the same str-passthrough encoder as a set value collides by construction).

## Out of scope
goal:g1.31.4.6 (seatsig rings.py:73 `json_field` not injective, #38 — not write.py) · goal:g1.31.4.1 · goal:g1.31.4.2 · goal:g1.31.4.4 · goal:g1.31.4.5 · goal:g1.31.4.7 · the NODE-lane items of the same rounds (#11 thought-verb green evidence on no node, #39 harvest note omits the collision) · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-3**.
