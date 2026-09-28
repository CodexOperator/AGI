---
id: experiment:a00-7808afee-031b26
mint_id: fdbc19c83172463f8df8b725b8554831
type: experiment
parents:
  - hypothesis:unreachable-key-authority-gates-the-swap-missing-ref-skips
next_edges: []
confidence: 0.95
edited_by: a00-0463f965
evidence_runs:
  - experiment:a00-7808afee-031b26
loop: hypothesis:unreachable-key-authority-gates-the-swap-missing-ref-skips@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "probe1c: _publish_row_to_authority on a tmp _fixture with origin set-url to a nonexistent path", "expected": "authority: FAILED", "observed": "authority: FAILED -- fatal: ... does not appear to be a git repository", "result": "pass"}
  - {"conjunct": 1, "class": "wire", "cmd": "probe3b: _finish_pending_swap_on_push(push: OK, authority_line=<the live FAILED line>)", "expected": "refused by name, key byte-identical, pending survives", "observed": "key swap NOT completed -- authority publish did not succeed; key unchanged; pending present", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "probe1a/1b: same fixture, refs/heads/season2/main deleted on a reachable origin", "expected": "authority: SKIPPED and _authority_publish_gates_swap False", "observed": "authority: SKIPPED -- no authority branch ...; gates==False", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "probe2a-c: ls-remote --exit-code rc on present/absent/unreachable origin", "expected": "0 / 2 / not in {0,2}", "observed": "0 / 2 / 128", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "pre-fix copy /tmp/ef73_prefix: pytest test_ef73_unreachable_origin_fails_and_defers_the_swap against the base rotate.py", "expected": "RED", "observed": "1 failed: AssertionError authority: SKIPPED ... .startswith(authority: FAILED)", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "pytest the three named files on the tip", "expected": "all green", "observed": "22 passed, 1 xfailed", "result": "pass"}
production_lines: 10
profile: balanced
role: kid
scaffold_hash: cd62362158b6b2d4
season: 2
title: An unreachable key authority FAILS the publish and defers the swap
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# EF.73 — an unreachable key authority FAILS the publish and gates the swap

Build order under
`hypothesis:unreachable-key-authority-gates-the-swap-missing-ref-skips`.
The fix was IMPLEMENTED, not merely measured.

## What was wrong (pre-fix bytes, verified at file:line)

`rotate.py:_publish_row_to_authority` set `attempted = True` only when
`git fetch origin <branch>` returned 0. A transport failure (network / 403 /
unreachable remote) therefore left `attempted == False`, and the tail returned

    authority: SKIPPED -- no authority branch season2/main (never fetched; ...)

`_authority_publish_gates_swap` gates only `HELD` / `FAILED`; a `SKIPPED` line
lets an authority-deferred successor-key swap COMPLETE — the one case where the
on-disk key can disagree with an authority the code could not read.

## The fix (`rotate.py` `_publish_row_to_authority` ONLY; 10 added / 2 removed)

After the retry loop, when no fetch succeeded, discriminate with a measured,
read-only probe:

    _probe = git -C <top> ls-remote --exit-code origin <branch>
    rc == 2    -> SKIPPED (reachable origin, ref truly absent)      [case a]
    otherwise  -> FAILED  (rc 0 ref exists; rc 128 unreachable)     [case b]

`rc 2` is git's own "ref absent" exit; any other nonzero is a transport
failure. Every other branch (REFUSED / HELD / first-seating / OK / the
attempted-push `FAILED`) is byte-unchanged.

## Red proof (pre-fix bytes, corrected test)

    env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_rotate_key_authority.py -q -k test_ef73
    F test_ef73_unreachable_origin_fails_and_defers_the_swap
    AssertionError: authority: SKIPPED -- no authority branch season2/main
      (never fetched; fatal: '.../gone.git' does not appear to be a git repository ...)
    assert False = "authority: SKIPPED ...".startswith("authority: FAILED")
    1 failed, 11 deselected

Full text: `.agi/sessions/iter-EF.73/a00-7808afee/red.txt`

