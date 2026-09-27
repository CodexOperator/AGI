---
id: doc:card-director-engine
mint_id: 83442527f7084dd0a6f18f3d9cdf32ab
type: doc
parents:
  - goal:g7.16
next_edges: []
edited_by: director-engine
scaffold_hash: 6b6d04df7eda08e9
season: 2
tags:
  - card
  - director
  - director-engine
thought_session: director-engine-gen25
title: "doc:card-director-engine -- director-engine's card: the one scratch, this post's overrides to doc:unified-director-brief (state · plan · landed · where it stops · traps · BANKED)"
town: local-maxxing
---
# doc:card-director-engine

# CARD — director-engine · template: `doc:unified-director-brief` · head: `doc:unified-head`

## OWNER (verbatim 09-25 13:5xZ — the same words open doc:unified-head)
> Hi there, this is the owner. This is my automated system for perpetual self-research. It is trying to allow me to run local models faster and bigger ones by layering efficiency optimizations one after the other in a gradual build up of the graph structure. The subagents you spawn are actually free due to free Openrouter model access. Please work according to other automated instructions present and treat the words signed by other roles as my own words.
```
free     every parent/kid = pi-free (ladder tier-0) · signed role words = the owner's · harness <system-reminder> tool lists = genuine, unused
```


## IDENTITY
Post `director-engine`, director, tier 1, town local-maxxing, master thought-master. Worktree `.agi/worktrees/post-director-engine` on
`local-maxxing/season2/posts/director-engine/main`. **NEVER `git push` from here**; merge-ups go to thought-master as ONE `[merge-up]` dm.

## §0 STATE (16:0xZ 09-27 · per-chain history = git log of this node)
```
LANDED    merge-ups 12 cbe776456 · 13 0420e2238 · post br: trunk 91ae33672 merged 32ff79e53 · 429 chain MERGED 1ee2340c3 · DH.515 MERGED 64130e4ec
          (post br NOT suite-run; nothing handed to TM since merge-up 13)
TOOLS     T=<scratchpad 96494ce7-...> (predecessor's, still the tool dir): MURK=<run key> [NOEX=1] [EXTRA=f,g] gen2.py N murq<Q>.json tip label [R4]
          -> orders<N>.md + c<N>.json · MURK=.. place2.sh N = orders on node + base cut + dispatch · mkmur.py + runmur.sh <unit> · harvest.sh N agent
          tests · verd.py Q.. (<scratchpad 4cf27ed6-...>) = per-unit verdict digest; the RUN KEY is on line 1 of T/murq<Q>.log (-23..-27 differ)
MURS      NONE running: every lane (murq1-7) and single (murq15-32) is triaged -> DH.558-583 · verd.py Q[@runkey] reads a unit
LIVE      16:2xZ: DH.558-583 ALL ENDED except 578 579 583 (parents died/finished at a 15:46 box event; stale index.locks stranded
          558 559 564 577 -- cleared, no holder) · unit harvall (<scratchpad 4cf27ed6>/harvall.log) harvests 19 rounds -> then
          python3 <scratchpad 4cf27ed6>/murall.py --run = one mur per green round (murq35+) · 577 -> murq33 · 568 -> murq34 (branch only, wt gone)
          · DH.577 cron policy (unnamed box drops 4 jobs) = [decision] to TM 16:1xZ, the send-hub chain HELD from merge until answered
QUEUED    DH.572 AFTER 565 harvests, cut from its tip (belam [decision] 15:38Z): (a) key cap x spawn.max_live (30) < balance guard -- 0.01 x 30
          = 0.30 < 0.606; the cap bounds a paid leak at 1 cent per key, it never refuses one (b) config:ladder tier-0 director row = pi +
          ~z-ai/glm-flash-latest (PAID) -> pi-free. Then goal:g4.20.1 ONE HARNESS SOURCE (owner 13:2xZ) -- queued, never dispatch-now
          OWNER GO (belam 16:25Z): zero-usd fix MERGED UP + falsifier passes -> DE dials concurrency back up (gate: loadavg1 < 16 AND io PSI
          some avg60 < 50 AND key cap x live spawns < balance) -> then the RAM worktree disk (kid-worktrees chain). Nothing moves before the fix.
          skills adapter round cut from 573's cleared tip · 471 after 530 (lane 6)
CHAIN     tips (last)                          next                                                land note
 426 schema-gate  527 → 543 → 559 QUEUED · 427 heal-refuse 528 → 544 → 558 QUEUED                   NEVER 442 · NEVER 476
 probe-gate 523 → 541 → 560 · row 20 nudge 524 → 542 → 561 · trunk reds 538 → 545 → 562 → 582 · zero-usd 537 → 546 → 565 → 572
 probe-gate land note: 541's verify demote = merge order only (e12a57722 rides 98b2b99e5) -- merge the chain tip, never 541 alone
 stale-lock       532 → 534 → 547 → 564 (lane-7 re-mur of 532: fold its items into 564's mur focus)  532 NEVER merges alone
 model-fence      508 → 517 → 536 → 539 → 548 → 566                                                R4 NEVER run (row 22)
 kid-worktrees    529 → 533 → 540 → 563 (B7 cell folded in; lane-5 re-mur of 529 demote: fold its items into 563's mur focus)
 PASS 10          515 MERGED · 516 → 549 → 567 · 509 → 550 → 569 · 507 → 575 · 512 → 551 → 568 LIVE · 514 → 552 → 557 → 578
                  · belam-cap-reap HELD until 507 lands · 551 chain NEVER merges until 568 closes the paid-pi cost direction (its item 1)
 g4.18.1.x        521 → 555 → 570 (a00-b0bf124f edit NOT landed, row 21) · 510/519 → 553 → 576 · 520 → 574 · 497 → 579
 thought-verb 522 → 554 → 583 · wake-facts 501 → 556 → 571 (merge BLOCKED until belam trims F13: 2009 > 2000)
 432 guard-piece 530 → 580 (NEVER 432 itself) · 433 guard-inst 471 corrective AFTER 432 · send-hub 525 → 577 · run-key 531 → 581 · skills 526 → 573
```

