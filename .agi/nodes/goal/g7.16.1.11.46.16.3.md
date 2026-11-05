---
id: goal:g7.16.1.11.46.16.3
mint_id: 4ce121fce2584433869c3609b6b509d8
type: goal
parents:
  - goal:g7.16.1.11.46.16
next_edges: []
edited_by: director-general-3
goal_id: G7.16.1.11.46.16.3
goal_kind: subgoal
season: 3
status: complete
title: "G7.16.1.11.46.16.3: the census's double_mints is exactly a NAMED set, each one resolved on its node or ruled by the owner (no double mint is an orphan nobody owns)"
town: local-maxxing
confidence: 0.5
origin: goal
seeds: []
tags: []
---
# goal:g7.16.1.11.46.16.3

## Why this exists
goal:g7.16.1.11.46.16 (closing at 429da99277) CARRIES 'double_mints 5 -> 10' and, once it lands, no open node owns the ten (self-perpetuating's placement note, relayed by SM 22:2xZ 10-27): goal:g7.16.1.11.46.16.1 refuses only a NEW double mint, and the 09-29 five are double-minted ids, not a goal tracking the class. MEASURED at 9ba23adc44 (`grid.py census --orphans`, each ghost's grid ref against the node file's own mint): 8 ghosts hold ONE version beside a live node with its own history (goal:g7.31.3.3.1-.5, goal:g7.32.5, experiment:a00-db75bb99-6d7472, experiment:a00-230456c1-1abcda: nothing to choose); goal:g7.33.9's ghost 65a8f6499c454efbb841185fcc92bfad holds FIVE versions while the node's mint 186661f2be holds ONE (a real choice of content, the owner's); hypothesis:a00-1467544f-chain-600hop's ghost sits under the malformed ref name refs/grid/node/hyp/a00-1467544f-chain-600hop (not a 32-hex mint) beside its node's mint 34a607fdc8 (5 versions). All ten came in through the origin-snap adoption of goal:g7.16.1.11.46.16, never through `commit` (which refuses them since goal:g7.16.1.11.46.16.1).

## Target end-state
- Each of the ten carries ONE THOUGHT line on its live node naming its ghost mint and why it is kept (the 09-29 five already do, rows (3) of the census-orphans decision); nothing is rewritten, no ref is deleted or renamed.
- goal:g7.33.9: RULED by the owner 10-28, option (a) (the OWNER block below): g7.33.9 stays the trunk's TEMPLATE-MAX goal (mint 186661f2be, its links unchanged); the origin ghost 65a8f6499c (5 versions) stays a NAMED reading in the grid history, never a live goal; nothing deleted. Its GHOST MINT line names the ruling.
- The malformed ref name refs/grid/node/hyp/a00-1467544f-chain-600hop stays COUNTED as one of the ten double mints (the census code is not changed); its node's ghost line names the malformed name.

## Invariants
- No grid ref is deleted, renamed or forced; no node is renumbered.
- The census never reads a double mint as anything else, and `unclassified` stays 0.

## Falsifier
1. `grid.py census --rev <trunk>` prints `double_mints=10`, and `census --orphans` lists double-mint rows whose LAST-ID column (the id the census PRINTS) is EXACTLY these ten: goal:g7.31.3.3.1 · goal:g7.31.3.3.2 · goal:g7.31.3.3.3 · goal:g7.31.3.3.4 · goal:g7.31.3.3.5 · goal:g7.32.5 · experiment:a00-db75bb99-6d7472 · experiment:a00-230456c1-1abcda · goal:g7.33.9 · hyp:a00-1467544f-chain-600hop (printed `hyp:`, its node file .agi/nodes/hypothesis/a00-1467544f-chain-600hop.md); a new id = RED. And for each of the ten, its node file (the file whose `id:` line is that printed id) must EXIST at the rev (`git cat-file -e <rev>:<path>`) BEFORE its grep counts -- absent = `unread <id>`, RED by name, never a 0 -- and then carry a `GHOST MINT` THOUGHT line naming its ghost: 10 of 10 at the close; 5 of 10 on the trunk at the build cut = RED.
2. Negative: `grid.py census` prints `unclassified=0`, and no double mint outside the named set appears after this leaf lands.

## OWNER 2026-10-28 02:3xZ, verbatim (owner chunk c:a3defee383b8)
"a is fine yes"

To belam in chat, 2026-10-28T02:31:38Z, answering SM's [owner-q] 23:1xZ 10-27 (via belam) on goal:g7.33.9: option (a) = g7.33.9 stays the trunk's TEMPLATE-MAX goal; the ghost's 5 versions stay a NAMED reading in the grid history, never a live goal (relayed by SM 02:41Z, belam [decision] 02:3xZ).

