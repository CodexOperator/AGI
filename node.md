---
id: experiment:a00-54383116-4775b1
mint_id: cf6736fd54f64ac38009462a2b696ffa
type: experiment
parents:
  - hypothesis:lm-typesafe-replay-200
next_edges: []
confidence: 0.3
edited_by: a00-1b660946
evidence_runs:
  - experiment:a00-54383116-4775b1
line_ceiling: 600
loop: hypothesis:lm-typesafe-replay-200@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "cost", "class": "auth", "cmd": "parent probe: one unauthenticated POST to https://api.typesafe.ai/v1/systemone with a minimal choice body (no Authorization header)", "expected": "refusal by name (HTTP 401) and $0 spend", "observed": "HTTP 403, 0.686s, {\"detail\":{\"error_type\":\"authentication_error\",\"message\":\"Must supply an API key! ...\"}} -- refusal by name, no spend; 403 not the 401 the brief predicted", "result": "held"}
  - {"conjunct": "cost", "class": "wire", "cmd": "parent probe: one POST with a deliberately invalid bearer token (Authorization: Bearer invalid-probe-not-a-real-key)", "expected": "the Authorization header bytes reach the live endpoint (distinguishable auth refusal), proving replay.py's call path is live and not stubbed", "observed": "HTTP 401, 0.562s, {\"detail\":{\"error_type\":\"authentication_error\",\"message\":\"Cannot authenticate with the server. Please check your API key ...\"}} -- distinct from the missing-key 403, so the bearer header is threaded live", "result": "held"}
  - {"conjunct": "A", "class": "gate", "cmd": "parent probe: env -u TYPESAFE_KEY python3 replay.py on a scratch copy of replay.py+cases.jsonl", "expected": "exit 2, zero network calls, records blocked", "observed": "blocked:no_key -- 141 records marked, 0 network calls, key absent; EXIT=2", "result": "held"}
  - {"conjunct": "B", "class": "gate", "cmd": "parent probe: independent line-anchored ^[tag] recount of the seven Prime tags over .agi/comms/season-2/dm/belam--*.md and all .agi/comms/season-2/dm/*.md", "expected": "claim needs 100 tagged lines from belam--*.md", "observed": "belam--* = 14 (red 5, complete 7, rotation 2; merge-up/decision/rule/owner 0); ALL dm = 41; owner 0 everywhere; shortfall 86 (belam) / 59 (all dm) -- set (B) cannot be built at n=100", "result": "refuted"}
  - {"conjunct": "hygiene", "class": "wire", "cmd": "parent probe: grep -rInE for sk-*, long bearer tokens, and IPv4 literals across the four artifact files and the kid node", "expected": "no key, credential, or non-loopback address in any committed file", "observed": "zero matches (loopback excluded); replay.py reads TYPESAFE_KEY from os.environ at call time and never logs/writes it", "result": "held"}
production_lines: 497
profile: balanced
rebrief_answer: "proceed with ceiling 600 (497 production lines: 125 replay.py + 282 generated cases/results JSONL + 90 prose; artifact is a labeled corpus, not code)"
rebrief_request: "497 production lines vs 40 ceiling (12x). Only 125 are replay.py; 282 are generated cases.jsonl+results.jsonl data and 90 are table.md+ledger.md prose. Requesting ceiling 600 for a replay round whose artifact is a labeled corpus plus a client. Remaining work: none writable offline -- the round resumes with one command once TYPESAFE_KEY is in the kid env (sanctuary-master)."
role: kid
scaffold_hash: 85297d6efa64cf50
season: 2
title: TypeSafe replay BLOCKED:no_key -- key stripped from kid env (sanctuary-master owes wiring), set-B shortfall named, 0 calls, $0.000000
town: local-maxxing
verdict: pending
---
<!-- BODY:BEGIN -->
# experiment:a00-54383116-4775b1

## Experiment — TypeSafe replay BLOCKED:no_key; offline corpus built, 0 calls, $0.000000

Kid for `hypothesis:lm-typesafe-replay-200` (TM.25). The FIRST tool call was the
key-presence gate the brief demands:

    $ python3 -c "import os;print('TYPESAFE_KEY' in os.environ)"
    False

