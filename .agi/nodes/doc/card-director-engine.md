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

## §0 STATE (13:3xZ 09-27 · per-chain history = git log of this node)
```
LANDED    merge-ups 12 cbe776456 · 13 0420e2238 · post br = trunk 45bf4f16f merged (NOT suite-run)
MINT FIX  LANDED on the trunk 91ae33672 (TMM.298), post br merged 32ff79e53 -- a base older than that still needs the cherry-pick
FALSIFIER MET: DH.533 ran + exited pi-free, keys 0.01 used 0, credits 0.6063 before = after -> [merge-up] line to TM 13:3xZ (inbox; nudge coalesced, sweep retries)
MURS      units agi-director-engine-murl1..3 = 3 LANES claiming batches murq1..7 by mkdir <scratchpad>/claims/b<N> (a pi-free run is
          SERIAL per stage, ~7 min each: one lane = ~5 h); run key mur-director-engine-23 shared (row 19), labels disjoint:
            1 509k1 509k2 512 514k1 · 2 514k2 515 516 510k4 · 3 519 522 521 501 · 4 526 520 507k1 507k2
            5 525k1 525k2 529k1 529k2 · 6 497k1 497k2 530 531 · 7 532 (review only; NEVER merge before 534)
          murq8 (mur-21) 429 close: verify AWR (my restore re-imported a stale clause) -> fixed 4eb08ee4e -> unit murq9 re-mur 7938a7103..4eb08ee4e
          unit murq11 = DH.538 over 123e0a487..aa383f9f8 (harvested: 184 passed 7 skipped, both retargets PASS)
          unit murq10 = DH.533 k1+k2 over f71d1915b..dedc18720 (harvested: config cell landed dedc18720; 38 touched + 281 heal/help-smoke green)   args + logs: scratchpad 96494ce7-.../murq*.{json,log}
          complete earlier (paid, still valid verdicts): 510k1-k3 (mur-18)
LIVE      NO parents. Harvested green, murs running (unit: round, range, harvest numbers):
          murq11 DH.538 123e0a487..aa383f9f8 184p/7s · murq13 DH.537 123e0a487..f109db023 363p/7s
          murq12 model-fence chain: DH.508-k1 cc35dcc43..360b0f0a1 + DH.539-k1 1faef6315..7d9cc0202 (context 25p, fence 10p)
          murq14 DH.534 5892ec137..e6e678bf2 290p/7s (chain 532 -> 534; 532 itself in murq7)
QUEUED    skills adapter round (hypothesis:skills-load-per-harness-per-tier-from-one-config-cell) after 526 clears · 471 after 530
BLOCKED   501 merge (belam F13 trim: region 2009 > 2000)
CLOSED    429 chain residues = node updates on its loop branch 7938a7103 + 4eb08ee4e (brief text, no kid; wt de-h429)
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
