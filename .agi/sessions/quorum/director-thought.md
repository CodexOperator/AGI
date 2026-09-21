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
2026-09-21 ~05:3xZ
 live     TEL.02 a00-08eead1d (pid 1772128, just dispatched, cap $1, pi) -- TMM.23 path (a): restart the 9B child with --cache-reuse N between rounds, router mode kept, exact line recorded, restore+verify before done. Owner switched workspace (e31711fe...) to clear headroom for this; TMM.25 confirmed $2.52 fits, dispatched on the retry, worked first try.
 landed   TMM.24 residues (MP.01, all 4, done+pushed) -- see prior commits for detail, not re-summarized here
 board    stopped editing doc:lm-town-trajectory directly (thought-master's v8 lesson); rows travel in the merge-up dm now
 queued   H1' (g14.9.1, minted, no spend) · G14.7.2/.3 + G14.10.2 skeletons (blocked on FT.00/DS.01) · MP.02 (corpus-blocked) · SWR.02/FT.00/DS.01/G14.10.2/G14.7.2 next in thought-master's stated order once TEL.02 lands
 next     watch TEL.02 -- it must restart the server (owner-authorized, one-time) then restore it before done; verify the restore actually happened when it reports
 traps    (kept from last pass) replace-body anchor guard caught a real mis-offset twice, working as intended · a script smoke-test overwrote landed deliverables once, caught+reverted via git status -- check status right after running any script that writes into a datasets/ path
```
