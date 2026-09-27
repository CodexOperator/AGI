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

## §0 STATE (14:0xZ 09-27 · per-chain history = git log of this node)
```
LANDED    merge-ups 12 cbe776456 · 13 0420e2238 · post br: trunk 91ae33672 (mint fix) merged 32ff79e53 · 429 chain MERGED 1ee2340c3 (242 green)
FALSIFIER MET (DH.533 pi-free: keys 0.01 used 0, credits 0.6063 = before) -> TM 13:3xZ
MURS      units agi-director-engine-<unit>; args + logs <scratchpad 96494ce7-...>/<unit>.{json,log}; verdicts MAIN runs/<key>/{review,verify}_<label>.json
          murl1..3 = 3 LANES claiming batches murq1..7 (mkdir claims/b<N>; a pi-free run is SERIAL per stage ~7 min), key mur-23:
            1 509k1 509k2 512 514k1 · 2 514k2 515 516 510k4 · 3 519 522 521 501 · 4 526 520 507k1 507k2 · 5 525k1 525k2 529k1 529k2
            6 497k1 497k2 530 531 · 7 532      (510k1-k3 cleared earlier, mur-18)
          murq11 DH.538 · murq12 DH.508-k1 + DH.539-k1 · murq13 DH.537 · murq14 DH.534   (all harvested green; numbers in each round's focus)
LIVE      DH.540 a00-c6a30652 (533 corrective) · DH.541-544 (the mur-20 correctives; bases = loop tip + cherry-pick 6f9b9a1d9,
          which the node BASE lines omit -- the --orders files in the scratchpad carry it); wt de-base-<N>
QUEUED    skills adapter round (hypothesis:skills-load-per-harness-per-tier-from-one-config-cell) cut from 526's cleared tip · 471 after 530
CHAIN     loop tip (last)   state                                                            land note
 426 schema-gate  527 → 543   mur-20 AWR -> DH.543 LIVE a00-51a6effb                            NEVER 442
 427 heal-refuse  528 → 544   mur-20 DEMOTE -> DH.544 LIVE a00-c7aa5f71                         NEVER 476
 432 guard-piece  530     lane 6                                                               NEVER 432 itself
 433 guard-inst   471     corrective AFTER 432 lands (mur-17 k1 unstructured, k3 AWR)
 g4.18.1.1        521     lane 3 (item 4 a00-9086ec16 UNLANDABLE, row 21)
 g4.18.1.3        519     lane 3 (510 k1-k3 cleared, k4 lane 2)
 g4.18.1.4        497     lane 6
 send-hub box     525     lane 5 (TMM.289 cleared: rows backfilled 91f9e1236)
 kid-worktrees    529 → 533 → 540   lane 5 (529) · 533 DEMOTE -> DH.540 LIVE
 row 20 nudge     524 → 542   mur-20 AWR -> DH.542 LIVE a00-e7cea940
 thought-verb     522     lane 3 · probe-gate 523 → 541: mur-20 AWR -> DH.541 LIVE a00-1362856d
 wake-facts       501     lane 3; BLOCKED: trunk region 2009 > 2000 until belam trims F13
 model-fence      508 → 517 → 536 → 539   murq12 (R4 test NEVER run: row 22)
 PASS 10          509 512 514 515 516 lanes 1-2 · 507 reap-chain lane 4 · belam-cap-reap HELD until 507 lands
 run-key          531     lane 6 · stale-lock 532 → 534 murq14 (532 NEVER merges before 534)
 zero-usd         537 murq13 · trunk reds 538 murq11 · skills 526 lane 4
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
