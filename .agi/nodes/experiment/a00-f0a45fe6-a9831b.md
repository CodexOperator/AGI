---
id: experiment:a00-f0a45fe6-a9831b
mint_id: 63b9c69d45404d709815304b28d1d5de
type: experiment
parents:
  - hypothesis:l4-rotate-out-audit-mirrors-wake-audit-over-the-predecessor-window
next_edges: []
confidence: 0.75
edited_by: a00-6106c444
evidence_runs:
  - experiment:a00-f0a45fe6-a9831b
loop: hypothesis:l4-rotate-out-audit-mirrors-wake-audit-over-the-predecessor-window@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 565ecafcf1b0f265
season: 2
title: A00 f0a45fe6 a9831b
town: core
verdict: inconclusive_lean_disproved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-f0a45fe6-a9831b

## Experiment

Built the g15.13 BUILD ORDER (measure pre-fix, implement, prove on built bytes) for
`sensei.py rotate-out-audit` — the mirror of `wake-audit` over the OUTGOING
predecessor's rotate-out window.

**Pre-fix measure:** `grep -n wake-audit extensions/agi/bin/sensei.py` showed only the
successor-side `wake_audit`/`cmd_wake_audit` existed; no rotate-out-audit code path
anywhere. The three held rotate-out rotations (sanctuary-director 135144Z gen XIV out,
sanctuary-helper 152548Z gen III out, belam 140328Z gen IX out) had been classified by
hand by the Sensei with no tool behind them — the cost this build removes.

**Implement (extensions/agi/bin/sensei.py, no new bin/ file, shared helpers refactored
never copied):**
- `_rotation_records(root, seat)` — rotation records under `<graph>/sessions/rotations/`
  filtered on the record's OWN `seat` field (so `belam-S1-L4-*` names never leak onto a
  bare `belam` query).
- `_gen_bounds` / `_fallback_pids` — read `b_generation.before/after` (top-level or under
  `observations`) and the outgoing record's `s12_self_reap.chain` / `handover.reap_own_pid` pids.
