# SESSION HANDOFF — 2026-09-02: LIVE SCRATCHPAD (session in progress)

Standing bootstrap lives in [QUICKSTART.md](QUICKSTART.md). This file is one
session only and the next director replaces it wholesale.

## §0 State block

| | baseline (session start) | now |
|---|---|---|
| active nodes | 869 | **887** |
| deprecated | 7 | 7 |
| `outcome_coverage` (primary) | 0.277 | 0.270 |
| `evidence_fraction` | 0.225 | **0.235** |
| `decisive_evidence_fraction` | 0.95 | 0.905 |
| unevidenced decisive | 1 | 1 |
| goals active / horizon / complete | 10 / 61 / 33 | 10 / 61 / 34 |
| tests | 1221 | **1250** |
| unpushed | 0 | 0 (cron pushes) |

**Runtime:** pi — deepseek-v4-flash kids under qwen3.8-27b parents, per the
owner's instruction to use cheap tokens liberally. **Budget:** max 10
iterations, max 8 kids per iteration. Six iterations used (101–106).

**`outcome_coverage` dipped 0.277 → 0.270 and that is expected, not a
regression.** It is mvps per hypothesis; this session minted hypotheses and
verdicts without minting mvps, so the denominator grew. `evidence_fraction` —
the metric that only moves when experiments actually run — went **up**.

## §1 The plan, and where it got to

Owner's ordering call: **honour `goal:g13`'s own scope note** (do not touch the
read/write path until the parent and kid tiers stand) rather than override it.
Phase A was not a detour — it is also the prerequisite for the next session.

### Phase A — the tiers stand ✅

- [x] **iter-101** — `goal:s28` closed. Manifest race found and fixed.
- [x] **iter-102** — two concurrent parents, no collision. `g4.1`/`g4.7` opened.

### Phase B — `goal:g13`, one read/write path ◐

- [x] **iter-103** — wide exploration. **`goal:g4.1` measured and settled.**
- [x] **iter-104** — read half: the canonical reader now keeps its contract.
- [ ] **iter-107 (next)** — `write.py`. Not started. See §3.

### Phase C — the viewport ✅ (space + time + live all landed)

- [x] **iter-105** — `bin/viewport.py`. All three axes the owner chose.
- [~] **iter-106** — chains on `g9.4`, `s31`, `g4.8`. In flight at handoff.

### Phase D — reserve

- [ ] **iter-108–110** — held. `g4.8` and `s31` are the obvious candidates.

## §2 What landed

### 🔴 The manifest race — the one that would have broken next session

`goal:s28` was `active` with its fix already shipped in `b8cb2ec05`. That fix
had **zero tests** (`grep -c manifest tests/test_dispatch.py` → `0`), so its
third falsifier clause had never been run. It did not hold.

The `rename` was atomic; the **read-merge-write cycle around it was not**, and
`.manifest.json.tmp` was a *fixed shared name*. Two dispatches overlapping →
one renames the file out from under the other, which dies `FileNotFoundError`
**after `Popen` has already run**. That is a spawned agent nothing tracks:
`heal.py` cannot time it out, `post_wire` cannot wire its node. `goal:g7`
failing at the instant of spawn.

Measured before the fix, 8 concurrent dispatches × 6 runs: **6/6 runs lost
entries, typically 6–7 of 8.** Fixed with `flock` around the whole cycle, a
re-read under that lock, and a unique `mkstemp` name. Six tests carry the
falsifier now.

**Verified live at the exact scale that broke it:** iteration 103 ran 4 parents
+ 4 kids into one manifest — 8 agents, zero lost.

### ✅ `goal:g4.1` settled after sitting open since 2026-08-22

A kid ran 10 trials (5 warm, 5 cold with the page cache dropped between).
**`git worktree add --detach` costs 0.09s warm, 0.80s cold** on this 133MB
repo — 56× and 19× inside the hypothesis bounds. Two kids: **0.19s**, against
the 2–5 minutes one collision costs to diagnose. Chain closed
`goal → hypothesis → experiment → verdict: proved` @0.99, evidence resolving to
a real node, no self-citation. **Worktree-per-kid is not a close call.**

### ✅ `goal:g13` read half — the canonical reader keeps its own contract

Six independent parsers measured, **four different failure semantics**. Two
findings sharper than the goal text:

- **`benchmark.py` never fails and is not YAML.** A hand-rolled
  `partition(":")` loop: returns `parents=''`, `tags=''`, injects a junk
  `'- goal'` key, leaves quotes on `id`. Every list field silently destroyed.
- **`graph_core.persistence.frontmatter` contradicted itself.**
  `FrontmatterError` is documented as *"raised when a node file cannot be
  parsed"*, but malformed YAML leaked `yaml.ParserError` — and malformed JSON
  leaked `json.JSONDecodeError`, which no chain had found because they only
  tested `.md`. **Both wrapped**, `__cause__` preserved and asserted.

### ✅ The viewport — `bin/viewport.py`

`goal:g9.4` built under `goal:g9.7`'s constraint. **One frame stream, two
formatters.** `render_human` and `render_llm` take identical arguments and read
only `Frame` fields, so there is no way to change what a human sees without
changing what a kid is handed.

```bash
python3 extensions/agi/bin/viewport.py                    # interactive
python3 extensions/agi/bin/viewport.py --emit both        # both views, one stream
python3 extensions/agi/bin/viewport.py --verify           # g9.7's falsifier
python3 extensions/agi/bin/viewport.py --live --iter iter-104 --anchor goal:g13 --depth 5
```

