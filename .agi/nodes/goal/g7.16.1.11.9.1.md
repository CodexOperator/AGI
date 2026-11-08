---
id: goal:g7.16.1.11.9.1
mint_id: 66fe6d0b06084e849e17c9df77d0c1d6
type: goal
parents:
  - goal:g7.16.1.11.9
next_edges: []
confidence: 0.5
goal_id: G7.16.1.11.9.1
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 2174e54183d71e3a
season: 3
seeds: []
status: active
tags:
  - viz
  - dashboard
title: "G7.16.1.11.9.1: the dashboard -- ONE graphweb export on loopback feeds four views (graph, crew, workflow cycle, comms cycle), read-only, post names and counts only, every number read back from the trunk at one sha"
town: core
---

# goal:g7.16.1.11.9.1

## Why this exists
Parent goal:g7.16.1.11.9 (the VIZ, horizon until this leaf): its Why names graphweb on loopback, its Invariant reads 'read-only, loopback only, never a key / name / address on screen', its Falsifier 2 reads 'a public listening port for the viz: zero'. The owner's 23:0xZ 11-07 ask (below) names its first deliverable: one dashboard of MULTIPLE VIEWS, shown 'when it's ready'. The council placed it here 3/3 (alive [decision] 23:24:04Z 11-07: sp [view] 23:08:01Z, aio [word] 23:11:49Z with its HOME and TERMS A and B, alive [view] 23:09:03Z + [correction] 23:09:30Z), read at trunk 39378cb4ba. goal:g2.17 stays graphweb's lineage (built under it 09-11; back to horizon at its 09-04 review, split into g2.20-g2.22): one live viz line, not two (the owner's 20:42:45Z 'reuse existing channels').

## Target end-state
- ONE EXPORT, ONE SERVER: graphweb (extensions/agi/bin/graphweb.py, 1444 lines at 39378cb4ba; today /graph.json, /live.json, /commands.json and POST /propose, which runs nothing) is the only reader of the repo and the box; every view reads only its JSON; nothing in the page opens the repo, refs or a box; the export names its trunk sha and built_at; a page published off this box is fed from the same export, never a second one.
- FOUR VIEWS on that one server: (1) graph = /graph.json; (2) crew = /live.json + the post tree by level and master, from config:posts; (3) workflow cycle = turn end -> lane tip -> gate -> [merge-up] -> land -> wrap -> re-extract, its clocks READ from config:crons (crons.md); (4) comms cycle = the box MATRIX over config:posts rows, per-edge counts from refs/box/<from>/<to> over a stated window. Views 3 and 4 are new reads on the SAME server.
- 'hunny screen' is the SCREEN the owner names (belam asked); until then the page is a private one the owner opens on any screen.

## Invariants
- PRIVACY: on screen, post names and counts only; never a person's name, a uid, a home path, a host name or address, a key, a message body or subject. The export passes anonymize.scan beside a control that flags.
- READ-ONLY, LOOPBACK ONLY, NO NEW DAEMON: no write to the tracked tree, refs or a box; graphweb's one write is its own gitignored layout cache (.agi/sessions/graphweb-layout.json: positions, never a number on screen); graphweb binds 127.0.0.1 only; `graphweb serve` stays the one process; the page loads nothing from beyond its own server (no CDN script, module or font): a library it needs is a pinned copy graphweb serves.
- A view that read NOTHING says so in words; it never draws an empty picture as a fact.
- Every number on screen reads back from the trunk at ONE sha.

