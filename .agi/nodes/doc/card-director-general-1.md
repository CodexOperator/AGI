---
id: doc:card-director-general-1
mint_id: 241494f333d2430abc688586909a2c99
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-1
scaffold_hash: ce9da8b3b952451b
season: 2
tags: []
title: Card director general 1
town: core
# doc:card-director-general-1 — director-general-1's card: the ONE scratch, replaced whole, <= 100 lines

## OVERALL GOAL (owner 10-08): encapsulation of grid slices, belam on the new engine, then the season rollover. DONE 10-15: season 3 is rolled. NOW (owner 10-21 14:45Z, goal:g7.16.1.11.45 THE POST SHUFFLE, council 3/3 design): this post is RENAMED director-general-1 -> director-goals-1 (design B: it keeps its uid, a fresh key is minted under director-goals-1@agi, belam's order, SM gives the GO per post, DG1 FIRST). After the shuffle: "focus on season 3 improvements".

## §0 State (10-21 ~15:0xZ, gen 27; encryption-town; trunk core/season3/main; crons + keepalive back)
| | |
|---|---|
| post | director-general-1 (about to become director-goals-1): a director, claude-code · parent SM (sanctuary-master) · ~/t is DETACHED at posts/<name>: NEVER `git checkout` in it · card edits: `agi-wt pull doc:card-director-general-1` + edit + agi-turn + agi-flush |
| AFTER THE MOVE | the home is /var/lib/agi/director-goals-1, the worktree branch posts/director-goals-1, mail `AGI_POST=director-goals-1 /opt/agi/bin/box read`, the card doc:card-director-goals-1 (this card's mint id 241494f333d2430abc688586909a2c99 is kept). A NEW Claude session starts (transcripts are keyed by path): THIS CARD is the resume path. My own Claude login stays mine; my ssh key does NOT move (agi-out mints a fresh one at the first start: check `git log --format=%G? -1` is G on my first commit, else tell SM) |
| mail | `box send sanctuary-master <<'EOF' ... EOF`, a QUOTED heredoc (an argv message arrives EMPTY). Box SM ONLY, NEVER belam, ONE message per finished thing, NO acks. Never a host act (belam's GO per act). 'director-general-1:' in git/mail before the move date is this same post, read from the rows' was/became cells |
| roles | DG1 = goals + nodes + JUDGING every return by RUNNING it · DG2 falsifier lanes · DG3/DG4 builders · SM gates + lands (council 3/3 first). After the shuffle the names change (goals-1, science-1, DG3/4/5 -> DG1/2/3); the roles are SM's to say |
| SCRATCH | /data/work/gate-director-general-1/wip (worktrees g123, cap, close80, close81, g123-trunk; all disposable; tmp = TMPDIR). The dir name may change with the uid: re-find it under /data/work/gate-director-goals-1. Cut a send: `git worktree add --lock --detach <dir> <live trunk>`, ONE signed commit, `git push /data/work/agi SHA:refs/heads/dg1-<new name>` (new branch name each time; the old dg1-* branches stay) |
| BOX RULES | NEVER start pytest while SM's gate suite runs (gates wait for 0 pytest peers); SM runs the full suite + lanes on the land tree; for a review-ready I run only the DERIVED set + my rows + mutants, and shell lanes (bare env -i, sh) |

## §1 Plan
```
NOTHING IN FLIGHT, NO TIP OF MINE UNLANDED (K2 met). L29 captive-lock fix, L30 g12.3 closed rows, L32 g12.3 follow-up (idempotent _append_season_row, 490fde78f1 in trunk) are all LANDED.
NEXT: send SM "move-ready" (card sha + open tips = none); on SM's GO stop for the move; after it, box read.
```

## 🔴 Where it stops + the exact next command
After the move: `AGI_POST=director-goals-1 /opt/agi/bin/box read`, then act only on what SM asks.
1. NITS riding my NEXT touch (council 3/3, no return): (a) season.py `_append_season_row`: `int(rows[-1].get("season", -1)) == int(g)` on both sides of the guard + a test row with a ledger {"season": "3"} (mutant: the str compare -> the row is duplicated); (b) goal:g12.3 BODY: the 10-15 'FALSE STATE ... season.py never sets closed' line marked 'FIXED (L30 3a91789da4)'. g12.3 stays ACTIVE (long-term umbrella, never closed as a leaf).
2. goal:g7.16.1.11.20.3 is NOT closed: its falsifier is a LIVE read of SM's after projection. When SM mails the read (or says close on the lanes): ONE signed commit on a worktree of the LIVE trunk "CLOSE .20.3 = 75743e7d06 + falsifiers RE-RUN at <trunk sha>: captive-release 14/0, post-env 33/0, engine-sizes 26/0" (lanes re-run at that sha, bare env -i).
3. Council residues for the NEXT agi-captive edit (none made): n1 `r=;` init (mutant env r=x + fresh window + stub agi-fill -> GATED), n2 a failed mv appends '(rename failed)' (mutant: read-only dir), n3 time the window from `.t` via jq not the mtime (mutant t=now-1000, mtime=now -> released).
4. Parked, nothing queued: goals .11.12 .11.13 .11.15 .11.17 at horizon (.11.13: the aa3 lanes run by the lanes post, then I close it in the standing form). Standing CLOSE form: "CLOSE <leaf> = <sha> + falsifiers RE-RUN at <trunk sha>: <counts>".
HOST ACTS (belam, never mine): alarm_spool install, cron-row `--seat` -> `--post`, crons apply, the sysctl drop-in, boxwake re-projection, and every step of the shuffle (usermod/groupmod, keys, rows).

## §2 Landed this generation (mine, via SM)
memguard stack, slab chain, sysctl-check, fill-line fix, thrash row, boxwake fingerprint, seat-alias fix, the bundle sweep (.11.20/.20.2/.40.1.1/.11.36/.5.3.2 closed), L29 captive-lock, L30 + L32 g12.3 (season_history closed rows + idempotent guard). Detail: git history + the grid.

## §4 Traps (this generation only)
| trap | rule |
|---|---|
| a node edit made via agi-wt/agi-turn on the posts branch | NEVER mailed as a sha for landing: re-cut the final blob as ONE commit on a worktree of the live trunk |
| `box send POST "text"` | arrives EMPTY: a quoted heredoc on stdin |
| a pytest started while SM's gate suite runs | blocks gates: check `ps` first |
| a ledger derivation from `git log --follow` | shows side-branch flip-flops: read `--first-parent` |
| the rollover rule | no commit stages spawn_gate.py, frontmatter.py, .agi/context/schemas/*, engine-post.md; ladder.md only alone in the season bump |
| the shuffle | no gate or land during a move; a land REFUSES a tip signed by a stamped (retired) key dated past its stamp; never carry a private key |

## §5 Verification: every return RUN at the sender's sha, bare `env -i`, nice 10. g12.3 derived set 1808 passed (rc 0); SM's gate106 4069 passed.

## §6 BANKED (to SM's digest; none blocks a build)
- user@-only memory thrash is logged but not noticed (memory_alarm_posts owns the notice).
- Branches I created that cannot be deleted from this uid (leave): the dg1-* ones.
- Banked for the owner (council): should posts mint through captive windows at all, and if so should agi-fill be in post bins (§Y2).
