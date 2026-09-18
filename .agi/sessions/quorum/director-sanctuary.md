# director-sanctuary card — ROLE: `doc:unified-director-brief` (read whole, then its §4 sanctuary) — this file is STATE ONLY, replaced whole each session

## §0 STATE — stamp 2026-09-18T05:01:02Z — gen 1, ROTATING NOW (meter crossed 0.85 of the line, heavy tool-call session, lots of live threads — see §3)
- Identity: `director-sanctuary`. Real branch `core/season2/posts/sensei-director/main` — confirm with `git status -sb`, never this prose.
- **Push target**: `remote.origin.push` refspec is still missing (lost in the 04:47Z history rewrite, never restored). Push EXPLICITLY every time: `git push origin core/season2/posts/sensei-director/main:refs/agi/posts/sensei-director`. A bare `git push origin <branch>` creates a stray `refs/heads/...` branch instead.
- 🔴 **Disk is at 98% (1.9G free of 77G) — was 100%/413M before I killed my own background suite run and deleted my own ~1.3G of basetemps.** This is NOT fixed, only less critical. Treat every git write as at-risk until the Prime confirms real space is freed. If a commit/push looks like it "succeeded" but `git cat-file -t <sha>` on the new HEAD fails, or `git status` itself errors with "fatal: bad object", this is the SAME corruption — see §4 for the exact repair sequence (safe, local-only, no data lost last time).
- 🔴 **TWO `[red]` messages sent to belam this session, NEITHER answered yet** (his pane was busy both times, nudges coalesced but messages are durably in his inbox): (1) the disk-full root-cause report, (2) the missing push-refspec report. **First action next session: check for his replies.**
- Live (mine): SM.105 `a00-cbd7ac18` pid 2996625 (workflow slice isolation + timeout, still running), SM.106 `a00-c2784b10` pid 2994677 (SM.104 corrective: global-rollover atomicity fix, still running). **My background pid-watch task dies with this session — it will NOT notify a successor. Set up a fresh watch on these same two pids on arrival**, or just `kill -0` them directly; branch names: `season2/loops/hypothesis-l4-a-failed-repeated--a00-cbd7ac18` and `season2/loops/hypothesis-l4-a-town-season-roll-a00-c2784b10`.
- Not mine: TM.30 (thought-master), uses the 4th fleet slot.
- Credits at last read (before this crisis): 65 total / 25.2 used (~$40 headroom) — re-read fresh, it has been a while.

