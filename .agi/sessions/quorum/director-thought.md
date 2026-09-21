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
2026-09-21 ~13:0xZ
 landed   SWR-B.03 a00-ec374f61 -- running->stalled(live pid)->done, SELF-finished (never killed, never force-completed). Arm B IFEval 541/541 scored: strict 0.778189 (421/541), loose 0.815157, instr-level 0.851319; threshold 0.781886 -> NOT FIRE, short 0.37pp, inside +/-0.4pp langdetect floor. 2 kids, 0 demoted, 0 failed.
 answered owner  Q: is stalled for-sure-accurate or just appears so? should kill-list include stalled+timeout?
   stall_detect.py L55-75  stalled = 4 ANDed conditions (cohort terminal, dispatcher record still "running", record MTIME UNCHANGED since spawn, worktree dirty) + age>45min -- real procedural check, but tests "bookkeeping file never rewritten," not liveness/progress -- equally true of a healthy long round and a dead one
   heal.py L217-226  stalled + pid DEAD -> already resolved via _reap_one (marked dead if warranted) -- not a "kill," a cleanup, nothing left alive to kill
   heal.py L227-235  stalled + pid LIVE -> deliberately excluded from kill (named ruling SM.23b/goal:g15.25: "still holding its lease") -- by design, not a gap
   proof not theory  SWR-B.03 itself sat live-stalled mid-run, was left alone, finished correctly with the score above -- auto-killing stalled+timeout would have destroyed that exact result
 self-caught (prior)  TMM.31 commit missed staging the experiment-node edit -- caught via post-commit status, fixed in a second commit, nothing lost
 landed   SWR-B.03 -- mur-director-thought/swr-b-03: accept_with_residue, NO demotion, pushed 7a4c4167b, merge-up dm sent. Arm B IFEval 541/541 scored strict 0.778189 (421/541) vs threshold 0.781886 -- does NOT fire, 0.37pp short, inside +/-0.4pp floor (mur independently re-ran the harness 10x: 420x6/421x3/422x1, confirms the floor, not fabrication). Fires HumanEval, misses IFEval -- two-eval hypothesis not satisfied by arm B alone. 1 defect refuted (llama-server restore wording), 1 residue + 1 note confirmed and fixed (stale worktree resume path, stale gap_table.md header).
 live     SWR-C2.02 a00-5265b6a1 (pid 4116174, cap $2, GPU) dispatched -- TMM.30 order, arm C2 (B + OrcaBonsai LoRA scale 2) IFEval, same 541-prompt file/harness/threshold as B, LoRA launch config sourced from a00-bb10233d-5a7f1f.md (C1 pattern) + a00-c4441397-c8a8c6.md (C2's own proven HumanEval launch). Orders warn: expect 2+ rounds like the B track (~2.2-2.7h generation), resume paths must be tracked-repo not worktree (B.03's own mur just caught that exact defect). Dry-run clean, real dispatch hit stale-base once (trunk had moved -- thought-masters own g14.11/board apply came in), merged clean, refired successfully second try.
 next     watch SWR-C2.02; standard landing (merge, read nodes, independent byte-check, mur, fix residues, note goal:g14.11.1, push, merge-up dm) once it produces a scored row or a resume-state report
 banked   fork get_can_shift probe on deployed prism build 10685/7dffb158d (TEL.03/TMM.29) -- SWR-B.03 closing just opened a GPU-free slot
 traps    ALWAYS check git status right after a commit, not just before -- a status shown before committing does not guarantee everything intended got staged · inbox has a SECOND raw delivery path (.agi/sessions/inbox/director-thought.md, untracked) · replace-body anchor guard treats a markdown TABLE, and a # comment inside a fenced code block, as heading-like · dispatch iter ids reject a hyphen after the dot · pool headroom can clear between a dry-run and the real dispatch seconds later · an APOSTROPHE inside a single-quoted write.py argument breaks the shell like the backtick-in-double-quote trap
```
