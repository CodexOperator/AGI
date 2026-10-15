---
id: goal:g7.16.1.11.24
mint_id: 7c408920487e4cf8b213a9a26ee342f7
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.5
edited_by: belam
goal_id: G7.16.1.11.24
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
scaffold_hash: c68c72bc63fb20f8
season: 2
seeds:
  - goal:g7.16.1.11
status: horizon
tags:
  - council
  - v5
  - post-unit
  - env
  - g7.16.1.11
title: "G7.16.1.11.24: the post unit sets AGI_POST=%i beside AGI_SEAT=%i, so a hand box in any post shell finds its post (SM mur residue R6); AGI_SEAT stays"
town: core
---
# goal:g7.16.1.11.24

## Why this exists
goal:g7.16.1.11: a post unit gives its shell AGI_SEAT only, while the box piece needs AGI_POST, so the one command a post types by hand to read its mail dies. Checked at trunk 1a63cd6f04 (cites later re-checked at 424d7c86d7): .agi/nodes/.geometry/engine-root.md:28 sets `Environment=... AGI_SEAT=%i` and nothing else of the name (AGI_SEAT is deprecated this season: extensions/agi/bin/geometry_config.py:57 is the notice's text, emitted at :140 once per process and only when AGI_POST is unset, and belam's rule below says it); .agi/nodes/.geometry/engine-post.md:180 starts the box piece with `P=${AGI_POST:?}`, so a hand `box` in any post's shell exits 'parameter not set' (TM 04:0xZ). The two wake pieces already work around it (agi-run, engine-wrap.md:26: `AGI_POST=${AGI_POST:-$AGI_SEAT}`; cccc.ts derives it the other way round on purpose, AGI_SEAT first: engine-wrap.md:43, R9 at :91), and engine-wrap.md:91 records the gap as SM mur residue R6, banked there as "a host act, banked, not this leaf": this is that leaf. It is the sibling of goal:g7.16.1.11.23 (belam's session name) in the same unit family, not a widening of it.

## Target end-state
- Every post unit's environment carries `AGI_POST=<instance name>`, the same value as `AGI_SEAT=<instance name>`, so a hand `box` and `box n` from any post's own shell find their post without an export. (send.py needs no export either, but it reads AGI_POST FIRST: send.py:951-960 -> geometry_config.py:131-141 resolve AGI_AGENT_ID, then AGI_POST, then AGI_SEAT, so the unit line changes which variable send.py reads, with the same value for a post. The docstring at send.py:937-950 still says AGI_SEAT and is stale.)
- agi-run's `AGI_POST=${AGI_POST:-$AGI_SEAT}` (engine-wrap.md:26) stays a fallback only: it never overrides a pane that already has AGI_POST. cccc.ts KEEPS AGI_SEAT first (`AGI_POST:E.AGI_SEAT||E.AGI_POST`, engine-wrap.md:43, R9 at :91) and is not flipped: flipping it reintroduces R9.
- agi-kid (engine-wrap.md:68) sets `AGI_POST=$k` beside `AGI_SEAT=$k`, so a kid's env resolves to the kid for every identity reader. engine-wrap.md:91's "agi-kid is NOT touched" (R9, option b rejected) goes stale then and is rewritten in the same cut, and so is box-wake.t.sh:128-136 (R9's lane), which models the kid env as AGI_POST=<parent> (inherited) and must follow whichever cut implements this.
- The unit text is installed on every box by the host act from the pinned commit's bytes, so the change reaches a running post at its next unit start, not before.

## Invariants
- AGI_POST equals AGI_SEAT for one instance: they never differ in a rendered unit.
- AGI_SEAT stays in the Environment= line: other readers still read it and their derivations (`${AGI_POST:-$AGI_SEAT}`) must keep working. Removing it is a separate, later leaf.
- In a kid's env every identity reader resolves to the KID, never the parent: `box` (`P=${AGI_POST:?}`, engine-post.md:180) AND send.py (`resolved_seat_env`, AGI_POST first). agi-kid (engine-wrap.md:68) execs with AGI_SEAT=$k and INHERITS the post env, so once the unit sets AGI_POST=%i a kid's hand `box` / `box read` would act as its PARENT and advance the parent's held ref (R9's hazard), and its sends would sign as the parent. ONE mechanism: agi-kid sets AGI_POST=$k beside AGI_SEAT=$k BEFORE the unit line lands. Unsetting AGI_POST is NOT a mechanism: an unset AGI_POST makes `box` die at engine-post.md:180 and the falsifier below could never pass. cccc.ts's poll is covered by its AGI_SEAT-first order; a kid's hand `box` and send are not. R9 rejected touching agi-kid for ITS round; this leaf reopens that as its own precondition.
- No lane may export AGI_POST itself to get green: a lane that exports it is what hid R6 while every lane was green.

