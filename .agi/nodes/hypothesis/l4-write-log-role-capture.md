---
id: hypothesis:l4-write-log-role-capture
mint_id: 03aa4c36b22f4f889b18d04381036d17
type: hypothesis
parents:
  - goal:g13
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 94a5254f20456703
season: 2
status: pending
tags:
  - l4
  - g13
  - write-log
  - provenance
testable_claim: "Every write-log entry records WHO wrote it. `node_writer._log_write` (`extensions/agi/bin/node_writer.py:1070-1126`) builds each entry from ts/operation/node_id/mint_id/path/sha256 and merges an optional `extra` dict at `:1120-1121`; TODAY NO CALLER PASSES AN ACTOR -- verified in two live entries in `.agi/sessions/write-log.jsonl`. Add `actor`, `role` and `seat` THROUGH THAT SAME `extra` HOOK: do not add a second logging path, and do not change or reorder the entry's existing six keys. The actor is already known at the call sites -- `write.py submit()` (`:545`) and `write.py create()` (`:932`) both take `actor=` and `session=` and already stamp provenance frontmatter, and `_default_actor()` (`write.py:889`) is the fallback. `role` and `seat` are READ from what the environment already sets, never invented: when a source is absent the key is ABSENT, never a placeholder. PROVED BY, in this order: (1) one write through `write.py submit` and one through `write.py create` each append an entry carrying `actor` -- and carrying `role`/`seat` where resolvable -- SHOW THE APPENDED JSON LINES copied out of `.agi/sessions/write-log.jsonl`, never a description of them; (2) `python3 extensions/agi/bin/write_guard.py check` still exits 0 and silent, and `check --strict` still reads the log (`write_guard.py:127 _load_log`, `:252 cmd_check`) with the new keys present; (3) `pytest extensions/agi/tests/test_write.py extensions/agi/tests/test_write_guard.py -q` green -- NO assertion weakened, removed or retargeted; (4) an entry written when no actor is resolvable still carries all six original keys and simply omits the new ones. DISPROVED IF: the six existing keys change shape or order, a second logging path appears, a missing actor is filled with a guess or a `TODO`, or any assertion is edited to make the suite green. HARD CEILING: 2 kids. Do NOT run the full pytest suite -- run those two test files only, and say so. Do NOT touch `.agi/nodes/.geometry/*`. Do NOT edit any node by rewriting its file -- use `write.py` verbs."
thought_session: sanctuary-director-genII-L4
title: The write-log records what was written and never who wrote it, so no report can name a node written by a role its schema does not admit
---
<!-- BODY:BEGIN -->
# hypothesis:l4-write-log-role-capture

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DEVIATION FROM `doc:l4-plan` §5.2, recorded rather than silently taken. The plan's dependency graph draws L4.05 and L4.06 as siblings, both depending only on L4.02 and both feeding L4.04. They are not siblings: L4.06 is L4.05's PREREQUISITE. L4.05 is `links.py roles`, a dry report naming every node written by a role its schema does not admit -- and there is no such data to read. `node_writer._log_write` (`node_writer.py:1110-1121`) builds every write-log entry from exactly six keys plus an optional `extra` dict, and no caller passes an actor, a role or a seat; two live entries in `.agi/sessions/write-log.jsonl` were read to confirm it rather than inferred from the code. An L4.05 run today could only report nothing, and a report that is empty by construction reads as a clean bill of health. So L4.06 runs first and L4.05 waits for its data. The ordering is the deviation; the plan's L4.02 dependency is untouched and L4.02 itself landed at L4.32 -- `[moral].md:3` carries `written_by: owner` and `write.py:514 _enforce_written_by` reads it as data.

WHY THE `extra` HOOK AND NOT A NEW FIELD SET. The hook already exists at `node_writer.py:1120-1121` and is already how `payload_ref`, `location` and `sha256` reach an entry (`:449`, `:506`, `:515`). Adding a second logging path to carry provenance would put two writers on one file, which is the shape this project keeps paying to remove. The claim therefore forbids the second path explicitly, and forbids a placeholder for a missing actor: `goal:g2.10` spent 8,034 fields teaching this corpus that an invented value is worse than an absent one.
<!-- THOUGHT:END -->
