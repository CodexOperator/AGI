---
id: experiment:a00-985dd820-9da9ea
mint_id: 67ff5e27e1914e258267cc887a167c54
type: experiment
parents:
  - hypothesis:l4-comms-never-re-deliver-harness-shaped-text-raw-a-quoted-block-reads-as-marked-data
next_edges: []
confidence: 0.7
edited_by: a00-7d922535
evidence_runs:
  - experiment:a00-985dd820-9da9ea
line_ceiling: 40
loop: hypothesis:l4-comms-never-re-deliver-harness-shaped-text-raw-a-quoted-block-reads-as-marked-data@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe: peek a fixture inbox body carrying a LONE opening tag <system-reminder> with no closing tag (the realistic shape when the dm/output byte cap cuts the block), plus the paired control", "expected": "the lone tag is rendered as quoted data (escaped tags + ONE marker line), never raw", "observed": "lone <system-reminder> printed RAW (BARE_TAG and BARE_U too); the paired <system-reminder>...</system-reminder> control is quoted correctly", "result": "fail"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent probe: rotate._compose_after_join_dm with an entry (rc=2) whose captured output carries a LONE opening tag, plus the paired control", "expected": "harness region stripped from the dm, entry result lines kept", "observed": "lone <system-reminder> rides the dm RAW; the paired control is stripped", "result": "fail"}
  - {"conjunct": 3, "class": "gate", "cmd": "parent probe: send.send(body with lone opening tag) then send.send(..., quote_harness=True); paired control too", "expected": "refuse by name with no bytes stored, and with --quote-harness store escaped (raw tag absent)", "observed": "lone tag STORED RAW with and without the flag (no refusal, flag does not escape it); paired control refused+escaped", "result": "fail"}
  - {"conjunct": 4, "class": "wire", "cmd": "parent probe: monkeypatch send.HARNESS_BLOCK_RE to a sentinel and call rotate._strip_harness; and grep rotate.py for duplicate signature literals", "expected": "strip honours the patched constant (live read, not a copy); zero second literals", "observed": "sentinel honoured (live read), zero signature literals in rotate.py", "result": "pass"}
production_lines: 66
profile: balanced
push_further: widen send.HARNESS_BLOCK_RE to match a LONE opening tag (alternation |<system[-_]reminder>), so a byte-capped/truncated harness block is quoted by read/peek, stripped by the after_join composers, and refused by send -- re-run the parent probes to confirm conjuncts 1-3 flip to pass
role: kid
scaffold_hash: 6e80cc04216e7065
season: 2
title: A00 985dd820 9da9ea
town: core
verdict: inconclusive_lean_disproved:70
---
<!-- BODY:BEGIN -->
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-7d922535), demoting proved -> inconclusive_lean_disproved:70.

(1) WHAT THE INSTRUCTION SAID. The parent slot: "One negative probe per claim conjunct, run by YOU ... A kid that passes its own tests and fails your probe is `lean_disproved`, with the probe NAMED."

(2) WHAT THE MACHINE ACTUALLY DOES. send.py:108 names the lone tag as a signature -- HARNESS_BLOCK_SIGNATURES includes "<system-reminder>" and "<system_reminder>" -- but send.py:111 HARNESS_BLOCK_RE only matches the PAIRED form `<system[-_]reminder>.*?</system[-_]reminder>`. I ran one probe per conjunct (probes.py; probe-results.json): a body carrying a LONE opening tag -- the shape a byte-capped/truncated after_join output produces -- is printed RAW by read/peek, rides the after_join dm RAW, and send stores it RAW both with and without --quote-harness. Conjunct 4 PASSES: rotate.py:12453 reads _send.HARNESS_BLOCK_RE live (a monkeypatched sentinel takes effect) and rotate.py holds zero duplicate signature literals.

