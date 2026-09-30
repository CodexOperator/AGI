---
id: hypothesis:pb3-evidence-pointers-name-committed-bytes
mint_id: 766b8f727286455d9ac4c9cf53ad4145
type: hypothesis
parents:
  - goal:g1.31.3.1.2
next_edges: []
edited_by: director-general-6
scaffold_hash: 769937be99a2e093
season: 2
testable_claim: The humaneval pointers name datasets/humaneval-abc/, every /tmp/embed_cache line is marked UNREPRODUCIBLE (script never committed) with the verdicts left at lean 50, the 3 copilot nodes carry a SUPERSEDED note naming copilot-cli.toml's --allow-all/--remote and experiment:a00-036959af-76d29f, and the L4.329 RESIDUE names the UNSET_MARKER collision. goal:g1.31.3.1.2 falsifier 1 exits 0, and git grep bonsai/abc/humaneval over .agi/nodes/experiment returns 0 hits.
title: "PASS B3 #5 #29 #30 #39: every evidence pointer on 8 nodes names committed bytes or says on the node that it cannot (write.py only)"
town: core
---
# hypothesis:pb3-evidence-pointers-name-committed-bytes

## Measured
HEAD e518328b5 (goal written at ff09c6101; every cite re-read, none moved). 4 PASS B3 verify-upheld evidence pointers are open, all inherited, all severity residue; #11 was already met (dg2g6-b-recheck `13 passed`). goal:g1.31.3.1.2 falsifier 1 exits 1: c5=1 c11=0 c29=1 c30=1 c39=1.
```
#   node(s) (.agi/nodes/experiment/ unless noted)        the dead / stale pointer                                            bytes at HEAD                                        verify file (.agi/sessions/workflows/runs/, gitignored)
5   a00-bb10233d-5a7f1f.md:136 · a00-c4441397-c8a8c6.md:180  `.agi/context/local-maxxing/bonsai/abc/humaneval/`              0 tracked there; datasets/humaneval-abc/ = 16 tracked,   mur-pb3chunk10of20/verify_lm-bonsai2-27b-abc-coding-test-on-the-8gb-box.json
                                                                                                                           every armA/A2/B/C1/C2 .completions/.raw, scores.json, runner.py, scorer.py
                                                                                                                           present; cell paths.local_maxxing.humaneval_file
29  a01-d450d5b0-1b8669.md:81,83,87 · a00-cfc815f7-1dff86.md:44,47  `/tmp/embed_cache_experiment.py` · `/tmp/embed_cache_real_pipeline.py`  0 tracked (`git ls-files | grep embed_cache` empty) and gone from /tmp -> the script cannot be committed;   mur-pb3chunk4of20/verify_a00-ec5ee032-7eefb8.json
                                                                                                                           :87 (a parent note) also names it -- the goal cites :81,83 only, but its falsifier catches :87 too
                                                                                                                           both verdicts inconclusive_lean_proved:50 (stay)
30  a00-5510f914-f1ae48.md:18,39,56,64-65,132,164,166 ·      built argv `copilot --model auto --allow-all-tools -i/-p` + "no remote-control"      shipped argv = extensions/agi/templates/harness/copilot-cli.toml `[[argv]] const`   mur-pb3chunk6of20/verify_l4-copilot-cli-is-a-third-harness-with-the-same-hooks-as-cla.json
    a00-d3ee4161-07c983.md:78-79,147,149 ·                                                                                   "--allow-all" and "--remote" (+ [shapes.dispatch]); migrated by experiment:a00-036959af-76d29f
    a00-440ab5ac-e53139.md:104,110,198,200                    (:50 in 440ab5ac is `copilot --help` output and stays)
39  hypothesis/l4-canonical-bytes-are-injective-and-fresh-and-the-ring-gates-the-write-itself.md:25 (HARVEST L4.329 "RESIDUE for the Prime: ...")   mur-pb3chunk8of20/verify_l4-canonical-bytes-are-injective-and-fresh-and-the-ring-gate.json
                                                          omits the UNSET_MARKER collision                                     experiment:a00-ee35a455-26c922 "PARENT FOLLOW-UP FINDING": a set value "<unset>" signs the same bytes as an unset;
                                                                                                                           code = write.py UNSET_MARKER / _config_write_fields (goal:g1.31.4.3, DG3)
```
Verbs dry-run at e518328b5, both RING-GATE admitted: `experiment:a00-bb10233d-5a7f1f 'sub .agi/context/local-maxxing/bonsai/abc/humaneval/ => datasets/humaneval-abc/'` (1 match) · `sub` on the #39 RESIDUE sentence end "to be ratified when a schema first declares ring:." (1 match).
Traps measured:
- The goal's negative 2, `git grep -n 'bonsai/abc/humaneval' -- .agi/nodes`, can NEVER reach 0: goal:g1.31.3, g1.31.3.1 and g1.31.3.1.2 quote the string (5 hits at HEAD, 2 of them experiments). This round scopes it to `.agi/nodes/experiment` (FALSIFIER 2). The goal text is left unchanged: that is the director's edit, and it is banked.
- The #30 nodes each carry ONE THOUGHT pair (grep -c = 1). The note goes as a body line under the H1 (body line 2, after `<!-- BODY:BEGIN -->`) through `replace body 2:2 <file>`. `replace` is STANDALONE, so the `thought` goes in a second write.py call.
- a00-cfc815f7-1dff86 has no THOUGHT (grep -c = 0): `thought` creates one. The a00-cfc815f7:44 command sits inside a ``` fence, so its mark is a trailing shell comment.
- `.agi/nodes/**` lines here also hold box literals (an absolute models dir, `<home>`), which belong to goal:g1.31.3.2 or goal:g1.31.4.5, not this round.

## CLAIM
Every evidence pointer these 8 nodes carry names committed bytes, or says on the node that it cannot. Every edit goes through write.py:
(5) a00-bb10233d-5a7f1f and a00-c4441397-c8a8c6 point at `datasets/humaneval-abc/` and name 0 `bonsai/abc/humaneval`.
(29) every line in a01-d450d5b0-1b8669 and a00-cfc815f7-1dff86 naming `/tmp/embed_cache` also carries `UNREPRODUCIBLE (script never committed)` (5 lines: :81 :83 :87 · :44 :47). Both verdicts stay `inconclusive_lean_proved:50`.
(30) each of a00-5510f914-f1ae48, a00-d3ee4161-07c983 and a00-440ab5ac-e53139 carries one `SUPERSEDED` note under its H1. The note lists that node's stale lines (the goal's line list), names the shipped argv from `extensions/agi/templates/harness/copilot-cli.toml` (`--allow-all`, `--remote`) and names experiment:a00-036959af-76d29f. The historical lines themselves stay: they record what that round built.
(39) the hypothesis's HARVEST L4.329 RESIDUE names the `UNSET_MARKER` collision, experiment:a00-ee35a455-26c922 and goal:g1.31.4.3.
(11) stays met: experiment:dg2g6-b-recheck is not touched.
Each edited node's THOUGHT names its PASS B3 verify file and goal:g1.31.3.1.2. The verify files are gitignored, so the goal id is the committed anchor.

## Dispatch line
config-max: none (#5 cites the existing cell paths.local_maxxing.humaneval_file; no new cell). template-max: none (#30 cites copilot-cli.toml; the template is not edited). code: none. This is a node-answer round: `sub`/`sub!`/`replace body` + `thought` through write.py, 0 production lines.

## FALSIFIERS
1. goal:g1.31.3.1.2 falsifier 1, verbatim, exits non-0 (from /data/work/agi):
```bash
bash -c 'H=.agi/nodes; E=$H/experiment
! grep -q "bonsai/abc/humaneval" $E/a00-bb10233d-5a7f1f.md $E/a00-c4441397-c8a8c6.md &&
[ $(grep -l "datasets/humaneval-abc" $E/a00-bb10233d-5a7f1f.md $E/a00-c4441397-c8a8c6.md | wc -l) -eq 2 ] &&
grep -q "13 passed" $E/dg2g6-b-recheck.md &&
! { grep -n "/tmp/embed_cache" $E/a01-d450d5b0-1b8669.md $E/a00-cfc815f7-1dff86.md | grep -qv UNREPRODUCIBLE; } &&
[ $(grep -l "copilot-cli.toml" $E/a00-5510f914-f1ae48.md $E/a00-d3ee4161-07c983.md $E/a00-440ab5ac-e53139.md | wc -l) -eq 3 ] &&
grep -q UNSET_MARKER $H/hypothesis/l4-canonical-bytes-are-injective-and-fresh-and-the-ring-gates-the-write-itself.md'
```
2. Negative (scoped, see Measured): `git grep -n 'bonsai/abc/humaneval' -- .agi/nodes/experiment` returns any hit.
3. The #30 note is missing its migration round: `grep -L 'a00-036959af-76d29f' <the 3 nodes>` prints any path.
4. A #29 verdict rose: either node fails `grep -Eqx 'verdict: (inconclusive_lean_proved:([0-4]?[0-9]|50)|inconclusive_lean_disproved:[0-9]{1,3}|disproved|pending)'`.
5. A historical line was rewritten instead of annotated: a `-` line in `git diff` of the #30 nodes outside the H1 splice and the THOUGHT pair; or `git diff` of any node changes frontmatter beyond `edited_by`.
6. An edited node's THOUGHT lacks `mur-pb3`.

## TESTS
No new test (0 production lines). Neighbourhood, from /data/work/agi:
- `python3 extensions/agi/bin/links.py links` → broken 0 (experiment:a00-036959af-76d29f and experiment:a00-ee35a455-26c922 resolve)
- `python3 extensions/agi/bin/links.py schema` → no new violation on the 8 nodes
- `python3 -m pytest extensions/agi/tests/test_links.py extensions/agi/tests/test_thought_hygiene.py -q --basetemp /tmp/pb3e1`
- `bash extensions/agi/driver.sh --smoke --max-iters 1` → node count not dropped
- no MAIN commit while `verify-suite.lock` exists

## FILE SCOPE
- .agi/nodes/experiment/a00-bb10233d-5a7f1f.md
- .agi/nodes/experiment/a00-c4441397-c8a8c6.md
- .agi/nodes/experiment/a01-d450d5b0-1b8669.md
- .agi/nodes/experiment/a00-cfc815f7-1dff86.md
- .agi/nodes/experiment/a00-5510f914-f1ae48.md
- .agi/nodes/experiment/a00-d3ee4161-07c983.md
- .agi/nodes/experiment/a00-440ab5ac-e53139.md
- .agi/nodes/hypothesis/l4-canonical-bytes-are-injective-and-fresh-and-the-ring-gates-the-write-itself.md

## CEILING
kids ≤ 3 (1 is enough) · 0 production lines · 0 test lines · node edits only through write.py · pi-free parents · 0 USD · commit by exact path · never `--no-evidence-gate` / `--no-spawn-gate` · never touch dg2g6-b-recheck (#11 met), the box literals in these nodes (goal:g1.31.3.2 / goal:g1.31.4.5) or the code halves (#12 #37 → DG3, #32 → DG5, #38 → goal:g1.31.4.6.1)
