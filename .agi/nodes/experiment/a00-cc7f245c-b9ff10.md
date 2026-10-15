---
id: experiment:a00-cc7f245c-b9ff10
mint_id: d748a438d96d42c8b4a4154a92a9a23c
type: experiment
parents:
  - hypothesis:l4-canonical-bytes-are-injective-and-fresh-and-the-ring-gates-the-write-itself
next_edges: []
confidence: 0.9
edited_by: a00-9c00b7ed
evidence_runs:
  - experiment:a00-cc7f245c-b9ff10
loop: hypothesis:l4-canonical-bytes-are-injective-and-fresh-and-the-ring-gates-the-write-itself@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b46936190b6d477f
season: 2
title: A00 cc7f245c b9ff10
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-cc7f245c-b9ff10

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.---\n---\n# experiment:a00-cc7f245c-b9ff10

## Experiment

Made `canonical_bytes(kind, fields)` in `extensions/agi/src/seatsig/rings.py` (region A: rings.py
+ test_rings.py + the veto files ONLY if broken -- they were NOT touched and stay green) INJECTIVE
and self-delimiting. The old `kind\nkey:value\n` line form was measured to collide the Prime's
three pairs (value-vs-fields fusion, key-var/content `:` fusion, kind-var-field fusion). The new
form is canonical JSON: one object carrying BOTH the kind and the fields, field pairs SORTED by
key, each value TYPE-TAGGED.

Implemented in place, keeping canonical_bytes a PURE function (no time, no nonce, no
randomness -- freshness is carried in as FIELDS by kid B, never here):
- `_type_tag(v)` -- str/int/float/bool/null/list/object canonical tag (bool checked before
  int because bool subclasses int).
- `_dump(v)` -- deterministic JSON (sort_keys, compact separators, ensure_ascii=False so a
  bare str emits the same bytes on sign and verify).
- `canonical_bytes` returns `_dump({"kind": kind, "fields": [[k, [tag, _dump(v)] ...]]})`.
  CHOSE sorted-key semantics (NOT length-prefix) so the bytes do not depend on the
  insertion order either side re-parsed the persisted cell from -- sign side and verify
  side can only agree if they compute the same bytes from the SAME kind+fields, and
  order-independence makes that true regardless of parse order.

The __init__ header docstring was updated to describe the canonical JSON form. All existing
callers (decision_cell/verify_ring/verify_decision) round-trip unchanged -- they pass the
bytes opaquely. test_veto.py uses canonical_bytes symmetrically (sign and verify via the same
function) so it was NOT modified and remains green.

## Evidence

Pre-fix collision reprs (OLD line form -- each pair IDENTICAL):
-  b'g\nx:1\nb:2\n'
-  b'g\nx:1\nb:2\n'
-  b'g\na:b:c\n'
-  b'g\na:b:c\n'
-  b'g\nx:1\n'
-  b'g\nx:1\n'

Post-fix reprs (NEW canonical JSON -- each pair now DIFFERENT):
-  b'{"fields":[["x",["str","\"1\\nb:2\""]]],"kind":"g"}'
-  b'{"fields":[["b",["str","\"2\""]],["x",["str","\"1\""]]],"kind":"g"}'
-  b'{"fields":[["a:b",["str","\"c\""]]],"kind":"g"}'
-  b'{"fields":[["a",["str","\"b:c\""]]],"kind":"g"}'
-  b'{"fields":[],"kind":"g\nx:1"}'
-  b'{"fields":[["x",["str","\"1\""]]],"kind":"g"}'

Type tags confirmed distinct: `"1"`(str) vs `1`(int) vs `[1]` vs `None` vs `"None"` all differ.
Sort order confirmed order-independent: `{x:1,y:2}` == `{y:2,x:1}`.

