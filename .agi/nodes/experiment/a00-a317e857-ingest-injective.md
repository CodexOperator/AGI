---
id: experiment:a00-a317e857-ingest-injective
mint_id: 526e674ba4934ba4ab0c162d41728995
type: experiment
parents:
  - hypothesis:a00-a317e857-9dba03
next_edges: []
edited_by: a00-a317e857
line_ceiling: 40
loop: goal:g7.32.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 22
profile: balanced
role: kid
scaffold_hash: 5a1e19f546198feb
season: 2
thought_session: a00-a317e857-DT.66
title: "Ingest key is injective: UUID bare slug, others sha256-suffixed"
town: core
---
# experiment:a00-a317e857-ingest-injective

## Experiment

Fix the ONE negative probe on `hypothesis:a00-dee8ad86-1ab674` (parent review
demoted it to `inconclusive_lean_disproved:70`): two DISTINCT session ids that
sanitize alike collapsed to one slug, so the second session hit an existing
path, `write_node(on_exists=SKIP)` returned SKIPPED, exit was 0, and the session
was silently dropped. The goal's invariant is "No silent drop: every ingest
writes a measurable node id or a refused reason".

### The fix (production: 22 added / 2 deleted lines, ceiling 40)

`extensions/agi/bin/ingest_session.py::slug_for` now splits the domain in two
disjoint cases:

```python
_UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")

def slug_for(sid):
    canon = re.sub(r"[^a-z0-9]+", "-", sid.lower()).strip("-")
    if _UUID.match(sid.lower()):
        return "grok-session-" + canon
    digest = hashlib.sha256(sid.encode("utf-8")).hexdigest()[:8]
    return f"grok-session-{canon}-{digest}"
```

- A **canonical UUID** (all 24 files in the repo-root `sessions/` corpus have
  one) keeps its BARE slug, so the node already minted by kid 1 at
  `doc:grok-session-019ddd0f-6751-75bc-a374-6c0fe036e262` stays idempotent and
  is never duplicated. UUID case is not significant, so `lower()` first keeps an
  upper-cased UUID the SAME session (measured below).
- **Every other id** gets a short `sha256(raw_id)` suffix, so two raw ids that
  sanitize alike address different files.

### Why this closes the loss, and what it does NOT close

`canon` alone is a lossy map (many raw ids -> one string); the suffix is a
function of the raw bytes, so `raw_a != raw_b` implies a different suffix except
on a sha256 8-hex collision (~2^-32, not audited). The UUID branch and the hashed
branch are disjoint in shape (`<canon>` vs `<canon>-<8hex>`) and cannot be
confused. **Not closed:** the key is still the *file path* — if someone deletes
the node and re-ingests, a new mint_id is issued (idempotence is the file's
existence, unchanged from kid 1); and 8 hex chars is a probabilistic bound, not
a proof.

## Evidence

Probe run against a throwaway graph root
(`.agi/sessions/iter-DT.66/a00-a317e857/graph`, schemas copied in). Raw
transcript, `2>&1`, no editing:

