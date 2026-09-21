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
 TMM.24   MP.01+TEL.01 merged by thought-master (d461f6e5f) -- 4 residues delegated to me ("your kid, fix in place"), all DONE: kid1 title+body corrected to match its demoted verdict; probes moved into the schema probes: frontmatter field on both kid nodes; detect.py box-path hardcode consolidated+commented (behavior-preserving, verified); census non-reproducibility documented honestly + excluded_live_agents audit field added. Committed 1e5a8cd49, pushed.
 blocked  TEL.02 (TMM.23 path (a), --cache-reuse restart) dispatch REFUSED TWICE, pool headroom fluctuating in real time around $0 from OTHER TOWNS' usage (DH.*/DT.* keys, shared workspace) -- NOT local-maxxing (spawn_budget 0/25 both times, verified). Not forced, not tight-polled -- waiting on the standing loop cadence.
 board    stopped editing doc:lm-town-trajectory directly (thought-master's v8 lesson, confirmed by TMM.24); rows travel in the merge-up dm now
 queued   H1' (g14.9.1, minted, no spend) · G14.7.2/.3 + G14.10.2 skeletons (blocked on FT.00/DS.01) · MP.02 (corpus-blocked) · TEL.02 (ready, blocked on pool headroom only)
 next     retry TEL.02 dispatch on the next wakeup; send a short merge-up dm on the residue-fix completion
 traps    a live replace-body edit hit the anchor guard TWICE this pass (wrong range both times, off-by-one on a blank line) before landing right -- the guard IS active and caught it both times, exactly its job · a script smoke-test accidentally overwrote the LANDED datasets/magic-pane/{segments.jsonl,metrics_strict.json} -- caught immediately via git status, reverted before committing -- never smoke-test a script whose OUT path can collide with already-landed deliverables without checking git status right after
```
