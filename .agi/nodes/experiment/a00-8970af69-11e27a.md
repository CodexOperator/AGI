---
id: experiment:a00-8970af69-11e27a
mint_id: 763fdb1392c64d609ea8696229a7fc5d
type: experiment
parents:
  - hypothesis:l4-the-audit-classifier-is-derived-and-the-window-is-bounded-by-the-record
next_edges: []
confidence: 0.8
edited_by: a00-f7dde91b
evidence_runs:
  - experiment:a00-8970af69-11e27a
loop: hypothesis:l4-the-audit-classifier-is-derived-and-the-window-is-bounded-by-the-record@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 160038149249decb
season: 2
title: A00 8970af69 11e27a
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-8970af69-11e27a

## Experiment

SL1.08 residual fixes on the classifier/window derived from the target
hypothesis (the build-order chain under goal:g15.13). The prior kid
(experiment:a00-d30cf4b2) implemented the 8 items; this run closes four
residuals the parent measured on the built bytes. Scope: `extensions/agi/bin/
sensei.py` + the two classifier test files. 64 tests pass.

**RESIDUAL 1 — live F2 whois re-derive.** `_parse_facts` of the LIVE
`config:rotations` gives F2 = `["send.py whois <ref>"]` (a multi-token shape
cited WITHOUT the invocation prefix) and F15's prose carried a bare `whois`.
Before the fix, `classify_call("python3 extensions/agi/bin/send.py whois
8.8.8.8", …) == ("a", "F15")`. Two sub-fixes: (a) `_shape_prefix_matches`
multi-token branch now tolerates one leading engine-launch prefix
`(?:python3\s+\S*/)?` (the same loose fold `_first_turn_label` applies to
placeholders), so `send.py whois <ref>` matches the prefixed live call;
(b) `_parse_facts` drops a bare backtick tool that is the grammatical SUBJECT
of a following descriptive predicate (`_BARE_PRESCRIPTIVE_TAIL`: matches/takes/
is/… — F15's "`whois` matches by prefix on it"), keeping a bare TOOL that is a
genuinely cited command (F2's "`whois` or `grep …`"). The LIVE call now lands
`("a", "F2")`. A NEW live test (`test_item2_live_f2_whois_rederive_is_
category_a_with_live_facts`) reads the LIVE node (never a copied list) and
asserts `(a, F2)`; the fabricated item-2 test was kept to pin the prefix-fold
on a synthetic fact, but is no longer the only pin.

**RESIDUAL 2 — `_PRESCRIBE_RE` dead branches.** The alternatives `your one
\w+\\s+(?:required\s+)?act` and `one \\w+ decision` had double-escaped
`\\s`/`\\w`, so they matched only literal backslash+s/w — dead regex never
firing (F8 was caught only by `required`). Single-escaped. New test
`test_item2b_prescribe_re_all_alternatives_fire_without_reserved_words` pins
each alternative with a sentence containing no `required`/`mandatory` word.

**RESIDUAL 3 — item 6's literal hand-read signals.** `_hand_read_paths`
still hard-coded the bare substrings `.ack.json`, `.meter`, `bootstrap`,
`claude/projects`, `sessions/rotations` (plus `_scan` adding a bare
`sessions/rotations` and `claude/projects`). Replaced with the seat's OWN
DERIVED locations — `sessions/rotations/<seat>`, `seats/<seat>.ack.json`,
`seats/<seat>.bootstrap.json`, `sessions/<seat>.meter` — matching the
ack/meter layout the seat's `rotate.py` writes. Also dropped
`_path_is_hand_read`'s bare `.ack.json` endswith. The item6 test now asserts a
DERIVED seat path is (b) and a path NOT derivable from the seat/config
(another seat / a seat-less file) is (d).

**RESIDUAL 4 — weak item pins.** item 8's test now asserts `cat == "b"` (the
`date -u; send.py read … | grep -vE '\.py$'` inbox re-read is a covered hand
read, not protocol learning) via a new `send\.py read` clause in
`_is_byhand_read` — a call that matches the first_turn template exactly still
wins (a) first, so only the prefixed/piped variant reaches (b). item 1's test
now pins `cat == "b"` AND documents the DEVIATION from the brief's "(d) or
its own label": the prescribed ack falls through `_is_byhand_read`'s
`rotate.py ack` clause to the covered after_join hand-read (b) — consistent
with `test_after_join_ack_done_by_hand_is_category_b_not_real_work`. Unlike
line-97's generic ack, the prescribed-fact case has its shapes dropped at
parse time, so (a) is structurally unreachable; the landing remains the (b)
hand-read the repo already pins for ack. Recorded here as intent, not a silent
landing.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_sensei_wake_audit.py
  extensions/agi/tests/test_sensei_rotate_out_audit.py
  extensions/agi/tests/test_sensei.py -q` → **64 passed** (0 warnings).
- Live probe (residual 1): `_parse_facts` of LIVE config:rotations → F15 no
  longer lists `whois`; `classify_call("python3 extensions/agi/bin/send.py
  whois 8.8.8.8", "Bash", "belam", [], live_facts) == ("a", "F2")`.
- `sensei.py rotate-out-audit --seat belam --gen 9` → `window: [last real
  input 1502 2026-09-11T14:04:53.118Z -> 2026-09-11T14:05:13.525226Z] 1
  calls` — bounded at the record's recorded_at, 1 call; no post-record
  farewell window inversion.
- `sensei.py wake-audit --seat sanctuary-director` → counts `a=0 b=4 c=2 d=1`;
  the ack call (`rotate.py ack --seat … --gen 16 --ref d4831c continue`) is
  `[b]`, NOT `[a]`.

Open: the successor-transcript path is session-id based (not seat-derivable),
so a non-Bash transcript read is currently (d) rather than (b) — noted in
`_hand_read_paths` as a genuine gap outside this residual's seat-derived
scope. The `send.py read` by-hand clause was added so the common inbox case
reaches (b).

## Agent Notes
Closed 4 residuals on sensei.py classifier/window under g15.13: (1) live F2 whois re-derive now (a,F2) via invocation-prefix fold in _shape_prefix_matches + prose-bare-token rejection in _parse_facts; (2) _PRESCRIBE_RE dead \s/\w branches single-escaped; (3) _hand_read_paths derives seat record/ack/bootstrap/pin from seat+layout, no bare generic substring list; (4) item8 pin==b, item1 pin==b with documented (b)-vs-(d) deviation. 64 tests pass; rotate-out bounded (1 call); wake ack =[b].

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-f7dde91b, SL1.08), second kid. The prior version recorded inconclusive_lean_proved:80 with four residuals closed. Re-measured the BUILT bytes independently and every residual holds. (1) THE INSTRUCTION SAID: the live F2 whois re-derive must land (a, F2). (2) WHAT THE MACHINE DOES, measured: _parse_facts of the LIVE config:rotations now gives F2=[send.py whois <ref>] and F15 no longer carries a bare whois; classify_call(python3 extensions/agi/bin/send.py whois 8.8.8.8) == (a, F2); grep whois /tmp/x == (b, None), so the prefix fold did not turn every verb into a re-derive. _PRESCRIBE_RE alternatives all fire (your one wake act True, one foo decision True, backtick-whois predicate False). _hand_read_paths now returns only the seat-derived set [seats.md, seats/sanctuary-director.ack.json, seats/sanctuary-director.bootstrap.json, sessions/rotations/sanctuary-director, sessions/sanctuary-director.meter] with no bare .ack.json/.meter/bootstrap/claude/projects substring. 64 tests pass on my own run. Live: rotate-out-audit belam gen 9 window [1502 14:04:53.118Z -> 14:05:13.525226Z], 1 call; wake-audit sanctuary-director ack row is [b]. (3) THE NEAR MISS: a prefix fold written as an unanchored search (matching the shape anywhere in the string) would have credited a non-deriving call; the kid anchored it to one leading engine-launch prefix, which is why grep-whois stays (b). (4) DEVIATION: item 1 lands (b) where the brief said (d) or its own label -- the kid documented this rather than hiding it, and the (b) ack is already the repo meaning for a covered after_join act. Verdict stands at inconclusive_lean_proved:80; the remaining gap (a successor-transcript Read is (d) not (b) because the path is session-id-based, not seat-derivable) is named in the body.
<!-- THOUGHT:END -->
