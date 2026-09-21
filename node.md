---
id: experiment:a00-94617bb7-43045e
mint_id: 7fdf037fa5aa49ebaf29cfd8c6cba8e5
type: experiment
parents:
  - hypothesis:l4-canonical-bytes-are-injective-and-fresh-and-the-ring-gates-the-write-itself
next_edges: []
confidence: 0.8
edited_by: a00-9c00b7ed
evidence_runs:
  - experiment:a00-94617bb7-43045e
loop: hypothesis:l4-canonical-bytes-are-injective-and-fresh-and-the-ring-gates-the-write-itself@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: aab1dc4821f9acb1
season: 2
title: A00 94617bb7 43045e
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-94617bb7-43045e

Kid B on `hypothesis:l4-canonical-bytes-are-injective-and-fresh-and-the-ring-gates-the-write-itself`: closed kid A's two residual injectivity holes, added the FRESHNESS primitive (ts|nonce as fields, canonical_bytes stays PURE), and wired freshness through the three ring gates (verification suite, dispatch round, write config) plus an opt-in read-side veto guard.

## Part 1 — injectivity holes closed (kid A's two measured live DISPROOFS)

Kid A's own caveat reproduced (both printed True on his bytes — a live disproof of the hypothesis as written):

```
python3 -c "import sys; sys.path.insert(0,'extensions/agi/src')
from seatsig import rings as R
print(R.canonical_bytes('g',{'x':{1:'a'}})   == R.canonical_bytes('g',{'x':{'1':'a'}})   )  # was True
print(R.canonical_bytes('g',{'x':(1,2)})     == R.canonical_bytes('g',{'x':[1,2]})       )"  # was True
```

Fixed in `rings.py` — canonical_bytes now recursively type-tags EVERY value AND every dict key via `_enc` (`[tag, content]` JSON): `tuple` gets its own tag (was sharing `list`); a dict keyed by int `1` is forever distinct from its `"1"` str twin. `json_field` (the config-write value serializer) uses the same `_enc` so a gate cannot fuse nested non-str dict keys at the field-string layer either.

AFTER the fix both pairs DIFFER (are injective):

```
pair1 int-key vs str-key dict differ: True
pair2 tuple vs list differ: True
```

The outer canonical shape changed from `{"kind":"g","fields":[["x",["str","1"]]]}` to `{"kind":"g","fields":[[["str","x"],["str","1"]]]}` — purely internal (a reader recomputes it from the persisted fields), so the one format-asserting test (`test_canonical_bytes_injective`) was updated to the new shape; every other existing assertion (order-independence, collisions, type tags, round-trips through verify/decision_cell) still passes unchanged.

## Part 2 — the freshness primitive (`rings.py`)

`DEFAULT_MAX_AGE_S=900`; `fresh_fields(fields, *, ts=None, nonce=None)` adds the reserved `_fresh` = `"<ts>|<nonce>"` (RFC3339/ISO-8601 UTC, `secrets.token_hex(16)`); the input dict is never mutated and a caller-supplied `_fresh` is OVERWRITTEN, never merged (test pins this). `freshness_refusal(fields, *, max_age_s, now, seen, remember)` refuses BY NAME (never a bare False): no `_fresh` / malformed / `age Ns > window Ms` / future clock-skew (>300s) / `replayed nonce '<nonce>'`; `remember(nonce)` fires ONLY on admit, so a refused record never burns its nonce. `nonce_ledger(root)` returns a `(seen, remember)` pair reading `<root>/nodes/.geometry/ring-nonces.json` fresh each call, pruning >24h on remember. Per-ring `max_age_s` is honored via `_effective_max_age_s` when the row carries it (load_rings/ring_by_name pass the raw row through unchanged).

Refusal strings verbatim:

```
record is stale: age 901s > window 900s (ts 2026-09-12T16:53:35Z)
record carries a future _fresh timestamp: ts 2026-09-12T17:13:37Z is 301s ahead (clock-skew guard)
carries no _fresh (ts|nonce) freshness field; refusing replay-by-age on a ring-authorized record
malformed _fresh value 'garbage' (expected '<ts>|<nonce>')
replayed nonce 'rep': a record with this _fresh nonce was already admitted
```

## Part 3 — wiring the gates (fresh fields signed + re-verified on the persisted cell)

