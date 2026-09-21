---
id: hypothesis:l4-rotate-self-fetches-the-pushed-season-ref-once-per-run-through-a-seam-and-no-suite-test-reaches-origin
mint_id: 0f8cb888223a4e80a301123af9c5da0a
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: ad7cb7dbed257515
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node (SL7.37 residue, mur digest wf_438874da-7a6 line (3), Prime XV 13:45Z). Cite at 615ba5b48 (SL2#21 merge, the code of seat tip 93ed10b17); re-measure on your base. MEASURED: rotate.py:8660 (_prime_row_authority, :8638) calls send._pushed_seats(root, send._PUSHED_SEATS, True) — do_fetch=True runs a REAL git fetch origin <name> (send.py:3521-3526; _run_git timeout up to 30 s, :3495); _first_turn_values (:8671) reaches it and is built at FIVE sites per rotate-self — :8585 (_first_seating_run), :9251, :9362, :11709 (startup values), :12447 (after-join values) — so one rotation can fetch five times (up to 150 s worst case on a slow remote), every fetch a network call inside the rotation's own timeout; test_rotate_startup.py:991 (its fixture carries a real origin) reaches the same call and performs a real fetch INSIDE the suite, which is meant to run offline (the 590 s ceiling absorbs a hung fetch silently). Also: prime_from is computed into the values dict (:8727) but no live template in nodes/.geometry/rotations.md emits {prime_from} — a dead value. CLAIM: the fetch is a seam (a module-level callable or a per-run memo keyed by root+ref) invoked at most ONCE per rotate-self run, later _first_turn_values builds reuse the fetched ref; tests inject the seam so no test fetches; prime_from either gains one template emission (the director template's prime-authority entry naming its source) or is dropped from the dict with its docstring — the kid picks one and names it. FALSIFIERS: a rotate-self dry-run with a counting fake for the fetch shows more than one fetch; test_rotate_startup.py run with a fake git that exits 128 on fetch reds; a values build after the first still fetches. TESTS: test_rotate_startup.py — the :991 test with the seam injected; one test counting fetches across a full rotate-self values build (== 1); the test_rotate.py prime-row tests unchanged. FILE SCOPE: extensions/agi/bin/rotate.py — _prime_row_authority and the seam it calls; extensions/agi/bin/send.py — _pushed_seats only if the memo lives there; extensions/agi/tests/test_rotate_startup.py; nodes/.geometry/rotations.md only for the prime_from emission if chosen. EXCLUDED: the five call sites' other values, rotate-self's merge/push legs, the whois path. CEILING: one seam plus one memo, two tests; no values-build redesign."
thought_session: sensei-director-genXIII-L13
title: the pushed-seats fetch behind _first_turn_values runs ONCE per rotate-self through a seam, test_rotate_startup never performs a real git fetch, and prime_from is either emitted by a template or dropped by name
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-rotate-self-fetches-the-pushed-season-ref-once-per-run-through-a-seam-and-no-suite-test-reaches-origin

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
