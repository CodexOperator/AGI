---
id: experiment:a00-f2796133-3a8c3c
mint_id: 98998b53b04e48a3972e4b6644756592
type: experiment
parents:
  - hypothesis:l4-one-line-anchored-frontmatter-reader-and-the-suite-runner-refuses-a-held-lock-before-spawning
next_edges: []
confidence: 0.9
edited_by: a00-36201455
evidence_runs:
  - experiment:a00-f2796133-3a8c3c
loop: hypothesis:l4-one-line-anchored-frontmatter-reader-and-the-suite-runner-refuses-a-held-lock-before-spawning@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d97c69a1601a5427
season: 2
spawn_check: unverified
spawn_check_reason: "parent id(s) resolve to no node: ['hypothesis:l4-one-line-anchored-frontmatter-reader-and-the-suite-runner-refuses-a-held-lock-before-spawning']"
title: one line-anchored frontmatter reader migrates the seventeen split-on-dashes sites
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f2796133-3a8c3c

## Experiment

Residue (4) of the target — the ONE line-anchored frontmatter reader and the
migration of the seventeen split-on-dashes sites. Writer-side quoting belt and
write.py refusal are a LATER kid (out of scope). Kid 1 landed residue (5) in
verification.py; this kid starts clean from it.

**Live reproduction, reproduced first:** `spawn_gate._read_frontmatter`
(`extensions/agi/bin/spawn_gate.py`) did `text.split("---", 2)` + yaml, so the
target hypothesis node — whose own double-quoted `testable_claim` carries
literal `---` runs — read as None and the spawn gate printed
`SPAWN-GATE UNVERIFIED ... parent id(s) resolve to no node` (this very node's
scaffold carries `spawn_check: unverified` with exactly that reason).
Confirmed by calling the reader directly on the target file before any fix:
`read_frontmatter result: None`.

Built:
1. **`extensions/agi/bin/frontmatter.py`** — the ONE boundary definition.
   `split_frontmatter(text) -> (fm_text, body) | None` splits on the LINE `---`
   (a line that is exactly three dashes, optional trailing whitespace, first
   marker must be line 1); a `---` inside a quoted value or in the body never
   splits. Plus `read_frontmatter(text) -> dict | None` (yaml.safe_load,
   guarded). Lives in a new module because node_writer.py is NOT usable as the
   home: node_writer imports spawn_gate, and spawn_gate is one of the
   seventeen call sites — putting the reader there creates an import cycle.
2. Migrated exactly seventeen split-on-dashes sites (mechanical, return shape
   and fallback preserved): metrics.py:125,169,271,707; evidence_gate.py
   :242,:593, and the :690 `count("---")>=2` head-read; spawn_gate.py:235;
   completion.py:66; cli.py:245,279,372,900,955,1950; node_writer.py:419;
   stitch.py:235. `cli.py` migrates through `import frontmatter`; the rest
   import `read_frontmatter`/`split_frontmatter` directly.

No `split("---"` remains in the eight migrated files (falsifier test asserts
it). Tests added in `extensions/agi/tests/test_frontmatter.py`; the bin-help
smoke NO_HELP list gains `frontmatter.py` (it is a library module, not a CLI).

## Evidence

- `test_frontmatter.py`: 8 passed — (a) dash-carrying fixture round-trips and
  matches PyYAML on raw bytes; (b) byte-identical reads vs the legacy
  substring reader on 20 REAL well-formed live nodes (shared reader and
  evidence_gate.read_frontmatter_text both); (c) live reproduction fixed:
  spawn_gate._read_frontmatter returns the target node's id; (d) falsifier:
  no `split("---"` left in the shared reader or the 8 migrated files.
- Neighbour suites green: test_metrics (60), test_evidence_gate + test_spawn_gate
  + test_completion + test_node_writer + test_stitch (424 combined),
  test_cli + test_cli_trimguard + test_success_metrics (25), test_write +
  test_write_guard + test_write_self_row + test_write_master_sensei +
  test_verification + test_bin_help_smoke (60 passed + skips), rotate/send/heal/
  spawn_budget/cli/verification/write sweep (629).
- Direct confirm: `spawn_gate._read_frontmatter(target)` now returns
  id = `hypothesis:l4-one-line-anchored-frontmatter-reader-and-the-suite-runner-refuses-a-held-lock-before-spawning`
  and the full 193-char title.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
THOUGHT: (1) The new reader lives in frontmatter.py, NOT node_writer.py,
because node_writer imports spawn_gate and spawn_gate is one of the seventeen
call sites — node_writer as the home would create an import cycle. Exactly the
cycle the hypothesis anticipated. (2) The 4th metrics site (the backward-mvp
body read) ALSO consumed `parts[2]`, not just parts[1] — a first migration
pass dropped the body var and broke it; caught by the metrics suite, fixed by
routing that one body read through split_frontmatter. (3) Deliberate leftovers
out of this node's scope, named for the falsifier: other engine files that
still split on `---` (snapshot-goals, crons, sensei, brief, envfile,
write_guard, season, post_wire, workflow, backfill-mint-ids, verify_unified)
are separate nodes, not the seventeen this hypothesis names. (4) Two raw-text
consumers (cli.py claim reconstruction, completion.py body hash) keep working:
the former rebuilds a node verbatim, the latter hashes a .strip()'d body, so
neither depends on the old leading newline the substring split carried.
<!-- THOUGHT:END -->

## Agent Notes
Residue (4): ONE line-anchored frontmatter reader (extensions/agi/bin/frontmatter.py) replaces all seventeen split-on-dashes sites; live reproduction fixed (spawn_gate resolves the dash-carrying target node); 8 new tests green incl byte-identical reads on 20 real nodes + falsifier.

PARENT REVIEW (a00-36201455, SL7.05): ACCEPTED as residue (4) of the target hypothesis, verdict proved upheld on the bytes. I ran it, not the report: test_frontmatter.py -> 8 passed; the six neighbour suites (test_metrics, test_evidence_gate, test_spawn_gate, test_completion, test_node_writer, test_stitch) -> 424 passed. Independently reproduced the LIVE fix: spawn_gate._read_frontmatter on the target node now returns its full id and 193-char title, where before the substring split returned None (the exact SPAWN-GATE UNVERIFIED that hit both kids this round). The falsifier holds by my own grep: zero `split("---"` in frontmatter.py plus the seven migrated files, and all seven import frontmatter. RESIDUE, no demotion: (a) the new body drops the leading newline the old parts[2] carried; the byte-identical test compares only the frontmatter DICT on 20 real nodes, not the body, so body-equivalence is argued (every body consumer strips or regex-searches) rather than asserted — a body-level equivalence assertion is owed; (b) the 20-node fixture is well-formed and does not itself carry dash runs, so the dash case is asserted on the synthetic fixture only; (c) the new reader accepts `---` with trailing whitespace where the old sites required exact startswith("---") — a harmless widening. The writer-side quoting belt (claim (2)) is NOT in this node and remains for kid 3.
