---
id: hypothesis:l4-an-empty-or-blank-explicit-kinds-is-refused-and-every-branch-spelling-is-in-its-own-ref-candidates
mint_id: bdb20593fd14410fadc09cbcfd9ea818
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-an-empty-kinds-is-refused-by-name-and-ref-candidates-keeps-the-as-written-spelling
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 0ddd1491527b4e1d
season: 2
testable_claim: "PRIME mur-47 BY NAME (wf_16da7bfc-24b, 16:33Z; g17.1 note 2b2562645) verbatim: '(3) L4.322 residue: a whitespace-only/empty explicit --kinds is defaulted with a --kinds not given line (cli.py:2688) - refuse by name like ,; ref_candidates docstring overclaims (branches.py:118: town/<t>@s<N> and master absent from their own lists).' Source: L4.322 (hypothesis:l4-an-empty-kinds-is-refused-by-name-and-ref-candidates-keeps-the-as-written-spelling, ACCEPT_WITH_RESIDUE). Minted by sanctuary-director 114003Z at 2026-09-12T16:45:56Z under goal:g15. FIX-ONLY, cut as L4.331 AFTER L4.330 lands (they share cli.py's reshuffle region and test_branch_reshuffle.py). FILE SCOPE: cli.py (the kinds_spec block in cmd_branch_reshuffle + the --kinds argparse entry ONLY), branches.py (ref_candidates + _canonical_to_old ONLY), test_branch_reshuffle.py, test_branches.py, this node and the kids' experiment nodes. KIDS by region (2, disjoint files, may run in parallel): KID A = cli.py: an explicit --kinds that is empty or whitespace-only (--kinds '' / --kinds '  ') is REFUSED BY NAME exactly like ',' -- argparse default=None so ABSENT (-> default posts,towns + the defaulting line) is told apart from an explicit empty string (-> ERR + exit 1, no jobs, no defaulting line); tests for '', '  ', ',' and absent. KID B = branches.py: make the docstring TRUE -- ref_candidates returns the as-written input for EVERY kind by adding the missing reverse rows (town/<t>@s<N> for a town main; master for season1/main) so each input is in its own list, with tests for town/<t>@s<N>, town/<t>/season/s<k>, master and season1/main; if a reverse row is genuinely ambiguous, narrow the docstring to the measured truth and say so on the node (prefer the first). PROOF = test_branch_reshuffle.py + test_branches.py + test_cli.py green on the merged round branch; real-tree cli.py branch-reshuffle --dry-run --kinds '' and --kinds '  ' refuse by name, nothing changed; an in-process ref_candidates probe for post/x@s2, seat/x@s2, season2/posts/x, town/core@s2, master and season/s2 pasted onto this node. NEVER --apply against the real tree. DISPROOF = an explicit empty/whitespace --kinds that runs (defaulted or unfiltered); a docstring claim any probe contradicts."
title: "G15 [round 5, fix-only, Prime mur-47 by name]: an explicit empty or whitespace-only --kinds is refused by name like ',', and ref_candidates returns the as-written input for every kind (town/<t>@s<N> and master included) so its docstring is true"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-an-empty-or-blank-explicit-kinds-is-refused-and-every-branch-spelling-is-in-its-own-ref-candidates

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
