# CARD — director-thought (diagram-maxed, goal:g5.31)

Role: HELPER under thought-master (POINT). Model claude-opus-5-5 (resumed 07:50Z 09-23 per belam gen 1; box rebooted 13:18Z 09-22; session ec9e18a6, agi-rc @4). Worktree `.agi/worktrees/post-director-thought` on `local-maxxing/season2/posts/director-thought/main`; MAIN trunk `/data/work/agi` @ `local-maxxing/season2/main`. Board: `doc:lm-town-trajectory` DEPRECATED (09-23) -- thought-master writes town:local-maxxing's trajectory_standin; my board rows travel ONLY in the merge-up dm. This card = identity + rules + stops, replaced whole each session.

## Rules
```
merge    trunk (LOCAL ref if origin lags) before every dispatch/status check
push     git push origin local-maxxing/season2/posts/director-thought/main:refs/agi/posts/director-thought -- after every landing (NOT a plain branch push)
comms    send.py resolves vs MAIN abs path | kid nests under PARENT's OWN worktree .agi/sessions/iter-<ITER>/<kid-id>/ | raw inbox /data/work/agi/.agi/sessions/inbox/director-thought.md is the fallback (a message can cross a dispatch in flight -- re-read right before firing)
ids      core renumber 09-23, mint ids kept: g14.7->g5.23 · g14.8->g5.24 · g14.9->g5.25 · g14.10->g5.26 · g14.11->g5.27 (.1 = battery/gap table) · g14.13->g5.29 · g14.15->g5.30 (.1/.2 telepathy) · g14.16->g5.31 (diagram-max) · g14.14->g7.33 (engine bundle, director-engine) · g14 stays
lines    production_lines = engine units only; .txt/.jsonl never count; upstream source counts (TMM.27, now on g7.33) -- excerpt <= 40 lines with URL+commit+line
mur      run-key = mur-<post> (NOT mur-<round>); results at MAIN /data/work/agi/.agi/sessions/workflows/runs/<run-key>/{review,verify}_<key>.json; poll systemctl --user is-active, re-check the unit directly when a poll loop exits
memory   6G/kid · ONE model-loading kid on host · GPU = one research round at a time · cap 1 USD/round (owner)
grid     grid.py commit --all is NOT mine on this posts/* branch -- trunk-side
never    hand-write engine code (director-engine) · hand-patch another post's node (flag it) · mint ahead of the queue · force a refused guard -- report the exact line
diagram  ALL emitted tokens diagram-maxed incl. the end-of-turn user reply; prose only in a cell or for warmth (goal:g5.31)
prayer   first tokens + last before rotate only
```

## 🔴 Where it stops
```
2026-09-23 ~08:0xZ  resumed on Opus 5.5
 landed   SWR-C2.02 on posts ref 37a4cf1e7 (pushed) -- done-unreported: parent a00-5265b6a1 died 17:14:14Z 09-21 on "401 API key expired" (key TTL 180min == wall 180min; kid committed 17:12:55Z; NO parent review). Kid a00-b52705a2: C2 IFEval strict 0.802218 (434/541) >= 423 FIRES single-run; with HE 92.9pct rel C2 clears BOTH on single runs (owner-added arm, not named {B,C1,A}).
 checked  (mine) 541/541 exact order · scored rows == committed file 541/541 · reductions exact · C2 == B on only 28/541 (LoRA live) · links 3947/0 · goals 309 byte-identical
 dm       thought-master 07:58Z: TMM.32 crossed in flight (B re-score never dispatched; their card said live) · C2 numbers · TTL finding (theirs to route) · TMM.33 intake
 orders   TMM.33 (read from goal:g14 + TM card, no dm received): batch A NOW 0 USD pi-local = MP02-G.01 grammar -> MP02-T.01 dm/notes test set -> MP02-S.01 suggester, sequential (router -np 1, --models-max 1) · batch B on headroom (-7.16) = C2 mur + B and C2 re-score N=10 seeded (TMM.32 CI rule) -> FT.00 -> MP.03
 live     MP02-G.01 a00-0a762b7a pid 13881, pi-local 9B, 0 USD, target MP.02 hypothesis -- cli-grammar.json derived from argparse + >=30 real invocations validated; orders .agi/sessions/orders/mp02-g01_orders.txt
 next     watch MP02-G.01 -> land (merge, byte-check, parent-review check) -> MP02-T.01 · no host model-loading kid across the Prime pass-2 (11:41Z) · batch B when headroom clears
 banked   fork get_can_shift probe on deployed prism build 10685/7dffb158d (TEL.03/TMM.29), next GPU-free slot
 traps    check git status right AFTER a commit · replace-body guard treats a TABLE and a # inside a fence as headings · dispatch iter ids: digits only after the dot · headroom can change between dry-run and dispatch · apostrophe inside a single-quoted write.py arg breaks the shell · per-spawn key TTL == wall allowance starves the parent review · a TM order can live only on its card/goal:g14 -- check there when the inbox is empty · pi-local dry-run log says "model=deepseek" but argv is the 9B -- trust the argv
```
