---
id: experiment:a00-e9f727c6-d2eba4
mint_id: b01bf5dd823e48be9493a4ac437b13b2
type: experiment
parents:
  - hypothesis:l4-delete-old-lease-guards-the-toctou-window-between-gate-and-delete
next_edges: []
confidence: 0.9
edited_by: a00-9438b47d
evidence_runs:
  - experiment:a00-e9f727c6-d2eba4
loop: hypothesis:l4-delete-old-lease-guards-the-toctou-window-between-gate-and-delete@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "PATH git-shim that force-pushes a racer commit onto origin/seat/post-a@s2 BETWEEN the CLI fresh ls-remote probe and its delete push (parent probe, independent of the kid pre-push-hook seam)", "expected": "delete REFUSES: rc != 0, branch named in stderr, remote ref PRESERVED at the racer sha", "observed": "RC 1; stderr: stale info rejection + ERR: --delete-old: 1 remote delete(s) refused: seat/post-a@s2; ls-remote ref = a3f38963... == racer sha. Pre-fix counterfactual (same shim vs lease-reverted cli.py copy): RC 0, raced ref DELETED", "result": "holds"}
  - {"conjunct": 1, "class": "wire", "cmd": "python3 -m CLI branch-reshuffle --delete-old on fixture repo, no concurrent writer", "expected": "rc 0, all 4 legacy remote branches deleted, live push argv carries --force-with-lease=refs/heads/season/s2:<40hex> --delete season/s2", "observed": "rc 0; lease line byte-equal in stdout; season/s2, seat/post-a@s2, town/core/season/s2, loop/x@s2 all gone from origin", "result": "holds"}
  - {"conjunct": 1, "class": "gate", "cmd": "fixture with origin set-url /nonexistent/origin.git, then CLI branch-reshuffle --delete-old", "expected": "refused by name, no --force-with-lease printed (never leases an unread sha)", "observed": "ERR: --delete-old REFUSED: origin unreachable; 7 candidates named; no --force-with-lease in stdout; rc != 0", "result": "holds"}
profile: balanced
role: kid
scaffold_hash: fe82af7a576da669
season: 2
title: A00 e9f727c6 d2eba4
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e9f727c6-d2eba4

## Experiment

BUILD round (g15 claim = behaviour to build, not to measure).
`branch-reshuffle --delete-old`'s per-job real delete carried NO sha
binding: it probed existence, then ran `git push origin --delete <old>`
unconditionally. Between the top-of-pass gates (B2 presence + containment)
and a job's own delete, origin/<old> could move; the delete would destroy
the moved content. I implemented the lease guard and proved it closes the
window.

### What changed (payload)

`extensions/agi/bin/cli.py`:

1. NEW helper `_post_rename_remote_ref_state_sha(repo, ref) -> (state, sha)`
   placed beside `_post_rename_remote_ref_state` (cli.py ~2602). Same
   rc-honesty contract as the existing state probe, but it also returns the
   tip sha: `('present', <sha>)` rc 0 + non-empty stdout, `('absent', '')`
   rc 0 + empty stdout, `('failed', '')` rc != 0. A failed/absent probe
   NEVER yields a sha, so no lease can ever be built on an unread value.
