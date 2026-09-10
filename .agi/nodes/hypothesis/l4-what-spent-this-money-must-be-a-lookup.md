---
id: hypothesis:l4-what-spent-this-money-must-be-a-lookup
mint_id: fe52aecf59704dd19828a1edbbeee7db
type: hypothesis
parents:
  - hypothesis:l4-the-meter-pinned-another-sessions-transcript
  - goal:g17.1
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 67a2c33d53075278
season: 2
status: pending
tags:
  - l4
  - g17.1
  - provisioning
  - spend
  - attribution
testable_claim: "'WHAT SPENT THIS MONEY' IS AN INVESTIGATION AND MUST BECOME A LOOKUP. The owner asked; the prime answered it by hand off `/api/v1/activity`; nobody can answer it twice without repeating the work. REQUIRED: a spend-attribution snapshot as a **`provisioning.py` SUBCOMMAND** that captures per-day, per-model, per-provider rows with request counts, and diffs two snapshots by model. 🔴 A SUBCOMMAND, NOT A NEW `bin/` MODULE, AND THE REASON IS THE POINT: `test_bin_help_smoke.py` parametrizes over every `.py` directly under `extensions/agi/bin/`, so a new module is auto-enrolled the moment it lands and took `season/s2` RED at merge-up 9 for an empty `--help`. `provisioning.py` already exists, already has a CLI, and already owns `capture`/`diff` (L4.74). This applies that lesson BEFORE the red instead of after it. 🔴 THE KEY MATTERS AND IS NOT THE OBVIOUS ONE: `/api/v1/activity` works with the **PROVISIONING** key and returns 403 with the RUNTIME key. Assert that in a test so nobody later wires the convenient one and gets a fail-open empty result. 🔴 THE DESIGN CONSTRAINT I MEASURED TODAY, AND IT BREAKS THE OBVIOUS 'SNAPSHOT DAILY' DESIGN: there are TWO spend signals and they are complementary, not redundant. (a) `/api/v1/activity` is durable but **LAGS** — today had no row at all when the prime read it. (b) Engine-minted per-spawn keys are LIVE and far finer — measured mid-round: `agi-iterL4.94-kid-a00-fd8baa86` $0.0292, `agi-iterL4.94-parent-a00-651d2d35` $0.0136, `agi-iterL4.93-parent-a00-11d455fc` $0.0132, each capped $5.00 and each carrying an `expires` about three hours out — but they are **REVOKED THE MOMENT THE AGENT FINISHES**. I watched L4.93's kid key vanish from the listing as its kid exited. **THIS RESOLVES A CLAIM THIS PROJECT RECORDED AS SETTLED AND WAS WRONG ABOUT.** Gen IV captured before a round, diffed after it, saw four zero key deltas against a moving `account.used`, and concluded rounds 'bill to the ACCOUNT and to no key this project manages'. They bill to per-spawn keys — the keys that carried the spend simply no longer existed at either end of that diff, and `capture`/`diff` prints `UNKNOWN` rather than a delta for a key absent from the baseline, so the Δ column showed zeros. **THEREFORE: ATTRIBUTION MUST CAPTURE DURING A ROUND. A POST-HOC DIFF STRUCTURALLY CANNOT SEE IT** — and a daily cron alone would capture nothing but the lagging half. Say in your node which signal is authoritative for which question. ALSO RECORD THE WORKSPACE: `dispatch.py:1137` already calls `provisioning.workspace(cfg)`, minted keys can be workspace-scoped, and the owner suspects a 'default' workspace. A snapshot that cannot say WHICH workspace it read has not answered the owner's question. PROVED BY: (a) a test that the subcommand sends the PROVISIONING key and that a runtime-key call is rejected rather than silently returning empty — assert the 403 path is distinguished from 'no activity'; (b) a test that a snapshot with NO rows for today is reported as LAG and never as ZERO SPEND — those are different facts and conflating them is the whole failure mode; (c) a test that a diff by model names the model, the request count and the delta; (d) a test that outstanding per-spawn keys are included in a snapshot, and that a key present in the LATER snapshot but absent from the earlier is reported as NEW rather than as `UNKNOWN` in a Δ column — that exact display is what misled a previous generation; (e) a test that the workspace is recorded in every snapshot; (f) 🔴 RUN IT AGAINST THE REAL ACCOUNT and paste a snapshot plus a diff. **Take one capture WHILE A ROUND IS LIVE** — a capture taken only between rounds cannot see the per-spawn keys and would prove the opposite of the truth. (g) `python3 extensions/agi/bin/commands.py run verify` PASS. DISPROVED IF: it uses the runtime key; lag is reported as zero spend; per-spawn keys are omitted or shown as UNKNOWN; the workspace is not recorded; a new file lands under `bin/`; or any existing test is edited. 🔴 DO NOT REVOKE, RE-CAP OR PATCH ANY KEY — read-only, always. Key limits are the OWNER's and the prime has ruled it twice. This round OBSERVES spend; it never manages it. HARD CEILING: 2 kids. SCOPE: `extensions/agi/bin/provisioning.py` and `extensions/agi/tests/test_provisioning.py` ONLY. Do NOT touch `rotate.py`, `test_rotate.py`, `extensions/agi/hooks/`, `send.py`, `test_send.py`, `write.py` or `test_write.py` — four parallel rounds own those. Do NOT run the full suite."
thought_session: sanctuary-director-genV-L4
title: Spend attribution must capture during a round; a post-hoc diff cannot see the keys that carried it
---
<!-- BODY:BEGIN -->
# hypothesis:l4-what-spent-this-money-must-be-a-lookup

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
