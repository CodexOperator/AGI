---
id: goal:g15.14
mint_id: 05df8a9e13594989881d1f1ed121cc70
type: goal
parents:
  - goal:g15
  - build:bin-rotate
next_edges: []
confidence: 0.6
edited_by: sensei-director
goal_id: G15.14
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 73137edbf9e5e688
season: 2
seeds:
  - hypothesis:l4-rotate-self-drives-the-handoff-and-prepares-the-spawn
  - hypothesis:l4-the-window-reply-and-harvest-or-cut-are-captive-steps
status: active
tags:
  - goal
  - subgoal
  - l4
  - sanctuary-director
thought_session: sensei-director-genI-L1
title: "G15.14: rotate.py prompts the LLM through the parts that need its judgement and performs the rest — driven handoff writer, rotate-self --prepare, captive window reply, captive harvest-or-cut"
town: core
---
<!-- BODY:BEGIN -->
**`rotate.py` PROMPTS the LLM through the parts that need its judgement and PERFORMS the rest: a driven handoff writer, a captive `rotate-self --prepare` checklist, a captive merge-up window reply, the point's captive harvest-or-cut.** Owner, 2026-09-11 15:5xZ, verbatim in `doc:l4-owner-decisions`: "propose any additional captive or driven steps the rotate.py script needs so that LLM's are properly prompted through parts needing their input, not just write and read things raw". Design rule (Sensei §2): wherever an LLM's judgement is genuinely needed, the script prints the exact bounded question with every measurable value pre-filled; wherever it is not, the script performs the step. Never remove a decision from the LLM — only the raw reads and writes around it. Today the only captive step is the ack (`continue|diff`).

## Why this exists

- `goal:g15` is the parent because every candidate is an optimization of the rotate-out / wake cost measured in tool calls, fixed in-loop under the perpetual goal; the Sensei's three held drafts (sanctuary-director 135144Z, sanctuary-helper 152548Z, belam 140328Z) are the pre-fix measurement each step is scored against.
- `build:bin-rotate` is the parent because `rotate-self` is the mechanism that already performs the mechanical half — `_write_handoff` writes only a 5-line header to `<sessions>/seats/<S>.handoff.md` while the LLM's card lives in `<sessions>/quorum/<S>.md` and is written raw; `rotate-self` refuses a blocked spawn only after the LLM has spent the calls discovering each blocker; the ack is the one captive reply the file has. The four steps extend that file's own template machinery (`config:rotations` `templates.<role>`), not a new tool.

## The four steps (each a hypothesis brief; parallel where file scopes are disjoint)

1. **Driven handoff writer** — `rotate.py handoff --driven --seat S`: §0 pre-filled from `verification.py` (counts, last suite numbers), the latest rotation record (gen, window @id, pid, model_confirm), the account (`provisioning.py status`), branch + behind-count + unpushed; the LLM is asked ONLY for §3 where-it-stops and §6 banked as bounded fields (a printed prompt; the answer read from a file/argv); the trim guard runs inside; the target is the seat's quorum card, the header file stays.
2. **`rotate-self --prepare`** — the captive rotate-out checklist printed BEFORE any spawn: unpushed commits, dirty tree, behind `season/s2`, card older than the last commit, missing/stale meter pin, stale `.ack.json` — each with the one command that clears it; exit 0 only when nothing blocks; `rotate-self` runs the same checks and refuses by name.
3. **Captive merge-up window reply** — one command in the tool that owns the lock and the baseline (`verification.py` or `rotate.py`; no new `bin/` file) prints lock state + tip + baseline in the shape the Prime replies with, replacing the three by-hand reads.
4. **The point's captive harvest-or-cut** — the successor's first decision beyond the ack: per open round the harvest table pre-filled (L4.236) and a bounded prompt `harvest <round> | cut <next>` per row.

## Testable claim

Each step names, BEFORE its code, the calls it removes in the three held rotations (the pre-fix count is the evidence line); lands as a subcommand or flag of an existing tool with a red-first test; leaves every decision named above with the LLM; `test_rotate_startup.py` + `test_rotate_templates.py` + `test_rotate.py` neighbours stay green. **Falsifier:** a step that decides for the LLM (writes §3/§6, chooses harvest-or-cut, acks) — that step is refused, not landed. **FILE SCOPE:** `extensions/agi/bin/rotate.py` (handoff / prepare regions), `extensions/agi/bin/verification.py` (window reply only), `extensions/agi/bin/season.py` (harvest-or-cut only) + tests. EXCLUDED: `config:rotations`, `config:seats`, the hooks, `send.py`. **CEILING:** 2 parents (steps 1+2; steps 3+4), up to 2 kids each. Shares the `rotate.py` lane with the point's queue — parents cut from this seat's branch, conflicts resolved at merge-up.

## Agent Notes
SL2.01 (sensei-director L2, Sensei 17:29Z floor-cutter 3): fix-only brief hypothesis:l4-the-driven-handoff-writer-keys-on-declared-titles-and-writes-the-seats-own-card — the SL1.02 writer keys on § numerals (the Prime layout) and writes MAIN's card; on this seat's card it would overwrite identity/never-touch/traps and drop the Open-asks table. Floor-cutters 1 and 2 (ack from the row's session_id; address in the alert) are SL1.06, harvested at 9460b63ea.

SL1.04 HARVESTED (sensei-director L2): steps 3+4 landed — verification.py window --grant <seat> (the captive merge-up reply: lock / tip vs MAIN HEAD / stamped baseline, from real files, identical from MAIN or a worktree) and rotate.py first-decision --seat S (one pre-filled harvest row per open round the seat's manifests own + ONE bounded prompt harvest|cut|hold; --answers replays into the named command, never runs). Five kids: the parent demoted its own kid 3 to DISPROVED (ancestry discriminator showed 0 rows after any seat merge) and cut kid 4 for the manifest join — exploration as designed. Live-probed on this seat. RESIDUE: a round with no commit yet (SL1.08, SL2.01 at probe time) is not a row — correct for a first decision, but a stuck parent with nothing committed stays invisible to it; the window subcommand prints, the Prime still has to SEND it (the captive reply is one command away for the Prime's pane, not automatic).

SL2.01 HARVESTED (sensei-director L2, one kid proved 0.85): the driven writer now keys on declared titles (STATE / where it stops / BANKED), rebuilds only the state table and the stops fence, and writes the seat's OWN card (_own_card_path shared with prepare). Live dry-run on the sensei-director card: nine headers byte-identical, §5 table rebuilt from measured values. RESIDUE: node counts read n/a from a worktree (verify-count.json lives in MAIN's shared state — the same seam SL1.04 kid 5 closed for the window subcommand; one-line fix); the composed state table names the Prime-shaped rows (record/counts/tree/meter/account), not this card's (seat/suite/graph/spend/unpushed/wake) — acceptable, the director trims after the driven pass.
