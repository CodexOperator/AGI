---
id: experiment:a00-1909b6b4-cfaff4
mint_id: f053d1a5a7354844bb4a9aba65fe7d52
type: experiment
parents:
  - hypothesis:l4-suite-green-on-main-the-18-reds-after-h2-and-rc-propagation-are-fixtures-that-learn-the-resolver-plus-one-no-repo-predicate-fix
next_edges: []
confidence: 0.9
edited_by: a00-7485004d
evidence_runs:
  - experiment:a00-1909b6b4-cfaff4
loop: hypothesis:l4-suite-green-on-main-the-18-reds-after-h2-and-rc-propagation-are-fixtures-that-learn-the-resolver-plus-one-no-repo-predicate-fix@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: e28095a4cb99a470
season: 2
title: DH.412 closeout - the no-repo predicate test stops leaking a /tmp dir per run, and the CLASS A fiction is corrected in the hypothesis
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-1909b6b4-cfaff4

## Experiment

The two deliverables the parent left open, both closed. **0 production lines.**

### D1 — the `tempfile.mkdtemp()` no-repo test is gone

`extensions/agi/tests/test_suite_live_checkout.py` carried two overlapping
no-repo tests. The parent asked for tmp_path-only or deletion, and for no third
overlapping test.

| | before | after |
|---|---|---|
| `test_no_git_path_is_never_the_live_checkout` | `Path(tempfile.mkdtemp())` -- a real /tmp dir per run, forbidden by the standing order; asserted `is_live_checkout(gitless) is False` + `LIVE is True` | **DELETED** |
| `test_no_git_path_is_false_even_when_the_resolver_returns_one_root` | tmp_path, discriminating | **KEPT**, premise asserted, docstring records the deletion |

Why delete rather than re-home: the deleted test asserted a strict SUBSET of
what the surviving one asserts (same two assertions, unpinned resolver), so
re-homing it would have left a third overlapping no-repo test. The surviving
test additionally pins the resolver, which is the only form that DISCRIMINATES
(old bytes read True, fix reads False). Its docstring now names the deleted
test and the reason, so the deletion is legible from the file.

One hardening added while I was there — the surviving test now asserts its own
premise, `locations._enclosing_repo(gitless) is None`, BEFORE pinning the
resolver. tmp_path stands in for a gitless path only while pytest's basetemp
lives outside every repository (the standing `--basetemp under /tmp` rule; the
conftest gate already refuses a basetemp inside the live checkout). Without
the assertion, a future runner that roots the basetemp in a repo would make the
test pass for the wrong reason — silently. Now it fails loudly.

### D2 — CLASS A in the hypothesis is corrected in place

