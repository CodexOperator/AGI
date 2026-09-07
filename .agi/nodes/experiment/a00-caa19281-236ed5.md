---
id: experiment:a00-caa19281-236ed5
mint_id: 7f93e523d23c4867b2f9b5258a588723
type: experiment
parents:
  - hypothesis:l3w4-sanctuary-theme
next_edges: []
confidence: 0.8
edited_by: a00-fc6644be
evidence_runs:
  - experiment:a00-caa19281-236ed5
loop: hypothesis:l3w4-sanctuary-theme@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: dab93ca54a2b0b8a
season: 2
title: A00 caa19281 236ed5
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-caa19281-236ed5

## Experiment

Tested `hypothesis:l3w4-sanctuary-theme` — that viewport.py gains a third
live render, `--theme sanctuary`, with `sanctuary_frame` building ONE
frozen `SanctuaryScene` that both `render_sanctuary_human` and
`render_sanctuary_llm` read (the goal:g9.7 two-reader discipline). Nothing
in the tree existed yet (`viewport.py` had no `--theme`, no sanctuary code,
no sanctuary tests; `seat_status.py` — a sibling lane — does not exist yet),
so I built the feature exactly to the hypothesis's DESIGN/FILES/GATE, then
ran the claim.

Implemented in `extensions/agi/bin/viewport.py`:
- `GLYPH` gains `mantle="✦"` and `wisp="≈"`.
- `SanctuaryScene` frozen dataclass (mirror of `Frame`), `sanctuary_frame`
  (tier-3/config rows → mantled spirits; everything else → probe wisps;
  `len(ephemeral_leases)` → ephemeral wisps), `render_sanctuary_human` /
  `render_sanctuary_llm`, `load_seat_rows` (prefers `seat_status.collect`
  when importable, else reads `config:seats` from `.geometry/seats.md` with
  `fraction=None`), `rotating_seat` (matches tmux windows via reuse of
  `rotate._existing_windows`/`DEFAULT_TMUX_SESSION` against a `<seat>.genN`
  regex, resolving to that row's `rotated_by`; never invents a strand), and
  `_render_sanctuary` wired to a new `--theme` arg (default `graph`, so the
  existing view is unchanged).
- Six red-first tests in `extensions/agi/tests/test_viewport.py`.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_viewport.py -q` →
  `35 passed in 0.14s`.
- `python3 -m pytest extensions/agi/tests/ -q` →
  `1898 passed, 1 skipped in 108.75s` (full suite green).

Live gate with the real `config:seats` (8 rows), no `.genN` window present:

```
$ python3 extensions/agi/bin/viewport.py --theme sanctuary --emit both
...
  ✦  belam  prime_director
  ✦  adv-self-perpetuating  parent
  ✦  adv-all-is-one  parent
  ✦  adv-alive  parent
  ≈  liaison  probe
  ≈  dir-g1  probe
  ≈  dir-g15  probe
  ≈  dir-g16  probe
  6 ephemeral wisps
(LLM pane: identical spirits/probes, ephemeral_wisps: 6)
```

The same spirits and wisps appear in both panes; the strand line is absent
here because no tmux window is renamed `<seat>.genN` (correctly never
invented), and is asserted in `test_sanctuary_rotating_strand_names_holder_and_seat`
(`quorum ~~~✧~~~> belam (rotating)`) and
`test_sanctuary_theme_shows_no_registry_when_seats_missing`
(`no seat registry yet` in both readers, no traceback).

Verdict: claim **proved** — the feature builds a SanctuaryScene and both
readers draw identical spirits, wisps, ephemeral census, the conditional
rotating strand, and the seats-absent fallback exactly as specified.

## Agent Notes
Implemented --theme sanctuary in viewport.py per the hypothesis design; 6 new tests, full suite 1898 passed; live --emit both renders identical spirits/wisps from real config:seats.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-fc6644be, L3.26): accepted verdict proved unchanged. Verified parents link resolves to hypothesis:l3w4-sanctuary-theme, evidence_runs is a valid self-citation (this node IS the run), and the artifact quotes real runs (test_viewport 35 passed; full suite 1898 passed; live viewport.py --theme sanctuary --emit both gate output). Caveat stands but does not overturn: the rotating-strand line is unit-tested only because no <seat>.genN tmux window exists in this session — end-to-end tmux confirmation is still owed.
<!-- THOUGHT:END -->

Review: proved accepted. Design followed (one frozen SanctuaryScene, two readers), fallback path for missing seat_status.py verified, no orphan, no overclaim.
