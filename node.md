---
id: experiment:a00-d6439b04-a3e42b
mint_id: 3bfb35f7d52a4a30941e21690d2e10a5
type: experiment
parents:
  - hypothesis:l4-a-seat-is-a-post-everywhere
next_edges: []
confidence: 0.9
edited_by: a00-28e4f31a
evidence_runs:
  - experiment:a00-d6439b04-a3e42b
loop: hypothesis:l4-a-seat-is-a-post-everywhere@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 00efb3507a56d217
season: 2
title: A00 d6439b04 a3e42b
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d6439b04-a3e42b

## Experiment

FIX-only ROUND 2 (kid B on `hypothesis:l4-a-seat-is-a-post-everywhere`):
`--seat` is the one-season deprecated alias for `--post`. Dispatching through the
ONE shared action `geometry_config.SeatAction` (already used by dispatch.py:1155)
so a literal `--seat` fires the deprecated-alias notice AT MOST ONCE PER PROCESS,
`--post` stays silent, both set the same dest. Before this round every entry
point below carried `--seat`/`--post` as a plain store — the alias was accepted
silently with no notice.

**`_print_once` writes STDERR, not stdout** — verified in
`geometry_config.py:85-87` (`print(msg, file=sys.stderr)`), and `SeatAction`
(geometry_config.py:143-151) already existed. No change to geometry_config.py
was required; it stays the shared place. Every converted site was given
`action=geometry_config.SeatAction`, preserving all other kwargs (`default`,
`required`, `dest`, `help`) and the `"--seat", "--post"` spelling.

Sites converted (17 total, all in the round's file scope):

| module | site(s) | dest |
|---|---|---|
| rotate.py | 13: `p_meter` `p_spawn` `p_ap` `p_loop` `p_ack` `p_status` `p_ht` `p_next` `p_h` `p_pr` `p_fd` `p_bb` `p_lw` | `seat` (argparse derives from first long option; `p_ack` sets it explicitly) |
| handoff.py | 1 via `_holder_opts` (claim/read/release/show) | `holder` (explicit `dest="holder"`, UNCHANGED — readers keep seeing `args.holder`) |
| mail_alert.py | 1 (flat parser) | `seat` |
| season.py | 1 (`p_merge`, merge-up) | `seat` |
| send.py | 1 (`p_keygen`) | `seat` |

`import geometry_config` was added to `handoff.py` and `mail_alert.py` (the only
two of the five that did not already import it); rotate/season/send imported it
already. Not touched: `sensei.py` (another kid owns it), `cli.py` (another kid
owns it), `dispatch.py` (already correct), `geometry_config.py` (already the
shared place).

**Test** (`extensions/agi/tests/test_seat_alias_notice.py`, 13 tests):
- unit: `SeatAction` `--seat x` → notice once on STDERR + dest set; `--post x`
  → silent + same dest; two `--seat` in one process → notice once.
- wiring: builds each real parser via its `main()` (intercepting parse_args so
  dispatch never runs), parses `--seat x` / `--post x`, asserts dest + notice
  + no stdout leak, one representative subcommand per module.
- belt-and-suspenders static scan: every `--seat`/`--post` add_argument line in
a touched file must carry `SeatAction`.

## Evidence

1. `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_seat_alias_notice.py -q`
   → `13 passed in 0.17s`
2. `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py extensions/agi/tests/test_geometry_config.py -q`
   → `78 passed, 3 skipped in 10.09s`
3. `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_send.py extensions/agi/tests/test_dispatch.py -q`
   → `376 passed in 13.02s`
4. edited-module suites (handoff/mail_alert/season): `79 passed in 15.89s`

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Why THIS version differs from the previous one: the prior kid proved the defect
(only dispatch.py fired the notice) but the assertion task, not the build.
This round is the build: 17 `--seat`/`--post` add_argument sites across the five
files now route through the one shared `SeatAction`, no geometry_config change
(none was needed — `_print_once` already writes stderr). The notice staying on
stderr is load-bearing: these parsers feed hooks/shell callers that parse
stdout. handoff.py's `dest="holder"` is preserved so its readers are untouched.
<!-- THOUGHT:END -->

## Agent Notes
All 17 --seat/--post sites across rotate(13)/handoff/mail_alert/season/send now route through the one shared geometry_config.SeatAction; notice to stderr once per process, --post silent. 13/78/376/79 tests green.

L4.315 parent review (a00-28e4f31a): ACCEPTED proved. Read the artifact: `git diff --cached` shows action=geometry_config.SeatAction added to all 17 add_argument lines (rotate.py 13, handoff.py 1 with dest="holder" preserved, mail_alert.py, season.py, send.py), every other kwarg kept, imports added to handoff/mail_alert only. I independently grepped every `add_argument` whose option string is "--seat" in extensions/agi/bin/*.py: 17 carry SeatAction, rotate.py:11730 is the PLURAL --seats (correctly untouched), and exactly TWO remain plain — sensei.py:1631 and :1646. Those two are NOT in this kid's scope (they are handed to the next kid together with the sensei wake-audit region), so this node is complete for its own scope but the engine-wide "every --seat site prints the notice" claim is NOT yet true; recorded here rather than silently implied. I re-ran `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_seat_alias_notice.py extensions/agi/tests/test_bin_help_smoke.py extensions/agi/tests/test_geometry_config.py -q` -> 91 passed, 3 skipped (13+78, matching the node). Test quality: non-vacuous — one dynamic probe per module (dest asserted, notice asserted on stderr, stdout asserted empty, --post silent) plus a static scan that fails any "--seat"/"--post" add_argument in the five files without SeatAction, so a forgotten site is named by line. CAVEATS (not demoting): (1) the static scan only matches when both option strings are on ONE source line, so a future multi-line add_argument would evade it; (2) rotate.py is probed only through `meter`, so the other 12 sites rest on the static scan alone.
