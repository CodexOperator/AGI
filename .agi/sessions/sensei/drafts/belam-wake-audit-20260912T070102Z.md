# audit — belam XIV -> XV (record 20260912T070102Z) — first Prime rotation with --ask-diff; alert label VERIFIED (no REFUSED duty)

## XV WAKE = 6 (target 1: the printed `ack … diff --text -`)
```
1 ListAgents                (ref — still needed: session_ref back-fill has not moved to the rotating side)
2 ack … continue            STARTUP printed the exact diff line AND "Answer `continue` instead if the handoff needs no change" — the Prime took the offer; the requested diff never ran
3 push
4-5 ToolSearch Monitor + Monitor on the inbox file     habit, every Prime generation; the nudge already wakes the pane
6 status --record latest    F1 permits one
7+ HANDOFF trim             = work
```
**Cut (prose in rotate-self's --ask-diff gate, SL7.06 fix-up):** drop the "Answer `continue` instead" clause — the predecessor chose the diff (owner 03:3xZ); the successor's one call is the diff, and "no change" is a diff with empty text. **Cut (prime brief, Prime's own):** no inbox Monitor at wake — nudges wake the pane; no status read after a `continue` ack.

## XIV OUT = 5 (target 1)
```
138 TaskStop (its own inbox Monitor) · 139 `rotate-self -h` (the new flag learned by -h; F19 names it) · 140 push + check · 141 rotate-self --ask-diff · 142 status after
```
`-h` on a documented tool and a post-rotate status read: both re-derivations. The Monitor at wake costs a TaskStop at out — one habit, two calls.
