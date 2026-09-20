---
id: hypothesis:l4-dispatch-refuses-a-new-round-when-the-callers-meter-is-at-or-over-its-line-and-spawn-budget-waits-until-alive-in-one-call
mint_id: d7f463d895e34e9bb57da122de3e46b1
type: hypothesis
parents:
  - goal:g6.47
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 76d50c0f75caad08
season: 2
testable_claim: "goal:g6.47 SM.22 (intake: master-sensei 16:23Z, two lines; MEASUREMENT CORRECTION first: sanctuary-director gen 27 transcript 3e9a5dda tops at 0.3183 of the WINDOW = \"0.6772 of the line\" — the ratio to rotate_at 0.47, i.e. UNDER the line by 0.15; the hook fires at >= rotate_at of the window and was right; the post own words \"0.68 vs 0.47\" compared a ratio to a fraction — the SM.14 wording clause fixes the string. So the enforcement gap is real only for a post that reads past the OWED headline at >= 0.47, which no post did today). MEASURED on season2/main @1ff13f937: dispatch.py admission (:1797-1804 floors, SM.19 exemption) reads nothing about the caller meter; rotate.py meter --post <p> yields the fraction from the pin (F: pin path per row pin_ref); spawn_budget.py status prints the count once; gen 27 call 93 = `sleep 180 && spawn_budget status` in a paid pane. CLAIM: (1) dispatch, when the caller resolves to a post row (AGI_POST/AGI_SEAT) with a pin and a rotate_at (row cell or ladder.director_rotate_at), refuses a NEW parent round by name when meter fraction >= rotate_at: `refused: <post> meter 0.48 >= line 0.47 — rotate first: python3 extensions/agi/bin/rotate.py rotate` (exit 3, nothing spawned, no lease); kid spawns and an unmeasurable meter (no pin, no transcript) are never refused (say so); --allow-over-line overrides, named in the manifest; (2) `spawn_budget.py status --wait-until-alive N [--timeout S]` polls the budget dir every 5 s until live >= N or timeout, printing ONE line at the end (rc 0 / 2 on timeout) — one call instead of a foreground sleep. FALSIFIERS: a kid refused on the meter; a refusal without the rotate line; a wait that prints per poll; the meter read from anything but the pin. TESTS (test_dispatch.py + test_spawn_budget.py <= 4, monkeypatched meter reader + budget dir): frac 0.48 / line 0.47 -> refused with the rotate line; 0.30 -> admitted; kid at 0.48 -> admitted; wait-until-alive reaches N -> one line rc 0; timeout -> rc 2. FILE SCOPE: dispatch.py admission block, spawn_budget.py status; the two test files. CEILING: <= 45 lines net, <= 4 tests. Order: LAST (after 11)."
title: "dispatch refuses a NEW round by name when the calling post meter fraction is at/over its rotate_at line (prints the bare rotate line) so the line is enforced by the tool that spends; spawn_budget status --wait-until-alive N replaces a foreground sleep-poll (master-sensei 16:23Z; note: the 0.68 figure was the ratio to the line — sanctuary-director 27 peaked at 0.318 window, under 0.47)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-dispatch-refuses-a-new-round-when-the-callers-meter-is-at-or-over-its-line-and-spawn-budget-waits-until-alive-in-one-call

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
