# CARD — director-thought (diagram-maxed, owner 01:57Z 09-21: "diagram max as well... retaining even more meaning")

Role: HELPER under thought-master (POINT). Worktree `.agi/worktrees/post-director-thought` on `local-maxxing/season2/posts/director-thought/main`; MAIN trunk `/data/work/agi` @ `local-maxxing/season2/main`. Board: `doc:lm-town-trajectory` -- as of 04:5xZ 09-21 this seat STOPPED editing it directly (thought-master v8 lesson: one writer per version, everyone else conflicted it every batch); board rows now travel in the merge-up dm instead, master applies them. Role docs read once per generation; this card = identity + rules + stops, replaced whole each session.

## Rules
```
merge    trunk (LOCAL ref if origin lags) before every dispatch/status check
push     git push origin local-maxxing/season2/posts/director-thought/main:refs/agi/posts/director-thought -- after every landing (NOT a plain branch push; no origin/<this-branch> exists)
comms    send.py resolves vs MAIN abs path, not cwd | kid nests under PARENT's OWN worktree .agi/sessions/iter-<ITER>/<kid-id>/, never top-level
lines    production_lines = engine units only (.py etc); .txt/.jsonl never count. Third-party/upstream reference source DOES count (TMM.27 ruling, on goal:g14.14) -- excerpt <= 40 lines with URL+commit+line, never copy a whole file in
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
2026-09-21 ~09:3xZ
 TMM.30   SWR-B.02 merged (ea0d48897); findings recorded on g14.11. SWR-B.03 = T1-only continuation, single-stream, resume at 110/541, wall 180min ALLOWED this round (exception to the usual), cap now $1. Dispatch when headroom clears -- my loop, never forced.
 blocked  SWR-B.03 still headroom-blocked ($-4.05 latest) -- headroom fluctuates fast enough that a clean dry-run moments earlier does not guarantee the real dispatch passes (same shape as TEL.02s two attempts). Not tight-polling further this pass.
 banked   fork get_can_shift probe for the next GPU-free slot (TEL.03 follow-up, not urgent)
 next     retry SWR-B.03 on the loop; no dm needed until it actually dispatches or the block changes materially
 traps    inbox has a SECOND raw delivery path (.agi/sessions/inbox/director-thought.md, untracked) alongside send.py read's tracked view · replace-body anchor guard treats a markdown TABLE, and a # comment inside a fenced code block, as heading-like -- widen past them · dispatch iter ids reject a hyphen after the dot · dispatch has no wall-clock override I could find -- "180min allowed" reads as a monitoring exception, not a settable flag · an APOSTROPHE inside a single-quoted write.py note argument breaks the shell like the backtick-in-double-quote trap -- write "does not" not "doesn't"
```
