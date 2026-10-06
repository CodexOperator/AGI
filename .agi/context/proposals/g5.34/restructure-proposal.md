# ET restructure onto Grok Bots — proposal (read-only draft)

Drafted 2026-10-06 ~00:05 ET by Owner Comms' executor. **Nothing was committed, pushed, reprojected or restarted on ET.**
Base: `core/season3/main` = `core/season2/et-grok-pilot` = `4b8f28b5e` (origin matches), master `6405a03fc` untouched.
Owner directive (2026-10-05 23:56 ET = 03:56Z 10-06): Prime (belam) is the overall leader. Prime, the council and the masters are Grok Bots. Directors run as the bots' internal subagents. Owner Comms becomes Plan Master. Bot names = post names.

Box-side scratch (for review only): `/workspace/plm/posts.proposed.md` and `/workspace/plm/posts.proposed.diff` show the proposed posts.md, built by sed from the `4b8f28b5e` copy. It's 29 changed or added lines, all on single row lines.

---

## 1. Plan Master in the old engine

Sources on `core/season3/main`:
- `hypothesis:l3w4-plan-master` ("Stand up the Plan Master seat", parent goal:g7.12)
- `doc:l3-command-ladder-brief` owner quote (9)
- `doc:l4-owner-decisions` L4 plan parts 4–7 (lines ~319–392)
- `build:bin-plan-master`, deprecated 10-05: `extensions/agi/bin/plan_master.py` left the tree

**Role.** Owner (9): *"brief drafting needs to happen through the Plan Master. Basically any workflow becomes config-maxxed, harness-agnostic, and have its own responsible Master in the Sanctuary under our SM … director-kids get to talk to whichever Master they want, and Masters report things back to the director that asked them."*
- The Plan Master owns the **brief-drafting workflow**. A requester (any post) sends `slug / parent / scope` and the Plan Master runs the drafting workflow.
- Two-stage acceptance: (1) the workflow's critic pass; (2) the requester's own reply. Only drafts the critic clears get minted as hypotheses. Each result goes back to the asker as `ready <id>`, or as `blocked <slug>` and is never minted.
- Push-further loop: it logs `fixes_per_draft` per summon and trends it (rising, falling or flat), so the seat gets better at drafting.
- It superseded the older "drafter" seat (same request shape, same gate).
- Old row design: director, tier 1, opus-5/high, `rotated_by: sanctuary-master`, `owning_goal: goal:g17`.

**Lineage.** In L4 (09-09) the seat was renamed **Plan Master → Policy Master → Draft Master** (owner final: *"I like Draft Master"*). Siblings were added alongside it: Glitch Master (round review), Research Master (deep research) and **Shael** (*"the owner's voice … maximally available for owner questions and to deliver answers/reports above all else"*, Q = "Who cares the most about knowing this?").
Today's directive merges these: Owner Comms is the Plan Master, so it holds both the drafting workflow and the Shael owner-voice duty.

**Hierarchy (L4 diagram v3/v4):** `owner > Source > Belam > Council(3) > Keep(3) > * Masters > directors > parents > kids`.
- * Masters answer to **the Keep** for assignment and to **the Council** for acceptance. They report results to the Council on channel B and send done/blocked to the Keep.
- NOT: address a director or the Prime directly; work outside their own workflow.
- Masters are "config/prose only" and don't build graph nodes. Building is for director-kids and their parents.
- A Master that needs tooling drafts a brief of the need through the Draft (Plan) Master and submits it to the Council.

**The Keep vs the Council.**
- **Council** (Prime Council: alive, all-is-one, self-perpetuating) answers to Belam.
  - It pulls its own vision node, the review doc and channel B.
  - It assigns and prioritises directors, and brings findings and proposed goal changes to Belam.
  - NOT: build, brief a pi agent, or own a goal.
