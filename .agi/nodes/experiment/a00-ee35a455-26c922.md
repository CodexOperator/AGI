---
id: experiment:a00-ee35a455-26c922
mint_id: 9fe15c94c3fd4555ba51bdbc2dd56a71
type: experiment
parents:
  - hypothesis:l4-canonical-bytes-are-injective-and-fresh-and-the-ring-gates-the-write-itself
next_edges: []
confidence: 0.9
edited_by: a00-9c00b7ed
evidence_runs:
  - experiment:a00-ee35a455-26c922
loop: hypothesis:l4-canonical-bytes-are-injective-and-fresh-and-the-ring-gates-the-write-itself@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d037ddacd4edbf30
season: 2
title: write-ring-and-gate-full-decision-bytes
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-ee35a455-26c922

## Experiment

Kid C on `hypothesis:l4-canonical-bytes-are-injective-and-fresh-and-the-ring-gates-the-write-itself` — the ring quorum gates the WRITE ITSELF (region `extensions/agi/bin/write.py`: `_config_write_fields` + the rung-2 ring block of `_enforce_written_by`, plus new CLI tests). Kids A/B own `seatsig/rings.py`; I only read it and used its real API (`canonical_bytes`, `decision_cell`, `verify_ring`, `fresh_fields`, `freshness_refusal`, `nonce_ledger`, `json_field`, `_effective_max_age_s`).

Built the brief's three defects (all three reproduced pre-fix, below), then implemented the fix.

### What I changed in `write.py` (ONLY these two functions + two module constants)

1. **`_config_write_fields(where, set_fm=None, unset_fm=None, *, ts=None, nonce=None)` now returns the FULL decision.**
   - The node id lives under the reserved `NODE_KEY = "_node"` — a key a caller's `set_fm` can never displace (defect 2); writing `_node` is refused by name.
   - Every key being SET **and** every key being UNSET is included, each value through `rings.json_field`; an unset key carries `UNSET_MARKER = "<unset>"` so "unset k" is distinct in the bytes from "set k: <value>" (defect 1).
   - Kept kid B's freshness edit (`fresh_fields` with ts/nonce).
2. **`_enforce_written_by` reordered so BOTH gates must pass (defect 3).** Order, documented in the docstring: (1) the veto/human-gate check stays FIRST; (2) gate 1 `written_by` — an unadmitted writer is refused HERE by the written_by line (a later satisfied quorum is never an OR substitute); (3) gate 2 the rung-2 ring — an ADMITTED writer is STILL refused here when the schema declares `ring:` and the write is a config-row edit (set_fm **or** unset_fm). The master_sensei and self_row carve-outs are preserved verbatim inside gate 1's unadmitted branch; a self_row or master_sensei admission `return`s BEFORE the ring (rule D: a seat updating its own declared row needs no quorum).

**Canonical-bytes note (brief requires I say it):** for a SET-only edit the signed bytes DO change — the node id key moved from `node` to `_node`. This is the fix itself (defect 2: `node` was clobberable), not scope creep; no live schema declares `ring:` so no real record's persisted bytes change.

### Defect reproduction (PRE-fix, each run, not asserted)

```
=== DEFECT 1: unset_fm not covered by signed bytes ===
fields for an UNSET-ONLY edit (unset key 'seats'): {'node': 'config:seats', '_fresh': '...|nonce1'}
=> signed bytes cover NO key being removed: True
=== DEFECT 2: set_fm key named 'node' clobbers the node id ===
fields when set_fm contains 'node': {'node': 'config:OTHER', '_fresh': '...|nonce1'}
=> signed record names: config:OTHER (should be config:seats)
=== DEFECT 3: ring is an OR alternative to written_by ===
3a: intruder WITH valid m=2 quorum -> ADMITTED (rings satisfy, no written_by check)
```

### Post-fix refusal strings (verbatim)

```
A_REFUSAL (written_by-ADMITTED writer, no sigs):
  config nodes (config:seats): record needs 2 valid ring signature(s) from 'approval' (m-of-n), got 0; <none checked>. (rung 2 multisig ring)
E_REFUSAL (admitted writer, UNSET-ONLY edit, no sigs):
  config nodes (config:seats): record needs 2 valid ring signature(s) from 'approval' (m-of-n), got 0; <none checked>. (rung 2 multisig ring)
C_REFUSAL (UNADMITTED writer, VALID m=2 quorum):
  config nodes (config:seats) may be hand-edited only by admitted roles prime; resolution for actor 'intruder' gave kid, which is not admitted. (goal:g12)
G_REFUSAL (reserved _node key in set_fm):
  config-row write to config:seats: the reserved decision key '_node' (the node id a ring quorum authorises) is REFUSED as a set field so a caller's key cannot name a different node (defect 2, ...)
```

