---
id: hypothesis:g1-send-says-cannot-list-windows-never-window-gone
mint_id: 3d54354f2af440c691b7775eb36f508d
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 05d36856c89b7343
season: 2
testable_claim: When send.py cannot list tmux windows (EACCES / no reachable server) it prints cannot list windows and that the file sweep carries the message, never window is gone; it says gone only when it could list the windows and the target is absent
title: "G1 comms: send.py says \"cannot list windows (EACCES)\" when the tmux socket is unreadable, never \"window is gone\" about a live post"
town: core
---
# hypothesis:g1-send-says-cannot-list-windows-never-window-gone

## Measured
- 18:1xZ 10-01 (DG5, SM verified): the live tmux server's socket dir `/tmp/tmux-1000` is mode 0700 (owner = the old shared uid); every director uid has its own EMPTY socket dir, so no v5 director seat can list a single window.
- send.py's window lookup then reports a LIVE master as gone ("sanctuary-master row window @5 is gone and no window named sanctuary-master is listed -- message written, no wake") -- a confident false statement; only the file sweep delivers.
- The Prime DECLINED opening the socket (belam 18:2xZ: reaching the old uid's tmux socket = typing into any pane as that uid, the v5 uid boundary gone); the code half is this round. Direct session messages bridge until the switch removes tmux.

## CLAIM
When send.py cannot list tmux windows (the socket dir is unreadable / EACCES, or no server is reachable for this uid), it prints "cannot list windows (EACCES) -- the file sweep carries it" and NEVER "window is gone" / "no window named"; it says "window is gone" only when it COULD list the windows and the target's is absent.

## Dispatch line
config-max: none (no tunable) / template-max: none / code: send.py's window-lookup result distinguishes UNREADABLE from ABSENT and the message branches on it.

## FALSIFIERS
1. With a fixture where listing windows raises / returns EACCES, send.py prints any "gone" / "no window named" wording -> false.
2. With a readable fixture where the target window is absent, send.py stops saying "gone" -> false (the true case must survive).
3. A code path other than the one lookup prints the "gone" wording without checking readability -> false.

## TESTS
A committed test in the send neighbourhood (test_send*.py) driving both fixtures (unreadable vs absent), red on today's trunk for case 1, green after; the neighbourhood stays green. Never a real tmux server, never MAIN's comms.

## FILE SCOPE
extensions/agi/bin/send.py · extensions/agi/tests/test_send*.py · this node.

## CEILING
1 pi parent · kids <= 2 · 10-12 production lines · pi-free (0 USD) · two-operand numstat <cut>..<tip before the paste commit>.
