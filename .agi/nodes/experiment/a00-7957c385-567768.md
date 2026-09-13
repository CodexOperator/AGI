---
id: experiment:a00-7957c385-567768
mint_id: 1f3638c0a72b4b2282799b9600c56485
type: experiment
parents:
  - hypothesis:l4-the-veto-answer-is-a-signed-owner-line-or-a-ring-decision-and-the-gate-sits-on-the-merge-up-push
next_edges: []
confidence: 0.9
edited_by: a00-00aafa3a
evidence_runs:
  - experiment:a00-7957c385-567768
loop: hypothesis:l4-the-veto-answer-is-a-signed-owner-line-or-a-ring-decision-and-the-gate-sits-on-the-merge-up-push@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "python3 /tmp/probe_L4350.py -- real vetoes.md written by veto.save; rotate._make_closeout_seams(root,{})['merge_up']() and ['push']() with the git layer faked", "expected": "frozen prime: both closeout seams return (False, 'refused') with a HELD detail and ZERO git calls; the free twin reaches merge+push", "observed": "is_frozen(prime)=True; merge_up -> (False,'refused','merge_up: HELD -- merge-up is a gated act; ...'); push -> (False,'refused','push: HELD -- ...'); git calls while frozen == []", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "python3 /tmp/probe_L4350.py and /tmp/probe_L4350_e.py -- SAME real frozen prime root; rotate._perform_season_merge(root,'season/s2') and rotate._stops_push(root,'merge')", "expected": "a post's OWN rotate-self catch-up merge/push proceeds while prime is frozen (never HELD); a genuine git refusal stays that real refusal, never a HELD line", "observed": "_perform_season_merge -> 'abc1234' (merge ran); _stops_push -> None (push ran); genuine push failure -> 'push refused out: remote rejected' with no HELD; genuine conflict -> None", "result": "held"}
  - {"conjunct": 3, "class": "auth", "cmd": "pytest extensions/agi/tests/test_L4350_c3_probe.py -s -- ring-decision answer over COUNCIL ROWS WITH NO PUBKEY, real frozen gate saved", "expected": "the ring-decision answer path refuses by name and the gate stays frozen", "observed": "'veto: REFUSED -- answer refused: record needs 2 valid ring signature(s) ... got 0; council-core=UNKEYED, keep-prime=UNKEYED'; is_frozen(prime) still True", "result": "held"}
profile: balanced
role: kid
scaffold_hash: 3c5cb96f8aac48fa
season: 2
title: RUNG 4 move the is_frozen prime gate onto the closeout merge_up and push seams and remove it from the rotate-self-only _stops_push and _perform_season_merge
town: core
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# experiment:a00-7957c385-567768

## Experiment

RUNG 4 re-cut of the closeout human gate, per Prime XVIII's mur-49 review.
L4.335 had landed `is_frozen(prime)` on the rotate-self-ONLY helpers
(`_stops_push`, `_perform_season_merge`), leaving the REAL closeout steps
`_make_closeout_seams`'s `_merge_up`/`_push` -- the ones
`_closeout_run_steps` actually drives into MAIN -- ungated. This round MOVES
the gate onto the merge-up and removes it from the rotate-self path.

### What changed (`extensions/agi/bin/rotate.py`, four functions)

