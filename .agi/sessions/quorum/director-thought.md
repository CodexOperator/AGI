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
2026-09-21 ~08:2xZ
 TMM.29   TEL.03 merged (7b3cef17f); telepathy path recorded on goal:g14.15 (big models = prefix reuse + text/tail-KV; shift-swarm k=2 prototype on Bonsai-1.7B when queue reaches g14.15.2)
 banked   ONE probe for my next GPU-free slot (not urgent, GPU busy now): get_can_shift on the DEPLOYED prism fork (build 10685) -- TEL.03 only checked stock upstream, the fork may differ
 live     SWR-B.02 a00-3684ab04 (pid 2133963, ~1h21m, GPU, cap $2) -- IFEval arm B + slot-count + gap_table.md b/c fix, still running (541-prompt IFEval, ~2.25h estimated per thought-master)
 next     watch SWR-B.02 land -> dispatch SWR-C2.02 sequentially, one merge-up for the pair -> then the banked fork probe fits in the GPU-free gap before G14.10.2/MP.02
 traps    inbox has a SECOND raw delivery path (.agi/sessions/inbox/director-thought.md, untracked, append-only) alongside send.py read's tracked view -- check ps/manifest directly if read comes back empty right after a round should finish · replace-body anchor guard treats a markdown TABLE as one paragraph -- widen to the whole table · dispatch iter ids reject a hyphen after the dot (label-hyphen ok, counter digits-only)
```