Keys: arrows/hjkl pan · `+`/`-` depth · `[`/`]` time · `a` live · `q` quit.

Cross-validates against `metrics.py` on two independent numbers: 1 damaged
node (= `unevidenced_decisive_verdicts`) and 5 nodes under agents in iter-104.

### 🆕 `goal:g9.7` and `goal:s31` minted

- **`g9.7`** — one render, two readers. Your constraint, now a falsifiable goal.
- **`s31`** — a scaffolded node ships schema-invalid. `[hypothesis].md` requires
  `title` + `testable_claim`; `node_writer` seeds neither; the kid is *correctly*
  forbidden from touching frontmatter (it would break `scaffold_hash`, which is
  how completion is detected). **The node cannot become valid by anyone doing
  their job as briefed.** Deliberately not scheduled ahead of `g13`.

## §3 🔴 Where it stopped, and the exact next command

Iteration 106's three parents were in flight when this was written. Read their
reports first:

```bash
for a in .agi/sessions/iter-106/a00-*/; do echo "== $a"; cat "$a/output.log"; done
```

Then the next real work is **`goal:g13`'s write half** — `write.py`. The read
half landed; `node_writer.write_node` is the starting point, and `goal:s31` is
the first thing it should fix.

```bash
python3 extensions/agi/bin/dispatch.py "$PWD" 107 --tier parent --target goal:g13 --level small
```

## §4 Traps hit this session

1. **A fix with no test is an assertion, not a fix.** `b8cb2ec05` claimed
   atomicity in a commit message. Nothing executed it. It was wrong.
2. **`grep` for an expected glyph hides a crash.** The viewport's default view
   crashed on `Graph.node_ids` (a set attribute, not a method) and the smoke
   check passed, because absent output and a traceback look identical to
   `grep`. Check the exit code.
3. **Breadth-first is wrong for a tree view.** It emits every depth-0 node then
   every depth-1 node, so indentation describes a nesting the order
   contradicts. Found by *looking at the output*, not by a test.
4. **Parents hang, and rate limits bite.** Two parents died — one silently past
   its 20-min timeout, one on `Upstream error from Reka: Too many requests`. In
   both cases **the kid's node had already landed** and was reviewable. The
   2026-08-31 field note (check the filesystem before resuming) paid for itself
   twice today. Back off when running >4 concurrent pi agents.
5. **gitnexus reported `g9.4` as `active` when it was `horizon`.** It is a
   semantic search, not an oracle. Confirm with `grep`.

## §5 Known-good verification sequence

```bash
bash extensions/agi/driver.sh --smoke --max-iters 1     # node count must NOT drop from 887
python3 -m pytest extensions/agi/tests/ -q              # 1250 passing
python3 extensions/agi/bin/viewport.py --verify         # goal:g9.7's invariant
python3 extensions/agi/bin/snapshot-goals.py --render --check
python3 extensions/agi/bin/grid.py commit --all
```

## §6 🔵 BANKED for you — decisions I deliberately did not make

**`goal:g13`'s three open questions.** Iteration 103's chain built argument on
these; none is decided. Each is a place where a decision this project already
paid for collides with the "node body is a marker, not data" shape:

1. **Where does `THOUGHT` live** once a body is a marker? Authored, durable,
   and frontmatter is ruled out — `write_frontmatter` flattens newlines and
   would destroy it silently.
2. **What is a goal node's linked file?** `goal:g6.9` made `GOALS.md` render
   *from* goal bodies. A live-linked body points the arrow the other way. One
   of the two has to give, and G6.9 was paid for.
3. **What does a link to a missing file do?** A deprecated node whose file is
   gone must not fail quietly — the exact defect g13 was written about,
   reappearing inside its own fix.

**Two smaller ones, yours because they are yours:**

4. **`goals_active` is 10 against `cc_dispatch.max_goals_active: 9`.** I marked
   `g9.4` active because it is genuinely being worked, rather than silently
   raising your cap. Either raise it to 10 or retire one — `g3`, `g5` and `g7`
   are overarching and arguably permanent residents, which may mean the cap
   should count only subgoals.
5. **Should the viewport replace `INJECTION.md`'s renderer outright?** `g9.7`'s
   falsifier is currently proven *within* `viewport.py`. Making `render-context.py`
   and `zoom.py` call `frame_stream` too is the real prize — it would delete
   4 of the 5 remaining render paths — but it changes what every kid is handed,
   so it should be your call, not one made overnight.

## §7 Next session: worktree branching + parallel parent/kid loops

Everything that session needs is now measured or fixed:

- **Concurrency is safe.** The manifest survives 8 concurrent agents.
- **Worktrees are cheap.** 0.09s warm — the cost objection in `g4.1` is dead.
- **The reaper exists but is half-wired.** A kid built `_reaper_phase` +
  adapter `is_alive`/`restart`; `restart()` is defined and **never called**
  (`dispatch.py`, "reserved for a future iteration"). Its verdict is honestly
  `inconclusive_lean_proved:55` because of exactly that.
- **`goal:g4.8` item 3 is still open:** `spawn.parallel` does not bound
  *grandchildren*. N parents × M kids is an unbounded population against one
  tree. Fix that before running many loops at once, or the worktree win gets
  spent on process explosion.