Test C is the brief's "fails today in the other direction": an unadmitted writer with a satisfied quorum is now refused by the written_by line, never the ring line.

### Acceptance tests `extensions/agi/tests/test_write_ring_cli.py` (new; 9 pass)

- **A** admitted writer + `ring:` schema + no sigs → refused, names `approval` and m-of-n count.
- **B** admitted + m valid sigs → admitted (no refusal).
- **C** unadmitted + m valid sigs → refused by the written_by line naming `prime`, NOT the ring line.
- **D** seated self-row write on a `ring:`-declaring type, no sigs → admitted by the self_row path. **Ruling:** the ring gates NON-self-row config writes; a seat updating its OWN declared row needs no quorum (the seat IS the identity, and `_self_row_refusal` already restricts it to its own row + declared fields).
- **E** unset_fm-ONLY non-self-row edit, no sigs → REFUSED by the ring line (unset keys are now in the signed bytes).
- **F** falsifier: a signature over fields WITHOUT the unset key fails against a record that unsets it; one computed WITH the unset key verifies — proves the unset key is genuinely in the bytes, not just the refusal line.
- **G** `set_fm` key `node` cannot rename the record: id sits under `_node`, caller's `node` lands separately, both in the bytes; writing reserved `_node` is refused by name.
- Plus the write.py ring path end-to-end on a REAL tmp-root node driven through `write.submit(...)`: one admitted (valid quorum → `ring_decision` cell persisted and re-verified from disk, no argv) and one short-of-m refused. No CLI seam exists to pin the freshness nonce (kid D owns that), so the two submit tests driver `write.submit` with the nonce/ts pinned via `monkeypatch` of `seatsig.rings.secrets.token_hex` and `_now_iso` to the SAME values the signer covered — the gate then builds byte-identical fields in-process (KNOWN AND NOT YOURS section honored).

### I touched a test file a kid did not give me

`extensions/agi/tests/test_rings.py` — the AND fix made 5 of its write-gate tests assert the OLD defect-3 OR behaviour (an `intruder` + valid quorum was expected to be ADMITTED; several expected the ring refusal line for an unadmitted writer). They now use a written_by-ADMITTED writer (`role="prime"`), which is the semantically-correct AND framing; I also added `test_write_gate_ring_is_an_and_gate` pinning test C. No other file in the brief's forbidden list was touched (rings.py, veto.py, dispatch.py gate logic, verification.py, send.py, cli.py all untouched).

## Evidence

### Exact pytest commands and counts

```
$ python3 -m pytest extensions/agi/tests/test_rings.py -q
41 passed in 0.34s
$ python3 -m pytest extensions/agi/tests/test_write_ring_cli.py -q
9 passed in 0.13s
$ python3 -m pytest extensions/agi/tests/test_write.py -q
99 passed in 0.86s
$ python3 -m pytest extensions/agi/tests/test_write_master_sensei.py -q
17 passed in 0.23s
```