## Falsifier
1. `sh extensions/agi/tests/viz-views.t.sh` exits 0 against a fixture AND the live trunk at one sha: nodes == the verify count; edges == the box matrix; each per-edge count == `git rev-list --count` of refs/box/<from>/<to> over the window; crew rows == config:posts rows; each clock == its crons.md cell; the export carries the trunk sha and built_at; anonymize.scan(export) == [] with a control that flags in the same call; an empty source prints its view's 'read nothing' line. Mutants, each RED: a hardcoded clock; a box subject or body on an edge (a leaked body); an edge count off by one; a view fed by a second reader; an empty source whose view draws nothing and prints NO 'read nothing' line; an export naming sha S while one view reads another rev (a fixture whose S and its child differ in config:posts rows: the crew count must be S's).
2. Negative, four rows, each with its RED control: a public listening port for the viz: zero (`ss -ltn` lists graphweb's port on 127.0.0.1 only; mutant: --host 0.0.0.0 reads RED); (a) each URL the page loads (fetch, dynamic and static import, export ... from, script src, link href, CSS url( and @import, new Worker / SharedWorker / WebSocket / EventSource; an a href is navigation and stays out) is one of graphweb's own endpoints, each site printed; a protocol-relative //host is not relative (mutants: a font stylesheet by link, a CSS @import url(//...), a new Worker("//cdn..."), a static import from //cdn, each RED); (b) the lines graphweb gains since this build's parent 32063f957b (pinned in full and printed, never HEAD~1, so a later run is not a vacuous pass; mutant: a 2-commit fixture whose first commit adds a write and whose second touches nothing reads RED at the second) hold no write (no open() in w or a mode, no update-ref, commit-tree, write-tree, hash-object -w or push; mutant: one added reads RED); (c) `git grep -n -E '(https?|wss?)://|["'\''(=]//[A-Za-z0-9]' -- extensions/agi/web/graph/` prints 0, a second net under (a) that also catches the protocol-relative spelling (mutants: one https:// URL, a //fonts link, a //unpkg THREE_URL, each reads 1).

## Out of scope
goal:g7.16.1.11.9's other parts (the boot matrix expansion, the matrix-op shell renderer, the map v0, the SPIDER viz, the sanctuary viz) · goal:g2.17 (lineage only) · goal:g2.20 goal:g2.21 goal:g2.22 · a page published OFF this box (it reuses this export; its own leaf if it comes) · the BUILD of this leaf (a later, separate cut by the same post)

## OWNER 2026-11-07 20:42:45Z + 23:0xZ, and 2026-10-01 06:1xZ, verbatim (owner chunk c:533e2dda8d8f for 23:0xZ (t 23:02:36.610Z, belam's relay 15:07Z 11-08) and c:be72d519c116 for 20:42:45Z; 10-01 06:1xZ from before the store, quoted from goal:g7.16.1.11, grandfathered)
23:0xZ 11-07: "Can we put the visual dashboard stuff up on hunny screen when it's ready so I can see the graph more and visualize how the crew is arranged and how they work as far as workflow cycle and comms cycle. Multiple views would likely work best."
20:42:45Z 11-07: "we always wanna reuse existing channels and remix or swirl or rotate them in new unique ways. Less complexity is always better." · "extract facts about the system, visualize its structure, maybe start implementing some more advancaed visualization systems for season 5 depending on how well we can get through season 3,4."
10-01 06:1xZ (goal:g7.16.1.11): "Let’s start graphweb but soon as possible  could we make it simpler? Just a shell piped into the web that renders everything in-shell? It’ll need a redesign already anyway since it won’t be able to follow the new engine I don’t think. But the new will be even better. Could just draw using existing git graph features to show all branches including local and worktrees as they pop up and get added. Colors could value what stage the node is in. Like just starting the write, writing, committing, etc. just piggy back of post wrapper tracking and system traces and git graph. Everything is already a git graph anyway just use built in graph render tools don’t reinvent the wheel. Or lightweight packages others made"
On timing (goal:g7.16.1.11.9's OWNER block, 06:5xZ): "do all other parts first before doing viz stuff."

## Agent Notes
Assigned to **director-general-2**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-2 11-08 v3 (the BUILD's first touch, RE-CUT 1; alive [decision] 16:21:40Z 11-08, RETURN 3/3: sp 16:04:27Z, alive 16:06:22Z, all-is-one 16:20:21Z): Falsifier 2's rows as minted could not read RED on spellings of the case Invariant 2 names, the council's own terms at the mint, not a builder's slip: (a) read fetch / import( / src= only, so a font stylesheet by link href, a CSS @import url(//...), a new Worker("//...") and a static import from //host each read 0 bad; (b) diffed graphweb against HEAD~1, so any run after this build read 0 added lines and passed on nothing; (c)'s (https?|wss?):// had a control of the pattern, never of the case, so every protocol-relative //host load read 0. So T1: (a) resolves every load site (link href, url(, @import, Worker / SharedWorker / WebSocket / EventSource, static import / export ... from; an a href is navigation and stays out), each with a RED mutant; T2: (b)'s base is pinned to 32063f957b, printed, with a 2-commit fixture mutant; T4: (c) takes the widened ERE, a second net under (a). T3: Invariant 2's 'no write anywhere' becomes 'no write to the tracked tree, refs or a box; graphweb's one write is its own gitignored layout cache', because graphweb's OLD _save_persisted_layout writes .agi/sessions/graphweb-layout.json (.gitignore :109), not a line this build adds. Carried from v2: the OWNER heading gains the 23:0xZ chunk c:533e2dda8d8f (belam 15:07Z 11-08); Invariant 2 gains aio's clause because app.js :26 + :693 imported three.js from unpkg.com; Falsifier 1 gains sp's two mutants (an empty view with no 'read nothing' line; an export naming one sha while a view reads another). The builder's call on the library: a pinned three@0.160.0 copy (npm integrity matched) under extensions/agi/web/vendor/three/, served by graphweb at a relative path, outside web/graph/ so (c) reads the page's own files only (the library carries two non-load URL strings, a doc link and the XHTML namespace). Residues placed 3/3: the working-tree stamp is a term for the next touch; the cold graph build is a cost; the DOM views are unrendered here (the owner's eyes are their test); the lane file has no build node.
<!-- THOUGHT:END -->
