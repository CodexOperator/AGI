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

## §0 STATE (22:1xZ 09-27 · this seat woke 20:33Z · per-chain history = git log of this node)
```
LANDED    merge-ups 12 cbe776456 · 13 0420e2238 · post br: 429 chain 1ee2340c3 · DH.515 64130e4ec · THIS SEAT: 427 heal-refuse c2f528ed8
          (heal+cli+dispatch+zero-usd = 389 passed 0 failed) · skills eb3369efe (285 passed 0 failed) · nothing handed to TM since merge-up 13 ·
          01fc645d6 (agi-dispatch §5 sweep row) rides the SAME merge-up as the kid-worktrees chain, never without it
TOOLS     T=<scratchpad 96494ce7-...>: MURK=<key> [NOEX=1] [EXTRA=f,g] gen2.py N murq<Q>.json tip label [R4] -> orders<N>.md (check TESTS/FILE
          SCOPE: empty when the diff has no code) · place2.sh N · drainqg.sh N:K.. (TMM.306-gated queue) · redispatch.sh · mkmur.py + runmur.sh
          D=<scratchpad 4cf27ed6-...>: verd.py Q · harvest-all.sh N.. > D/harvallN.log (chain units with a while-is-active wait)
GATE      TMM.306 (TM 21:59Z): NO parent slot refilled until load1 < 16 AND io PSI avg60 < 50 on two reads 5 min apart, then ONE step at a time
          (drainqg1 enforces it); stop nothing live · first freed slot = DH.650 RAM round (repo half) · arm 10 unchanged
MURS      running murq97 99 103-109 = DH.627 614+631 633 632 634 620 624 635 637 · next murq 110 · next DH 651
LIVE      parents 621 638-646 (spawn_budget.py) · drainqg1: 650 647 648 649 (gated) · harvall26 = 640 (read D/harvall26.log, then mur)
DECISION  out to TM: DH.577 cron policy (send-hub chain HELD from merge) · DE.1 22:0xZ: who mounts the tmpfs (off-repo) · wake-facts MAJOR
CHAIN     last round (→ = corrective, mN = murq N running)                                           land note
 schema-gate 527 → 543 → 559 → 597 → 644 · heal-refuse 528 → 544 → 558 → 592 MERGED c2f528ed8     NEVER 442 · NEVER 476
 probe-gate 523 → 541 → 560 → 589 → 626 → 641 · row 20 nudge 524 → 542 → 561 → 602 → 637 m109
 trunk reds 538 → 545 → 562 → 582 → 606 → 623 → 646 · zero-usd 537 → 546 → 565 → 572 → 608 → 638 (638 re-applies the ladder revert)
 stale-lock 532 → 534 → 547 → 564 → 594 → 627 m97                                                   532 NEVER merges alone
 model-fence 508 → … → 590 → 613 → 633 m103                                                         R4 NEVER run (row 22)
 kid-worktrees 529 → 533 → 540 → 563 → 598 → 624 m107 → RAM round 650 (hypothesis:kid-worktrees-resolve-from-one-cell-and-can-live-in-ram)
 PASS 10 516 → … → 616 → 636 → 647 · 509 → … → 599 → 630 → 649 · 507 → … → 612 → 635 m108 (never run test_rotate_selfreap whole)
         512 → … → 585 → 614 → 631 m99 · 514 → … → 604 → 617 → 632 m104 · belam-cap-reap HELD until 507
 g4.18.1.x 521 → … → 610 → 621 LIVE · 510/519 → … → 611 → 618 → 642 · 520 → … → 605 → 625 → 640 HARV · 497 → … → 603 → 619 → 643
 thought-verb 522 → 554 → 583 → 607 → 639 · wake-facts 501 → 556 → 571 → 601 → 629 → 648 (BLOCKED: config:rotations, belam's -- DE.1)
 guard-piece 530 → 580 → 591 → 615 → 634 m105 (NEVER 432) · guard-inst 471 AFTER 432 · send-hub 525 → … → 609 → 622 → 645 (HELD)
 run-key 531 → 581 → 600 → 620 m106 · skills 526 → 573 → 595 → 628 MERGED eb3369efe
```