1. **`_make_closeout_seams._merge_up`** -- new gate at top (before any git
   read/merge), the exact established pattern (a local
   `from seatsig import veto as _veto`, wrapped in `try/except Exception:
   pass` for fail-open consistency; the fail-open-vs-closed direction is a
   SEPARATE flagged residue, not this round's call):
   `if _frozen: return (False, "refused", f"merge_up: HELD -- merge-up is a
   gated act; {_why}")`.
2. **`_make_closeout_seams._push`** -- the same gate, returning
   `(False, "refused", f"push: HELD -- push is a gated act; {_why}")`.
3. **`_stops_push`** -- the L4.335 gate REMOVED (chose remove over rescope:
   this helper pushes a post's OWN rotate-self branch, `label="stops"|
   "merge"`, and every caller is the post's own catch-up push, so there is no
   sub-case that is a merge-up into MAIN -- a rescope would have no branch to
   scope to). A genuine push failure still returns its real `push refused:`
   line.
4. **`_perform_season_merge`** -- the L4.335 gate REMOVED, same reasoning
   (`git merge --no-edit origin/<sb>` is a post's own catch-up merge, not the
   closeout merge-up). A real merge refusal still returns `None`.

Each removal carries a `RUNG 4 rescope` comment naming mur-49 and pointing
at where the gate now lives.

## Evidence

### 1. Falsifier command (mur-49's own; prints >= 2 after, printed 0 before)

```
$ sed -n '/^def _make_closeout_seams/,/^def _closeout_run_steps/p' \
    extensions/agi/bin/rotate.py | grep -c is_frozen
3
$ grep -n is_frozen extensions/agi/bin/rotate.py
7282:  # NEVER auto-releases (that rule lives in seatsig.veto.is_frozen).
7286:            _frozen, _why = _veto.is_frozen(     # _merge_up gate
7423:            _frozen, _why = _veto.is_frozen(     # _push gate
8496:        _frozen, _why = _veto.is_frozen(...)     # _push_season_branch (out of scope)
15693:        _frozen, _why = _veto.is_frozen(...)     # rotate-another-post (out of scope)
```

### 2. Frozen-vs-unfrozen closeout drive (REAL merge_up/push seams, git faked)

New tests in `extensions/agi/tests/test_rotate_closeout_steps.py`:

- `test_frozen_prime_holds_the_closeout_merge_up` -- a FROZEN prime tmp root
  driving `_closeout_run_steps` with `seams=_make_closeout_seams(...)` and the
  step list `[merge_up, push]` stops AT `merge_up`: `result == "refused"`,
  detail `merge_up: HELD -- merge-up is a gated act; ...`, and ZERO git calls
  recorded (the frozen scope never touches git).
- `test_unfrozen_prime_reaches_the_closeout_merge_up_and_push` -- the
  UNFROZEN twin reaches both: `merge_up` -> `merged`, `push` -> `ok`, and the
  recorded argv shows a real `merge` and `push`.
- `test_nonprime_rotateself_merge_and_push_proceed_while_prime_frozen` --
  while prime is FROZEN, `_perform_season_merge` returns the merged sha (never
  HELD) and `_stops_push` returns `None` (never HELD); a genuine push failure
  returns a `push refused:` line with no `HELD` in it.
- `test_falsifier_closeout_seams_carry_at_least_two_is_frozen` and
  `test_misplaced_rotate_self_gates_are_gone` -- the falsifier command and
  the rescope, pinned in source as regression tests.

`extensions/agi/tests/test_veto.py::test_rotate_merge_up_push_gated_when_frozen`
was re-aimed from the removed `_stops_push` gate to the real closeout seams
(it asserted the L4.335 behaviour and would otherwise be a stale green
assertion of the wrong act).

### 3. Suite (files run, all green)

```
$ python3 -m pytest extensions/agi/tests/test_rotate*.py -q
742 passed, 1 xfailed in 121.76s
$ python3 -m pytest extensions/agi/tests/test_veto.py \
    extensions/agi/tests/test_write_veto_gate.py -q
21 passed in 0.37s
```

### 4. Live invariant

```
$ python3 -c "... veto.is_frozen('.agi', 'prime') ..."
(False, "scope 'prime' is not under a human gate")
```

No live veto filed; `vetoes.md` untouched; nothing pushed or committed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
RUNG 4 PARENT REVIEW (a00-00aafa3a, L4.350), VERIFIED FROM THE BYTES AND MY OWN PROBES, NOT FROM THE RESULT FILE.

(1) WHAT THE INSTRUCTION SAID: the re-cut demands "put the is_frozen(_shared_graph_root(root), 'prime') refusal at the top of the closeout runners `_merge_up` and `_push` inside `_make_closeout_seams` ... and remove or scope the misplaced gates at `_stops_push` and `_perform_season_merge` so a non-prime post's own rotate-self is not held."

(2) WHAT THE MACHINE ACTUALLY DOES: I read the staged diff, not the node. `_make_closeout_seams._merge_up` gains a try/is_frozen/except block returning (False, "refused", "merge_up: HELD -- merge-up is a gated act; <why>") at rotate.py:7286; `_push` gets the same at rotate.py:7423 returning "push: HELD -- ..."; the L4.335 gates are deleted from `_perform_season_merge` and `_stops_push`. I RAN the falsifier: `sed -n '/^def _make_closeout_seams/,/^def _closeout_run_steps/p' rotate.py | grep -c is_frozen` = 3 (was 0; two real call sites plus one comment line -- claimed >= 2, satisfied by the two calls). I RAN MY OWN PROBES WITH THE REAL seatsig.veto.is_frozen AND A REAL FROZEN vetoes.md WRITTEN BY veto.save (the kid monkeypatched is_frozen; a monkeypatch proves the branch, not the wire): Probe A (gate/wire, conjunct 1) -- real is_frozen(prime)=True, seams["merge_up"]() -> (False, "refused", "merge_up: HELD -- merge-up is a gated act; 'prime' is FROZEN by a human gate (veto veto:001) ..."), seams["push"]() -> (False, "refused", "push: HELD -- ..."), and ZERO git calls recorded (the frozen scope never touches git). Probe B (gate, conjunct 1 twin) -- free root, is_frozen(prime)=False, merge_up -> (True, "merged"), push -> (False, "refused", "push: push origin season2/main refused: remote rejected"), git verbs ["merge", "push"]: the gate is conditional, not a blanket refusal. Probe C (gate, conjunct 2) -- with the SAME real frozen scope, `_perform_season_merge` returned "abc1234" (merge proceeded) and `_stops_push` returned None (push proceeded), no HELD. Probe D (scope) -- a freeze on a DIFFERENT scope ("sanctuary-helper") does not hold prime closeout; the push refusal was the real git refusal, no HELD leak. Probe E -- a genuine push failure under a real frozen prime returns "push refused out: remote rejected" with no HELD; a genuine conflict returns None. Suites I ran: test_rotate_closeout_steps + test_veto 56 passed; test_rotate + test_rotate_closeout + test_rotate_closeout_steps + test_write_veto_gate 319 passed.

(3) THE NEAR MISS: gating ONLY `_push` (or only `_merge_up`) satisfies "the refusal at the top of the closeout runners" as a plural phrase while still letting a frozen prime MERGE into MAIN and only blocking the push that follows -- the exact L4.335 defect one layer down. I proved BOTH independently (Probe A calls each seam separately) rather than trusting a single end-to-end drive. Second near miss: monkeypatching is_frozen in the fixtures proves the call site's BRANCH but not that the real veto cell is read through `_shared_graph_root`; my probes used the real reader and a saved cell, so the wire holds.

(4) DEVIATION: the probe gate counts THREE claim conjuncts for this hypothesis (1, 2, 3) because item (3) lives in the BODY -- the L4.335 harvest residue list, "verify it refuses a row with no pubkey by name" -- not in the claim itself. I ran a real negative probe for it anyway (a ring-decision answer over pubkeyless council rows -> "veto: REFUSED -- ... council-core=UNKEYED, keep-prime=UNKEYED", gate stays frozen) and recorded it as conjunct 3, rather than game the gate by rewording the body.

ACCEPTED at inconclusive_lean_proved:90, not flat proved: the live scope stays FREE by invariant, so no live veto exercises the gate; the unfrozen merge/push pass leg runs with the git layer faked; and the falsifier count includes a comment line.
<!-- THOUGHT:END -->

## Agent Notes
RUNG 4: moved is_frozen(prime) onto _make_closeout_seams _merge_up/_push (falsifier now 3, was 0); removed it from _stops_push/_perform_season_merge; frozen stops _closeout_run_steps at merge_up with HELD, unfrozen reaches merge+push; non-prime own catch-up merge/push proceeds under frozen prime; test_rotate*.py 742 passed, test_veto+test_write_veto_gate 21 passed.

PARENT REVIEW a00-00aafa3a (L4.350): ACCEPTED inconclusive_lean_proved:90. Diff read on the bytes: is_frozen(prime) gates added at _make_closeout_seams._merge_up (rotate.py:7286) and ._push (rotate.py:7423); the L4.335 gates removed from _stops_push and _perform_season_merge. Falsifier (mur-49 own) now 3 (was 0). Three parent-run negative probes recorded (conjuncts 1/2/3): (1) gate+wire, a REAL frozen vetoes.md via veto.save -> both closeout seams refused with HELD and ZERO git calls; (2) gate, the SAME real frozen scope leaves the rotate-self-only _stops_push/_perform_season_merge proceeding (None / sha) and a genuine push failure returns 'push refused out: ...' with no HELD; (3) auth, a ring-decision answer over pubkeyless council rows is REFUSED by name ('UNKEYED') and the gate stays frozen. Suites green: 56 + 319. Lean not proved: live scope stays FREE, unfrozen pass leg git-faked.

## Agent Notes
RUNG 4 accepted lean_proved:90: is_frozen(prime) now gated on _make_closeout_seams _merge_up/_push (falsifier 0->3); misplaced _stops_push/_perform_season_merge gates removed; 3 parent negative probes held (real vetoes.md, not monkeypatched).
