---
id: hypothesis:l4-the-meter-hook-rotates-at-threshold-never-mid-merge-up
mint_id: 8aabf8f0fab24405a5c142e252efc122
type: hypothesis
parents:
  - goal:g15.25
  - hypothesis:l4-the-predecessor-answers-the-ack-and-rotate-out-is-one-signed-call
next_edges: []
edited_by: sensei-director
scaffold_hash: 2463ab4d14fc78bf
season: 2
testable_claim: "goal:g15.25 line (4) build order (owner 20:3xZ via the Sensei 21:16Z: \"rotate-out 0\"; Prime XI 21:20Z (d) GATE, verbatim: \"line (4)'s meter hook must not fire rotate-self while a merge-up is in flight. A rotation landing mid-merge is worse than one extra tool call, and it is the kind of thing that only fails under load.\"). SERIAL behind line (3) (SL4.08: rotate-self --stops = the one-call rotate-out). MEASURED: `extensions/agi/hooks/rotation_alert.py` runs on UserPromptSubmit (~/.claude/settings.json:46-51), computes the seat's fraction against `rotate_at` (main-checkout row first, SL4.05 labels) and PRINTS \"## ⚠️  approaching rotation\" bands (264-) — it never acts; `prepare` refuses through its captives (behind season/s2, dirty tree, card age vs the last WORK commit, stale pin, stale ack, suite lock) and `rotate-self --prepare` runs them; a merge-up in flight is visible as MAIN's `.git/MERGE_HEAD`, the suite lock `<sessions>/verify-suite.lock` with a live pid (verification.py:75, 371, 665), or an unpushed merge commit on season/s2 (`git -C <main> status -sb` ahead). CLAIM: (1) the hook, when `fraction >= threshold` for the seat it serves, RUNS `rotate.py rotate-self --stops '<text>'` (line 3) itself — rotate-out ZERO calls — with the stops text derived from the seat's LAST SIGNED COMMIT message and its last signed dm (the two most recent signed acts, one line each, `stops: <commit subject> | last dm: <first 80 chars>`), and prints what it did as the hook's output; (2) it is GATED, in this order, each gate printing its reason and doing nothing when it holds: (a) prepare's card-age captive (the card must have been written after the last WORK commit — the hook never rotates a seat whose card is stale; it prints the card line to write instead), (b) NO MERGE-UP IN FLIGHT: MAIN's MERGE_HEAD absent AND the suite lock absent-or-dead AND season/s2 has no unpushed merge commit — when any holds, the hook prints `rotation deferred: merge-up in flight (<which>)` and re-checks on the next prompt; (c) prepare's other captives (behind / dirty / pin / ack) as today; (d) a once-per-generation latch (a marker under sessions/ keyed by seat + generation) so a slow spawn is never doubled; (3) the hook stays P7: it never raises, never blocks the prompt, times out its rotate-self call (background it and print the record path), and emits the threshold bands exactly as before below the line; (4) the threshold band text gains the deferral reason so the operator sees why a seat over its line has not rotated. FALSIFIERS: the hook fires rotate-self with MERGE_HEAD present, or with a live suite lock, or with a stale card; it fires twice for one generation; it raises or delays the prompt on a failure; the stops text is empty when a signed commit exists. PROOF on the fake tmux: a fake seat over its line with a clean state rotates from the hook with zero calls (record success, stops line on the card); the same seat with a live fake lock prints the deferral and does not rotate; with a stale card prints the card line and does not rotate. TESTS: test_rotation_alert*.py + test_rotate*.py + test_session_start*.py + test_bin_help_smoke.py with neighbours; the hook's tests keep the autouse AGI_SEAT delenv. RULES: merge, never rebase, in every clear line; the hook must never break a session (P7); no new bin/ file — the gates are rotate.py subcommands or prepare captives the hook calls. FILE SCOPE: hooks/rotation_alert.py, rotate.py prepare (the merge-in-flight captive is reusable there too), tests. EXCLUDED: send.py, heal.py, verification.py. CEILING: 1 parent, up to 2 kids, small."
thought_session: sensei-director-genIV-L4
title: the meter hook runs rotate-self --stops at threshold (rotate-out 0 calls), stops line from the last signed commit/dm, gated by the card-age captive and NEVER while a merge-up is in flight
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-meter-hook-rotates-at-threshold-never-mid-merge-up

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
