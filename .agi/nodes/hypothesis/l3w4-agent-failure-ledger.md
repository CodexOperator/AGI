---
id: hypothesis:l3w4-agent-failure-ledger
mint_id: edae3df7721142c8b5bac5f6208ca536
type: hypothesis
parents:
  - goal:g16
next_edges: []
edited_by: belam-S1-L3-V
scaffold_hash: 1d35deef8d61c89c
season: 2
testable_claim: Given a fixture iteration whose manifest.json/agent.json, evidence-gate stamps, write-log.jsonl and output.log reproduce all 8 closed failure categories (died, demoted, rejected, overclaim, broken_frontmatter, session_limit, wrong_file, no_build_probe_only), failures.py ledger appends exactly one row per event — keyed by sha256(agent_id+category+detail) — into a new build:g16-failure-ledger node's payload via write.py, appends zero new rows on an immediate rerun (idempotent), and failures.py rates --by model|role|harness prints per-axis counts summing to the total row count, while failures.py never calls node_writer.write_node/update_node directly on any node's frontmatter.
thought_session: L3.27
title: Build the agent failure ledger
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-agent-failure-ledger

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## CLAIM

New `extensions/agi/bin/failures.py`: `ledger(root, since=None)` idempotently derives per-agent failure rows from manifest/agent.json, evidence-gate stamps, write-log repairs, adapter session-limit lines and spawn-budget zombie sweeps, and lands the merged table as one build node's payload via `write.py`; `rates(root, by)` groups it by seat/model/role/harness. Rendered by g16 telemetry; Master Sensei is its first reader.

## WHY

Owner (12): "We need a way to track how often a given agent fails and then use that as a way for Sensei to home in on where improvements are needed... Like the kids delivering bad nodes." Director gloss, same quote: "so the Sensei reads a measured table, not recollection."

## FILES

- extensions/agi/bin/locations.py :: list_iterations L551, iteration_dir L546, sessions_dir L542 (reused)
- extensions/agi/bin/dispatch.py :: agent_record dict L1207-1252 (id/tier/harness/model/status/node_id/parent/verdict); "unadmitted" L963
- extensions/agi/bin/heal.py :: TERMINAL L36, fail_reason "pid disappeared..." L117, status "hung-healed" L247
- extensions/agi/bin/spawn_budget.py :: _sweep_locked L188 (zombie/orphan leases), live_agents L229
- extensions/agi/bin/adapters/claude_code_adapter.py :: SESSION_LIMIT_SUBTYPE L654, scan_log_for_session_limit L701
- extensions/agi/bin/evidence_gate.py :: apply_gate L373, DEMOTED/REJECTED res.messages
- extensions/agi/bin/cli.py :: cmd_done L312 (demoted_from/demote_reason), _ensure_frontmatter repair L180-276, _FM_REPAIR_OP L102
- extensions/agi/bin/node_writer.py :: log_write L1113 → .agi/sessions/write-log.jsonl `operation` field
- extensions/agi/bin/write_guard.py :: WRITE_LOG L26, cmd_check L252, "WARN unsanctioned write" L304
- .agi/nodes/hypothesis/l3w4-bug-master-seat.md :: `results.json`'s `overclaims=<n>` — precedent, not built, optional input
- .agi/nodes/goal/g16.md — parent; .agi/context/schemas/[build].md :: parent_shapes L28-40 — landing rule
- extensions/agi/bin/write.py; extensions/agi/bin/telemetry_rollup.py :: SUMMARY_FIELDS L46 (sibling pattern)
- extensions/agi/bin/failures.py, extensions/agi/tests/test_failures.py, extensions/agi/tests/fixtures/failures/ — NEW

## DESIGN

Row: `{agent_id, iter, tier, role, model, harness, target, node_id, category, detail, source_path, ts}`. Closed `category` set: `died` (status failed/hung-unhealed, or `_sweep_locked` reclaiming a lease with no matching `done` — zombie/bare-scaffold); `demoted` (`demoted_from`/`demote_reason` present); `rejected` (`EVIDENCE-GATE REJECTED` in output.log, exit 2, nothing written); `overclaim` (`results.json` `overclaims>0` when present, else skipped); `broken_frontmatter` (write-log.jsonl `operation=="repair-frontmatter"`); `session_limit` (output.log's last line, subtype `session_limit`); `wrong_file` (`cmd_check` WARN at ledger-run time, attributed to the iter's freshest agent — pre-commit only, a stated gap); `no_build_probe_only` (verdict `pending` at done). `unadmitted` slots never count — no agent ran. `ledger()` walks `list_iterations` newest-first from `since`, keys each row `sha256(agent_id+category+detail)` for idempotent append, and lands the merged table via `write.py build:g16-failure-ledger "payload -"` (new build node, `parents:[mvp:g16-failure-ledger]` per goal:s29 — mint the mvp first, director proposal). `rates(root, by)` reads that payload and groups/divides by axis.

## TESTS (red-first)

test_ledger_reads_died_from_swept_zombie_lease; test_ledger_reads_demoted_and_rejected_from_evidence_gate_fixtures; test_ledger_reads_broken_frontmatter_from_write_log; test_ledger_reads_session_limit_from_output_log; test_ledger_skips_unadmitted_slots; test_ledger_is_idempotent_on_rerun; test_rates_by_model_and_by_harness_sum_to_total; test_ledger_never_writes_node_frontmatter_directly.

## GATE

A fixture iteration mixing all 8 categories: `failures.py ledger` prints "N rows appended", then 0 on rerun; `failures.py rates --by model` prints per-model counts summing to N. Suite green.

## NOT IN SCOPE

Glitch/Bug Master and `results.json` itself (`l3w4-bug-master-seat`); live seat-status rendering (`l3w4-telemetry-seat-status`); `write_guard.py` internals (unchanged); Sensei's training/prompt-rewording behaviour (`l3w4-master-sensei`).

## SOURCE

`.agi/context/l3-command-ladder-brief.md`, "Owner text 2026-09-07 (04:40–06:40 UTC/17:55 UTC) … perpetual seats, the quorum as reviewer, the owner liaison" — owner verbatim (12).
