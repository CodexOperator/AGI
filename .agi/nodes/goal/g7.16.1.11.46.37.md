---
id: goal:g7.16.1.11.46.37
mint_id: 2ebb3e21ed4a40309cf295e802bf7270
type: goal
parents:
  - goal:g7.16.1.11.46
  - goal:g7.16.1.11.46.35
next_edges: []
confidence: 0.5
goal_id: G7.16.1.11.46.37
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
scaffold_hash: ef0cfd130a4722f3
season: 3
seeds: []
status: active
tags:
  - hub
  - quota
  - fallback
title: "G7.16.1.11.46.37: an automatic hub fallback on a recorded QUOTA limit only: any post moves to the other hub, never on hub-down alone, never into a hub that is not ok, and the move is LOUD (the owner's Q3 yes, 11-15)"
town: local-maxxing
---

# goal:g7.16.1.11.46.37

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, the live umbrella): a residue that needs its own home becomes a leaf under the bundle that yielded it. goal:g7.16.1.11.46.35 (the quota leaf, complete at L522) SAYS a hub's quota cooldown and names it in stall-watch. Its Target (c) said NO hub move: 'nothing in this leaf moves a post between hubs', the fallback banked for the owner. The owner has now answered (Q3, 11-15, relayed by meme-master 18:57Z via belam; see the OWNER block): yes, an automatic fallback, for QUOTA limits only. SM placed it (P5 of [decision] 19:39:37Z 11-15, 3/3 approve) as a CHILD of .46.35, minted by director-goals-1.
goal:g7.16.1.11.46.35: the parent of lineage and of every word this leaf reads. Its state file (hub, model, state, T, LAST) and its said file are the inputs here, and hub_quota.py and stall-watch stay as they landed.
MEASURED (director-goals-1, 11-15, trunk 7dd7a239b3): /run/agi-hub/state holds one line per (hub, model) with STATE ok | quota | hub-down; /run/agi-hub/route holds 'POST HUB MODEL' per post. The route is written by belam's root timer from the hub's journal and the post's unit start line. The post-to-hub route itself is a root-only env file per post (0600, it also holds the hub token), so applying a move is a HOST act, not engine code a post can run. A real case for the positive row: hub B sat in quota from 05:36Z to 15:00Z 11-15 (aio, SM's placement note 19:56Z).
WHY it needs its own leaf: .46.35's Invariant 'stall-watch still acts on nothing' stands for the reader; a mover is a different actor with a different blast radius (it changes where a post's tokens are spent). It is its own unit, never stall_watch.sh and never hub_quota.py say.

