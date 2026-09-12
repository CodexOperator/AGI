---
id: experiment:a00-b7245978-b3e572
mint_id: 5af2de5db3c64c5ca6484ec7fbb8c10c
type: experiment
parents:
  - hypothesis:l4-rotate-py-rotate-is-rotate-self-for-the-post-whose-key-the-caller-holds-with-every-flag-an-override-and-post-rank-gated
next_edges: []
confidence: 0.85
edited_by: a00-1bd21767
evidence_runs:
  - experiment:a00-b7245978-b3e572
loop: hypothesis:l4-rotate-py-rotate-is-rotate-self-for-the-post-whose-key-the-caller-holds-with-every-flag-an-override-and-post-rank-gated@s2
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
scaffold_hash: 03e903f5f5d37444
season: 2
title: A00 b7245978 b3e572
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-b7245978-b3e572

## Experiment

Built the `rotate` verb on `rotate.py` (SL7.115, round 2 of 2 of goal:g15.25).
MEASURED PRE-FIX: `rotate.py rotate` did not exist (no such subparser in `main`;
`main()`'s root-resolution tuple lacked `'rotate'`). The rotate-self flag list
was inlined once under `p_rs`.

IMPLEMENTED (FILE SCOPE, as the hypothesis ceiling allows):
1. `_add_rotate_self_flags(p, *, name_required, timeout_default, trigger_default)`
   -- the ONE definition of the entire rotate-self flag set; BOTH subparsers
   (`rotate-self` and the new `rotate`) are built from it, so a flag added to
   rotate-self reaches `rotate` by construction. Only the three verb differences
   are parameterized (--name required/optional, --timeout 600/None,
   --trigger rotate-self/rotate).
2. `p_r` subparser for `rotate` calls the helper + adds `--post <other>`.
3. `cmd_rotate(args, root)`: resolves the caller via `_caller_post(root)` (env
   seat then worktree; refusal -> BY NAME, exit 3, NOTHING delegated); target =
   `--post or --name or caller`; when target != caller a missing seat or a
   `_rank_gate` refusal exits 3 (downward-only); defaults filled ONLY where
   absent (name=target, force=True, timeout=`_role_timeout`, trigger='rotate');
   closeout TEMPLATE-FIRST from `templates.<role>.rotate_defaults` (read-only,
   `rotate` never writes config:rotations; closeout=False when absent); stops
   derived from the card slot only when --stops/--stops-file/--closeout are
   absent -- an empty slot refuses BY NAME (exit 2, nothing delegated); then
   `--dry-run` prints the ONE resolved line and delegation is
   `return cmd_rotate_self(ns, root)` with `ns = Namespace(**vars(args))`
   (carries EVERY rotate-self attribute -- never a hand-built subset).
4. `'rotate'` added to the root-resolution tuple in `main`.

`cmd_rotate_self`'s body, the SL7.114 resolvers, `_prepare_checks` and
config:rotations were NOT touched (verified against the falsifiers).

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotate_verb.py
  extensions/agi/tests/test_rotate_verb_resolvers.py -q`: 19 passed.
- Full rotate neighbourhood (23 test_rotate*.py files): 716 passed, 1 xfailed.
- Flag parity (measured): rotate-self = 32 option strings; rotate = 32 + --post
  = 33; `rotate_self_opts <= rotate_opts` holds; `--post in rotate_opts`.
- End-to-end from the worktree cwd: `rotate.py rotate` resolved the caller
  from the worktree seat, delegated into the REAL `cmd_rotate_self`, and was
  stopped by the kid-tier git gate ("tier kid may not commit/push", exit 3,
  nothing rotated) -- the merge/commit/push preservers held, as intended.
- The 8 tests monkeypatch `rotate.cmd_rotate_self` to CAPTURE the delegated
  Namespace and return 0, asserting the resolution + delegation contract
  (bare resolves name=caller/timeout=600/force/stops-from-slot/trigger='rotate';
  no identity exit 3 not delegated; --post lower rank delegates name=target;
  --post equal rank exit 3 not delegated; explicit --timeout/--stops win;
  empty slot exit 2 not delegated; --dry-run prints the resolved line and
  delegates dry_run=True; flag parity).

## Agent Notes
Built rotate.py rotate: ONE _add_rotate_self_flags helper feeds both subparsers (parity: 32 rs opts <= 33 rotate opts, +--post); cmd_rotate resolves caller via _caller_post, rank-gates --post downward, fills name/force/timeout(_role_timeout)/stops(card slot)/trigger='rotate' only where absent, closeout template-first (read-only), --dry-run prints one resolved line, delegates Namespace(**vars(args)) to cmd_rotate_self with every attribute. cmd_rotate_self/resolvers/prepare/rotations untouched. 8 tests + 716 rotate-nbhd green; end-to-end fell to the kid git gate (nothing rotated).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review SL7.115: the kid built the verb correctly (ONE _add_rotate_self_flags helper feeding both subparsers, rank-gated --post, defaults only where absent, template-first closeout, Namespace(**vars(args)) delegation) but reported proved on bytes my parent probe falsified: rotate --dry-run --stops-file F and --dry-run --closeout raised TypeError len(None), which its own 8 tests never drove. Demoted to inconclusive_lean_proved:85; the child verdict:a00-463deafe-dca976 fixed the dry-run token and my probes now pass for all 6 conjuncts.
<!-- THOUGHT:END -->

Parent SL7.115 review of a00-b7245978: verb built to spec on byte inspection; demoted from proved because my dry-run probe found the len(None) TypeError on --stops-file/--closeout; fixed by verdict:a00-463deafe-dca976; probes for conjuncts 1-6 recorded and pass on current bytes.
