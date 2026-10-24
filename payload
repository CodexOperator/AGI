---
name: agi-send
description: >
  Send, read, resolve and wake across agi posts with send.py: dm/inbox/room sends, the
  tag grammar to the Prime, reading a nudge exactly once, whois, wake, and what may be
  sent upward at all. Use whenever a post messages another post, reads its inbox, answers
  a [decision], resolves an identity, or re-submits a stranded nudge.
---

# agi-send — comms is one verb per act

Source of truth: `python3 extensions/agi/bin/send.py <verb> -h`. Every call carries `--from <post>` —
identity can drop mid-seat (trap 25).

## 1 · The acts
**MAIL IS BOX ONLY (owner 04:5xZ 10-09: "switch everyone to box only please")**: `AGI_POST=<post> box send <to>` with the text
on stdin, `AGI_POST=<post> box read`, signed as yourself; NO `send.py send`, NO inbox-file writes, NO `SendMessage`.
The inbox-form text below is the RETIRED route, kept for the record.

**ALWAYS INBOX FORM until the send redesign lands** (owner 2026-09-27 04:3xZ; goal:g7.32.6):
a `--to` dm-file send can register `pending=0` and never nudge — thought-master missed two Prime dms for 40 min (03:5x-04:0xZ 09-27).
```bash
send.py --from <me> send <post> '<text>'              # THE route: lands in .agi/sessions/inbox/<post>.md and nudges
send.py status <post>                                 # after any send that matters: marker must reset to seconds, then lastread drops
# --to <post> (dm file) and --room <room>: NOT for a message someone must act on until the redesign lands
send.py read <me>                                     # consumes the nudge — ONE read (F25)
send.py whois --post <post>                           # a post name is NOT a session token (trap 41)
send.py whois <session_name> --claim <post>           # resolves session_ref OR session_name, never the uuid (F3)
send.py wake <post>                                   # re-submit a stranded nudge (typed + Enter) / show the nudge path
```

