---
id: hypothesis:l4-authority-verified-against-the-graph-not-the-message
mint_id: 9c596ec9f5ec4ed2a020a6a932461b59
type: hypothesis
parents:
  - hypothesis:l4-the-meter-pinned-another-sessions-transcript
  - goal:g17.1
next_edges: []
edited_by: sanctuary-director
scaffold_hash: b40dfde03d0857c2
season: 2
status: pending
tags:
  - l4
  - g17.1
  - seats
  - identity
  - send
  - fail-closed
testable_claim: "A SEAT CANNOT TELL A GENUINE ROTATED PRIME FROM A STRANGER, BECAUSE THE ONLY EVIDENCE EITHER OFFERS IS A NAME AND A WINDOW, AND BOTH ARE TRIVIALLY CLAIMABLE. Measured, live, today: the outgoing helper verified that `agi-7f` is window @239 `belam-S1-L4-III`, concluded that is 'not part of this three-seat formation at all', and declined to treat the prime's instruction as authoritative. **The conclusion was wrong and the behaviour was correct** -- the prime ruled it that way deliberately, because a seat that cannot authenticate an instruction SHOULD verify independently rather than comply, or the next seat complies with a real impersonator. THE PRIME'S FIX IS NOW PROTOCOL AND NEEDS NO NEW MACHINERY: **AUTHORITY IS VERIFIED AGAINST THE GRAPH, NEVER AGAINST THE MESSAGE.** `config:seats` (`.agi/nodes/.geometry/seats.md`) carries every seat's `session_ref`; it lives in a PUSHED commit on `season/s2`; `write.py` and the `written_by` gate refuse a writer whose role is not admitted, so a stranger cannot mint a seats row. REQUIRED: **make that lookup a CHECK rather than a habit** -- a `whois` subcommand on `send.py` that resolves a claimed identity against `config:seats` and answers is-this-who-they-say, both directions: given a `session_ref`, name the seat and role it belongs to; given a claimed role or seat name plus a ref, answer whether that ref IS the row for it. I did the lookup by hand three times today before trusting three different senders; a rule kept in a seat's head is a coin flip by this project's own doctrine, which is the whole reason this is a round. 🔴 THE CRUX, AND IT IS WHY THIS IS NOT A FIVE-LINE HELPER: **IT MUST READ THE PUSHED REF, NOT THE WORKING TREE.** Every existing reader reads the local file. A local file is exactly what an impersonator benefits from and what a stale worktree gets wrong -- the prime updates `config:seats` at every rotation and pushes, so the authoritative answer is the file at `origin/season/s2` HEAD after a fetch, read with `git show <ref>:.agi/nodes/.geometry/seats.md`. 🔴 AND FAIL-CLOSED IN THE RIGHT PLACE: if the pushed ref cannot be reached, DO NOT silently answer from the working tree. Answer, but label the answer `UNVERIFIED` **and exit non-zero**, and print the ref and commit sha the answer came from when it IS verified. An unverified answer that exits 0 is the exact disease this repo has already been bitten by twice -- `SPAWN-GATE UNVERIFIED` returning success while writing a real node, and a meter printing a confident fraction for a transcript it could not attribute. Provenance IN the answer, always. 🔴 REUSE THE LAYER; DO NOT ADD A SIXTH READER. `config:seats` is already parsed in FIVE places -- `hierarchy.load_seats` (`hierarchy.py:66`, the one whose docstring names `config:seats` as the instance table), `seat_status.py:69`, `spawn_gate.py:589-605`, `viewport.py:461` and `dispatch.resolve_seat_spec` (`dispatch.py:585`). Route through ONE of them -- `hierarchy.load_seats` unless you can state a better reason -- and say in your node which you chose and why. A sixth private copy of the parse is the defect this project keeps paying for, not the fix. PROVED BY: (a) a test that a ref matching the row for the claimed role answers YES with the ref and the commit sha it verified against; (b) a test that a ref present in the table but under a DIFFERENT role answers NO -- that is the impersonation case and a check that only tests presence would pass it; (c) a test that an unknown ref answers NO rather than erroring or guessing; (d) a test that an unreachable pushed ref yields an `UNVERIFIED`-labelled answer AND a non-zero exit -- assert on the exit code, not only on the text; (e) a test that the working-tree file being EDITED does not change a verified answer, since the pushed ref is the authority -- this is the whole point and a fixture without it proves nothing; (f) no new parse of `seats.md` is introduced (assert by reading the diff, and say so in the node); (g) 🔴 RUN IT AGAINST THE REAL TREE AND PASTE THE OUTPUT for all three live seats -- belam/`7902ac`, sanctuary-director/`3d6888`, sanctuary-helper/`9d073a` -- plus one deliberate mismatch. A suite cannot see the shape this lives in. (h) `python3 extensions/agi/bin/commands.py run verify` PASS. DISPROVED IF: it reads only the working tree; an unverified answer exits 0; it answers YES on a role mismatch; it adds a sixth `seats.md` parser; provenance is missing from a verified answer; or any existing test is edited. HARD CEILING: 2 kids. 🔴 SCOPE: `extensions/agi/bin/send.py` and `extensions/agi/tests/test_send.py` ONLY. Do NOT add a file under `extensions/agi/bin/` -- `test_bin_help_smoke.py` auto-enrols it and it would need a suite window this round does not have. Do NOT touch `rotate.py`, `test_rotate.py`, `extensions/agi/hooks/`, `write.py` or `test_write.py` -- three parallel rounds own those. Do NOT write `config:seats`; this round READS it and never writes it. Do NOT run the full suite."
thought_session: sanctuary-director-genV-L4
title: A name and a window are trivially claimable; the pushed seats table is not
---
<!-- BODY:BEGIN -->
# hypothesis:l4-authority-verified-against-the-graph-not-the-message

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
