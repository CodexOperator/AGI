---
id: experiment:a00-217797be-f1590a
mint_id: f5084d2fa1fd4a6c97dc9c8d807d9d74
type: experiment
parents:
  - hypothesis:lm-kid-persona-sft-corpus
next_edges: []
confidence: 0.85
edited_by: a00-217797be
evidence_runs:
  - experiment:a00-217797be-f1590a
loop: hypothesis:lm-kid-persona-sft-corpus@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 33d8fd27cbbe2fdc
season: 2
title: Kid persona SFT corpus - 354 accepted-round examples built at $0, scrub-clean, held-out 12
town: local-maxxing
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# Kid persona SFT corpus — built 354 accepted-round examples at $0

## What I did

Round 1 of hypothesis:lm-kid-persona-sft-corpus. I wrote one stdlib build script
(`build_corpus.py` under `.agi/context/local-maxxing/kid-sft/`) and ran it once on this A1
(loadavg 1.68 measured before the run, < 3; no q4-KV bench live — the only live process was
an unrelated `workflow.py run trove-survey`). No model load, no pip installs, no ssh, no
GPU, no Camber rental. Door-to-door wall well under the 20 min ceiling. It produced
`kid_sft.jsonl` (7,051,231 bytes, 354 lines) + `heldout_rounds.txt` + `stats.md` +
`scrub_report.md` + `camber_xs_pricing.md`.

The session store is NOT under this worktree's relative paths — it lives at the absolute
`/home/ubuntu/work/agi/.agi/sessions/iter-*/<agent-id>/` (gitignored). Tool trajectories are
pruned from the pi store (`/home/ubuntu/.pi/agent/sessions/...`), which retains transcripts
for only the recent worktrees. Kid experiment nodes are tracked at
`.agi/nodes/experiment/a00-<id>-<suffix>.md`.

## Mapping / count method (sessions → nodes → verdicts)

Agent id `a00-<8hex>` (session dir name and experiment-node filename leading segment are the
same 8-hex base) is the binder. For every session dir with a `spawn.json` I looked up the
matching experiment node by the `a00-[0-9a-f]{8}` filename prefix, read its `verdict:`
frontmatter line, and applied the accept filter. 973 session dirs had spawn.json; 570
carried a decisive (`proved`/`disproved`) node; 354 additionally had a non-trivial node body.

## Accept filter (conjunct 1) — counts

ACCEPTED = round's kid experiment node verdict is `proved` or `disproved` (decisive), AND
spawn.json brief exists AND node body >= 300 chars.
- accepted=354, rejected=197, unlabelled=422.
- The alternative ACCEPT route (parent hypothesis note says ACCEPT) was **not needed** — the
decisive-verdict route alone cleared the >=300 bar.

## Per-conjunct results

1. **>=300 accepted**: YES — 354 accepted rounds (>=300). Filter written down and counted
   (above) and re-countable from the jsonl.
2. **Shape**: every example = `{system: KID-PREAMBLE (verbatim) + role-brief header, user:
   the round's spawn.json brief (the complete orders text the kid received that round),
   assistant: tool-call trajectory (when the pi store still holds it) + the experiment node
   body}`. **Fidelity caveat:** only **10/354** examples carry a full tool trajectory (the pi
   store has pruned the rest); the other **344** have a node-body-only assistant and are
   flagged `trajectory_available=false` in the jsonl — honest labelling of the fidelity.
3. **Held-out**: by-ROUND 10% split, whole rounds never split inside a round — 7 of 273
   rounds held out = **12 held-out orders** (>=10). `heldout_rounds.txt`.
4. **Scrub**: ZERO address tokens / key-shaped strings remain, proved twice — in-build decode
   + redact (6394 tokens redacted; dropped=0) and post-build `grep` over the jsonl:
   dotted-quad=0, `sk-or-`=0, `OPENROUTER`=0, hex>=40=0. `scrub_report.md`.
5. **Tokens**: median=4877, p95=7355, max=17220, sum=1,798,090, over 354 examples. Tokenizer
   **named**: tiktoken `cl100k_base` used as a proxy for the Qwen3.5 tokenizer, which is not
   shipped offline here — counts are ESTIMATE (documented in `stats.md`).
6. **Camber**: On-Demand GPU **XSMALL = 1× NVIDIA L4, 24 GB VRAM = 3 credits/h**; 1 credit =
   $1.00 (AWS Marketplace Camber Research Cloud) ⇒ **~$3.00/h**. 2-epoch QLoRA over this
   corpus ≈ **~0.67 XS-hour ≈ ~$2.00** (ESTIMATE at ~1500 tok/s). Note: the page has no
   literal "XS" tier — the L4-24 GB engine is named **XSMALL**; the owner's "XS 24 GB" maps
   to it. `camber_xs_pricing.md`, URL + date quoted.

## Struggles / caveats (honest)

- **Tool trajectory is mostly unavailable**: the pi transcript store retains only ~10 of the
  354 decided rounds. Conjunct (2)'s "trajectory as the harness emits it" is met fully for
  10 examples; the other 344 are node-body-only. This is the single biggest fidelity gap and
  the thing a reviewer should weigh most. Fix = stop pruning the pi store / export sessions
  at close, or accept node-body-only as the common case.
- **Scrub overlap bug (fixed)**: an 8-hex sub-window inside a 64-hex sha was redacted before
  the longer token, corrupting it and leaking 56 hex chars. Fixed by longest-token-first
  redaction; final grep is the proof. A fixed regex order silently misses this.
- **Over-redaction**: every 8-hex token (agent ids, short hashes) decodes to a 32-bit integer
  and is conservatively redacted — 6290 ip_hex hits. Acceptable collateral: keeps addresses
  at zero (the hard requirement) at the cost of blurring non-secret identifiers.
- **Tokenizer**: Qwen3.5's own tokenizer is not available offline; counts use the named
  cl100k_base proxy and are ESTIMATE.
- **Camber**: no literal "XS" tier on the public page (XSMALL instead), and the USD figure
  rests on the 1-credit=$1.00 conversion from AWS Marketplace.

## File note

`kid_sft.jsonl` is 7.05 MB (< 20 MB), so no sha256/gitignore detour was required.

## Evidence

- Deliverables: `.agi/context/local-maxxing/kid-sft/{build_corpus.py, kid_sft.jsonl,
  heldout_rounds.txt, stats.md, scrub_report.md, camber_xs_pricing.md}`.
- Runtime evidence: `python3 build_corpus.py` printed `accepted=354 rejected=197
  unlabelled=422`, `7 of 273 rounds held out; 12 held-out orders`, `kid_sft.jsonl 7051231
  bytes, 354 lines`, `token_sum=1798090 median=4877 p95=7355 max=17220`.
- Scrub recheck (post-build, on the jsonl): dotted-quad=0, sk-or-=0, OPENROUTER=0,
  hex>=40=0.

## Agent Notes
Kid persona SFT corpus built at /bin/bash: 354 accepted-round examples (>=300), scrub-clean (grep 0 dotted-quad/sk-or/OPENROUTER/hex40), by-round held-out 12 orders, tokens med4877/p9557355/sum1.798M (cl100k proxy ESTIMATE), Camber XSMALL 1xL4 24GB=3cred/h(~/h) quoted. Caveat: only 10/354 have full tool trajectory.
