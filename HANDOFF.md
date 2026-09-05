# SESSION HANDOFF — 2026-09-05: L1.13 director session (engine work, no waves)

Standing bootstrap lives in [QUICKSTART.md](QUICKSTART.md). This file is one
session only and the next director replaces it wholesale. Prior sessions are in
the grid: `grid.py payload build:HANDOFF.md --version N` (v57 is L1.08–L1.12).

**Closed loops are recorded in [COMPLETE.md](COMPLETE.md)** (`goal:g1.13`),
which follows the **same rule as this file: replaced whole by default, appended
only when the owner asks.** It currently holds two sections because the owner
asked — this session continues directly off loop L1. Read it for what L1 did and
did not close; this file is only the bridge to the next session.

## §0 State block

| | value |
|---|---|
| active nodes / deprecated | **1108** / 181 |
| goals | 124 (16 active, 1 newly active: `s35`) |
| `outcome_coverage` (primary) | 0.190 |
| tests | **1493** via `commands.py run tests` |
| broken links | 0 (1286 resolved) |
| goals round trip | byte-identical |
| unpushed | 0 |
| agents live | none — no dispatch this session |

**Crons are still OFF.** Push by hand: `git -C /home/ubuntu/work/agi push origin master`

## §1 What this session did

No waves, no kids, no provider spend — the owner drove directly.

- [x] **Reviewed loop L1** against the handoff and wrote the first
      `COMPLETE.md` (`goal:g1.13`), including the finding that **zero goals
      closed** in L1 and that `goal:g4.6` was marked `complete` two days before
      its adapter existed.
- [x] **`goal:g9.4` split.** The live view shipped as a list, not a web. Back to
      `horizon`, umbrella over `g9.8` (hook layer, player avatar, LOD),
      `g9.9` (spider skin), `g9.10` (space skin).
- [x] **Minted `horizon`:** `g1.12` (loop-flavor tags), `g5.2` (mechanical goal
      splitting), `g14` (local-maxxing), `g2.12` (the FEELING block).
- [x] **`[goal].md` widened** — a goal may name the build node that produced it.
      Ingest preserves it; one test, verified red.
- [x] **`[build].md` widened twice** — `location:` (a payload's base is a NAME,
      not a path) and two parent shapes so the goal that motivated a version can
      join the lineage. Bare `[goal]` stays forbidden (`goal:s29`).
- [x] **`write.py` gained payload verbs** (`goal:g13.1`): `payload <path>`,
      `payload_text <inline>`, `payload -` (stdin). Editing the file behind a
      build node is finally a named operation. 10 tests, verified red.
- [x] **Fixed in-loop:** `g4.9`, `s33`, `s34` were schema-invalid since L1.12.
- [ ] **`goal:s35` — schemas are nodes. NOT STARTED.** Minted `active` with the
      full plan. This is the next piece of work.

## §2 🔴 Where it stops, and the next command

Everything is committed, grid-versioned and pushed; working tree clean.

```bash
cd /home/ubuntu/work/agi
git status --short                                    # expect empty
bash extensions/agi/driver.sh --smoke --max-iters 1    # 1108 active, must NOT drop
python3 extensions/agi/bin/commands.py run tests       # 1493
```

Then **`goal:s35`**, in the order the goal node states — it is written out step
by step there and the ordering is the whole safety of it:

1. Write `[schema].md` (the meta-schema).
2. Add node frontmatter to all 17 schema files **in place, under
   `context/schemas/`** — `mint_id` via `backfill-mint-ids.py`, never by hand.
3. Teach `schema_registry` both locations, nodes-first.
4. Move to `.agi/nodes/schema/`. `active_node_count` rises by 17; a drop is
   never legal.
5. Verify, then drop the fallback in a **later** commit.

Rehearse before the real cut — `goal:g11`'s migration was rehearsed four times
against exactly this invariant.

## §3 Traps hit this session

1. **No prose verb can contain `&&`.** `parse_script` splits on it, so `note`,
   `thought` and `payload_text` all break on it — found when a `thought` whose
   text was *about* the `&&` split failed to parse. `payload -` (stdin) escapes
   it for bytes; `note` and `thought` have no escape yet.
2. **Payload writes are whole-file only.** No anchored or partial edit, so a
   one-line change to a large module still means emitting the whole file. Real
   engine surgery is therefore still ordinary tools **plus a `thought`
   afterwards**. Marked 🔴 in `SKILL.md`; a hole in `goal:g13.1`.
3. **Two engine modules had no build node at all** — `write.py` (the write path
   itself) and `links.py`. Both found by trying to record a thought and getting
   "no node file". Nothing checks that every tracked source file has a node.
4. **`write.py create --payload` stamps `link_ref`, not `payload_ref`.** Same
   bug an L1.12 kid hit. Set `payload_ref` by hand after creating, or it reads
   as a link rather than the file the node *is*.
5. **`snapshot-goals.py --render --check` fails after any node edit** until
   `--render` (or a smoke run) has rewritten `GOALS.md`. That is the check
   working, not a break.

## §4 Known-good verification sequence

```bash
bash extensions/agi/driver.sh --smoke --max-iters 1 && echo SMOKE_OK
python3 extensions/agi/bin/commands.py run tests          # 1493
python3 extensions/agi/bin/snapshot-goals.py --render --check
python3 extensions/agi/bin/links.py links                 # 0 broken
python3 extensions/agi/bin/links.py schema                # no `goal` row
python3 extensions/agi/bin/grid.py commit --all
git push origin master
```

## §5 BANKED for the owner

1. **`goal:s35` execution** — decided, planned, not run. It touches
   `schema_registry` resolution, which every spawn depends on. Options: run it
   here with the rehearsal, or dispatch parents at it once OpenRouter is live
   again. **Recommend running it directly with the rehearsal**, because the
   failure mode is silent (a schema that resolves nowhere falls through to the
   generic schema and every gate quietly stops checking).
2. **19 parentless build nodes**, including `build:bin-node-writer`,
   `build:bin-locations` and `build:CLAUDE.md`. They cannot take a goal parent
   without the bare `[goal]` shape `goal:s29` forbids, so they are linked from
   the goal's `seeds:` instead. Fixing them properly means giving each a real
   mvp or census parent — work with an owner, not a field to backfill.
3. **`goal:g2.12` (the FEELING block) is specified but unimplemented.** No
   writer emits it, nothing carries it across a regenerating scan yet. It is
   `horizon` on purpose; say the word to make it live.
4. **Carried from L1 and still open:** the OpenRouter workspace weekly budget
   (`$50/week` on `agi`, `$10` on `default`) and whether to restore the six
   demoted prior-director experiments. Recommendation on the latter is
   unchanged: leave them demoted.

## §6 Standing hazards carried forward

- **`snapshot-build-site.py` deletes every `origin: build-site` node it does not
  re-derive.** Moot here (no kits), live for any project that keeps them.
- **A guard that has never failed on purpose is not a guard.** Every test added
  this session was verified red with its change stashed.
- **Run the suite AFTER the last edit**, and **through `commands.py run tests`**
  — direct `pytest` stayed green once while the runner's loader was broken.
- **Node bodies go through `write.py`; payload bytes go through its payload
  verbs; the node behind a payload owes a `thought`.** The whole rule is now in
  `SKILL.md` rather than only in `CLAUDE.md` and this file.
- **`pgrep -af "cli.js"` does not find pi** — the process is named `pi`.
- **A parent's REPORT is not its artefact.** Check the node file on disk.
