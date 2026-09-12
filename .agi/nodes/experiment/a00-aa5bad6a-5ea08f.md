---
id: experiment:a00-aa5bad6a-5ea08f
mint_id: fc063275c2424902a21436e354a3af67
type: experiment
parents:
  - hypothesis:l4-the-dry-run-pathspec-and-the-alias-notice-say-only-what-is-true
next_edges: []
confidence: 0.8
edited_by: a00-0d8af889
evidence_runs:
  - experiment:a00-aa5bad6a-5ea08f
loop: hypothesis:l4-the-dry-run-pathspec-and-the-alias-notice-say-only-what-is-true@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 06d1fe160b0c0dc7
season: 2
title: SessionStart hook drops the deprecated --seat spelling; run-based test proves no unconditional notice
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-aa5bad6a-5ea08f

## Experiment — Region C: the SessionStart hook must use the current seat spelling

Acceptance criterion (Region C of `l4-the-dry-run-pathspec-and-the-alias-notice-...`):
`cc-session-start.next.sh` emits the deprecated-alias notice only when a deprecated
spelling (`--seat`, `AGI_SEAT`, `config:seats`) is actually in use for that session,
never unconditionally on every session start. Fix + a run-based test.

## MEASURED GROUND TRUTH — case (b), the claim is stale as literally stated

`rotate.py bootstrap-block` registers `--seat --post` on ONE parser through
`geometry_config.SeatAction`; a literal `--seat` fires `_FLAG_DEP_MSG`
("note: --seat is deprecated; use --post this season.") to **stderr**. The hook
wraps that python call in `$( ... 2>/dev/null || true )`, so the notice is
**swallowed** — NOTHING visible escapes to the session.

Direct probe (this tree, pre-fix):
```
$ python3 extensions/agi/bin/rotate.py bootstrap-block --seat nosuchseat --root . 2>err
rc=1 err="note: --seat is deprecated; use --post this season."
$ python3 extensions/agi/bin/rotate.py bootstrap-block --post nosuchseat --root . 2>err
rc=1 err=""   (silent)
```

```
$ bash hooks/cc-session-start.next.sh   (tmp project, AGI_SEAT set)
rc=0  notice lines stdout=0 stderr=0      <- nothing visible, despite deprecated env+flag spelling present
```

So the defect in the handed tree was **(b)**: the hook still **invoked the
deprecated `--seat` spelling** and no test pinned it. The literal-round claim
"emits the notice on every session start" is FALSE as written; what was true is
"invokes the deprecated spelling".

## The fix (both parts)

**1. Hook spelling.** In BOTH `extensions/agi/hooks/cc-session-start.next.sh`
(line 241) and `cc-session-start.sh` (line 238), the bootstrap invocation is now:
```
"$PLUGIN_ROOT/bin/rotate.py" bootstrap-block --post "$BOOTSTRAP_SEAT" \
  --root "$PROJECT_ROOT" 2>/dev/null || true)"
```
No literal `--seat` remains anywhere in either hook (`grep -- '--seat'` = empty).
`BOOTSTRAP_SEAT="${AGI_POST:-${AGI_SEAT:-}}"` already prefers AGI_POST and only
falls back to the deprecated AGI_SEAT. The stale comment ("named by AGI_SEAT")
was corrected to name AGI_POST as primary, AGI_SEAT as deprecated fallback.
The two hooks still differ ONLY in their header (verified by `diff`), so they
stay in step.

