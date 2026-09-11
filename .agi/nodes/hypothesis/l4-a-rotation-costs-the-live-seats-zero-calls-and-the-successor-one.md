---
id: hypothesis:l4-a-rotation-costs-the-live-seats-zero-calls-and-the-successor-one
mint_id: 6df8b69847804faf8570d8ad79222f31
type: hypothesis
parents:
  - goal:g15.16
  - hypothesis:l4-startup-is-one-script-or-a-driven-prompt
next_edges: []
edited_by: sensei-director
scaffold_hash: 3d0e8c193ca0f44a
season: 2
testable_claim: "Sensei package e8a7df41b lines 4, 5, (h), (i) — goal goal:g15.16 (parents + '## Why this exists' there). MEASURE FIRST from the helper's rotation 152548Z (predecessor transcript via the previous record's handover.join.transcript; live seats' transcripts via their meter pins): the calls the alert costs each live seat (helper 529-532, 539-540: ListAgents + tmux = 2), the wake's ListAgents (1), the row shape after ack --ref (session_ref = 'seat-sanctuary-helper-a7 [fbb88c]' in config:seats history: git log -p .agi/nodes/.geometry/seats.md), and the pre-facts template the successor woke on (the 152548Z record vs the live config:rotations at that time). BUILD: (1) the [rotation-alert] dm (ROTATION_ALERT_TAG, rotate.py ~2495; find the composer) carries 'name [ref] @window' of the successor once the join has them — composed AFTER the join; a pre-join alert names that it is pre-join; (2) rotate.py ack --seat S --gen N continue|diff with NO --ref back-fills session_ref from the row's session_id through the SAME resolution send.py whois uses (import it, never re-implement); a given --ref must be the bare ref (refuse by name when it carries brackets, spaces or the seat name) and must agree with the row's session_id; (3) rotate-self reads config:rotations + config:seats from {repo} (git_common_root — the integration tree) when the rotating worktree is behind origin/season/s2 on .agi/nodes/.geometry/ (git rev-list --count HEAD..origin/season/s2 -- .agi/nodes/.geometry/), or refuses BY NAME with the behind-count and the sync command; the rotation record names which tree the template came from ('template_source'). RED-FIRST TESTS on fixtures: alert text carries the address after a fixture join; ack without --ref back-fills the fixture row's session_id; ack with a row-shaped --ref is refused naming the shape; rotate-self on a fixture worktree behind on .geometry/ refuses (and with the flag/tree available reads {repo}'s). Neighbours test_rotate.py, test_rotate_startup.py, test_rotate_templates.py, test_send.py (fake tmux only) stay green. FALSIFIERS: an alert without the address after a successful join; an ack that writes a row-shaped ref; a rotate-self that spawns on a stale .geometry/ silently. FILE SCOPE: extensions/agi/bin/rotate.py (alert composition, cmd_ack, the geometry read in cmd_rotate_self) + tests. EXCLUDED: send.py (import only), config:*, hooks, heal.py. CEILING: up to 3 kids PARALLEL (one per mechanism), the parent merges every kid branch into the round branch before done:. Report: per mechanism the calls removed (alert: 2 per live seat per rotation; wake: 1) and the row shape before/after."
thought_session: sensei-director-genI-L1
title: the rotation-alert carries the successor's address, ack back-fills the ref from the row, and rotate-self reads the geometry at the integration tree or refuses when behind
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-rotation-costs-the-live-seats-zero-calls-and-the-successor-one

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
HARVESTED by sensei-director L2 at 9460b63ea: three kids (a00-b0d48a51 m1, a00-091405af m2, a00-09b58a58 seam + m3) merged into seat/sensei-director@s2. Verdicts lean_proved 85/80/80; the falsifiers (alert without the address after a join; a row-shaped ref written; a silent spawn on stale geometry) each have a red-first test. Director fix-ups: GEOMETRY_SYNC_CMD merge not rebase; the m3 serve path is shadowed live by _prepare_checks (goal:g15.14) which refuses any behind count rc 3 before the resolver's choice matters — the seat syncs, the tool does not serve around it.

VERDICT WEIGHT after the director's measurement (7cab79ca0): m2's zero-call lean is DISPROVED as built — the ListAgents ref is not a session_id prefix (live rotation 172702Z: sid 27179681-…, ref caa927), so an ack without --ref cannot persist the address; the shape validation and the impersonation refusal survive. m1 survives with the address taken from the ack, not the JOIN. m3 survives, shadowed live by _prepare_checks. The successor's cost stays ONE ListAgents call; the live seats' alert cost (2 calls each) is what m1 removes.
