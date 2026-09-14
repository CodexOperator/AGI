---
id: hypothesis:l4-the-never-lower-baseline-counts-committed-node-files-and-records-the-manifest-so-a-drop-names-the-file
mint_id: aa022d9fcacb456d998c15dff7f65334
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: ee67189a26543783
season: 2
testable_claim: "goal:g15 SM.33 (Prime XX 01:36Z, measured 01:24-01:33Z: the never-lower node-count baseline is stamped from the WORKING TREE, so in the shared MAIN checkout an untracked node file — a MAIN-resident post mid-mint — inflates the stamp; a worktree post then measures commits only and reads a false DROP: SL2#32 sat red 10 min on 2841 vs an honest 2840; hand-corrected once, reason in verify-count.json). MEASURED on season2/main @930a60a05: verification.py _stamp_context :259 decides can_stamp per run; the count walks the tree (rglob) not git ls-files; verify-count.json carries {active, deprecated, total, sha, stamped_at, reason} and NO file manifest, so a drop is a number with no name. CLAIM: (1) the stamp COUNTS COMMITTED FILES ONLY (git ls-files -- .agi/nodes, live + deprecated) — or REFUSES BY NAME while `git status --short .agi/nodes` is non-empty in the stamping checkout, printing the untracked/modified node paths; never a working-tree count; (2) the stamp records the file MANIFEST (sorted relative paths, or its sha256 + the list in a sibling verify-manifest.json) beside the numbers, so a real drop prints the MISSING file names (set difference against the stamped manifest), not 2841 vs 2840; (3) a read in a worktree compares its own committed manifest against the stamped one — an untracked file on either side never enters either set; (4) the hand-correction path (reason cell) is kept but a stamp with a reason names the manifest it was corrected to. FALSIFIERS: a stamp taken with an untracked node present that does not refuse; a drop report with no file name; a worktree read that counts an untracked file. TESTS (<= 4, fixture repo): untracked node present → stamp refuses naming it; committed count matches ls-files; a deleted committed node → the drop names it; worktree with the same commits reads equal. FILE SCOPE: verification.py (count + stamp + compare), verify-count.json shape, test_verification*.py. CEILING: <= 40 production lines, ONE kid. STATUS: minted under the owner 01:38Z pause — NOT dispatched until the pause lifts."
title: L4 the never lower baseline counts committed node files and records the manifest so a drop names the file
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-never-lower-baseline-counts-committed-node-files-and-records-the-manifest-so-a-drop-names-the-file

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