## Green proof (tip bytes)

    env -u TMUX -u TMUX_PANE python3 -m pytest \
      extensions/agi/tests/test_rotate_key_authority.py \
      extensions/agi/tests/test_rotate_pending_swap_authority.py \
      extensions/agi/tests/test_rotate_alert_two_tree.py -q
    22 passed, 1 xfailed

Full text: `.agi/sessions/iter-EF.73/a00-7808afee/green3.txt`

## Exact discriminator rc measured (probe, not assumed)

| origin state | `ls-remote --exit-code origin season2/main` rc | outcome |
|---|---|---|
| reachable, ref truly absent | 2 | SKIPPED |
| reachable, ref exists but fetch failed | 0 | FAILED |
| unreachable (nonexistent path) | 128 | FAILED |

## Test added (`test_rotate_key_authority.py`)

`test_ef73_unreachable_origin_fails_and_defers_the_swap`:

1. `_publish_row_to_authority` with origin pointed at a nonexistent path
   returns `authority: FAILED`, never `SKIPPED` (the red-on-prefix assertion).
2. A real `_commit_spawn_row(..., rekey=True)` carrying an
   authority-deferred `.key.pending` leaves the key byte-identical and the
   pending file in place.
3. The gate itself, independent of the push leg:
   `_finish_pending_swap_on_push("push: OK", authority_line=FAILED)` refuses
   with "authority publish did not succeed"; a pre-fix `SKIPPED` line falls
   through to the committed-row check instead.

The existing deleted-ref test
`test_ef56_no_authority_branch_skips_and_completes_the_swap` stays green —
case (a) unchanged.

## Deviations / notes

- Test (3) asserts the gate's OWN refusal text, not `_complete_pending_key_swap`'s
  "AUTHORITY leg" text: `_finish_pending_swap_on_push` short-circuits on the
  gating authority line BEFORE reaching that helper. A first draft asserted the
  wrong string and was corrected.
- `production_lines = 10` (`git diff --numstat` over
  `extensions/agi/bin/rotate.py`, tests excluded; the ceiling was 40).

## Falsifiers checked

None observed: the new test is red on the pre-fix bytes, all three named files
are green on the tip, and no file outside FILE SCOPE changed.

## Agent Notes
Unreachable origin now yields authority: FAILED (ls-remote --exit-code rc!=2) and gates the C3 swap; deleted-ref still SKIPPED. Test red on pre-fix, green on tip; the three named files green (22 passed, 1 xfailed). production_lines=10.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-0463f965, EF.73) -- accepted as proved. (1) WHAT THE INSTRUCTION SAID: "run one negative probe per claim conjunct yourself and record them as probes ... a kid that passes its own suite but fails your probe is lean_disproved". (2) WHAT THE MACHINE DOES: _publish_row_to_authority now discriminates a failed fetch with git ls-remote --exit-code origin <branch> (rotate.py:10493-10499): rc 2 gives SKIPPED, any other rc sets attempted so the tail returns FAILED. _authority_publish_gates_swap (rotate.py:17544-17551) gates only HELD/FAILED. I ran six probes, recorded in this node probes: frontmatter: reachable-absent gives SKIPPED and gates==False; unreachable gives FAILED and gates==True; ls-remote rc is 0 present, 2 absent, 128 unreachable; the live FAILED line refuses a push-OK completion and leaves the key byte-identical with the pending file present; and the new test is RED on a pre-fix copy of rotate.py (1 failed) while the three named files are GREEN on the tip (22 passed, 1 xfailed). (3) THE NEAR MISS: a fix that set attempted=True on ANY fetch failure would return FAILED for a reachable origin whose branch was simply deleted -- test_ef56_no_authority_branch_skips_and_completes_the_swap would go red and every swap for a genuinely absent authority would be deferred. The rc-2 discriminator is what separates the two, and probe1a/1b pin it. (4) DEVIATION: none; the review edit is parent-scoped and the kid rotate.py and test bytes are untouched.
<!-- THOUGHT:END -->

Parent a00-0463f965 accepts experiment:a00-7808afee-031b26 as proved: read the 10-line rotate.py diff and the 54-line test against the kid diff, ran six parent negative probes (recorded in probes:), confirmed the new test RED on a pre-fix copy of rotate.py and 22 passed 1 xfailed for the three named files on the tip, no falsifier observed.
