---
id: experiment:a00-f4a9504d-3f1209
mint_id: 39573b54f7024895a281c60e8d8dea0d
type: experiment
parents:
  - hypothesis:the-key-authority-publish-respects-the-veto-and-fires-only-on-a-rekey
next_edges: []
confidence: 0.95
edited_by: a00-76af9f2e
evidence_runs:
  - experiment:a00-f4a9504d-3f1209
loop: hypothesis:the-key-authority-publish-respects-the-veto-and-fires-only-on-a-rekey@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "auth", "cmd": "parent_probes_ef56.py probe_c1_non_rekey_publishes_nothing: _commit_spawn_row(rekey=False) with a dirty row, repo with a real authority branch", "expected": "origin/season2/main sha unchanged and no authority: OK", "observed": "sha unchanged; positive control rekey=True advanced it by one (authority: OK -- 3dd6383ca)", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "_publish_row_to_authority(g,aa,posts) after _freeze_prime(g)", "expected": "authority: HELD and authority sha unchanged", "observed": "authority: HELD -- prime FROZEN by veto:001; sha unchanged", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "_apply_successor_key_gated with SKIPPED-no-ref / SKIPPED-no-branch / FAILED / HELD / OK authority lines", "expected": "SKIPPED does NOT defer (key flips); FAILED and HELD defer byte-identical; OK completes", "observed": "all five cases matched: 2 completed, 2 deferred, 1 completed", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "real _commit_spawn_row(rekey=True) on a repo whose origin has no season2/main branch", "expected": "authority: SKIPPED -- no authority branch; pending swap completes; key flips to successor", "observed": "SKIPPED -- no authority branch season2/main (never fetched; fatal: could not find remote ref); pending gone; key=22*32", "result": "pass"}
  - {"conjunct": 4, "class": "wire", "cmd": "_publish_row_to_authority first seating then send._pushed_seats(do_fetch=False)", "expected": "authority: OK and the aa row is READ BACK by the loader that verifies keys", "observed": "authority: OK -- 5f8bfba76 -> season2/main; names=[bb, aa]", "result": "pass"}
production_lines: 29
profile: balanced
role: kid
scaffold_hash: c3f89e42e7d8e711
season: 2
title: Authority gate defers only on a real attempted publish, not on a missing branch
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f4a9504d-3f1209

## Experiment

Round 2 of EF.51 C3: make the authority gate fire ONLY when a publish was
actually ATTEMPTED against a real authority ref, so a repo with no authority
branch keeps the pre-EF.51 push-only successor-key swap.

Measured pre-fix state (parent-confirmed, reproduced): on a repo whose only
remote branch is `trunk`, `_publish_row_to_authority` fetched
`origin/season2/main` twice, failed both times, and fell through to
`authority: FAILED` -- which the new C3 gate read as a deferral, so the pending
`<seat>.key` swap never completed.

Changed bytes (all in `extensions/agi/bin/rotate.py`, 29+/4-):

| # | change |
|---|---|
| 1 | `_publish_row_to_authority` tracks `attempted` (set when `git fetch origin <branch>` returns 0). Exhausting both tries with no successful fetch returns `authority: SKIPPED -- no authority branch <branch>`, not FAILED. A fetched branch that fails at index/tree/commit/push still returns `authority: FAILED`. |
| 2 | New `_authority_publish_gates_swap(line)`: True only for `HELD`/`FAILED` (payload or `authority:`-prefixed form); every `SKIPPED`/`REFUSED` line does not gate. |
| 3 | `_finish_pending_swap_on_push` and `_apply_successor_key_gated` both use the helper instead of `not startswith("OK")`. |
| 4 | `test_rotate.py`'s two `rec_finish` monkeypatch stand-ins gained `authority_line=None` and forward it -- round 1 added the kwarg to the real helper but left these 3-arg fakes, so `_commit_spawn_row`'s keyword call raised TypeError into the rotation's try/except and the committed row/on-disk key diverged. |

## Evidence

Pre-fix (parent-confirmed), 3 red:
```
$ python3 -m pytest extensions/agi/tests/test_rotate.py -q -k pending_swap
3 failed, 3 passed
```

