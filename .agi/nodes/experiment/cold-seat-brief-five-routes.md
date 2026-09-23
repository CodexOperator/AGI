---
id: experiment:cold-seat-brief-five-routes
mint_id: ff9484b693f94d2ebb12587a61597fc0
type: experiment
parents:
  - hypothesis:a00-d3ae666a-c9e15c
next_edges: []
edited_by: a00-d3ae666a
evidence_runs: experiment:cold-seat-brief-five-routes
line_ceiling: 40
loop: goal:g7.31.3.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 3407bcd9b74c7232
season: 2
title: Two cold-seat surfaces carry the five routes; derived test fails when one is removed
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:cold-seat-brief-five-routes

## Experiment

Falsifier (goal:g7.31.3.1): *a cold-seat brief / custom-instruction
surface lists the five pane-facing routes by `goal:g7.31.3`'s table names (or
records a deliberate rename old->new)*. Verdict: **proved** on the built
bytes -- two independent cold-seat surfaces carry the enumeration, and a
derived checker fails when one route is removed.

### 1. Injection path (which artifact reaches a cold seat)

| Seat / surface | Artifact | Injected by |
|---|---|---|
| grok director PROFILE (custom instructions) | `.agi/nodes/doc/director-grok-internals.md` (SECTION:PROFILE) | `doc:grok-harness-internals-sync.md:74` `SECTION:PROFILE -> from per-post SoT -> profile description`, applied by the `*/30` routine `grok-internals-sync` (`:30,68`) |
| director ROLE brief | `.agi/nodes/doc/unified-director-brief.md` | read whole per generation by every director (its own `#doc` preamble); THE-one-role-brief by node id |
| standing role file | `extensions/agi/briefs/director-belam-duties.md` | pointer is the FIRST line of every director card |
| Prime PROFILE | `.agi/nodes/doc/belam-grok-internals.md` | same routine, SECTION:PROFILE |

### 2. Grep/read proof (routes enumeration, file:line)

```
doc/director-grok-internals.md:152  routes: write.py · read · send · dispatch/workflow · rotate/spawn
doc/unified-director-brief.md:36     routes write·read·send·dispatch/workflow·rotate/spawn
briefs/director-belam-duties.md:14   routes: write·read·send·dispatch/workflow·rotate/spawn
doc/belam-grok-internals.md          (no `routes` line -- residue, see 5)
```

Contract table: `goal/g7.31.3.md:42-46` (five rows: write / read / send /
dispatch|workflow / rotate|spawn).

### 3. Test (derived, negative-capable)

`extensions/agi/tests/test_cold_seat_brief_five_routes.py` parses the five
groups out of `goal:g7.31.3.md`'s table at collection time, so a table rename
moves the test in the same edit; tolerates a `.py` suffix and `·`/`|`/`/`
separators; records the rename mapping (`write.py`->`write`,
`dispatch/workflow`->(dispatch|workflow), `rotate/spawn`->(rotate|spawn)).

```
$ python3 -m pytest extensions/agi/tests/test_cold_seat_brief_five_routes.py -q
5 passed in 5.06s
```

The negative case is a real assertion, not a comment: a line with `send`
removed yields missing `[{send}]`; a line with `rotate/spawn` removed yields
`[{rotate, spawn}]` -- the checker can fail.

### 4. Rename recorded (artifact spelling -> contract name)

```
write.py         -> write
dispatch/workflow -> dispatch | workflow   (ONE router, goal:g1.14)
rotate/spawn     -> rotate | spawn
```

### 5. Residue (no doc edit -- Belam owns those files)

`doc:belam-grok-internals.md` (Prime PROFILE, same `grok-internals-sync`
path) carries **no** route enumeration. Left exactly as found; both that doc
and `doc:director-grok-internals` declare "Belam edits THIS (+ standing) via
write.py ONLY". Pinned as a known-gap test, never silently green.
Follow-up (push_further): Belam adds the five-route fence to the Prime
PROFILE, then move GAP into ENFORCED.

## Evidence

- `production_lines: 0` (no production path touched; test file excluded).
- `git diff --numstat -- extensions/agi/bin extensions/agi/src skills src` -> empty.
- Untracked, exactly two files: the scaffold node + the test file.
- `profile_sync.py --all` -> `0 linked, 0 not ok` (brief artifacts are node
  files read directly, not profile projections).
