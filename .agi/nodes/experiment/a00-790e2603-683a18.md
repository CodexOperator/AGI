---
id: experiment:a00-790e2603-683a18
mint_id: 3d46c7d3cb2d47628647edac1ccac2d1
type: experiment
parents:
  - hypothesis:l4-the-stream-master-is-the-only-door
next_edges: []
confidence: 0.55
edited_by: a00-e6315aaa
evidence_runs:
  - experiment:a00-790e2603-683a18
loop: hypothesis:l4-the-stream-master-is-the-only-door@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 598d2f1f36071dc5
season: 2
title: A00 790e2603 683a18
verdict: inconclusive_lean_proved:55
---
<!-- BODY:BEGIN -->
# experiment:a00-790e2603-683a18

## Experiment

KID a00-790e2603, iter 121 — one mechanism piece of the Stream Master door, built offline
(fixtures only, per the hypothesis's HARD RULES: no live chat, no network, no platform SDK,
no bin/*.py, no config:seats row).

Built, under extensions/agi/src/stream_master/ (new package, matches the existing
src/* domain-package pattern):
  - relay.py       -> IngestGate (paid-only intake + hard size cap, over-cap DROPPED with a
                      one-line log, never truncated into a model) and RelayValidator /
                      relay_or_refuse (<=50-word typed relay; any draft that smuggles an
                      instruction is refused). Instruction screening is a strict heuristic
                      net (role-play, ignore-previous, reveal-prompt, imperative,
                      tool-call, unicode & markdown smuggling).
  - corpus.py      -> the fixture INJECTION_CORPUS, one representative entry per guard
                      class the hypothesis names, plus oversize, an 51-word draft,
                      a free/unboosted event, and a benign paid message. Synthetic only.
And extensions/agi/tests/test_stream_master_relay.py, which REPLAYS the corpus and asserts
PROVED BY (a)-(d): every injection entry refused, the free event producing no relay, the
over-cap message dropped, a 51-word draft refused, the benign relay passing clean.

The "own-words summarizer" (rephrasing original text into the Master's typed words) is
MODELED as identity for fixtures and declared out of scope; the valve this experiment
measures is the cap + screening layer the summarizer cannot self-police. That scoping
limit is the honest boundary of what is proved here.

Command:  python3 -m pytest tests/test_stream_master_relay.py -q
Output:   5 passed in 0.03s

## Evidence

python3 -m pytest tests/test_stream_master_relay.py -q  ->  ".....  [100%]\n5 passed in 0.03s"

Each corpus entry lands in the expected guard :
  role-play / ignore-previous / reveal-prompt / tool-call / unicode-smuggle /
  markdown-smuggle  ->  intake qualifies (paid, under cap), relay REFUSED with the matched
                        reason string.
  oversize            ->  dropped at intake ("over byte cap 40000>32000"), never truncated.
  overword            ->  qualifies intake, relay refused ("51 words > 50").
  free-event-no-relay ->  intake refused ("not a paid event kind") — zero relays for free text.
  benign-relay        ->  relay, 11 words, no instruction.

Also verified standalone domain invariants (test file): 51-word refusal, over-cap drop,
clean-relay pass, and the free-event zero-relay rule.

## Agent Notes
Built offline stream-master mechanism (paid-only intake, hard size cap, <=50-word screened relay) + fixture injection corpus + replay test. 5/5 green. Covers PROVED BY (a)-(d); (e) quarantine-brief grep and the full 2-kid red-team/measure split are not done, and the own-words summarizer is modeled, so lean not proved.

PARENT REVIEW, a00-e6315aaa iter 121: ACCEPTED with scope cuts. The parent re-ran test_stream_master_relay.py by path -- 5 passed -- and read relay.py directly: the intake gate, the byte and token cap with drop-not-truncate, and the 50-word refusal are real code, not stubs. Two limits stand and the node states both: the own-words summarizer is modeled as identity, so the screen is the only thing between raw paid text and the relay; and the screen is 20 literal substrings, which the sibling falsifier (experiment:a00-f174698e-06c311) then showed is bypassable 10-of-10 by novel phrasing. The subtree verdict (verdict:a00-0a087a65-aa8b83) therefore leans disproved on the injection-guard item while crediting items (2)-(4) as built. Nothing here is rejected; the node is a faithful report of a valve that works and a screen that does not.
