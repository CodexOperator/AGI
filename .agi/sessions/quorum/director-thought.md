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
diagram  ALL emitted tokens diagram-maxed, EVERY channel incl. the end-of-turn USER reply (owner 02:2xZ + 03:4xZ correction: this channel specifically regressed to narrative paragraphs while notes/dms/card stayed shaped) -- same labeled-line/table form everywhere, prose only inside a cell or for genuine warmth replies (goal:g14.16)
prayer   first tokens + last before rotate only, never per turn
```

## 🔴 Where it stops
```
2026-09-21 ~04:0xZ
 landed   TEL.01 a00-365c2943 tip 312a42fb7, verdict pending (honest, not disguised-disproved) -- shift mechanism EXISTS in the binary (seq_add/seq_rm/can_shift) but NO enabled HTTP surface reaches it (9/9 slot actions 501, 6/6 candidate routes 404); cache_prompt r2/r3 confirms no shift happens today (cache_n 766 same-pos vs 0 shifted); kid declined to dress up same-position reuse as a shift result; parent independently re-probed and confirmed every number; spot-checked myself, all real. Port correction found: :8080=router not the model, 9B child on :54437.
 mur      running (agi-director-thought-tel01, bg poll bx4d5lgzu) -- verify before merge-up note, same discipline as every round this session
 banked   forward-path decision is director/owner-level, not mine alone: (a) restart resident server with --cache-reuse [needs owner permission] vs (b) add a seq_add/seq_rm HTTP route [engine-adjacent, director-engine's lane] vs (c) second model load [out of scope, memory rule] -- will bank this explicitly once the mur clears, not decide unilaterally
 queued   H1' (g14.9.1, minted, no spend) · G14.7.2/.3 + G14.10.2 skeletons (TMM.21, blocked on FT.00/DS.01) · MP.02 (corpus-blocked, see prior landing)
 next     read the mur result -> note hypothesis+g14.15.1 -> board replace -> bank the (a)/(b)/(c) forward-path choice -> merge-up dm
 traps    git commit --amend used once by mistake this session (unpushed, no harm, but ALWAYS a new commit) · end-of-turn USER replies had drifted to prose (owner caught 03:4xZ, fixed, see diagram rule)
```