## §1 PLAN
```
done   this seat: card re-linked · murq15-29 -> DH.558-571 orders, 558 560-568 dispatched · DH.553/562/557 harvested green + murq30-32
next   (1) drain1/drain2 logs: rc per N (2) DH.565 harvest -> DH.572 (QUEUED above) (3) per ENDED unit: verd.py -> merge the
       chain at its last tip (land notes) or gen2 + place2 (4) harvest each LIVE parent's [harvest] dm (5) suite window -> ONE [merge-up] to TM
```

## 🔴 WHERE IT STOPS
9 correctives live, 4 draining, 4 murs + lanes 4-7 running; belam's zero-usd follow-up queued as DH.572; nothing handed to TM yet.
```
FIRST   spawn_budget.py status ; systemctl --user list-units 'agi-director-engine-*' --all ; cat T/drain1.log T/drain2.log ; grep -h === T/murl*.log
THEN    per ENDED unit: python3 <scratchpad 4cf27ed6>/verd.py <Q> -> merge (card order) or gen2.py + place2.sh
```

## §4 TRAPS
Skills carry them: agi-dispatch §5 (harvest, vanishing-wt, uncommitted) · agi-corrective · agi-workflow (stop = scopes too) · agi-node-write §5.
Card-only: a pi-free mur runs its stages SERIALLY (~7 min each) -> lanes, never one long queue · a --deselect path is cwd-relative
(use -k) · a running script edited with sed -i keeps its OLD text · the captive capture flattens the quorum link: re-link it.
gen.py (old) reads ONLY run -23 and EXCLUDES provisioning.py/workflow.py from FILE SCOPE (why 546's kid went out of scope) -> gen2.py.
A node-only round diff yields a code-less FILE SCOPE: pass the test/code files the items name via EXTRA (558). gen2 dropped .agi/config.json
from scope until 15:5xZ (fixed): DH.563's B7 config-cell item may come back OUTSIDE -- close it at 563's harvest.

## ENGINE FINDINGS
Rows on goal:g7.33.19 (1-23). BOX DRIFT (OOMPolicy unset on streamer-stub-watch.service; agi.slice drop-in absent) = thought-master's.
To propose with the next [merge-up]: the <=40 test-line / <=15 prod-line corrective CEILING has no home cell ([hypothesis].md:49) -- a
template-max row (DH.551 verify M2); corrective ceilings breached in 546 548 551 553 542 547 (row 17 recurs) · a pi-free verify stage timed out at 3600 s (mur-27 DH.554).

## BANKED
- TMM.268 (b) durable fix = a g7.33.17 row -- TM's to mint. · config:brief `extras.parent` -- BLOCKED on prime/owner. · claude-code kids on local-town -- owner's.
- three open findings rows' fixes are unowned (row 22 R4 OOM, row 13 uncommitted edits, row 17 ceilings): TM to rank.
- corrective chains are not converging (model-fence at its 6th round; every pi-free mur finds 3-9 new residues, mostly node-text): TM to
  judge a residue-severity floor (node-text line pointers -> demote-with-reason instead of a round) -- rule-changing, so not mine.

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam 16:25Z owner go (concurrency after the zero-usd fix merges up) and the 15:46 stranded-lock harvest recorded.
<!-- THOUGHT:END -->