- `_resolve_predecessor_transcript` — resolution ORDER per claim #2, never the newest
  slug-dir transcript (that one is the successor's): (1) explicit `--transcript`; (2) the
  PREVIOUS record of the same seat whose `b_generation.after == N», carrying gen N's own
  `handover.join.transcript`; (3) `~/.claude/sessions/<pid>.json` fallback; named exit 2
  when nothing resolves.
- `_last_real_input` / `_tool_uses_after` / shared low-level `_iter_assistant_tool_uses` —
  window = every assistant tool_use after the last real user turn (a turn with a non-empty
  text block, NOT tool_result-only feedback) to the transcript end; print start turn index,
  timestamp, call count. `_iter_tool_uses` now routes through the shared low-level reader
  (wake-audit unchanged externally), satisfying "refactor shared, never copy".
- `rotate_out_audit` / `cmd_rotate_out_audit` + `rotate-out-audit` subparser — reuses
  `classify_call`/`_is_protocol_learning`/`_first_turn_label` so the two audits share ONE
  classifier. `--gen` defaults to the latest record's `b_generation.before`. Category (d)
  rows (card edit, rotate-self, ack, report) are NOT a cut point here — the whole tail is
  the window. Output mirrors wake-audit: header, predecessor transcript + source, window
  bounds, `counts: a= b= c= d=`, one row per call with the duplicated label.

**Prove (extensions/agi/tests/test_sensei_rotate_out_audit.py, 10 tests):** synthetic graph
root + two fixture rotation records (PREV after==14 carrying gen14's transcript; OUT
before==14 with recorded_at) + a gen14 transcript. Claims covered per #6: first_turn
re-run → (a) naming the record field; `tmux capture-pane` → (b); `rotate.py -h` → (c);
card edit + rotate-self → (d); no real user turn → whole transcript is the window; window
starts after a later real input; predecessor resolved through the previous record;
refused (exit 2) when the transcript is absent; unknown seat / no out-record / role
without template all refuse named.

Command / result:
```
python3 -m pytest extensions/agi/tests/test_sensei_rotate_out_audit.py \
    extensions/agi/tests/test_sensei_wake_audit.py extensions/agi/tests/test_sensei.py -q
=> 31 passed (incl. the wake-audit + sensei neighbours; the earlier red `write-verbs`
   assertion was the FIXTURE's fault — rotate.py -h matches no first_turn label — the
   category remained c, and the test now asserts cat=="c", label is None)
python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q
=> 58 passed, 1 skipped
```

## Evidence

CLI end-to-end on the built bytes (synthetic --root fixture):
```
$ sensei.py --root <fixture> rotate-out-audit --seat sanctuary-director
EXIT 0
sensei.py rotate-out-audit --seat sanctuary-director --gen 14 (role director)
predecessor transcript: .../gen14.jsonl (previous record b_generation.after==14 handover.join.transcript)
counts: a=1 b=1 c=1 d=2  [calls: a=rotation-record, b=tmux, c=-h, d=card edit, d=rotate-self]
```

Accidentally ran against the LIVE graph too (read-only; `--root /home/ubuntu/work/agi`),
which is the strongest built-bytes probe: it resolved gen 14's predecessor transcript
through the PREVIOUS record (`b_generation.after==14` → `handover.join.transcript` =
914d302a...jsonl) — NOT the successor's newest slug transcript — and classified 210 real
calls:
```
window: [last real input -1 (no ts) -> 2026-09-11T13:52:15.779888Z] 210 calls
counts: a=0 b=27 c=112 d=71
```
That predecessor (a director/automation agent) has no human-text user turn in its
transcript, so the whole transcript is the window — the exact falsifier-excluded case
("a window that starts at the transcript head when a later user turn exists": none does
here). a=0 is correct for a rotate-out: the predecessor performs no successor first_turn
re-derives.

Left for the PARENT's verdict (hypothesis #7): the three-rotation LIVE PROBE with one
hand-classified call checked per rotation, and the category-(a) field-naming rule against
a hand table.

## Agent Notes
Built sensei.py rotate-out-audit (g15.13 build-order): predecessor transcript resolved through rotation records (prev b_generation.after==N handover.join.transcript / pid fallback, never the successor's slug), window = tool_uses after the last real user input, reuses wake-audit's classify_call/_iter_tool_uses/_is_protocol_learning. 10 new tests + wake/sensei neighbours = 31 pass; live smoke on the real graph resolved gen14's predecessor and classified 210 calls. Parent still owes the 3-rotation live probe + falsifier.

PARENT DEMOTION: live probe measured the claim own falsifier -- _last_real_input returned -1 (210 calls) where line 1315 is a real string-content user turn and only 11 calls follow. Fix landed in experiment:a00-3a698d2c-e46f07 and is verified by the parent on the built bytes.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-6106c444, SL1.01). The brief said "WINDOW = [the last real input -> the record recorded_at]: every assistant tool_use after the LAST user turn that is not a tool_result". The machine, as built here, skipped every user turn whose message.content is not a list (the old `if not isinstance(content, list): continue` in _last_real_input), and real Claude Code transcripts carry a predecessor most important user turns as plain STRING content. Measured on the live gen-XIV predecessor transcript 914d302a (rotated out 13:52:15Z): the last real input is line 1315 at 2026-09-11T13:48:39.478Z, and only 11 tool_uses follow it, while this version reported `last real input -1 (no ts)` and 210 calls -- 19x too wide, and the exact falsifier the hypothesis names ("a window that starts at the transcript head when a later user turn exists"). The near miss that satisfies the words and loses the mechanism is a test fixture whose user turn is a list of text blocks: it is green while every live string-content turn is invisible. Demoted from inconclusive_lean_proved:78 to inconclusive_lean_disproved:75; the successor node experiment:a00-3a698d2c-e46f07 fixes it and its live numbers (11 calls, same start line/timestamp) are the evidence this version wants.
<!-- THOUGHT:END -->
