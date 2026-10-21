---
id: doc:card-director-goals-1
mint_id: 241494f333d2430abc688586909a2c99
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-1
scaffold_hash: ce9da8b3b952451b
season: 2
tags: []
title: Card director goals 1
town: core
---
# doc:card-director-goals-1 — director-general-1's card, now doc:card-director-goals-1 (DG5's 4a renames the file, the mint id 241494f333d2430abc688586909a2c99 is kept): the ONE scratch, replaced whole, <= 100 lines

## READ THIS FIRST (step 0 of G3, 10-21 ~19:3xZ): YOU ARE director-goals-1, a NEW SESSION
The post was director-general-1 and is RENAMED director-goals-1 (goal:g7.16.1.11.45 THE POST SHUFFLE, design B: same uid, a fresh key minted at the first start under director-goals-1@agi; belam ran the move, SM and the council gave the GO). Claude keys transcripts by path, so this session starts empty: THIS CARD is the resume path. Your own Claude login stayed yours.
- New address: doc:card-director-goals-1 · home /var/lib/agi/director-goals-1 · worktree branch posts/director-goals-1 · mail `AGI_POST=director-goals-1 /opt/agi/bin/box read` · parent SM (sanctuary-master).
- New ROLE: doc:role-director-goals (read it): you keep the goals TRUE: you RUN falsifiers and PROPOSE close / split / retire to SM; the goal family's WRITER and the close itself are NOT yours. A falsifier is run at mint and must exit non-zero then; per landing re-run only the leaves that landing touched, under the run gate. (Before 10-21 I closed leaves in the standing form myself: from now on I PROPOSE it, SM/the writer lands it.)
- Check your first commit: `git log --format=%G? -1` is G (the key is new). If not, tell SM, nothing else.
- 'director-general-1:' in git history and mail before 2026-10-21 is THIS post (the rows' was/became cells). A NEW director-general-1 (the ex-DG3) comes later: not me.
- First act: `box read`, then act only on what SM asks. Box SM ONLY, NEVER belam, ONE message per finished thing, NO acks; `box send sanctuary-master <<'EOF' ... EOF`, a QUOTED heredoc (argv text arrives EMPTY). Never a host act. After the shuffle SM's word: "focus on season 3 improvements".

## OVERALL GOAL (owner 10-08): encapsulation of grid slices, belam on the new engine, then the season rollover. DONE 10-15: season 3 is rolled; progress is read on town:local-maxxing 'Engine rework trajectory'.

## §0 State (10-21 19:3xZ, trunk core/season3/main = 1e820aff91 at writing; crons + keepalive on)
| | |
|---|---|
| tree | ~/t is DETACHED at posts/<name>: NEVER `git checkout` in it · card edits: `agi-wt pull doc:card-director-goals-1` + edit + agi-turn + agi-flush |
| IN FLIGHT | NOTHING. No tip of mine is unlanded (K2 met): L29 captive-lock, L30 g12.3 closed rows, L32 g12.3 follow-up (idempotent _append_season_row) are all in the trunk |
| SCRATCH | /data/work/gate-director-general-1/wip KEPT under its OLD name (council R5): worktrees g123, cap, close80, close81, g123-trunk, all disposable; tmp = TMPDIR there. Cut a send: `git worktree add --lock --detach <dir> <live trunk>`, ONE signed commit, `git push /data/work/agi SHA:refs/heads/dg1-<new name>` (a NEW branch name each time; the dg1-* ones cannot be deleted from this uid) |
| BOX RULES | NEVER start pytest while SM's gate suite runs (gates wait for 0 pytest peers); SM runs the full suite + lanes on the land tree; for a review-ready I run only the DERIVED set + my rows + mutants, and shell lanes (bare env -i, sh) |

## 🔴 OPEN ITEMS (every one; none lost in the move)
1. TWO NITS riding my NEXT touch (council 3/3 on L32, no return): (a) season.py `_append_season_row`: `int(rows[-1].get("season", -1)) == int(g)` on the guard + a test row with a ledger {"season": "3"} (mutant: the str compare duplicates the row); (b) goal:g12.3 BODY: the 10-15 'FALSE STATE ... season.py never sets closed' line marked 'FIXED (L30 3a91789da4)'. g12.3 stays ACTIVE (long-term umbrella; never closed as a leaf).
2. goal:g7.16.1.11.20.3 is NOT closed: its falsifier is a LIVE read of SM's after projection (SM's Fc4 read). When SM mails it (or says close on the lanes): PROPOSE/cut ONE signed commit on a worktree of the LIVE trunk "CLOSE .20.3 = 75743e7d06 + falsifiers RE-RUN at <trunk sha>: captive-release 14/0, post-env 33/0, engine-sizes 26/0" (lanes re-run at that sha, bare env -i); say to SM it is a proposal under the new role.
3. THREE agi-captive residues for the NEXT edit of that piece (none made): n1 `r=;` init first (mutant env r=x + fresh window + stub agi-fill -> GATED); n2 a failed mv appends '(rename failed)' (mutant: read-only dir); n3 time the window from `.t` via jq, not the mtime (mutant t=now-1000, mtime=now -> released).
4. PARKED, nothing queued: goals .11.12 .11.13 .11.15 .11.17 at horizon (.11.13: the aa3 lanes are run by the lanes post, then the close is proposed in the standing form "CLOSE <leaf> = <sha> + falsifiers RE-RUN at <trunk sha>: <counts>"; a close without a run at the named sha is refused).
HOST ACTS (belam, never mine): alarm_spool install, cron-row `--seat` -> `--post`, crons apply, the sysctl drop-in, boxwake re-projection, and every step of the shuffle.

## §2 Landed (mine, via SM)
memguard stack, slab chain, sysctl-check, fill-line fix, thrash row, boxwake fingerprint, seat-alias fix, the bundle sweep (.11.20/.20.2/.40.1.1/.11.36/.5.3.2), L29, L30, L32. Detail: git history + the grid.

## §4 Traps (this generation only)
| trap | rule |
|---|---|
| a node edit made via agi-wt/agi-turn on the posts branch | NEVER mailed as a sha for landing: re-cut the final blob as ONE commit on a worktree of the live trunk |
| `box send POST "text"` | arrives EMPTY: a quoted heredoc on stdin |
| a pytest started while SM's gate suite runs | blocks gates: check `ps` first |
| a ledger derivation from `git log --follow` | shows side-branch flip-flops: read `--first-parent` |
| the rollover rule | no commit stages spawn_gate.py, frontmatter.py, .agi/context/schemas/*, engine-post.md; ladder.md only alone in the season bump |
| the shuffle | a land REFUSES a tip signed by a stamped (retired) key dated past its stamp; never carry a private key; no gate or land during a move |

## §5 Verification: every return RUN at the sender's sha, bare `env -i`, nice 10. g12.3 derived set 1808 passed (rc 0); SM's gate106 4069 passed.

## §6 BANKED (to SM's digest; none blocks a build)
- user@-only memory thrash is logged but not noticed (memory_alarm_posts owns the notice).
- Banked for the owner (council): should posts mint through captive windows at all, and if so should agi-fill be in post bins (§Y2).
