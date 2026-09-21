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
2026-09-21 ~03:3xZ
 landed   MP.01 a00-af8cefa3 accept_with_residue (mur-mp-01, both stages ok) -- corpus insufficient (63 real forms vs required 200; dm/merge_up=0) not detector-falsified; kid1 237-set VOID (label-leak, demoted :55), kid2 honest null stands (:70); 4 real residues flagged not fixed (stale kid1 title/body, probes-as-prose not schema field x2, non-reproducible census, hardcoded box path) -- notes on hypothesis+g14.8.3, board Board-section replaced, merge-base a46a1a8db
 minted   MP.02 (hypothesis:lm-magic-pane-wrapper-prose-to-one-structured-call, TMM.22) under g14.8.3 -- corpus-blocked on real dm/merge_up examples; CHECKED myself: claude-code harness session jsonl exists on disk today (confirmed real, e.g. this own session file) and is a plausibly cheaper unblock than waiting on the full G14.10.2 round -- not attempted, named as the likely first real chunk
 live     TEL.01 a00-365c2943 (pid 1468591, ~26min elapsed, healthy, status=running) -- kid1 already found the real answer: slot-save/seq/kv HTTP routes all 501/404, but libllama-server-impl.so DOES carry seq_add/seq_rm/can_shift -- mechanism exists, not exposed. Declined a same-position cache-reuse proxy as a substitute (would have faked a shift result). Verdict trending `pending`, honest, exactly the ABL.01-style outcome the orders asked for. Bonus correction: :8080 is the ROUTER not the model; the 9B child is on :54437 -- fix this on the hypothesis node once the round lands.
 queued   H1' (g14.9.1, minted, no spend) | G14.7.2/.3 + G14.10.2 skeletons (TMM.21, blocked on FT.00/DS.01) | MP.02 (corpus-blocked, see minted line above)
 next     let TEL.01 finish (parent still deciding continue/adjust/done) -- not yet landed
 traps    git commit --amend used once by mistake (unpushed, no harm, but ALWAYS a new commit -- do not repeat) · end-of-turn USER replies drifted to prose paragraphs this session (owner caught it 03:4xZ) -- fixed, calibrated against director-engine/thought-master cards, see diagram rule above
 inbox    merge-up dm sent to thought-master (coalesced, pane busy, will retry -- not a failure); TMM.21+TMM.22 fully closed out
```
