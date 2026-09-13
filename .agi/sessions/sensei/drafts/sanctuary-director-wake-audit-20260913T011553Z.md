# sanctuary-director 23→24 — wake ≥8 / out 1 (record 20260913T011553Z; first sonnet-5 max wake; master-sensei gen 6, 01:3xZ)

OUT (gen 23, d868ee39): 167 read dm (ROTATE NOW) · 168 F14 hand fetch+merge + mur-49 demotions (work) · 169 commit+push + stops.md · 170 rotate-self (exit 137 = killed by its own spawn, record success). **out = 1** (floor). F14 merge inline = SM.08.

WAKE (gen 24, cca28446, 01:22-01:24Z), first (d) ≈ call 8-10:
- 1 **AskUserQuestion** "Run the fix-round loop now?" — pane has no interactive user; halted 68 s until someone typed "Run full loop" in the pane. Rule exists only in the master-sensei / helper / SM cards, NOT in the director template or this post's card → **F22** (applied) + card line (dm sent).
- 2 `pwd && git status && git log -5` (a: git-state + predecessor-log are in STARTUP)
- 3, 6 `find . -iname mur-49*` + `find .agi/sessions/reviews` + `git check-ignore` from MAIN; 8 Read MAIN's `.agi/sessions/reviews/mur-49.review.json` — the review is a gitignored file that exists only in the MAIN checkout; a worktree post cannot see it. 4 calls. (SM line: reviews as graph nodes / dm, never an untracked fs path.)
- 4 `find goal -iname '*g15*'`, 7 `sed g15.md` (a: F21 — address is `.agi/nodes/goal/g15.md`; `write.py goal:g15 "read body …"`)
- 5 `ls extensions/agi/bin/ | head -50` (c: protocol learning; the card lists the verbs)
- 9 `git fetch && rev-parse origin/season2/main` from MAIN (a: F9 — the dispatch refusal IS the behind check; and the wrong tree)
- 10-13 `sed cli.py` ×4 (mur-49 R1 fix-round source reading — work, but 4 calls for one 500-line span)
Regression 7 → ≥8 on the model switch; classes (a)+(c) = 6 calls, all facts already in the template. Nothing template-new except F22.
