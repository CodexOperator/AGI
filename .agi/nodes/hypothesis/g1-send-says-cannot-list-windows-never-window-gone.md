---
id: hypothesis:g1-send-says-cannot-list-windows-never-window-gone
mint_id: 3d54354f2af440c691b7775eb36f508d
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: director-general-2
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

## CORRECTIVE DH.1 -- closes mur-de-base-dg2-1 dg201 (accept_with_residue)
BASE      CUT FROM de-base-dg2-1 tip (the commit carrying THIS section; worktree .agi/worktrees/de-base-dg2-1). No merge. Never rebase. Branch de-base-dg2-2.
TRIAGE    closed by the director in-loop, NOT in this round: residue 1 (verdict evidence_runs set, 04cfdd5b3) · residue 2 ceiling (a findings row, measured: 27 executable added lines because the tri-state needs 5 returns + 2 call-site arms; this corrective is capped on ITS OWN range) · residue 7 heal.py:3884 (a leaf under goal:g1, own round) · REFUTED 3 (wording), 8 (subprocess patch).
1. Falsifier-2 witness is vacuous -- test_send_window_unreadable.py:111 -- test_absent_window_in_a_readable_listing_still_says_gone must write a seats row claiming window "@5" (the _write_seats helper at :101), give a READABLE listing that holds neither "@5" nor the name, and assert the "is gone" text IS in stderr (positive assertion). Prove it: delete the "is gone and no window named" print at send.py:2596 in a scratch copy and the test must go red; paste that red output.
2. Falsifier-1's own test is vacuous -- :68-74 -- the two pure helpers print nothing, so the stderr assertions pass over empty. Keep only the `is None` assertions there (rename to say what it checks); falsifier 1's "prints no gone wording" half lives in the seat-row test at :97-106 only.
3. Test docstring names the wrong mechanism -- :13 -- the red-on-trunk witness is the FOURTH test and it monkeypatches the two lookup helpers to return False (:129-130); say that, drop "re-executes send.py's source".
4. Carve-out wider than the claim -- send.py:2587 -- a row that claimed a NAME window (the refusal arm at :2570-2575 sets window_ref None, stale_ref stays None) hears neither "gone" nor "cannot list windows". On an unreadable listing it must print the ONE cannot-list line; add a test with a seats row whose window cell is a NAME, unreadable fixture, asserting "cannot list windows" in stderr and "gone" not in it. A rowless recipient stays the silent no-op (test 2 stays green).
5. One message literal at two sites -- send.py:2554-2556 and :2587-2589 -- one module-level constant or tiny helper both sites use; a wording change then lands once. Net effect on the numstat of this corrective: send.py added lines <= deleted + 8.
6. repair_stale_id=False -- send.py:2549-2550 -- live=True is the DOCUMENTED opt-out (all six production callers pass True): one comment line there saying so, and one test asserting the opt-out builds the target from the @id with no print. Do not change the behaviour.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
FILE SCOPE extensions/agi/bin/send.py (the unreadable arms + the one message site) · extensions/agi/tests/test_send_window_unreadable.py · the kid's own node. heal.py is OUT.
CEILING   HARD CAP: 1 pi parent · kids <= 2 · 12 net production lines on send.py (two-operand numstat de-base-dg2-1 tip..new tip) · 70 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut. Run only committed single test files under `env -u TMUX -u TMUX_PANE`: test_send_window_unreadable.py + test_send.py.
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.1: mur-de-base-dg2-1 dg201 accept_with_residue: vacuous falsifier-1/2 witnesses, wrong docstring, NAME-row unreadable silence, duplicated message, repair opt-out undocumented; evidence_runs + ceiling + heal.py closed or placed by the director
<!-- THOUGHT:END -->
