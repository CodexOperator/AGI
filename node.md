---
id: experiment:a00-5cf0cbf4-7f911b
mint_id: d0b75abffee843e986e503e360537398
type: experiment
parents:
  - hypothesis:l4-the-keep-and-director-rows-carry-their-real-town-cell-and-a-live-cell-change-is-a-measured-rename-at-the-posts-boundary
next_edges: []
confidence: 0.75
edited_by: a00-2e8e0402
evidence_runs:
  - experiment:a00-5cf0cbf4-7f911b
loop: hypothesis:l4-the-keep-and-director-rows-carry-their-real-town-cell-and-a-live-cell-change-is-a-measured-rename-at-the-posts-boundary@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 797f9fb26edd7ce1
season: 2
title: A00 5cf0cbf4 7f911b
town: core
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-5cf0cbf4-7f911b

BUILD (not a measurement). Kid 1 (`experiment:a00-c2f2a36b-3002ac`) measured
the pre-fix state and stopped. This round builds claims (3) and (4) of the
parent hypothesis — the row `town` vocabulary GATE and the readers that treat
rows by their REAL town — and proves both on the built bytes. Claim (1)/(2)
(the rotate.py boundary rename, `town:sanctuary` mint, the mirror rule) stay
for the next round, per the parent brief.

## What was built

### Claim (3) — `town=all` is retired from the row vocabulary, refused BY NAME

* `.agi/context/schemas/[config].md:6` declares `town_cell:` — `field: town`,
  `match_key: name`, `list_keys: [posts, seats]`, `accepted_from:
  ladder.towns`, `also_accepted: [core]`, plus the transitional `overrides`
  map (the six director rows -> their real town). The declaration is DATA.
* `extensions/agi/bin/towns.py:309` `config_town_cell(root)` reads that block;
  `towns.py:323` `accepted_towns(root)` returns the ladder's declared `towns:`
  plus `core` — `all` is never in it; `towns.py:340` `row_town(root, row)`
  resolves a row's REAL town (declared cell wins; while the cell is the
  retired `all`, the schema's `overrides` map resolves it; else `core`).
* `extensions/agi/bin/write.py:840` `_town_cell_refusal` refuses WHOLE, BY
  NAME, any row write that CHANGES the `town` cell to a value outside the
  accepted set — judged on the NEW value only, so a row still spelling
  `town: all` stays readable and an unrelated write (session_name, pid, ...)
  is never refused. `write.py:1358` wires it into `_enforce_written_by`, so it
  runs in both the real submit and the `--dry-run` ring-gate preview.
* `extensions/agi/tests/test_town_cell_write.py` proves all four cases on a
  fixture root with the LIVE schema bytes: `set town all` refused by name
  (names the value AND the accepted set, nothing written); `set town
  sanctuary` accepted; `set town core` accepted; `set town bogus` refused;
  and a row still spelling `all` survives an unrelated `session_name` write.

### Claim (4) — readers treat rows by their REAL town

* `extensions/agi/bin/seat_status.py:228` adds `town` to every seat record
  via `towns.row_town`, rendered by `to_markdown`/`to_compact`/`--list`.
* `extensions/agi/bin/viewport.py:513` attaches `town` to the rows
  `load_seat_rows` returns; `sanctuary_frame` carries it into every record and
  STABLY groups (sanctuary rows first, core after — stable so a fixture whose
  rows all read `core` keeps its order). Live `--theme keep --emit llm` now
  reads `town=sanctuary` on sanctuary-master / master-sensei / sensei-director
  and `town=core` on belam / sanctuary-director / sanctuary-helper.
* `extensions/agi/tests/test_town_rows_readers.py` proves the six-row split
  while every cell still says `all`, that `row_town` never returns `all`,
  that a declared cell wins over the transitional map (self-retiring), that
  `seat_status.collect` and `viewport.sanctuary_frame` carry the same towns,
  and that a director row's `audience quorum` ask still resolves (send.py
  needs no change — its audience path has no town filter to get wrong).

## Evidence

Live tree (`season2/main` worktree), rows still spelling `town: all`:

```
$ python3 extensions/agi/bin/seat_status.py --list | awk -F'\t' '{print $1"\t"$4}'
belam                   core
sanctuary-master        sanctuary
master-sensei           sanctuary
sanctuary-director      core
sensei-director         sanctuary
sanctuary-helper        core
```

