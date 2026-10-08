---
id: doc:l5-plan
mint_id: 91459ad346de4a27852b37dcf4f20f50
type: doc
parents:
  - goal:g1.20
next_edges: []
edited_by: belam
scaffold_hash: da94842de9d92f69
season: 2
tags:
  - doc
  - l5
  - plan
thought_session: dissolve-legacy-2026-09-19
title: "L5 plan — the tidy pass: branch deletes, post session-name updates, stragglers; Prime + one director"
town: core
---
<!-- BODY:BEGIN -->
# L5 — the tidy pass (owner GO 2026-09-17 13:3xZ; verbatim in doc:l5-owner-decisions; loop goal goal:g19)

A SMALL loop. Three heads in a FIXED order, then close. No new goals, no relocation, no towns woken. Scope creep is the failure mode.

## §0 Formation (owner: "a single director running several parents at a time")

```
owner ──► belam (Prime, REVIEW not work; chain restarts belam-S1-L5-I at the next Prime rotation)
            └──► director-belam (today's post sanctuary-director; the name lands in L5.02) ──► <=8 live parents (pi, ~deepseek/deepseek-v4-flash-latest), <=5 kids each
IDLE, never woken in L5: sanctuary-master · master-sensei · sensei-director (rotates ONCE in L5.02 -> director-sanctuary, then idles) · sanctuary-helper · thought-master · director-thought · stream-master
NO livestream: view-<post> sessions / livestream repoint NOT required; a missing view session is never a red (owner).
```

The director works in its own worktree (`.agi/worktrees/post-sanctuary-director`, post branch), mints one hypothesis node per round (parents: goal:g19 for the three heads; goal:g15 for every little gap found in-loop -- the standing 09-11 05:1xZ rule), dispatches parents from the worktree (`dispatch.py . L5.NN --target <node> --level small --tier parent --harness pi --branch`), reviews each round BY NAME on pi (`workflow.py run merge-up-review`), merges up by SHA (one GO at a time), and dms the Prime ONLY a `[merge-up]` numbers line + proposed g15 lines, a `[decision]`, a `[rotation]`, a `[red]` or a `[rule]`. The Prime accepts or demotes from the report + the bytes, verifies on season2/main after each landing, runs the live Prime acts below, keeps goal:g19's notes.

## §1 Order and rounds

