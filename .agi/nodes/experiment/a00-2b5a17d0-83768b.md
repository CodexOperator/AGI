---
id: experiment:a00-2b5a17d0-83768b
mint_id: 0c14b9e132554facbb799c13145d0c28
type: experiment
parents:
  - hypothesis:l5-key-history-retires-a-key-by-fingerprint-never-by-generation-pair
next_edges: []
confidence: 0.9
edited_by: a00-e8270d8c
evidence_runs:
  - experiment:a00-2b5a17d0-83768b
line_ceiling: 4
loop: hypothesis:l5-key-history-retires-a-key-by-fingerprint-never-by-generation-pair@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "auth", "cmd": "parent probe: _successor_row_write(seat=ghost-seat, no seats.md row, real key_rotation dict)", "expected": "refused BY NAME (skipped: no seat-registry row with name ghost-seat); no row created", "observed": "exact named refusal returned; no ghost-seat row exists after the call", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "parent probe: after a real rotation appends fp X at pair (2,3), resubmit the SAME fp X at (2,3) with a different rotated_by_sig", "expected": "history length unchanged: the SAME fp is refused as a duplicate", "observed": "before=2 after=2, unchanged", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "parent probe (counterfactual): row rebuilt as the OLD from,to predicate would leave it (append dropped, pubkey already rotated), sign with the dropped predecessor key, call send._label_for_sig directly", "expected": "FORGED, reproducing the SM.128 incident mechanism (RETIRED path finds no fp match, LIVE path fails under the new key)", "observed": "FORGED", "result": "pass"}
  - {"conjunct": 4, "class": "wire", "cmd": "parent probe: on the POST-FIX row, sign the same message with the same predecessor key, call send._label_for_sig directly (never called by the kid suite directly)", "expected": "RETIRED plus fp, never FORGED", "observed": "RETIRED:4bb70436884ba194", "result": "pass"}
production_lines: 4
profile: balanced
role: kid
scaffold_hash: f1940aa3ca69fbea
season: 2
title: Key-history retires by fingerprint not generation pair -- the rotate-out dedupe predicate
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-2b5a17d0-83768b

## Experiment

WHAT: build the fix for hypothesis:l5-key-history-retires-a-key-by-
fingerprint-never-by-generation-pair, measured pre-fix first, then proved on
the built bytes.

PRE-FIX (the defect reproduced): `_successor_row_write`'s key_history append
deduped on the `(from,to)` generation pair:

    if _ret and not any(h.get("from") == _ret.get("from")
                        and h.get("to") == _ret.get("to")
                        for h in _hist if isinstance(h, dict)):
        _hist.append(_ret)

A test seeded a row whose key_history already carried a `(2,3)` pair under
fp `fp-old`, then offered a DIFFERENT retired key fp `fp-new` at the SAME
`(2,3)` pair. Pre-fix the append was dropped: history stayed at its prior
length (assertion wanted `existing_hist + [retired]`, got `existing_hist`).
That is exactly the live symptom -- after a gen-count reset every re-used
pair drops its retired key, so `send._label_for_sig`'s RETIRED path (which
matches by `fp`) finds no entry and the outgoing post's last lines read
FORGED at an enforcing reader.

FIX (extensions/agi/bin/rotate.py, the ONE dedupe predicate, 4 production
lines):

    if _ret and not any((h.get("fp") or h.get("pub"))
                        == (_ret.get("fp") or _ret.get("pub"))
                        for h in _hist if isinstance(h, dict)):
        _hist.append(_ret)

The retired key's IDENTITY is its fingerprint (fp, falling back to pub),
never the `(from,to)` pair. A repeated pair with a new fp is appended; a
retried write re-offering the SAME fp is still a no-op -- history never
shrinks and never duplicates a key.

POST-FIX measured: the same test passes. `key_history == existing_hist +
[retired]` with `[-1]["fp"] == "fp-new"`; the second, deliberate retry of
`fp-new` leaves the length unchanged (idempotent on fp).

FILE SCOPE respected: extensions/agi/bin/rotate.py (production) and
extensions/agi/tests/test_rotate.py (the falsifier). No repair of already-
dropped entries.