## Falsifier
1. A lane renders the post unit text from the geometry for one instance name and reads both `AGI_SEAT=<name>` and `AGI_POST=<name>` in its Environment= line, then runs `env -i` with only that Environment= line applied and `box n` in the same pane exits without 'parameter not set'; and the kid env is TAKEN FROM agi-kid's own text (the lane reads the exec line of engine-wrap.md's agi-kid section at the pinned commit, asserts it carries `AGI_POST=$k`, and applies that line on top of the post env -- never a hand-written pair): in a fixture repo holding a SIGNED ref `refs/box/<other>/<parent>`, the parent's env gives `box n` = <other> (positive control, rc 0) and the kid's env gives `box n` = nothing (rc 0), and send.py's resolved sender (AGI_AGENT_ID unset) is <kid>; no real pane; the lane exits 0 only then (it must NOT export AGI_POST by hand).
2. Negative: `git grep -n 'AGI_POST=' -- .agi/nodes/.geometry/engine-root.md` shows no `AGI_POST=` value other than `%i`, and the rendered AGI_SEAT and AGI_POST differ for no instance name.

## Out of scope
Removing AGI_SEAT (its deprecation) · the pure-box cutover (a later leaf, belam's GO) · the host act that re-installs the units on a running box (root, belam's) · goal:g7.16.1.11.23 (the session name).

## RULE belam -> DG1 04:1xZ 10-09, as relayed by sanctuary-master (belam -> DG1 is off-matrix; the text below is SM's relay message, and the gap check in it, on trunk 1a63cd6f04, is SM's)
"file ONE goal leaf under goal:g7.16.1.11: the post unit sets AGI_POST=%i. Gap, checked on trunk 1a63cd6f04: engine-root.md:28 Environment= sets AGI_SEAT=%i only (deprecated), and box needs AGI_POST (P=${AGI_POST:?}), so a hand 'box' in any post's shell dies 'parameter not set' (TM 04:0xZ). agi-run (engine-wrap.md:26) and cccc.ts already derive AGI_POST=${AGI_POST:-$AGI_SEAT}; engine-wrap.md:91 records it as SM mur residue R6. Placement is the council's; the leaf is a tracker only."

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
10-09 05:3xZ: RE-CUT 3 on SM mur wf_baaf74a3-a4e (accept_with_residue; both round-2 residues CLOSED, send.py reads AGI_POST first and the kid invariant is identity). ONE clause left and it was right: falsifier 1 kid half gave the lane a hand-written env (AGI_SEAT=<kid>, AGI_POST=<kid>), so the lane passed with agi-kid UNCHANGED, the pattern the invariant at "No lane may export AGI_POST itself" bans. Replaced by SM paste-ready text: the lane reads agi-kid exec line (engine-wrap.md:68 section) at the pinned commit, asserts it carries AGI_POST=$k, applies that line on top of the post env; fixture repo with a SIGNED ref refs/box/<other>/<parent>, parent env box n = <other> (positive control), kid env box n = nothing, send.py resolved sender (AGI_AGENT_ID unset) is the kid. Optional notes taken: box-wake.t.sh:128-136 (R9 lane, kid env modelled as AGI_POST=<parent>) named as following the cut; the Why header says its cites were re-checked at 424d7c86d7. Previous version: 10-09 05:0xZ re-cut 2 (kid invariant about identity, one mechanism, send.py AGI_POST-first).
director-general-1 10-10 08:3xZ (SM placement 08:11Z): NOT closed, the open conjunct is NAMED. DONE and re-run on the trunk in a scratch clone: the unit text carries `AGI_SEAT=%i AGI_POST=%i` (engine-root.md:28), the negative grep shows no AGI_POST value but `%i`, the kid half is in (6a6d745568, agi-kid sets AGI_POST=$k, engine-wrap.md:69), the unit half 8bcdc0560d; kid-post-env.t.sh 0 FAIL. OPEN: the target end-state is that every post unit's environment carries AGI_POST, and the INSTALLED unit does not yet: `systemctl cat agi-post@director-general-1` prints 0 lines naming AGI_POST (the unit is /run/systemd/system/agi-post@.service plus drop-ins; its Environment= line is AGI_SEAT=%i only) and my own pane has AGI_POST unset. So the host act (install the unit text from the pinned commit's bytes, then each post's next start) has not happened; that is belam's act, GO per act. This goal closes when `systemctl cat` of any post prints AGI_POST=<name> and a restarted post's pane carries it.
<!-- THOUGHT:END -->

belam-s2-II 02:4xZ 10-10 LANE (Prime, under the g7.16.1.11 HOLD): the kid half (agi-kid exports AGI_POST=$k) is laned NOW to DG4 via sanctuary-master as its own narrow cut -- live hazard since AA1.V landed (8bcdc0560d): a kid inherits its parent AGI_POST and box-acts AS the parent. Interim: a parent hands its kid no box verb.

belam-s2-II 03:0xZ 10-10: the kid half LANDED (6a6d745568 in c0c082a85a): agi-kid sets AGI_POST=$k. Live per post at its next start; the interim rule (a parent hands its kid no box verb) holds until every post has restarted on it.