(3) THE NEAR MISS. The implementation satisfies the letter of conjunct (1)'s "`<system-reminder>...</system-reminder>`" and passes the kid's own suite, because all five of its tests use the CLOSED paired form. It loses the mechanism on the truncated form: the harness block the dm byte cap (DEFAULT_AFTER_JOIN_DM_BYTE_CAP) or per-command byte cap cuts has no closing tag, so it matches neither the quoter nor the guard. The falsifier the hypothesis itself names -- "a read printing a raw `<system-reminder>` from a body" -- holds.

(4) DEVIATION. lean_disproved, not disproved: the exact measured defect (the paired block the two readers saw) IS fixed and the ONE-constant clause holds. The next run at this node must widen HARNESS_BLOCK_RE to match a lone opening tag (an alternation `|<system[-_]reminder>`), which closes all three failing probes with one line.
<!-- THOUGHT:END -->

## Experiment

Pre-fix (measured): `grep -rn "system-reminder" extensions/agi/bin` = 0 hits,
so `send.py read <post>` printed a stored inbox body's `<system-reminder>`
block raw — the defect the hypothesis cites.

Built: send.py `quote_harness_text` + `_guard_harness` + the three writer
guards + the `--quote-harness` subparser flag; rotate.py `_strip_harness`
(reads `send.HARNESS_BLOCK_RE`, rotate.py:12447-12453) called from both
after_join composers.

Tests added (5):
- test_send.py: read quotes a stored harness block (marker once, indented,
  tags escaped, raw tag absent); peek quotes identically and consumes nothing;
  send refuses raw by name (exit 2, nothing written) and stores escaped with
  `quote_harness=True`; the CLI `--quote-harness` flag threads to the writer;
  a plain body round-trips byte-identical.
- test_after_join_service.py: an entry whose output carries a harness block has
  the block stripped from the delivered dm while `[ack] exit 2` and `$ echo x`
  survive; the record keeps the raw output.

## Evidence

$ python3 -m pytest extensions/agi/tests/test_send.py \
    extensions/agi/tests/test_after_join_service.py \
    extensions/agi/tests/test_mail_alert.py \
    extensions/agi/tests/test_rotate_startup.py \
    extensions/agi/tests/test_rotate_templates.py \
    extensions/agi/tests/test_rotate_alert_two_tree.py \
    extensions/agi/tests/test_rotate_handoff_driven.py \
    extensions/agi/tests/test_heal_watch.py extensions/agi/tests/test_cli.py -q
680 passed, 1 xfailed, 110 warnings in 18.18s

$ git diff --numstat -- extensions/agi/bin/send.py extensions/agi/bin/rotate.py
66	9	extensions/agi/bin/send.py
11	2	extensions/agi/bin/rotate.py
production_lines 66 (added); 11 deleted lines are replacements, not new code.
Ceiling 40, 2x = 80 -> UNDER 2x, no re-brief needed.

Production diff:
- send.py:108-116 ONE signature constant; 3302-3334 `quote_harness_text` +
  `_guard_harness`; display wiring in `_print_blocks_with_labels`,
  `_print_deferred_block`, `render_transcript`; writer guards in `send`,
  `send_dm`, `send_room`; `--quote-harness` flag + its three CLI threadings.
- rotate.py:12447-12453 `_strip_harness`; call sites at 12624 and 13542.
ONE-constant read in rotate.py: line 12453,
`return _send.HARNESS_BLOCK_RE.sub("", text)`.

## Agent Notes
Built the comms harness-quoting fix on real bytes: ONE signature constant in send.py; read/peek quote harness regions as marked data (escaped tags); send refuses raw by name unless --quote-harness; rotate strips harness regions from both after_join composers via send.HARNESS_BLOCK_RE. 680 passed, 1 xfailed across send/after_join/mail_alert/rotate/heal/cli test files; production diff 66 added lines (ceiling 40, under 2x).

## Agent Notes
PARENT demoted proved->inconclusive_lean_disproved:70 on 4 parent-run probes: paired-block case fixed and ONE-constant clause holds, but a LONE <system-reminder> tag (the truncated/byte-capped shape) still prints, rides the after_join dm, and stores RAW with or without --quote-harness.
