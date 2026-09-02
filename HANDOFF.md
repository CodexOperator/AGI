# SESSION HANDOFF — 2026-09-02: LIVE SCRATCHPAD (session in progress)

Standing bootstrap lives in [QUICKSTART.md](QUICKSTART.md). This file is one
session only and the next director replaces it wholesale.

## §0 State block

| | |
|---|---|
| baseline taken | 2026-09-02, `driver.sh --smoke --max-iters 1` |
| nodes | 876 total = 869 active + 7 deprecated |
| primary | `outcome_coverage` = **0.277** |
| evidence_fraction | 0.225 (25 / 111 asserting) |
| decisive_evidence_fraction | 0.95 · unevidenced decisive = **1** |
| thought_coverage | 0.082 (72 nodes) |
| goals | 10 active · 61 horizon · 33 complete · 2 retired |
| unattributed_nodes | 591 |
| unpushed | 0 |
| runtime | **pi** — `spawn.harness: pi`, deepseek-v4-flash kids under qwen3.8-27b parents |
| director | this chat. Parents are subagents; the director reviews deltas, not every node. |
| budget | owner-set: **max 10 iterations, max 8 kids per iteration**. Use cheap tokens liberally. |

## §1 The plan — 10 iterations in three phases

Owner's ordering decision, taken 2026-09-02: **honour `goal:g13`'s own scope
note** ("not until parent and kid tiers are both properly standing") rather
than override it. The tier plumbing is *also* next session's prerequisite, so
phase A is not a detour — it is the same work, paid once.

### Phase A — the tiers actually stand (iters 1–2)

- [ ] **iter-1 — `goal:s28` closed for real, with a test behind it.** `NEXT`
      The manifest merge shipped in `b8cb2ec05` and
      `grep -c manifest extensions/agi/tests/test_dispatch.py` returns **0**.
      s28's falsifier (spawn parent → 2 kids → assert 3 agents with
      `tier: parent` intact; then `post_wire` admits the parent via
      `owns_all_complete`) is unexecuted. Also `goal:g4.8` item 3:
      `spawn.parallel` does not bound grandchildren.
- [ ] **iter-2 — `goal:g4.7` + `goal:g4.1`.** Healing for every harness;
      measure worktree-per-kid against ownership-in-the-brief. Direct prep for
      the worktree/parallel-loops session that follows this one.

### Phase B — `goal:g13`, one read/write path (iters 3–5)

- [ ] **iter-3 — exploratory, wide.** Chains on g13's three open questions.
      **These are BANKED for the owner, not decided by the director** (see §6).
- [ ] **iter-4 — `read.py`.** One parse, one failure semantics. Today's defect
      is not divergent parsing, it is divergent *failure*: malformed input
      raises / skips / returns `{}` / returns `None` / vanishes, depending
      which of the readers you reached. None of those was chosen.
- [ ] **iter-5 — `render.py` + `write.py`.** Route existing callers through
      the one door. `node_writer.write_node` is the write half's starting point.

### Phase C — the viewport (iters 6–8)

Owner picked **three axes**, not four. Chain-walk was explicitly not selected.

- [ ] **iter-6 — space.** Pan/zoom a viewport across a graph bigger than the
      screen. `--level 1..5`, the same axis as everywhere else.
- [ ] **iter-7 — time.** Step through iterations and grid versions; scrub
      backward and watch the graph change.
- [ ] **iter-8 — live.** Agents as spiders on the web, where they are actually
      working, refreshing during a run.

### Phase D — reserve (iters 9–10)

- [ ] **iter-9** — whatever phases A–C surfaced. Held deliberately empty.
- [ ] **iter-10** — goal sweep, metric delta, and the handoff that hands the
      worktree + parallel-parent-loops session its starting line.

## §2 What landed

_(nothing yet — session just started)_

## §3 🔴 Where it stopped, and the exact next command

Baseline is taken and the plan is fixed. Nothing dispatched yet.

```bash
cd /home/ubuntu/work/agi && python3 extensions/agi/bin/dispatch.py agi 1 --tier parent
```

## §4 Traps hit this session

_(none yet)_

## §5 Known-good verification sequence

```bash
bash extensions/agi/driver.sh --smoke --max-iters 1     # node count must NOT drop from 876
python3 -m pytest extensions/agi/tests/ -q
python3 extensions/agi/bin/grid.py commit --all
```

## §6 🔵 BANKED for the owner — do not decide these without them

The owner granted director authority for calls "small enough that they aren't
too structurally foundational" and asked that the big ones be banked for the
morning. These are the big ones. All three are `goal:g13`'s own open questions,
and each is a place where a decision this project already paid for collides
with the new shape:

1. **Where does `THOUGHT` live** once a node body is a marker rather than
   data? It is authored and durable; frontmatter is ruled out already, because
   `write_frontmatter` flattens newlines and would destroy it silently.
2. **What is a goal node's linked file?** `goal:g6.9` established that
   `GOALS.md` renders *from* goal node bodies. A live-linked body points the
   arrow the other way. One of the two has to give, and G6.9 was paid for.
3. **What does a link to a missing file do?** A deprecated node whose file is
   gone must not fail quietly — that is exactly the divergent-failure-semantics
   defect g13 was written about, reappearing inside its own fix.

Iteration 3 exists to build the *argument* on each — chains, not conclusions —
so the owner reads options with evidence rather than a director's guess.

**New invariant to mint, not yet in any goal:** the human viewport and the LLM
injection view are the **same render**. The owner's words: *"the same view as
you'd want to present to an LLM, so we can iterate on it as I use it."* That
fuses `goal:g9.4` with `goal:g13`'s read path and it is the reason the viewport
comes after the unification rather than beside it.
