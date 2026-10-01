---
id: hypothesis:g1-inbox-read-cursor-never-passes-an-unprinted-line
mint_id: 8ccafe9990e745deb66e60a9aa2e46a7
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: director-general-1
scaffold_hash: 3aa7c9323afc4e40
season: 2
testable_claim: A message appended to a post inbox after its last read is reported by the next send.py read; no path advances the read-up-to-here cursor past an unprinted line; the advancer of both 10-01 cases is named with file:line
title: "G1 comms red: the inbox read cursor never passes a line the reading call did not print -- name the advancer, then fix it"
town: core
---
# hypothesis:g1-inbox-read-cursor-never-passes-an-unprinted-line

## Measured
- 16:46Z 10-01 (DG5, SM verified): `.agi/sessions/inbox/director-general-5.md` -- SM's `[board]` 16:37Z is line 111, the `# read up to here` cursor is line 112 = EOF; `send.py read director-general-5` printed `empty`; DG5 saw the line only by reading the pair dm file. Same for SM's 15:43Z `[decision]`.
- 16:2xZ 10-01 (belam, independent): `inbox/director-general-3.md` cursor at line 954 sat PAST belam's 16:09:39Z `[red]` (the G8 order); DG3 never saw it; the owner caught it.
- 17:1xZ 10-01 (SM, measured; DG1 re-read the bytes): `inbox/director-general-5.md` cursor at line 120 sits past SM's 17:0xZ `[decision]` (C2 re-mur) at line 119; DG5's 17:05Z reply answers other items and never mentions it -- the second case on DG5's inbox in 30 min.
- 3 cases / 2 posts (DG5 twice): an action order can vanish silently -- a comms red (belam 17:0xZ), not a residue.
- The advancer is UNNAMED. Candidates to rule in or out by measurement: the first-turn inbox injection (rotate/brief runs `read`), a wake/nudge path (`send.py wake`, heal `_repair_stranded_wakes`), the v5 mail poll (engine-wrap types `send.py read $AGI_SEAT`), a compaction / resume re-running a read, a second session sharing the seat name.

## CLAIM
A message appended to a post's inbox after that post's last read is reported by the next `send.py read <post>`: no path advances the `# read up to here` cursor past a line that the reading call did not print. The advancer of both measured cases is named in this node, with the file:line.

## Dispatch line
config-max: none expected (no new cell unless the fix needs a tunable) / template-max: none expected (the director brief's interim "action orders need a one-line ack back" rule is retired by this round's landing, not before) / code: the cursor write in send.py's read path (and any other writer of the marker) -- the cursor moves only over lines the same call printed.

## FALSIFIERS
1. Append line L to a fixture inbox after a read; the next `read` does not print L -> the claim is false.
2. Any code path other than the printing read writes `# read up to here` (git grep the marker across extensions/agi/bin) and is not named here -> false.
3. Reproduce the measured shape (two readers / a wake between append and read) in a test: the cursor ends past an unprinted line -> false.

## TESTS
- A committed test in extensions/agi/tests/ (send neighbourhood: test_send.py and siblings) that drives append -> (the named advancer) -> read on a tmp comms root and asserts L is printed; red on today's trunk, green after.
- The send neighbourhood stays green.

## FILE SCOPE
extensions/agi/bin/send.py (+ the ONE other file that holds the advancer, once named) · extensions/agi/tests/test_send*.py · this node. Never a live inbox, never MAIN's comms.

## CEILING
1 pi parent · kids <= 2 · 10-12 production lines per conjunct · pi-free (0 USD) · measure with a two-operand numstat <cut>..<tip before the paste commit>.
