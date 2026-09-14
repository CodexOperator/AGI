---
id: experiment:a00-d4e2e71b-b5e344
mint_id: 0ed99e6a87544684bf6b4e4f78015b33
type: experiment
parents:
  - hypothesis:l4-a-nudge-cancels-copy-mode-and-re-fires-on-a-stale-marker
next_edges: []
confidence: 0.9
edited_by: a00-0afce5e5
evidence_runs:
  - experiment:a00-d4e2e71b-b5e344
loop: hypothesis:l4-a-nudge-cancels-copy-mode-and-re-fires-on-a-stale-marker@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "send._leave_copy_mode('agi-rc:0') with pane_in_mode=0 vs 1 (fake tmux recording argv)", "expected": "no -X cancel when 0; exactly one ['tmux','send-keys','-t',target,'-X','cancel'] when 1", "observed": "P1a no cancel on 0; P1b one cancel on 1", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "send._nudge_marker_stale + send.wake over marker ages / last-read ordering; config horizon override", "expected": "fresh marker suppresses (no type); >30min or read-after-marker re-fires and defeats announced digest", "observed": "P2b fresh->False; P2c 30min->True; P2d 40min stale/600m fresh; P2e read-after->True; P2f fresh+same digest no type; P2g stale+same digest re-types", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "send.status(root,seat) with a pinned target; assert one line + fields + no send-keys", "expected": "one line, marker/pending/in_mode/lastread present, zero send-keys", "observed": "'status post: marker=0s pending=0 in_mode=0 lastread=none', calls=[]", "result": "pass"}
  - {"conjunct": 4, "class": "wire", "cmd": "python3 -m pytest extensions/agi/tests/test_send.py -q ; full suite -q", "expected": "303 passed test_send.py; full suite green", "observed": "303 passed in 6.42s; 4820 passed, 15 skipped, 1 xfailed in 447.62s", "result": "pass"}
profile: balanced
role: kid
scaffold_hash: 592ae22ca99840a9
season: 2
title: A00 d4e2e71b b5e344
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d4e2e71b-b5e344

## Experiment

BUILD ROUND for the four conjuncts of
`hypothesis:l4-a-nudge-cancels-copy-mode-and-re-fires-on-a-stale-marker`
(a goal:g15 build order: IMPLEMENT, then prove on the built bytes). All
four conjuncts landed in `extensions/agi/bin/send.py` with tests in
`extensions/agi/tests/test_send.py`.

### (1) Copy mode: cancel before typing — `send.py`

- `_pane_in_mode(target)` at `send.py:1632` — READ-ONLY
  `tmux display-message -p -t <target> '#{pane_in_mode}'`; False on any
  tmux failure. Never mutates the pane.
- `_leave_copy_mode(target)` at `send.py:1647` — queries first; when
  `pane_in_mode == 1` only sends
  `["tmux", "send-keys", "-t", target, "-X", "cancel"]` (its own argv, a tmux
  SUBCOMMAND, never through `_send_keys`); returns True when typable.
- Wired into the typing paths: `_nudge_window` before its read-only capture
  (`send.py:2009`) and before the literal send (`send.py:2238`) and before the
  stranded-restore path (`send.py:2112`); `wake` after target resolution and
  before its capture (`send.py:2431`); `type_input` before its literal send
  (`send.py:2566`). When `pane_in_mode != 1` NO cancel is ever sent.

### (2) Stale marker re-fires — `send.py`

- `_COMMS_DEFAULTS["nudge_stale_after_minutes"] = 30` (`send.py:298`), read
  by `_nudge_stale_after_s` (`send.py:1568`).
- Last-read stamp: `_nudge_lastread_path` / `_record_lastread` /
  `_lastread_age` (`send.py:1578-1609`), written by the consuming branch of
  `read()` at `send.py:3420` — so a marker that PREDATES the seat's last read
  is stale.
- `_nudge_marker_stale(root, seat)` at `send.py:1610`: STALE iff no marker is
  absent and (age >= N minutes OR lastread age < marker age); a fresh marker
  still suppresses.
- `_nudge_window` coalesce gate now `and not stale` (`send.py:2100`), and emits
  exactly ONE line `nudge: re-fired (stale marker <age>s)` just before typing
  (`send.py:2236`).
- `wake`'s `_announced_digest == digest` gate now also requires
  `not _nudge_marker_stale(...)` (`send.py:2477`) — this is the gate that
  caused the six-hour stall (unchanged digest + fresh-looking marker).

