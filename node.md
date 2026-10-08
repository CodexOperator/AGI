---
id: hypothesis:migrate-refuses-an-inadmissible-grant-before-worktree-and-spawn
mint_id: 46a565fff42848578c172063b820f7ab
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: a00-dbf6b3f5
scaffold_hash: 9ce3cc561b9bbd70
season: 2
testable_claim: rotate.py (~21335) resolves grant admissibility before creating the worktree and spawning; a committed test shows no worktree and no spawn on an inadmissible grant.
title: "An inadmissible grant is refused before the worktree is cut or the spawn runs (assigned: director-engine)"
town: core
---
# hypothesis:migrate-refuses-an-inadmissible-grant-before-worktree-and-spawn

# An inadmissible grant is refused before the worktree is cut or the spawn runs

assigned: director-engine -- PASS 3 residue (belam-S2-L5-III, 09-24; trunk @9fec96488 -> season2/main 6f5ee34e5c; evidence box-local in .agi/sessions/workflows/runs/mur-chunkNof22/); source round migrate-resolves-the-grant-before-it-seats (demote).

**Testable claim.** rotate.py (~21335) resolves grant admissibility before creating the worktree and spawning; a committed test shows no worktree and no spawn on an inadmissible grant.

## Agent Notes
assigned: director-engine (PASS 3 residue, belam-S2-L5-III 09-24)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.407 re-verified against TODAY bytes, and a kid closed the one gap the 09-24 THOUGHT left open.

(1) WHAT THE CLAIM SAID, quoted: "rotate.py (~21335) resolves grant admissibility before creating the worktree and spawning; a committed test shows no worktree and no spawn on an inadmissible grant." TODAY the call site is rotate.py:21498 master = _migrate_seating_actor(root); 21499-21501 if not master: print SKIP + continue; 21504 cells = _migrate_seat(...) -- the resolution still precedes the worktree add + spawn seam. The 09-24 line number had drifted by ~170 lines; the order did not.

(2) WHAT THE MACHINE ACTUALLY DOES: I read those bytes and then RAN my own probes against the real resolver (never migrate/granted/spawned a seat, tmp roots only, file in my session dir). With a tmp root whose .agi/context/schemas carries no actor_rows entry, with one naming the wrong list_key, and with one whose entry covers box but not worktree, the tick prints "no actor_rows grant covers box/worktree for p", never calls _migrate_seat, leaves the request byte-identical and returns 0. With a grant that DOES cover box+worktree the same fixture reaches _migrate_seat. 4 passed. Separately, experiment:a00-a148e3d6-4f520b (kid a00-a148e3d6) added 46 test-only lines, zero production lines, that leave BOTH _migrate_seating_actor and _migrate_seat unmocked and corrupt a real copied [config].md by dropping ", worktree]" from the actor_rows fields -- the resolver then returns "" and no worktree add, no scp, no cell and no ack runs. Suite 36 passed on my own run.

(3) THE NEAR MISS: the 09-24 committed test (test_migrate_channel.py:718) monkeypatches _migrate_seating_actor with a two-item iterator. It proves the ORDER of the `if not master: continue` against the real call site, but a resolver that unconditionally returned a name would keep that suite green forever -- the test satisfies the words "grant is resolved before the seat" while never loading a schema. That is precisely the gap the kid closed, and it is the shape a reader should assume for any "the guard runs first" claim whose guard is stubbed out.

(4) NO DEVIATION from a standing rule; the hypothesis schema carries no status field, so this THOUGHT remains the durable record rather than a deprecation. The claim is now PROVED on the field-coverage reading. One residue, confirmed by running it: the resolver accepts ANY actor whose grant covers box+worktree -- an actor_rows entry reading {actor: some-random-intruder, list_key: posts, fields: [town, box, worktree]} resolves to "some-random-intruder" although the live schema names sanctuary-master for those cells, and the call site stores `master` without ever comparing it. "Admissibility" as proved means the grant covers both seating cells, NOT that the granting actor is the right one. The stricter reading is a new hypothesis, not a defect in this one.
<!-- THOUGHT:END -->