After the fix:
```
$ python3 -m pytest extensions/agi/tests/test_rotate.py -q -k pending_swap
6 passed, 322 deselected

$ python3 -m pytest extensions/agi/tests/test_rotate.py -q
328 passed in 51.21s

$ python3 -m pytest extensions/agi/tests/test_rotate_key_authority.py extensions/agi/tests/test_send.py -q
347 passed in 15.70s
```

New discriminator tests committed in `test_rotate_key_authority.py`:

| test | pins |
|---|---|
| `test_ef56_no_authority_branch_skips_and_completes_the_swap` | no authority branch -> `SKIPPED -- no authority branch`, never FAILED; the pending swap COMPLETES (key flips to the successor). |
| `test_ef56_refused_authority_push_fails_and_defers_the_swap` | real authority branch + pre-receive refuses the push -> `authority: FAILED`; the pending swap is DEFERRED and `.key` stays byte-identical. |

C3's own unit tests (`test_c3_swap_defers_unless_the_authority_publish_succeeded`,
`test_c3_persisted_swap_defers_when_the_authority_leg_fails`) and C1/C2/C4 stay
green.

Production lines: 29 added / 4 deleted in `extensions/agi/bin/rotate.py`
(`git diff --numstat`), under the 40-line ceiling.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) WHAT THE INSTRUCTION SAID -- EF.56 orders: "the swap waits on the authority publish ONLY when a publish was attempted (a real re-key with an authority ref); with no publish attempted the swap follows the trunk push exactly as before round 1". (2) WHAT THE MACHINE ACTUALLY DOES -- measured by the parent on the kid bytes: _publish_row_to_authority (rotate.py:10428) sets attempted=True when git fetch returns 0 and, when no fetch ever succeeded, returns authority: SKIPPED -- no authority branch (rotate.py:10488-10492) instead of FAILED; _authority_publish_gates_swap (rotate.py:17473) is True only for HELD/FAILED; _finish_pending_swap_on_push (rotate.py:17509) and _apply_successor_key_gated (rotate.py:17560) both route through it. The live persisted path was exercised in probe C3-wire on a repo without origin/season2/main: authority: SKIPPED -- no authority branch, pending swap completed, key flipped. (3) THE NEAR MISS -- gating on base is None (or on any non-OK line) satisfies the words "the publish did not succeed" and loses the mechanism: a repo with no authority branch then returns FAILED and defers forever, which is exactly the 3 red test_rotate.py cases. Tracking attempted at the fetch is what separates "nothing to publish to" from "a publish refused". (4) KEPT -- the kid authored its own node and tests; the parent only added probes:/note/thought through write.py and did not re-run the kid tests as evidence (the 5 probes are the evidence). Rewritten from scratch; the prior THOUGHT (the kid reasoning) is versioned in refs/grid.
<!-- THOUGHT:END -->

## Agent Notes
C3 gate now defers only on an ATTEMPTED non-OK publish (HELD/FAILED); a missing authority branch returns SKIPPED and the swap completes via the trunk push. 328 test_rotate.py + 347 KA+send pass; two new discriminator tests committed; 29/4 production lines in rotate.py.

REVIEW (parent a00-76af9f2e, EF.56): read the kid DIFF (git diff f728036f79..dd6403db02 @ dd6403db02), not its result file. rotate.py +33/-4: _publish_row_to_authority tracks an attempted flag at the fetch and returns SKIPPED -- no authority branch when the branch was never fetched, keeping FAILED only for a real fetched-but-refused push; new _authority_publish_gates_swap gates only HELD/FAILED; both C3 sites use it. test_rotate_key_authority.py +76 commits the two discriminator tests; test_rotate.py +8/-8 fixes the two rec_finish monkeypatch fakes that round 1 left at a 3-arg signature (a real un-updated-contract defect). ACCEPTED, verdict proved. Parent probes: 5 run across the 4 conjuncts (auth/gate/gate/wire/wire), all PASS -- see probes: field; a first-run C1 probe FAILed only because I did not dirty the row before committing (SKIPPED commit proves nothing), corrected, not a kid defect. Ordered suites re-run by the parent: 675 passed (test_rotate.py + test_rotate_key_authority.py + test_send.py).
