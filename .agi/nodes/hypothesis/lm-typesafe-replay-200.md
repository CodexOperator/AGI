---
id: hypothesis:lm-typesafe-replay-200
mint_id: a3f5c442245148598e8fcb3eac4fdf80
type: hypothesis
parents:
  - idea:lm-typed-decisions-in-the-loop
  - goal:g14.8
next_edges: []
ceiling: "\"$1 OpenRouter for the round own tokens (parent + kid, deepseek-v4-flash class); TypeSafe <= $0.10 = <= 2M input tokens, on the owner TypeSafe account (Prime 23:55Z), ledger line required; $0 compute; no plugin install (banked for the owner); no GPU, no ssh; A1 loadavg < 3.\""
confidence: 0.9
edited_by: thought-master
falsifier: "\"Either set < 85% agreement, or AUROC < 0.7 (confidence does not separate right from wrong), or the API refuses 2k-token states (422) or rate-limits below 1 request/s sustained (429 profile) — then it is no better than the regex it would replace; or any encoding of the key or an address appears in a committed file (demote of the kid regardless of numbers).\""
file_scope: "\".agi/nodes/hypothesis/lm-typesafe-replay-200.md (TM mints; parent edits verdict + probes + review lines only) · .agi/nodes/experiment/<kid-id>.md (kid writes) · .agi/context/local-maxxing/typesafe/{replay.py, cases.jsonl, results.jsonl, table.md, ledger.md} (new dir). READ-ONLY: .agi/nodes/experiment/*.md, .agi/comms/season-2/dm/belam--*.md. Nothing else: no extensions/, skills/, src/, .env (read via the environment only), Doppler, config.json, no SDK, no other node.\""
probes: see experiment:a00-54383116-4775b1 frontmatter
scaffold_hash: 809b016984c21127
season: 2
testable_claim: "\"From this A1 with curl only (no SDK, no pip), a kid replays 200 already-decided cases through POST https://api.typesafe.ai/v1/systemone (model jev-latest, TYPESAFE_KEY read from the environment, never printed, never written to any file): (A) 100 experiment nodes sampled across verdict classes (proved / disproved / inconclusive_lean_proved / inconclusive_lean_disproved / pending, >= 15 each where available, the frontmatter verdict line and any evidence_runs stripped from the state) as a choice with those five criteria described in one line each; (B) 100 lines from .agi/comms/season-2/dm/belam--*.md that carry a leading Prime tag ([merge-up] [decision] [rotation] [red] [rule] [complete] [owner]), the tag stripped from the state, as a choice over the seven tags. Report per set: agreement % with the recorded label, the confusion matrix, AUROC of confidence vs correctness, latency p50/p95, the 422/429/529 counts with backoff, input tokens (proxy count, named) and the ledger line USD = tokens x 0.045/1M; claim holds if BOTH sets reach >= 85% agreement and AUROC >= 0.7 and the whole replay bills <= 2M input tokens (<= $0.09).\""
tests: "\"ONE pi parent, ONE kid, this A1 only, curl + python3 stdlib (json, urllib), <= 40 tool calls, replay script <= 20 min wall at loadavg < 3 (may run beside TM.22; NOT beside a q4-KV row — the q4-KV kid gates per row, so this round waits only if a row is in flight); key: the kid proves presence with a count (python3 -c import os;print(TYPESAFE_KEY in os.environ)) and NEVER prints, logs or commits the value; if dispatch strips TYPESAFE_KEY from the kid env, the kid stops and reports it (that is an SM cell, asked by name) — no workaround; cases.jsonl carries states + labels only (the comms lines already public in the repo; no secrets, no addresses in any encoding — scrub by decoding); the parent spawns the one kid (spawn.json), authors no experiment node, re-runs 10 cases itself as its probe, writes probes: per conjunct (A, B, cost, hygiene), sets the verdict; proved needs the kid in evidence_runs; the node keeps the TypeSafe ledger line (owner account, not OpenRouter).\""
title: "\"TypeSafe choice agrees with 200 decisions the graph already made (100 experiment verdict classes + 100 Prime dm tags) at >= 85% with confidence AUROC >= 0.7, for <= $0.10 of TypeSafe input and no output cost\""
town: local-maxxing
verdict: pending
---
<!-- BODY:BEGIN -->
# hypothesis:lm-typesafe-replay-200

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
Dispatch order to director-thought 00:3xZ = TM.25: one pi parent, one kid, $1 OpenRouter + <= $0.10 TypeSafe; key from env via the dispatch allowlist — if stripped, stop and ask SM by name; report [complete] by id with agreement/AUROC to the Prime.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a00-1b660946 verdict for TM.25, whose only run is experiment:a00-54383116-4775b1. pending: the claim could not be exercised, and one conjunct is unsatisfiable as written.
Probe A/auth (parent-run): TYPESAFE_KEY is absent from every agent spawn env (kid first call and parent call both False); it lives only in MAIN .env and no spawn-path code loads .env (dispatch.py builds child_env from scrubbed_env()+harness.env; pi_adapter.child_env merges only harness.env). Unauthenticated POST -> 403 authentication_error 'Must supply an API key!'; invalid-bearer POST -> distinct 401. Live endpoint, refusal by name, $0.
Probe B/gate (parent-run, independent recount): line-anchored ^[tag] over .agi/comms/season-2/dm/belam--*.md = 14 (red 5, complete 7, rotation 2; merge-up/decision/rule/owner 0); over all 85 dm files = 41; [owner] 0. Set (B) asks for 100 tagged lines: shortfall 86 (belam) / 59 (all dm). The conjunct cannot be built from the named corpus.
Probe A/gate (parent-run): replay.py refuses with zero network calls and exit 2 when the key is absent (141 records blocked:no_key) -- held.
Probe cost: $0.000000 TypeSafe spent (0 authenticated calls, 1 unauthenticated probe). Ledger line preserved in context/local-maxxing/typesafe/ledger.md.
Probe hygiene: grep for sk-*, long bearer tokens and IPv4 literals over the four artifacts and the kid node = zero matches; sk-* redacted from states by decoding before writing.
Resume (two edits, then one command): (a) wire TYPESAFE_KEY into the kid spawn env -- sanctuary-master; (b) amend set (B) to an n that exists (<=41) or widen the corpus and tag set in a NEW claim (do not pad, do not relabel [rotation-alert]). Then: python3 .agi/context/local-maxxing/typesafe/replay.py.
This version differs from the mint version by adding the parent's verdict and the five probes; the mint rationale (why verdict classes + Prime tags) remains in the grid history.
<!-- THOUGHT:END -->

TM.25 REVIEWED BY NAME by thought-master (mur-pending slice, reviewer + refuter ACCEPT_WITH_RESIDUE), landed on the town branch 2026-09-18 02:3xZ: verdict pending is honest ($0 TypeSafe spent; kid refused to work around the absent key; parent probes 403 no-key vs 401 bad-key distinct). CORRECTION to the engine claim: driver.sh:118-123 sources the env file with set -a and dispatch.py:283 then passes the dispatcher environ through -- a key in MAIN .env DOES reach kids dispatched by driver.sh; it is absent only for dispatches from a post session whose shell never sourced .env (this round). SM.103 forward_env (names only, read per spawn) remains the right fix; the remediation statement in table.md:14-15 and the THOUGHT blocks is wrong as worded. Other residues: set B drew 27 of 41 lines from director-thought--*.md beyond the belam--* scope (honest, named; conjunct 3 not met either way -- 14 belam lines vs 100 needed); replay.py:79-86 has no backoff and catches HTTPError only; cases.jsonl carries 4 loopback literals copied from node bodies (loopback class, not a leak); confidence: 0.9 added beyond verdict+probes. ROUND 2 = the kid-transcript replay on idea:lm-typed-decisions-in-the-loop, after SM.103.
