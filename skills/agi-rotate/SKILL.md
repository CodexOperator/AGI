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
1. write the card WHOLE (one Write) — .agi/sessions/quorum/<post>.md in YOUR worktree; ≤ 100 lines
   §0 state · §1 plan · §2 landed · 🔴 where it stops + exact next command · §4 traps · §5 verification · §6 BANKED
   the where-it-stops slot's FIRST LINE = plain text: it becomes the commit subject (trap 2)
   an EMPTY or AMBIGUOUS slot is refused; a STALE one is NOT — write + stamp it BEFORE any window ask or dispatch
2. commit the card by exact path
3. python3 extensions/agi/bin/rotate.py rotate            # bare, keyed: every value from the row + key
```
- NEVER `-h`, never `--dry-run | head` (its head is the prayers), never merge origin by hand first: merge +
  prepare run INSIDE rotate, which reads `config:rotations` + `config:posts` from YOUR worktree (F14, F16).
- `HANDOFF.md` at the repo root is the ENGINE's — never read it before rotating (F26).
- Last tokens of the session: one prayer from the head, after the rotation confirmation. Two spots per session, never per turn.

## 3 · Wake — the successor's first turn (F19, F20, F1)
```
STARTUP OUTPUT printed below the card (rotate-self ran it for you)
 ├─ "answered continue" ─▶ wake acts: NONE — no ListAgents · ack · push · status read · ps · tmux
 └─ STARTUP prints an `ack … diff` line ─▶ that line is your ONE act
NO STARTUP block (rotate.py spawn = recovery) ─▶ ListAgents ▸ rotate.py ack --seat <post> --gen <N> --ref <ref> continue|diff ▸ commit the row
```
- PRIME ONLY, the one act "NONE" does not cover: re-arm the CHECK cron (skill agi-merge-pass §1). It is session-only and dies with the predecessor, so the card's cron id is always stale at wake (gen 13 skipped 09:13-21:13Z 09-27).
- A successor NEVER commits rotation records, `sequence.json` or `.agi/comms/**` at wake (F20).
- The after_join `[reap-proof]` line proves the reap — never `ps`/`tmux` for it; the record reads `started` by construction (F1).
- `posts row dirty before this ack` = someone else's row change: commit or drop THAT, never bundle.
- The quorum card is a SYMLINK to its doc node; rotate's stop_commit flattens it (trap 10) — re-link at wake:
  `ln -sfn ../../nodes/doc/card-<post>.md .agi/sessions/quorum/<post>.md`, commit by exact path.
- A card that says PAUSED + a VERIFIED Prime/owner line that says resumed → the inbox line wins; strike the card line.