## §1 PLAN
- [done] SM.102 (proved), SM.103 (inconclusive_lean_proved:88): harvested, merged, independently tested (145+45 and 9+377 passed), pushed. Full suite for these two together: 5506 passed / 0 failed (trustworthy, ran with no concurrent tree writes).
- [done] SM.104 (two kids, both self-demoted by their own parent for hitting real falsifiers — align gate fixed, global-rollover atomicity left open): harvested, merged, pushed. Residue note written on the node for the next parent. SM.106 dispatched as the corrective round.
- [done] Weathered a full-history force-scrub rewrite (owner-ordered, anonymize for open-sourcing): held per Prime order, resumed per Prime order, recovered my in-flight commits with zero data loss (see §4 for the exact mechanism — useful if it happens again).
- [done] Merged the anonymize-rule scrub from origin/season2/main (had to discard ~14 files of other-posts' noise first, verified safe — see §4).
- [done] Discovered + reported the lost push-refspec (origin recreated without it post-rewrite).
- [done] Hit, diagnosed, and repaired a LOCAL git object corruption (my own card commit) — root-caused to the disk being at 100%. Reported to the Prime. Freed ~1.3G of my own throwaway test artifacts as a partial, safe mitigation.
- [in flight, not mine to rush]: SM.105 and SM.106 (corrective), both still running. **No full-suite run has successfully completed since SM.104 landed** — the one I started got killed deliberately (disk crisis took priority over trusting its result anyway).
- [next, in order, once resumed]: (1) check belam's replies to both `[red]`s — his disk-space fix may change what's safe to do; (2) `kill -0` check on SM.105/SM.106, harvest whichever/whatever has landed using the full verification sequence (branch-vs-parent-branch trap, independent test re-run, full suite IF disk allows it — season.py and workflow.py are both cross-cutting enough to earn one, but weigh that against disk risk first); (3) run `workflow.py run merge-up-review --harness pi` for real for the first time this seat has ever run it (dry-run only so far) covering the whole batch (SM.102/103/104/105/106), fix any `[red]` it finds in-loop; (4) deliver ONE `[merge-up]` line to SM covering all five nodes — MUST include: the ceiling-measurement finding (three kids claimed `line_ceiling: 40` against real ceilings of 20/15/~55, a fourth claimed 80 — worth her eye as a scaffold question), the suite-lock-vs-concurrent-write race (g15-worthy), and a one-line mention of the disk/corruption incident for the record.
- [STOP condition unchanged, from the owner]: once the full set (102/103/104/105/106) lands clean with residue closed — no new rounds, no new nodes, idle at card.

## §2 WHAT LANDED THIS SESSION (one line each, cite by commit SUBJECT — every SHA before 04:47Z names dead pre-rewrite history, and my own local corruption/repair minted a THIRD generation of SHAs on top of that for the same two commits, so subjects are the only reliable citation this whole session)
- Rotation joined clean as director-sanctuary; card written, rewritten, and rewritten again as the session's incidents landed.
- Trunk sync (core town + global ladder), read the new unified-director-brief, read all five SM.10x/SM.106 node bodies.
- Dispatched, harvested, merged, tested, pushed: SM.102, SM.103, SM.104.
- Weathered the force-scrub history rewrite with zero data loss.
- Diagnosed and worked around the lost push-refspec.
- Merged the anonymize-rule scrub, discarding verified-safe noise from other posts' domains.
- Wrote the SM.104 residue note; dispatched SM.105 and SM.106.
- Diagnosed and repaired local git object corruption (disk-full root cause); reported it; freed ~1.3G of my own artifacts; disk still tight (98%).

## §3 🔴 WHERE IT STOPS — the next command
```
cd /home/ubuntu/work/agi/.agi/worktrees/post-sensei-director
python3 extensions/agi/bin/send.py read director-sanctuary   # check for belam's replies first — his pane was busy both times, may have landed since
kill -0 2996625   # SM.105 — still alive?
kill -0 2994677   # SM.106 — still alive?
```
If either finished, harvest it (verify parent-branch vs kid-branch, `git diff --stat` against `MB=$(git merge-base HEAD <branch>)`, read every kid node, `git merge --no-ff`, run its own tests, push with the EXPLICIT refspec — see §0). **Before any git write, glance at `df -h /` — if it is back near 100%, stop and re-flag rather than risk another silent corruption.** Once both are in and (disk permitting) a full suite is clean, run the real mur review and deliver the batched `[merge-up]` line per §1.

## §4 TRAPS — three genuinely new mechanisms this session, in the order they'd bite a cold reader
- 🔴🔴🔴 **A commit or `git add` can "succeed" (exit 0, prints a SHA) while silently writing a corrupted/truncated object, when the disk is nearly full.** Symptom chain: `git status` starts failing with `fatal: bad object HEAD`; `git cat-file -t <the new commit sha>` fails with "could not get object info"; even a fresh `git add` of the SAME file can then fail with `error: invalid object ... Error building trees`. **The repair, safe and local-only, no data lost**: (1) confirm the actual working-tree file content is still intact (`tail`/`cat` it — corruption hits the git OBJECT, never the checked-out file); (2) `git update-ref refs/heads/<branch> <last-known-good-sha>` to point your branch back at a commit that DOES `cat-file` cleanly (this alone fixes `git status`); (3) `git reset <that-sha>` to clear the index without touching the working tree; (4) re-`git add` + re-`git commit` the same content fresh. Root cause here was the disk hitting 100% (`df -h /`) — **check disk space FIRST** if you see this pattern, before assuming it is a remote or network problem.
- 🔴🔴 **A `git push origin <branch>` reporting `[rejected] ... needs force` with the hint "points at a non-commit object" can be a RED HERRING for local corruption, not a real remote conflict** — the actual problem in this session was upstream of the push entirely (the local commit object itself was bad). Do not force-push in response to this message; diagnose locally first (`git cat-file -t $(git rev-parse HEAD)`) before touching the remote at all.
- 🔴🔴 **A remote recreated after any git-remote-touching operation can be missing its custom push refspec even though `git remote -v` looks completely normal.** Check `git config --get-all remote.origin.push` if a routine push unexpectedly reports "[new branch]" instead of updating the ref you expected. Workaround: push with the explicit `<local-branch>:<remote-ref>` form. Flag it — this is shared config, likely affects every post on the box.
- 🔴🔴 **The suite-window lock only blocks a SECOND pytest invocation from starting — it does not stop a `git merge` into the same tree from a different process while a full-suite run is already mid-collection.** Wait for a backgrounded suite's completion notification before touching the working tree at all.
- 🔴 **Before discarding any "not mine" modified file to unblock a merge, diff it against the incoming trunk ref first** (`git show <ref>:<path>` vs the working copy) — do not assume "looks unrelated" means "safe to discard" without checking; in this session one such file was actually *behind* trunk (an unscrubbed hardware-model name trunk had already correctly redacted), which made discarding it not just safe but the anonymization-correct thing to do.
- 🔴 **Three kids across three rounds this session all self-reported `line_ceiling: 40` regardless of their real brief ceiling (20, 15, ~55); a fourth used 80.** Not one hardcoded constant — always compare a kid's own ceiling math against the actual brief (SM's dm or the node body), never trust the kid's frontmatter number.
- `[decision] hold` from the Prime overrides the standing meter-rotation rule — do not rotate (or commit/push/merge/dispatch) under a hold, no matter what the meter says, until the matching `[decision] resume`.
- After a resume from a history rewrite: `git status` first, re-commit only your own paths under NEW SHAs, cite prior work by commit subject not SHA.
- Card path collision, `Edit`-doesn't-restage, pid-watch pattern (but see §0 — it dies with the session, a successor must re-arm it), harvest-time branch/claim verification, backtick-free dm/note bodies via scratch-file+python-subprocess, `dispatch.py` numeric-only iteration id, `--prompt-file` per-kid-only, queue vocabulary, provisioning workspace switch — all still live, see `doc:unified-director-brief` §2; not restated, unchanged.

## §5 KNOWN-GOOD VERIFICATION
- `df -h /` — check before every git write while the disk incident is open.
- `git status -sb`, `git cat-file -t $(git rev-parse HEAD)` — confirm your own HEAD is healthy before trusting anything else.
- `git config --get-all remote.origin.push` — confirm the mirror-ref redirect before a bare `git push origin <branch>`.
- `python3 extensions/agi/bin/spawn_budget.py status` — live count before any dispatch.
- Credits: `K=$(grep -m1 '^OPENROUTER_PROVISIONING_KEY=' /home/ubuntu/work/agi/.env | cut -d= -f2-) && curl -s -m 20 https://openrouter.ai/api/v1/credits -H "Authorization: Bearer $K"`.
- `python3 extensions/agi/bin/workflow.py run merge-up-review --harness pi --dry-run` — this seat has still never run the real thing; do the dry-run first regardless.

## §6 BANKED (owner-only)
- None new. Both `[red]` reports (disk-full, push-refspec) are already sent and are the Prime's to act on; nothing further needed from the owner directly.
