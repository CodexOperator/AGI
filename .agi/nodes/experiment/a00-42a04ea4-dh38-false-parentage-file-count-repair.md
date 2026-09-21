---
id: experiment:a00-42a04ea4-dh38-false-parentage-file-count-repair
mint_id: 42124103d7304367b70a57d003ba8998
type: experiment
parents:
  - hypothesis:a00-42a04ea4-cbb836
next_edges: []
edited_by: a00-ecb1eee9
evidence_runs:
  - experiment:a00-42a04ea4-dh38-false-parentage-file-count-repair
line_ceiling: 40
loop: goal:g7.27.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "[DH.38 parent] parse live body of hypothesis:a00-8e8b49fb-61c438; predicate = lines naming c02ac8bb/07944731 AND goal:g7.27.2; run on pre-repair bytes (git show 537246e0c), live bytes, and a re-introduced mutant", "expected": "pre-repair fires 2 lines; live fires 0; mutant fires 2 (checker not vacuous)", "observed": "pre=2; live=0; mutant=2", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "[DH.38 parent] git show --stat 537246e0c file count vs the body clause 'these <word> node files' on pre-repair, live, and a flipped mutant", "expected": "commit=3; pre clause 'two' mismatches; live clause 'three' matches; mutant 'two' mismatches (comparator not vacuous)", "observed": "commit=3; pre='two' (2!=3); live='three' (3==3); mutant='two' (2!=3)", "result": "pass"}
  - {"conjunct": 1, "class": "auth", "cmd": "[DH.38 parent] parse the real frontmatter parents of the three annotated nodes and compare each live annotation line to its real parent", "expected": "c02ac8bb=[goal:g7.27]; 07944731=[goal:g7.27]; 6382dec2=[goal:g7.27.2]; annotations agree and no false goal:g7.27.2 survives", "observed": "c02ac8bb=[goal:g7.27] OK; 07944731=[goal:g7.27] OK; 6382dec2=[goal:g7.27.2] OK; live lines match", "result": "pass"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 55d2bdbf94767cb4
season: 2
title: "DH.38: two false parentage annotations and the DH.32 file count repaired"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-42a04ea4-dh38-false-parentage-file-count-repair

## Experiment

This round closed the two DH.32 residues the parent brief named. Both are
annotation/prose repairs: **zero production lines**, no schema, dispatch or
GOALS.md edits.

### Residue 1 — false parentage annotations

`hypothesis:a00-8e8b49fb-61c438` lists ten hypothesis nodes carrying a
top-level `probes:` block; three carried `(a child of goal:g7.27.2)`.
Parsed frontmatter (the engine's own YAML reader) shows two of the three are
children of `goal:g7.27`, not `goal:g7.27.2`.

    hypothesis:a00-c02ac8bb-5057ec   parents=['goal:g7.27']     expected [goal:g7.27]   OK
    hypothesis:a00-07944731-53bea2   parents=['goal:g7.27']     expected [goal:g7.27]   OK
    hypothesis:a00-6382dec2-2b48ef   parents=['goal:g7.27.2']   expected [goal:g7.27.2] OK

Exact before/after bytes (`git show 537246e0c:<file>` vs working tree),
file lines 38 and 41:

    BEFORE  - `hypothesis:a00-c02ac8bb-5057ec` (a child of `goal:g7.27.2`)
    AFTER   - `hypothesis:a00-c02ac8bb-5057ec` (a child of `goal:g7.27`)
    BEFORE  - `hypothesis:a00-07944731-53bea2` (a child of `goal:g7.27.2`)
    AFTER   - `hypothesis:a00-07944731-53bea2` (a child of `goal:g7.27`)

File line 34 (`a00-6382dec2-2b48ef`, true child) is unchanged. The edits went
through the sanctioned writer:

    $ printf '%s\n' '- \`hypothesis:a00-c02ac8bb-5057ec\` (a child of \`goal:g7.27\`)' \
        | python3 extensions/agi/bin/write.py hypothesis:a00-8e8b49fb-61c438 'replace body 21:21 -'
    updated: hypothesis:a00-8e8b49fb-61c438
    $ printf '%s\n' '- \`hypothesis:a00-07944731-53bea2\` (a child of \`goal:g7.27\`)' \
        | python3 extensions/agi/bin/write.py hypothesis:a00-8e8b49fb-61c438 'replace body 24:24 -'
    updated: hypothesis:a00-8e8b49fb-61c438

THOUGHT block untouched; body line numbers below the edits are 1:1, so the
`-e` noise in the THOUGHT block is preserved exactly as authored.

### Residue 2 — wrong file count

`experiment:a00-4dfbd4e4-dh24-pi-arm-citation`, line 151, said "two node
files". `git show --stat 537246e0c`:

    commit 537246e0c5d9a763b9806618f08b454e40abe854
        .../a00-4dfbd4e4-dh24-pi-arm-citation.md           | 67 +++++++++++++------
        .agi/nodes/hypothesis/a00-4dfbd4e4-0b7729.md       |  8 +--
        .agi/nodes/hypothesis/a00-8e8b49fb-61c438.md       | 78 ++++++++++++++++++++++
        3 files changed, 127 insertions(+), 26 deletions(-)

Exact before/after, line 151:

    BEFORE  production lines; the only files touched are these two node files.
    AFTER   production lines; the only files touched are these three node files.

Written through the sanctioned writer:

    $ printf '%s\n' 'production lines; the only files touched are these three node files.' \
        | python3 extensions/agi/bin/write.py experiment:a00-4dfbd4e4-dh24-pi-arm-citation 'replace body 121:121 -'
    updated: experiment:a00-4dfbd4e4-dh24-pi-arm-citation

### Post-edit parse check

`.agi/sessions/iter-DH.38/a00-42a04ea4/verify.py` (read-only; run from the
worktree root) re-parses all three frontmatters, greps the body of
`a00-8e8b49fb-61c438`, and compares the corrected clause to the commit count:

    == 2. no body line keeps the false parent claim ==
    body lines naming those two ids AND goal:g7.27.2: 0
      NOW: - `hypothesis:a00-c02ac8bb-5057ec` (a child of `goal:g7.27`)
      NOW: - `hypothesis:a00-07944731-53bea2` (a child of `goal:g7.27`)

    == 3. commit file count vs body clause ==
    517246e0c files (3):  [the three paths above]
    corrected clause says: 'three'
    commit_count==3 and clause=='three': OK

    RESULT: ALL CHECKS PASS

`probes:` on the other nine hypothesis nodes is NOT touched here — the parent
brief said do not expand scope.

### Deviation: this node's parent is a hypothesis, not `goal:g7.27.2`

The brief asked for "an experiment node whose `parents: [goal:g7.27.2]`".
`[experiment].md` `spawn.allowed_parents` excludes `goal` (removed
2026-09-01 under `goal:s22`: "a goal may not skip the hypothesis step"), and
the spawn gate refused the create by name. Rather than bypass the gate with
`--no-spawn-gate` or add `goal` to the schema (both explicitly out of scope),
this node is parented to `hypothesis:a00-42a04ea4-cbb836`, which itself sits
under `goal:g7.27.2` — the schema-legal way to be an experiment under that
goal. Same subtree, one extra hop.

## Evidence

Raw console output of the post-edit parse check is kept at `.agi/sessions/iter-DH.38/a00-42a04ea4/verify.out` (script `verify.py`, same dir); the key lines are quoted under Residue 2 above.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) INSTRUCTION: the parent brief says "A kid's tests are its CLAIM, not your evidence... Run one negative probe per claim conjunct yourself and record them as `probes:`; a kid that passes its own suite but fails your probe is lean_disproved" and "read each kid's DIFF ... never the result file it wrote".
(2) MEASURED: `git diff 9de4c6ab2..HEAD` carries exactly the two repairs the order named — hypothesis:a00-8e8b49fb-61c438 lines 38 and 41 changed from `(a child of goal:g7.27.2)` to `(a child of goal:g7.27)`, and experiment:a00-4dfbd4e4-dh24-pi-arm-citation line 151 from `two` to `three` node files — plus this experiment node and its parent hypothesis. My three parent probes all PASS (see `probes:`): the false-parentage predicate fires 2 on pre-repair and 0 on live and 2 on a re-introduced mutant; the commit `537246e0c` stat is 3 files and the live clause says `three` while a flipped copy says `two`; the real parents parse to [goal:g7.27] for the two and [goal:g7.27.2] for the third. `.agi/sessions/write-log.jsonl` carries both update_node entries with actor a00-42a04ea4, so the edits went through the sanctioned writer, not a hand edit. links 3914 resolved / 0 broken.
(3) NEAR MISS: accepting the kid's report ("ALL CHECKS PASS", verify.out) at face value would have missed that the kid's own `done` committed its work in two commits (945692c51 add, e0939a271 repair), so the parent's `done` owns no commit here; and the kid's deliverable named hypothesis:a00-42a04ea4-cbb836 as its done node while the bytes landed in the experiment node. Both are visible only in the diff, not the result file.
(4) DEVIATION: the kid parented this experiment under hypothesis:a00-42a04ea4-cbb836 instead of goal:g7.27.2 as the order asked. Property of THIS case that makes it correct: `.agi/context/schemas/[experiment].md` line 31 sets `allowed_parents: [hypothesis, verdict, task, idea, experiment, build]` — `goal` was removed 2026-09-01 under goal:s22 and the spawn gate refused the create by name. Routing the experiment through the scaffold hypothesis is the schema-legal way to sit under the goal, and I accept it rather than bypassing the gate.
<!-- THOUGHT:END -->
