# sanctuary-director — gen VI slice (LIVE, 2026-09-09)

**Seat:** `agi-fa [c6e62f]`, tmux `agi-rc:@231`. Pin `.agi/sessions/sanctuary-director.meter`.
**Correspondent: XVI = `agi-05 [eb30d2]` @230**, re-confirmed by XVI itself this session.
Gen V (`agi-cc [f9472e]` @229) was wiped by PID on the owner's generation-wipe order.
🔴 Survival mode: prime + me only. Wake no seat. L3 takes no new work.

| | |
|---|---|
| Meter | **0.1478** of 0.35 at last read |
| Suite | **2256 passed, 1 skipped** — measured at claim, inherited green |
| Graph | node_count 1780 · active 1586 · deprecated 194 |
| Branch | `season/s2`, clean at claim, `03da1b9ba`, nothing unpushed |
| Key | $7.87 of $15 · account $12.7887 of $92 at first dispatch |
| Live | SD.17 parent `a00-814a8dd9` (pid 1192923) + kid `a00-063eca6a`; SD.18 parent (wrapper pid 1368018) |

## Round: SD.17 (item 49 remainder) + SD.18 (L3 COMPLETE.md DRAFT), both from XVI

Both briefs are **gated into their target nodes** (verified in the bytes, not the
`updated:` line): SD.17 -> `hypothesis:l3-engine-files-outside-the-grid`,
SD.18 -> `mvp:complete-md-the-post-loop-completion-report`.

## 🔴 Findings this session — measured, and each one changed the work

1. **`dispatch.py --prompt-file` is SILENTLY DROPPED for `--tier parent`.** It is
   the *kid* channel (SD.12). Proved on the real composer, not the dry-run:
   `brief.assemble(tier='parent', addendum=MARKER)` -> **0** occurrences;
   `tier='kid'` -> **1**. A parent dispatched with `--prompt-file` gets a brief
   that never mentions it, and the flag reports nothing wrong.
   **Route parent-round terms through the TARGET NODE's note instead** — that is
   what I did for both rounds. **Banked to L4** (fixing it is new work).
2. **The dry-run display TRUNCATES the brief** (`...<N chars>`). My first gate read
   0 occurrences of my own text and I nearly banked a false finding off it. Trap
   0ah one level up: *the dry-run is a report, not the bytes.* Verify against
   `brief.assemble`, never against the dry-run render.
3. **`grid.py` is LOCATION-BLIND, so `location: graph_root` silently breaks grid
   readback.** `resolve_payload` computes `engine_root / payload_ref` and never
   consults `locations.payload_base`. Measured both shapes for `.agi/config.json`:
   `graph_root`+`config.json` -> write.py resolves, **grid.py returns None**
   (acceptance test would fail); `source_root`+`.agi/config.json` -> both agree.
   All 10 nodes carrying `location:` use `source_root` (8) or `repo_root` (2);
   **none uses `graph_root`.** XVI's order said graph_root; I deviated to
   source_root with the measurement in the brief. **Banked to L4.**
4. **Trap 2 confirmed in code:** `write.py create --payload` stamps
   `links.LINK_FIELD == "link_ref"`, but `grid.py` and `grid_coverage_check.py`
   read **only `payload_ref`**. A node minted with `--payload` alone is invisible
   to the grid. Working precedent to copy: `build:drafting.json` carries **both**
   fields plus `location: source_root`, and `grid.py payload` returns its bytes.
5. **`COMPLETE.md`'s L2 section is NOT L3's start state.** It reports tests 1629 at
   L2's close; L2 then ran L2.12 (1650) and L2.13 (**1661**). True boundary:
   L2 last `fed533924`, L3 first `000cc83f3`.
6. **Iteration dirs are not a round ledger.** `iter-SD.12`/`iter-SD.13` do not exist
   though both rounds ran; `iter-SD.09/10/11/18` exist and are empty.
7. **Node counting method matters.** `git ls-tree` path-count gives HEAD 1591/189;
   the engine's smoke gives 1586/194 — deprecation is a frontmatter `status:`, not
   only a directory. Both ends of a delta must use one method.

## 🔴 Next action if I die here

Both parents are `--branch`. Harvest each: **`git -C <worktree> status --porcelain`
BEFORE believing a branch empty** (staged-with-zero-commits is the recorded shape),
then merge-base diff (`git diff $(git merge-base season/s2 <br>)..<br>`), full
verify sequence, merge, `grid.py commit --all`, push, report the balance delta to
XVI. Worktree/branch come from `.agi/sessions/iter-SD.NN/manifest.json`, not from
`agent.json` or the released lease (trap 0n).
