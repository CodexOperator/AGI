---
id: goal:g1
mint_id: 556869f3f6454ffe9118a793e062aa5f
type: goal
confidence: 1.0
edited_by: kid:a00-38101b34
goal_id: G1
goal_kind: perpetual
heading_level: 2
origin: goals-doc
season: 1
seeds:
  - goal:g1.1
  - goal:g1.2
  - goal:g1.3
  - goal:g1.4
  - goal:g1.5
  - goal:g1.6
  - goal:g1.7
  - goal:g1.10
  - idea:engine-cli
  - idea:engine-driver-sh
  - idea:engine-find-root
status: horizon
tags:
  - goal
  - root
thought_session: L3.07
title: "G1: Config-maxxing: every engine action is declared, never improvised"
---
**Renamed 2026-09-02 by the owner, from "Zero-operations loop: every mundane
step is a command".** The invariant did not change; the framing got one level
deeper, and the new name is the one that generalises. Recorded as a rename
rather than a fresh goal because the seeds, the banked results and every
subgoal below still hold verbatim — this project does not renumber, and it
does not edit drift away either.

**The owner's statement of it:**

> Everything is in a config, everything is a node, everything is a unified
> spawn path, everything is a unified read and write path. Every action is
> defined, config-maxxed. Nothing is just created randomly or freely — the
> graph is the creation engine, so each engine action must be as mechanical as
> possible.

**Why the rename is not cosmetic.** "Zero-operations" names a *cost* to be
driven down: the agent should not spend motion tending the machine. That is
true and it stays true, but it is a symptom. **Config-maxxing names the
cause.** An action that is improvised has to be re-derived, re-typed and
re-checked by whoever meets it next; an action that is *declared* is read once
and executed identically forever. Zero operations is what you get when
everything is declared — not a separate target to aim at.

**Invariant, restated at the deeper level:** every engine action is declared in
a node or a config the engine reads. Any repeated, mechanical step is a named
command, and every surviving manual handle carries a written reason.

## The four "everything"s, and where each stands

| | claim | status |
|---|---|---|
| **everything is in a config** | behaviour is declared data the engine reads, never a fork of engine code | partial — `config.json` is the customization surface; `goal:g1.10` extends it to the commands themselves |
| **everything is a node** | including the engine's own geometry: crons, secrets, commands | partial — `.geometry/crons.md` and `secrets.md` exist; commands do not |
| **one spawn path** | a harness is an adapter named in config, not a parallel code path | `goal:g4.6` |
| **one read/write path** | one way in, one way out of the graph | `goal:g13` — read half landed 2026-09-02 |

**`.geometry/crons.md` is the working precedent and the shape to copy.** It is
graph content declaring cron cadences; `crons.py apply` is the one command that
makes reality agree with the declaration; editing the node *is* the change. No
schedule is typed at a shell. That is config-maxxing built and running, on one
narrow surface, and `goal:g1.10` is the argument that the surface should be
wider.

**The counter-example this goal exists to prevent** is the one the repo has
already paid for: a step that is mechanical but undeclared gets done slightly
differently each time, and the differences are invisible until one of them is
wrong. Six node parsers that agree only by accident (`goal:g13`), a manifest
merge asserted in a commit message and nowhere else (`goal:s28`), a scaffold
that omits schema-required fields nobody declared it must supply
(`goal:s31`) — each is an undeclared action drifting.

Already banked — cron owns all remote traffic (H10), embedded maps cut kids from
11-13 tool calls to 5-7 (L7), the DONE contract makes stopping one line.

Owns: **L11** remainder (one command that renders *and* spawns — the parent's
last machine-tending chore), **L12** remainder (a runtime flag rather than a
parallel code path; hook parity audit), **L17** (config schema plus a writer, so
configs stop being hand-written), **L18** action 2 (`agi-tree init` scaffolds a
project), **H6** (`--iter-base N` for `dispatch.py`, so a run stops clobbering
prior session manifests).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
L3 wave 1 (hypothesis:l3w1-goal-kind-perpetual): this goal is perpetual — long-horizon, one director, no active-goal cap.
<!-- THOUGHT:END -->