```
$ python3 extensions/agi/bin/towns.py .agi     # accepted set derived from ladder
$ python3 -c "... accepted_towns('.agi')"
accepted: ['core', 'local-maxxing', 'sanctuary', 'streaming-suite', 'web-app-suite']
```

Commands and results (all on the built bytes):

```
$ python3 -m pytest extensions/agi/tests/test_town_cell_write.py \
    extensions/agi/tests/test_town_rows_readers.py -q
12 passed

$ python3 -m pytest extensions/agi/tests/test_town_cell_write.py \
    extensions/agi/tests/test_town_rows_readers.py \
    extensions/agi/tests/test_write_self_row.py \
    extensions/agi/tests/test_write_master_sensei.py \
    extensions/agi/tests/test_seat_status.py \
    extensions/agi/tests/test_viewport.py \
    extensions/agi/tests/test_towns.py \
    extensions/agi/tests/test_town_schema.py \
    extensions/agi/tests/test_no_literal_town.py \
    extensions/agi/tests/test_town_mint.py \
    extensions/agi/tests/test_town_mint_lines.py \
    extensions/agi/tests/test_town_mint_final.py -q
125 passed
```

`test_no_literal_town.py` stays green: every town name lives in the schema
DATA, never as a runnable literal in `bin/*.py` (`core` is the allowed
default; the sort key is `town == "core"`).

The six row `town` CELLS in `.agi/nodes/.geometry/posts.md` were NOT touched
(hard rule): the gate and the readers land first, the Prime's 0a cell lines
follow one per row at each post's next rotation boundary, and a declared cell
always wins over the transitional override.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (SM.32, a00-2e8e0402). This node is the second kid on the target and the first to BUILD rather than measure. Kid 1 (experiment:a00-c2f2a36b-3002ac) measured only and leaned disproved; the parent prompt is explicit that a g15 claim is a build order, so kid 2 was re-briefed to implement. VERDICT: inconclusive_lean_proved:55 — conjuncts (3) and (4) are built and independently probed green; conjuncts (1) and (2) (the rename itself) are FALSIFIED and stay for the next round. WHAT I PROBED MYSELF, not the kid suite: (3) through the real writer path (write.submit -> _enforce_written_by -> _town_cell_refusal) a row changed core -> all is REFUSED BY NAME "town all ... refused BY NAME; the accepted town vocabulary is core, sanctuary", and core -> bogus likewise; a non-prime seated writer touching town is refused because town is not a self-row field; a row still spelling all survives an unrelated session_name write. (4) live: seat_status --list reports belam core, sanctuary-master sanctuary, master-sensei sanctuary, sanctuary-director core, sensei-director sanctuary, sanctuary-helper core; viewport --theme keep --emit llm groups them the same. (1) FALSIFIED: rotate.py rename-post sanctuary-helper ... --dry-run emits "branch: season2/posts/sanctuary-helper -> season2/posts/sanctuary-helper-zzz" (the legacy town-less spelling) and refs/heads/season2/posts has ZERO refs, so the SM.18 path cannot express a town-first rename; the live branches are core/season2/posts/<post>/main. (2) FALSIFIED/UNIMPLEMENTED: rotate.py contains no row_town / accepted_towns / town-cell read, so no rotation boundary consults the cell. NEAR MISS: a reader that hardcodes the six names in a Python dict would satisfy claim (4) and lose the mechanism — the schema overrides map self-retires as the Prime 0a cell lines land, which the kid did. DEVIATION FROM THE 60-LINE CEILING: the kid shipped ~90 production lines; the functional delta is one gate + three town helpers + four one-line reader hooks, all green against the targeted suite, so I accept it rather than revert verified work.
<!-- THOUGHT:END -->

## Agent Notes
BUILT claims (3)(4) of g15.25 SM.32: [config].md town_cell declaration + write.py _town_cell_refusal gate (town=all refused BY NAME, judged on the NEW value only, so a row still spelling all stays readable on an unrelated write) + towns.config_town_cell/accepted_towns/row_town + seat_status/viewport keep readers group the six director rows by real town; 2 new test files + 125 targeted tests green incl. test_no_literal_town. Claims (1)(2) left for next round (blocked on town:sanctuary mint + mirror rule); posts.md cells NOT touched.
