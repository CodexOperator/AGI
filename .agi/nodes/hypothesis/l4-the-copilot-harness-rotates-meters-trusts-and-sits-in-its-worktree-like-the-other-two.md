---
id: hypothesis:l4-the-copilot-harness-rotates-meters-trusts-and-sits-in-its-worktree-like-the-other-two
mint_id: bb5c795dbf584f8bb7b9bcf02f08857a
type: hypothesis
parents:
  - goal:g6.10
next_edges: []
edited_by: belam
scaffold_hash: 50458edc79741f13
season: 2
testable_claim: "goal:g15 (Prime XXI 2026-09-14; residue of L4.371): re-cut SD.03 START from tip 2f7e6235b, rebase onto origin/season2/main resolving conflicts in favour of trunk structure, keep the experiment nodes, and re-run tests. Measure six seams: copilot rotation through the bare keyed rotate path; rotate-self/seats-launch reads the row harness exactly as spawn does; meter from the actual ~/.copilot transcript; worktree cwd; idempotent trust/path allow-list preservation; and fixture-backed models-table mapping. A fixture row with harness copilot-cli must make rotate-self --dry-run emit copilot --model auto --effort E --allow-all --remote -i, not Claude. Run fixtures only, do not rotate live posts, and keep the suite green. FALSIFIERS: rotation needs a second command; rotate-self ignores a copilot-cli row or emits Claude; meter reads Claude transcript; cwd needs hand row edit; trust drops existing entries."
thought_session: dissolve-legacy-2026-09-19
title: The Copilot harness rotates, meters, trusts and sits in its worktree like the other two (Prime XXI 2026-09-14; continues L4.366)
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-copilot-harness-rotates-meters-trusts-and-sits-in-its-worktree-like-the-other-two

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
L4 CLOSE TRIAGE (belam gen 24, 2026-09-16 16:3xZ; workflow g15-close-triage wf_b1179398-7ab, reader + adversarial refuter on season2/main eb21d601f): KEEP for the next stream (KEEP) -- live defect: Falsifier reproduces: cmd_rotate_self's spawn_window call (rotate.py:17805-17817) passes model/effort/settings/seat/rc_name/successor_argv but no `harness=` although spawn_window accepts `harness: str EVIDENCE: None = None` (rotate.py:1631), so a copilot-cli row rotates to Claude. Reader's "grep .copilot = 0" is slightly off: MEASURED 2 hits in rotate.py (:1673, :19466) but both are `harnesses.copilot-cli` config-key text, not a ~/.copilot transcript meter, so no copilot meter exists. Three unmerged loop branches season2/loops/hypothesis-l4-the-copilot-harnes-a00-{5c87163d,693b8938,a528cbd1} MEASURED present via `git branch -a`. Never rounded at close (owner 14:1xZ).