**2. New run-based test** `extensions/agi/tests/test_hook_alias_notice.py` — a
NEW file (region B's `test_seat_alias_notice.py` is untouched). Parametrized over
BOTH hooks; each is run as a real subprocess (`bash <hook>`, cwd = a tmp project
with `.agi/config.json` + `.agi/context/INJECTION.md`, stdout and stderr captured
SEPARATELY) twice: Run A with `AGI_SEAT` (deprecated env spelling, no AGI_POST),
Run B with `AGI_POST` (current spelling, no AGI_SEAT).
Assertions (all observe real subprocess output): rc==0 both; the
`--seat`/`AGI_SEAT`/`config:seats` `is deprecated` family appears **0 times on
the current-spelling run** and at most once across both runs. A SECOND, cheaper
source guard keys to the ONE bootstrap-call line (the two-line invocation) to
pin `--post` present and `--seat` absent — never the only check, the run-based
test is.

## BEFORE / AFTER

BEFORE (hook still `--seat`): `pytest test_hook_alias_notice.py -q` →
`2 passed` (both run-based assertions!) and the source guard `FAILED`
(bootstrap call still carries `--seat`, no `--post`).
That is the honest stale-claim signature: the swallow makes the visible notice
unobservable at the subprocess boundary, so the run-based criterion held even
pre-fix; only the mechanism-level guard caught the deprecated spelling.

AFTER (both hooks on `--post`): all 3 tests pass.

## Proof

```
$ python3 -m pytest extensions/agi/tests/test_hook_alias_notice.py extensions/agi/tests/test_geometry_config.py -q
20 passed in 3.69s

$ python3 -m pytest extensions/agi/tests/test_seat_alias_notice.py extensions/agi/tests/test_post_rename.py -q
40 passed in 15.91s     (sibling regions A+B still green, shared infra intact)
```

Real hook output after the fix, both runs of `hooks/cc-session-start.next.sh`
in a tmp project (cache reused; map + injection emitted, no notice):
```
$ env -u AGI_POST AGI_SEAT=seatA bash hooks/cc-session-start.next.sh 1>out 2>err ; echo rc=$?
rc=0     notice lines stdout=0 stderr=0
$ env -u AGI_SEAT AGI_POST=postB bash hooks/cc-session-start.next.sh 1>out 2>err ; echo rc=$?
rc=0     notice lines stdout=0 stderr=0
# stdout tail (identical shape both runs):
# ## agi-tree map (auto-injected) ... Full injection at .../INJECTION.md. Skill: agi.
# stderr: empty
```

## THOUGHT
Hook resolution resolves the project root to the `.agi` GRAPH dir (goal:g11),
so the injection file must live at `.agi/context/INJECTION.md`, not
`context/` beside it — a first draft placed it at the wrong level and the hook
self-healed by rebuilding via inject.py (worked, but slow/nondeterministic).
Fixed the helper to reuse the cache deterministically (3.69s vs slower).

## Agent Notes
Region C: switched SessionStart bootstrap-block to --post in both hooks (no --seat left), added run-based test_hook_alias_notice.py (parametrized both hooks, subprocess cwd=tmp project, stdout/stderr separate). Measured ground truth was (b): notice swallowed by 2>/dev/null so the literal claim was stale; test passed pre-fix on run-based asserts, source guard caught the --seat. Post-fix 20 green (region C + geometry), 40 green (siblings).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Region C reviewed and accepted by parent a00-0d8af889, 2026-09-12. The kid did the honest thing I briefed it to do: it MEASURED rather than parroted the claim and found the literal claim ("emits the deprecated-alias notice on every session start") is stale, because the hook wraps the rotate.py call in `$( ... 2>/dev/null || true )` and the SeatAction notice goes to stderr, so nothing visible escapes. I had measured the same thing before spawning and the kid reached it independently. The real fixable defect was invoking the deprecated spelling, and both hooks (cc-session-start.next.sh and cc-session-start.sh) now call `rotate.py bootstrap-block --post ...`; `grep -- --seat` over both hooks is empty. I verified the mechanism myself: read the cached diff, confirmed the only two-line bootstrap invocation changed from --seat to --post in BOTH hooks and the stale "named by AGI_SEAT" comment now names AGI_POST primary with AGI_SEAT as deprecated fallback, and ran `pytest extensions/agi/tests/test_hook_alias_notice.py -q` -> 3 passed. The falsifier subtlety is the valuable part and it is recorded correctly: the kid reports that pre-fix the RUN-based assertion PASSED (the swallow makes the notice unobservable at the subprocess boundary) and only the source-level guard keyed to the bootstrap invocation caught the deprecated spelling -- i.e. the run-based criterion alone was vacuous for this defect, and the second guard is what bites. Non-blocking residue: the run-based test cannot distinguish a hook that re-adds `2>/dev/null` from one that never emitted, so the guarantee that a future notice would SURFACE is carried by the source guard, not by the subprocess observation; a future round could drop the swallow so a real notice is observable and the run-based assert becomes the load-bearing one.
<!-- THOUGHT:END -->
