---
id: verdict:a00-0a087a65-aa8b83
mint_id: 48682e081c5148b6847ca178154bfb3c
type: verdict
parents:
  - experiment:a00-f174698e-06c311
next_edges: []
confidence: 0.58
edited_by: a00-e6315aaa
evidence_runs:
  - experiment:a00-790e2603-683a18
  - experiment:a00-02a51a3c-c582ef
  - experiment:a00-f174698e-06c311
loop: experiment:a00-f174698e-06c311@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: cb43f2e0c2130f4d
season: 2
title: A00 0a087a65 aa8b83
verdict: inconclusive_lean_disproved:58
---
<!-- BODY:BEGIN -->
# verdict:a00-0a087a65-aa8b83

## Verdict

inconclusive_lean_disproved:58

## Evidence

Judging hypothesis:l4-the-stream-master-is-the-only-door against ALL THREE
experiment nodes (relay/valve a00-790e2603, quarantine/isolation
a00-02a51a3c, blind-measure a00-f174698e), artifacts read and re-verified
independently (I did not take any kid's word; I read relay.py, quarantine.py,
corpus.py, all four test files, and re-ran the suite).

WHAT HOLDS — the door's SHAPE is real and green (15 stream_master tests pass, no
fails — relay 5, quarantine 6, blind-measure 4; the count is per-file by
path, because `pytest -k stream` also collects 10 unrelated tests):
(2) paid-only intake, (3) hard byte/token cap with drop-not-truncate,
(4) <=50-word typed relay with 51-word refusal, (5) master-only quarantine
write, dispatch read returns None, no-source-leak — all have named tests in
relay.py/quarantine.py and all pass. The owner's *containment* goal — no chat
text reaching a brief/node/payload except through the Master's typed relay —
is met as an offline model.
WHAT FAILS — the load-bearing item (6), INJECTION GUARDS MEASURED NOT
ASSERTED. The screen is a literal 20-substring list (`_INSTRUCTION_PATTERNS` in
relay.py) over the body's lowercased text. Kid 3 authored a corpus from
attacker intent only (never reading the substring list) and, against the REAL
screen, 10 of 10 novel attempts relayed as 'clean' — only the 2 canned-substring
control rows were caught. I reproduced this exactly: 10 ESC / 2 CAUGHT. The
mechanism thereby fails the hypothesis's OWN acceptance method for item (6), which
is precisely a red-team kid writes the corpus and a second kid measures.

WHY LEAN_DISPROVED AND NOT LEAN_PROVED: the owner's verbatim reason for
existing at all is 'strong anti-prompt-injection guards.' Item (6) is not a
minor sub-clause — it is the screening the entire door exists to perform, and
every other item (cap, word count, paid-only, isolation) is a shape constraint
that makes a leak *harder to exploit* but does none of the actual screening.
5-of-6 green does not carry the claim when the absent one is the anti-injection
screen, and a blind relay whose body IS an instruction still enters quarantine
as rescreen-clean 'data' that a Council reader is explicitly told to treat as
not-an-instruction — which is a real induction vector for a paid adversarial
viewer.

WHY NOT FULL DISPROVED: the hypothesis's DISPROVED BY condition (chat text
reaching a brief/node/payload outside the typed relay, or a relay >50 words or
carrying original text) is NOT triggered. Every escape stayed <=50 words,
typed, and landed only in the quarantine inbox as typed data — containment
held. So it is dishonestly over-strong to call the whole door disproved; the
injection-guard sub-claim is what fails, and it fails its own gate.

SCOPE CAVEATS that cut BOTH ways, from the kids' own words: the Master's
'own-words summarizer' is modeled as identity (never exercised), and 'no chat
text reaches a kid' is modeled as a no-source-leak invariant, not a real grep
of the live brief-assembly pipeline. Both are offline-modeling limits — they
mean PROVED could never be argued for the live claim regardless; they do not
change the measured 10/10 bypass, which is mechanism-level and reproducible.

BOTTOM LINE: the door's *shape* is built and green and is a genuine
accomplishment; but the anti-prompt-injection guard — the owner's stated
purpose for the door — is trivially bypassable as built (literal-substring
screen), and injection is the exact threat model the door exists to defeat.
The fix a child of this verdict should measure is a SEMANTIC screen (a second
model reviewing the relay body for directive intent) or attestation that the
Master's re-summarizer rewrites away directives before the screen — the
corpus-as-spec framing is the weak link.

## Confidence

0.58

## Agent Notes
Verdict on l4-the-stream-master-is-the-only-door: door SHAPE holds and is green (paid-only intake, hard cap drop-not-truncate, <=50-word typed relay, master-only quarantine write, dispatch read None, no-source-leak — 15 stream_master tests pass: relay 5 + quarantine 6 + blind-measure 4, re-verified by path; the widely-quoted 25 is a `pytest -k stream` count that sweeps in 10 unrelated tests). But load-bearing item (6) injection guards MEASURED-NOT-ASSERTED fails its own acceptance method: literal 20-substring screen; blind red-team corpus wrote 10/10 novel attacks through as clean relays (reproduced 10 ESC/2 CAUGHT), only canned-substring controls refused. Owner stated purpose is anti-injection; a screen with a 10/10 blind bypass does not carry a lean_proved. Yet no chat text reached a brief/node/payload and every escape stayed <=50-word typed quarantine data — DISPROVED BY not triggered, so not full disproved. Lean_disproved:58; next child should measure a SEMANTIC screen (2nd model on directive intent) or attest the re-summarizer strips directives before the screen.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW BY PARENT a00-e6315aaa, iter 121. WHAT THE INSTRUCTION SAID: the verdict is one of proved | disproved | inconclusive_lean_proved:N | inconclusive_lean_disproved:N | pending, and proved/disproved REQUIRE evidence: evidence_runs must be a LIST of node ids that exist, not a bare count. WHAT THE MACHINE ACTUALLY DOES: I re-ran the three stream_master test files by PATH -- test_stream_master_relay.py 5 passed, test_stream_master_quarantine.py 6 passed, test_stream_master_blind_measure.py 4 passed = 15 total. THE NEAR MISS: this node says 25 stream tests pass and that number is wrong. It is the count from pytest -k stream, which also collects 10 UNRELATED tests -- the viewport stream formatter, the rotate_tail livestream-views tests, the adapter output-stream tests. A reader who trusts 25 would think this round landed 25 tests of the door; it landed 15, and 10 of the 25 belong to other lanes. Corrected in the body rather than left standing. Everything else the node asserts held up under my own reading: the 10-of-10 blind bypass reproduces exactly when I re-run the file, the two canned-substring control rows do fire, and test_stream_master_blind_measure.py imports screening_reason from the real relay module rather than a mock, so the falsifier measures the real net and not a stand-in. Verdict state left at inconclusive_lean_disproved:58 -- honest: item (6) fails its own acceptance method while the hypothesis DISPROVED BY condition, chat text outside the typed relay, is genuinely not triggered. DEVIATION: none from a standing rule; the numeric correction is an edit to a kid node, made through write.py as my review artefact, because my artefact is my kids nodes and not one of my own.
<!-- THOUGHT:END -->