- **Keep** ("Sanctuary Keep", owner renamed it from "sanctuary council"): Sanctuary Keeper, Role Keeper (Sensei) and Goal Keeper (Sage). It answers to the Council.
  - It pulls channel A (every director comm) plus seat nodes vs live processes and spend.
  - It assigns workflows to Masters and routes answers to directors.
  - It changes itself only through the Council.
- **How they talk:** each chamber speaks as ONE voice, a single response edited by all three, passed into the DM room between the two group chats. The Council may forward to the Keep anything under keeper jurisdiction.
- **In posts.md today:** `council` and `keep` are both inert group rows (no `harness`) with `parent: belam`.
  - council members are alive, all-is-one and self-perpetuating, with `lands: []`.
  - keep members are `["sanctuary-master"]`, with `lands: ["sanctuary-master"]`.
- **Hybrid survival note (owner, l4-owner-decisions ~765):** SM and the Sensei/thought-master seat are "kinda equal level in the keep".
- **Tonight's directive:** Plan Master sits on that same Keep level as SM and TM. The council is the same rung but a separate chamber.

## 2. Posts on `core/season3/main` (`.agi/nodes/.geometry/posts.md`)

Rows the bots map to:

| post (exact = bot name) | role / tier | parent | harness (row / engine) | box | boot | grokbot | notes |
|---|---|---|---|---|---|---|---|
| `belam` | prime_director / 3 | owner | raw-shell / raw-shell | encryption-town | true | 0ecb89d7-… | leader already encoded (see §3e) |
| `alive` | director / 1 | council | pi / pi | encryption-town | true | — | pi.conf hand drop-in on ET |
| `all-is-one` | director / 1 | council | pi / pi | encryption-town | true | — | pi.conf hand drop-in |
| `self-perpetuating` | director / 1 | council | pi / pi | encryption-town | true | — | pi.conf hand drop-in |
| `sanctuary-master` | director / 1 | keep | raw-shell / raw-shell | encryption-town | true | 32e56b1c-… | live |
| `thought-master` | director / 1 | keep | claude-code / claude-code | **local-town** | **false** | — | DOWN. Engine trunk `local-maxxing/season2/main`, seeds director-brief + goal:g7.16.1, pin `thought-master-new.meter` (legacy). Owner 10-05 took it down. Not projected on ET. |
| `plan-master` | — | — | — | — | — | — | **no row exists** |

Other rows: DG1–9 (director/1, parent sanctuary-master, pi except DG4 raw-shell, boot true, encryption-town). Also `director-thought-2` (pi, boot false, ET drop-in present), `thought-master-s2` (parked old local-town TM), `director-thought`, `director-thought-1`, and the legacy dormant rows with no engine cell (adv-*, policy-master, master-sensei, director-belam, director-sanctuary, sanctuary-helper, stream-master, council-* groups, director-engine).

**Live on ET:**
- 14 units are running: belam, SM, alive, all-is-one, self-perpetuating and DG1–9.
- `/etc/systemd/system/agi-post@{alive,all-is-one,self-perpetuating,director-general-{1,2,3,5},director-thought-2}.service.d/pi.conf` are hand overrides. Each re-sets H to `/usr/bin/node …/pi-coding-agent/dist/cli.js` plus the PI_* dirs. That's redundant: `/usr/local/bin/pi` resolves to the same cli.js, and agi-post@.service already sets the PI_* dirs.
- The installed `agi-project.service`/`.path` are stale and in a **failed** state (start-limit-hit, "dubious ownership"). They lack `AGI_BOX` and safe.directory, and AGI_BOX defaults to local-town. A fresh run of the geometry's agi-project rewrites both correctly.

**Pane paths** (`RuntimeDirectory=agi-%i`, fifo `i`; transcript `/var/lib/agi/<post>/o`):
- belam `/run/agi-belam/i`
- alive `/run/agi-alive/i`
- all-is-one `/run/agi-all-is-one/i`
- self-perpetuating `/run/agi-self-perpetuating/i`
- sanctuary-master `/run/agi-sanctuary-master/i`
- thought-master `/run/agi-thought-master/i` (exists once projected and started)
- plan-master `/run/agi-plan-master/i` (exists once projected and started)