```
$ python3 extensions/agi/bin/ingest_session.py <scratch>/p_real.jsonl --out-root <scratch>/graph
INGEST ok doc:grok-session-019ddd0f-6751-75bc-a374-6c0fe036e262
exit=0
$ python3 extensions/agi/bin/ingest_session.py <scratch>/p_real.jsonl --out-root <scratch>/graph
INGEST skip doc:grok-session-019ddd0f-6751-75bc-a374-6c0fe036e262
exit=0
$ python3 extensions/agi/bin/ingest_session.py <scratch>/p_coll_a.jsonl --out-root <scratch>/graph
INGEST ok doc:grok-session-probe-aaaa-1111-bd22a2c0
exit=0
$ python3 extensions/agi/bin/ingest_session.py <scratch>/p_coll_b.jsonl --out-root <scratch>/graph
INGEST ok doc:grok-session-probe-aaaa-1111-4058a4f3
exit=0
$ python3 extensions/agi/bin/ingest_session.py <scratch>/p_noid.jsonl --out-root <scratch>/graph
INGEST refuse no-session-id: the session record has no id
exit=2
$ find <scratch>/graph/nodes -name '*.md' | sort
<scratch>/graph/nodes/doc/grok-session-019ddd0f-6751-75bc-a374-6c0fe036e262.md
<scratch>/graph/nodes/doc/grok-session-probe-aaaa-1111-4058a4f3.md
<scratch>/graph/nodes/doc/grok-session-probe-aaaa-1111-bd22a2c0.md
$ grep -H '^source_session:' <scratch>/graph/nodes/doc/grok-session-probe-*.md
.../grok-session-probe-aaaa-1111-4058a4f3.md:source_session: probe_aaaa_1111
.../grok-session-probe-aaaa-1111-bd22a2c0.md:source_session: Probe-aaaa-1111
```

`p_coll_a` carries `{"type":"session","id":"Probe-aaaa-1111"}`, `p_coll_b`
carries `id":"probe_aaaa_1111"` — the exact pair the parent's falsifier used.
Before the fix both sanitized to `grok-session-probe-aaaa-1111` and the second
printed `INGEST skip`, minted nothing. Now: **two files, two ids, and each
carries its own raw `source_session`** — no session lost.

The parent's three original conjuncts re-run in one transcript: fresh mint
(ok + file), re-ingest (`skip`, one file, same id), malformed (refuse by name,
exit 2). Plus the UUID-continuity behaviour: re-ingesting the real corpus node
prints `INGEST skip` on the BARE slug, so the existing graph node is not forked.

### Test run

```
$ python3 -m pytest extensions/agi/tests/test_ingest_session.py -q
......                                                                   [100%]
6 passed in 22.53s
```

Kid 1's 4 tests still pass; 2 new ones added: the colliding-pair falsifier
(asserts two distinct files or a named refusal, never one node for two sessions)
and UUID case-insensitivity / bare-slug continuity.

## Secondary caveat (noted, deliberately NOT fixed here)

Kid 1's real-graph node was left UNTRACKED by its own `done` commit because
`_round_scope_ok` (`cli.py:2084`) carries only `.agi/nodes/` paths whose basename
contains the round's agent id, and `grok-session-<uuid>.md` does not. So the
residue the *director-run* ingest creates does not reach the branch tip. A safe
fix is a caller-side one — the ingest tool takes an explicit slug prefix, or the
invoking director commits that residue outside `done`. `_round_scope_ok` must
NOT be widened: it is the `add -A` hazard guard. Left untouched this round.

## Constraints honored

`dispatch.py` and `rotate.py` untouched; nothing under `.agi/bin/`; scratch under
`.agi/sessions/iter-DT.66/a00-a317e857/`; no git commands except one read-only
`git diff --numstat`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version of this node; nothing preceded it. Chose the hybrid (bare slug
for canonical UUIDs, sha256 suffix otherwise) over the two options the brief
offered because BOTH pure options have a cost the hybrid avoids: strict UUID
validation would refuse any non-UUID id the tool might legitimately meet (a
sibling fixture already carries `grok-2026-09-22-abc123`), and an unconditional
hash suffix would re-slug the 24 real UUID sessions and fork the node kid 1
already minted at the bare `grok-session-<uuid>` — a duplicate on re-ingest,
which is the very invariant the goal protects. The UUID branch is guarded by
`sid.lower()` so case-variant UUIDs stay one node (case is not significant in a
UUID) while case-variant non-UUIDs still get distinct hashes. The experiment is
parented to my own hypothesis, not the goal: `[experiment].md` removed `goal`
from `allowed_parents` (goal:s22), so the brief's `parents: [goal:g7.32.1]`
would be refused by the real gate — same wall kid 1 hit.
<!-- THOUGHT:END -->
Raw output, screenshots, logs.