The design tension: canonical_bytes must be pure AND the signer/gate/reader must agree on the SAME bytes. So each gate mints the fresh decision ONCE and threads those exact `fields` through sign + gate + persisted decision cell (never argv). Each gate's `_*_refusal` was given a `fields=`/`ring_fresh=` seam: present-use-those-exact-bytes; None-mint-fresh-here. On quorum satisfy, each gate now also calls `freshness_refusal` (with the ring's `max_age_s`) against the nonce ledger and refuses a stale/replayed decision BY NAME.

- `verification.py` — `_suite_grant_fields` returns `rings.fresh_fields({...})`; `_ring_gate_refusal` takes `fields=` and refuses freshness on admit; `main()` computes the grant ONCE and reuses it for the persisted `_suite_decision`.
- `dispatch.py` — `_round_cut_fields` returns fresh fields; `_round_ring_refusal` takes `fields=`, refuses freshness; `main()` mints the round-cut once.
- `write.py` — `_config_write_fields(where, set_fm, *, ts, nonce)` returns fresh fields; `_enforce_written_by` takes `ring_fresh=(ts,nonce)` and refuses freshness in the ring block. Kid C's semantics (unset_fm, the `node` key, `return` vs `written_by`) were NOT touched — the freshness edit is additive and minimal.
- `veto.py` — OPT-IN read-side guard only (see caveat below): `evaluate_veto` refuses a veto DECISION that carries `_fresh` if it is stale; `veto_fields` stays signature-stable so rung 3's tests/stacking path are untouched.

Existing suite-gate tests were updated to hand the gate the exact fresh decision they signed (pinned ts/nonce via `_iso(time.time())` — always within window), which is the honest contract: the signer covers the fresh decision; the gate verifies that very decision.

## Tests (all in `test_rings.py`, plus 2 in `test_veto.py`)

Part 1: no-fuse for int/str dict keys (nested too), tuple-vs-list no-fuse, `json_field` nested-key injectivity.
Part 2: reserved key not spoofable (overwritten, input not mutated); missing/malformed/unparseable `_fresh` refused by name; window (901s refused w/ age+window, 899s + exact-900s boundary admitted); future-skew (301s refused, 300s boundary admitted); replay (same nonce twice — 2nd refused by name; a REFUSED record never burns its nonce); nonce_ledger round-trips across two `nonce_ledger(root)` calls.
Part 3 end-to-end: a FRESH suite-grant admitted / a STALE one refused BY NAME through `verification._ring_gate_refusal` (fixtures only, no real key minted); veto opt-in fresh-admits and stale-refused in `test_veto.py`.

## Evidence — pytest counts

