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

## §0 STATE (17:0xZ 09-27 · per-chain history = git log of this node)
```
LANDED    merge-ups 12 cbe776456 · 13 0420e2238 · post br: trunk 91ae33672 merged 32ff79e53 · 429 chain MERGED 1ee2340c3 · DH.515 MERGED 64130e4ec
          (post br NOT suite-run; nothing handed to TM since merge-up 13)
TOOLS     T=<scratchpad 96494ce7-...>: MURK=<run key> [NOEX=1] [EXTRA=f,g] gen2.py N murq<Q>.json tip label [R4] -> orders<N>.md · place2.sh N
          (orders on node + base cut + dispatch) · mkmur.py/runmur.sh · harvest.sh N agent tests      D=<scratchpad 4cf27ed6-...>: verd.py Q[@key]
          (verdict digest) · harvest-all.sh N.. (stale-lock clear + harvest) · murall.py --run (one mur per green harvall round) · watch.sh
MURS      running murq36 38 39 43 45 47(re-run 4G) 51 52 54 55 56 (key map: T/murq<Q>.json) · every ENDED unit is triaged into 584-596
LIVE      parents 572 584 585 586 587 588 (spawn_budget.py) · drainers (WAITFOR chain, arm-cell): drainq1 589 590 591 · drainq2 594 592 ·
          drainq3 596 595 (T/drainq<N>.log) · 565's 2 small residues FOLD into 572's next corrective (572 is cut from 565's tip)
GATE      OWNER GO (belam 16:25Z, TMM.300): step values.local_maxxing.de_live_parents.arm up ONE arm (10 -> 15) only while loadavg1 < 16 AND io
          PSI some avg60 < 50 AND key cap x live spawns < balance; re-read at each step, step back on any fail. 17:0xZ: load 23.5 = HOLD.
          Then the RAM worktree disk (kid-worktrees chain). Drainers hardcode -lt 10: a new drainer reads the cell + the gates
QUEUED    goal:g4.20.1 ONE HARNESS SOURCE (owner 13:2xZ) -- after 572, never dispatch-now · skills adapter round from 573's cleared tip · 471 after 580
DECISION  sent TM 16:1xZ: DH.577 cron policy (AGI_BOX unset -> the fail-closed gate drops mail_poll maint_gc prime_merge memory_alarm) --
          send-hub chain HELD from merge until answered
CHAIN     tips (last)                                                                               land note
 426 schema-gate 527 → 543 → 559 murq36 · 427 heal-refuse 528 → 544 → 558 → 592                                  NEVER 442 · NEVER 476
 probe-gate 523 → 541 → 560 → 589 (541 demote = merge order: e12a57722 rides the tip) · row 20 nudge 524 → 542 → 561 murq38
 trunk reds 538 → 545 → 562 → 582 murq52 · zero-usd 537 → 546 → 565 → 572 LIVE
 stale-lock 532 → 534 → 547 → 564 → 594 (532 lane re-mur folded into 564's mur)                             532 NEVER merges alone
 model-fence 508 → 517 → 536 → 539 → 548 → 566 → 590                                                    R4 NEVER run (row 22)
 kid-worktrees 529 → 533 → 540 → 563 murq39 (529 lane re-mur folded into 563's mur; B7 config cell maybe OUTSIDE)
 PASS 10 515 MERGED · 516 → 549 → 567 → 584 (wires pi_adapter) · 509 → 550 → 569 murq43 · 507 → 575 → 596 · 512 → 551 → 568 → 585 (round-mur.json STILL paid pi: 585 item 0) · 514 → 552 → 557 → 578 murq55
         · belam-cap-reap HELD until 507 lands
 g4.18.1.x 521 → 555 → 570 → 587 · 510/519 → 553 → 576 → 588 · 520 → 574 murq47 · 497 → 579 murq54
 thought-verb 522 → 554 → 583 murq56 · wake-facts 501 → 556 → 571 murq45 (merge BLOCKED until belam trims F13: 2009 > 2000)
 guard-piece 530 → 580 → 591 (NEVER 432 itself) · guard-inst 471 AFTER 432 · send-hub 525 → 577 → 586 (HELD: decision) · run-key 531 → 581 murq51 · skills 526 → 573 → 595
```

## §1 PLAN
```
done   this seat: card re-linked · murq15-32 + lanes 1-7 triaged -> DH.558-583 · 26 correctives dispatched · 21 harvested green (5 known
       old-base/F13 reds) + murred · stale locks cleared (558 559 564 577) · 572 dispatched on belam's decision
next   (1) per ENDED mur: verd.py Q -> clean = merge the chain at its last tip (land notes, --no-ff, card order) · residue = gen2 + place2
       (2) harvest each ended parent: D/harvest-all.sh N.. > D/harvallN.log, then HLOG=.. Q0=<next> D/murall.py --run (3) clean chains merged -> suite window -> ONE [merge-up] to TM (4) gate re-read -> arm step
```

## 🔴 WHERE IT STOPS
11 murs + 6 parents running, 7 correctives queued; nothing merged this seat yet; cron-policy decision out to TM.
```
FIRST   spawn_budget.py status ; systemctl --user list-units 'agi-director-engine-*' --all ; python3 D/verd.py <Q> per ended murq
THEN    clean -> git merge --no-ff <loop branch> (card order) · residue -> MURK=.. T/gen2.py + T/place2.sh (a drainer when slots are full)
```

## §4 TRAPS
Skills: agi-dispatch §5 · agi-corrective · agi-workflow · agi-node-write §5. Card-only: pi-free mur stages are SERIAL (~7 min, verify can time
out at 3600 s) · a running script edited with sed -i keeps its OLD text · the captive capture flattens the quorum link: re-link it ·
gen.py (old) reads only run -23 and drops workflow/provisioning from scope -> gen2.py · a node-only diff -> pass code files via EXTRA ·
parents end WITHOUT a harvest dm: reconcile by spawn_budget + the parent worktree's done commit · a stale .git/worktrees/<a>/index.lock
(15:46 box event) silently refuses every kid commit: /proc fd+cwd scan, then rm · place2's node commit can lose a race to a card commit
(561's orders landed late): git status after each placement batch · harvest.sh's pass/fail grep matches 'failed' inside a node slug · two drainers that each wait for 'any other' deadlock: drainqw.sh + WAITFOR.

## ENGINE FINDINGS
Rows on goal:g7.33.19 (1-23). BOX DRIFT (OOMPolicy unset on streamer-stub-watch.service; agi.slice drop-in absent) = thought-master's.
To propose with the next [merge-up]: corrective CEILING has no home cell ([hypothesis].md:49; DH.551 verify M2) · ceilings breached in
546 548 551 553 542 547 (row 17) · pi-free verify timeout 3600 s (DH.554) · parents exit without a harvest dm · stale index.lock strands
kid commits (the stale-lock chain's own mechanism, live).

## BANKED
- TMM.268 (b) durable fix = a g7.33.17 row -- TM's to mint. · config:brief `extras.parent` -- BLOCKED on prime/owner. · claude-code kids on local-town -- owner's.
- three open findings rows' fixes are unowned (row 22 R4 OOM, row 13 uncommitted edits, row 17 ceilings): TM to rank.
- corrective chains are not converging (model-fence at its 6th round; every pi-free mur finds 3-9 new residues, mostly node-text): TM to
  judge a residue-severity floor (node-text line pointers -> demote-with-reason instead of a round) -- rule-changing, so not mine.

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
17:0xZ: second wave triaged (584-596), 578/579/583 harvested and murred; 565 residues fold into 572.
<!-- THOUGHT:END -->
