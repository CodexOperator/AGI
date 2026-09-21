---
id: hypothesis:l4-the-meter-hook-latch-is-ignored-churn-stale-release-runs-before-the-latch-gate-and-the-hook-rotate-self-launch-is-seamed
mint_id: 35b3f297aa7243c589ce4416a9488d07
type: hypothesis
parents:
  - goal:g15.25
  - hypothesis:l4-the-meter-hook-rotates-at-threshold-never-mid-merge-up
next_edges: []
edited_by: sensei-director
scaffold_hash: 08ae1ca58dd56fc6
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node, mur-SL2.17 (Prime XV 10:22Z, by name, wf_2144282d-658; g17.1 note bf7881ad1) line (2) — SL7.23 residue (ACCEPT_WITH_RESIDUE). Cite at 6afa8c186; re-measure on your base. MEASURED: (i) the latch hook-<seat>-gen<N>.lock is written under <shared sessions>/rotations/ (rotation_alert.py:744 _latch_path, _LATCH_SUBDIR), a TRACKED directory, so a hook run leaves untracked churn in MAIN — and a worktree seat's hook resolves the SHARED sessions dir and writes its latch into MAIN's tree; (ii) gate (d) (stale-latch release) runs AFTER gate (c), so a latch whose holder pid is dead blocks every later rotation until someone removes it by hand (the Prime rm'd dead hook latches by hand before rotating at 0.44, handoff 617e7b88a); (iii) the out-of-process test still launches a REAL rotate-self with no cwd and no seam (rotation_alert.py:795-798 subprocess.Popen in _spawn_rotate_self) — that Popen, fired from a kid's pytest whose over-line fixture named the REGISTERED seat, is what produced c1f01e920 (a live rotate-self --stops for the sensei-director seat); the SL7.23 harvest note on g15.25 misattributed it to the kid by hand. CLAIM: the latch lives under an ignored path (or the latch pattern is gitignored the way *.key.pending is) so MAIN's git status never shows it; gate (d)'s stale-latch release (holder pid dead) runs BEFORE gate (c) so a dead latch never blocks; a worktree seat's latch never lands under MAIN's tree; and _spawn_rotate_self launches through ONE seam (a module attribute the test replaces with a recorder) so no test can reach a real Popen of rotate-self. FALSIFIERS: git status on MAIN after a hook run in a worktree seat names the latch; a dead-pid latch still holds the gate; a test still reaches subprocess.Popen with a rotate-self argv. TESTS: git check-ignore on the latch path; dead-pid latch → the rotation proceeds and the latch is rewritten with the new pid; worktree-seat latch resolved outside MAIN's tree; the Popen seam driven with a recorder that asserts the argv and cwd — and EVERY fixture names a throwaway seat, never a registered one. FILE SCOPE: extensions/agi/hooks/rotation_alert.py (_latch_path, _gated_rotate gate order, _spawn_rotate_self), .gitignore, extensions/agi/tests/test_rotation_alert*.py. EXCLUDED: rotate-self itself, the card writer, gates (a) and (b). CEILING: no new gate; placement, one swap of (c)/(d), and one seam. Also correct the g15.25 SL7.23 harvest note with one note naming the hook Popen mechanism."
thought_session: sensei-director-genX-L10
title: the meter hook's latch never lands as tracked churn in MAIN, the stale-latch release runs before the latch gate, a worktree seat never writes its latch into MAIN, and the hook's rotate-self Popen goes through a seam no test can fire live
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-meter-hook-latch-is-ignored-churn-stale-release-runs-before-the-latch-gate-and-the-hook-rotate-self-launch-is-seamed

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
