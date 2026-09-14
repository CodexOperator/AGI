---
id: hypothesis:l4-a-workflow-pi-stage-mints-its-own-capped-key-like-a-dispatched-spawn
mint_id: cf73a57539e249fd84c2894da655e751
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam
scaffold_hash: 211a57948ee22cf0
season: 2
testable_claim: "goal:g15 (Prime XXI 2026-09-14 07:3xZ; MEASURED on TM.2 paper-digest .agi/context/local-maxxing/papers/.run-TM.2.log and on mur-tm-01, both dead at stage 1 with `401 User not found`): a `workflow.py run … --harness pi` stage runs `pi -p` under `_pi_env()` (workflow.py L1068-1073), a copy of the CALLER environ minus `_SCRUB` — so the stage inherits whatever OPENROUTER_API_KEY the caller shell carried (the deleted .env key), while `dispatch.py` L2395-2402 mints a per-spawn capped key through `provisioning.mint(iter_n, agent_id, tier, limit_usd, ttl_minutes, workspace_id, root)` and sets `provisioning.RUNTIME_KEY_VAR` in the spawn env. CLAIM: when `_run_stage_pi` (L1099) takes its env from ONE new seam that mints a capped key per RUN — one key for all stages of the run, iter_n the run_key, agent_id `workflow:<key>`, tier from the stage ladder role, limit/ttl from `provisioning.settings(cfg)`, workspace from `provisioning.workspace(cfg)` — whenever `provisioning.available(root)` and `adapters.needs_credential(pi)`, sets RUNTIME_KEY_VAR to the minted secret, and otherwise falls back to the inherited env with ONE stderr line naming the fallback, then: (a) a pi workflow run from a shell whose OPENROUTER_API_KEY is deleted or unset completes stage 1 (prove live on paper-digest with the same 4 papers in .args.json, or on a 1-stage fixture workflow against a fake pi bin that echoes its env); (b) the minted key name carries the run_key and shows in `provisioning.py status` outstanding while the run lives; (c) tests never mint — the L4.155 `_mutation_guard` holds; seam the mint through a fixture and assert the env the fake pi receives; (d) `--dry-run` prints one `[credential] mint per-run | inherited env (reason)` line before the dispatch lines so a director sees it from the built command; (e) the claude-code path env is byte-identical to today; (f) the full suite stays green under the 590 s ceiling. FALSIFIERS: a pi stage still 401s with the .env key present and the provisioning key valid; a test run leaves a key in `provisioning.py status`; two stages of one run mint two keys. (g) MEASURED 07:36Z on this Prime: `provisioning.mint()` with no limit_usd takes the library default DEFAULT_LIMIT_USD 0.25 (L94), while dispatch.py passes `provisioning.settings(cfg)` ($5.0) — and dispatch.py then REFUSED both L4.367 and L4.368 with `ERR: outstanding minted key agi-itermur-tm-01-parent-belam-review remaining $0.21 is below the configured floor $1.00 (provisioning.min_key_remaining_usd)`: a key whose CAP is below the floor can never pass it, so one hand mint blocks every dispatch for its whole TTL. CLAIM (g): `mint()` with limit_usd unset resolves the limit from `settings(cfg)` when a root is given (the bare default stays only for a rootless call), and the dispatch floor check SKIPS a key whose cap is below the floor, printing one line naming it as a sub-floor key rather than refusing the spawn; a test proves both from a fixture with no network."
title: A workflow pi stage mints its own capped key like a dispatched spawn (Prime XXI 2026-09-14; measured on TM.2 + mur-tm-01)
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-workflow-pi-stage-mints-its-own-capped-key-like-a-dispatched-spawn

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