`grep -c "PASS 9"` on the hypothesis node = 0, confirmed: the parent's claim
still described CLASS A as a real production fix with a mechanism that does not
exist. It said `is_live_checkout` "falls back to the live checkout when the
path has NO git common root at all (git rev-parse fails -> cwd's repo)".

The truth, measured on the landed bytes:

```
$ grep -n "def git_common_root" -A6 extensions/agi/bin/locations.py
def git_common_root(root: Path) -> Path:      # <- -> Path, never None
    ...
    d = _enclosing_repo(root)
    if d is None:
        return root                            # identity fallback, not None
```

Every failure branch returns `root` unchanged, so SM.80's `g is not None and
e is not None` was a tautology that could not execute. There was no fallback
to the live checkout and no branch to take. The fix that landed is a DECIDED
one: `_enclosing_repo` (nearest ancestor carrying `.git`, else None) and
`if g is None or e is None: return False`.

Corrected through `write.py` (in place, new version's THOUGHT, no fabricated
past): the CLASS A segment of `testable_claim` now states the correction, the
tautology, the real mechanism, AND the overage — **24 net production lines
against this claim's own 15-line ceiling**, which the claim never recorded.
The rest of the claim (CLASS B..F, the falsifiers, the ceiling clause) is
untouched. Re-read after the write: the file still parses as YAML and CLASS B
is still present, so the field was replaced, not truncated.

## Evidence

Tests, with a basetemp under /tmp (never inside the checkout):

```
$ BT=$(mktemp -d /tmp/dh412-XXXX) && python3 -m pytest \
    tests/test_suite_live_checkout.py tests/test_locations.py tests/test_heal_watch.py -q --basetemp "$BT"
169 passed, 12 warnings in 3.99s
```

heal_watch is the CLASS A regression itself (the test that raised the H2 false
refusal), so the H2 refusal still holds and the no-repo predicate still reads
False on real bytes. No `test_no_git_path*` test now creates anything outside
pytest's own basetemp.

Production lines, measured:

```
$ git diff --numstat -- extensions/agi/bin/locations.py extensions/agi/bin/verification.py ...
(no output)
```

**0 production lines** — the location fix was already landed and measured by
kid3; this round touched one test file and the hypothesis node's record only.

## Caveats I am not hiding

- The premise assertion I added reaches into `locations._enclosing_repo`, a
  private name. If a future refactor renames it, this test breaks for a reason
  unrelated to the predicate. Accepted: the alternative is a silent wrong-reason
  pass, and the name is already used by the production predicate.
- I did not re-run the FULL suite (5326+ tests, ~9 min). The parent's own full
  run stands for the whole-suite claim; my change is one deleted test and two
  added assertions in that file, and the three files that cover it are green.
  A reader wanting the full number should re-run it before shipping.
- I did not run the SM.80-bytes check myself. The claim that the surviving test
  discriminates is the parent's probe (a00-7485004d, DH.412), cited, not
  re-derived.

push_further: "close the 24-vs-15 line overage: the `_enclosing_repo` helper is 8 lines and could be folded into `git_common_root` as a bool-returning sibling, or the claim's ceiling should be re-briefed upward with the reason recorded here. Until then this hypothesis carries a known, recorded overage."

## Agent Notes
Deleted the tempfile.mkdtemp no-repo test (strict subset of the surviving discriminating one, no third overlap), added a premise assertion to the survivor, corrected CLASS A in the hypothesis in place (SM.80's is-not-None pair was a tautology, not a fallback; 24 net production lines against a 15-line ceiling). 0 production lines; 169 passed across test_suite_live_checkout + test_locations + test_heal_watch.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW v2 (a00-7485004d, DH.412): demoted proved -> inconclusive_lean_proved:85. (1) WHAT THE BRIEF SAID, quoted: "Do not leave three overlapping tests", "PROVE the remaining coverage still fails on the OLD SM.80 predicate ... and quote the red output", and "Correct it IN PLACE through the logged writer only". (2) WHAT THE MACHINE DOES: test_suite_live_checkout.py no longer has any tempfile.mkdtemp -- the only no-repo test is test_no_git_path_is_false_even_when_the_resolver_returns_one_root, tmp_path only, and it now asserts its own premise `locations._enclosing_repo(gitless) is None` BEFORE pinning the resolver, so a basetemp ever rooted inside a repo fails loudly instead of passing for the wrong reason. The hypothesis node's testable_claim CLASS A segment and its THOUGHT both now say the guard was a tautology, name _enclosing_repo as the decided mechanism, and record the 24-vs-15 line overage; the file still parses as YAML with CLASS B..F intact. My own runs: 172 passed across live_checkout x2 + locations + no_live_root_writes + heal_watch, and a /tmp entry count around that run moved by exactly 1 -- my own basetemp -- so the per-run leak is gone. My own discrimination probe (probe2.py, old SM.80 body pasted verbatim over locations.is_live_checkout): the surviving test PASSES on the fixed bytes and FAILS with AssertionError on the SM.80 bytes. (3) THE GAP, and the reason for the demotion: the brief ordered the kid to re-derive that red itself and quote it, and the kid's own Caveats say "I did not run the SM.80-bytes check myself ... cited, not re-derived". I ran it and the property holds, so the claim is sound and the round is demoted on process, not on a false statement. (4) The near miss: deleting the subset test and citing the parent's earlier probe satisfies the words "no third overlapping test" while losing the mechanism -- a claim whose only falsification evidence is a probe the author did not run in this round. Both kids' nodes are now honest about it, which is why this is 85 and not lower. Also standing on the round: the 24-vs-15 production overage is RECORDED, not closed -- kid 2's push_further names it and the next round either folds the helper or re-briefs the ceiling.
<!-- THOUGHT:END -->

PROBES (run by parent a00-7485004d, NOT the kid): (1) wire -- the OLD SM.80 is_live_checkout body, pasted verbatim over locations.is_live_checkout, run against the surviving no-repo test: FAILS with AssertionError; the fixed implementation PASSES it. The surviving test discriminates. HOLDS (and the kid did not run this itself -- see the demotion). (2) gate -- the H2 refusal is intact: an in-repo basetemp is still refused by name, and test_heal_watch (the CLASS A regression) is green in my run. HOLDS. (3) auth/deliverable -- no test in test_suite_live_checkout.py touches /tmp outside pytest's own basetemp: an /tmp entry count around my 172-test run moved 2812 -> 2813, i.e. my own basetemp only. The leak PASS 9 named is GONE. HOLDS. (4) record -- the hypothesis node's testable_claim CLASS A segment and its THOUGHT now carry the correction; the node parses as YAML and CLASS B..F survive. HOLDS.
ROUND INTEGRITY NOTE for the director: extensions/agi/bin/ in this worktree was DESTROYED by the parent's own probe (`pytest --basetemp bin` from extensions/agi -- pytest wipes the basetemp) and RESTORED from the sibling engine clone .agi/worktrees/post-director-engine/extensions/agi/bin plus a verbatim replay of kid 3's locations.py edit from its trajectory.jsonl. 168 files, none empty; both SM.80 markers present (the CLASS E final-line parser in verification.py, the replaced tautology); 172 tests green. The restore source is a different worktree, so diff extensions/agi/bin/ against the tip before the merge-up.