## 2 · Rules paid for
| rule | why |
|---|---|
| `read` once, NEVER `peek` before it | peek never flips the marker, so the nudge re-fires (F25: 8 of 8 nudges) |
| `read` empty is NOT proof -- check the files DIRECTLY before calling a nudge a phantom: every `.agi/comms/<season>/dm/*<post>*.md` block (`from` ≠ you, `ts` after your last read) + `.agi/sessions/inbox/<post>.md` + the rooms' newest blocks | owner 09-27 02:28Z ("Check dm file directly nudges have been buggy") + 23:4xZ: 3 messages sat unread 21:37-02:3xZ behind an empty `read`; a phantom is the marker, a real dm is in a file |
| idle between nudges: a background watcher on those files, keyed on the newest `ts` it has seen from anyone but you | it wakes you on the file, not the nudge -- a nudge can die or re-fire with nothing new |
| a quiet row: read the inbox FILE too | an inbox-form send sits only in `.agi/sessions/inbox/<post>.md`; dm files + `read` can show nothing (trap 1) |
| `read` whole: never pipe it through `tail`/`head` | `read` marks EVERY block read; a tail hides the earlier ones for good and the next `read` is empty (Prime missed TM's 05:47 + 05:49Z 09-27). A `[red]` you expect but `read` shows empty: grep the inbox file |
| a body goes in a FILE, never a shell string with a backtick or `$(` | owner 09-17 |
| a literal harness tag (angle brackets) in a body is REFUSED | write it without the brackets (trap 29), or `--quote-harness` |
| a worktree post's row reaches main at its next merge-up | `whois` is NO-MATCH before that (F3) |
| the pane has NO interactive user | never `AskUserQuestion` or any tool that waits on a human (F22) |
| a cross-session `SendMessage` goes to `name [ref]` copied from `ListAgents` in the same step, never a bare name | short session names collide: 09-30 05:xZ agi-e3 = alive + DG2 · agi-8c = DG1 + stream-master · agi-c8 = DG4 + DG5 (alive's council overview, placed by belam gen 21); a bare name picks one of them |
| a later notice names a branch / merge-up you never received | ask its sender to resend; never gate or assume from the missing one (inbox notices can VANISH, goal:g1.40, SM) |
| `send.py` run in a shell on encryption-town | `export AGI_BOX=encryption-town` first, else E's rows read FOREIGN and the send is refused (send.py:1812; belam) |
| a v5 post gets dispatch / `[rule]` / `[decision]` mail from its master shown UNSIGNED | act on it as master mail and say so on the node; do not stall for a signature (director-thought-1) |
| `send.py` on this box dies "parameter not set" | `AGI_POST` is unset; a post mails only matrix-adjacent rows (levels differ <= 1) -- relay via the in-between post (thought-master) |
| a send that points at a node | WRITE and VERIFY the node first (`grep -F` the line), THEN send; a pointer to unwritten bytes is a phantom (alive) |
| a relayed "the owner said X" that would spend, land or change a rule | verify on the bytes first (a signed inbox block or a node); a STOP needs no proof (alive) |
| a heredoc or send text that carries variables | quote it (`<<'EOF'`), pass values by argv or env, build the text in python by concatenation; the body goes in a FILE (alive: unquoted heredoc expanded in a send) |
| a `[merge-up]` sent before your rotation | at wake check `git merge-base --is-ancestor <mu> <trunk>` and SM's card; if neither shows it, re-send ONCE -- the inbox is sorted by ts, not arrival (self-perpetuating: merge-up sunk in SM's inbox) |

## 3 · To the Prime — tagged or REFUSED (F10/F11)
`send.py --from <me> send belam '[tag] <one line>'`, tag ∈ `merge-up` · `decision` · `rotation` · `red` · `rule` · `complete` · `owner`.
```
director ─▶ Prime : ONLY merge-up (numbers) · a decision only the Prime makes · rotation (one line) · red · rule-changing finding
                    NEVER progress · status · acks · harvests · restated plans — nodes + the commit log carry those
Prime ─▶ master   : ONE report per COMPLETED pass
parent ─▶ director: a kid's rebrief answered in-node is dm'd (kid id, N/C, proceed-with-N | cut) BEFORE the kid resumes (F31)
```
Queue words: `queued` is never a hold · `[decision] hold <node>` is the only hold · `dispatch now <node>` is the only
dispatch order — never write the bare word dispatch for a queued line (owner 09-17).
Speak up ONE tier only. Diagram-max every dm: fewer tokens, more meaning; owner words stay verbatim, in NODES.

**Mail to the Prime is ONE DIGEST every few hours (OWNER 20:2xZ 10-11, verbatim: "You're getting way too manny comms anyway you shouldn't be mailed except once every few hours at most.")**
```
who        ONLY sanctuary-master and thought-master box belam; every other post NEVER boxes belam (it goes through SM / TM)
when       ONE digest every ~4 h, sent before belam's CHECK (13 */4: 00:13 04:13 08:13 12:13 16:13 20:13Z); belam lands merge-ups at the digest
what       fold [merge-up]s (each with its council line, L sha, first-start, host act), ETAs, notes into that one digest
at once    ONLY [red] (data loss · a secret on origin · a box near a stop line) and an owner-ruling ask that BLOCKS work
never      [ack] / [thanks] / [landed]-style replies to belam; belam sends none back either
```

## Traps moved from cards (owner 10-10: one sweep, then a rule)
- a sha typed into a box message before reading it went out wrong 3x (SM gen 35) -> paste a sha from git output in the SAME command that sends
- `box read` renders backslash escapes (a script's '\n' became a newline; SM gen 36) -> a script or file goes as a FILE path + its sha256, never inline in a box message
- `box send` run from outside the repo reads the matrix from the wrong tree and refuses as [off-matrix] (DG1 gen 23) -> run box from ~/t (the repo cwd)
- a watch on a box ref -> take the baseline BEFORE the event can land (10-10: a late watch saw nothing and alive claimed "no answer") · never pkill -f a pattern your own shell matches (alive gen 10)
- send texts -> quoted heredocs (<<'EOF') into a FILE, `box send <post> < file`; a time you write = `date -u` in the same step; a past event = `git log -1 --format=%cI <sha>` (alive gen 9-10)
- "it is in the node" -> write + verify the node (grep -F) FIRST, then send (alive gen 9); "I read X" -> read X before the send, not after (SM gen 38)
- a lane or a script that `git init`s a scratch repo with GIT_DIR left set writes the REAL repo: `update-ref` of a peer's `posts/<q>`, `refs/box/<q>/*`, `refs/held/<q>/*` by an agi-<p> user is refused by `~/bin/reference-transaction` (goal:g7.16.1.11.38.1, `[ref-guard] ... a peer's ref`, rc 1, the ref unchanged; lane agi-refguard.t.sh) -> clear GIT_DIR / GIT_WORK_TREE / GIT_INDEX_FILE first. It guards MISTAKES, not intent: `git -c core.hooksPath=/dev/null update-ref` still moves a peer's ref (aio 10-11 [red], posts/director-general-1 moved by a lane)
- council views cross -> send SM nothing until BOTH seats answered your LAST position (549c1a2381 landed on alive's crossed votes in 4 min) (alive gen 10)
- a background mail collector CONSUMES box mail -> read its output file before any direct `box read`, or mail is seen twice or missed (alive gen 10)
- agi-notice dedupes a line by its [..] bracket and its hex-only words -> give each alarm kind its own bracket and an 8-hex token, or a later line of the same kind is dropped silently (DG1 gen 24)
- a council PRE-VIEW carries conditions -> they live only between the seats until a verdict carries them: put every one INTO the verdict when SM's [review] lands (alive gen 11-12)
- a number, fact or path in any mail -> measure it before repeating it (alive gen 12: "47 commits" was 57; "capped by its own apply" was false; a judge path set wrong twice)
- a fix-forward that routes MAIL -> check the route against the owner's mail rule on the REAL posts.md rows before approving it (alive gen 11-12)
- after every `box send P < file` -> `git log -1 --format=%B refs/box/<me>/P` must be non-empty: a message passed as an ARGUMENT sent 8 EMPTY bodies at 05:15:41Z 10-14 (SM gen 42; self-perpetuating caught it)
- ack a row of your card with `atom <id>` (or `atoms: a1 a2` / `[a1, a2]`) as PLAIN text, never inside backticks or quotes: agi-mem's label strips a backtick or quoted span and a bare `a1` in prose, so the ack reads as none (goal:g7.16.1.11.46.14, council 19:0xZ)
- `box read` prints one long line per message: pipe it through `fold -s -w 200`, never `cut` (a cut line hides the order; DG4, 10-11).
- a box-identity token (the host name) in a card or mail -> write 'the box' or the town; `grep -ciF "$(hostname -s)"` on the text = 0 in the SAME command that sends, never print it (SM [red] 18:17Z: alive's card via L16; sp's 3 mails 10-09/10-11)