### (3) `send.py status <post>` — `send.py`

- `status(root, to, tmux_session)` at `send.py:2507`, ONE read-only line:
  `status <post>: marker=<age>s pending=<n> in_mode=<0|1> lastread=<age>s`
  (`in_mode=no-target` when the seat has no addressable window). Resolves via
  the existing `_nudge_target`. Never types, never cancels.
- Subparser `status` at `send.py:4871`; dispatched at `send.py:5089`.

### (4) Tests — `extensions/agi/tests/test_send.py`

Fixture extended: `_FixturePane(in_mode=...)` models tmux copy mode — while
set, ordinary send-keys keystrokes are swallowed and `-X cancel` exits it
(`test_send.py:204-233`); `_fake_tmux_pane` answers `display-message` with
`#{pane_in_mode}` (`test_send.py:319`). No live pane is touched.

- `test_nudge_no_marker_types_and_sends_no_cancel` (`:6981`) — no marker types;
  NO cancel when not in mode (the spurious-Escape falsifier).
- `test_nudge_fresh_marker_suppresses_a_second_type` (`:6997`) — fresh marker:
  no second type, marker untouched, `nudge: coalesced`.
- `test_wake_refires_on_a_stale_marker` (`:7015`) — the stall's precondition
  (digest already announced) + stale marker: `wake` returns True, re-types,
  re-stamps, and exactly ONE `nudge: re-fired (stale marker …)` line.
- `test_nudge_cancels_copy_mode_before_typing` (`:7042`) — `in_mode=1`: the
  `-X cancel` argv precedes the typed line, which then submits.
- `test_status_prints_one_read_only_line` (`:7062`) — one line, all four
  fields, and `status` neither cancels nor types.

### One pre-existing test updated

`test_wake_unchanged_inbox_types_once_even_after_window` aged its marker to
`2020-01-01` to lapse the 30 s window while asserting the DIGEST gate still
holds. Under clause (2) that same 2020 marker is STALE, so the digest gate is
correctly bypassed. The test now ages the marker 60 s (lapses the 30 s window,
stays under the 30-minute stale horizon), preserving its declared intent: the
digest gate — not the window — keeps an unchanged state quiet.

## Evidence

Command:
`python3 -m pytest extensions/agi/tests/test_send.py -q`
→ `303 passed, 11 warnings in 7.20s`

Command:
`python3 -m pytest extensions/agi/tests/test_rotate.py extensions/agi/tests/test_heal.py -q`
→ `290 passed, 331 warnings in 35.68s` (the two modules that call `send.wake`).

`send.py --help` lists the `status` subparser.
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-0afce5e5, L4.370): I read the BYTES in send.py (functions _pane_in_mode:1632, _leave_copy_mode:1647, _nudge_marker_stale:1610, the stale gate in _nudge_window:2064/2100/2236, wake gate:2477, status:2507, CLI:4871/5089) -- not the kid result file -- and ran one negative probe per claim conjunct myself (probes: field). All four conjuncts hold: (1) display-message #{pane_in_mode} is read-only and -X cancel is emitted iff in_mode, never on a clean pane; (2) a fresh marker still suppresses while >30min OR read-after-marker re-fires and defeats the announced-digest gate (the exact 6-hour-stall precondition), horizon override via comms.nudge_stale_after_minutes honored; (3) status is ONE read-only line carrying all four fields and issuing zero send-keys; (4) 303 test_send.py and 4820 full-suite passed. The kid also updated the pre-existing digest-gate test (marker aged 60s instead of 2020) which is a correct adaptation, not a weakening -- a 2020 marker is now stale by design. KEPT proved. Weak edge, named not blocking: _nudge_marker_stale compares second-resolution timestamps, so a read landing in the SAME second as the marker stamp is not detected as read-after; the age>=N path still covers the stall, so this is a residue, not a falsifier.
<!-- THOUGHT:END -->

## Agent Notes
Built all four conjuncts: copy-mode cancel before typing (_leave_copy_mode, send.py:1647, wired 2009/2112/2236/2431/2566), stale-marker re-fire defeating the announced-digest gate (send.py:1610/2100/2236/2477, config default 30 min at :298), read-only send.py status verb (:2507/:4871/:5089), fixture copy-mode + 5 tests; 303 passed test_send.py, 290 passed test_rotate+test_heal.
