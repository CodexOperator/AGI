---
id: exp:noncode-surface-census
mint_id: fa7f62e0dc3547d783675b3adc19ee61
type: experiment
parents:
  - goal:g6.6
confidence: 0.9
edited_by: season.py
evidence_runs: 1
season: 1
subgraph: false
tags:
  - g6.6
  - level3
  - census
thought_session: season
title: "Census: level3.py sees 23% of the engine, 39% after excluding generated noise"
---
**What was run:**

```
# 1. the predicate (level3.py, lines 120-158)
SRC_PREFIX = "extensions/agi/src/"
BIN_PREFIX = "extensions/agi/bin/"
# a tracked file is IN scope iff:
#   f.startswith(SRC_PREFIX) and f.endswith(".py")           (any depth)
#   or (f.startswith(BIN_PREFIX) and f.endswith(".py") and "/" not in f[len(BIN_PREFIX):])  (direct children only)

# 2. covered set (one payload_ref per node, frontmatter written twice per file but unique per path)
ls /home/ubuntu/work/agi-tree/nodes/level3/*.md | wc -l              # -> 74
grep -h 'payload_ref' nodes/level3/*.md | sed 's/payload_ref: //' | sort -u > covered.txt
wc -l covered.txt                                                     # -> 74

# 3. universe
cd /home/ubuntu/work/agi && git ls-files | sort > universe.txt
wc -l universe.txt                                                    # -> 316

# 4. gap
comm -23 universe.txt covered.txt > uncovered.txt
wc -l uncovered.txt                                                   # -> 242

# sanity: every file inside the *declared* scope is covered (no scanner bug)
git ls-files | grep -E '^extensions/agi/(src|bin)/.*\.py$' | sort > scope_declared.txt
comm -23 scope_declared.txt covered.txt                               # -> empty
```

**What happened:**

`level3.py`'s own docstring already says the scope is "~70 files" and out of
scope for shell/TS/prose "for this first pass" — that part of the claim was
right. The numbers:

| | count |
|---|---|
| tracked files in `agi` (universe) | 316 |
| covered (level-3 nodes exist) | 74 |
| uncovered | 242 |
| declared-scope files (`src/**/*.py` + `bin/*.py`) not covered | 0 |

Coverage of the *declared* scope is 74/74 = 100% — the generator does exactly
what it says. The gap is entirely a scope decision, not an execution bug.

Raw coverage (covered / all tracked files): **74/316 = 23.4%**

242 uncovered files include generated/ephemeral artifacts that were never
candidates for a hand-worthy contract node. Exclusion predicate applied,
each bucket justified by what produces it:

| excluded bucket | count | why excluded |
|---|---|---|
| `experiments/*/output.txt` | 96 | per-run benchmark output, regenerated every invocation |
| `sessions/*.jsonl` + `autoresearch.jsonl` | 25 | append-only run/session logs, gitignored in new projects, tracked here as historical scratch |
| `**/__pycache__/*.pyc` | 3 | compiled bytecode cache |
| `.gitnexus_cache.json` | 1 | generated code-graph index cache |
| `pi-agi.log` | 1 | generated log |
| `.gitignore` | 1 | VCS meta, no contract semantics |
| **total excluded** | **127** | |

Eligible set = 316 − 127 = **189**. Eligible coverage: **74/189 = 39.2%**.
Uncovered-but-eligible = 189 − 74 = **115**, broken down:

| category | count | examples |
|---|---|---|
| tests, python (`extensions/agi/tests/**/*.py` + `conftest.py`) | 51 | `test_level3.py`, `test_grid.py`, `conftest.py` |
| prose/markdown (non-test) | 37 | `README.md`, `TODO.md`, `HANDOFF.md`, all of `context/`, `skills/agi/SKILL.md`, `extensions/agi/lib/agent-prompt.md` |
| tests, fixtures (`.md`/`.json` under `tests/fixtures/`) | 13 | `tests/fixtures/schemas/example.md`, `tests/fixtures/nodes/sample.json` |
| shell | 6 | `driver.sh`, `find-root.sh`, `cc-session-start.sh`, `run-loop.sh`, `start.sh`, `autoresearch.sh` |
| JSON/TOML config | 5 | `package.json`, `decompose-engine.goalmap.json`, `autoresearch.config.json`, `embeddings.toml`, `graph-core.toml` |
| TypeScript | 1 | `extensions/agi-bridge/index.ts` |
| SQL | 1 | `schema.sql` |
| other (real script outside declared scan dirs) | 1 | `extensions/agi/scripts/migrate_to_sqlite.py` |
| **total** | **115** | |

