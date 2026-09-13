---
id: hypothesis:l4-non-prime-posts-are-generation-less-on-every-surface-seatings-key-on-session-id-and-the-label-is-the-post-name-alone
mint_id: 9602f53b2040402e8ad2740b03c07f11
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: c95e8757b5baba15
season: 2
testable_claim: "goal:g15.25 SM.24 (intake: sanctuary-master 16:47:04Z dm, owner order via belam). CLAIM: non-Prime posts are generation-less on every surface: (1) the ack keys by session id, not generation (`--gen` is refused for a non-Prime post); (2) rotation records and dm lines carry no gen field for a non-Prime post; (3) the hook latch keys by session id, not generation; (4) the rotation-alert window uses `.prev` rather than a generation number; (5) the display label is the post name ALONE (no -gN suffix) -- `label_word` is retired via a Prime unset line; (6) every row writer stops writing a generation cell for a non-Prime post (the self_row half). The kid ALSO ships the `{gen}` template-placeholder list for master-sensei (every template string that still interpolates {gen} for a non-Prime post, so she can retire them). FALSIFIERS: any of the above still keyed/labelled by generation for a non-Prime post after the round lands; a Prime posts own generation handling changed (it must not be); the {gen} placeholder list incomplete or unshipped. TESTS: per-surface coverage (ack, record, dm, hook latch, window, label, row writer) for a non-Prime post vs a Prime post, plus the placeholder-list output. FILE SCOPE: rotate.py (ack, record, self_row), heal.py (hook latch), the label/window code, their test files. CEILING: <=250 lines net, 3-4 kids -- RE-BRIEF SM before any kid whose projected work passes 2x this ceiling. Order: after SM.23, before SM.20 (SMs 16:47:04Z order: 21 -> 23 -> 24 -> 20 -> 17 -> 14 -> 15 -> 10 -> 11 -> 22)."
title: non-Prime posts are generation-less on every surface -- seatings key on session id, the display label is the post name alone (label_word retired), and the kid ships the {gen} template-placeholder list for master-sensei to retire
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-non-prime-posts-are-generation-less-on-every-surface-seatings-key-on-session-id-and-the-label-is-the-post-name-alone

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
