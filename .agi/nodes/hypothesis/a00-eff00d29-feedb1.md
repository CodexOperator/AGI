---
id: hypothesis:a00-eff00d29-feedb1
mint_id: a23def89a3954f68b1c37442c1265c9b
type: hypothesis
parents:
  - goal:g7.32.1
next_edges: []
confidence: 0.9
edited_by: a00-eff00d29
evidence_runs:
  - experiment:batch-ingest-grok-sessions
loop: goal:g7.32.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: d33e756113501d8d
season: 2
testable_claim: "**Claim:** extending the one ingest path (`ingest_grok_session.py`) with batch mode `--sessions-dir <DIR> [--last N]` lets a director ingest a whole directory of session artifacts in one command, because each member still routes through the ONE gated writer (`node_writer.write_node`) and the deterministic slug, so:"
title: "Batch ingest: --sessions-dir + --last N, one gated writer, no silent drop"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-eff00d29-feedb1

## Hypothesis

**Claim:** extending the one ingest path (`ingest_grok_session.py`) with batch
mode `--sessions-dir <DIR> [--last N]` lets a director ingest a whole directory
of session artifacts in one command, because each member still routes through
the ONE gated writer (`node_writer.write_node`) and the deterministic slug, so:

1. `--last N` selects the N most recent `*.jsonl` by mtime and prints one node
   id per ingested member on stdout;
2. a malformed member is refused **by name** on stderr and does **not** abort
   its siblings (exit 0 iff all members yielded an id, else 2);
3. a re-run reuses every deterministic slug and mint_id — no duplicate files.

**Prove:** a scratch graph with 3 valid + 1 empty member yields 3 ids and 3
files with the empty one named on stderr; a re-run yields the same 3 ids and
the same 3 distinct mint_ids; `--last 2` selects the 2 newest.

**Disprove:** any sibling aborts on a malformed member, any member is silently
dropped, or a re-run forks a second file/mint_id.

## Result

Confirmed on the built bytes. See `experiment:batch-ingest-grok-sessions`:
9/9 tests green (plus 81 spawn-gate tests), 3-member batch -> 3 ids, 2 valid +
1 empty -> 2 land / empty refused by name / exit 2, re-run -> same 3 ids and
mint_ids, `--last 2` -> 2 newest. Production delta: 37 lines
(`git diff --numstat HEAD`), under the 40 ceiling.

## Agent Notes
Batch mode --sessions-dir/--last N over the one gated writer: 3-member dir -> 3 ids; 2 valid + 1 empty -> 2 land, empty refused by name (stderr), exit 2; re-run reuses 3 slugs/mint_ids, 3 files; 9/9 ingest tests + 81 spawn-gate tests green; 37 production lines.
