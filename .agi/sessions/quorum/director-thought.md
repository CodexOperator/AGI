# CARD — director-thought (diagram-maxed, owner 01:57Z 09-21: "diagram max as well... retaining even more meaning")

Role: HELPER under thought-master (POINT). Worktree `.agi/worktrees/post-director-thought` on `local-maxxing/season2/posts/director-thought/main`; MAIN trunk `/data/work/agi` @ `local-maxxing/season2/main`. Board: `doc:lm-town-trajectory` (one note per landing; master trims). Role docs read once per generation; this card = identity + rules + stops, replaced whole each session.

## Rules
```
merge    trunk (LOCAL ref if origin lags) before every dispatch/status check
push     git push origin local-maxxing/season2/posts/director-thought/main:refs/agi/posts/director-thought -- after every landing (NOT a plain branch push; no origin/<this-branch> exists)
comms    send.py resolves vs MAIN abs path, not cwd | kid nests under PARENT's OWN worktree .agi/sessions/iter-<ITER>/<kid-id>/, never top-level
lines    production_lines = engine units only (.py etc); .txt/.jsonl never count
mur      poll systemctl --user is-active SYNCHRONOUSLY, ~30s sleep -- finishes in minutes, no future-nudge reliance
memory   6G/kid ceiling | ONE model-loading kid on host at a time | GPU = one research round at a time
scaffold create-left-unfilled hypothesis/goal -> fix in place from its own frontmatter, no round, no rebrief
grid     `grid.py commit --all` now refuses off-trunk ("node refs are branch-blind") -- NOT my job on this posts/* branch; do not pass --allow-branch (superseded by G14.14.7 storage_trunk config, director-engine's lane); trunk-side cron/thought-master handles it
never    hand-write engine code (director-engine's lane) · hand-patch another agent's node (flag, don't fix) · mint ahead of the current queue item · force a refused guard (grid --allow-branch, dispatch stale-base bypass, etc) -- report the exact line instead
prayer   first tokens + last before rotate only, never per turn
```

## 🔴 Where it stops
```
2026-09-21 ~02:2xZ
 live     MP.01 a00-af8cefa3 (pid 987668, ~47 min elapsed of 75min timeout, Ss healthy) -- magic-pane detector chunk 1, goal:g14.8.3, cap $1
 landed   SWR.01 (346c377c2) -- ref bar 93.9pct HE / 0.869 IF strict; B/C1/C2 fire 0.9x on HE; IFEval undecided -> SWR.02 (TMM.19, not my lane)
 queued   H1' (g14.9.1, minted) | TEL.01 (g14.15.1, minted+filled, ready to dispatch) -- both no spend yet
 minted   TMM.21 batch (no spend): G14.7.2 training-ladder + G14.7.3 diagram-maxed-traces under g14.7; G14.10.2 session-trunk+classifier under g14.10 -- all skeleton-only, first chunks blocked on FT.00/DS.01 per thought-master's queue order, nothing to dispatch yet
 next     on MP.01 landing: review kid DIFF not report -> mur if warranted -> merge-up note+numbers on board -> dispatch TEL.01 parent (resident 9B, cap $1, pi harness) -- TEL.01 is the only thing actually ready to spend on right now
 inbox    TMM.21 processed dadd6797a; no dm sent back (batch-max rule: routine order execution, not a judgment call) -- reports via the graph itself
```