Per the dispatch order clause ("if dispatch strips TYPESAFE_KEY from the kid env,
the kid STOPS and reports it by name to sanctuary-master -- no workaround") the
live replay was STOPPED. No credential was used: no key read, no `.env` touched,
no `config.json` edit, no export, no fabrication.

**Seat owed the key wiring: `sanctuary-master`.** The key exists only in the MAIN
checkout `.env`; `extensions/agi/bin/dispatch.py` never calls `envfile.read_env`
and `extensions/agi/bin/adapters/pi_adapter.py:child_env()` only merges
`harness.env` (absent in `harnesses.pi`), so it never reaches a kid.

Allowed work still done offline, under `.agi/context/local-maxxing/typesafe/`:

* `cases.jsonl` — 141 records. Set A complete at 100: proved 25, ilp 25, ild 22,
  pending 15, disproved 13 (all that exist, below the 15 floor). Set B is every
  genuinely tagged dm line: **41**, not 100 — NAMED DEFECT, unpadded, tag list
  not widened, `[rotation-alert]` (323 lines) not relabelled in.
* `replay.py` — urllib client; reads `TYPESAFE_KEY` from `os.environ` at call
  time, POSTs `{state, model:jev-latest, questions:{q:{type:choice,
  instructions, criteria}}}`, parses `choice`/`confidence`; exits 2 with ZERO
  network calls when the key is absent; never prints or writes the key.
* `results.jsonl` — all 141 records `blocked:no_key`; nothing fabricated.
* `table.md`, `ledger.md` — the metrics are BLOCKED (not placeholders), the
  blockers named with measured numbers, and the one-command resume.

## Evidence

Wire probe — ONE unauthenticated POST, explicitly allowed even with no key:

    POST https://api.typesafe.ai/v1/systemone
    body {"state":"probe","model":"jev-latest","questions":{"q":{"type":"choice",
          "instructions":"pick","criteria":{"a":"A","b":"B"}}}}
    -> HTTP 403, latency 0.594 s, {"detail":{"error_type":"authentication_error",
       "message":"Must supply an API key! ..."}}

Deviation: brief expected 401; the endpoint returns **403** for a missing key.
The call site reaches the live endpoint and spent nothing.

Independent data-gate counts (line-anchored `^[tag]`):

| corpus | tagged lines | breakdown |
|---|---|---|
| `.agi/comms/season-2/dm/belam--*.md` (6 files) | 14 | red 5, complete 7, rotation 2 |
| ALL 85 `.agi/comms/season-2/dm/*.md` | 41 | red 23, complete 7, rotation 2, rule 1, merge-up 7, decision 1, owner 0 |

Claim asked for 100 lines from `belam--*.md`; that corpus has **14** (shortfall
86). The widest defensible corpus (all dm) has **41** (shortfall 59). `[owner]`
is 0 everywhere. Both counts are my own, and they reproduce the parent's.

Replay run with no key:

    $ python3 .agi/context/local-maxxing/typesafe/replay.py
    blocked:no_key -- 141 records marked, 0 network calls, key absent
    EXIT=2

Hygiene: `cases.jsonl` states decoded and redacted for `sk-*` tokens before
writing; no key, credential or non-loopback address appears in any artifact.

## Verdict — pending

The hypothesis was neither exercised nor harmed: the replay could not begin
because `TYPESAFE_KEY` never reached the kid environment. Blocker 2 (set B caps
at 41, not 100) is structural and independent of the key. What remains is one
command once the key is wired, run by sanctuary-master or a fresh kid:

    python3 .agi/context/local-maxxing/typesafe/replay.py

Production lines 497 vs the 40 ceiling (12x; 282 of them generated JSONL data,
90 prose, 125 replay.py) — `rebrief_request` filed in frontmatter per the
harness overage rule.

## Agent Notes
TYPESAFE_KEY absent from kid env (measured False) -> live replay stopped, sanctuary-master owed the wiring, 0 calls, $0.000000; offline cases.jsonl built (A 100: 25/25/22/15/13; B 41 not 100, belam 14, named defect); results.jsonl all blocked:no_key; unauthenticated wire probe 403; resume = python3 .agi/context/local-maxxing/typesafe/replay.py

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a00-1b660946 reviewed this kid's BYTES (not its result file) on TM.25 and accepts it as pending/blocked.
(1) What the instruction said: the round's tests clause requires the kid to prove TYPESAFE_KEY presence with a count and, if dispatch strips it, to STOP and report it by name to sanctuary-master with no workaround; the parent records probes per conjunct.
(2) What the machine actually does (cited to artifacts BUILT AND RUN, not to how code looks): the kid's first call and the parent's own `python3 -c "import os;print('TYPESAFE_KEY' in os.environ)"` both print False. dispatch.py:2446 builds spawn_env from scrubbed_env() plus adapter.child_env; pi_adapter.py:93 merges only harness.env; neither path calls envfile.read_env, so a key living in MAIN .env never reaches a kid. On a scratch copy, `env -u TYPESAFE_KEY python3 replay.py` printed blocked:no_key and EXIT=2 with 0 network calls. One unauthenticated POST returned 403 authentication_error 'Must supply an API key!' and one invalid-bearer POST returned a distinct 401, so the endpoint is live and the Authorization path is threaded.
(3) Near miss: a kid that read TYPESAFE_KEY out of MAIN .env and exported it would have satisfied the words 'read from the environment' and produced numbers -- while spending the owner's TypeSafe account from a seat the wiring never authorized. That is exactly the workaround the order forbids.
(4) Deviation: none by the kid. This version adds the parent's five probes (A gate, B gate, cost auth, cost wire, hygiene) and answers the kid's rebrief_request: ceiling 600, because 282 of the 497 production lines are generated cases/results JSONL, not code.
Verdict stays pending: the replay could not begin. Conjunct (B) is independently refuted by data -- only 14 tagged belam lines (41 across all dm) exist, never 100.
<!-- THOUGHT:END -->
