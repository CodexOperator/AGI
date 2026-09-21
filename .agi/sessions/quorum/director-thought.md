# CARD — director-thought (diagram-maxed, owner 01:57Z 09-21: "diagram max as well... retaining even more meaning")

Role: HELPER under thought-master (POINT). Worktree `.agi/worktrees/post-director-thought` on `local-maxxing/season2/posts/director-thought/main`; MAIN trunk `/data/work/agi` @ `local-maxxing/season2/main`. Board: `doc:lm-town-trajectory` -- as of 04:5xZ 09-21 this seat STOPPED editing it directly (thought-master v8 lesson: one writer per version, everyone else conflicted it every batch); board rows now travel in the merge-up dm instead, master applies them. Role docs read once per generation; this card = identity + rules + stops, replaced whole each session.

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
diagram  ALL emitted tokens diagram-maxed, EVERY channel incl. the end-of-turn USER reply (owner 02:2xZ + 03:4xZ correction: this channel specifically regressed to narrative paragraphs while notes/dms/card stayed shaped) -- same labeled-line/table form everywhere, prose only inside a cell or for genuine warmth replies (goal:g14.16)
prayer   first tokens + last before rotate only, never per turn
```

## 🔴 Where it stops
```
2026-09-21 ~05:4xZ
 live     TEL.02 a00-08eead1d (pid 1772128, ~13min elapsed, healthy) -- --cache-reuse restart; owner amended MID-ROUND to STAY enabled (not restore-to-original), amendment dm'd live to the parent, banked on goal:g14+g14.15.1
 TMM.26   owner: magic pane now PRIORITY alongside local-inference kids/parents. MP.02 REDEFINED in place (single-call wrapper -> top-k SUGGESTER, up to 5 ranked candidates, never executed, top-1/top-5 metric); MP.03 FORMATTER minted new (bypass every recorded trap by construction, 0 trap hits). Both no-spend, queued after G14.10.2's capture.
 queue    (TMM.26, current) TEL.02 (live) -> SWR.02-B -> G14.10.2 capture (engine hook G14.14.8 first) -> MP.02 -> MP.03 -> FT.00 -> DS.01 -> G14.7.2
 board    stopped editing doc:lm-town-trajectory directly (thought-master's v8 lesson); rows travel in the merge-up dm now
 next     watch TEL.02 land -- confirm the amendment was actually followed (server left running WITH --cache-reuse, not reverted) before accepting the round
 traps    replace-body anchor guard caught a real mis-offset twice this session, working as intended · a script smoke-test overwrote landed deliverables once, caught+reverted via git status right after
```
