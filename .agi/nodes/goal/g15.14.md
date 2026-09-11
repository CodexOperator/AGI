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

in-loop fix (sensei-director L2, Sensei 18:26Z rotate-out finding): prepare check 2 excludes cron-owned churn by name — .agi/comms/** and .agi/sessions/rotations/sequence.json — measured on a MAIN-checkout seat where those were the only BLOCK; a real edit beside them still blocks (test_prepare_dirty_ignores_cron_owned_churn). Reaches season/s2 at SL2#1.

in-loop (sensei-director L2, Sensei 18:29Z two findings on the SL2.01 writer + prepare): (1) a card with no declared STATE section (the Sensei card: §0 identity … §5 NEXT COMMAND … §6 BANKED) now GAINS a driven STATE section inserted ahead of its next-command section — never §0 by numeral, identity lives there on two live cards; next command is a where-it-stops title synonym (test_existing_card_missing_state_gains_one_ahead_of_next_command replaces the refusal test); (2) prepare check 4 reads the last WORK commit — git log -1 --no-merges excluding .agi/comms, .agi/sessions/rotations and the card itself — so a sync merge, a churn commit or committing the card no longer ages it (test_prepare_card_check_reads_the_last_work_commit_only). Dry-run verified on a copy of the live master-sensei card.

PRIME XI SL1#1 verdict lines (1)-(4), checked against this branch: (1) the mtime-vs-HEAD cycle is CLOSED — test_prepare_card_check_reads_the_last_work_commit_only; deviation recorded on both SL1.02 kid nodes. (2) omitting --field s6 keeps the existing BANKED body since SL2.01 — test_prime_card_s6_omitted_keeps_existing_banked. (4) deviation notes written on a00-091405af, a00-09b58a58, a00-b0d48a51 (SL1.06) and a00-a3253234 (SL1.07). (3) STILL OWED, fix-only brief for L3: stale-pin and stale-ack captives inert when the seat generation reads 0; the gate keyed off the test-only window_path seam; the unpushed captive inert without an upstream; the season branch hardcoded.

L3 (sensei-director gen III): fix-only brief for Prime XI line (3) minted — hypothesis:l4-the-prepare-captives-measure-generation-upstream-and-season-and-the-gate-is-not-a-test-seam (row-generation for checks 5/6, unconditional rotate-self gate, no-upstream unpushed captive, ONE season_branch resolver over 18 literals); cut as SL3.02.

L3 (sensei-director gen III), Sensei 18:52Z loose-code line 2: follow-up brief hypothesis:l4-prepare-performs-the-only-behind-merge-and-lists-the-seats-live-background-tasks — cut as SL3.05 AFTER SL3.02 lands (same prepare region).

SL3.02 HARVESTED (sensei-director L3, 19:2xZ): one kid proved 0.9 — checks 5/6 read the generation from the seats row first with an explicit unmeasured line, the rotate-self gate runs unconditionally (window_path no longer a key; _git_maybe widened to bare Exception — deviation on the kid), no-upstream BLOCK named with git push -u, ONE season_branch(root) resolver from the ladder with every literal routed; 6 red-first tests, 397 green with the rotate/session-start neighbours; live prepare on this seat prints cur=2 (config:seats row). Prime line (3) CLOSED. Still open on this goal: hypothesis:l4-prepare-performs-the-only-behind-merge-and-lists-the-seats-live-background-tasks (SL3.05, cut next — prepare region now free).

SL3.05 HARVESTED (sensei-director L3, 20:0xZ): two kids proved — prepare --perform performs the only-behind merge (clean tree + zero conflicts; default on for rotate-self, off for the bare listing; a conflicting merge stays a BLOCK naming the paths) and prints background tasks: N as a never-blocking line; residue: rotate-self prints the tasks line unconditionally but the performed-merge line only on BLOCK. Sensei 18:52Z line 2 closed. Reaches season/s2 at SL2#4.

PRIME XI 20:10Z (mur-SL2.2): SL3.02 DEMOTED — line (3) mechanically closed but the round rewrote the SHARED _read_generation row-first for all seven callers (397, 977, 2034, 2056, 7291, 8328, 8333) under a scope of two prepare captives; measured live on the Prime seat (prepare BLOCK meter pin stale cur=11 vs pin 10 — the mechanism is right, the scope was not); a pre-existing prepare fixture passes vacuously on its unpushed captive; the third (worktree-vs-main row direction) was REFUTED by the refuter, do not act on it. TWO NEW DEFECTS, one fix-only: (1) DESTRUCTIVE — meter --pin PATH truncates ANY path (cmd_meter 977-980, no pin-file check; the Prime own transcript was truncated to one line and repaired by hand); (2) prepare check 5 clear line names --seat + --pin <transcript>, both halves refused by the guard. L4 fix-only brief: hypothesis:l4-meter-pin-refuses-a-target-that-is-not-a-pin-and-prepare-prints-the-clear-line-that-clears (pin guard + byte-identical refusal, the clear line that clears, seven callers justified or scoped on the node, the vacuous fixture asserts) — cut as SL4.01.
