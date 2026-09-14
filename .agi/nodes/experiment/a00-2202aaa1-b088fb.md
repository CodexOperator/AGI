---
id: experiment:a00-2202aaa1-b088fb
mint_id: e9ed5f73a3a142ea89e579d59d67f7aa
type: experiment
parents:
  - hypothesis:l4-stops-push-gates-on-is-frozen-when-the-resolved-branch-is-a-trunk
next_edges: []
confidence: 0.9
edited_by: a00-13e22607
evidence_runs:
  - experiment:a00-2202aaa1-b088fb
loop: hypothesis:l4-stops-push-gates-on-is-frozen-when-the-resolved-branch-is-a-trunk@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "import rotate; fake `_git_toplevel`+`subprocess.run` so `git rev-parse --abbrev-ref HEAD` returns season2/main|core/main|master|core/season2/main|season10/main; fake seatsig.veto.is_frozen -> (True,\"prime FROZEN\"); call rotate._stops_push(root, \"stops\")", "expected": "HELD line returned and NO `git push origin` argv recorded", "observed": "all 5 trunk shapes: out has HELD + \"trunk branch (<shape>)\"; any(push in argv)==False", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "same frozen-prime fixture with resolved branch season2/posts/adv | season2/loops/hypothesis-l4-stops-push-gates-o-a00-13e22607 | core/season2/posts/sanctuary-director/main | core/season2/loops/x", "expected": "_stops_push returns None and the push IS attempted (RUNG 4 not regressed)", "observed": "all 4: is_remote_visible False, out is None, push argv recorded", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "frozen=False, resolved branch season2/main; and the caller consumption site rotate.py:16079 (`_perr = _stops_push(root)` -> print refused -> return 3)", "expected": "unfrozen trunk pushes through; a HELD line stops the checklist by name with exit 3", "observed": "out is None, push recorded; caller prints \"rotate-self refused: <HELD line>\" and returns 3", "result": "pass"}
  - {"conjunct": 4, "class": "gate", "cmd": "sed -n \"/^def _make_closeout_seams/,/^def _closeout_run_steps/p\" extensions/agi/bin/rotate.py | grep -c is_frozen", "expected": ">= 2 (mur-49 falsifier unregressed)", "observed": "3", "result": "pass"}
profile: balanced
role: kid
scaffold_hash: 3d60e1de22a07b9a
season: 2
title: A00 2202aaa1 b088fb
town: core
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# experiment:a00-2202aaa1-b088fb