## goal:g7.33.9, the owner's pick (RULED (a), above): the node's mint 186661f2be (1 version, 10-08) -> the ghost 65a8f6499c (5 versions, 09-28), node.md
```diff
diff --git a/node.md b/node.md
index c4a5c1ff02..d5da9c1a30 100644
--- a/node.md
+++ b/node.md
@@ -1,40 +1,68 @@
 ---
 id: goal:g7.33.9
-mint_id: 186661f2be774b178e0e9d05d944d1f2
+mint_id: 65a8f6499c454efbb841185fcc92bfad
 type: goal
 parents:
   - goal:g7.33
 next_edges: []
-confidence: 0.9
-edited_by: thought-master
+confidence: 0.85
+edited_by: belam
 goal_id: G7.33.9
 goal_kind: subgoal
 heading_level: 4
+location: source_root
 origin: goals-doc
-scaffold_hash: b5210303cfffe508
+scaffold_hash: c48a5a8b2feef73e
 season: 2
-seeds: []
-status: active
+seeds:
+  - goal:g7.33.9.1
+  - goal:g7.33.9.2
+  - goal:g7.33.9.3
+status: complete
 tags:
-  - local-maxxing
-  - engine
-  - template-max
-title: "G7.33.9: TEMPLATE-MAX FOR MODEL-FACING PROSE -- every warning, refusal, nudge and reminder the engine sends a model loads at run time from a template, never a literal in a build node"
+  - skills
+  - write
+  - mint
+  - redesign
+thought_session: belam-g73391-close-20260928T224501Z
+title: "G7.33.9: skills + write/mint foundation (redesign order step 1-2)"
 town: core
 ---
+<!-- BODY:BEGIN -->
 # goal:g7.33.9
 
-| | |
-|---|---|
-| goal | every warning, refusal, nudge and reminder the engine sends back to a MODEL loads at run time from a template -- never a literal in a build node |
-| origin | the owner 16:20Z 09-24 (verbatim on town:local-maxxing's board) · first case: rotation_alert.py's band text read as a stop (director-engine idled at 0.40 of the 0.47 line, 14:10-16:16Z) |
-| scope | text a model reads: hook output (UserPromptSubmit / SessionStart), CLI refusals and warnings an agent acts on, nudges, reminders · NOT human-only logs, internal exceptions, test fixtures |
-| where | extensions/agi/templates/<family>/ -- ONE loader, placeholders filled at the call site, no second copy in code |
-| order | T0 = the inventory (every model-facing literal: file:line, family, fields; committed) + the loader + rotation_alert migrated -> T1..Tn one family per batch, the largest model-facing surface first |
-| rule | byte-identical first: a test per family pins old render == new render · wording changes land separately, one per commit |
-| done | the inventory's "still in code" column = 0, and every migrated family has a guard test that it prints only through the loader |
-| who | director-engine, batched by thought-master · feeds goal:g1.19 (core's engine surface inventory under config-maxxing) |
+## Why this exists
+**Parent `goal:g7.33`.** Belam 2026-09-28 activate for write/mint foundation: redesign land order is **skills → write/mint → spawn/rotate → messaging**. This leaf is steps 1–2 (adoption/order track). Engine write.py ergonomics traps stay on `goal:g7.33.1`; this leaf does not re-own those FIX rounds. SoT patch `/tmp/belam-sot-patch/goals/g7.33.skills.md` (link_ref) + Belam note on `goal:g7.33`: nest skills adoption under g7.33.
+
+## Target end-state
+- `skills/agi-*` (at least agi-node-write · agi-goal · agi-verify · agi-merge-pass) present on core trunks; `.claude/skills` symlinks resolve to them.
+- Directors pursue all node+goal writes via `skill:agi-node-write` / `skill:agi-goal` → `write.py` only — no hand-edit of `.agi/nodes/**`, no inlined PROFILE write recipes.
+- write/mint foundation usable without pi parents: `write.py create|set|note|thought|replace body` + spawn gate; ACTIVE-BEFORE-SPAWN / pi dispatch are out of this leaf (OWNER FULL STOP: NO pi).
+- Nested kids carry the adoption split: `.1` skills present+wired · `.2` write/mint route discipline.
+
+## Invariants
+- `write.py` is the only sanctioned node writer (skill agi-node-write §1).
+- Never invent a new top-level `g7.N` (Belam/Prime only). Nest under `goal:g7.33` / this leaf.
+- `goal:g7.33.1` keeps the engine FIX track for replace-body / create-scaffold / compose traps; this leaf never duplicates those hypotheses.
+- Caps ≤10/dir · ≤20 box still apply to non-pi work. No durable OpenRouter pi spawn from this leaf.
+- Deprecate-never-delete; GOALS.md is derived (`snapshot-goals.py --render`).
+
+## Falsifier
+1. `test -f skills/agi-node-write/SKILL.md && test -f skills/agi-goal/SKILL.md && test -L .claude/skills/agi-node-write` exits 0 on seat tip.
+2. `python3 extensions/agi/bin/write.py -h` exits 0 and documents replace-body standalone rule.
+3. Negative: zero hand-edit commits under `.agi/nodes/goal/g7.33.9*` that bypass write.py actor/session stamping on this leaf after foundation land.
+
+## Out of scope
+- `goal:g7.33.1` write.py ergonomics engine rounds (hypotheses under that leaf).
+- spawn/rotate redesign (redesign order step 3) and messaging (step 4) — later leaves under g7.33 or sibling tops when Belam mints.
+- town:core stop-line assignment moves (Belam daily board SoT); this leaf does not rewrite `doc:geometry-towns-core` seat rows.
+- pi parent dispatch / agi-dispatch durable spawn (OWNER FULL STOP).
+
+## Agent Notes
+Assigned to **director-belam**. Foundation write/mint only via write.py + graph skills; no pi. Kids: `goal:g7.33.9.1` (skills adoption), `goal:g7.33.9.2` (write/mint route).
 
 <!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
-renumbered goal:g5.32 -> goal:g7.33.9 on the owner 16:24Z 09-24 rule (fixes nest as sub-sub goals inside a fixes subgoal of the top-level subgoal they apply to, never a new top-level goal): g7.33 = ENGINE FIXES SURFACED BY THE TOWN; mint_id unchanged; the one frontmatter reference (the town:local-maxxing board rows) re-pointed in the same commit
+NO-PI pass: parallel seat already minted .1/.2 (skills adoption + write/mint route, still active); this pass minted .3 title-regex residue COMPLETE + schema/tests; parent stays active
 <!-- THOUGHT:END -->
+
+Belam NO-PI: closed g7.33.9.2 write/mint route (falsifiers GREEN; residues=0; format✓). g7.33.9.1 skills adoption still active. No pi.
```

## Out of scope
goal:g7.16.1.11.46.16 (closing) · goal:g7.16.1.11.46.16.1 (complete: the commit-path refusal) · goal:g7.16.1.11.46.16.2 (the owner-batch scope) · the owner's pick for goal:g7.33.9 (RULED (a) 10-28; applied here, never made here)

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-3 10-27 22:3xZ: minted on self-perpetuating's placement note (via SM 22:2xZ): ONE leaf for the class, its falsifier = the census's double_mints equals the named set, each resolved or ruled (sp's recommendation). Node only; the THOUGHT lines and the bank row come in its build.
BUILD (director-general-3 10-27 22:4xZ, SM [placed] 22:3xZ: the mint carried in): a GHOST MINT THOUGHT line on the five nodes that had none (goal:g7.32.5, experiment:a00-db75bb99-6d7472, experiment:a00-230456c1-1abcda, goal:g7.33.9, hypothesis:a00-1467544f-chain-600hop), the 09-29 five already carry theirs; goal:g7.33.9's diff in the section above, for the owner's pick SM banked. Nothing rewritten, no ref touched. RE-WORDED before the build (all-is-one's pre-read 22:32:42Z: the Target's 'name the malformed ref as a reading' contradicted falsifier 1's count of 10): that Target line is replaced by 'stays counted' (no census code change, the smaller scope), so one text, one count: double_mints = the named 10. RE-CUT 1 (self-perpetuating 22:45:36Z via SM 22:46Z): falsifier 1 names the ids the census PRINTS (the malformed one is `hyp:`, its file under hypothesis/) and requires each node file to EXIST at the rev before its grep counts (an absent path is `unread <id>`, never a 0: git grep over an absent path reads like a missing line).
OWNER'S PICK APPLIED (director-general-3 10-28 02:5xZ, SM [relay] 02:41Z): option (a), owner chunk c:a3defee383b8. The Target's g7.33.9 line now reads RULED; the OWNER block carries the words verbatim; goal:g7.33.9's GHOST MINT line names the ruling. Nothing rewritten in g7.33.9's body, no ref touched, the ghost stays counted (falsifier 1's ten unchanged). With this, each of the ten is resolved on its node or ruled.
CLOSE goal:g7.16.1.11.46.16.3 = THIS tip + falsifiers RE-RUN at c61e59d6e7 (L250, the live trunk, the owner's pick (a) landed), director-general-3 10-28 04:1xZ, the falsifier AS WRITTEN, nothing amended: ROW 1 `grid.py census --rev c61e59d6e7` prints double_mints=10; `census --orphans` lists exactly ten double-mint rows whose printed ids are the named ten (goal:g7.31.3.3.1-.5, goal:g7.32.5, experiment:a00-db75bb99-6d7472, experiment:a00-230456c1-1abcda, goal:g7.33.9, hyp:a00-1467544f-chain-600hop), no new id; each node file EXISTS at the rev (git cat-file -e, 0 unread), its id: line = the printed id, and carries ONE GHOST MINT line naming its own ghost (the mint, or for the hyp the malformed name hyp/a00-1467544f-chain-600hop): 10 of 10. ROW 2 `grid.py census`: unclassified=0, and no double mint outside the named set. goal:g7.33.9 is RULED by the owner (a) (L250, chunk c:a3defee383b8): the ten are each resolved on their node or ruled.
<!-- THOUGHT:END -->
