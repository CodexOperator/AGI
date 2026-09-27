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

## §0 STATE (14:2xZ 09-27 · per-chain history = git log of this node)
```
LANDED    merge-ups 12 cbe776456 · 13 0420e2238 · post br: trunk 91ae33672 (mint fix) merged 32ff79e53 · 429 chain MERGED 1ee2340c3 (242 green) · DH.515 MERGED 64130e4ec (185 green)
FALSIFIER MET (DH.533 pi-free: keys 0.01 used 0, credits 0.6063 = before) -> TM 13:3xZ
TOOLS     <scratchpad 96494ce7-...>: gen.py N args tip labels [R4] + place.sh N (corrective) · mkmur.py + runmur.sh unit (mur) · harvest.sh N agent tests (diff, lands write-log-matching dirty nodes, tests on de-h<N>) · murq<N>.json args
          · orders<N>.md + c<N>.json (generated from verdict files) · verdicts MAIN .agi/sessions/workflows/runs/mur-director-engine-23/
          · a base older than 91ae33672 needs `cherry-pick -x 6f9b9a1d9` before dispatch (else the mint refuses at 0.61)
MURS      murl1..3 = 3 LANES over batches murq1..7 (mkdir claims/b<N>; pi-free = SERIAL per stage ~7 min): 1 509k1 509k2 512 514k1 ·
          2 514k2 515 516 510k4 · 3 519 522 521 501 · 4 526 520 507k1 507k2 · 5 525k1 525k2 529k1 529k2 · 6 497k1 497k2 530 531 · 7 532
          single units: murq15 DH.544 · murq16 DH.543 · murq17 DH.541 · murq18 DH.542 · murq19 DH.545 · murq20 DH.540 · murq21 DH.547 · murq22 DH.546   (a unit that ENDS = read its verdicts, triage)
LIVE      DH.549 a00-60e5d07e (516) · DH.548 a00-366fb511   (wt de-base-<N>)
QUEUED    skills adapter round (hypothesis:skills-load-per-harness-per-tier-from-one-config-cell) cut from 526's cleared tip · 471 after 530
CHAIN     tips (last)                 state                                                          land note
 426 schema-gate  527 → 543           harvested 117b61216 (4 nodes landed, 153p) -> murq16           NEVER 442
 427 heal-refuse  528 → 544           harvested feeff05ac (3 nodes landed, 101p) -> murq15           NEVER 476
 probe-gate       523 → 541           harvested 98b2b99e5 (150p) -> murq17
 row 20 nudge     524 → 542           harvested 7502fa786 (470p; send.py net 38 vs 15, row 17) -> murq18
 trunk reds       538 → 545           harvested e4f039c8d (184p, 2 nodes landed) -> murq19
 zero-usd         537 → 546           DH.546 harvested 87995d360 (454p; provisioning.py touched, named by the residue) -> murq22
 stale-lock       532 → 534 → 547     DH.547 harvested 62b036f4d (291p) -> murq21; 532 review in lane 7; 532 NEVER merges alone
 model-fence      508 → 517 → 536 → 539 → 548   mur-23 508 demote + 539 AWR (verify died: memory-cap, R4) -> DH.548 LIVE
 kid-worktrees    529 → 533 → 540     529 lane 5 · DH.540 harvested 357c4b4f2 (287p; parent falsified A1/A2/A4, regenerable set is a LITERAL
                                      -> config_max; B7 note/sample_n = director at landing) -> murq20
 432 guard-piece  530                 lane 6                                                         NEVER 432 itself
 433 guard-inst   471                 corrective AFTER 432 lands (mur-17 k1 unstructured, k3 AWR)
 g4.18.1.1/.3/.4  521 · 519 · 497     lane 3 · 519 lane 3, 510-k4 DEMOTE: corrective cut from 519's tip AFTER 519's verdict · lane 6; 521 item 4 UNLANDABLE (row 21)
 send-hub box     525                 lane 5 (TMM.289 cleared)
 thought-verb     522                 lane 3
 wake-facts       501                 lane 3; BLOCKED: trunk region 2009 > 2000 until belam trims F13
 PASS 10          515 MERGED · 516 AWR -> DH.549 LIVE · 514-k2 AWR: HOLD for 514-k1 (lane 1) then ONE corrective · 509 512 lane 1
                  · 507 reap-chain lane 4 · belam-cap-reap HELD until 507 lands
 run-key          531                 lane 6 · skills 526 lane 4
```

## §1 PLAN
```
done   wake: card re-linked 0c20cadf2 · trunk merged · 22 rounds re-murred on pi-free · DH.534 + DH.536 dispatched (535 OOM-died, re-fenced) · 429 residue closed
next   (1) read murq verdicts per batch -> triage (skill agi-corrective) (2) harvest 533/534/535 (3) merge cleared chains in card order
       (4) credits-after for DH.533 -> TM (5) suite window -> ONE [merge-up]
```

## 🔴 WHERE IT STOPS
Murs draining in unit murq; three parents live; nothing merged since 511.
```
FIRST   systemctl --user list-units 'agi-director-engine-*' ; grep -h === <scratchpad>/murl*.log ; spawn_budget.py status
THEN    verdicts: /data/work/agi/.agi/sessions/workflows/runs/mur-director-engine-2*/{review,verify}_<label>.json
```

## §4 TRAPS
Skills carry them: agi-dispatch §5 (harvest, vanishing-wt) · agi-corrective (triage, orders ON the node, pi-free) · agi-workflow (stop = scopes too) · agi-node-write §5.
Card-only: a clean round worktree is PRUNED while you use it -> land its edits first, test on git worktree add --detach de-h<N> · stale index.locks recur
(row 18): check /proc cwd+fd holders, then rm · write.py sub is literal (no backslash-n, no empty replacement).
A running bash script edited in place: sed -i swaps the inode, so the running loop keeps the OLD text -- add a batch as its own unit.

## ENGINE FINDINGS
Rows on goal:g7.33.19 (1-22). BOX DRIFT (OOMPolicy unset on streamer-stub-watch.service; agi.slice drop-in absent) = thought-master's.

## BANKED
- TMM.268 (b) durable fix = a g7.33.17 row -- TM's to mint. · config:brief `extras.parent` -- BLOCKED on prime/owner. · claude-code kids on local-town -- owner's.

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Whole rewrite at the rotation line: the zero-USD mint fix and its live falsifier lead; every stopped paid mur is listed with its args path and must re-run on explicit pi-free from a tree that carries 6f9b9a1d9.
<!-- THOUGHT:END -->
