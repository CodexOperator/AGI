---
name: agi-rotate
description: >
  Rotate an agi post out and wake its successor: when to rotate (the meter), the card
  written before the out-line, the one bare `rotate.py rotate` command, what a successor
  does and does NOT do at wake, the ack, and re-linking the card. Use when the meter
  nears the line, when a post is told to rotate, or on the first turn after a rotation.
---

# agi-rotate — wake 0 / out 1 (owner 09-12)

Source of truth: `config:rotations` (the `facts` block: `write.py config:rotations 'read body 37:64'`) and the
`rotate.py` record: `rotate.py status --post <post> --record latest`. Never read `rotate.py` source to learn this (22k lines).

## 1 · When (F27)
The meter hook prints `[meter] post=<post> <f> ... line=0.47`. Rotate when **f ≥ 0.47** — only `f`, never the
ratio `r = f/0.47`. A step that cannot finish before the line is handed on whole, not started (the near miss:
starting it obeys "run it now" and strands it mid-step). Prime HARD RULE: an irreversible / multi-ref operation is
never started at f ≥ 0.41 nor while a rotation is pending — it becomes the successor card's first line.

## 2 · Out — ONE command, in this order (F23, F26, F14)
```
1. write the card WHOLE (one Write) — .agi/sessions/quorum/<post>.md in YOUR worktree; §0-§6 ≤ 100 lines
   §0 state · §1 plan · §2 landed · 🔴 where it stops + exact next command · §4 traps · §5 verification · §6 BANKED
   · §7 ATOMS: bounded by age, not length (an atom open > 1 lap = red); rotation carries §7 whole, never trims it (.46.2)
   the where-it-stops slot's FIRST LINE = plain text: it becomes the commit subject (trap 2)
   §4 traps: only THIS generation's; an older trap moves to its skill / role doc first (owner 10-10: one sweep, then a rule)
   an EMPTY or AMBIGUOUS slot is refused; a STALE one is NOT — write + stamp it BEFORE any window ask or dispatch
2. commit the card by exact path
   then `git status --porcelain <card>` must be empty: the privacy guard can refuse a card commit silently; write 'home-path' in prose, never a literal home path (SM)
3. python3 extensions/agi/bin/rotate.py rotate            # bare, keyed: every value from the row + key
```
- `rotate.py rotate` refuses 'behind origin/season2/main by N' -> never merge origin into your tree by hand; `[red]` to SM and stay seated below the line (DG2).
- NEVER `-h`, never `--dry-run | head` (its head is the prayers), never merge origin by hand first: merge +
  prepare run INSIDE rotate, which reads `config:rotations` + `config:posts` from YOUR worktree (F14, F16).
- `HANDOFF.md` at the repo root is the ENGINE's — never read it before rotating (F26).
- The rotation alert has TWO senders (goal:g7.16.1.11.20). (1) agi-run's `.fresh` branch runs on EVERY start that finds `~/.fresh`: a v5 post's own rotation (`touch ~/.fresh; kill $PPID`, see the v5 line below), its FIRST start, a hand `touch ~/.fresh`. It box-sends the alert AS the post, backgrounded, `timeout -k 2 20`, to config:rotations `alerts` (audit + edges[post] - silent - self) read from the trunk; no liveness filter, and the Prime is NOT excluded; the exec never waits on it. Its stderr goes to `$RUNTIME_DIRECTORY/alert`, never the TUI pane: an unreadable alerts cell = ONE `warn: rotation alert` line there and nothing sent; a failing receiver warns once EACH; a timeout kill warns none. (2) `rotate.py rotate` inbox-copies each receiver and, when the ROTATING post is not the Prime, also box-sends it (signed by the post, ONE 20 s budget armed at the first box call, plus up to 5 s of reap after a timeout); a rotating Prime sends no box message there (its branch returns before the box loop), but a Prime can RECEIVE one. A captive / master-path rotation runs as the HOLDER (`AGI_POST=<holder>`), so it sends the inbox copy only.
- Last tokens of the session: one prayer from the head, after the rotation confirmation. Two spots per session, never per turn.

## 3 · Wake — the successor's first turn (F19, F20, F1)
```
STARTUP OUTPUT printed below the card (rotate-self ran it for you)
 ├─ "answered continue" ─▶ wake acts: NONE — no ListAgents · ack · push · status read · ps · tmux
 └─ STARTUP prints an `ack … diff` line ─▶ that line is your ONE act
NO STARTUP block (rotate.py spawn = recovery) ─▶ ListAgents ▸ run the ack line you were handed (config:rotations `recovery_ack`) ▸ commit the row
```
- PRIME ONLY, the one act "NONE" does not cover: re-arm the CHECK cron (skill agi-merge-pass §1). CronList FIRST: a `--resume` RESTORES a session's old CronCreate jobs (gen 19's pre-reboot STOP + CHECK fired again in the idle agi-c2 at 04:43Z 09-30), and the post rotating OUT CronDeletes its own. It is session-only and dies with the predecessor, so the card's cron id is always stale at wake (gen 13 skipped 09:13-21:13Z 09-27).
- A successor NEVER commits rotation records, `sequence.json` or `.agi/comms/**` at wake (F20).
- The after_join `[reap-proof]` line proves the reap — never `ps`/`tmux` for it; the record reads `started` by construction (F1).
- `posts row dirty before this ack` = someone else's row change: commit or drop THAT, never bundle.
- The quorum card is a SYMLINK to its doc node; rotate's stop_commit flattens it (trap 10) — re-link at wake:
  `ln -sfn ../../nodes/doc/card-<post>.md .agi/sessions/quorum/<post>.md`, commit by exact path.
- A card that says PAUSED + a VERIFIED Prime/owner line that says resumed → the inbox line wins; strike the card line.
- recovering a crashed seat: run `git ls-files --others` for its untracked mints before re-minting any node; `git ls-files` alone hides them (DG1).
- v5 post (no meter hook): f = newest usage in `~/.claude/projects/*/<session>.jsonl` (input + cache_read + cache_creation) / 1e6; at 0.47: card whole + commit + `touch ~/.fresh` + `kill $PPID` (thought-master).
- a whole-card replace -> keep `tags: []`; commit the card by agi-at (Door 1); at the rotation write it in the agi-wt tree, then agi-flush (alive gen 10).
- After a turn your ~/t is DETACHED: a plain `git commit` is refused (`[detached]`); commit the card or a node with `agi-at <path>` (DG4, 10-11).

## Traps moved from cards (owner 10-10: one sweep, then a rule)
- belam (the pushing seat): the rotation / restart rewrites ~/.gitconfig WITHOUT the github credential lines: the push fails 'could not read Username' -> at wake `git config --global --get-all credential.https://github.com.helper` must print '' then `!sudo -n -u belam /usr/bin/gh auth git-credential` (the token lives in uid belam; a plain gh line fails); else `--add` both, then `git push --dry-run` (belam gen II, again at gen IV's wake)
- a card carrying a literal home path was refused at the push AFTER the :28 board land had already ff'd posts/belam into MAIN (22:28Z 10-21, belam trap 123) -> anonymize the card DIFF before landing (`git diff HEAD -- <card> > f; anonymize.py check --diff-file f`; a whole-file check trips on the co-author test address) and write ~/ for every own path
