---
id: experiment:a00-f2b9aefb-f82039
mint_id: 5774116bbc2d47a28497fc2dddf93dbc
type: experiment
parents:
  - hypothesis:l4-the-stream-fragment-argv-resolves-to-executables
next_edges: []
confidence: 0.85
edited_by: a00-ede39964
evidence_runs:
  - experiment:a00-f2b9aefb-f82039
loop: hypothesis:l4-the-stream-fragment-argv-resolves-to-executables@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 7bc43c1ac2ca53d0
season: 2
title: A00 f2b9aefb f82039
town: streaming-suite
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-f2b9aefb-f82039

## Experiment

Hypothesis `l4-the-stream-fragment-argv-resolves-to-executables`: the stream
command group's argv must resolve (after `locations.streamer_stub`
substitution) to existing **executable files**, each reaching its intended
mode.

**Measured mechanism** (`/home/ubuntu/work/streamer-stub/bin/hold.sh:21-25`):

```
case "${0##*/}" in
  brb)  MODE="${1:---pause}" ;;
  back) MODE="${1:---off}" ;;
  *)    MODE="${1:---status}" ;;
esac
```

hold.sh dispatches on **argv[0]'s basename**, not argv[1]. Sandboxed runs
(`SB_HOME=/tmp/sbx-a00`, production untouched):

| argv | result |
|---|---|
| `hold.sh brb` | `usage: brb \| retract \| back \| brb --status` → **exit 2** (does NOT pause) |
| `hold.sh --pause` | `PAUSED. card on air; ring kept` → exit 0 |
| `hold.sh --off` | released → exit 0 |
| `hold.sh --status` | `not on hold` / relay state → exit 0 |
| `panic.sh` (no arg) | `nothing was streaming` → exit 0 (the full hard cut) |
| `<stub>` alone (directory) | not a file at all — executing it runs a directory |

**Falsified sub-claim:** the proposed rewrite `brb → <stub>/bin/hold.sh brb`
is DISPROVED as written. It satisfies "argv[0] is a file" but reaches the
usage error: basename `hold.sh` falls to `*` → `MODE="$1"`="brb", and `brb` is
not a known MODE, so `case "$MODE"` falls to `*` → usage/exit 2. Decide: line
where `case "${0##*/}"` runs (hold.sh:21) + the terminal `*) echo "usage: ...";
exit 2` (hold.sh last branch, line ~94).

**Change landed (intent, with measured spellings):**
rewrote all four argv entries in
`extensions/agi/briefs/commands.stream.fragment.md`:
`sb-status` = `[<stub>/bin/hold.sh, --status]`, `brb` =
`[<stub>/bin/hold.sh, --pause]`, `back` = `[<stub>/bin/hold.sh, --off]`,
`panic` = `[<stub>/bin/panic.sh]` (no flag = hard cut, still `owner_only: true`).
`<stub>` stays the ONE configurable root (`locations.streamer_stub`); the
`<stub>/bin/...` form resolves and keeps every argv under the stub directory.
Fixed the prose sentence that produced the bug ("the four commands are the
streamer-stub's own CLI subcommands, so each argv is `<stub>/<subcommand>`")
to describe the measured basename/explicit-flag dispatch.

**Test added** (`extensions/agi/tests/test_commands.py`): reads the REAL
fragment (not a synthetic fixture), extracts every argv from the yaml block,
substitutes `<stub>`, asserts `os.path.isfile` + `os.access(..., os.X_OK)` for
each argv[0], a static dispatch assertion (argv[1] ∈ `--status|--pause|--off`
for hold.sh commands; panic.sh with no flag = hard cut) — this would catch the
`hold.sh brb` spelling — plus panic is `owner_only: true` and the group stays
HELD/declared. Tests never execute hold/panic/live (stream is LIVE); verified
sandboxed only.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_commands.py -q` → **32 passed**.
- Broader set (commands/brief/briefing/locations/cli/viewport) → **287 passed**.
- **Mutation check:** reverting the fragment to the BROKEN spelling
  (`["<stub>", "sb-status"]` etc.) makes
  `test_stream_fragment_argv_resolves_to_executable_files` FAIL
  (`argv[0] is not a file: <stub-dir>`); restored, it passes. The new guard
  has failed once on purpose, so it is a guard.
<!-- BODY:END -->

## Agent Notes
Fixed the stream fragment so each argv resolves to an executable FILE reaching its mode (hold.sh --status/--pause/--off, panic.sh) and added a test reading the REAL fragment asserting isfile+X_OK+mode and panic owner_only; sandboxed hold.sh brb → exit 2 falsifies the proposed spelling

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-ede39964, L4.143). Demoted proved -> inconclusive_lean_proved:85. WHAT THE INSTRUCTION SAID: the target claim names the rewrite "brb/back -> <stub>/bin/hold.sh brb / <stub>/bin/hold.sh back". WHAT THE MACHINE ACTUALLY DOES: /home/ubuntu/work/streamer-stub/bin/hold.sh:21-25 dispatches on argv[0] basename, case "${0##*/}" in brb) MODE="${1:---pause}"; a hold.sh basename falls to *) MODE="$1"="brb", which is not a known MODE at the case "$MODE" table, so the command reaches hold.sh:81 *) echo "usage: ..."; exit 2. Measured by the kid in a sandboxed SB_HOME (exit 2, does not pause); confirmed by the parent by reading the two cases. THE NEAR MISS: a fix that satisfies the words "argv[0] is a file" and loses the mechanism -- hold.sh brb IS an existing executable file that passes isfile+X_OK and still never pauses; that is exactly why the landed test asserts argv[1] equals --pause/--off and not merely that argv[0] exists. IF DEVIATED FROM A STANDING RULE: none; the deviation is from the CLAIM, not from a rule, and it is documented in the body. WHY NOT proved: the node is cleared on its stated falsifier (no argv[0] is a directory or absent) and the guard is mutation-checked, but the claim letter itself was corrected in flight -- the named brb/back spelling was disproved and replaced -- and one run with no independent replication is thin ground for a strong claim.
<!-- THOUGHT:END -->