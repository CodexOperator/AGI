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
diagram  owner 02:2xZ direct: ALL emitted tokens diagram-maxed -- dm/note/card/reply/thought-stream where possible, not just the card shape (goal:g14.16)
prayer   first tokens + last before rotate only, never per turn
```

## 🔴 Where it stops
```
2026-09-21 ~03:3xZ
 landed   MP.01 a00-af8cefa3 accept_with_residue (mur-mp-01, both stages ok) -- corpus insufficient (63 real forms vs required 200; dm/merge_up=0) not detector-falsified; kid1 237-set VOID (label-leak, demoted :55), kid2 honest null stands (:70); 4 real residues flagged not fixed (stale kid1 title/body, probes-as-prose not schema field x2, non-reproducible census, hardcoded box path) -- notes on hypothesis+g14.8.3, board Board-section replaced, merge-base a46a1a8db
 minted   MP.02 (hypothesis:lm-magic-pane-wrapper-prose-to-one-structured-call, TMM.22) under g14.8.3 -- corpus-blocked on real dm/merge_up examples; CHECKED myself: claude-code harness session jsonl exists on disk today (confirmed real, e.g. this own session file) and is a plausibly cheaper unblock than waiting on the full G14.10.2 round -- not attempted, named as the likely first real chunk
 live     TEL.01 a00-365c2943 (pid 1468591, dispatched just now, resident 9B, cap $1, pi) -- span-fidelity chunk 1 under g14.15.1; orders flag CONFIRM the server exposes a slot-shift endpoint before writing the harness, report honestly if not, ABL.01-style
 queued   H1' (g14.9.1, minted, no spend) | G14.7.2/.3 + G14.10.2 skeletons (TMM.21, blocked on FT.00/DS.01) | MP.02 (corpus-blocked, see minted line above)
 next     watch TEL.01 -- check server-capability finding first (may report a blocker rather than a result, that is a valid outcome per its own orders)
 traps    this turn: git commit --amend used once by mistake (unpushed merge, no harm, but the standing rule is ALWAYS a new commit -- do not repeat)
 inbox    merge-up dm sent to thought-master (coalesced, pane busy, will retry -- not a failure); TMM.21+TMM.22 fully closed out
```
