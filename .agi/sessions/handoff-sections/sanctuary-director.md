# sanctuary-director — gen VI slice (LIVE, 2026-09-09)

**Seat:** `agi-fa [c6e62f]`, tmux `agi-rc:@231`. Pin `.agi/sessions/sanctuary-director.meter`.
**Correspondent: XVI = `agi-05 [eb30d2]` @230**, re-confirmed by XVI itself this session.
Gen V (`agi-cc [f9472e]` @229) was wiped by PID on the owner's generation-wipe order.
🔴 Survival mode: prime + me only. Wake no seat. L3 takes no new work.

| | |
|---|---|
| Meter | ~0.23 of **0.47** — owner raised the cap 0.35 -> 0.47 (61262b5a2), standing for every role |
| Suite | **2256 passed, 1 skipped** — measured at claim, inherited green |
| Graph | node_count **1784** · active **1590** · deprecated 194 (SD.17 minted 4) |
| Branch | `season/s2`, clean at claim, `03da1b9ba`, nothing unpushed |
| Key | $7.87 of $15 untouched · account **$12.7286**, round burn **$0.0601** |
| Live | **nothing running** — SD.19 harvested and merged |

## Round: SD.17 CLOSED BY HAND · SD.18 NOT DONE, needs re-dispatch

🔴 **BOTH DISPATCHED KIDS MISSED THE ASSIGNMENT, and the cause was my channel choice.**
Each produced a verdict node *about* the work instead of the work: SD.17's kid
re-verified SD.13's already-closed state and declared the hypothesis "fully
satisfied"; SD.18's kid wrote an outcome on the COMPLETE.md contract at lean 75.
Neither node was minted, no L3 section was written. Both parents then exited
after ONE kid (under-iteration trap). Total burn for both failed rounds: **$0.0601**.

**Root cause, and it is reusable:** a brief appended as a `note` at the BOTTOM of a
long node does not dominate the node's own `testable_claim` in frontmatter. The
SD.17 node still asserted SD.13's remainder-is-zero claim, so a kid reading it
concluded "satisfied" — correctly, from what the node said. **My brief was arguing
with the node it was attached to.** Gating on "the bytes are in the node" was not
enough: bytes-in-node is not brief-in-effect. Put the assignment where the agent
reads first, or do not delegate it.

**SD.17 then done by hand** (small, and fully specified by my own measurements —
a third paid attempt through a channel that had failed twice was throwing money).

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

## SD.17 CLOSED (33fc2eff1) — done by hand, proved through the grid

`build:agi-config.json` + `build:briefs-prime-director-successor`, each under an
mvp minted with it (`mvp:graph-config`, `mvp:briefs`) because goal:s29 needs an
mvp parent and neither the graph root nor `extensions/agi/briefs/` had one.
Both carry `link_ref` AND `payload_ref` plus `location: source_root`, copying
`build:drafting.json`. **The close passed:** after `grid.py commit --all`,
`grid.py payload` returns the real bytes for both. `graph_root` would have
returned nothing — the deviation is what made the acceptance test reachable.
Verify at close: pytest 2256/1 unchanged · coverage clean, exclusions untouched ·
links 1764 resolved 0 broken · goals 128 identical · smoke 1780 -> **1784**,
active 1586 -> **1590**, deprecated 194.

**Known, not damage:** `write_guard check` WARNs on both new payloads because the
NODES are new, though the files are byte-identical to HEAD. `check` exits 0,
`--strict` exits 1. Adopting an existing file into the grid trips the strict
guard with no bytes changed. No pre-commit hook installed. Do NOT "fix" it by
running the guard's suggested `write.py <id> payload <path>` — that writes a
file onto itself.

## SD.19 CLOSED — the L3 completion report is in COMPLETE.md, DRAFT

The retry worked: kid `a00-6a1a360e` under parent `a00-72658f67` wrote the L3
section. **78 insertions, 0 deletions** in COMPLETE.md — appended newest-first
between the header block and `## Loop L2`, nothing existing touched. Seven
sections in order, the closed failure-category set used exactly (`none` printed
for `late-minting` rather than dropped), claims carried on commit hashes.
It used the director's measurements instead of re-deriving: the true boundary
`fed533924 -> 000cc83f3`, the L2-report-is-not-the-start-state correction, and
it STATES its counting method per the trap.
**Verified by me, independently: all 24 cited shas resolve** (`git cat-file -e`),
links 1766/0 broken, goals 128 identical, coverage clean, write_guard silent,
smoke 1786 / 1592 / 194.

🔴 **One factual error I caught and fixed in a SEPARATE commit** (so the kid's
work stays attributable): the section credited **`sanctuary-director` as L3's
prime director**. That is this worker seat. L3's prime is **Belam**
(`belam-S1-L3-I..XVI`) — HANDOFF line 1 is the evidence. Fixed via
`write.py build:COMPLETE.md "patch -"`, which is also a third-actor live
adoption proof of the patch verb.

🔴 **A red suite that was NOT mine:** the prime's `61262b5a2` moved the owner's
rotation cap 0.35 -> 0.47 in `ladder:ladder` but left
`test_ladder_node.py:52` asserting 0.35 — 1 failed, 2255 passed. Fixed through
`write.py build:tests-test-ladder-node "patch -"` (assertion + docstring).
**Both stale spots are now FIXED** (`2d89b2af5`, prime handed it back to me):
`rotate.py:75 DEFAULT_DIRECTOR_ROTATE_AT` and the `(0.35)` docstring at 2113 are
0.47; no `0.35` remains in the file. The four other occurrences read the
constant. `test_spawn_gate.py`'s two `0.35` values are synthetic fixture ladders,
not the code default — left alone, still passing. Suite run ALONE for it:
**2256 passed, 1 skipped**. The owner's 0.47 order is now applied end to end:
ladder node, successor brief, SKILL.md (prime) + engine default (me).

## 🔴 trap 0ai is WORSE than recorded — escalate it

`nohup` does NOT protect a long run. The harness's low-memory reaper killed a
**nohup'd pytest at 63%** (twice) while `free` showed **18 GB available** of 23.
Gen V recorded it taking a dispatch wrapper; it takes the suite too.
**Run a long verification in the FOREGROUND** (Bash `timeout: 400000`) — that
completed first time, 117.97s. Background is for dispatch, not for verification.
Also reproduced: `pgrep -af "pytest extensions/agi/tests"` matched **the seat's
own session**, whose prompt text contains the string — the item-71 hazard in a
new dress. Never conclude "not running" from a `ps` grep.

## New traps this session

- 🔴 **bytes-in-node is not brief-in-effect** (see above). Put the assignment in
  the node's `testable_claim`, not in a note at the bottom.
- 🔴 **`--prompt-file` is framed as "inherited context, NOT your assignment"** in
  the kid brief. Even where it lands, it cannot carry an assignment.
- 🔴 **dispatch REFUSES a target minted but not committed** — a worktree is cut at
  the last committed tip. **Commit and push the brief BEFORE dispatching at it.**
  Fails closed with an exact fix.
- **0aj** (prime's number): the dispatch dry-run TRUNCATES the brief it prints.

## 🔴 Next action if I die here

Both parents are `--branch`. Harvest each: **`git -C <worktree> status --porcelain`
BEFORE believing a branch empty** (staged-with-zero-commits is the recorded shape),
then merge-base diff (`git diff $(git merge-base season/s2 <br>)..<br>`), full
verify sequence, merge, `grid.py commit --all`, push, report the balance delta to
XVI. Worktree/branch come from `.agi/sessions/iter-SD.NN/manifest.json`, not from
`agent.json` or the released lease (trap 0n).
