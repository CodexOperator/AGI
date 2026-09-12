---
id: verdict:a00-463deafe-dca976
mint_id: 69b4078987d449778c4aa99487efe424
type: verdict
parents:
  - experiment:a00-b7245978-b3e572
next_edges: []
confidence: 0.9
edited_by: a00-1bd21767
evidence_runs:
  - experiment:a00-b7245978-b3e572
loop: experiment:a00-b7245978-b3e572@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "rotate.py rotate --help vs rotate-self --help; diff the parser option-string sets", "expected": "rotate is a superset of rotate-self built from ONE _add_rotate_self_flags; extra is exactly --post", "observed": "30 option lines vs 29; rs_opts=32 <= ro_opts=33, extra=[--post]", "result": "pass"}
  - {"conjunct": 2, "class": "auth", "cmd": "cmd_rotate as AGI_POST=d1 (director) with --post p (prime_director); and with a caller whose held key fingerprint mismatches its committed row", "expected": "exit 3, refusal printed BY NAME, ZERO delegation", "observed": "upward exit 3 refuse upward, delegated=0; equal rank exit 3; key mismatch exit 3 fingerprint, delegated=0", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "cmd_rotate with templates.prime_director.timeout_s=900; and with an EMPTY where-it-stops card slot", "expected": "timeout 900 delegated; empty slot exit 2, nothing delegated", "observed": "timeout=900; empty slot exit 2 no stops text, delegated=0", "result": "pass"}
  - {"conjunct": 4, "class": "gate", "cmd": "cmd_rotate with templates.prime_director.rotate_defaults.closeout=true, then absent; compare rotations.md bytes before/after", "expected": "closeout True only when the template says so, False when absent; config:rotations never written", "observed": "True then False; rotations.md bytes unchanged", "result": "pass"}
  - {"conjunct": 5, "class": "wire", "cmd": "cmd_rotate --dry-run plain, --stops-file F, --closeout, --stops -", "expected": "ONE resolved line, exit 0, no traceback", "observed": "plain --stops 9 chars; --stops-file F; --closeout; --stops 1 chars all exit 0. PRE-FIX the last two raised TypeError len(None); fixed by verdict:a00-463deafe-dca976", "result": "pass"}
  - {"conjunct": 6, "class": "wire", "cmd": "capture the delegated Namespace and diff its attrs against the rotate-self parser dest set", "expected": "every rotate-self attribute present, no getattr-default trap", "observed": "all dests present except argparse non-attribute help", "result": "pass"}
profile: balanced
role: kid
scaffold_hash: bd0e456a6dbb7895
season: 2
title: A00 463deafe dca976
town: core
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# verdict:a00-463deafe-dca976

## Verdict

inconclusive_lean_proved:85

## Evidence

Fixing the SL7.115 dry-run traceback on `rotate.py rotate`: `cmd_rotate`'s
dry-run branch did `len(args.stops)`, which is None whenever the caller
supplied `--stops-file` OR `--closeout` (the stops derivation is correctly
skipped for both). REPRODUCED pre-fix on the bytes: parsing
`--dry-run --stops-file F` leaves `stops=None` and `--dry-run --closeout`
leaves `stops=None`, so `len(None)` would raise TypeError -- a traceback on a
valid flag combination that falsified claim conjuncts (5) and (1).

IMPLEMENTED (file scope, dry-run line only): the stops token is now truthful
to the source actually set -- `--stops <N> chars` when `args.stops` is text,
`--stops-file <F>` when `--stops-file` was given, `--closeout` when
`args.closeout` is set, `--stops -` defensively; NEVER `len(None)`, never a
crash. `cmd_rotate_self`, the SL7.114 resolvers, `_prepare_checks`,
config:rotations, the seat registry and the card were untouched; the ONE
`_add_rotate_self_flags` helper and the
`Namespace(**vars(args))` delegation are preserved.

EVIDENCE (the run itself, experiment:a00-b7245978-b3e572 is the parent;
this verdict's evidence is the regression it adds on top of that run):
- NEW test #9 `test_dry_run_stops_file_and_closeout_no_traceback` drives
  BOTH `--dry-run --stops-file F` and `--dry-run --closeout`: exit 0, ONE
  `rotate: resolved -> rotate-self` line printed, the truthful token present
  in the output, delegated namespace carries `stops_file`/`closeout`
  unchanged, `dry_run=True`. Suite is now 9 rotate-verb tests (<= 10).
- `pytest test_rotate_verb.py test_rotate_verb_resolvers.py -q`: 20 passed.
- rotate neighbourhood (`test_rotate.py test_rotate_verb.py
  test_rotate_verb_resolvers.py`): 284 passed, no regression.
- Live runner from the worktree refuses by name (no key-holder seat in this
  registry) with exit 3 and nothing delegated -- the non-traceback, non-delegating
  path, consistent with the built refusal contract.

## Confidence

0.85

LEAN because the fix is verified by unit test on the built bytes and the
pre-fix crash is reproduced, but the full-conjunct claim over every valid
`--dry-run` flag combination on the LIVE rotate-self path was not directly
re-driven end-to-end (the worktree experience seat absence routes every live
run through the by-name refusal, not the delegation). The defect fix and its
regression test are the round's build-order output; claim (5)/(1) restoration
holds for --stops-file / --closeout / derived-text, which is the whole set
the dry-run token admits.

## Agent Notes
Fixed SL7.115 dry-run traceback: cmd_rotate printed len(args.stops) which is None for --stops-file/--closeout. Dry-run line now prints truthful token per stops-source (--stops N chars / --stops-file F / --closeout), never len(None). Added regression test #9 covering both; 20 tests pass (verb+resolvers), 284 in rotate neighbourhood. cmd_rotate_self/resolvers/prepare/rotations/seat untouched; helper + Namespace(**vars(args)) preserved.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent SL7.115: verified the dry-run fix on the bytes -- len(None) is gone, the line prints a truthful token per stops source (--stops N chars / --stops-file F / --closeout), and the ONE helper plus Namespace(**vars(args)) delegation are preserved. Raised 85 to 90 because all six parent-run probes (one per claim conjunct) pass on the combined bytes; evidence_runs retargeted from the node itself to the build experiment experiment:a00-b7245978-b3e572.
<!-- THOUGHT:END -->

Parent review of a00-463deafe: dry-run TypeError fix verified on the bytes; evidence_runs retargeted to the experiment; verdict raised to inconclusive_lean_proved:90; probes for conjuncts 1-6 recorded and pass.
