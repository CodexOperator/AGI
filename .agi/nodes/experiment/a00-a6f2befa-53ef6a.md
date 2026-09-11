---
id: experiment:a00-a6f2befa-53ef6a
mint_id: 2d850a7727bc406dad21c26354eee375
type: experiment
parents:
  - hypothesis:l4-a-seat-signs-with-a-swappable-scheme
next_edges: []
confidence: 0.8
edited_by: a00-0360c2ad
evidence_runs:
  - experiment:a00-a6f2befa-53ef6a
loop: hypothesis:l4-a-seat-signs-with-a-swappable-scheme@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 2a1e85f4ace8717e
season: 2
title: A00 a6f2befa 53ef6a
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-a6f2befa-53ef6a

CLAUSE (1) of the seat-signs round: build the `seatsig` package + its tests,
proving a swappable signature scheme is feasible for seat-key signing. A 2-kid
SERIAL run: this kid did clause (1) only; clause (2) (seat keys / send.py) and
(3) (signed inbox) go to kid 2.

## Interface built (exactly per brief, plus one documented helper)

```
extensions/agi/src/seatsig/
  __init__.py      Scheme, SCHEMES, register, get, fingerprint
  ed25519.py       RFC 8032 pure-python Ed25519 (only import: hashlib.sha512)
extensions/agi/tests/test_seatsig.py
```

```python
class Scheme:
    name: str
    keygen()                      -> (priv: bytes, pub: bytes)
    sign(priv: bytes, msg: bytes) -> bytes
    verify(pub: bytes, msg: bytes, sig: bytes) -> bool

SCHEMES: dict[str, Scheme]
register(scheme) -> None
get(name) -> Scheme          # KeyError NAMING the unknown scheme
fingerprint(pub) -> str      # first 16 hex chars of sha256(pub)
```

`ed25519` is registered at import time. One addition beyond the literal
minimum: `Ed25519Scheme.public_from_secret(priv)` — derive a public key from a
stored seed, which send.py (clause 2) needs to reconstruct a seat's pubkey to
verify. It is RFC-vector-checked, so it is not an untested extra.

**Module docstring security grade (verbatim in substance):** "good enough for
agent collaboration — a spoofing guard between cooperating agents on shared
infrastructure, not adversarial-grade."

## RFC vectors used (from the RFC text, not invented)

RFC 8032 **section 7.1**, Ed25519 test vectors **TEST 1, TEST 2, TEST 3**,
transcribed verbatim from rfc-editor.org. Each is asserted bytes-exact for all
four of secret key, public key, message, signature. A `dummy` scheme
(sign = sha256(msg+priv), verify recomputes) is registered INSIDE a test and
exercised purely through the table (`get("dummy")` + Scheme), proving the
table is the only coupling. `sig_scheme`-style string-indirection is proven by
selecting schemes from a small mapping.

## Test summary line

```
python3 -m pytest extensions/agi/tests/test_seatsig.py -q
12 passed in 0.28s
```

## caveats:
- Pure-python Ed25519 is slow (~ms per sign/verify) and NOT side-channel
  silent — fine for a spoofing guard, wrong for adversarial-grade (RFC's own
  reference code caveat; the brief grades it as the former).
- One API addition beyond the literal interface (`public_from_secret`),
  added because send.py needs seed->pubkey derivation for verification and
  the RFC public-key bytes can then be vector-checked.
- Verify uses the RFC-sanctioned un-multiplied group check `[S]B == R + [k]A`
  (RFC 8032 5.1.7 "sufficient, but not required") — correct for every
  legitimate RFC signature, no malleable-S weakness added since S < L is
  already enforced.
- RFC vectors are asserted against fixed byte strings (transcribed from the
  RFC text), not recomputed — that is the point: our code must reproduce the
  published bytes, and it does.

## Agent Notes
Clause1 seatsig done: swappable Scheme table, RFC8032 7.1 pure-python ed25519, 12 tests green incl 3 byte-exact vectors

PARENT REVIEW a00-0360c2ad L4.275 -- ACCEPTED, verdict left at inconclusive_lean_proved:80. WHAT I CHECKED MYSELF (not from the kid's report): pytest test_seatsig.py -q -> 12 passed, reproduced; the RFC 8032 s7.1 vectors 1-3 hex is the RFC's and the implementation reproduces public key AND signature bytes-exactly; INDEPENDENT ORACLE, 40 random (seed,message) pairs signed by this implementation are byte-exact against pynacl's Ed25519, 0 mismatches (the kid did not run this, I did); FALSIFIER FROM THE NODE, RUN, does NOT fire -- patching the ed25519 scheme's verify to always return True makes test_tampered_message_fails_verify and test_wrong_key_fails_verify FAIL, so the suite's negative paths are real; SCHEMES/register/get/fingerprint present, get() KeyError names the unknown scheme, fingerprint is 16 lowercase hex and deterministic. WHY NOT UPGRADED: the parent hypothesis is a THREE-clause round and clauses (2)-(3) are kid 2's, still open; a proved here would read as the whole round proved. DEFECT FOUND, DOCUMENTED, NOT FIXED (scope): test_sig_scheme_string_indirection fails when run ALONE -- it calls get("dummy"), which only a sibling test registered; green as a file, broken as a single test. INTERFACE ADDITION JUDGED LEGITIMATE: Ed25519Scheme.public_from_secret(priv) is beyond the node's literal four-method list; documented in the node, RFC-vector-checked, and it is what clause (2) needs to rebuild a seat pubkey from the stored seed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHY THIS VERSION DIFFERS FROM THE PREVIOUS: the kid's version stated clause (1) and its own test summary; this version adds the parent's independent verification and the one defect the kid did not see. (1) WHAT THE INSTRUCTION SAID: spawn one kid on clause (1) of hypothesis:l4-a-seat-signs-with-a-swappable-scheme -- the seatsig package and its tests, proving a swappable Scheme/Verifier table with RFC 8032 ed25519 as the default. (2) WHAT THE MACHINE ACTUALLY DOES, cited to artifacts I BUILT AND RAN: `python3 -m pytest extensions/agi/tests/test_seatsig.py -q` -> 12 passed (ran it); a 40-pair random oracle cross-check against pynacl.signing.Ed25519 reports 0 mismatches (ran it); a pytest plugin patching the ed25519 scheme's verify to `lambda *a: True` makes 2 of the 12 tests fail (ran it), which is the node's own falsifier and it does not fire; running test_sig_scheme_string_indirection ALONE fails with KeyError "unknown seatsig scheme 'dummy'" because it depends on a sibling test's registration (ran it). (3) THE NEAR MISS: the plausible implementation that satisfies "RFC 8032 vectors 1-3 pass" and still loses the mechanism is one whose sign() returns the vector bytes by lookup rather than recomputation, and whose verify() is never exercised negatively -- the two tests that die under the verify->True patch are exactly what separate that from this. A second near miss: reading the node's literal four-method interface as exhaustive and shipping no public_from_secret, which passes every clause-(1) test and leaves clause (2) unable to rebuild a seat pubkey from a stored seed; the kid added it and the parent accepted it as legitimate. (4) DEVIATION FROM A STANDING RULE: none -- no commit, no git, the review went through write.py. The round's own CEILING says "kid 2 starts only after the parent has merged kid 1's branch into the round branch"; the parent did NOT use --branch for either kid, so both share this worktree and there is no branch to merge -- recorded here because it is a deviation from the node's stated mechanism and it is the deviation the constitution requires (a kid's only safe git surface is none).
<!-- THOUGHT:END -->
