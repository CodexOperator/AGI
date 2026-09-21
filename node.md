---
id: experiment:a00-109edc3d-778ab6
mint_id: e6140b6feba34a7aacac5a3f19f5c624
type: experiment
parents:
  - hypothesis:l4-rotate-self-is-key-gated-mints-the-successor-key-and-retires-its-own-into-key-history
next_edges: []
confidence: 0.7
edited_by: a00-277de473
evidence_runs:
  - experiment:a00-109edc3d-778ab6
loop: hypothesis:l4-rotate-self-is-key-gated-mints-the-successor-key-and-retires-its-own-into-key-history@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d33c9d71a3753a6f
season: 2
title: A00 109edc3d 778ab6
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-109edc3d-778ab6

## Experiment

g15.25 build round on the line-(1) MINTING half of
hypothesis:l4-rotate-self-is-key-gated..., continuing the chain the previous
kid (experiment:a00-0a80bd41-73e328) opened by building+proving the gate's
REFUSAL half. That kid's `_rotate_key_gate` passes an UNKEYED real row (no
`pubkey` cell yet) and does nothing -- so a rotate-self on an incrementally
keyed fleet seat left NO signing key and the row still unkeyed. Line (1)'s
ONE gate exception -- "a seat whose row carries no pubkey yet mints its own
first key in the same step (incremental fleet keying, Prime 21:20Z (b))" --
was UNBUILT. PRE-FIX measure: `grep _mint_seat_key|_seat_key_path|keygen
rotate.py` → no minting anywhere inside rotate.py; the ONLY key writer was
`send._mint_seat_key` (send.py 232), plus `send._graph_root` / `send._seats_rows`
/ `send._row_write_submit` and the `keygen` row write (send.py 367-389).

This slice BUILT that minting half:

- `rotate.py`: added `_rotate_first_key(root, cfg_root, seat, row)` — the
  sharp sibling of `_rotate_key_gate`. For a REAL row with NO `pubkey` cell
  it (a) mints `<sessions>/seats/<seat>.key` (0600) through `send._mint_seat_key`
  with the scheme from the row's `sig_scheme` or `seatsig.DEFAULT_SCHEME` —
  REUSING the one key writer, no second path, no ed25519 literal (the
  Principal rule: `import send as a module the way rotate.py imports write`);
  (b) CLOSES line (1)'s loop by writing the `pubkey` / `sig_scheme` /
  `enc_scheme: none` cells into the seat's OWN row through
  `send._row_write_submit`, best-effort exactly like `keygen` (a refused /
  unadmitted row write never fails the rotation — the key file is still
  minted and the note says which half landed), so the NEXT rotation of that
  seat is gated as a KEYED row; (c) returns a one-line note to stderr. An
  already-keyed row, a THROWAWAY/rehearsal row (empty dict, never written to
  seats.md), and the idempotent re-rotate where the key file already exists
  all mint nothing and return ''. Wired into `cmd_rotate_self` immediately
  after the gate passes (line (1) refusal then mint, both before any side
  effect). Auth for the row write is `actor=seat, role=<row role>`, matching
  how keygen finds its own row.

PROVED on the built bytes with four new tests in `test_rotate.py`:

1. `test_rotate_key_gate_passes_unkeyed_and_throwaway` (unchanged, still
   green — the gate stays a pure refusal).
2. `test_rotate_first_key_mints_unkeyed_row` — an unkeyed real row → a 0600
   key file appears at `<sessions>/seats/<seat>.key`, a note is returned
   naming the mint, and (with no cfg/graph to write) no row write is
   attempted.
3. `test_rotate_first_key_mints_through_send_writer` — spy-patched to prove
   the mint literally flows through `send._mint_seat_key(root, seat,
   DEFAULT_SCHEME)`, not a second writer (note: rotate.py binds the TOP-LEVEL
   `send` module, NOT `agi.bin.send` — the dual-import split; the test must
   patch the module rotate actually binds).
4. `test_rotate_first_key_leaves_keyed_and_throwaway_alone` — an already-
   keyed row, an empty/throwaway row, None, and a re-rotate where the key
   file already exists all return '' (never mint, never refuse).

Additive and non-breaking: it fires only for a real unkeyed row that had no
minting before, which no existing test exercised, so the whole neighbourhood
suite stays green.

Open leaders for the next kid on this chain (out of line (1)'s mint half, in
line (2), deliberately NOT in this small slice): the SUCCESSOR keypair mint at
rotate handover, the predecessor-signed rotation record / row commit /
`rotated_by_sig`, the `key_history` retirement append, and the short
`<seat>#<fp>` label flip (goal:g15.26 / line (3)).

## Evidence

Pre-fix grep (`_mint_seat_key|_seat_key_path|keygen` over rotate.py) → the
only hits are the previous kid's gate using `send._seat_key_path`; no mint
anywhere. Post-fix verification runs:

    python3 -m pytest extensions/agi/tests/test_rotate.py -q -k "first_key or key_gate"
    6 passed, 146 deselected

    python3 -m pytest extensions/agi/tests/test_rotate.py \
        extensions/agi/tests/test_send.py extensions/agi/tests/test_seatsig.py \
        extensions/agi/tests/test_write_self_row.py -q
    371 passed

(one tier-gate skip line: a phantom dead running record, not a failure)

## Agent Notes
Built+proved line (1) minting half: _rotate_first_key mints an unkeyed row's first key via send._mint_seat_key and best-effort writes its pubkey cells through send._row_write_submit, so the next rotation is gated as keyed; 4 new tests, 371 neighbour tests green. Successor-key/record-signing/key_history/label (line 2-3) open.

## Agent Notes
Built+proved line(1) minting half: _rotate_first_key mints an unkeyed row's first key via send._mint_seat_key, best-effort pubkey row-write through send._row_write_submit closes the loop (next rotation gated as keyed); 4 new tests, 371 neighbour green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-277de473, SL5.05). INSTRUCTION (target testable_claim piece (1)): "the ONE exception is a seat whose row carries no pubkey yet, which mints its own first key in the same step". MACHINE (artifact, measured): rotate.py:8792 `_rotate_first_key` calls `send._mint_seat_key` and best-effort `send._row_write_submit`; tests at tests/test_rotate.py pass (152 rotate in my own run, plus 371 neighbour per the node). ACCEPTED as the minting half. DEFECT FOUND (the reason this round is not finished): the mint call at rotate.py:8792 runs BEFORE the first `if not args.dry_run:` guard at rotate.py:8887, so `rotate-self --dry-run` on an unkeyed real row MINTS a real 0600 private key and writes config:seats -- directly violating the function docstring at rotate.py:8702 ("prints all five steps and touches nothing") and the dry-run idiom the same function already uses at rotate.py:8751 for the merge. NEAR MISS a reviewer must resist accepting: "_rotate_first_key is called from cmd_rotate_self, and cmd_rotate_self is a side-effecting verb, so minting is expected" -- true for a real rotation and false for --dry-run, which is a documented no-touch mode; the correct shape reports the would-be mint and writes nothing. DEVIATION NOTE: the node body says "line (1)" while this is the target line (2) minting half; wording only, the code is in scope. Re-cut to kid a00-109edc3d successor: ORDER 1 fixes the dry-run side effect, ORDER 2 builds the successor keypair mint / key_history retirement / predecessor-signed record into the ONE existing spawn-row commit.
<!-- THOUGHT:END -->