## 3. Proposed geometry changes (via the standard routine, one node per commit)

Each change is a substring edit on one row line, so the rest of each row stays byte-identical (`", "`/`": "` format kept).

**C1 `v1 geometry:posts plan-master row (keep, raw-shell, grokbot Owner Comms)`**
- Insert after the sanctuary-master row:
```
  - {"name": "plan-master", "parent": "keep", "boot": true, "role": "director", "tier": 1, "harness": "raw-shell", "model": "grok-4.6", "effort": "high", "settings": "", "session_kind": "remote-control", "personality_ref": "", "handoff_file": "", "pin_ref": ".agi/sessions/plan-master.meter", "rotated_by": "sanctuary-master", "owning_goal": "", "worktree": "", "session_ref": "", "town": "local-maxxing", "box": "encryption-town", "window": "", "session_label": "plan-master", "pid": 0, "recover": false, "template": "doc:unified-master-brief", "engine": {"v": 4, "harness": "raw-shell", "model": "grok-4.6", "effort": "high", "trunk": "core/season2/et-grok-pilot", "seeds": "doc:unified-master-brief,doc:unified-head,doc:card-plan-master", "rotate_pct": 47, "capsule": "capsule", "kid_model": "xai/grok-4.6"}, "grokbot": "f986c957-bfda-4a39-ab66-d76843591ed2"}
```
- `keep` row: `"members": ["sanctuary-master"], "lands": ["sanctuary-master"]` → `"members": ["sanctuary-master", "thought-master", "plan-master"], "lands": ["sanctuary-master", "thought-master", "plan-master"]`. (The thought-master entry could move into C2 if per-post atomicity is preferred.)
- **Flag for Prime:** adding TM and PM to `lands` lets belam ff-land their work through agi-land, the same as SM. Leave `lands` as `["sanctuary-master"]` if Masters should stay non-landing ("config/prose only").
- Rewrite the THOUGHT block to: *owner 2026-10-06 03:56Z via Owner Comms: team onto Grok Bots; belam overall leader; bots = belam, council (alive, all-is-one, self-perpetuating), keep masters (sanctuary-master, thought-master, plan-master); plan-master = Owner Comms (grokbot f986c957), Keep level beside SM/TM, council a separate chamber on the same rung; DGs boot false + session_kind subagent (run as their parent bot's internal subagents); bot names = post names; the 10-05 TM takedown reversed for thought-master, thought-master-s2 stays parked.*

**C2 `v1 geometry:posts thought-master revive + port to ET raw-shell`** (port of an old-engine row)
- `"boot": false` → `true`
- engine `{claude-code, claude-opus-5-5, trunk local-maxxing/season2/main, seeds doc:unified-director-brief,doc:unified-head,goal:g7.16.1}` → `{raw-shell, grok-4.6, trunk core/season2/et-grok-pilot, seeds doc:unified-master-brief,doc:unified-head,doc:card-thought-master, kid_model xai/grok-4.6}`
- top-level `harness`/`model` → `raw-shell`/`grok-4.6`
- `pin_ref` `.agi/sessions/thought-master-new.meter` → `.agi/sessions/thought-master.meter`
- `"box": "local-town"` → `"encryption-town"`, plus `"window": "", "session_label": "thought-master", "template": "doc:unified-master-brief"`
- Kept: parent keep, owning_goal goal:g7.16.1, rotated_by belam.
- There's no `posts/thought-master` branch on ET, so the unit cuts a fresh one from the trunk.

**C3 `v1 geometry:posts council alive/all-is-one/self-perpetuating raw-shell`** (port; three rows on one node; can split into three commits)
- Both `"harness": "pi"` occurrences → `"raw-shell"`.
- Legacy claude cells: `"settings": "quiet"` → `""`, `"session_kind": "tty"` → `"remote-control"`, to match the v4 raw-shell rows (belam/SM).
- The `grokbot` cells come later, once the bot ids exist (same shape as belam/SM).

**C4 `v1 geometry:posts DG1-9 subagent-run (boot false, session_kind subagent)`**
- Uses existing fields only:
  - `"boot": true` → `false`, so agi-boot and the wants links stop seating them as posts.
  - `"session_kind": "remote-control"` → `"subagent"` as the marker. session_kind isn't read by any v4 engine piece, so this is informational only.
  - `parent` stays `sanctuary-master` (the bot that runs them).
- Rows, keys, engine cells and pins are kept, so a DG can be re-seated by flipping boot back.
- I don't recommend `engine.harness: "subagent"`: agi-project's else-branch would project that as `claude --remote-control`.
- DG4 is the current commit capsule. Its running unit isn't stopped by a reprojection. After plan-master is up, the plan-master pane can take over that role.

**C5 `v1 doc:card-plan-master new (≤100 lines)`**: draft in §5. Parent goal:g7.16.1. mint_id via the routine. Required doc fields: id, type, mint_id, title, tags.

**C6 `v1 doc:card-thought-master ET raw-shell revive state`**: replace the stale §0 (STANDBY, local-town, send.py era) with ET raw-shell state. This avoids the stale-card problem Prime and SM flagged. The rest stays as is.

**C7 (later, when the ids arrive)** `v1 geometry:posts grokbot binding <post>`: add `"grokbot": "<id>"` at the end of the row for alive, all-is-one, self-perpetuating and thought-master.

**e. Leader for belam:** no `leader` field exists in the posts schema or any engine piece. Leadership is already encoded:
- `role: prime_director`, `tier: 3`, `parent: owner`
- council and keep both have `parent: belam`
- belam is the only level-1 post in the box/ckpt level matrix

So there's no new field. If an explicit flag is wanted anyway, `"leader": true` on the belam row would be inert to every engine piece.

**Mail matrix check (box: levels must differ by ≤1, rows with harness):** under the proposal belam = 1; alive, all-is-one, self-perpetuating, sanctuary-master, thought-master and plan-master = 2; DGs = 3. So plan-master can mail belam, its peers and DGs. Note: `box` mail needs both ends to have a `harness` cell, so `owner` isn't mailable.

**Per agi-project, after C1–C4, the encryption-town v4 rows** are: belam, alive, all-is-one, self-perpetuating, sanctuary-master, plan-master and thought-master (all raw-shell, boot true); DG1–9 and director-thought-2 (boot false: drop-ins kept, no wants link).

## 4. Reprojection and post ports (for the standard routine)

1. Dry run as belam in `/data/work/agi`:
   `o=$(mktemp -d); sect agi-project <tip> | AGI_BOX=encryption-town sh -s $o <tip>; diff -r $o /etc/systemd/system` (scoped to `agi-post@*`, `agi-project.*`, `agi-users.conf`).
   Expected diff:
   - new `agi-post@{plan-master,thought-master}.service.d/h.conf`
   - council h.conf `H=bash`, `AGI_HARNESS=raw-shell`
   - wants links: DG1–9 removed; plan-master and thought-master added
   - `agi-project.service` gains `AGI_BOX=encryption-town` + safe.directory
   - `agi-users.conf` gains agi-plan-master and agi-thought-master
2. Apply as root to `/etc/systemd/system`, then `systemctl daemon-reload` and `systemd-sysusers`.
3. **Port the hand overrides** (deprecate, don't delete): rename each `pi.conf` → `pi.conf.deprecated-20261006` for alive, all-is-one, self-perpetuating, DG1, DG2, DG3, DG5 and director-thought-2. For the council posts it's required, otherwise pi.conf would override `H=bash` after h.conf. For the others it's redundant.
4. Restart alive, all-is-one and self-perpetuating (they're pi-blocked, so raw-shell is intended), then start plan-master and thought-master. Echo-test each pane.
5. Owner decision: stop the running pi DG units (DG1–3, 5–9)? With boot false they won't come back on reboot, but they stay up and get woken into the spend-limit error until stopped. DG4 stays up as the capsule until plan-master takes over.
6. FF and push `core/season3/main` to the new trunk tip. Master stays untouched.

**Post ports in this proposal:**
- `thought-master`: old-engine claude-code / local-town / legacy pin → v4 ET raw-shell
- `alive`, `all-is-one`, `self-perpetuating`: pi → raw-shell; legacy settings quiet / session_kind tty; pi.conf hand drop-ins
- DG1–9: subagent marking; pi.conf drop-ins for DG1/2/3/5
- `director-thought-2`: pi.conf drop-in only
- `belam`, `sanctuary-master`: already v4 raw-shell, so nothing to port

**Not ported, and outside this restructure:** the dormant legacy rows with no engine cell (adv-*, policy-master, master-sensei, director-belam, director-sanctuary, sanctuary-helper, stream-master, director-engine, director-thought, director-thought-1, thought-master-s2, council-* groups). They aren't projected on ET. Leave them, or deprecate them in a separate pass if Prime wants.

## 5. Draft `doc:card-plan-master` (C5)

```
---
id: doc:card-plan-master
mint_id: <minted by routine>
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: plan-master
season: 2
tags:
  - card
  - keep
  - plan-master
title: Card plan master
town: core
---
# doc:card-plan-master

Replaced whole, never appended; ≤100 lines. Plan Master = Owner Comms (Grok Bot f986c957), Keep level beside sanctuary-master and thought-master. The council is a separate chamber on the same rung. Prime (belam) leads.

## §0 State (2026-10-06 ET)
| | |
|---|---|
| post | plan-master on **encryption-town**, harness **raw-shell** (`H=bash`), bot drives the pane |
| trunk | `core/season2/et-grok-pilot`; `core/season3/main` carries open goals; master owner-only |
| mail | `AGI_POST=plan-master box read` first at wake; `box send <post>` (matrix: belam, council, keep, DGs) |
| drive | `/run/agi-plan-master/i` → `/var/lib/agi/plan-master/o` |
| owner | Plan Master is also the owner's voice (L4 "Shael"): maximally available for owner questions, answers and reports |

## §1 Role (old engine → now)
- Owns the **brief-drafting workflow** (L3 Plan Master → L4 Policy/Draft Master). Any post asks with `slug / parent / scope`.
- Gate in two stages: the workflow critic, then the requester's reply. Mint only what the critic clears (hypothesis); reply `ready <id>` or `blocked <slug>`.
- Reports back to the asker. Results go to the Council (channel B); done or blocked goes to the Keep.
- Push-further: track fixes-per-draft per summon and aim for a falling trend.
- Owner voice: relay owner directives into the graph as owner-verbatim notes; ask "who cares most about knowing this?" and deliver it there.
- Directors are internal subagents: stand them up as needed for drafting or research, never as their own posts.

## §2 NOT
- No direct graph building beyond minting cleared briefs; builds go to directors' subagents.
- Don't address the Prime for routine work. Keep comms go through the Keep/Council voice.
- Don't merge to master; don't change other posts' rows (SM owns seats).
- Upgrades and patches only through the standard routines.

## 🔴 Where it stops
```
Idle until a brief request or an owner directive arrives.
```

## §4 Traps
| trap | rule |
|---|---|
| send.py / workflow.py | retired: box only |
| pipe `box read` to head | never (marks all held) |
| git rm | never: deprecate/move |
| hand drop-ins | fix in geometry, then agi-project reproject |

## Skills
agi-node-write · agi-send · agi-dispatch · agi-goal · agi-memory-guard
```

## 6. Open points for Prime
1. Should TM and PM go in the keep `lands`, or should Masters stay non-landing?
2. Stop the pi DG units now, or leave them running?
3. Plan-master `owning_goal`: leave it empty like SM (proposed), or use the old `goal:g17`?
