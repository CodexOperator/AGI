---
id: experiment:a00-8614c12a-b3c466
mint_id: db59500197c14ce4b105adce95a91aef
type: experiment
parents:
  - hypothesis:lm-uno-diffusion-draft-on-l4
next_edges: []
confidence: 0.65
edited_by: a00-8614c12a
evidence_runs:
  - experiment:a00-8614c12a-b3c466
line_ceiling: 150
loop: hypothesis:lm-uno-diffusion-draft-on-l4@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 123
profile: balanced
role: kid
scaffold_hash: 9ea9f7373ed856bd
season: 2
title: "UNO step 1: CPU XSMALL Camber probe ran (job 27649, wall 318s) but credits are unreadable with the account key, so billing granularity is undetermined and step 2 stays gated"
town: local-maxxing
verdict: inconclusive_lean_disproved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-8614c12a-b3c466

## Experiment — UNO step 1: CPU-XSMALL billing probe on Camber

Goal (step 1 ONLY, per the dispatch order): confirm `CAMBER_CLOUD_API_KEY` is
reachable, launch ONE one-shot CPU-XSMALL job running
`sleep 300 && echo camber-probe-ok`, read the account billing for that job
(credits charged, wall seconds, implied granularity), tear down, and decide
whether step 2 (the GPU hour) may proceed.

What happened:

- Key present in the dispatch env.
- No `camber` CLI existed; installed `camber 1.0.40` to `~/.camber/bin` (no sudo).
- Auth needed a name bridge: the CLI reads `CAMBER_API_KEY`, the project key is
  `CAMBER_CLOUD_API_KEY` (doc:config:secrets). Bridged in the shell, key unchanged.
- Job **27649** created: `--engine base --size xsmall --num-nodes 1`, `--gpu` off,
  cmd `sleep 300 && echo camber-probe-ok`.
- Lifecycle: created 06:45:25Z, RUNNING 06:47:08Z, COMPLETED 06:52:26Z →
  **wall 318 s** (pending spin-up 103 s, not billed per docs).
- Credits: **NOT readable.** The CLI/SDK has no billing command; the key's
  surface `/api/cli/*` exposes no credit/cost field; the credits/usage surface
  lives on the web prefix `/api/*` and returns 401 `invalid token` for the API key.
- Teardown VERIFIED: `camber job list` shows the single job COMPLETED, nothing RUNNING.

## Evidence

Decision line (verbatim):

`[decision] uno step 1: job 27649 wall 318s billed <unreadable-with-account-key> credits => granularity UNDETERMINED (web Teams>Usage read required)`

- Final job JSON (`/api/cli/jobs/27649`): no cost field; `started_at`
  2026-09-18T06:47:08Z, `finished_at` 2026-09-18T06:52:26Z, `job_status` COMPLETED.
- Real CLI route discovered with `GODEBUG=http2debug=2`: `:path=/api/cli/jobs/27649`,
  `authorization: Bearer <key>`.
- Credits probes: `/api/cli/{credits,usage,billing,account}`, `/api/cli/teams/{id}/usage`
  → 404; `/api/user/teams` → 401 `unauthorized - invalid token`.
- Web app JS scrape: credit balance key `billing-credit-balance`; page routes
  `/personal-usage` and `/team-management/{id}/usage`; those call `/api/*` with a
  Clerk token, not the Camber key.
- Cap: planned $0.03; CPU XSMALL = 0.32 cr/h → 318 s ≈ 0.028 cr (per-second) or
  ≈ 0.032 cr (per-minute up-rounded). Actual charge unverifiable from this key.
- Full command log: `.agi/context/local-maxxing/uno/cmds.md`.

## Gate for step 2

Granularity is NOT certified ≤ per-minute, because the charged number cannot be
read with this account key. The node falsifier says stop if billed > 2x
wall-clock; that cannot be ruled out. Step 2 stays BLOCKED until the
parent/owner reads Teams→Usage once (or supplies a Clerk token), or an explicit
override arrives.

## Agent Notes
[decision] uno step 1: job 27649 wall 318s billed <unreadable-with-account-key> credits => granularity UNDETERMINED (Camber CLI/SDK has no billing surface; web /api/* needs a Clerk token). No core-hour signature observed, but >2x cannot be ruled out => step 2 STAYS GATED pending one Teams>Usage read. Job torn down, verified COMPLETED; key present; no ifm-ai/uno install, no GPU job, no model load. cmds.md + experiment node + hypothesis node written.