## Evidence

Pre-fix run (test fails exactly on the dropped append):

    $ python3 -m pytest extensions/agi/tests/test_rotate.py -q -k "repeated_generation_pair"
    >       assert own["key_history"] == existing_hist + [fresh["retired"]]
    E       AssertionError: assert [{'fp': 'fp-o...ig-old', ...}] == [{'fp': 'fp-o...ig-new', ...}]
    E         Right contains one more item: {'fp': 'fp-new', 'from': 2, ...}
    FAILED test_key_history_appends_a_repeated_generation_pair_with_a_new_fp

Post-fix run (the new falsifier plus the two neighbouring key_history
tests):

    $ python3 -m pytest extensions/agi/tests/test_rotate.py -q -k
        "repeated_generation_pair or appends_key_history_once or survives_a_rename"
    3 passed, 319 deselected

Whole-file regression:

    $ python3 -m pytest extensions/agi/tests/test_rotate.py -q
    322 passed, 348 warnings in 73.90s

Reader-side regression (the RETIRED path in send._label_for_sig, which
already matched by fp and needed only the entry to exist):

    $ python3 -m pytest extensions/agi/tests/test_send.py -q -k
        "retired or key_history or forged"
    25 passed, 302 deselected

Production diff (measured, read-only):

    $ git diff --numstat -- extensions/agi/bin/rotate.py
    4	2	extensions/agi/bin/rotate.py

Within the 4-line ceiling.

## Agent Notes
Built the fix, not just measured: rotate.py's key_history append now dedupes by the retired key's fp (fallback pub), never the (from,to) generation pair. Pre-fix test dropped a new-fp repeat of a (2,3) pair; post-fix it appends, and a same-fp retry stays a no-op. test_rotate.py 322 passed; test_send.py retired/key_history/forged 25 passed. 4 production lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-e8270d8c, iter 128). (1) Instruction: the target claim says the dedupe predicate must key on the retired key fingerprint (fp, fallback pub), never the (from,to) generation pair, and that a message signed by a dropped predecessor key must label RETIRED:<fp> against a post-fix row, never FORGED. (2) Machine: read rotate.py:9470-9472 pre-review -- confirmed the OLD predicate compared (from,to) only, matching the bug exactly; the kid diff (d92221102..6e0ed3cfe, single commit, 3 changed predicate lines + 2 comment lines, git diff --numstat 4/2) rewrites it to compare (fp or pub). I then built and RAN my own adversarial script (not the kid tests) using the REAL rotate._rotate_successor_key + rotate._successor_row_write + send._label_for_sig with genuine ed25519 keys: GATE probe (resubmitting the SAME fp at the SAME pair is a no-op, len unchanged), WIRE probe (post-fix row + a message signed by the dropped predecessor key -> send._label_for_sig returns RETIRED:<fp>, a call site the kid own suite never exercises), WIRE counterfactual (the row rebuilt exactly as the OLD predicate would have left it -> the SAME signature labels FORGED, reproducing the reported SM.128 mechanism independent of the historical claim), and AUTH probe (an unregistered ghost-seat is still refused BY NAME with no phantom row, so the fix did not loosen the surrounding identity-cells guard). All 4 recorded under probes: all pass. (3) Near miss: a fix that ORs fp with the OLD from/to check (fp OR (from,to)) would pass the kid own suite (which only offers colliding pairs with distinct fps) while still silently deduping a genuinely NEW retirement that happens to reuse both an old fp-less placeholder AND an old pair -- my counterfactual probe is what would have caught that, since it rebuilds the exact dropped-history shape and checks the READER side (_label_for_sig), not just the writer side the kid tested. (4) No deviation from a standing rule: ran the suite for regressions only (322 passed, not cited as my evidence), cited my own probe script output as evidence_runs for the parent round instead. Verdict left at proved -- the fix and the kid own tests hold under adversarial review.
<!-- THOUGHT:END -->

Parent review accepted: rotate.py fix (fp/pub dedupe, 4 production lines) verified against 4 independent adversarial probes (auth/gate/wire x2), all pass; verdict proved stands, confidence 0.9.