2. The `--delete-old` job loop (cli.py ~4475): the dry leg still prints the
   unchanged `[DRY ] ... git push origin --delete <old>` preview. The real
   leg now reads `(state, sha)` from the NEW helper; `failed` refuses by name
   and continues (unchanged rc-honest shape), `absent` keeps the
   `skip: ... already absent (resumed run)` line and continues, and only a
   non-empty sha reaches
   `git push origin --force-with-lease=refs/heads/<old>:<sha> --delete <old>`.
   The printed `[APPLY]` line is the REAL argv, byte-equal to what is run.
   A non-zero push rc (git's `stale info` rejection) names the branch, notes
   the content was PRESERVED, appends to `refused`, and CONTINUES — the
   existing per-job refusal shape. All-or-nothing walls (top-of-pass gates)
   untouched, as scoped.

No other file touched. `_rs_ls_remote_sha` (rc-BLIND: '' for absent AND
failed) was NOT reused for the delete leg — that blindness is why the leg
already used `_post_rename_remote_ref_state`; the new helper keeps the same
rc-honesty and adds the sha.

### Scope honoured

`_rs_containment_state` / `_rs_containment_targets` / the gates untouched;
`post-rename --delete-old` (~2952) untouched; the `--apply` callers of
`_rs_ls_remote_sha` untouched.

## Evidence

### The race window, proven discriminating

The seam is a PATH shim for `git`: when argv contains
`--delete seat/post-a@s2`, the shim first force-pushes a NEW commit onto
origin/<old> (a real concurrent writer) and then execs real git. That move
lands AFTER the CLI's fresh `ls-remote` probe and BEFORE the delete push
even advertises refs — the exact TOCTOU window. (A pre-push hook fires too
late: git has already captured the advertised value, so even an unguarded
delete rejects; the shim is the seam that actually exercises the claim.)

Run against the pre-fix bytes (same cli.py with only the lease argv/print
reverted to the bare `--delete`), the shim race DELETES the moved commit:

    PREFIX RC 0
    PREFIX REMOTE PRESERVED? False  (None)

Run against the built bytes:

    RC 1
    PRESERVED? True 9122264c... RACED 9122264c...
    ERR: git push origin --delete seat/post-a@s2 failed (a 'stale info'
    rejection means origin/seat/post-a@s2 moved after the fresh lease probe;
    content PRESERVED): ... ! [rejected] (delete) -> seat/post-a@s2
    (stale info)
    ERR: --delete-old: 1 remote delete(s) refused: seat/post-a@s2

The moved ref survives with the concurrent writer's sha; the lease sha in
the printed line is the pre-move probe value, so the two differ.

### Tests added (fixture repo only, no real branch deleted)

`extensions/agi/tests/test_branch_reshuffle.py`:

- (A) `test_delete_old_lease_refuses_when_origin_moves_between_probe_and_push`
  — the shim race above; asserts rc != 0, branch named, remote sha == the
  raced sha (ref PRESERVED), and lease sha != raced sha.
- (B) `test_delete_old_lease_delete_succeeds_without_a_race` — no writer:
  rc 0, all four legacy branches gone from origin, APPLY line carries
  `--force-with-lease=refs/heads/season/s2:<40-hex> --delete season/s2`.
- (C) `test_delete_old_lease_probe_is_rc_honest_and_never_a_garbage_sha` —
  unit-level against the new helper: `('present', 40-hex)`, `('absent', '')`,
  `('failed', '')` under an unreachable origin.
- Extended `test_delete_old_ls_remote_failure_is_rc_honest` with
  `assert "--force-with-lease" not in res.stdout` (a failed probe never
  becomes a lease).
- Updated `test_delete_old_orders_posts_towns_mains_and_keeps_master`'s
  ordering needle from `origin --delete <old>` to `--delete <old>` because
  the APPLY line is now the real lease-guarded argv (same ordering intent).

### Suite

    python3 -m pytest extensions/agi/tests/test_branch_reshuffle.py \
      extensions/agi/tests/test_branch_reshuffle_v3.py -q
    ... 85 passed in 58.17s

### Chosen refusal shape (justified)

Per-job, non-fatal, non-zero at the end: the lease rejection is one branch's
problem, not the pass's. The all-or-nothing walls are the top-of-pass gates
(B2 presence and containment), which this round does NOT change. A single
stale lease therefore refuses only that job and the run continues, exactly
like today's failed-push refusal — proven by the new race test where the
other jobs still delete.

## Agent Notes
BUILT the lease guard: --delete-old now probes (state,sha) rc-honestly and deletes via git push origin --force-with-lease=refs/heads/<old>:<sha> --delete <old>. Race test (PATH-shim concurrent writer between probe and push) preserves the moved ref and refuses non-zero; pre-fix bytes delete it. No-race deletes unchanged; failed probe never yields a sha. 85 tests green in both branch-reshuffle suites.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-9438b47d, L4.364). (1) INSTRUCTION: the target hypothesis says the real delete call site carries no sha lease and "a fresh probe-then-force-with-lease immediately before the mutating push closes the TOCTOU window"; FILE SCOPE is the one delete call site in branch-reshuffle --delete-old, not post-rename ~2952; PROOF is a fixture where origin moves between the gates and the delete, refusing non-zero and preserving content, with the no-race case unchanged. (2) MACHINE: read the staged diff, not the kid report. cli.py gains _post_rename_remote_ref_state_sha (rc-honest (state,sha): present/absent/failed, sha only on present) and the non-dry delete leg now runs subprocess.run(["git","push","origin","--force-with-lease=refs/heads/<old>:<sha>","--delete",old]) at cli.py:4524-4529, argv byte-equal to the printed [APPLY] line, with the dry leg unchanged and the post-rename delete at 2952 untouched. I ran MY OWN probes, not the kid suite: a PATH git-shim that moves origin/seat/post-a@s2 between the CLI fresh probe and its push -> rc 1, stale-info rejection, ref preserved at the racer sha; the SAME shim against a lease-reverted copy of cli.py -> rc 0 and the raced commit DELETED, so the probe discriminates pre-fix from built. No-race gives rc 0 with the lease in the live argv and all four legacy branches gone; unreachable origin refuses by name with no lease printed. Recorded in probes:. (3) NEAR MISS: a build that prints the lease in the [APPLY] line but keeps the bare --delete in argv, or that reuses rc-blind _rs_ls_remote_sha and leases a "" sha when ls-remote fails, satisfies the wording of the claim and loses the mechanism; this build avoids both (argv is the real one; a failed/absent probe never yields a sha). (4) DEVIATION: none; the refusal shape chosen (per-job, non-fatal, non-zero at the end) is the existing per-job shape and is justified, since the all-or-nothing walls ARE the top-of-pass gates this round deliberately does not change.
<!-- THOUGHT:END -->

PARENT VERDICT: proved kept. Build order met at the one call site; lease is real in argv (wire probe), refuses the moved ref while preserving it (gate probe, pre-fix deletes it), and never leases an unread sha (rc-honesty probe). Caveat #1: the --dry-run preview still prints the lease-less `git push origin --delete <old>` while APPLY prints the lease, so the preview no longer byte-matches what a real run would do -- out of the claim scope but a real fidelity gap. Caveat #2: race test (A) hardcodes /usr/bin/git in its shim; portable on this tree only. Caveat #3: only the legacy post path is raced; a v3 --kinds loop direct-delete job is not.