Note `decompose-engine.goalmap.json` is not generated — its own header says
"Declared deliberately by a human or a verdict decision" — so it stayed in
the eligible set, not the exclusion list, alongside `package.json` and the
`.toml` templates. `migrate_to_sqlite.py` is real, hand-written engine code
that misses the scan only because `extensions/agi/scripts/` isn't one of the
two scanned prefixes — a second, narrower scope bug distinct from the
non-code-surface gap.

**Named-file check** (all 9 files G6.6 calls out by name, verified against
`covered.txt`): `skills/agi/SKILL.md`, `extensions/agi/lib/agent-prompt.md`,
`extensions/agi/driver.sh`, `extensions/agi/lib/find-root.sh`,
`extensions/agi/hooks/cc-session-start.sh`, `extensions/agi-bridge/index.ts`,
`schema.sql`, `README.md`, `TODO.md` — **9/9 uncovered.** Every file G6.6
uses as evidence checks out.

**Judgement call — agent-prompt.md vs SKILL.md, do kids get contradictory
instructions?** Yes, direct and unambiguous. `extensions/agi/lib/agent-prompt.md`
(the pi kid brief) rule 5: *"**Commit your work.** Before signaling done, run:
`git add -A && git -c user.email=... commit -m "iter-N agent-id: short
summary"`"* and rule 6: *"**Signal completion via CLI.** After your last
commit: `python3 <plugin>/bin/cli.py done <iter_n> <agent_id> --verdict
<state> ...`"*. `skills/agi/SKILL.md`'s "Iteration protocol (parent)" step 3
says the opposite for the same role: *"Kid deltas from the normal rules: **do
not commit**, and do not call `cli.py done` — write the node file, report,
stop."* and its "Kid end-of-job contract" section: *"**No git, no push, no
sync, no cli.py** — spending tokens on those is waste; automation owns all
remote traffic."* One file tells a kid to commit and call `cli.py done`; the
other tells the same role never to touch git or `cli.py`. Neither document
references or defers to the other — there is no runtime-scoping language in
`agent-prompt.md` itself that would resolve this (e.g. this run's own zoom
brief had to add an out-of-band note telling the kid to ignore the
`cli.py done` instruction because "it's for a different runtime" — a patch
applied at dispatch time, not in the source file). This is exactly the
failure mode G6.6 predicts: a file with no node behind it drifted out of
sync with its sibling doc, and nothing short of a human or kid actually
reading both caught it.

**What it means for G6.6:** the evidence supports the claim, doesn't just
gesture at it. Coverage is 23% raw / 39% against a defensible eligible set —
either way, most of the engine's surface has zero graph representation, and
the omitted surface is disproportionately the highest-leverage part: the two
docs that define what every kid is told to do (`SKILL.md`,
`agent-prompt.md`), all three shell entry points, the TS bridge, and the
schema. The agent-prompt/SKILL contradiction is not a hypothetical cost of
being outside the graph — it is a live, currently-uncaught bug of exactly
the kind G6.6 says `stitch.py --verify` should have caught if these files
carried nodes. G6.1 (assembling `agi` from `agi-tree`) cannot be truthful
while 61% of the eligible surface, including the two docs that steer every
kid, has never been stitched. Coverage is not better than G6.6 assumed;
if anything the reflexive case it flags (G1.3/G1.4 touching
`agent-prompt.md` directly) is corroborated by a second, independently
found defect in that same file.