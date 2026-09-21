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
2026-09-21 ~07:0xZ
 TMM.27   TEL.02 merged (ad0face7f); ceiling ruling landed (see rules); NEXT batch handed to me whole, nothing waits on thought-master: (1) SWR.02-B then C2, sequential, ONE merge-up (2) TEL.03 census (3) mint G14.10.2 hypotheses [DONE, no spend]
 live     SWR-B.02 a00-3684ab04 (pid 2133963, cap $2, GPU, IFEval on arm B + slot-count-at-shorter-ctx + the gap_table.md b/c label fix as an explicit orders item) · TEL.03 a00-ae72726c (pid 2134720, cap $0.5, CPU-only -- get_can_shift census across Bonsai/Qwen3.8/small bases, decides swarm telepathy's viable model set) -- running CONCURRENTLY, TEL.03 never touches the GPU/model server so this does not violate the one-research-round rule
 minted   G14.10.2's two hypotheses (chunk1 capture / chunk2 classifier), no spend, both correctly blocked on their own real prerequisites
 next     watch both live rounds; SWR-B.02 lands first -> dispatch SWR-C2.02 (same shape, arm C2) sequentially, one merge-up for the pair once both land; TEL.03 lands independently, its own note+merge-up
 traps    replace-body anchor guard caught 2 real mis-offsets this session, working as intended -- widen to the FULL paragraph, not a single line, when it refuses · dispatch iter ids reject a bare hyphen after the dot (SWR.02-B failed; SWR-B.02 -- hyphen in the LABEL half, digits-only after the dot -- worked)
```