### HEAD 1 — BRANCH DELETES (first; owner) = the reshuffle SECOND PASS
Measured at open (13:3xZ): origin refs/heads = 21; TARGET (Option B, owner GO 09-12 18:4xZ, defaults accepted 09-17) = 13:
```
master · season1/main · season2/main                                   (3 trunks; season2/main = the Prime's)
core/main · core/season2/main                                           (town pairs: <town>/main + <town>/season<m>/main)
sanctuary/main · sanctuary/season2/main
streaming-suite/main · streaming-suite/season1/main
web-app-suite/main · web-app-suite/season1/main
local-maxxing/main · local-maxxing/season1/main
```
GONE from refs/heads (12): season2/posts/{sanctuary-director,sanctuary-helper,sensei-director} (pre-v3 twins, stale 09-13) · core/season2/posts/{sanctuary-director,sanctuary-helper,sensei-director}/main (LIVE posts -> mirrored to hidden refs/agi/posts/<post>, worktree upstreams re-pointed, THEN deleted) · season2/loops/* (3) · season2/sensei/genless-templates · collaborator-branch · copilot/add-open-source-license (foreign; deleting closes the Copilot PR -- owner: delete).
Local at open: 678 branches (646 merged into season2/main), 109 dead kid worktrees `.agi/worktrees/a00-*`.

- **L5.01** (director; 1-2 parents, fixture-proven, no live ref touched by the round): (a) `cli.py branch-reshuffle --dry-run --kinds main,posts,towns,loops` plans EXACTLY today's delta -- creates only the 4 missing town branches, no-ops the 6 town branches already on origin and `master:season1/main`, treats the 3 `season2/posts/*` twins as DELETE (never a rename onto an existing v3 name), mirrors the 3 live posts to refs/agi/posts/<post> and re-points the post worktrees' upstreams, plans the 12 deletes and nothing else; (b) `--delete-old` deletes exactly the plan's 12, refuses without a fresh green stamp, leases through the SM.92 helper; (c) a post's merge-up, the dispatch behind-check (F9) and `whois` work with the post branch on the hidden ref only (no refs/heads post branch on origin); (d) `cli.py loop-prune` (dry-run default) covers BOTH loop grammars (`season2/loops/*` and legacy `loop/*@s2`), deletes only branches merged into season2/main, `git worktree prune`s dead kid worktrees, never a post worktree, never an unmerged branch, and lists every skip by name.
- **L5.01-live** (PRIME act on MAIN, after L5.01 lands): fresh stamp (suite, one runner) -> `branch-reshuffle --dry-run` (read whole) -> `--apply` -> `--delete-old` -> `git ls-remote --heads origin` == the 13 -> `loop-prune --apply` -> verify -> note on goal:g19 with the before/after counts.

### HEAD 2 — POST SESSION-NAME UPDATES (second; owner)
Staged 09-16 20:24Z and never applied: `rotate.py` defines `_apply_staged` (rotate.py:3898) and nothing calls it. Target names: **director-belam** (= sanctuary-director; owner: "not anything else") · **director-sanctuary** (= sensei-director) · director-thought already right · masters and the helper keep their names.
- **L5.02** (director; 1 parent, fixture-proven with the fake tmux): `rotate` / `rotate-self` read `seats/<old>.rename.json` BEFORE the successor spawn, re-derive every surface from branches.py + the row at that moment (the json is a plan, refused on drift), apply atomically (SM.18's function), seat the successor under the NEW name (window, --remote-control name, worktree dir, post branch, row + session_label, key/ack/bootstrap files, inbox + nudge files, dm logs + sidecars, alerts edges), write the applied surfaces into the rotation record, consume the json, refuse on a dirty tree; a missing view session is NOT a red (no livestream). Old names stay dm aliases for the season (SM.18).
- **L5.02-live** (PRIME): the point rotates on my word -> comes up as director-belam (the L5 director from then on); sensei-director rotates -> director-sanctuary, idles. Verify: `tmux list-windows -t agi-rc` names · `send.py whois` · `send.py send director-belam` lands · both `.rename.json` consumed · `config:posts` rows carry the new names.

### HEAD 3 — EVERYTHING ELSE (third; owner): the stragglers, and every little gap surfaced in-loop, fixed in-loop
The list at open: the 23 g15 hypotheses with no experiment node that survived the L4 retire pass (rows in hypothesis:a00-e1933e6a-176c0e) · SM.101 (wake-audit PENDING vs 0 = the floor) · node-count follows the MINT ID across a deprecation move (never "missing committed file" for a move) · the three rotation-audit code lines · the F23 fact fix · whatever L5.01/L5.02 surface. The director triages into waves of <=8 parents (retire + note anything already closed by landed bytes; never round a closed item); each round = one hypothesis, <=5 kids, review by name, merge-up by SHA.

### CLOSE
goal:g19 done-state holds (every claim measured on season2/main) -> COMPLETE.md L5 section as a WHOLE REPLACEMENT -> push -> the prayer. No other close step (no stream, no panic).

## §2 Gates (unchanged from L4, the paid-for ones)
review by name on pi, never the Claude Workflow tool (F29) · ONE suite runner per tree, every pytest --basetemp under /tmp · stamp before any delete · `grid.py commit --all` on season2/main only · commit + push after every action · floor `provisioning.min_account_remaining_usd` 1.6, switch accounts at the gate's refusal (doc:l4-owner-decisions :882 + 2b) · directors dm the Prime only when necessary, tagged · message bodies backtick-free · never git add -A · never `git rm` under .agi/nodes · every finding -> a g15 node fixed in-loop, never residue prose.

## §3 The director's brief (dm'd by node id; this section IS the brief)
You are the L5 single director (post sanctuary-director today; director-belam from L5.02). Read this node whole, then goal:g19 and doc:l5-owner-decisions. Work HEAD 1 -> HEAD 2 -> HEAD 3 in that order, one hypothesis per round, <=8 live parents, from your worktree, reviews by name on pi, merge-ups by SHA with a numbers-only `[merge-up]` line + one proposed g15 line per finding. Never touch HANDOFF.md, the L5 docs, goal:g19's body or briefs/. When HEAD 1's round lands, say so in the merge-up line; the Prime runs L5.01-live. Same for HEAD 2. Then the stragglers until the list is empty.
