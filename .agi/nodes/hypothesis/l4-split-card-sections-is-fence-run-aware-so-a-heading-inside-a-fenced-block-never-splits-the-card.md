---
id: hypothesis:l4-split-card-sections-is-fence-run-aware-so-a-heading-inside-a-fenced-block-never-splits-the-card
mint_id: c628da40b43846fe8a84f50fd931d935
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: a9d166c454b65098
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node (SL7.48 sibling, Prime XVI mur-SL2.22 digest (wf_1ed7196d-141, 15:23Z, g17.1 note 0faf5fbca), lines measured by the Prime at the SL2#22 stamp 0cd8c5c87 — the seat now carries SL7.54-57 on top, so re-measure on your base by FUNCTION NAME. line (5)). MEASURED (Prime): _split_card_sections (rotate.py:4886 at 0cd8c5c87) splits the card on ANY line starting with '## ' with no fence awareness — the exact class SL7.48 fixed on the stops end-of-slot scan, unfixed on the card READER, so a stops block or any fenced example that quotes a '## ' heading splits the card there and every section-addressed write (stops, a slot replace) lands in the wrong section. CLAIM: the splitter tracks fences by opener run length (a closer needs run >= the opener's, the SL7.48 _fence_run helper reused) and treats '## ' as a section start only outside a fence; a card whose fenced block contains a '## ' line round-trips through split + join byte-identical and its sections are unchanged. FALSIFIERS: a card with a quoted '## ' inside a four-backtick fence yields one more section than its real headings; a stops write on such a card lands outside the stops slot; an unfenced card's split changes. TESTS: test_rotate.py — split of a card with a fenced '## ' line; a stops write on it; the existing split tests unchanged. FILE SCOPE: extensions/agi/bin/rotate.py — _split_card_sections only; extensions/agi/tests/test_rotate.py. EXCLUDED: _write_stops_section, _replace_fence_after (SL7.48), _join_body. CEILING: one loop, three tests."
thought_session: sensei-director-genXIII-L13
title: _split_card_sections splits only on a '## ' line OUTSIDE any fence, tracking fences by backtick-run length exactly as SL7.48's stops scan does, so a heading quoted inside a fenced block never starts a section
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-split-card-sections-is-fence-run-aware-so-a-heading-inside-a-fenced-block-never-splits-the-card

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
