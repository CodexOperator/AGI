---
id: hypothesis:l4-the-copilot-harness-rotates-meters-trusts-and-sits-in-its-worktree-like-the-other-two
mint_id: bb5c795dbf584f8bb7b9bcf02f08857a
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam
scaffold_hash: 50458edc79741f13
season: 2
testable_claim: "goal:g15 (Prime XXI 2026-09-14 07:3xZ; continues L4.366 hypothesis:l4-copilot-cli-is-a-third-harness-with-the-same-hooks-as-claude-code-and-pi, landed 7b01de287: adapter + dispatch spawn/loop + rotate spawn; owner order 07:1xZ at 50ab689b2: copilot launches with --allow-all on every path): the Copilot harness is COMPLETE for a post only when five remaining seams are MEASURED, each its own kid + experiment node + test: (1) ROTATION — a `config:posts` row with `harness: copilot-cli` rotates by the same bare keyed `rotate.py rotate` and `seats-launch`: the successor is launched through the copilot adapter (the built command from a fixture-row `rotate-self --dry-run` shows `copilot … --allow-all` and the post name), and the record/row/pin/ack shape is byte-for-byte the claude-code one except `harness`; (2) METER — the UserPromptSubmit-equivalent hook prints the same `[meter] post=<post> <f>` line for a copilot post, reading the copilot session transcript from where Copilot CLI ACTUALLY writes it on this box (measure under ~/.copilot; a felt path is a falsifier), and `rotate.py meter --pin` accepts that transcript; (3) CWD — a copilot post whose row names a worktree is spawned with cwd `.agi/worktrees/post-<name>` (director-thought @369 runs in MAIN today, measured); prove from /proc/<pid>/cwd of a fixture spawn; (4) TRUST — the spawn path pre-sets ~/.copilot/config.json `trusted_folders` for the post cwd BEFORE launch, idempotent, never dropping an existing entry, so no first-run folder-trust prompt is answered by hand again (the 07:12Z seating needed one); (5) MODELS — the models-table reader (copilot model listing → the row allowed models) ships with a fixture; the LIVE table is gated on the OWNER Copilot Pro login (`gh auth refresh` or `copilot` /login; the CodexOperator gh token lists only `auto`): a live listing of only `auto` is recorded as the measured state, never as a defect. No live post is rotated, respawned or re-cwd-ed by this round — fixtures only; director-thought @369 and thought-master @366 stay untouched; the suite stays green under the ceiling. FALSIFIERS: a copilot post rotates only by a second command; the meter reads a claude-code transcript path for a copilot post; the cwd fix needs a row edit by hand; the trust pre-set drops an existing entry."
title: The Copilot harness rotates, meters, trusts and sits in its worktree like the other two (Prime XXI 2026-09-14; continues L4.366)
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-copilot-harness-rotates-meters-trusts-and-sits-in-its-worktree-like-the-other-two

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
