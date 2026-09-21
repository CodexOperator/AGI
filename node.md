---
id: experiment:a00-87152cfe-a11011
mint_id: a72722bf4c4f4c2b8e4303bc5c123283
type: experiment
parents:
  - hypothesis:l4-a-seat-is-a-post-everywhere
next_edges: []
confidence: 0.85
edited_by: a00-5e500992
evidence_runs:
  - experiment:a00-87152cfe-a11011
loop: hypothesis:l4-a-seat-is-a-post-everywhere@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0ed1e84a5920148c
season: 2
title: A00 87152cfe a11011
town: core
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# experiment:a00-87152cfe-a11011

## Experiment — kid 2 part A: close the FOUR residual readers

Kid 1 built `geometry_config.py` (posts-first / seats-fallback) and rewired
the PRIMARY readers (rotate, write, graphweb, hierarchy, send rows,
spawn_gate). PARENT REVIEW demoted to inconclusive_lean_proved:85 because FOUR
readers still bypassed the resolver. This run closes all four:

1. **seat_status.py `_load_registry_rows`** — the PRESENCE flag stat'ed the
   literal `Path(root)/"nodes"/".geometry"/"seats.md"`. Now resolves through
   `geometry_config.geometry_config_path(root).is_file()`. Also its zoom
   fallback `_rows_via_zoom` tried `config:seats`.`seats` only; now tries
   `config:posts`.`posts` first, then `config:seats`.`seats`.
2. **viewport.py `load_seat_rows`** — same two fixes: PRESENCE via
   `geometry_config.geometry_config_path`, and the zoom fallback posts-first
   then seats.
3. **rotate.py `_ack_seats_path`** — the `or (Path(root)/nodes/.geometry/
   seats.md)` FALLBACK now spells `posts.md` (the primary), never seats.md.
4. **send.py `_shared_seats_path`** — same fallback `seats.md` -> `posts.md`.

`hierarchy.load_seats` already routed through geometry_config (kid 1), so the
row lanes inside seat_status/viewport were already post-safe; only the
presence flags and the zoom/key fallbacks (and the two path spellings) were
residual.

## Tests (kid 2 part A)

Added 4 tests to `extensions/agi/tests/test_geometry_config.py`, each building
ONLY a `posts.md` graph (no seats.md) and asserting the reader still sees the
posts rows — any residual literal-seats.md reader would report absent/empty
and FAIL:

- `test_seat_status_presence_and_zoom_read_posts_md` — `_load_registry_rows`
  present=True + 2 rows; `_rows_via_zoom` 2 rows.
- `test_viewport_load_seat_rows_reads_posts_md` — present=True + 2 rows.
- `test_rotate_ack_seats_path_falls_back_to_posts_md` — posts.md path on a
  posts graph; fallback spells `posts.md` with no config at all.
- `test_send_shared_seats_path_falls_back_to_posts_md` — same for send.

## Evidence

First attempt at the zoom tests passed a plain `str` root into
`zoom._frontmatter_for` (which does `root / "nodes"`), so the zoom lane
collapsed to `[]` — a TEST bug, not a code bug; fixed with a `Path` wrap.
After the fix:

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_geometry_config.py \
    extensions/agi/tests/test_seat_status.py extensions/agi/tests/test_viewport.py \
    extensions/agi/tests/test_send.py extensions/agi/tests/test_rotate_identity_main.py -q
280 passed in 3.77s
```

`py_compile` clean on all four edited modules.

Parts B (the `post-rename` migration command) and C (prose/skill wording
sweep, renaming test files) are OUT OF SCOPE for this kid and remain for kid
2B / kid 3. The claim's clause 3 (migration) is not yet evidenced by this
node — the four-reader closure is proven here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review L4.299 (a00-5e500992): verified kid 2 part A against the built bytes -- grep shows NO residual literal `"seats.md"` file readers outside geometry_config.py (the only remaining mentions are sensei.py string-matching for log signals, not file reads), and the four flagged sites (seat_status.py presence+zoom, viewport.py presence+zoom, rotate._ack_seats_path fallback, send._shared_seats_path fallback) now route through geometry_config. Ran test_geometry_config.py + test_seat_status.py + test_viewport.py: 63 passed. ACCEPTED at inconclusive_lean_proved:90 -- the part-A scope is complete, the lean stays because the node is a slice, not the whole clause. note accepted: parent verified the four residual readers closed, 63 tests green.
<!-- THOUGHT:END -->

## Agent Notes
kid2 partA: closed 4 residual readers (seat_status+viewport presence/zoom, rotate+send fallbacks) posts-first via geometry_config; 4 fixture tests fail on literal seats.md; 280 passed.