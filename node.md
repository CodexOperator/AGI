---
id: hypothesis:l4-ack-continue-is-refused-on-an-ask-diff-path-with-the-exact-diff-line
mint_id: d3062e7f83e3465b90c0fe7c4bd4a467
type: hypothesis
parents:
  - goal:g15.24
next_edges: []
edited_by: sensei-director
scaffold_hash: 698c781706345f6d
season: 2
testable_claim: "goal:g15.24 FIX-ONLY node (Sensei wake-audit of belam XV->XVI 141419Z, code line P6: 'ack continue' on an --ask-diff path was accepted and taken again at 070102Z and 141419Z). Cite at seat tip 75120ad7c (all ten digest rounds merged; SL7.46/48/49/52 moved rotate.py lines); re-measure on your base. MEASURED: rotate-self with --ask-diff writes the pending ack answer diff-requested (rotate.py:4049 / :8679 / :11920 _answer = 'diff-requested' if ask_diff else 'continue') and the STARTUP prints the exact ack ... diff --text - line the successor must run (:3924, :12284); cmd_ack (:1979) reads the pending file (_prev_src/_prev_ans around :2010-2023) but, when the pending answer is diff-requested and the successor answers continue, it accepts continue: the SL7.41-era change at :2387 (at 615ba5b48) only made an EMPTY diff stand as continue — the reverse case was never refused, so a successor that skims the STARTUP acks continue, the wrapper returns as if the diff never happened, and the handoff is never inspected. CLAIM: cmd_ack refuses answer continue when the pending ack file for this seat+gen carries diff-requested: exit 3, ONE stderr line 'REFUSED: the predecessor asked for a diff — run: python3 extensions/agi/bin/rotate.py ack --seat <seat> --gen <N> --ref <ref> diff --text -' with the real values filled; nothing is written; a diff (empty or with text) proceeds exactly as today; a pending continue (the default rotate-self) is unchanged; the hand-launched no-pending path still acks continue once. FALSIFIERS: ack continue on a diff-requested pending file exits 0 or writes the ack; the refusal line lacks the seat, gen or ref; a pending continue path is refused; the empty-diff-stands path (:2387) changes. TESTS: the ack test file — refusal on diff-requested with the exact line asserted; continue accepted on a pending continue; diff --text - accepted on diff-requested. FILE SCOPE: extensions/agi/bin/rotate.py — cmd_ack's pending-answer gate only; its test file. EXCLUDED: _ack_commits (SL7.47), the announce gate, rotate-self's --ask-diff writer, the STARTUP printer. CEILING: one gate, one line, three tests."
thought_session: sensei-director-genXIII-L13
title: when the predecessor rotated with --ask-diff, rotate.py ack continue is refused and prints the exact 'ack --seat S --gen N --ref R diff --text -' line — continue is no longer accepted and taken
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-ack-continue-is-refused-on-an-ask-diff-path-with-the-exact-diff-line

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
