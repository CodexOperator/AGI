---
id: goal:g7.27
mint_id: 16851767a106428e9fbd3c38873c3558
type: goal
parents:
  - goal:g7
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.27
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: d584c8888a19d9cf
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
  - harness
  - template
  - spawn
thought_session: texas-two-step-belam-voice-2026-09-20
title: "G7.27: Templates are the sole harness arg builders"
town: core
---
# goal:g7.27

## Why this exists

**Parent `goal:g7` (Sanctuary / seat lineage).** Today argv construction is scattered: `rotate.py` has `_KNOWN_HARNESSES` + `_build_claude_command` / `_build_copilot_command` / `_build_harness_command`, `dispatch.py` calls per-adapter `build_command`, and each adapter embeds its own flag dance (Claude's `--append-system-prompt-file` + tools + `--` closing turn; pi's trajectory wrapper; copilot's `--allow-all --remote`). Adding Grok Bot (or any fourth seat harness) forces special-casing in rotate even when the dispatch adapter already exists.

Owner ask 2026-09-19 (voice): templates become the **sole** arg builders.

## Target end-state

- Every harness's invocation logic (flags, brief assembly spelling, env exports that belong to the harness, closing line) lives in a **post/harness template**, not inline in `rotate.py`, `dispatch.py`, or thick adapter bodies.
- The adapter's `build_command` either **becomes the template renderer** or is **retired in favor of it** — one seam.
- Templates are rich enough to express peer flag dances (e.g. Claude's `--append-system-prompt-file` + tools + closing turn) **without becoming mini-programs**.
- If the template format cannot capture something, keep a **thin adapter hook** rather than overloading the template.

## Invariants

- No harness argv builder remains in `rotate.py`.
- `dispatch.py` does not grow harness string branches; it resolves a template (or thin hook) the same way for every harness.
- Peer behavior (pi / claude-code / copilot-cli) stays byte-measurable after the move — no silent flag loss.

## Falsifier

1. For each of `pi`, `claude-code`, `copilot-cli`: spawn dry-run argv is produced only from the template (+ optional thin hook), with **zero** hits for that harness's flag construction inside `rotate.py`.
2. A new harness can add a template (+ optional thin hook) without editing `rotate.py` allowlists or `_build_*_command`.
3. Something the format cannot express is isolated behind a named thin hook, not a template "scripting" escape hatch.

## Out of scope

- Persistent seat watch/restart (`goal:g7.28`).
- Deleting rotate's orchestration / pane layout (`goal:g7.29` consumes this).
- Landing grok-bot on main (`goal:g7.30` consumes the grok post template from this).

## Agent Notes

Assigned to **director-helper**. Point director-belam stays on current batch — do not reassign or interrupt.
Owner voice 2026-09-19: templates sole arg builders; thin hook only when format cannot capture.

Owner 2026-09-20 voice: assigned to director-helper. Split into sub-goals as you see fit — reasonable and doable. Spawn parallel pi parents for those sub-goals (spawn.parallel=1 per command; soft ≤7 live via separate dispatches). Continue from harness-template land already on MAIN.
