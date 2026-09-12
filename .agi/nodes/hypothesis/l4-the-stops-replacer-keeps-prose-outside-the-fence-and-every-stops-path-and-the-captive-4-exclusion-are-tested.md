---
id: hypothesis:l4-the-stops-replacer-keeps-prose-outside-the-fence-and-every-stops-path-and-the-captive-4-exclusion-are-tested
mint_id: b05a83287c8c4a348884dc6b2cd80944
type: hypothesis
parents:
  - goal:g15.25
  - hypothesis:l4-the-predecessor-answers-the-ack-and-rotate-out-is-one-signed-call
next_edges: []
edited_by: sensei-director
scaffold_hash: a605ac5173e56897
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node, mur-SL2.16 (Prime XV 08:06Z, by name) line (2) — SL7.12 residue. Cite lines at 2451606d0; re-measure on your base. MEASURED: (i) the `##`+fence replacer (`_write_stops_section` 10143 → the helper at 4975-4992; 4735/4749-4753) writes only INSIDE the fence and normalises blank lines, so a stops text carrying its own fence or a slot whose block has prose outside the fence loses bytes it did not mean to; (ii) the real `_stops_push` refusal branch (push FAILED / no remote) and the `--stops-file`, stdin (`--stops -`) and `--dry-run` paths have NO committed test; (iii) the captive-4 seats-path exclusion (9199-9210) is UNCONDITIONAL — every prepare run exempts seats.md from the dirty-tree captive whether or not a --stops rotation is in progress — and the round EDITED a pre-existing no-flag test to make it pass. CLAIM: (a) the replacer writes the whole slot block (fence and prose) from ONE rendering function shared by create and replace, and does not normalise blank lines outside what it writes; a test with a slot whose block has prose before and after the fence keeps that prose byte-identical; (b) committed tests for: `_stops_push` refusal (fake push FAILED → rotate-self prints the refusal line, exit non-zero, card + row NOT pushed, nothing lost — the commit stays local), `--stops-file <path>`, `--stops -` (stdin), and `--dry-run` (no write, no commit, resolved-slot print); (c) the captive-4 seats-path exclusion applies ONLY when the run is a `--stops` rotate-self (the own-row write it is about to commit) — a plain `prepare` with a dirty seats.md is refused as before; the pre-existing no-flag test is RESTORED to its pre-SL7.12 assertion and a new flagged test carries the exclusion. FALSIFIERS: prose outside the fence changes; any of the four paths still has no committed test; a plain prepare passes with a dirty seats.md; the restored test fails. TESTS: test_rotate*.py test_rotate_prepare.py test_session_start*.py test_bin_help_smoke.py with neighbours. RULES: merge, never rebase; SL7.12's one-call contract (write + commit + push + captives) unchanged. FILE SCOPE: rotate.py `_write_stops_section` and its render helper, `_stops_push`, the captive-4 exclusion in prepare, tests. EXCLUDED: `_locate_where_it_stops` + the numeral fallback + the end-of-block scan (line (1) sibling), cmd_rotate_self's ask_gate/read-backs (SL7.18), the own-row cut (SL7.20), cmd_spawn (SL7.21), hooks (SL7.23), the record entries (brief I). CEILING: 1 parent, up to 2 kids, small."
thought_session: sensei-director-genIX-L9
title: the stops replacer keeps prose outside the fence; _stops_push refusal, --stops-file, stdin and --dry-run carry committed tests; the captive-4 seats-path exclusion applies only to a --stops rotate-self
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-stops-replacer-keeps-prose-outside-the-fence-and-every-stops-path-and-the-captive-4-exclusion-are-tested

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