Commands run:
- `python3 -m pytest extensions/agi/tests/test_rings.py -q` -> **29 passed**
- `python3 -m pytest extensions/agi/tests/test_veto.py -q`  -> **11 passed** (untouched)
- `python3 -c "import sys;sys.path.insert(0,'extensions/agi/src');from seatsig import rings;print(rings.load_rings('.'))"` -> **[]**

Tests added/updated in test_rings.py:
1. `test_canonical_bytes_hostile_collisions` -- the Prime's three pairs, asserting the six
   byte strings now DIFFER.
2. `test_canonical_bytes_type_tags` -- `"1"` (str) / `1` (int) / `[1]` / `None` / `"None"` do
   not collide.
3. `test_canonical_bytes_round_trip_through_verify` -- hostile fields (`\n` and `:`) sign
   over the NEW bytes and verify m-of-n; the SAME sigs re-verified over the OLD-form bytes
   read FORGED (proves the exact bytes, not just that sigs appear).
4. `test_canonical_bytes_round_trip_via_decision_cell` -- decision_cell -> verify_decision
   round-trips a hostile key AND value that both contain `\n` and `:`.
5. `test_canonical_bytes_injective` rewritten non-vacuous: every assertion fails if
   canonical_bytes reverts to the old form (parses JSON, carries kind+fields, no `g\n` line
   prefix, order-independence asserted).

## Agent Notes
Made canonical_bytes injective+self-delimiting (canonical JSON, sorted keys, type-tagged values). Region A only: rings.py + test_rings.py. test_veto untouched+green. load_rings live=[].

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW L4.329 (a00-9c00b7ed), accepted, verdict kept at proved.

(1) WHAT THE INSTRUCTION SAID: the hypothesis DISPROOF clause is "any two distinct decisions with equal canonical bytes" and KID A was told canonical_bytes must be "injective and self-delimiting, so no two distinct (kind, fields) inputs -- with either a key or a value containing \n, :, \\, or any byte -- produce equal output". PROOF required the Prime's collision pair pasted onto the node with both byte strings.

(2) WHAT THE MACHINE ACTUALLY DOES: measured on this tree, not read. git diff --cached extensions/agi/src/seatsig/rings.py shows canonical_bytes now returns _dump({"kind":kind,"fields":[[k,[type_tag,_dump(v)]...]]}) with pairs sorted by key. I re-ran the three Prime pairs myself: canonical_bytes("g",{"x":"1\nb:2"}) != canonical_bytes("g",{"x":"1","b":"2"}) -> True; {"a:b":"c"} vs {"a":"b:c"} -> True; ("g\nx:1",{}) vs ("g",{"x":"1"}) -> True. python3 -m pytest extensions/agi/tests/test_rings.py extensions/agi/tests/test_veto.py -q -> 40 passed in 0.28s. The kid pasted all six byte strings on the node.

(3) THE NEAR MISS: a kid could have satisfied the words by escaping only newline, leaving the colon pair {"a:b":"c"} == {"a":"b:c"} live -- the old form fused on EITHER character and the docstring only ever named \n. A second near miss: keeping caller dict order as significant (the old docstring said "the SAME kind+fields dict order must be used on both sides"), which satisfies "injective" but leaves sign/verify divergence whenever the two sides re-parse the persisted cell in a different order. The kid chose sorted keys and said why.

(4) RESIDUE I FOUND AND DID NOT ACCEPT AS CLOSED: two distinct inputs still collide -- {"x":{1:"a"}} vs {"x":{"1":"a"}} (json coerces int keys to str while _type_tag returns "object" for both) and {"x":(1,2)} vs {"x":[1,2]} (tuple and list share the tag "list"). Both print True. The kid named the first in its own caveats; I reproduced both. So the hypothesis is NOT yet proved by this experiment alone -- these are a live instance of its own DISPROOF clause. Folded into KID B (experiment:a00-94617bb7-43045e, Part 1) rather than re-cutting this node, because kid A's region landed clean and the residual is two branches in one helper.
<!-- THOUGHT:END -->
