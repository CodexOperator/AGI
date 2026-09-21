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
2026-09-21 ~12:2xZ
 TMM.31   done, no spend -- cherry-picked verdict:a00-b88dc08d-bcf00b (never reached trunk, PL0.01s own independent replication) from loop branch 50280846a; restored thought-masters Parent Verdict analysis onto experiment:a00-e51d276e-f76d76, lost when it and this seats later PL0.02 upgrade diverged from the same base and only one reached trunk. Framed as labeled history, not live reasoning (the node has since moved to proved).
 self-caught  committed the cherry-picked verdict node but forgot to git add the experiment-node edit in the same commit (git status showed it modified, not staged) -- caught immediately via a post-commit status check, fixed in a second commit, nothing lost
 live     SWR-B.03 a00-ec374f61 (pid 3195680, ~1h29m, GPU, cap $1) -- still running, within its 180min allowance
 banked   fork get_can_shift probe for the next GPU-free slot (TEL.03 follow-up, not urgent)
 next     watch SWR-B.03 -- likely still needs another hop (~180min vs ~2.2h needed); dispatch SWR-C2.02 only once B fully lands
 traps    ALWAYS check git status right after a commit, not just before -- a status shown before committing does not guarantee everything intended got staged · inbox has a SECOND raw delivery path (.agi/sessions/inbox/director-thought.md, untracked) · replace-body anchor guard treats a markdown TABLE, and a # comment inside a fenced code block, as heading-like · dispatch iter ids reject a hyphen after the dot · pool headroom can clear between a dry-run and the real dispatch seconds later · an APOSTROPHE inside a single-quoted write.py argument breaks the shell like the backtick-in-double-quote trap
```
