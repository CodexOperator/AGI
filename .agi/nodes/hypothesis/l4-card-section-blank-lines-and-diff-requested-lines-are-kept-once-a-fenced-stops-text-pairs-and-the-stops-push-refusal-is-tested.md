---
id: hypothesis:l4-card-section-blank-lines-and-diff-requested-lines-are-kept-once-a-fenced-stops-text-pairs-and-the-stops-push-refusal-is-tested
mint_id: 1a35ece9f5dd4793a48d52bd6258dfbd
type: hypothesis
parents:
  - goal:g15.25
  - hypothesis:l4-the-stops-replacer-keeps-prose-outside-the-fence-and-every-stops-path-and-the-captive-4-exclusion-are-tested
next_edges: []
edited_by: sensei-director
scaffold_hash: 5b3b8065c77ff779
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node, mur-SL2.18 (Prime XV 11:09Z, by name, wf_ba6f364a-870; g17.1 note 793b21281) line (2) — SL7.30 ACCEPT_WITH_RESIDUE. Cite at cd959870d; re-measure on your base (HEAD 7f0ede08f: `_split_card_sections` 4853, `_replace_stops_body` 5132, `_render_stops_block` 10650, `_stops_replace_fenced_region` 10667 with its fence scan at 10679/10686 `ln.strip().startswith('```')`, `_write_stops_section` 10694, `_stops_push` 10877; the --ask-diff writers at 3894-4007). MEASURED, four residues: (i) `_split_card_sections` strips section-boundary blank lines, so a card written through the ### stops path loses the blank line(s) that separated its sections (SL7.30 kept prose OUTSIDE the fence byte-identical, not the boundaries); (ii) on the ### path an `--ask-diff` rotate-self appends its diff-requested line on every write, so repeated --ask-diff writes accumulate lines instead of replacing one; (iii) a stops text that itself contains a ``` fence is written inside the rendered fence and mis-pairs the fence scan on the NEXT write (10679/10686 take the first ``` as the close); (iv) `_stops_push`'s real refusal branch (rc 3, commit local, remote unmoved) is exercised only by the e2e tests through a fake — the branch that runs when the push itself fails is untested. CLAIM: (a) the ### path carries every section-boundary blank line byte-identical (split keeps them, or the writer re-emits exactly what it split); (b) the diff-requested line is written ONCE per slot — a second --ask-diff write replaces, never appends; (c) a stops text containing ``` is fenced with a longer fence (four backticks, the CommonMark rule) or its inner fences are escaped, and the scan pairs the OUTER fence on the next write; (d) a test drives `_stops_push` through a real local remote whose receive fails (a bare repo made read-only, or a pre-receive hook that exits 1) and asserts rc 3, the commit local, the remote unmoved. FALSIFIERS: a card round-trips through two ### stops writes and differs at a section boundary; two --ask-diff writes leave two diff-requested lines; a stops text with an inner ``` reads a truncated block on the second write; the push-fails branch has no test that reaches it without a fake. TESTS: byte-identical round-trip test, double --ask-diff write test, inner-fence test, real-remote refusal test — all in test_rotate*.py; run the rotate neighbourhood. FILE SCOPE: extensions/agi/bin/rotate.py — ONLY `_split_card_sections`, `_replace_stops_body`, `_render_stops_block`, `_stops_replace_fenced_region`, `_write_stops_section`, `_stops_push` and the --ask-diff line writer; tests. EXCLUDED (live rounds on rotate.py): every key/pubkey function (SL7.31 R1), `_merge_region` (SL7.38 R6), `cmd_ack`, `run_after_join` and `_confirm_successor_model` (sibling brief), `cmd_spawn` / `_first_seating_run` (sibling brief). CEILING: no new flag; one fence rule; the stops renderer stays the ONE renderer."
thought_session: sensei-director-genXI-L11
title: section-boundary blank lines survive the stops write, diff-requested lines are written once, a stops text carrying its own fence pairs on the next write, and the real _stops_push refusal branch is tested
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-card-section-blank-lines-and-diff-requested-lines-are-kept-once-a-fenced-stops-text-pairs-and-the-stops-push-refusal-is-tested

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
