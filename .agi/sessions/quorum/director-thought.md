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
2026-09-21 ~06:2xZ
 landed   TEL.02 a00-08eead1d, tip f10eef594 -- DECISIVE finding: --cache-reuse reaches the 9B child then is DISABLED AT LOAD, architecturally: qwen35 IMROPE -> n_pos_per_embd()==4 -> get_can_shift()==false -> seq_add hard-asserted to n_pos_per_embd==1 (real upstream llama.cpp cited by file:line, spot-checked by me against the actual copied source, matches exactly). Same-prefix reuse WORKS (24/24, 0.093x prefill) but is a different weaker mechanism than the arbitrary-position shift the hypothesis needs (shifted-span negative: cache_n=0, 1.07x compute -- no savings at all). Kid explicitly refused to conflate the two. Verdict inconclusive_lean_disproved:80 -- the fallback (saved-TEXT-plus-tail-KV, already named in the hypothesis) is now the live path for telepathy chunks 2-3.
 flagged  harvest DM overage 12107/40 no-rebrief -- INVESTIGATED: node's own production_lines=66 (the kid's real script) is correct; the other ~12041 lines are FOUR VERBATIM unmodified upstream llama.cpp .cpp files copied in only so the file:line citations are checkable against real bytes, never executed/modified. Spot-checked myself: real #include headers, cited lines match exactly. This reads like reference material (should be exempt like .txt/.jsonl) not authored code, but I did not rule on it myself -- put to the mur explicitly, not decided unilaterally.
 mur      running (agi-director-thought-tel02, bg poll bccnsgnow)
 TMM.26   MP.02 redefined to SUGGESTER, MP.03 FORMATTER minted -- both no-spend, queued after G14.10.2's capture (see prior commit for detail)
 board    stopped editing doc:lm-town-trajectory directly; rows travel in the merge-up dm now
 next     read the mur result -> notes on hypothesis+g14.15.1 -> merge-up dm (numbers + the ceiling-exemption question, banked for thought-master) -> next queue item is SWR.02-B, not mine
```
