---
id: experiment:a00-8632c40f-52c98f
mint_id: f2224d1c6bb545a3b33fa97910547c18
type: experiment
parents:
  - hypothesis:l4-reshuffle-delete-old-is-never-unfiltered-and-post-n-maps-to-season2-posts
next_edges: []
confidence: 0.9
edited_by: a00-d5b6e48c
evidence_runs:
  - experiment:a00-8632c40f-52c98f
loop: hypothesis:l4-reshuffle-delete-old-is-never-unfiltered-and-post-n-maps-to-season2-posts@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 7ea02987121ca3be
season: 2
title: A00 8632c40f 52c98f
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-8632c40f-52c98f

## Experiment — build the `post/<n>@sN` intermediate alias rule in branches.py

Prime ruling (goal:g17.1, window-46): "branches.py gets the post/<n>@sN
intermediate rule so reshuffle maps it to season2/posts/<n>".

**BEFORE (the defect, measured today ):**
```
$ python3 -c "import sys; sys.path.insert(0,'extensions/agi/bin'); import branches; print(branches.parse('post/foo@s2'))"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File ".../extensions/agi/bin/branches.py", line 259, in parse
    raise ValueError(f"unrecognised branch name: {name!r}")
ValueError: unrecognised branch name: 'post/foo@s2'
```
`_canonical_to_old('season2/posts/foo')` -> `seat/foo@s2` (only the deprecated
spelling, no intermediate).

**Implemented in `extensions/agi/bin/branches.py` only** (KID A owns cli.py):
1. Added `_POST_AT_RE = re.compile(r"^post/(.+?)@s(\d+)$")` beside `_SEAT_RE`.
2. `_alias_canonical` gains a `_POST_AT_RE` branch BEFORE the loop branch, so
   `post/<n>@sN` -> `season{int(group(2))}/posts/group(1)` — the intermediate
   alias of a post, same place `seat/<n>@sN` keys. Never raises: it is an
   alias, parse returns kind="alias" + canonical.
3. `_canonical_to_old` gained a `legacy_seat: bool = False` keyword. The posts
   reverse now returns the INTERMEDIATE spelling `post/<n>@sN` by default; with
   `legacy_seat=True` it returns the DEPRECATED `seat/<n>@sN`. `ref_candidates`
   passes `legacy_seat=True`, so a reader handed a canonical POST name on a
   PRE-migration tree still finds the live seat branch (the pinned contract
   `test_ref_candidates_post_keeps_legacy_seat_alias` stays green untouched).