- `test_rings.py test_veto.py`: 53 passed
- `test_verification*.py` (4 files): 71 passed
- `test_dispatch*.py` + write/seatsig/send (eleven files): 577 passed
- rotate suite (test_rotate*.py, dispatch model-allowlist/no-secrets): 293 passed, 1 xfailed
- `test_stream_master_blind_measure_v2.py` has 1 pre-existing FAIL unrelated to this work (a `polite-binding` prompt-injection escape class the live ModelJudge's model now flags — a model-dependent classification test; my changes never touch it).

No real key was minted anywhere; all keys are `_DummyScheme` fixtures. No git commands were run; `cli.py done` owns versioning.

DONE experiment:a00-94617bb7-43045e
caveats: json_field's stored value is a JSON string (round-trips losslessly) — its per-non-str-key injectivity is now guaranteed via `_enc`, but a pre-existing persisted record written under the old `sort_keys` format re-verifies its own (old) canonical fine; only NEW aliasing is closed.
struggles: the gate sign-vs-verify agreement under random freshness forced threading `fields=`/`ring_fresh=` seams through all three gates plus editing six existing tests; the edit tool repeatedly mis-escaped multi-line heredoc blocks (stray `\n`/`n` chars) — worked around with isolated python patch scripts, but each cost a turn.

## Agent Notes
Closed kid A's 2 injectivity holes (int/str dict keys + tuple vs list, both measured live-disproved before, distinct after); added freshness primitive (fresh_fields/freshness_refusal/nonce_ledger) with canonical_bytes PURE; wired freshness through verification/dispatch/write ring gates + opt-in veto read-guard. test_rings 53, verification 71, dispatch/write/seatsig/send 577, rotate 293 all green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW L4.329 (a00-9c00b7ed). Verdict KEPT at inconclusive_lean_proved:80 -- correct, not demoted: the kid's own 80 is honest and the residue below is real.

(1) WHAT THE INSTRUCTION SAID: KID B was told to close kid A's two residual collision holes ("a live DISPROOF of the hypothesis as written"), add freshness as FIELDS with canonical_bytes staying PURE, add freshness_refusal refusing by name, wire the three signed records plus the veto record through one shared path, and prove with tests that a replayed/stale suite-grant is refused and a fresh one admitted. PROOF clause of the hypothesis: "test_rings.py + test_veto.py + test_write* + test_verification* + test_dispatch_dry_run green on the merged round branch; the collision pair pasted onto this node with both byte strings".

(2) WHAT THE MACHINE ACTUALLY DOES -- measured, not read:
- Both A holes closed. I ran the kid's two probes myself: canonical_bytes('g',{'x':{1:'a'}}) != canonical_bytes('g',{'x':{'1':'a'}}) -> True; {'x':(1,2)} vs {'x':[1,2]} -> True. All three of A's pairs still differ. kind is now tagged inside the JSON ({"kind":"g","fields":[[["str","x"],["str","1"]]]}).
- Freshness works. Mine, with calendar.timegm: fresh admitted -> None; stale -> "record is stale: age 960s > window 900s (ts 2026-09-12T16:00:00Z)"; replay -> "replayed nonce 'n1': a record with this _fresh nonce was already admitted"; skew -> "record carries a future _fresh timestamp: ts ... is 600s ahead (clock-skew guard)". A caller-supplied _fresh is overwritten, not merged.
- Wiring is real, not claimed: freshness_refusal is called at verification.py:1031, dispatch.py:1155, write.py:1290, veto.py:299, each against rings.nonce_ledger(root).
- Sign/gate/persist agree on ONE field dict: dispatch.py:1334 mints round_fields once and passes fields=round_fields into _round_ring_refusal at 1337 and into decision_cell at 1350; verification.py does the same at 1137/1149. That is the bug I expected to find and did not.
- suite: python3 -m pytest extensions/agi/tests/ -q --ignore=.../test_stream_master_blind_measure_v2.py -> 4131 passed, 8 skipped, 1 xfailed in 9m32s. The stream_master file the kid called a pre-existing FAIL PASSES on rerun (8 passed) -- a flaky live-model classification test, and it only matches the word "fresh" (grep line 53), so it is unrelated either way.

(3) THE NEAR MISS: the obvious implementation of "the gate also checks freshness" is to call freshness_refusal with its own freshly-minted fields AFTER verify_ring passed -- which verifies the quorum over bytes A and then re-checks the window over bytes B. The kid avoided it by threading fields= through all three gates. The second near miss is making canonical_bytes itself non-pure (stamping ts inside it), which would satisfy "fresh" and destroy sign/verify agreement forever.

(4) DEVIATIONS AND RESIDUE I RECORD RATHER THAN ACCEPT AS CLOSED:
- The kid narrowed the veto wiring to an OPT-IN READ-SIDE guard (veto.py:299, and veto_fields stays signature-stable). That is a deviation from "the three signed records and rung 3's veto record get it through the shared path" -- but it is the right call: rung 3's own expiry_seconds/active_gates are a different lifecycle, and breaking them would break the freeze-never-frees invariant. Recorded, not penalised.
- THE ONE I FOUND AND FOLDED FORWARD: the gates mint `_fresh` with secrets.token_hex(16) INSIDE the process, and there is no CLI seam to supply it. Two calls to dispatch._round_cut_fields with identical argv give _fresh b8d0607288b7474f3f39a46737cfc2cb and _fresh 4e5e955627e24b357d00f7b481e7bf55, and canonical_bytes differ. So no out-of-process signer can ever produce a --ring-sig that matches what --ring-gate will verify: the CLI quorum path with m>0 is un-signable. The hypothesis's own PROOF clause ("the CLI flags end-to-end untested") is therefore still open, and this is why 80 and not a clean proved. Folded into KID D, not re-cut, because the primitive is right and only the seam is missing.
- Minor, recorded: json_field now persists a non-str value in the _enc tagged form, so a config-write field for the int 1 reads as the STRING ["int",1] in the persisted cell (was "1"). Lossless through canonical_bytes and no reader json.loads it, but it is a visible format change a human reading a persisted decision cell will notice.
<!-- THOUGHT:END -->
<!-- THOUGHT:END -->
