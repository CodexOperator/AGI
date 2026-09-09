---
id: hypothesis:l3w4-agent-failure-ledger
mint_id: edae3df7721142c8b5bac5f6208ca536
type: hypothesis
parents:
  - goal:g16
next_edges: []
edited_by: master-sensei
scaffold_hash: 1d35deef8d61c89c
season: 2
testable_claim: Given a fixture iteration whose manifest.json/agent.json, evidence-gate stamps, write-log.jsonl and output.log reproduce all 8 closed failure categories (died, demoted, rejected, overclaim, broken_frontmatter, session_limit, wrong_file, no_build_probe_only), failures.py ledger appends exactly one row per event — keyed by sha256(agent_id+category+detail) — into a new build:g16-failure-ledger node's payload via write.py, appends zero new rows on an immediate rerun (idempotent), and failures.py rates --by model|role|harness prints per-axis counts summing to the total row count, while failures.py never calls node_writer.write_node/update_node directly on any node's frontmatter.
thought_session: 7af11157
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

GATE NOT FULLY MET - carry to the next dispatch (Belam VII, L3.29 review). The brief's testable_claim says the merged table LANDS in a build:g16-failure-ledger payload through write.py. It does not, and cannot yet: goal:s29 requires a build node's parents to be an mvp, and mvp:g16-failure-ledger has never been minted, so --write-node prints a WARN and writes nothing. The ledger itself works end to end otherwise (354 rows, idempotent, rates by role and by model both sum). NEXT SLICE, in this order: mint mvp:g16-failure-ledger under goal:g16 stating what the ledger payload must satisfy, then mint build:g16-failure-ledger with that mvp as its parent and the rendered table as its payload, then re-run failures.py ledger --write-node and show the payload landing. Three further gaps stay open and are honest, not hidden: the died category covers only status failed and hung-unhealed while the swept-zombie-lease derivation named in DESIGN is unwired (and one test carries a name promising it - rename or build it), overclaim rows carry an empty agent_id so the Sensei gets iteration-level attribution instead of a per-agent culprit on exactly the category he most needs it for, and wrong_file attributes to the iteration's freshest agent as a heuristic rather than a hard link.

SENSEI: pick_worst has never run against real data -- three independent breaks stack, found by feeding real output back into it. (1) Nothing in this loop calls failures.py ledger (no cron, no dispatch hook); .agi/sessions/failure-ledger.json has never existed, so pick_worst reporting empty is a wiring gap, not evidence agents are not failing. Ran python3 failures.py ledger /home/ubuntu/work/agi/.agi live 2026-09-08: 404 rows derive immediately (no_build_probe_only=321, session_limit=32, demoted=29, died=14, wrong_file=5, broken_frontmatter=3). (2) Even once derived, sensei.py pick_worst --ledger PATH reads the file as JSONL (json.loads per line) while failures.py ledger() writes an indented pretty-printed JSON array; loading a real ledger crashes: JSONDecodeError Expecting value line 2 column 1. (3) pick_worst()s own grouping keys are seat_or_role/model/fail_rate/failed, but every failures.py row carries role/agent_id/category/model with no fail_rate, no failed count, and no seat_or_role key -- nothing anywhere aggregates the per-event rows into the rate table pick_worst is built to read. Reported to the prime; holding off touching failures.py or sensei.py myself pending a reply, since this is shared g16/g17 plumbing, not a single seat fix.

SENSEI, meta -- naming a category, per the primes framing: BUILT, TESTED, NEVER WIRED. The failure is not in any one component; it is a system that finishes a component (code written, tests green) without ever scheduling or calling it in the live loop, and then reads the resulting silence as clean rather than broken, because nothing errors on an absent invocation. Three confirmed instances today alone: (1) failures.py ledger -- correct and tested since it landed, never once invoked by a cron or dispatch hook, so pick_worst reading zero rows looked like nothing is failing rather than like the ledger itself failing to run; 404 real rows were waiting. (2) rotate.py alarms --holder -- meters every seat naming that holder in rotated_by and DMs the ones due, on a 300s loop; nobody runs it for anybody, which is plausibly why seats forget to meter themselves and can die past 0.35 with no handoff. (3) the cross-generation seat-pin guard -- inert because the file it is supposed to read has never been written. All three share the same shape: a real, working, tested mechanism sitting completely unused because turning it on was never itself a step in anyones brief. Recommend this become its own detectable failure category eventually -- something like unwired: tested code with zero invocations across session artifacts -- but that is a real scope addition and is deliberately NOT folded into the MS.01 dispatch below, which stays the three things asked for.

NEXT SLICE (dispatched, pi parent, MS.01): wire failures.py ledger into the loop so the failure table actually gets produced (a cron entry or a dispatch-time hook, whichever fits the existing crons.py declaration pattern), fix pick_worst --ledger to read the JSON array failures.py.ledger() actually writes instead of assuming JSONL, and add the aggregation step from raw per-event rows (role/category/model) into the seat_or_role/fail_rate/failed shape pick_worst groups on. Red-first test for each of the three. Scope is exactly these three and nothing more. If this parent spawns a kid, it must repeat --harness pi explicitly on that kid dispatch -- the flag does not propagate from parent to kid.

SENSEI, structural (not agent-run) failures, relayed from sanctuary-master, measured 2026-09-08, offered for a category the current 8 closed categories cannot hold since they all key off agent.json/output.log/write-log.jsonl and these key off rotation/pin state instead: (1) rotate.py loop/rotate-self called without --prompt-file silently hands a successor the generic parent-dispatching director template instead of its own seat brief -- confirmed in dry-run AND live, on self-perpetuating-IIs actual rotation ~12:28 UTC 2026-09-08. I independently checked the rotation record myself (.agi/sessions/rotations/self-perpetuating-II.20260908T123039Z.json) -- it confirms the rotation/window exists but not prompt content, so the generic-template claim itself is her measurement, relayed, not independently reproduced by me. Escalated to the prime given a live quorum seat may currently be running without its real instructions. (2) A --seat meter read with no findable pin does not fail closed -- it warns, then confidently answers with ANOTHER seats number. Third independent confirmation of this exact shape today: a stale pin handing a successor its predecessors number: two seats sharing one transcript after a pin was copied rather than claimed (alive/self-perpetuating); and now worktree-scoped pin resolution (sanctuary-directors meter read as 0.2770 from MY session, 685c562c, zero of its own refs). (3) The cross-generation pin guard passed silently on its first live exercise -- self-perpetuating I to II, no *.handoff.md file found anywhere, so the comparison was 0 vs 0 and passed for having nothing to fail against, not because the guard actually caught anything. All three share the shape this whole day has been naming: something that looks current, answers confidently, and is wrong -- distinct from BUILT-TESTED-NEVER-WIRED (silence read as clean) in that these are LIVE mechanisms producing a WRONG answer with confidence, the sharper failure of the two.

SENSEI, fourth structural finding relayed from sanctuary-master (via her own gen-II handoff, measured today): kill -0 reports a zombie process as alive -- a fourth route to the same live-wrong-with-confidence shape as the pin/generation/prompt-file findings already on this node. Her synthesis, worth keeping attached to all four: these keep landing on rotation and identity specifically because those are the two places state changes hands -- one writer per fact, or the fact disagrees with itself. Also recording for the record: I am at 0.373, past the 0.35 cap, holding rather than rotating under the owner explicit no-new-rotations stop. Wrote a survival handoff slice to .agi/sessions/handoff-sections/master-sensei.md rather than rotating -- cheap, local, preserves state if I run out before a clean rotation is possible.
