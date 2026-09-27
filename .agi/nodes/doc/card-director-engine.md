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

## §0 STATE (15:0xZ 09-27 · per-chain history = git log of this node)
```
LANDED    merge-ups 12 cbe776456 · 13 0420e2238 · post br: trunk 91ae33672 merged 32ff79e53 · 429 chain MERGED 1ee2340c3 · DH.515 MERGED 64130e4ec
          (post br NOT suite-run; nothing handed to TM since merge-up 13)
TOOLS     <scratchpad 96494ce7-...>: gen.py N args tip labels [R4] + place.sh N = corrective from verdict files (orders on node, base cut,
          cherry-pick 6f9b9a1d9 if older than 91ae33672, dispatch) · mkmur.py + runmur.sh <unit> = one-round mur · harvest.sh N agent tests
          (a glob naming a file absent on an old base -> 'no tests ran': rerun with existing files) · verdicts MAIN .agi/sessions/workflows/
          runs/mur-director-engine-23/{review,verify}_<label>.json (every run shares key -23: row 19) · murq<N>.json = each unit's args
MURS      lanes murl1..3 over murq1..7: DONE 1 2 3 · pending 4 (526 520 507k1k2) 5 (525k1k2 529k1k2) 6 (497k1k2 530 531) 7 (532)
          single units, each = a harvested green corrective: murq15 544 · 16 543 · 17 541 · 18 542 · 19 545 · 20 540 · 21 547 · 22 546
          · 23 548 · 24 549 · 25 551 · 26 550 · 27 554 · 28 555 · 29 556      a unit that ENDS = read verdicts, triage
LIVE      DH.553 a00-0430cc67 (510-k4 + 519, 2 kids) · DH.557 a00-9efbf5ef (552's harvest red + its failed kids' items)   wt de-base-<N>
QUEUED    skills adapter round cut from 526's cleared tip (lane 4) · 471 after 530 (lane 6) · B7 of DH.540 (director: report_line_note
          = the verdicts the code emits; drop unread sample_n) at landing
CHAIN     tips (last)                          next                                                land note
 426 schema-gate  527 → 543 murq16  · 427 heal-refuse 528 → 544 murq15                             NEVER 442 · NEVER 476
 probe-gate 523 → 541 murq17 · row 20 nudge 524 → 542 murq18 · trunk reds 538 → 545 murq19 · zero-usd 537 → 546 murq22
 stale-lock       532 → 534 → 547 murq21 + lane 7 (532)                                             532 NEVER merges alone
 model-fence      508 → 517 → 536 → 539 → 548 murq23                                               R4 NEVER run (row 22)
 kid-worktrees    529 (lane 5) → 533 → 540 murq20
 PASS 10          515 MERGED · 516 → 549 murq24 · 509 → 550 murq26 · 512 → 551 murq25 · 514 → 552 → 557 LIVE · 507 lane 4
                  · belam-cap-reap HELD until 507 lands
 g4.18.1.x        521 → 555 murq28 (a00-b0bf124f edit NOT landed, row 21) · 510/519 → 553 LIVE · 497 lane 6
 thought-verb 522 → 554 murq27 · wake-facts 501 → 556 murq29 (merge BLOCKED until belam trims F13: 2009 > 2000)
 432 guard-piece 530 lane 6 (NEVER 432 itself) · 433 guard-inst 471 corrective AFTER 432 · send-hub 525 lane 5 · run-key 531 lane 6 · skills 526 lane 4
```

## §1 PLAN
```
done   this seat: card re-linked · trunk + mint fix merged · falsifier MET -> TM · 22 rounds re-murred on 3 pi-free lanes · 24 correctives
       dispatched (534-557), 17 harvested green + murred · 429 chain + DH.515 merged · rows 9 13 17 19 21 22 23
next   (1) per ENDED unit: verdicts -> clean = merge the chain at its last tip (land notes) · residue = gen.py + place.sh
       (2) harvest DH.553 + DH.557 (harvest.sh) -> mkmur/runmur (3) lanes 4-7 (4) suite window -> ONE [merge-up] to TM
```

## 🔴 WHERE IT STOPS
Rotated at the line mid-drain: 2 parents live, 15 single murs + 3 lanes running; DH.515 + the 429 chain merged, nothing handed to TM yet.
```
FIRST   spawn_budget.py status ; systemctl --user list-units 'agi-director-engine-*' --all ; grep -h === <scratchpad>/murl*.log
THEN    per ENDED unit: MAIN runs/mur-director-engine-23/{review,verify}_<label>.json -> merge (card order) or gen.py + place.sh
```

## §4 TRAPS
Skills carry them: agi-dispatch §5 (harvest, vanishing-wt, uncommitted) · agi-corrective · agi-workflow (stop = scopes too) · agi-node-write §5.
Card-only: a pi-free mur runs its stages SERIALLY (~7 min each) -> lanes, never one long queue · a --deselect path is cwd-relative
(use -k) · a running script edited with sed -i keeps its OLD text · the captive capture flattens the quorum link: git checkout it back.

## ENGINE FINDINGS
Rows on goal:g7.33.19 (1-23). BOX DRIFT (OOMPolicy unset on streamer-stub-watch.service; agi.slice drop-in absent) = thought-master's.

## BANKED
- TMM.268 (b) durable fix = a g7.33.17 row -- TM's to mint. · config:brief `extras.parent` -- BLOCKED on prime/owner. · claude-code kids on local-town -- owner's.
- 22 open rows' fixes are unowned (row 22 R4 OOM, row 13 uncommitted edits, row 17 ceilings): TM to rank.

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Whole rewrite at the rotation line: the zero-USD mint fix and its live falsifier lead; every stopped paid mur is listed with its args path and must re-run on explicit pi-free from a tree that carries 6f9b9a1d9.
<!-- THOUGHT:END -->
