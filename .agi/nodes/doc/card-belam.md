---
id: doc:card-belam
mint_id: ced15049ceb843b08e51cc50da416298
type: doc
parents:
  - goal:g7.16
next_edges: []
edited_by: belam
scaffold_hash: 3388df8d4c85caa7
season: 2
tags:
  - card
  - prime
  - belam
thought_session: belam-S2-L5-I
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam

# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23 (goal:g5): the card is the handoff scratch space, and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this node's file. Role = the Prime template (`build:briefs-prime-director-successor`, which carries the five-axis map) + the HEAD (`doc:unified-head`); brief.py will assemble HEAD + template-by-role + card (`hypothesis:brief-py-assembles-every-first-turn-from-config`, director-engine). Written DURING the work, replaced whole, ≤ 175 lines; owner verbatim lives in nodes, never here.

## §0 State (09-23 09:0xZ)
| | |
|---|---|
| post | belam-S2-L5-I (gen 2) · Opus 5.5 · remote-control, the owner watches from claude.ai |
| box | local-town: MAIN `/data/work/agi`, user belam, tmux `agi-rc`, logs `~/logs/agi-crons-agi-3fbc6951.log`; core-town DOWN |
| branches | town trunk `local-maxxing/season2/main` (MAIN; thought-master commits here — exact-path commits only) · root `season2/main` = origin only, ancestor of the trunk · posts on `local-maxxing/season2/posts/<post>/main` worktrees · push UP (origin redirects to CodexOperator/AGI.git) |
| formation | Prime · thought-master (point, R&D) · director-thought (helper, R&D) · director-engine (build: Prime-assigned g15 only; goal:g7.33 HELD = core's) |
| crons | SESSION-ONLY, re-arm FIRST on wake from `.agi/sessions/prime-merge.crons.md`: CHECK every 4 h "13 */4 * * *" (owner 09-23 15:0xZ; the row is QUIET: read the dm logs directly, not send.py read) · PASS one-shots as the check arms them · persisted `prime_merge 13 */4` INERT until `extensions/agi/bin/prime_merge.py` lands |
| merge | BASE 8cf1eb4c9 → trunk: 233 commits / 135 experiment files (08:45Z) · notice 06:41Z · PASS 2 = 11:41Z · state `.agi/sessions/prime-merge.state.json` |
| nodes | links 0 broken · GOALS byte-identical (309 goals) · active never drops |
| spend | 39.76 USD left at 09:2xZ 09-23 (total 155, usage 115.24) · floor -50 (owner 09-23 10:3xZ) · `OPENROUTER_API_KEY` empty by design |
| harness | pi at `/home/belam/.npm-global/bin/pi` · `PI_BIN` + `PATH` in profile + tmux -g (sessions older than 05:22Z 09-20 prefix inline) · `workflow.py --harness pi` works here only because the config's `/home/ubuntu/…/pi` path was made to exist |
| meter | pin `.agi/sessions/belam.meter` · rotate at f ≥ 0.47: stops slot + stamp FIRST, then bare `AGI_SEAT=belam AGI_POST=belam python3 extensions/agi/bin/rotate.py rotate` |

## §1 Plan — DOC UNIFICATION (owner 09-23, verbatim on goal:g5; the doc half of doc:s3-plan HEAD 1.5)
```
model   per role: HEAD (doc:unified-head, same bytes for every role incl. parents + kids)
        + TEMPLATE by role (director · master · Prime), chosen by config: the post row cell, else the formation default
        + CARD (per post: its own loop + live scratch) · TOWN TRAJECTORY (the town todo, mostly the master's)
        assembled by brief.py straight into the first turn — no injection file · HANDOFF → this card (symlink)
✅ owner lines banked · model on doc:s3-plan · flavor doc retired (969c7390b) · HEAD drafted: doc:unified-head (1e6ca0056)
✅ director-engine rounds: hypothesis:brief-py-assembles-every-first-turn-from-config (template BY ROLE) · hypothesis:write-py-inline-replace-verb · hypothesis:links-py-flags-live-references-to-retired-goals
✅ HANDOFF.md + the quorum card = symlinks to doc:card-belam · card orders sent: thought-master · director-thought · director-engine
✅ retired ids out of use (owner 09:0xZ-09:1xZ): g14→g5 · g14.3→g5.19 · g14.14→g7.33 · g9.7→g2.19 · g13/g13.1→none · g14's 70 owner lines MOVED to goal:g5 (no pointer) · owning_goal cells hand-edited · commands tables fixed · lint round → director-engine
✅ templates (owner 09:1xZ go): director doc:unified-director-brief (role only, 20.5 KB) · master doc:unified-master-brief (new, five axes) · Prime = the brief + five axes · this card = doc:card-belam (owner 09:2xZ)
✅ old ids out of the prose of CLAUDE.md · QUICKSTART.md · SKILL.md (998aa21d7) · seat keys republished on season2/main: belam 7e134ba7b, thought-master ed54be7d8 · key round → director-engine FIRST (c445296c0)
⏳ after brief.py lands: retire CLAUDE.md (→ the claude-code harness block) · the 5 INJECTION.md writers · the prime [handoff-head] entry
```

## §2 Landed (09-23)
969c7390b owner lines + L6 note + flavor doc retired · 1e6ca0056 doc:unified-head · 4c08f0c3a brief.py hypothesis · c80b7d4fb HANDOFF symlink + card + Prime template + brief.py amendment + write.py round + g14→g5 re-cites · 07adbae3a commands tables + g14 owner lines → g5 + owning_goal cells + lint round · 7e134ba7b (season2/main) the belam key row · 52d046afd templates + doc:card-belam · 998aa21d7 prose ids · ed54be7d8 (season2/main) thought-master key row · c445296c0 key round

## 🔴 Where it stops
```
09:4xZ 09-23 (gen 2) — IDLE, minimum tokens (owner 09:4xZ: settled + handed off → idle protocol). Next, only as they fire:
 1. PASS 2 at 11:41Z from the session cron (procedure: .agi/sessions/prime-merge.crons.md §2) · daily activation 08:13Z
 2. after ANY rotation on this box: republish that post's re-keyed row on season2/main by hand (as 7e134ba7b / ed54be7d8) until the key round lands
 3. key authority = route B (owner 09:4xZ) · watch, never steer: director-engine queue = key round → brief.py → write.py sub → retired-id lint
```

## §4 Traps
| # | trap | rule |
|---|---|---|
| 2 | Bash-tool shells never re-source the profile inside a running session | env edits reach NEW sessions only; prefix `PI_BIN` inline |
| 3 | `workflow.py` stages run SERIALLY (~15 min each on deepseek) | parallelise by running chunks as separate processes |
| 5 | `write.py replace body 1:N` on a fresh node eats the `<!-- BODY:BEGIN -->` marker; a range that splits a heading from its section is refused | restore the marker as body line 1 · replace whole sections |
| 6 | `send.py send` to a busy pane → `[undelivered-yet]` | the dm IS written; the sweep re-nudges |
| 7 | after a seat key is re-minted, `send.py read belam` re-delivers old dms marked `RETIRED:<key>` | read the timestamp, not the position |
| 8 | two `note` units in one write.py submit keep only one | one note per call |
| 9 | the grid cron versions an UNCOMMITTED node within minutes | a fresh node is retired + moved, never deleted |
| 10 | write.py edits body/payload only; config frontmatter (templates, rows) = `set <field>` whole | frontmatter reshapes → a director-engine round until the in-line replace verb lands |
| 12 | a rotation re-mints the seat key but publishes the pubkey only to the town trunk; verifiers read origin/season2/main → the Prime's dms read UNVERIFIED | publish the seat row on season2/main at once (7e134ba7b); the durable fix = the integration-branch cell (§6) |
| 11 | the harness says "use the Workflow tool" every turn (row setting ultracode) | not the route: workflow.py by name on pi (F29, owner 09-16 19:1xZ) |

## §5 Verification
`links.py links` 0 broken · `snapshot-goals.py --render --check` byte-identical · `commands.py run verify` all green · `git branch --show-current` = local-maxxing/season2/main

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| global git identity on this box (10 of the 18 red tests) | `git config --global user.name/email` for user belam |
| `.agi/config.json` carries core-town literals (`box.*`, `harnesses.*.bin`) in a merge-shared file | director-engine round: `{user}`/`$PATH` resolution or the box overlay; not blocking while `PI_BIN` covers dispatch |
| engine-wide config/template maxxing pass (owner 08:5xZ idea, goal:g5) | after brief.py lands: one goal, nested rounds, config-max first |
