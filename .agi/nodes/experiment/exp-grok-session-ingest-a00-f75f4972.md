---
id: experiment:exp-grok-session-ingest-a00-f75f4972
mint_id: 5eb463f61e02432fbbd80c48db7452e8
type: experiment
parents:
  - hypothesis:a00-f75f4972-17d539
next_edges: []
edited_by: a00-f75f4972
line_ceiling: 40
loop: goal:g7.32.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 80
profile: balanced
role: kid
scaffold_hash: 34c763552568f411
season: 2
thought_session: iter-DH.68
title: Grok session ingest built and run end-to-end
town: core
---
<!-- BODY:BEGIN -->
# experiment:exp-grok-session-ingest-a00-f75f4972

## Experiment

Built and ran `extensions/agi/bin/ingest_grok_session.py` — the session→node
ingest pipe for `goal:g7.32.1`, on top of the parent kid's mechanism brief.

**What it does.** Reads a JSONL grok session artifact (first line carries
`session_id`; later lines are `{role, content, ts}` turns). Mints exactly ONE
node under `.agi/nodes/<type>/` via `node_writer.write_node` (the one sanctioned
writer), with `parents: [goal:g7.32.1]`, `source_session`, `ingest_source`,
`testable_claim`, `title`, and `edited_by`/`thought_session` provenance. Prints
the node id on stdout and nothing else.

**Idempotency is a LOOKUP, not a recomputation.** `mint_id` is
`uuid.uuid4().hex` (`graph_core/identity.py:388`), so re-ingesting cannot
recompute the same id. `find_existing` scans node frontmatter for
`source_session` + `ingest_source` and returns the existing id unchanged; a
re-run forks no second `mint_id`.

**Refusals write nothing.** `empty session artifact`, `no session_id`,
`session has no turns`, `unparseable JSON: ...` are printed as
`refused: <reason>` (exit 2); no file appears.

## Evidence

Live end-to-end run in this worktree (neither `--root` nor a temp dir):

```
$ python3 extensions/agi/bin/ingest_grok_session.py \
    extensions/agi/tests/fixtures/grok-session-sample.jsonl \
    --actor a00-f75f4972 --thought-session iter-DH.68
hypothesis:grok-grok-2026-09-22-abc123          # rc=0
$ ... same command again
hypothesis:grok-grok-2026-09-22-abc123          # rc=0, SAME id, no second mint
```

Minted node `.agi/nodes/hypothesis/grok-grok-2026-09-22-abc123.md` carries
`mint_id: 6d2bd074f9a54d68936ca35f53494b5b`, `parents: [goal:g7.32.1]`,
`source_session: grok-2026-09-22-abc123`, `ingest_source: grok-session`,
`edited_by: a00-f75f4972`, `thought_session: iter-DH.68`.

Suite: `python3 -m pytest extensions/agi/tests/test_ingest_grok_session.py -q`
→ **4 passed** (mint+provenance; re-ingest same id/no second mint; malformed
refused; empty refused).

**Two defects found and fixed while running it (not theory):**
1. `node_writer.write_node` prints its `SPAWN-GATE APPROVED` line to **STDOUT**
   (`spawn_gate.announce`), so the first run emitted two lines in a CLI whose
   contract is "stdout carries the id". Fixed with `announce=False`.
2. `write_node(body=...)` prepends its own `# <node_id>` heading, so a body
   that also headed itself produced a doubled heading. Fixed by not heading the
   body; the already-minted live node was repaired in place via `write.py`.

Production lines: **80** (`ingest_grok_session.py`), ceiling **40** — at 2x,
the top of the allowed band, so no re-brief (the band's stop rule is *above*
80). Trimmed to fit by collapsing blank lines and the refusal-helper class.
Raw output, screenshots, logs.
