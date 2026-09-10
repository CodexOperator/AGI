---
id: experiment:a00-842bed89-b28df3
mint_id: 344aeeffb72b4b71b78ad9a6f8fd31bf
type: experiment
parents:
  - hypothesis:l4-links-roles-report
next_edges: []
confidence: 0.8
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-842bed89-b28df3
loop: hypothesis:l4-links-roles-report@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b99529bcff1aa891
season: 2
thought_session: sanctuary-director-genII-L4
title: "links.py roles: the coverage-gap report built and shown dry"
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-842bed89-b28df3

## Experiment

Built the THIRD dry report, `links.py roles`, on the `hypothesis:l4-links-roles-report` claim — the one that finds the coverage GAP (almost no schema declares `written_by:`) instead of hiding it behind a near-empty violations list.

What I did:
1. Added `_roles_report(root)` to `extensions/agi/bin/links.py`, reading each type's declared writer straight from the schema registry (`schema.frontmatter["written_by"]`, via the same `node_writer.required_fields` path so the report agrees with the schema by convention). Admitted writers = the `written_by:` value(s); a node's recorded writer is `role:` then `edited_by:`, and a node with neither is UNRECORDED, never guessed.
2. Wired it in as the third `action` at the argparse choices (`links` | `schema` | `roles`) with its own dispatch, ahead of the `links`/`schema` branches — those two code paths are untouched.
3. `roles` writes nothing: no `--fix`, no node_write, no schema edit. Dry by default and loudly so.
4. Added two tests to `extensions/agi/tests/test_links.py` (fixture corpus per the claim's proof (3)) and ran `pytest extensions/agi/tests/test_links.py -q` — NOT the full suite, per the claim's hard ceiling. I did not touch `.agi/nodes/.geometry/*`.

Actual output of `python3 extensions/agi/bin/links.py roles --root .` on this corpus (paste, not description — proof (1)):
```
roles: 18 node type(s) in the corpus; 1 declare(s) written_by, 17 do not (the coverage gap)
  coverage census (18 type(s)):
    type              nodes  written_by
    bigger_outcome       19  (none)
    build               298  (none)
    command               1  (none)
    config                2  (none)
    cron                  1  (none)
    doc                   5  (none)
    experiment          477  (none)
    goal                144  (none)
    hypothesis          412  (none)
    idea                 91  (none)
    ladder                1  (none)
    moral                 5  owner
    mvp                  62  (none)
    outcome              24  (none)
    overview             17  (none)
    task                 91  (none)
    verdict             165  (none)
    vision               20  (none)
roles: 1 declared type(s) — every recorded writer is admitted, none unrecorded
```
The census confirms the claim's central finding with live numbers: **18 node types, only 1 (`moral`) declares `written_by:` at all**. A violations-only report would have printed "0 violations" and read as clean; both halves are the honest read.

## Evidence

Proof (2) — dry by construction, shown by byte-identical porcelain (I ran the report between the two captures):
```
$ git status --porcelain
 M extensions/agi/bin/links.py
?? .agi/nodes/experiment/a00-842bed89-b28df3.md
diff before.txt after.txt -> IDENTICAL — report wrote nothing
```
Proof (3) — `pytest extensions/agi/tests/test_links.py -q` = **22 passed** in 0.16s. Of these, the two new tests:
- `test_roles_report_names_a_violation_and_writes_nothing`: a schema declares `written_by: owner`; a node with `role: kid` is NAMED with writer `'kid'` and `admitted: owner`, the `owner` node is not flagged, and a node file is proven byte-identical afterwards (report writes nothing).
- `test_roles_report_marks_unrecorded_without_guessing`: a node in a declared type with no `role:`/`edited_by:` prints `UNRECORDED`, never a guess or silent skip.
Proof (4) — the existing two actions are untouched and still print their prior reports:
```
$ links.py links   -> links: 1817 resolved, 0 broken (18 retired payload(s), not damage)
$ links.py schema  -> schema: 144 node(s) missing a required field
```

Edge cases handled: multi-value `written_by:` (space/comma separated -> admitted set); `unknown` type when frontmatter lacks `type`; deprecated nodes (under `nodes/deprecated/`) count under their real type; a type with no schema file is a gap, not a crash.

Caveat: the claim's stated baseline (214 of 1830 nodes carry `role:`) does not reproduce on this checkout — here almost every node records no `role:` (only ~185 total). The roles *mechanism* is exactly as documented; the corpus makeup differs from the director's earlier sampling. The report measures what is there, so this weakens only the hypothesis's quoted numbers, not its structure.

## Agent Notes
Implemented and proved links.py roles: reports the coverage gap (18 types, 1 declares written_by: owner) plus violations and UNRECORDED nodes, via schema-registry written_by; writes nothing (porcelain identical); 2 new tests in test_links.py, 22 passed; links/schema outputs unchanged.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-03c876a0, L4.05): accepted as proved. I reproduced all four proofs myself on this checkout: `links.py roles` prints the census shown (18 types, 1 declares written_by), test_links.py 22 passed including the two new fixture tests, third action wired at links.py:294/:311, working tree carries only the expected files. Verdict stands — the coverage gap IS the finding and the report prints both halves. One caveat upheld rather than refuted: the claim baseline "214 of 1830 role: nodes" did not reproduce (~185 here); that weakens the quoted numbers, not the mechanism, and is recorded in the node Evidence section honestly. links and schema outputs unchanged.
<!-- THOUGHT:END -->

**DIRECTOR REVIEW (L4.05, sanctuary-director L4 gen II). Verdict `proved` ACCEPTED.**

I ran the report rather than reading the claim about it. Output, verbatim from the round's own worktree:

```
roles: 18 node type(s) in the corpus; 1 declare(s) written_by, 17 do not (the coverage gap)
    moral                 5  owner
    build               298  (none)      hypothesis          412  (none)
    experiment          477  (none)      goal                144  (none)
    ... 13 more types, all (none)
roles: 1 declared type(s) -- every recorded writer is admitted, none unrecorded
```

**And `git status --porcelain` was 0 lines before AND after the run.** That was half the claim -- a dry report that writes nothing -- and it is the half easiest to get wrong quietly, so it was checked directly rather than inferred from the absence of a `--fix` flag. `pytest extensions/agi/tests/test_links.py -q` -> **22 passed**. `links` and `schema` print exactly what they printed before (1817 resolved / 0 broken; 144 nodes missing a required field), so the two existing actions are untouched.

**THE REFRAME EARNED ITSELF, and the number is the argument.** A violations-only report would have printed `0 violations` and been true, while 17 of 18 types in this corpus admit nothing at all and are therefore unfalsifiable rather than clean. 477 experiments, 412 hypotheses, 298 builds, 144 goals -- every one of them uncheckable, and a report that said only `0 violations` would have implied the opposite. The census is what makes the number honest.

**This report is now the input to a decision that has since been made.** The owner ruled (`doc:l4-owner-decisions`, verbatim): *"I'm fine with making the check more strict per type ... I'm find having graph nodes that lack writers for now can backfill at the end since it used to be all Director Prime so it's easy to backfill truthfully."* L4.09 -- `written_by` warn -> refuse, one type at a time -- is GO on the strength of exactly the gap this report measures. The round's value was never the violation list; it was knowing the size of what could not be checked.

**One pre-existing debt this run surfaced and did NOT touch, recorded so it is not mistaken for damage later:** `links.py schema` reports 144 nodes missing a required field, 124 of them hypotheses missing `testable_claim`. That predates this round and belongs to neither it nor L4.09.
