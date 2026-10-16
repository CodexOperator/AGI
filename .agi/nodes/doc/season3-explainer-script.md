---
id: doc:season3-explainer-script
type: doc
mint_id: 50b27f111180485f8cc5c600426a6b6c
parents:
- goal:g5.4.2
next_edges: []
key: 3dbc163531a12b56
schema: doc@5d9146e2fcfd
title: season3-explainer-script
tags:
- media
- season3
- explainer
- script
origin: doc-version
link_ref: .agi/context/media/season3-explainer-script.md
---

# doc:season3-explainer-script

The narration and the HTML text of the season 3 explainer (goal:g5.4.2, stage M2), as a payload: `.agi/context/media/season3-explainer-script.md`. Per chapter: the claim-to-cite pairs the council reads, the narration the voice will read (numbers only through slots), and the HTML explainer's additions with byte-exact excerpts at the cited sha.

Every sentence of the narration and the HTML text ends with a tag: `[Cn.k]` (a pair of its own chapter proves what it says about the engine) or `[image]` (a picture, greeting or transition that claims nothing about the engine). The re-cut after the council's return of 7d4ee1db9e is listed, sentence by sentence, in `.agi/context/media/season3-explainer-recut-diff.md`.

Checks (read-only, no spend): `python3 extensions/agi/tests/media_fm1.py .agi/context/media/season3-explainer-script.md .` (excerpts, functions, callers) and `python3 extensions/agi/tests/media_fm2.py .agi/context/media/season3-explainer-script.md .` (pairs, bare numbers, slots). Tests: `test_media_fm2.py`, `test_media_fm1.py`. The outline it follows: doc:season3-explainer-outline.
