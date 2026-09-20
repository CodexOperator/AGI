# TypeSafe replay table — hypothesis:lm-typesafe-replay-200 (TM.25)

Status: **BLOCKED:no_key**. Every metric below is BLOCKED, not zero and not a
placeholder. `results.jsonl` marks all 141 records `blocked:no_key`.

## Blocker 1 (HARD GATE) — TYPESAFE_KEY stripped from the agent spawn env

Measured, verbatim:

    $ python3 -c "import os;print('TYPESAFE_KEY' in os.environ)"
    False

The key exists only in the MAIN checkout `.env`; nothing in the spawn path
(`extensions/agi/bin/dispatch.py` never calls `envfile.read_env`;
`extensions/agi/bin/adapters/pi_adapter.py:child_env()` only merges `harness.env`)
loads it. Seat owed the key wiring: **sanctuary-master**. No workaround was used:
no key read, no `.env` touched, no `config.json` edit, no export, no fabrication.

Wire probe (ONE unauthenticated POST, allowed even with no key):

    POST https://api.typesafe.ai/v1/systemone
    body: {"state":"probe","model":"jev-latest","questions":{"q":{"type":"choice","instructions":"pick","criteria":{"a":"A","b":"B"}}}}
    -> HTTP 403, latency 0.594 s
    -> {"detail":{"error_type":"authentication_error","message":"Must supply an API key! ..."}}

The call site reaches the live endpoint with no spend. **Deviation from the
brief:** expected HTTP 401; the endpoint returns **403** for a missing key.

## Blocker 2 (DATA GATE) — set (B) cannot be built at n=100

Independent counts, line-anchored `^[tag]`:

| corpus | tagged lines | breakdown |
|---|---|---|
| `.agi/comms/season-2/dm/belam--*.md` (6 files) | **14** | red 5, complete 7, rotation 2 |
| ALL 85 `.agi/comms/season-2/dm/*.md` | **41** | red 23, complete 7, rotation 2, rule 1, merge-up 7, decision 1, owner 0 |

`[owner]` = 0 everywhere. `[rotation-alert]` (323 lines) is NOT one of the seven
tags and was NOT relabelled in. The claim specified `belam--*.md`, which yields
only **14** records — a shortfall of **86** against n=100. The widest defensible
corpus (all dm) yields **41** — a shortfall of **59**. Built set (B) from all 41
genuinely tagged dm lines; the shortfall is a NAMED DEFECT, unpadded.

Set (A) is complete at n=100:

| class | records |
|---|---|
| proved | 25 |
| inconclusive_lean_proved | 25 |
| inconclusive_lean_disproved | 22 |
| pending | 15 |
| disproved | 13 (all available; below the 15 floor) |

Total `cases.jsonl`: 141 records (100 A + 41 B). State = node/file text with the
frontmatter `verdict:` line and any `evidence_runs:` removed; label = recorded
class/tag. `sk-*` tokens redacted from states by decoding before writing.

## Metric table — all BLOCKED

| metric | set A | set B | note |
|---|---|---|---|
| agreement % | BLOCKED | BLOCKED | needs key |
| confusion matrix | BLOCKED | BLOCKED | needs key |
| AUROC(confidence vs correctness) | BLOCKED | BLOCKED | needs key |
| latency p50 / p95 | BLOCKED | BLOCKED | needs key |
| 422 / 429 / 529 counts | BLOCKED | BLOCKED | needs key (seen instead: 403 unauthenticated) |
| input tokens (proxy) | BLOCKED | BLOCKED | proxy = `len(state)//4` whitespace-token estimate, named not measured |
| USD = tokens x 0.045/1M | $0.000000 | $0.000000 | no billed call |

## Exact one-command resume (once the key is wired)

    python3 .agi/context/local-maxxing/typesafe/replay.py

Reads `TYPESAFE_KEY` from `os.environ` at call time; exits 2 with no network
when absent; never prints or writes the key. Until then the replay stays blocked.
