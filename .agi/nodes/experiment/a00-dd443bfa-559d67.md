---
id: experiment:a00-dd443bfa-559d67
mint_id: f50a5e0543224b25b11fd2968c227aa8
type: experiment
parents:
  - hypothesis:pb3-agi-post-stream-registered-and-current
next_edges: []
confidence: 0.85
edited_by: a00-06814999
evidence_runs:
  - experiment:a00-dd443bfa-559d67
loop: hypothesis:pb3-agi-post-stream-registered-and-current@s2
model: stealth/space-bunny-alpha
production_lines: 62
profile: balanced
role: kid
scaffold_hash: 6dac41798d6baa61
season: 2
title: agi-post and agi-stream build nodes minted; the rotations.md clause half is blocked by the config write guard
town: core
verdict: proved
---
# experiment:a00-dd443bfa-559d67

## What I built (half the claim landed)

| step | command | result |
|---|---|---|
| pre-fix suite | `pytest extensions/agi/tests/test_skills_first_turn_entry.py -q` | RED: `director: the skills entry omits ['agi-post', 'agi-stream']` (1 failed, 3 passed) |
| build node 1 | `write.py create build skills-agi-post-SKILL.md --parent goal:g1.31.2 --parent idea:engine-skill-doc --payload skills/agi-post/SKILL.md --set payload_ref=... --set build_kind=prose --set link_ref=... --set location=source_root` | created `.agi/nodes/build/skills-agi-post-SKILL.md.md` |
| build node 2 | same for `skills-agi-stream-SKILL.md` -> `skills/agi-stream/SKILL.md` | created `.agi/nodes/build/skills-agi-stream-SKILL.md.md` |
| rotation edit | `write.py config:rotations "sub! ; ...agi-SKILL.md 'read payload 2:12' => ; ...agi-post... ; ...agi-stream... ; ...agi-SKILL.md 'read payload 2:12'"` | **REFUSED** (below) |

Both build nodes resolve via `node_writer.find_node_file` and their `read payload 2:7`
clauses run rc 0, so only the `rotations.md` half is outstanding.

## The blocker (a write-guard refusal, not a defect in the claim)

```
$ python3 extensions/agi/bin/write.py config:rotations "sub! ...agi-SKILL.md 'read payload 2:12' => ..." --dry-run
  RING-GATE PREVIEW: config nodes (config:rotations) may be hand-edited only by admitted roles
  owner, prime_director; resolution for actor '' gave kid, which is not admitted. (goal:g12)
$ ... (same line, applied)
ERR: config nodes (config:rotations) may be hand-edited only by admitted roles owner,
prime_director; resolution for actor '' gave kid, which is not admitted. (goal:g12)
```

`.agi/context/schemas/[config].md` carries `written_by: [owner, prime_director]`; the
`actor_rows` grant covers `templates` for `master-sensei` only (`deny_roles: [prime_director]`,
and a kid is in neither). `write.py::_enforce_written_by` documents that a satisfied rung-2
ring quorum does NOT admit an unadmitted role ("refusal here is the written_by line, never
the ring line"), so `--ring-sig` is not a route either. The dry-run diff was correct and
matched exactly 2 occurrences; the ONLY reason nothing landed is the role gate.

## The edit a prime/owner seat must apply (measured, byte-exact)

Two clauses, both `skills` first_turn entries, `--dry-run` showed 2 matches:
`python3 extensions/agi/bin/write.py build:skills-agi-post-SKILL.md 'read payload 2:7'; `
`python3 extensions/agi/bin/write.py build:skills-agi-stream-SKILL.md 'read payload 2:7'; `
inserted before the final `build:skills-agi-SKILL.md 'read payload 2:12'` clause.

## Measured bytes (the cap MUST move, 6000 -> 7000)

| quantity | bytes | how |
|---|---|---|
| director entry today, stdout+stderr | 5259 | `/bin/sh -c "$cmd" \| wc -c` (stderr 0) |
| the two new clauses alone | 908 | the two-clause `/bin/sh -c` run |
| projected total with both clauses | **6167** | 5259 + 908 -> **over the 6000 cap** |

So `byte_cap: 6000 -> 7000` in BOTH entries is not cosmetic: without it the entry would
breach its own cap and `test_the_skills_entry_runs_under_its_own_byte_cap` would go red
instead of green. Extend `why` with "agi-post + agi-stream named since <ref> (build nodes
minted under goal:g1.31.2); cap 6000->7000 at 6167 measured bytes".

## Production lines

`git diff --numstat` over `.agi/nodes/.geometry/rotations.md` (unchanged: 0),
`.agi/nodes/build/skills-agi-post-SKILL.md.md`, `.agi/nodes/build/skills-agi-stream-SKILL.md.md`
= 24 lines total, two new files, rotations.md untouched.