4. The `seat/<n>@sN` deprecated alias is untouched and keeps parsing.
5. `town/<t>@s<N>` gap in `_canonical_to_old` NOT touched — out of round (it is
   `town/<t>/season/s<k>`, not the intermediate post rule's table).

**WHY default-reverse returns the intermediate, not the legacy seat/ (chosen
deliberately):** the g17.1 ruling names `post/<n>@sN` THE intermediate alias;
`_canonical_to_old` inverts the alias table, so asking the reverse for the
alias of a post yields that intermediate spelling. Both spellings stayed
producible (the assignment's own hedge), so no reader lost the seat/ fallback —
`ref_candidates` keeps it via the flag, and the two are tied in the `_canonical
_to_old` test. cli.py's own reshuffle (`--dry-run`/`--apply`) composes the
`post/<n>@s2` target from a JSON record, not from this reverse, so this change
cannot perturb the live rename path.

**AFTER (measured on built bytes):**
```
$ python3 -c "... branches.parse('post/foo@s2') ..."
branches.py: deprecated alias used: post/foo@s2 -> season2/posts/foo
{'kind': 'alias', 'season': 2, 'name': 'foo', 'canonical': 'season2/posts/foo'}

$ python3 -c "... branches._canonical_to_old('season2/posts/foo'); ..."
post/foo@s2          <- intermediate (default)
seat/foo@s2          <- deprecated (legacy_seat=True)
```
`parse('seat/foo@s2')` still -> canonical `season2/posts/foo` (alias intact);
`ref_candidates('season2/posts/foo')` still -> `['season2/posts/foo','seat/foo@s2']`.

**Tests added** — `test_branches.py`:
- `post/foo@s2` parses to canonical `season2/posts/foo`, no raise;
- round-trip: `_canonical_to_old(canonical) == "post/foo@s2"`;
- reverse under `legacy_seat=True` == `seat/foo@s2`;
- `seat/foo@s2` still resolves (alias intact);
- negative: `post/foo` (no @sN) and `post/foo@s` (no digits) still raise.
`test_branch_reshuffle.py` (ADD only): a `post/post-y@s2` branch on the fixture
remote, dry-run plan names `post/post-y@s2` and `season2/posts/post-y` with no
"NO-MATCH". --dry-run only, never --apply.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_branches.py -q
tier-gate: phantom running record ... (dead) -- skipped
..................................................   [100%]
50 passed in 0.14s

$ python3 -m pytest extensions/agi/tests/test_branch_reshuffle.py -q
tier-gate: phantom running record ... (dead) -- skipped
................   [100%]
16 passed in 9.87s   (15 KID A + 1 ADD dry-run intermediate test)
```
(tier-gate line is the repo's shared phantom-record notice, not a failure.)

**Disproof (what would disprove this round):** `post/<n>@s2` fails to map to
`season2/posts/<n>`, or `seat/<n>@s2` stops resolving, or the reshuffle dry-run
reports NO-MATCH / a wrong kind for the post branch. None observed: the built
bytes parse backwards and forwards, seat/ intact, dry-run composes the
canonical with no NO-MATCH.

Live steps (`--apply`, `--delete-old`) never run against the real tree — HELD.

## Agent Notes
branches.py gains the post/<n>@sN intermediate alias (forward maps to season2/posts/<n>, never raises) plus a legacy_seat kwarg so _canonical_to_old returns post/...@sN by default while ref_candidates keeps the seat/ deprecated fallback; tests green 50+16, dry-run composes post/post-y@s2 -> season2/posts/post-y with no NO-MATCH; live steps HELD.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEWED by parent a00-d5b6e48c (L4.319), verdict kept: proved.

(1) INSTRUCTION: Prime window-46 HOLD line (goal:g17.1) -- "branches.py gets the post/<n>@sN intermediate rule so reshuffle maps it to season2/posts/<n>".
(2) WHAT THE MACHINE DOES, read on the built bytes: branches.py L56 defines _POST_AT_RE = ^post/(.+?)@s(\d+)$; the _alias_canonical branch at L298 maps it to season{int(group(2))}/posts/{group(1)} before the loop rule, so parse("post/foo@s2") returns kind=alias canonical=season2/posts/foo and never raises. _canonical_to_old gains keyword-only legacy_seat=False (L130), post branch at L148-155 returns post/<n>@sN by default and seat/<n>@sN when legacy_seat=True; ref_candidates (the only in-engine caller, L124) passes legacy_seat=True, so the pre-migration seat fallback survives untouched. Measured by hand, not trusted: parse(post/foo@s2) -> season2/posts/foo; parse(seat/foo@s2) unchanged; _canonical_to_old -> "post/foo@s2" default and "seat/foo@s2" with the flag; ref_candidates -> ["season2/posts/foo","seat/foo@s2"]. Re-ran the three suites myself: test_branches.py + test_branch_reshuffle.py + test_cli.py -> 85 passed.
(3) NEAR MISS: flipping the _canonical_to_old DEFAULT for posts without the legacy_seat flag. That satisfies the ruling words ("the reverse yields the intermediate spelling") and silently breaks every pre-migration reader that asked the function for the DEPRECATED spelling -- ref_candidates would hand back a branch name no live tree carries, and test_ref_candidates_post_keeps_legacy_seat_alias would have been the only thing standing. KID B added the kwarg instead of the flip, so both spellings stay producible and only the default moved.
(4) DEVIATION: none. Live steps (--apply, --delete-old) not run, stated on the node.

DEFECT FOUND, NOT THE KID S OWN FILE: cli.py _reshuffle_canonical (L2426-2436) still carries the comment "The only name branches.py does not know is post-rename s own output post/<name>@s<N>" and its _RS_POST_RE fallback at L2434. That sentence is now FALSE -- branches.py knows it (this node) -- and the fallback is unreachable for this shape because branches.parse now returns an alias first. Harmless (post_branch(2,"foo") == season2/posts/foo, same answer) but the comment tells a later reader something untrue. cli.py was KID A s scope and is out of this kid s file scope; recorded here as the sharper edge for a follow-up round, not a reason to demote.
<!-- THOUGHT:END -->

Parent review (a00-d5b6e48c, L4.319): ACCEPTED, verdict proved, evidence_runs resolves to this node. branches.py _POST_AT_RE + legacy_seat kwarg implemented as ruled; 85 tests green re-run by the parent; parse/round-trip/ref_candidates measured by hand. Caveat: cli.py _reshuffle_canonical comment is now stale and its _RS_POST_RE fallback unreachable (cli.py out of this kid scope). Live steps HELD.
