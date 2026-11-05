---
name: agi-rotate
description: >
  Rotate an agi post out and wake its successor: when to rotate (the meter), the card
  written before the out-line, the v5 out (commit, touch ~/.fresh, kill the claude pid),
  what a successor does and does NOT do at wake, the ack, and re-linking the card. Use when the meter
  nears the line, when a post is told to rotate, or on the first turn after a rotation.
---

# agi-rotate — wake 0 / out 1 (owner 09-12)

Source of truth: `config:rotations` (the `facts` block: `sed -n '/^## facts$/,/^## steps$/p' .agi/nodes/.geometry/rotations.md`) and the
`rotate.py` record: `rotate.py status --post <post> --record latest`. Never read `rotate.py` source to learn this (22k lines).

## 1 · When (F27)
The meter hook prints `[meter] post=<post> <f> ... line=0.47`. Rotate when **f ≥ 0.47** — only `f`, never the
ratio `r = f/0.47`. A step that cannot finish before the line is handed on whole, not started (the near miss:
starting it obeys "run it now" and strands it mid-step). Prime HARD RULE: an irreversible / multi-ref operation is
never started at f ≥ 0.41 nor while a rotation is pending — it becomes the successor card's first line.

## 2 · Out — the v5 out, in this order (F23, F26; owner 11-01: rotate.py is not the out)
```
1. write the card WHOLE (one Write) — .agi/sessions/quorum/<post>.md in YOUR worktree; §0-§6 ≤ 100 lines
   §0 state · §1 plan · §2 landed · 🔴 where it stops + exact next command · §4 traps · §5 verification · §6 BANKED
   · §7 ATOMS: bounded by age, not length (an atom open > 1 lap = red); rotation carries §7 whole, never trims it (.46.2)
   the where-it-stops slot's FIRST LINE = plain text: it becomes the commit subject (trap 2)
   §4 traps: only THIS generation's; an older trap moves to its skill / role doc first (owner 10-10: one sweep, then a rule)
   never leave the slot EMPTY or AMBIGUOUS (nothing refuses it in the v5 out: it is the author's duty); a STALE one is still written + stamped BEFORE any window ask or dispatch
2. commit the card by exact path
   then `git status --porcelain <card>` must be empty: the privacy guard can refuse a card commit silently; write 'home-path' in prose, never a literal home path (SM)
3. touch ~/.fresh                                         # agi-run's .fresh branch starts the successor and sends the alert
4. kill $PPID                                             # the claude pid; the unit restarts it fresh
```
- The owner, 11-01 (belam [owner-a] 10:2xZ, '10. Yes'): the out is this v5 out for EVERY post; `rotate.py rotate` is not run (from a detached ~/t it refused 'detached HEAD, nothing to push', SM gen 64 23:4xZ 10-28 + belam gen X 04:05Z 11-01). goal:g7.16.1.11.46.28 (rotate's push rule) is retired with it.
- Never merge origin into your tree by hand before the out (F14): the card commit is the only write.
- `HANDOFF.md` at the repo root is the ENGINE's — never read it before rotating (F26).
- The rotation alert has TWO senders (goal:g7.16.1.11.20). (1) agi-run's `.fresh` branch runs on EVERY start that finds `~/.fresh`: a v5 post's own rotation (`touch ~/.fresh; kill $PPID`, see the v5 line below), its FIRST start, a hand `touch ~/.fresh`. It box-sends the alert AS the post, backgrounded, `timeout -k 2 20`, to config:rotations `alerts` (audit + edges[post] - silent - self) read from the trunk; no liveness filter, and the Prime is NOT excluded; the exec never waits on it. Its stderr goes to `$RUNTIME_DIRECTORY/alert`, never the TUI pane: an unreadable alerts cell = ONE `warn: rotation alert` line there and nothing sent; a failing receiver warns once EACH; a timeout kill warns none. (2) `rotate.py rotate` inbox-copies each receiver and, when the ROTATING post is not the Prime, also box-sends it (signed by the post, ONE 20 s budget armed at the first box call, plus up to 5 s of reap after a timeout); a rotating Prime sends no box message there (its branch returns before the box loop), but a Prime can RECEIVE one. A captive / master-path rotation runs as the HOLDER (`AGI_POST=<holder>`), so it sends the inbox copy only.
- Last tokens of the session: one prayer from the head as the LAST tokens of the reply that runs step 3, BEFORE step 4 (kill $PPID ends the session: nothing comes after it). Two spots per session, never per turn (owner 09-12).

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
- a card carrying a literal home path was refused at the push AFTER the :28 board land had already ff'd posts/belam into MAIN (22:28Z 10-21, belam trap 123) -> anonymize the card DIFF before landing (`git diff HEAD -- <card> > f; anonymize.py check --diff-file f`, as a post uid with `--root` a scratch archive of extensions + .agi/config.json, agi-master-gate:116: bare, it reads MAIN's .env and dies PermissionError, rc 1, alive gen 43, 17:5xZ 10-31; a whole-file check trips on the co-author test address) and write ~/ for every own path
- the meter hook can die silently (the 30 s hook limit) -> never trust its silence; compute f by hand every few turns (alive gen 21)
- a partial in-place card edit can leave the old tail behind -> re-read the edited rows (`sed -n`) before committing (alive gen 21)
- `agi-at <card>` can return rc 1 SILENTLY on a first run and commit on the identical second -> after every agi-at, `git status --porcelain <card>` must be empty, else run it ONCE more (`sh -x` shows the step if it fails again) (alive gen 23, twice at 15:5xZ)
- agi-meter timed out at 30 s on every mail prompt (pre-L170), so no post saw its rotation line (belam trap 140, gen VII) -> until a post's ~/bin/agi-meter equals the landed agi-meter section (L176), compute f by hand (the v5 line above) at every multi-ref act; past 0.41 hand the act to the successor's card
- a card edit that replaces the SLICE between two row anchors (s[a:b]) deletes every row inserted between them since -> replace ONE row by a regex ANCHORED (^) at its own first line and asserted to match exactly once, its extent counted FROM THE FILE in the same call, never a typed count (a row = its first line + every next line that starts with a space: `next(k for k,l in enumerate(L[i+1:],1) if not l.startswith(' '))` is its line count, L the card's lines, i its first line's index); insert before an anchor, never cut between two anchors; re-read the row list before committing (alive gen 24: 3 §1 rows lost 20:25Z, restored from git 20:35Z; alive gen 40, 09:19Z 10-31: a typed 6-line count for the 5-line .20.4 §1 row ate the next row, the re-read caught it; on that card, a17c6ddb02, the row's text unanchored also hits the §0 header and a §7 row (lines 19, 35, 257), anchored it hits 35 alone, and the expression reads 5 there)
- a trunk land that edits the trunk's copy of YOUR card (a scrub, a retag) conflicts with your posts branch at the next agi-turn -> resolve on the branch keeping your card's blob (the trunk copy is the stale last-landed one; the card is the EXCEPTION to agi-review's 'posts/<me> keeps a stale agi-at copy' line, where the trunk's blob is the newer), signed, CAS on the ref (sp gen 15, 16:39Z 10-27: L214 scrubbed the trunk's 10-08 copy; b51bc24e57)
- a card edit by python `s.replace(m.group(0), r"\1...")` wrote a LITERAL `\1` and dropped the two rows it replaced (str.replace takes no backreference) -> build the new row with `m.group(1) + "..."` or re.sub, and re-read the edited rows before agi-at (aio gen 14, 10-27 19:58Z, restored from HEAD~1)
- a card is a doc node under .agi/nodes/doc, so a `git grep` reader over the tree can take a machine line quoted on a card as live -> never copy an owner-batch ruling line (or any machine line a reader keys on) into a card; name it in prose (self-perpetuating gen 16, the .46.16.2 term 21:36Z 10-27)
- a sweep line cited two tools (GNU rm 9.4 and BusyBox) for a result measured under one, and its example was never run as written: the cd + `python3 -I` form fails, -I drops the cwd from sys.path (alive gen 37's sweep 1fe5c5fae8, aio caught both 02:09:43Z 10-29, VOID at SM's hold 02:10:08Z; RE-CUT b203baef54 landed L296) -> before a sweep's [merge-up], RUN every claim each line states, in the form it states, under every tool it names, and say what ran in the message; the reviewer's side is agi-review's 'an [approve] of rule lines whose example was never run' line