## §1 PLAN
```
done   this seat: 9+ harvest batches, murs 82-109, correctives 624-650, 2 chains merged (triage: notes / refuted / merge-order = demote)
next   (1) per ENDED mur: D/verd.py Q -> CLEAN (after demotes) = git merge --no-ff the chain tip, never while a place2 runs · residue = gen2
           orders -> T/drainqg.sh queue (TMM.306) (2) harvest each ended parent; land LOGGED node edits + ORDERED in-scope config only
       (3) enough chains merged -> neighbourhood run -> ONE [merge-up] to TM (+ the two banked [rule] lines)
```

## 🔴 WHERE IT STOPS
Murs 97 99 103-109 running; 650 647-649 gated on load/io (TMM.306); 640 harvested next; 2 chains merged, no merge-up sent yet.
```
FIRST   spawn_budget.py status ; systemctl --user list-units 'agi-director-engine-*' --all ; python3 D/verd.py <Q> per ended murq
THEN    clean -> git merge --no-ff <tip> -F <msgfile> · residue -> MURK=.. T/gen2.py, trim non-defects, queue on T/drainqg.sh
```

## §4 TRAPS
Skills: agi-dispatch §5 · agi-corrective · agi-workflow · agi-node-write §5 · agi-memory-guard · agi-master-gate (TMM.304). NEXT TRUNK MERGE:
add/add on doc:draft-skills-first-turn -> TAKE THE TRUNK'S version. Card-only: pi-free murs ~7 min/stage, verify can die (review stands) ·
harvests under load flake 1 test: re-run before a corrective · `pgrep -f place2` matches your own shell: list /proc cmdlines instead ·
`git merge -F -` does not read stdin · worktrees VANISH (617 618 597 parents/kids): harvest from the branch, update-ref to fast-forward ·
done-time commits skip foreign nodes: check the KID worktree too (618) · parents end WITHOUT a harvest dm: reconcile · stale index.lock
(no holder) refuses kid commits · murall/harvest greps match 'failed' in slugs · only / fills: /tmp basetemps.

## ENGINE FINDINGS
Rows on goal:g7.33.19 (1-23). Propose with the next [merge-up]: CEILING has no home cell ([hypothesis].md:49) · ceilings breached (row 17;
DH.599 +57, DH.622 +58 test) · pi-free verify 3600 s timeout · parents exit without a harvest dm · stale index.lock · parents strand non-node
edits · `write.py <id> 'thought -'` writes a literal '-' (DH.613 M1, DH.622) · done-time commit skips foreign nodes (cli.py:2443) · kid
brief forbids git while orders demand a commit (brief.py:1488) · write_guard misses a raw python splice · plan_move renames the body-linked
file on a link-only row (write.py:2322) + replace_payload never creates (node_writer.py:643) · refusals say 'pass --force', CLI has none
(write.py:2504-2535 vs :448) · season.py:1639 nested-heading reader trap · worktrees removed under live/unharvested rounds (597 617 618) ·
dispatch.py > 300 s at load 32 killed a parent (621).

## BANKED
- [rule] to ride the next [merge-up]: (a) skills/agi-merge-pass: every pasted measurement names its base commit + a re-runnable command
  (mur-37 DH.626, 4x in probe-gate) (b) skills/agi/SKILL.md:528 has no home for the structural-count rule (mur-38 DH.597).
- TMM.268 (b) durable fix = a g7.33.17 row -- TM's. · config:brief `extras.parent` -- prime/owner. · claude-code kids on local-town -- owner's.
- findings rows 22 13 17 unowned: TM to rank · residue-severity floor (node-text pointers -> demote) -- rule-changing, TM to judge.

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Whole rewrite at 22:1xZ, trimmed to <= 100 lines: 2 chains merged this seat (heal-refuse, skills, both after note/refuted/merge-order demotes); TMM.306 load/io gate now fronts every dispatch (drainqg.sh); the RAM round DH.650 carries only the repo half, the tmpfs mount is off-repo and asked of TM.
<!-- THOUGHT:END -->
