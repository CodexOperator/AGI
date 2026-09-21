---
id: experiment:a00-18b5dac7-28b90e
mint_id: 32357333475a41b692b5310edb988558
type: experiment
parents:
  - hypothesis:l4-trimguard-subcommand
next_edges: []
confidence: 0.95
edited_by: a00-698453a0
evidence_runs:
  - experiment:a00-18b5dac7-28b90e
loop: hypothesis:l4-trimguard-subcommand@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: c7b2b2ec5ea27f68
season: 2
title: A00 18b5dac7 28b90e
verdict: proved
---
## Experiment

Folded the untracked `.agi/sessions/trimguard.py` (§6 owner-quote-loss guard for
HANDOFF.md) into `extensions/agi/bin/cli.py` as a new `trimguard` subcommand,
then proved byte-behaviour-identical against the original on a controlled fixture.

**Host tool chosen: `cli.py` — why.** It is the natural host on shape alone:
it already uses argparse subparsers dispatching to `cmd_*` functions
(`cmd_done`, `cmd_pending`, `cmd_scaffold`, `cmd_claim`, `cmd_detect_stale`,
`cmd_reclaim`, `cmd_status`, `cmd_session_complete`), it is not in the
point's exclusion set, and it already imports `re`, `subprocess`, `pathlib`
and `locations`. Adding `cmd_trimguard` + one `add_parser("trimguard")` was
a one-region change with zero new imports. No other tracked bin/*.py was a
closer fit, and a NEW bin/*.py is disallowed by design (`test_bin_help_smoke`
would enrol it — the whole reason this is a fold).

**What changed.** `cmd_trimguard(args)` reproduces the original logic exactly:
locate `## §6 Owner decisions` in `HANDOFF.md` at the checkout root (parent of
the `.agi/` graph dir — `locations.find_project_root()` returns the `.agi/`
dir, so `root.parent` is the repo root where `HANDOFF.md` lives beside
`.agi/`), extract every real double-quoted span ≥25 chars (straight or curly)
plus open-ended truncated quotes, strip the `(N quotes archived)` marker, grep
`.agi/nodes/` with `grep -rlF` (cwd=repo root, same as the original), print
`MISSING` per unresolved probe, and `ABORT`(1)/`OK`(0). Exact output strings
and exit codes preserved verbatim. Registered in `main()` via
`p_tg = sub.add_parser("trimguard"); p_tg.set_defaults(func=cmd_trimguard)`.

**Verification — byte-identical on the SAME fixture.** Built a fixture root
`/tmp/tgfix/` holding a copy of the live `HANDOFF.md`, the live `.agi/nodes/`
tree (2017 files), and a stub `.agi/config.json`. Ran BOTH the original
untracked script and the folded subcommand against it:

- ABORT path: `§6 lines 175-301 bytes=14112 real quoted spans: 6`, two
  `MISSING` probes, `ABORT: 2 owner quote(s) resolve in NO node.` — exit 1
  both. `diff` of the two stdout streams: **empty (byte-identical)**.
- OK path (dropped both probes into a resolver node): `OK: all 6 owner quotes
  resolve in .agi/nodes/ — safe to collapse.` — exit 0 both. `diff`: **empty**.
- `cli.py --help` shows `trimguard` in the subparser set (not enrolled as a new
  bin file — `test_bin_help_smoke.py` still 57 passed, 1 skipped).
- `test_cli.py` 13 passed — the edited host file's own suite unaffected.

**Delete the original untracked script — YES, explicitly.** Once the tracked
`cli.py trimguard` subcommand supersedes it, the untracked
`.agi/sessions/trimguard.py` should be deleted; leaving two live copies of the
same safety check is how one gets silently stale. I did NOT delete it here:
it lives in the MAIN checkout (`/home/ubuntu/work/agi/.agi/sessions/`), a
different worktree this seat may not edit, so the deletion is a recorded
recommendation for the director, not an action I take. The port is complete;
nothing in the fold depends on the untracked file in any way (verified by
running from a clean fixture with no access to the original).

## Evidence

Fixture `/tmp/tgfix/` = HANDOFF.md copy + `.agi/nodes/` copy + `{}` config.json.
Commands run:
- `python3 /home/ubuntu/work/agi/.agi/sessions/trimguard.py`  -> exit 1 then 0
- `python3 extensions/agi/bin/cli.py trimguard` (cwd=/tmp/tgfix) -> exit 1 then 0
- `diff /tmp/tg_orig{2,3}.out /tmp/tg_fold{2,3}.out` -> no differences on either path.
- `pytest test_cli.py` -> 13 passed. `pytest test_bin_help_smoke.py` -> 57 passed, 1 skipped.
- `python3 extensions/agi/bin/cli.py --help` -> `trimguard` listed among subcommands.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-698453a0) ACCEPTED, verdict proved stands. Verified independently, not from the report: (1) cmd_trimguard exists at cli.py:1673 and is registered via add_parser("trimguard")+set_defaults at 1830-1835 — subcommand on an existing tracked tool, not a new bin/*.py; (2) logic matches the original guard section-for-section (§6 heading locate, >=25-char double-quoted spans straight/curly, archived-marker strip, open-ended truncated-quote prefix, grep -rlF, MISSING/ABORT(1)/OK(0) strings); (3) test_cli.py 13 passed re-run by reviewer, --help lists trimguard. Near miss the kid itself avoided and I confirm matters: find_project_root() returns the .agi dir, so root.parent is the only correct HANDOFF.md anchor — a naive root/"HANDOFF.md" satisfies the words and FileNotFound. Evidence-run is the experiment itself; its fixture diff (empty on both ABORT and OK paths) is the byte-identity proof. Deletion of the untracked original in the MAIN checkout is correctly left as a director recommendation — this worktree must not edit main.
<!-- THOUGHT:END -->

## Agent Notes
Folded untracked .agi/sessions/trimguard.py into cli.py as 'trimguard' subcommand (host chosen: existing argparse subparser+cmd_* shape). Byte-identical vs original on a shared fixture for both ABORT(exit1) and OK(exit0) paths. test_cli 13 passed, test_bin_help_smoke 57+1skip. Recommend deleting the untracked original (left in main — different worktree).