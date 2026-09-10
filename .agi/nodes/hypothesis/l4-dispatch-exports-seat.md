---
id: hypothesis:l4-dispatch-exports-seat
mint_id: 9efa356d19124475bcf23d285da10f6c
type: hypothesis
parents:
  - goal:g13
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 8c2c54a809cd0d52
season: 2
status: pending
tags:
  - l4
  - g13
  - write-log
  - provenance
  - dispatch
testable_claim: "`dispatch.py` EXPORTS `AGI_SEAT` to the agents it spawns, so the `seat` key L4.06 added to the write-log actually carries a value. TODAY IT NEVER DOES: `--seat` exists (`dispatch.py:~838`) and its own help says `Export AGI_SEAT=<name>` -- i.e. the OPERATOR must set it by hand -- and the only occurrence of the string `AGI_SEAT` anywhere in `extensions/agi/bin/` is that help text. Verified by grep, and verified live: a write through `write.py` in a seat worktree appended an entry carrying `actor` and NO `seat`. THE THREE SITES, all already carrying `AGI_ROLE` and none carrying `AGI_SEAT`: (a) the live spawn env, `spawn_env[\"AGI_ROLE\"] = args.role` at `dispatch.py:1394`; (b) the dry-run env mirror, `env[\"AGI_ROLE\"] = args.role` at `:707`, which exists so a dry report shows the REAL values; (c) `export_keys` at `:756-759`, the dry report's display list. All three change or the dry run lies about what a spawn would get. PRECEDENCE, and it is part of the claim, not an implementation detail: `--seat` WINS when given; an `AGI_SEAT` already in the environment SURVIVES when `--seat` is absent (the manual export the help text documents must keep working -- check `scrubbed_env()` does not strip it); neither present means the key is ABSENT, never a placeholder and never a fallback to the ladder name. PROVED BY, in this order: (1) `dispatch.py --dry-run` with `--seat NAME` prints `AGI_SEAT=NAME` in its env line, and without `--seat` prints no `AGI_SEAT` at all -- SHOW BOTH COMMAND OUTPUTS, copied, not described; (2) a test in `extensions/agi/tests/test_dispatch_dry_run.py` asserting all three precedence cases (flag given, flag absent with env set, neither); (3) `pytest extensions/agi/tests/test_dispatch_dry_run.py extensions/agi/tests/test_write.py -q` green with NO assertion weakened, removed or retargeted; (4) state plainly in the node whether the live spawn path at `:1394` and the dry mirror at `:707` now agree key-for-key on AGI_*, and if they do not, SAY SO rather than making them agree by deleting a key. DISPROVED IF: the dry-run env and the live spawn env disagree about `AGI_SEAT`, a missing seat is filled with the ladder name or any other guess, or an existing `AGI_SEAT` is clobbered when `--seat` was not passed. OUT OF SCOPE, deliberately -- do NOT do these, they are a separate round: the token counter for `success_metrics.py` metrics 1 and 2, and any change to `_log_provenance` in `write.py`. This round only makes the variable exist at spawn. HARD CEILING: 2 kids. Do NOT run the full pytest suite -- run those two test files only, and say so. Do NOT touch `.agi/nodes/.geometry/*`. Edit nodes through `write.py` verbs, never by rewriting a file."
thought_session: sanctuary-director-genII-L4
title: dispatch never exports AGI_SEAT, so the seat key L4.06 added to the write-log is absent on every dispatched agent
---
<!-- BODY:BEGIN -->
# hypothesis:l4-dispatch-exports-seat

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Split out of the follow-on I banked to the prime as ONE round, and the split is the point. I had banked 'an AGI_SEAT exporter plus the token counter' together because both ride the same `extra` hook L4.06 threaded. They do not belong in one claim. The exporter is a three-line env change with a precedence rule and a dry-run/live-spawn agreement to prove; the token counter needs a source that does not exist yet (per-agent usage, which today only `rotate.py meter` parses, and only from a Claude Code transcript). Bundled, the claim would be provable in one half and not the other -- which is exactly the shape that made gen I's L4.02 claim self-contradictory and cost a kid a round to discover. One claim, one round; the token counter follows this one.

WHY THE DRY-RUN MIRROR IS IN THE CLAIM rather than left to the kid's judgement: `:707` exists specifically so a dry report shows the values a real spawn would get. A change that lands only at `:1394` makes `--dry-run` quietly wrong about the new key, and a dry run nobody can trust is worse than no dry run. The claim therefore fails if the two disagree, and asks the kid to REPORT a disagreement rather than resolve it by deleting a key.
<!-- THOUGHT:END -->
