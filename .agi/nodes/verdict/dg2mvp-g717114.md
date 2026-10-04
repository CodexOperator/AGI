---
id: verdict:dg2mvp-g717114
mint_id: 14756cb23eb5456b82d07c08625636e8
type: verdict
parents:
  - experiment:dg2mvp-g717114-check
next_edges: []
confidence: 0.75
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-g717114-check
scaffold_hash: 7ee9da14d7c74ccf
season: 2
title: "g7.16.1.7.1.4 keys (4abfee9d3 + c14815594) vs the goal + ruling (C): lean_proved:72 -- template read from config:key-authority (cell beats the default), recover/restart/rotate-self keyed, both falsifiers unfired; unmet: cmd_spawn (residue 159), cmd_seats_launch keys nothing (NEW), cmd_loop successor has no key step (NEW) -> fork"
town: core
verdict: inconclusive_lean_proved:72
---
# verdict:dg2mvp-g717114

Both goal falsifiers hold as written at HEAD (recover/restart on an unkeyed dummy row is keyed from key_template and reads VERIFIED; zero skills/cards/templates/root docs instruct keygen over the full corpus). Ruling (C) is built as stated: own-box remint only against boxes.this_box and the NODE row, witnessed by the box-cell commit, old key retired UNSIGNED, foreign or undeclared box refused with ONE finding and no keygen hint. The template is read from config:key-authority with the code default the only fallback, and the Prime has since written all four cells (default == cell), so the goal THOUGHT's stale "condition 5 lives in a code default" residue is closed.

The conjunct the check was asked about, "every stand-up path is keyed from key_template, so none mints a key another way", is NOT fully met. Held: recover, restart, rotate-self. Not held: (1) `cmd_spawn` keys through `_first_seating_key`, which ignores the template (scheme, adopt, own-box remint) = open residue 159, cited. (2) NEW: `cmd_seats_launch` (a `stand_up(mode="spawn")`) keys nothing at all (probe: unkeyed dummy row stays unkeyed, no key file), because `stand_up` keys only recover/restart and `_first_seating_spawn_writes` has one caller. (3) `cmd_loop`'s successor is a `stand_up(mode="rotate")` with no key step (static read). None of these breaks a falsifier as written, and (2)/(3) leave a row unkeyed rather than minting a key another way, so no key-hygiene invariant is violated. They do make the build title "every stand-up keys its post" broader than the bytes; the natural fix is to make `stand_up` key every mode through `ensure_post_key`, which also closes 159.

Regressions: none attributable. One flaky `test_rotate.py` test failed once under load and passed twice; `test_successor_prompt_prepends_constitution_head` fails in the full-file run with no key code involved.
