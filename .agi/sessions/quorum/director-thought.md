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
diagram  owner 02:2xZ direct: ALL emitted tokens diagram-maxed -- dm/note/card/reply/thought-stream where possible, not just the card shape (goal:g14.16)
prayer   first tokens + last before rotate only, never per turn
```

## 🔴 Where it stops
```
2026-09-21 ~02:4xZ
 live     MP.01 a00-af8cefa3 (pid 987668, 1h15m elapsed, PAST its 75min manifest timeout but pid alive, Ss) -- manifest top-level status=stalled/overdue_since=None (stale label: NOT trusted alone) vs raw output.log mtime = now, kid a00-5b80b456 actively writing datasets/magic-pane/segments.jsonl (segs~36-39 of the >=200 target, still climbing) -- treated as overdue-but-working (card rule), not dead; no kill, no replacement, no dispatch of a second round
 landed   SWR.01 (346c377c2) -- ref bar 93.9pct HE / 0.869 IF strict; B/C1/C2 fire 0.9x on HE; IFEval undecided -> SWR.02 (TMM.19, not my lane)
 queued   H1' (g14.9.1, minted) | TEL.01 (g14.15.1, minted+filled, ready to dispatch) -- both no spend yet
 minted   TMM.21 batch (no spend): G14.7.2 training-ladder + G14.7.3 diagram-maxed-traces under g14.7; G14.10.2 session-trunk+classifier under g14.10 -- skeleton-only, blocked on FT.00/DS.01
 vision   TMM.22 (owner, goal:g14.8): magic pane = the unified messaging layer (LLM speaks prose/diagram -> system wraps the structured call; jev first, town's own tiny model later per G14.7.2/.3+G14.16). Chain: MP.01 detector -> MP.02 wrapper (prose->1 call, real town dms/notes/merge-ups as test set, jev=judge) -> MP.03 replaces send.py grammar for one post pair -> MP.04 own tiny model vs jev. MP.01 itself UNCHANGED.
 next     on MP.01 landing: review kid DIFF not report -> mur if warranted -> merge-up note+numbers on board -> mint MP.02 hypothesis under g14.8.3 (per TMM.22) -> dispatch TEL.01 parent (resident 9B, cap $1, pi) -- TEL.01 stays the only thing actually ready to spend on right now
 inbox    TMM.21 (dadd6797a) + TMM.22 (af8931916) processed; no dm sent back either time (batch-max: routine order execution, reports via the graph)
```
