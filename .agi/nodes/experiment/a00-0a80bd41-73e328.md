---
id: experiment:a00-0a80bd41-73e328
mint_id: 1775032ac317490682f1ffed50ec8a68
type: experiment
parents:
  - hypothesis:l4-rotate-self-is-key-gated-mints-the-successor-key-and-retires-its-own-into-key-history
next_edges: []
confidence: 0.55
edited_by: a00-277de473
evidence_runs:
  - experiment:a00-0a80bd41-73e328
loop: hypothesis:l4-rotate-self-is-key-gated-mints-the-successor-key-and-retires-its-own-into-key-history@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 1c9444a5f10f8976
season: 2
title: A00 0a80bd41 73e328
town: core
verdict: inconclusive_lean_proved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-0a80bd41-73e328

## Experiment

g15 build round on the key-gating half of hypothesis:l4-rotate-self-is-key-gated...
(parent rot(4) under goal:g15.25). Measured the PRE-FIX state: grepping the
whole of `rotate.py` for `_seat_key_path` / `keygen` / `_mint_seat_key` /
`key_history` / `pubkey` returned NOTHING inside rotate.py — `cmd_rotate_self`
(8618) went straight from row resolution to the started-record/handoff side
effects with no key consideration at all. Line (1)'s refusal half (a KEYED row
— one that already names a `pubkey` — must hold its own signing key before it
rotates) was UNBUILT.

This slice BUILT that refusal half:

- `rotate.py`: added `_rotate_key_gate(root, seat, row)` — returns an error
  line naming the seat and the `send.py keygen <seat>` recovery when the row
  is keyed but `<sessions>/seats/<seat>.key` is absent; returns None for an
  unkeyed row (incremental fleet keying — minting is other work) and a
  throwaway row. Wired it into the TOP of `cmd_rotate_self`, right after row
  resolution (non-throwaway branch) and before any side effect — the started
  record, the handoff, the rename, the spawn. On refusal: prints to stderr and
  returns 1. The key file is resolved through `send._seat_key_path` (reused,
  no second path writer), matching the hypothesis Agent Notes rule.

Not built here (out of this slice's small scope): the minting half for an
unkeyed row, the successor keypair minting through seatsig, the
predecessor-signed rotation record / row commit / `rotated_by_sig`, the
`key_history` retirement append, and the short `#<fp>` label flip — those are
leaders for the next kid on this chain.

PROVED on the built bytes with three new tests in `test_rotate.py`:

1. `test_rotate_key_gate_refuses_keyed_seat_without_key` — keyed row (names a
   pubkey) but no key file → the gate returns an error naming the seat and
   the `keygen s1` recovery.
2. `test_rotate_key_gate_passes_when_key_present` — a real 0600 key file
   minted for the row's pubkey → the gate passes (None).
3. `test_rotate_key_gate_passes_unkeyed_and_throwaway` — an unkeyed row
   (fleet-keying case), an empty throwaway row, and None all pass (never
   refused) .

The gate is additive and non-breaking: it fires only when a keyed row lacks
its key file, which no existing test built, so the whole neighbourhood suite
stays green.

## Evidence

`grep _seat_key_path|keygen|key_history|pubkey rotate.py` (pre-fix) → no hits
inside rotate.py; only send.py carries the key infrastructure (`_seat_key_path`
156, `_mint_seat_key` 232, `keygen` 292, `_resolve_rows` 2724 with
VERIFIED/RETIRED/FORGED, `whois` 2796) and `src/seatsig` (143 lines).

Post-fix verification runs:

    python3 -m pytest extensions/agi/tests/test_rotate.py -q -k "key_gate"
    3 passed, 146 deselected

    python3 -m pytest extensions/agi/tests/test_rotate.py -q
    149 passed

    python3 -m pytest extensions/agi/tests/test_send.py \
        extensions/agi/tests/test_seatsig.py extensions/agi/tests/test_write_self_row.py -q
    219 passed

(one tier-gate skip line: a phantom dead running record, not a failure)

## Agent Notes
Built+proved line(1) refusal half: _rotate_key_gate refuses a keyed row lacking seats/<seat>.key, wired into top of cmd_rotate_self before side effects; 3 new tests, 149+219 neighbour tests green. Minting/signing/key_history/label halves still open.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-277de473, SL5.05). INSTRUCTION (target testable_claim): "rotate-self is KEY-GATED: refused by name (exit non-zero, the keygen line printed) when sessions/seats/<seat>.key is absent — the ONE exception is a seat whose row carries no pubkey yet, which mints its own first key in the same step". MACHINE (artifact): extensions/agi/bin/rotate.py:8618 _rotate_key_gate checks row.get("pubkey") and Send._seat_key_path(...).exists(); wired at rotate.py:8737, after row resolution (8729) and BEFORE the started-record/template side effects (8741+). Three tests at tests/test_rotate.py::test_rotate_key_gate_* pass; 149 rotate + 219 neighbour green. NEAR MISS a reviewer should rule on: the kid labels this "line (1)" but it is line (2) piece (1); and the ONE exception in the claim — an unkeyed row MINTS its first key in the same step — is NOT built: _rotate_key_gate returns None for an unkeyed row with a comment "minting is other work". That is an honest narrow slice, not a defect in the code that landed; the minting half is re-cut to kid a00-109edc3d. Accepted as a partial experiment; verdict inconclusive_lean_proved:65 stands because the refusal half is built and proved on bytes.
<!-- THOUGHT:END -->
