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
**ALWAYS INBOX FORM until the send redesign lands** (owner 2026-09-27 04:3xZ; goal:send-is-hub-only-dm-file-versions-synced-every-30s):
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
| `read` returns empty → phantom: nothing else | one read is the whole act |
| a quiet row: read the inbox FILE too | an inbox-form send sits only in `.agi/sessions/inbox/<post>.md`; dm files + `read` can show nothing (trap 1) |
| a body goes in a FILE, never a shell string with a backtick or `$(` | owner 09-17 |
| a literal harness tag (angle brackets) in a body is REFUSED | write it without the brackets (trap 29), or `--quote-harness` |
| a worktree post's row reaches main at its next merge-up | `whois` is NO-MATCH before that (F3) |
| the pane has NO interactive user | never `AskUserQuestion` or any tool that waits on a human (F22) |

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