## Agent Notes
Minted build:skills-agi-post-SKILL.md and build:skills-agi-stream-SKILL.md (both resolve, payload 2:7 rc 0); the rotations.md clause half is REFUSED by the [config] written_by gate (kid not admitted), measured 5259+908=6167 bytes so byte_cap must go 6000->7000.

REVIEW a00-06814999 (parent): ACCEPTED as an honest HALF, verdict pending stands. PROBES RUN BY ME, not by the kid: (gate) I re-ran extensions/agi/tests/test_skills_first_turn_entry.py -q myself: 1 failed 3 passed, the omit test naming [agi-post, agi-stream] — the claim conjunct (1) is NOT satisfied, exactly as the kid said. (auth) I re-ran the config write myself: `write.py config:rotations "sub! ..."` -> RING-GATE PREVIEW + ERR "may be hand-edited only by admitted roles owner, prime_director; resolution for actor gave PARENT" — so the block is not kid-specific: a parent is refused too, and .agi/context/schemas/[config].md:8 actor_rows grants `templates`+`startup` to master-sensei (deny_roles: [prime_director]). BYTES I read, not the report: nodes/build/skills-agi-post-SKILL.md.md and skills-agi-stream-SKILL.md.md EXIST and both resolve via node_writer.find_node_file; rotations.md still carries zero agi-post/agi-stream strings. DEFECT (cosmetic, not a demotion): each new build node body repeats its own H1 twice. ESCALATION: the second half of conjunct (1) needs master-sensei or owner, not a kid and not a parent — the exact byte edit is in the node and it is measured (5259+908=6167 B, cap 6000->7000).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
RE-JUDGE 10-02 14:5xZ (director-general-1, belam [owner] 14:54Z: 'a00-dd443bfa is YOUR node: all three conjuncts now hold on the trunk -> re-judge it'). The blocker named here is GONE: belam wrote the config:rotations half (ae3d4e366 + ab864f427, landed in 96140880b with the build nodes; why cells 9917f032d name cap 7000 / 6205 B measured) and the locations.stream cell (369b03607). PROBES I RAN on the trunk fa527d71c, not the kid: (1) test_skills_first_turn_entry.py + test_locations.py 89 passed (4 + 85; the trunk red is gone, SM's full suite 7911 passed / 0 failed at 96140880b); (2) `paths.py audit skills/agi-stream` rc 0 and `git grep -nE '<home>/|~/|/home/' -- skills/agi-stream skills/agi-post` 0 hits; (3) `git grep -nE '(heal|rotate|send)\.py:[0-9]' -- skills/agi-post/SKILL.md` 0 hits (the cites by name were ast-checked inside their functions by SM at landing); (4) `locations.py --stream stub` == `locations.streamer_stub(root)` (same directory); `"stream"` is a cell in .agi/config.json. VERDICT: proved (was pending): the kid's half (build nodes, 6167 B projection, the exact edit) was correct as measured, and the other half it named as a Prime step was written byte-exact as it said.

PARENT REVIEW, rewriting: the kid did not overclaim, and that is the finding. (1) WHAT THE BRIEF SAID, quoted: "Both config:rotations skills entries name every skills/agi*/ dir through its build node under a raised byte_cap (test_skills_first_turn_entry.py green)". (2) WHAT THE MACHINE DOES: half of it landed as BYTES I read — nodes/build/skills-agi-post-SKILL.md.md and skills-agi-stream-SKILL.md.md exist and node_writer.find_node_file resolves both; the other half is a hard role gate, and I re-ran it myself, not the kid: write.py config:rotations sub! -> "config nodes (config:rotations) may be hand-edited only by admitted roles owner, prime_director; resolution for actor gave parent", so the refusal is not a kid artefact, it binds this parent too; schemas/[config].md actor_rows row 1 grants templates/startup to master-sensei with deny_roles [prime_director], which is the only admitted route. My own pytest run: 1 failed 3 passed, the omit test still names [agi-post, agi-stream], so the suite is RED and the conjunct is honestly unmet. (3) NEAR MISS: a kid that had written rotations.md by hand would have turned the suite green and shipped an unsanctioned, unwritten node edit that write_guard flags and the next rotate discards — green tests with no sanctioned bytes behind them, the exact shape of the SL7.136 defect. (4) NO DEVIATION from the parent rule against hand-landing a kid edit: I did not land it, I could not; the edit needs a seat the graph admits and this tier is not one. Verdict pending is the honest state; the node keeps its evidence (byte-exact clauses + the 5259+908=6167 measurement) so the master-sensei/owner round is a paste, not a re-derivation.
<!-- THOUGHT:END -->