## OWNER 2026-11-15 (c:696556deb72a), verbatim (Q3 'auto hub fallback on quota'; the owner's eight answers + the Quo note, speaker owner, verified in meme-master's mem store by it at 19:59Z, relayed by SM [note] 20:00:30Z; belam's Q3 text relayed by SM 19:58:53Z)
belam's question, asked 16:2xZ 11-14 (belam gen XIX's relay 19:5xZ via SM 19:58:53Z, the mail it sent meme-master): "3. Auto-fallback between hubs on a quota limit: today nothing moves a post between hubs unless the owner asks. Allow an automatic move to the other hub on a limit, yes or no?"
The owner's answer, as meme-master relayed it (18:57Z): "3. Yes"
The chunk holds the owner's whole answer set; Q3's 'Yes' is in it (meme-master's relay 18:57Z).
SCOPE as belam relayed it (19:58:53Z): ANY post, to THE OTHER hub (A <-> B), ON A QUOTA LIMIT only. belam: 'Not asked: which account a crew post may move onto, hub-down moves, moving back after the limit clears: those go back to the owner through me if the leaf needs them.' READING, not the owner's words (alive 20:19Z, .46.35 :31): two hubs ARE two accounts, so 'the other hub' answers A <-> B and only a THIRD account is unasked; hub-down moves and a move back stay unasked, so they are NOT built here.

## Target end-state
- A post is moved to the other hub ONLY on a recorded quota limit: the state file's `quota` line for that post's (hub, model), written from the hub's own cooldown. Never on hub-down alone, never on an unread or stale state, never on a post's symptom (mail, a stalled screen).
- The target hub is checked first: the move happens only if the OTHER hub's state line for that model reads ok, in a state file that is FRESH. FRESH means the state FILE's `written` line is within max-age (hub_quota.py read_state), and an ok line of ANY age counts as ok: an idle hub records nothing, so hub A's opus line on the live file is days old while it reads ok (measured 11-15: written 1794774432, hub A opus T 1794581580). A per-line age would read the 05:36Z-15:00Z window as NO MOVE. A move into a hub that is itself in quota, down or unread does not happen, and the refusal is said once.
- The move is LOUD (sp): ONE line to the said file and the alarm spool names the post, the model, the hub it left, the hub it went to, the quota reset time, the reason `quota`, and the AGE of the target line it trusted: `post X B -> A on quota (B until HH:MMZ); A ok as of MM-DD HH:MMZ, unconfirmed since`. A move with no such line is a defect. If a post is then quota or down on its new hub, that is .46.35's ordinary SAID case, never a second move.
- The move is bounded: ONE automatic move per post, full stop, until belam or the owner clears that post's standing line (alive 20:19Z). So a post moved B -> A on B's quota is NEVER moved A -> B by the mover, whether the first hub's limit cleared or A later hits a quota of its own while B reads ok: that second move would be a move back by another name, and it gets NO MOVE and ONE said refusal naming the standing move. The said file carries ONE standing line per moved post (`post X on hub A since HH:MMZ, moved from B on quota`) so nobody forgets it moved. A move BACK is BANKED for the owner through belam.
- The mover is its own unit. stall_watch.sh and hub_quota.py `say` still act on nothing and move nothing; their old no-move lines are updated in this leaf's tip to point here (see Invariants).
- Scope is exactly Q3's text: any post, the other hub, quota only. Reading (alive 20:19Z, .46.35 :31): two hubs ARE two accounts, so Q3's 'the other hub' answers A <-> B, and the account question is answered for those two; only a THIRD account is unasked. A wider scope (hub-down moves, a move back, a third account) is a question to the owner, not a build.

## Invariants
- NEVER on hub-down alone. The 11-10 night (14:22Z-19:34Z, both hubs unable to resolve upstream) is a day on which a move would have helped nobody and spent the other hub's quota.
- The applying step is belam's host act (the route file is root-only). The engine half decides from the state and route files, with no token and no account name; the host half applies it. Nothing here edits a hub or its config.
- The move carries the hub, the model, the post and a time only. No token, key or account name leaves the host.
- Two places state the OLD rule: goal:g7.16.1.11.46.35 Target (c) stays as history WITH a pointer to this leaf (put there by the mint tip, its last sentence folded into the history bracket), and extensions/agi/bin/hub_quota.py line 29 (and the subject of build:bin-hub-quota) hands the move to this leaf (aio, 19:56Z).
- The moved POST is told: ONE line in its own box names the move, the hub it is on now and its standing line (sp 20:25Z), so a post that wakes on the new hub knows why.
- The host half names WHEN a new route takes effect (a restart at the move, the post being stalled on its quota anyway, or its next start), and row 7 pins which (sp 20:25Z).
- A post with NO route line (belam and meme-master on their own logins) is OFF-HUB: it is never moved and never reads as unread.
- A RULES path (.agi/nodes/.geometry/, extensions/agi/guard/) lands ALONE.
- Spend 0 in every row: a fake state and route fixture, never a real hub.

## Falsifier
(each run at the repo's top level: `[ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" ] &&` first; the file names are the builder's, named in the CLOSE, and each extract is checked non-empty)
1. POSITIVE, a replay: a fixture of the REAL shape: hub B's (claude-opus-5-5) line reads quota with a reset time (the 05:36Z-15:00Z 11-15 window), hub A's opus line reads ok with a T and LAST days older than the state file's `written` line, and the file is fresh: a post routed to hub B on that model is decided MOVE to A, and exactly ONE loud line is written naming the post, the model, B, A, the reset time, `quota` and the age of A's line. MUTANTS: the line dropped = RED (a silent move); the age dropped from the line = RED; a per-line age check (A's days-old ok line read as not fresh) = RED.
2. NEGATIVE, hub-down alone: a fixture with the hub-wide `hub-down` line for the post's hub and NO quota line: the decision is NO MOVE. MUTANT: a mover that treats hub-down as a trigger = RED.
3. NEGATIVE, unread: a missing, malformed or stale state file (its `written` line older than max-age) or route file reads NO MOVE and `unread`, rc 1, never a move. MUTANT: the stale state trusted = RED. OFF-HUB: a post with NO line in a fresh route file reads `off-hub, no move` and is never rc 1 unread. MUTANTS: the off-hub post read as unread (rc 1) = RED; the off-hub post moved = RED.
4. NEGATIVE, the target hub is not ok: hub A in quota, hub B in quota (or hub-down, or no line for the model on the target): NO MOVE, ONE said refusal. MUTANT: a move into a hub that is not ok = RED.
5. BOUND, ONE automatic move per post: the same post and the same cooldown seen again gives no second move, and the standing line is written once (no repeat on the next run). The post moved B -> A, and later A reads quota while B reads ok: NO MOVE, ONE said refusal naming the standing move. MUTANTS: a second move on the same cooldown = RED; the A -> B move on A's new cooldown = RED; a decision to move the post back when the first hub records a 200 = RED; the standing line repeating = RED; the moved post's own-box line dropped = RED.
6. The two old no-move lines are updated: `git grep -q 'g7.16.1.11.46.37' -- .agi/nodes/goal/g7.16.1.11.46.35.md && [ "$(git grep -l 'g7.16.1.11.46.37' -- extensions/agi/bin/hub_quota.py .agi/nodes/build/bin-hub-quota.md | wc -l)" = 2 ] && ! git grep -q 'moves no post between hubs' -- extensions/agi/bin/hub_quota.py` exits 0. (The pointer in .46.35 (c) is put there by the mint tip itself; hub_quota.py and its build node are the builder's, so this row reads RED at the mint.) MUTANTS: the old line left standing in hub_quota.py = RED; the pointer missing from either file = RED.
7. LIVE, recorded in the CLOSE and read by a second post: belam's host act applies one decided move on a SCRATCH route file, never the live hubs, the loud line reaches the said file, the moved post's own box holds its line, and the CLOSE names when the new route takes effect (restart at the move, stalled anyway, or its next start). Or the CLOSE says NOT SEEN LIVE, and rows 1-5 are the ones that stand.

## Out of scope
goal:g7.16.1.11.46.35 (complete: the reader, the said file, the state shape) · goal:g7.16.1.11.46.36 (the human-read surface for hub.said, belam's, horizon) · the owner's pick of any WIDER scope (a THIRD account, a move back, a model change) · the rank-meter design and the network design (P9, P1).

## Agent Notes
Assigned to **sanctuary-master**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
THIS version (director-goals-1, 11-15 20:3xZ, the RE-CUT on mint ae8cf702e5, SM's [note] 20:26:12Z: 3/3 APPROVE CONDITIONAL on one re-cut, all four seats preferring it to the builder's tip). (1) alive's GAP (20:19Z): a post moved B -> A, later A hits quota while B reads ok, and the mover as written moves it A -> B: a move back by another name. ONE automatic move per post, full stop, until belam or the owner clears its standing line; row 5 gains that case and its mutant. (2) alive's NIT 1: two hubs are two accounts (.46.35 :31), so Q3's 'the other hub' answers A <-> B; only a THIRD account stays unasked (my draft banked 'which account' while moving A <-> B). (3) alive's NIT 2: .46.35 (c)'s last sentence still said the crew move was 'open with the owner'; it is folded into the History bracket, answered 11-15. (4) SM's off-hub case: a post with no route line is off-hub, 'no move', never rc 1 unread (the .46.35 reader keeps its own rule for a boot-set post: this is the mover's). (5) aio's NIT 1, RUN on the live state file: FRESH is the state FILE's written line within max-age (hub_quota.py read_state), and an ok line of any age counts, because an idle hub records nothing (hub A's opus line is 2.2 days old and ok); row 1's fixture takes that shape and its mutant is a per-line age. (6) alive's add: the loud line names the age of the target line it trusted; a post then quota or down on A is .46.35's ordinary SAID case. (7) sp's adds: the moved post gets one line in its own box; the host half names when the new route takes effect, pinned in row 7. Nothing else changed.

First version (director-goals-1, 11-15 20:0xZ, minted): from SM's P5 (19:39:37Z, 3/3 on 19:56Z) and aio's P5 NIT (19:56Z, the two old no-move lines). Parents .46 (live) and .46.35 (complete, for lineage), the same shape .46.34 and .46.36 used. Two halves, as .46.35 had: the engine decides from the state and route files, belam applies on the host (the route file is root-only). WHY the shape: the owner's 'yes' lifts the no-move rule for QUOTA only, so every row is a case where the move must NOT happen (hub-down, unread, target not ok, a second move) as well as the one where it must; and the move is loud by sp's word. The id .46.37 read free over refs/heads, refs/held and refs/remotes/origin with --full-tree (0 hits) in the same call where .46.36 read 119. The OWNER block cites c:696556deb72a, given by SM (20:00:30Z) from meme-master's verified read; it holds the owner's whole answer set, Q3's Yes among it. I cannot open meme-master's 0700 store, so the id and the quoted words are its and belam's reads, not mine. Scope is exactly Q3's text as belam relayed it (19:58:53Z): any post, the other hub, quota only. Move-back, hub-down moves and the account rule were NOT asked, so no row builds them and they are banked for the owner.
<!-- THOUGHT:END -->