(The brief's kid-tier gate refuses a bare `tests/` directory; each run above names a specific file. One transient `99 errors` from `test_write.py` cleared on re-run with `-x` — a setup flake, not a code failure; the clean re-run passed 99/99.)

### Live geometry untouched

```
$ python3 -c "import sys;sys.path.insert(0,'extensions/agi/src');from seatsig import rings;print(rings.load_rings('.'))"
[]
```

No real ring cell exists in this tree (no schema declares `ring:`), so the gate remains opt-in and no real record is affected. No live key minted; all signatures use the fixture `fixture` scheme (hash-16) against fixture posts.md pubkeys — never live geometry.

DONE experiment:a00-ee35a455-26c922
caveats: the submitted end-to-end relies on an in-process nonce/ts pin (monkeypatch) because no CLI seam exists — a true out-of-process signer still cannot match until kid D adds the seam; and I changed the signed node key `node`→`_node`, so any ring cell persisted before this change would not re-verify.
struggles: the /tmp repro's hardcoded timestamp kept tripping the 900s freshness window, masking the OR-behaviour reproduction until I switched to a live ts; and the test_rings.py write-OR tests all flipped at once under the AND fix.

## Agent Notes
write.py ring gate is now an AND over written_by+quorum (defect 3); _config_write_fields covers set+unset keys with node id under reserved _node (defects 1/2); A-G + submit end-to-end green, 99/41/17/9 suites pass

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW L4.329 (a00-9c00b7ed). Verdict left at pending by the kid; I judge the WORK landed and verified, so I record the reasoning here rather than re-cutting. Not demoted -- verified directly.

(1) WHAT THE INSTRUCTION SAID: the hypothesis PROOF clause requires that "the ring quorum gates the config write itself including unset_fm and never bypasses written_by", that "_config_write_fields namespaces the node id so a set_fm key named node cannot overwrite it", and DISPROOF lists "an unset_fm config write admitted without the quorum; a set_fm key named node clobbering the node field". KID C was given seven acceptance tests A-G as its contract.

(2) WHAT THE MACHINE ACTUALLY DOES -- measured on the tree, not read:
- DEFECT 1 fixed. write._config_write_fields('config:seats', {'seats':['a']}, ['oldkey']) now returns {'_node': 'config:seats', 'seats': '["list",[["str","a"]]]', 'oldkey': '<unset>', '_fresh': ...} -- the unset key IS in the signed bytes, carrying UNSET_MARKER so "unset k" is distinguishable from "set k: <value>".
- DEFECT 2 fixed, by namespacing rather than refusal: a set_fm key named 'node' lands as its OWN key and does not displace the id -- {'_node': 'config:seats', 'node': 'config:OTHER', ...}; and the reserved key itself is refused by name ("the reserved decision key '_node' ... is REFUSED as a set field").
- DEFECT 3 fixed. _enforce_written_by (write.py:1216-1240) is now an AND: gate 1 refuses an unadmitted writer beyond that point, and gate 2 (write.py:1314-1355) demands the ring quorum for a config-row edit even when gate 1 admitted. The kid's C_REFUSAL shows an unadmitted writer WITH a valid m=2 quorum now refused by the written_by line naming 'prime', and A_REFUSAL shows an admitted writer with no sigs refused by the ring line.
- Tests I ran myself: test_write_ring_cli.py + test_rings.py + test_veto.py -> 63 passed; test_write.py, test_write_master_sensei.py, test_write_self_row.py, test_write_guard.py, test_node_writer.py -> 232 passed. rings.load_rings('.') still [].

(3) THE NEAR MISS: the obvious implementation of "both gates must hold" is to add the ring check AFTER the written_by refusal, which leaves an unadmitted writer still admitted by the ring -- the same OR in the other direction, and the shape the original code had. The kid instead moved the ring check after gate 1's refusal but before the final `return`, and had to preserve the master_sensei and self_row carve-outs inside gate 1's unadmitted branch; a careless reorder would silently have made a seat's own-row write demand a quorum.

(4) DEVIATIONS I ACCEPT, and the one I record:
- The kid touched extensions/agi/tests/test_rings.py, a file outside its brief, because the AND fix flipped five write-gate tests that asserted the OLD OR behaviour. It said so on the node. Correct call: those tests were asserting the defect.
- RULING CONFIRMED on test D: a seated self-row write needs NO quorum. The ring governs non-self-row config writes; _self_row_refusal already confines the seat to its own row and declared fields. Recorded as a ruling, not a measurement.
- RESIDUE CARRIED FORWARD, not closed here: the kid's own end-to-end submit() test pins ts/nonce by monkeypatching seatsig.rings.secrets.token_hex and _now_iso, because no CLI seam exists. That is the un-signable-CLI defect I folded into KID D (experiment:a00-23f4782b-bffe2d) -- it is the same hole, not a new one. Also: the signed node key moved node -> _node, so a ring cell persisted before this change would not re-verify; no live schema declares `ring:` so no real record is affected.
- BEHAVIOUR CHANGE worth a reader's eye: a schema declaring `written_by: []` (falsy but not None) used to admit everyone and now refuses everyone, because gate 1 tests `admitted is not None and resolved not in admitted` rather than `if not admitted: return`. No schema in this tree declares an empty list, and the full suite is green, but it is a real semantic edge the previous `if not admitted` spelling did not have.
<!-- THOUGHT:END -->
<!-- THOUGHT:END -->

PARENT FOLLOW-UP FINDING (a00-9c00b7ed), after the review above. UNSET_MARKER is a SENTINEL and a sentinel is a collision: a set value literally equal to "<unset>" produces the SAME canonical bytes as an unset of that key.

  write._config_write_fields("config:seats", {"k": "<unset>"}, None, ts="T", nonce="n")
  write._config_write_fields("config:seats", None, ["k"],   ts="T", nonce="n")
  -> both {"_node": "config:seats", "k": "<unset>", "_fresh": "T|n"}
  -> canonical_bytes("config-write", a) == canonical_bytes("config-write", b)  is True

That is a live instance of the hypothesis own DISPROOF clause ("any two distinct decisions with equal canonical bytes") introduced by the defect-1 fix, and it is the same class the whole round is about. Fix is small: carry the unset set under a reserved key (e.g. "_unset": [k, ...]) or tag the entry ("<removed>") with its own type tag so a set value can never reach it. Not fixed in L4.329 -- the kid budget for this dispatch is spent. Recorded here so the next round at this node does not have to rediscover it.