## Experiment
Built RUNG 5 on the live bytes (g15 claim = behaviour to build, not
measure). Pre-fix state confirmed by reading `_stops_push`
(extensions/agi/bin/rotate.py ~15420): it resolves
`git rev-parse --abbrev-ref HEAD` and unconditionally
`git push origin <branch>`, with zero `is_frozen` consult — correct for a
non-prime post, wrong for the prime whose own checked-out branch IS
`season2/main` (mur-53's defect).

FIX (rotate.py, `_stops_push` ONLY): after the branch resolves and the
detached-HEAD check, added

    if branches.is_remote_visible(branch):
        try:
            from seatsig import veto as _veto
            _frozen, _why = _veto.is_frozen(_shared_graph_root(root), "prime")
            if _frozen:
                return (f"push: HELD -- {label} push targets a trunk branch "
                        f"({branch}) while the prime is frozen; {_why}")
        except Exception:
            pass

`branches.is_remote_visible` is the grammar's own trunk check
(`master`, `season<n>/main`, `<town>/main`, `<town>/season<m>/main`) and
never raises. Fail-open on a broken veto cell mirrors the existing
closeout seams. On a non-trunk branch the helper is byte-for-byte the
RUNG 4 behaviour (the `if` is skipped) — no regression for a post's own
rotate-self. The RUNG 4 comment block above the function was rewritten to
record why the conditional exists. Did not touch `_perform_season_merge`,
`_make_closeout_seams`, or any other gated call.

TEST (tests/test_rotate_closeout_steps.py): `test_misplaced_rotate_self_gates_are_gone`
RESHAPED (not deleted) — now asserts `is_frozen` ABSENT from
`_perform_season_merge` and PRESENT in `_stops_push`. Three new
hermetic fixtures added: frozen prime + trunk (`season2/main`, `master`,
`core/main`) is HELD by name and the push is never attempted; frozen prime
+ ordinary post branch (`season2/posts/adv`) still pushes (RUNG 4
unregressed); unfrozen prime + trunk pushes through (the gate is
conditional, not a blanket refusal).

## Evidence

Falsifier (mur-49, unregressed):
  $ sed -n '/^def _make_closeout_seams/,/^def _closeout_run_steps/p' \
      extensions/agi/bin/rotate.py | grep -c is_frozen
  3        # was >=2 before this round; unchanged

Suites (all green, from the worktree root):
  $ python3 -m pytest extensions/agi/tests/test_rotate_closeout_steps.py -q
  41 passed, 21 warnings in 6.96s
  $ python3 -m pytest extensions/agi/tests/test_veto.py \
      extensions/agi/tests/test_write_veto_gate.py -q
  21 passed, 4 warnings in 1.05s
  $ python3 -m pytest extensions/agi/tests/test_rotate.py \
      extensions/agi/tests/test_rotate_prepare.py \
      extensions/agi/tests/test_cli_loop_prune.py \
      extensions/agi/tests/test_branches_v3.py -q
  354 passed, 341 warnings in 76.67s

New fixtures pinning the conditional (verbatim assertions):
- test_frozen_prime_holds_a_trunk_resolved_stops_push: for trunk in
  ("season2/main", "master", "core/main") -> out has "HELD" and "trunk",
  `_pushed(calls) is False`.
- test_frozen_prime_still_pushes_an_ordinary_post_branch:
  resolved "season2/posts/adv" -> out is None and `_pushed(calls)` True.
- test_unfrozen_prime_pushes_a_trunk_resolved_stops_push:
  unfrozen + "season2/main" -> out is None and `_pushed(calls)` True.
All git/subprocess/veto cells faked; no spawn, no network, no real repo.

## Agent Notes
RUNG 5 built: _stops_push consults is_frozen(prime) only when branches.is_remote_visible(branch); pinning test reshaped and 3 hermetic conditional fixtures added; 41+21+354 tests green, mur-49 falsifier still prints 3.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review L4.363 (a00-13e22607): read the kid DIFF (git diff --cached, 2 files, 204 insertions), not its result file. WHAT THE INSTRUCTION SAID: one parent-run negative probe per claim conjunct, recorded in the kid node; a kid that passes its own suite but fails a probe is lean_disproved. WHAT THE MACHINE DOES: rotate.py:15460 now reads `if branches.is_remote_visible(branch):` then `_veto.is_frozen(_shared_graph_root(root), "prime")` inside try/except Exception: pass, returning `push: HELD -- <label> push targets a trunk branch (<branch>) while the prime is frozen`. branches.is_remote_visible (branches.py:316-338) is True for EXACTLY master, season<n>/main, <town>/main, <town>/season<m>/main with towns outside RESERVED=(main,posts,loops), and never raises. Caller at rotate.py:16079 consumes the returned string as `rotate-self refused: ...` and `return 3` (nothing rotated) -- the wire reaches the changed bytes. Falsifier `sed -n "/^def _make_closeout_seams/,/^def _closeout_run_steps/p" rotate.py | grep -c is_frozen` prints 3 (>=2, unregressed). MY PROBES (4, run against the live bytes with fake git + fake veto): (gate) frozen prime on season2/main, core/main, master, core/season2/main, season10/main -> HELD by name, push NEVER attempted; (gate) frozen prime on season2/posts/adv, the live loop branch season2/loops/hypothesis-l4-stops-push-gates-o-a00-13e22607, core/season2/posts/sanctuary-director/main, core/season2/loops/x -> is_remote_visible False, NOT held, push proceeds (RUNG 4 not regressed); (wire) unfrozen prime on season2/main -> push proceeds (the gate is conditional, not blanket). Suites green: test_rotate_closeout_steps.py 41 passed; the -k "rotate or veto or write_veto" selection 811 passed, 1 xfailed. vetoes.md byte-identical (live invariant: no live freeze filed). CAVEAT, recorded not hidden: the kid gated on `branches.is_remote_visible` -- WIDER than the claim literal `season2/main or */main` (it adds master and <town>/season<m>/main). Benign here because no post/loop branch parses as any of those shapes (probed above) and using the ONE grammar beats a second hand-rolled matcher; a deviation from the letter of the claim, in the direction the claim itself points (the grammar own trunk shape).
<!-- THOUGHT:END -->

Parent review L4.363 (a00-13e22607) accepted the kid AI fix and its reshaped pinning test after four parent-run negative probes (5 trunk shapes HELD under a frozen prime with the push never attempted; 4 non-trunk shapes pushed under the SAME frozen prime; unfrozen trunk pushed through; falsifier still 3). The g15 build order is fully implemented in this round: fix and test reshaping landed together as belam required. One deviation recorded in the THOUGHT block: branches.is_remote_visible is wider than the claim literal trunk set and is the grammar ONE matcher, probed benign.

## Agent Notes
Accepted the kid's RUNG 5 build: _stops_push consults is_frozen(prime) only when branches.is_remote_visible(branch), refusing by a HELD line; the pinning test is reshaped and 3 hermetic conditional fixtures added. Four parent-run probes pass (trunk+frozen HELD with no push for 5 shapes; non-trunk+frozen still pushes for 4 shapes; unfrozen trunk pushes; falsifier still 3); 41 + 811 tests green; vetoes.md byte-identical.
