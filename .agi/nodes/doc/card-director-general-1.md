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

## OVERALL GOAL (owner 10-08): encapsulation of grid slices, belam on the new engine, then the season rollover. DONE 10-15: season 3 is rolled (SM notice 06:29Z), all 12 posts restarted on AGI_TRUNK=core/season3/main. Progress is read on town:local-maxxing 'Engine rework trajectory'.

## §0 State (10-16 ~12:1xZ, gen 26; encryption-town; trunk core/season3/main; OWNER PAUSE 12:0xZ: "Pause and let everyone go idle now. We are out of use" + crons and keepalive: start nothing new (no dispatch, gate, review, merge-up, spend, mint); no reply needed)
| | |
|---|---|
| post | director-general-1: a director, claude-code, engine v5 · parent SM (sanctuary-master) · ~/t is DETACHED at posts/director-general-1: NEVER `git checkout` in it · card edits: `agi-wt pull doc:card-director-general-1` + edit + agi-turn + agi-flush (the pull dir vanishes after agi-turn: a harmless getcwd error) |
| mail | `AGI_POST=director-general-1 /opt/agi/bin/box read` (send: `box send sanctuary-master <<'EOF' ... EOF`, a QUOTED heredoc; an argv message arrives EMPTY). Box SM ONLY, NEVER belam, ONE message per finished thing, NO acks. Never a host act (belam's GO per act). |
| roles | DG1 = goals + nodes + JUDGING every return by RUNNING it · DG2 falsifier lanes · DG3/DG4 builders · SM gates + lands (council 3/3 first; a send addressed to the council needs no reply from me) |
| SCRATCH | /data/work/gate-director-general-1/wip: worktrees g123 (stack), cap (captive), close80 (trunk 7965c4fe8c), g123-trunk (a detached trunk for lane diffs); tmp = TMPDIR; scratchpad lane.sh/derive.py under the session scratchpad. Cut a send: `git worktree add --lock --detach <dir> <live trunk>`, ONE signed commit, `git push /data/work/agi SHA:refs/heads/dg1-<new name>` |
| BOX RULES | NEVER start pytest while SM's gate suite runs (gates wait for 0 pytest peers; find by comm + cwd, stop by TERM); SM runs the full suite + all lanes on the land tree; for a review-ready I run only the DERIVED set + my rows + mutants, and shell lanes (bare env -i, sh) |

## §1 Plan
```
SENT, WAITING ON THE COUNCIL: goal:g12.3 STACK (season_history closed rows): branch dg1-g123 tip 3882925f10, 7 G commits on trunk 4248324248; gate99 GREEN (9212 passed, 58 lanes 0 FAIL); SM agrees with my two calls (no 100-s sanctuary season-1 row; the season-3 rows keep the rollover's own opened). On APPROVE SM lands it as L30. HOLD THE BRANCH UNCHANGED.
LANDED: goal:g7.16.1.11.20.3 captive-lock fix (L29 7965c4fe8c, 75743e7d06, 3/3; engine-wrap.md agi-captive 576 -> 1005 B, lane captive-release.t.sh 14/0, post-env e4 stubs agi-fill).
```

## 🔴 Where it stops + the exact next command
Nothing in flight, nothing unsent. NEXT after the pause lifts: `AGI_POST=director-general-1 /opt/agi/bin/box read`.
1. g12.3 landed (L30)? Then CLOSE it in the standing form, ONE signed commit on a worktree of the LIVE trunk (status complete + a THOUGHT; the goal id is goal:g12.3): "CLOSE g12.3 = <sha> + falsifiers RE-RUN at <trunk sha>: <counts>". Re-run at the LANDED trunk: `python3 -m pytest extensions/agi/tests/test_season_rollover_global.py extensions/agi/tests/test_season_rollover_align.py -k g123 -q` (3 rows + the align row, each mutant RED) and the live-nodes row = 0 violations. A RED comes back as one fix commit.
2. goal:g7.16.1.11.20.3 is NOT closed: its own falsifier (no post locked with a window open and no agi-fill = 0) is a LIVE read, SM's, once the piece is projected to the posts (my ~/bin/agi-captive was still the OLD 576 B at 10-16 11:5xZ). When SM mails the read (or says close on the lanes): CLOSE .20.3 = 75743e7d06 + lanes captive-release 14/0, post-env 33/0, engine-sizes 26/0 re-run at the trunk sha.
3. Council residues for the NEXT agi-captive edit (none made): n1 initialise `r=;` first (mutant env r=x + fresh window + stub agi-fill -> GATED), n2 a failed mv appends '(rename failed)' to the line (mutant: read-only dir), n3 time the window from `.t` via jq, not the mtime (mutant t=now-1000, mtime=now -> released).
4. Parked, nothing queued: goals .11.12 .11.13 .11.15 and .11.17 at horizon (.11.13: DG2 runs the 17 aa3 lanes, then I close it in the standing form).
HOST ACTS (belam, never mine): install alarm_spool.py to /opt/agi/bin, the two cron rows `drain --seat` -> `--post`, crons.py apply, the sysctl drop-in, agi-project re-projection of the boxwake fingerprint.

## §2 Landed this generation (mine, via SM)
memguard stack, slab chain, sysctl-check, fill-line fix, thrash row, boxwake fingerprint, seat-alias fix, the bundle sweep (.11.20/.20.2/.40.1.1/.11.36/.5.3.2 closed, .4 .4.3 .11.17 horizon), L29 the captive-lock fix. Detail: git history + the grid.

## §4 Traps (this generation only)
| trap | rule |
|---|---|
| a node edit made via agi-wt/agi-turn on the posts branch | NEVER mailed as a sha for landing (drags the post history): re-cut the final blob as ONE commit on a worktree of the live trunk |
| `box send POST "text"` | the message arrives EMPTY: use a quoted heredoc on stdin |
| a pytest started while SM's gate suite runs | blocks gates (they wait for 0 peers): check `ps` first; stop by TERM on the pid whose cwd is mine |
| a test that runs a gate in an env with no helper on PATH | a release-when-absent gate passes it: put the stub helper on PATH (post-env e4) |
| a ledger derivation from `git log --follow` | shows side-branch flip-flops: read the trunk's `--first-parent` line |
| the rollover rule | no commit may stage spawn_gate.py, frontmatter.py, .agi/context/schemas/*, engine-post.md; ladder.md only alone in the season bump |

## §5 Verification: every return RUN at the sender's sha, bare `env -i`, tree and basetemp on DISK, nice 10. g12.3 derived set 1824 passed; captive lanes 14/0 14/0.

## §6 BANKED (to SM's digest; none blocks a build)
- user@-only memory thrash is logged but not noticed (memory_alarm_posts owns the notice).
- Branches I created that cannot be deleted from this uid (leave): the dg1-* ones.
- Banked for the owner (council): should posts mint through captive windows at all, and if so should agi-fill be in post bins (§Y2).
