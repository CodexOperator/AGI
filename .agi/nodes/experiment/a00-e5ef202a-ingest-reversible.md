---
id: experiment:a00-e5ef202a-ingest-reversible
mint_id: 589b49603a504fc280dccf3831d0f2ff
type: experiment
parents:
  - hypothesis:a00-e5ef202a-0326f9
next_edges: []
edited_by: a00-e5ef202a
line_ceiling: 40
loop: goal:g7.32.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 36
profile: balanced
role: kid
scaffold_hash: cfadab05f383f29d
season: 2
tags:
  - grok-session
  - ingest
  - injective
thought_session: a00-e5ef202a-DT.66
title: Ingest key injective by reversible encoding, not a truncated hash
town: core
---
# experiment:a00-e5ef202a-ingest-reversible

## Experiment

Fix the parent's falsifier on `hypothesis:a00-a317e857-9dba03` (demoted to
`inconclusive_lean_disproved:60`): `slug_for` appended `sha256(raw_id)[:8]` to a
non-UUID id, a 32-bit birthday bound rather than an injection. Two distinct raw
ids sharing a canon *and* an 8-hex suffix mapped to one file; the second ingest
printed `INGEST skip`, exit 0, and the session was silently dropped — breaking
the goal invariant "no silent drop".

### The encoding (production: 36 added / 8 deleted lines, ceiling 40)

`extensions/agi/bin/ingest_session.py::slug_for` keeps the canonical-UUID branch
(bare slug, unchanged, so the one live node `doc:grok-session-019ddd0f-...`
stays idempotent) and replaces the truncated hash with a **reversible** suffix:

```python
if _UUID.match(sid.lower()):
    return "grok-session-" + sid.lower()
canon = re.sub(r"[^a-z0-9]+", "-", sid.lower()).strip("-")
suffix = sid.encode("utf-8").hex()          # raw bytes -> hex, a bijection
slug = f"grok-session-{canon}-{suffix}" if canon else f"grok-session-{suffix}"
if len(slug) > _MAX_SLUG:                   # 200
    raise SlugTooLong("slug-too-long: ... refusing rather than truncating")
```

Proof injectivity is a property of the encoding, not a probability:

1. `hex` is a bijection on byte strings, so `raw_a != raw_b` implies
   `hex_a != hex_b` — no collision is possible, at any input size.
2. The slug's tail is fixed-length for a given raw length. Two slugs can be
   equal only if their tails are equal (string equality) and the tails have
   equal length, so `tail_a == tail_b`, hence `raw_a == raw_b`. The cosmetic
   `canon` prefix cannot rescue a collision because the tail alone determines
   the raw id.
3. The UUID and non-UUID branches have disjoint shapes: a bare
   `grok-session-<uuid>` vs `grok-session-<canon>-<hex>`; a non-UUID id whose
   canon looks like a UUID still carries a hex tail, so it never lands on a
   bare-UUID path.

An over-long slug is **refused BY NAME** (`slug-too-long`, exit 2) rather than
truncated — a truncation would reintroduce exactly the collision this encoding
removes, so there is deliberately no fallback below the 200-char guard.

## Evidence

Raw transcript against a throwaway graph root (`<scratch>/graph`,
`.agi/context` copied in), stdout+stderr, no editing.

### The parent's crafted collision pair — the falsifier

A = `x_-x:x.x.x_~-x-x_~x.x~x~x`, B = `x__x._x:.x._x~x_-x_-.x__~x_-x-x`
(under the old scheme both -> `...-e4ab01f1`; B was skipped).

```
INGEST ok doc:grok-session-x-x-x-x-x-x-x-x-x-x-x-785f2d783a782e782e785f7e2d782d785f7e782e787e787e78
exit=0
INGEST ok doc:grok-session-x-x-x-x-x-x-x-x-x-x-x-785f5f782e5f783a2e782e5f787e785f2d785f2d2e785f5f7e785f2d782d78
exit=0
--- files after collision pair ---
grok-session-x-x-x-x-x-x-x-x-x-x-x-785f2d783a782e782e785f7e2d782d785f7e782e787e787e78.md
grok-session-x-x-x-x-x-x-x-x-x-x-x-785f5f782e5f783a2e782e5f787e785f2d785f2d2e785f5f7e785f2d782d78.md
--- source_session values ---
source_session: x_-x:x.x.x_~-x-x_~x.x~x~x
source_session: x__x._x:.x._x~x_-x_-.x__~x_-x-x
```

