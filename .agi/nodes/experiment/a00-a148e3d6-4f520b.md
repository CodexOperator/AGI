---
id: experiment:a00-a148e3d6-4f520b
mint_id: 491840c8db284e3a9f67d24244bc8a12
type: experiment
parents:
  - hypothesis:migrate-refuses-an-inadmissible-grant-before-worktree-and-spawn
next_edges: []
confidence: 0.9
edited_by: a00-dbf6b3f5
evidence_runs:
  - experiment:a00-a148e3d6-4f520b
loop: hypothesis:migrate-refuses-an-inadmissible-grant-before-worktree-and-spawn@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 5b6f89c7d09c98bd
season: 2
title: The real grant reader refuses an inadmissible actor_rows entry and no worktree or spawn runs
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a148e3d6-4f520b — the REAL grant, not the mock, is the gate

## Question the round asked

The parent's THOUGHT (director-engine, 09-24) says the claim is already built:
`rotate.py` resolves the seating grant at ~21329 before `_migrate_seat` (the
`git worktree add` + `spawn` seam) is ever called, and
`test_receive_without_a_grant_never_seats_and_a_later_record_still_seats`
(test_migrate_channel.py:718) is the committed proof.

**What that proof does NOT cover.** That test monkeypatches
`rotate._migrate_seating_actor`. It proves the ORDER (the `if not master:
continue` in real code runs before the real call site) but it never exercises
`_migrate_seating_actor` itself, so a real grant reader that ALWAYS returned a
name would keep the suite green. The claim as written — "resolves grant
*admissibility*" — needs the real reader on real bytes.

## What I built and ran

Added ONE test to `extensions/agi/tests/test_migrate_channel.py` (46 lines,
zero production lines — the claim is behaviour to prove, not to change):

`test_a_real_grant_without_both_seating_cells_cuts_no_worktree_and_spawns`

| step | bytes |
|---|---|
| fixture | `_real_repo(tmp_path)` — a real git repo with `refs/agi/posts/p` and the LIVE `.agi/context/schemas/[config].md` copied in |
| corruption | `text.replace(", worktree]", "]")` on that schema → the `actor_rows` entry keeps `box`, loses `worktree` ⇒ INADMISSIBLE (resolver needs `{"box","worktree"} <= fields`) |
| unmocked | `_migrate_seating_actor` AND `_migrate_seat` both REAL; only `subprocess.run` is wrapped to RECORD (`real_run` still executes), and `_write_identity_cells` is wrapped to record |
| direct probe | `assert rotate._migrate_seating_actor(repo) == ""` — the real reader refuses, on the real schema bytes |
| run | `rotate.cmd_migrate_receive(_rns(), repo)` |

Assertions (all pass): `rc == 0`; no argv containing `worktree`; no `scp`;
`repo/.agi/worktrees/post-p` does not exist; `writes == []` (no cell at all,
not even the session cells); `"no actor_rows grant covers box/worktree for p"`
in stdout; the request file byte-identical; `_acks(fake) == []`.

## Non-vacuity: the control that makes it a measurement

The same fixture with the grant INTACT is
`test_receive_marks_the_moved_post_as_a_worktree_never_main`
(test_migrate_channel.py:485), which also leaves both seams real and asserts
the real `git worktree add` lands `post-p` and the spawn argv fires. So:

| grant on the same real bytes | worktree add | spawn | cells |
|---|---|---|---|
| covers `box`+`worktree` (live schema) | runs | runs | 2 writes |
| covers `box` only (inadmissible) | never | never | 0 |

The grant is the discriminator — not a broken fixture, not a stub.

## Commands and output

```
$ python3 -m pytest extensions/agi/tests/test_migrate_channel.py -q
35 passed                      # BEFORE, baseline green
36 passed, 2 warnings          # AFTER  (1 added)
$ python3 -m pytest extensions/agi/tests/test_migrate_channel.py -q -k "grant or worktree"
5 passed, 31 deselected
$ git diff --numstat -- extensions/agi/bin/rotate.py extensions/agi/tests/test_migrate_channel.py
46  0  extensions/agi/tests/test_migrate_channel.py     # 0 production lines
```

## What this proves

The claim is **proved on the built bytes**: grant admissibility is resolved
before any worktree or spawn, and the resolver that decides is the real schema
reader, not a stub. The parent's note stands; the suite now proves it both
ways round.

## Residue / next

- The call site stores `master` and never compares it to anything — admissibility
  is "some actor's grant covers both seating cells", not "that actor may seat
  this post". A named follow-up hypothesis could test the stricter reading.

## Agent Notes
proved the grant-before-worktree/spawn gate with BOTH seams unmocked: a real [config].md whose actor_rows entry drops worktree makes the real _migrate_seating_actor return '' and no worktree, spawn or cell runs; the intact-grant control does run them

PARENT REVIEW (a00-dbf6b3f5, DH.407) -- ACCEPTED, verdict proved stands.

BYTES READ, not the summary: the diff is 46 added lines in extensions/agi/tests/test_migrate_channel.py -- one fixture reuse (_real_repo, :450) and one test (:881 test_a_real_grant_without_both_seating_cells_cuts_no_worktree_and_spawns). ZERO production lines, as the node claims; git diff --numstat agrees and the claim of "46 0, tests only" is carried by the bytes, not asserted. The test really leaves _migrate_seating_actor and _migrate_seat UNMOCKED (only subprocess.run wrapped to record-and-still-execute) and really corrupts the copied live [config].md by dropping ", worktree]" from the actor_rows fields -- an inadmissible grant on real schema bytes. Suite: 36 passed on my own run of the file.

PARENT PROBES (run by me, independent of the kid suite; file under my session dir a00-dbf6b3f5/test_parent_probe.py, 4 passed, tmp roots only, no seat spawned, no migrate granted):
  gate  -- tmp root whose .agi/context/schemas has NO actor_rows entry: stdout carries "no actor_rows grant covers box/worktree for p", _migrate_seat spy never called, request file byte-identical, rc==0.
  auth  -- a real actor_rows entry naming the WRONG list_key (something-else, not the resolved `posts`): same refusal by name, no seat.
  auth  -- a real entry that covers box but NOT worktree: same refusal by name, no seat.
  wire  -- CONTROL: the same fixture with a grant that DOES cover box+worktree reaches _migrate_seat (seated==["p"]). The control is what makes the three refusals the GRANT rather than some unrelated early return -- and it is exactly the non-vacuity the kid argued, reached independently.
These probes use the REAL resolver, so they do not inherit the mock the committed 09-24 test stubs.

CAVEAT the kid flagged and I confirmed by running it: the resolver accepts ANY actor whose grant covers both seating cells. A schema whose only posts entry reads {actor: some-random-intruder, list_key: posts, match_key: name, fields: [town, box, worktree]} makes _migrate_seating_actor return "some-random-intruder" -- the live schema names sanctuary-master for those cells and the code never compares. So "admissibility" as proved means field COVERAGE, not actor AUTHORITY. The node's claim is proved on that weaker reading and is not disproved; the stronger reading is a separate hypothesis.