**Two files, two ids, each carrying its OWN raw `source_session` — no session
lost.** (Both A and B also share the same `canon` prefix, and A is the same
id the parent probe used, so this is the parent's exact falsifier.)

### Original `Probe-aaaa-1111` / `probe_aaaa_1111` pair

```
INGEST ok doc:grok-session-probe-aaaa-1111-50726f62652d616161612d31313131
INGEST ok doc:grok-session-probe-aaaa-1111-70726f62655f616161615f31313131
```

Two distinct ids (hex `50726f...` = `Probe-aaaa-1111`, `70726f...` =
`probe_aaaa_1111`) — the first falsifier kid 1 hit, still fixed.

### Real corpus UUID — fresh mint then re-ingest, plus case

```
INGEST ok   doc:grok-session-019ddd0f-6751-75bc-a374-6c0fe036e262   exit=0
INGEST skip doc:grok-session-019ddd0f-6751-75bc-a374-6c0fe036e262   exit=0   (re-ingest)
INGEST skip doc:grok-session-019ddd0f-6751-75bc-a374-6c0fe036e262   exit=0   (UPPER-cased UUID = same session)
```

Bare slug preserved, so the live node is never forked; UUID case-insensitivity
holds.

### Named refusals (never a crash, never a silent drop)

```
INGEST refuse no-session-id: the session record has no id          exit=2
INGEST refuse no-session-record: no {"type":"session"} line        exit=2
INGEST refuse slug-too-long: slug is 914 chars (limit 200) for a 300-char session id; refusing rather than truncating   exit=2
```

### Length guard boundary: accept exactly 200, refuse above

```
slug-len expected for 200: 200 -> rc=0 out='INGEST ok doc:grok-session-ab-61622d7e...' err=''
slug-len expected for 202: 202 -> rc=2 err='INGEST refuse slug-too-long: slug is 202 chars (limit 200) ...'
```

### Tests

```
$ python3 -m pytest extensions/agi/tests/test_ingest_session.py -q
.........                                                                [100%]
9 passed in 14.63s
```

Kid 1's 4 and kid 2's 2 tests still pass; 3 added: the parent's hash-colliding
pair (asserts two distinct files each with its own `source_session`), the
over-long-id refusal by name, and the 200/202 length boundary.

## Constraints honored

`dispatch.py` / `rotate.py` untouched; zero `grok` special-case; nothing under
`.agi/bin/`; scratch under `.agi/sessions/iter-DT.66/a00-e5ef202a/`; the only
git command was one read-only `git diff --numstat`.

## Secondary caveat (carried, deliberately NOT fixed here)

Kid 1's real-graph node is left UNTRACKED by `cli.py done` because
`_round_scope_ok` (`cli.py:2084`) keeps only `.agi/nodes/` paths whose basename
contains the round's agent id, and `grok-session-<uuid>.md` does not. So a
director-run ingest's residue does not reach the branch tip. A safe fix is
caller-side (the ingest tool takes an explicit slug prefix, or the invoking
director commits that residue outside `done`); `_round_scope_ok` must NOT be
widened — it is the `add -A` hazard guard.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHAT CHANGED: kid 2's non-UUID branch was `sha256(raw)[:8]`, a 32-bit birthday
bound; the parent's probe found two raw ids sharing that suffix and the second
session was silently skipped. THE CHOICE: the brief offered reversible encoding
or strict UUID validation. I took the encoding because strict validation would
refuse the sibling fixture id `grok-2026-09-22-abc123`, which is a legitimate
non-UUID session id — refusing it would be a named refusal, but of a session the
tool should ingest. Hex of the raw UTF-8 bytes is the smallest reversible
suffix that needs no padding or alphabet reasoning (base64url's `=` strip and
`-`/`_` alphabet are one more thing to prove injective; hex is a bijection by
definition). The UUID branch is kept verbatim so the ONE live node at
`doc:grok-session-019ddd0f-...` stays idempotent — kid 2's hybrid already got
that right and re-slugging would have forked it. The length guard is REFUSAL,
never truncation: a truncated reversible suffix stops being reversible and
silently recreates the collision, so there is no fallback below 200. DEVIATION
FROM THE BRIEF, disclosed: the brief suggested the experiment could parent to
`[goal:g7.32.1]`, but `[experiment].md` removed `goal` from `allowed_parents`
(goal:s22), so a goal parent would be refused by the real gate; I parented to
`hypothesis:a00-a317e857-9dba03`, the demoted hypothesis whose falsifier this
run fixes. The kernel caveat (kid 1's residue not tracked by `done`) is a
different mechanism, out of this round's scope, and is recorded above rather
than papered over.
<!-- THOUGHT:END -->
