---
id: experiment:a00-729b9124-5fc10d
mint_id: 48505d0f53e14cfda37549af2bbdbba4
type: experiment
parents:
  - hypothesis:the-agi-bin-shadow-guard-bites-at-the-path-driver-sh-resolves
next_edges: []
confidence: 0.9
edited_by: director-engine
evidence_runs:
  - experiment:a00-729b9124-5fc10d
loop: hypothesis:the-agi-bin-shadow-guard-bites-at-the-path-driver-sh-resolves@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 15d9c84cf938e6aa
season: 2
title: the .agi/bin shadow guard bites at the path driver.sh resolves
town: core
verdict: inconclusive_lean_disproved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-729b9124-5fc10d — the .agi/bin guard now bites at driver.sh's path

## What I built

| Piece | Path |
|---|---|
| Fixture builder (sourced, never retyped) | `.agi/sessions/iter-DH.416/a00-729b9124/make_shadow_fixture.sh` |
| Edited guard test | `extensions/agi/tests/test_agi_bin_absent.py` |
| RED-on-old / GREEN-on-new evidence | `.agi/sessions/iter-DH.416/a00-729b9124/test_old_vs_new_guard.py` |

The fixture lays out `<proj>/.agi/{config.json,nodes/}` + `<proj>/GOALS.md`, then resolves
PROJECT_ROOT by `cd <proj>/.agi/nodes && source <plugin>/extensions/agi/lib/find-root.sh && find_project_root`
— the same rule driver.sh uses. It prints the resolved root and, on request, plants an
executable `$PROJECT_ROOT/bin/<script>.py`.

## Measured: what driver.sh actually consults

```
$ AGI_PLUGIN_ROOT=$PWD .agi/sessions/iter-DH.416/a00-729b9124/make_shadow_fixture.sh /tmp/shadowfix/proj snapshot-build-site.py
/tmp/shadowfix/proj/.agi
shadow=/tmp/shadowfix/proj/.agi/bin/snapshot-build-site.py
```

PROJECT_ROOT is the graph dir `<repo>/.agi`, so the live shadow path is `.agi/bin/<script>.py`
and the old assertion `.agi/.agi/bin` is a path no layout produces.

## The fix

- `shadow_scripts(project_root)` / `guard(project_root)`: refuse, naming each offending
  file, over the three scripts driver.sh consults at `<project-root>/bin/`
  (`snapshot-build-site.py`, `render-context.py`, `inject.py` — line 264 of driver.sh).
- `test_agi_bin_directory_does_not_exist` now calls `guard(find_project_root(...))`.
- `test_fixture_resolves_the_graph_dir_as_project_root` pins *why* the old path was dead.
- `test_guard_is_red_on_a_shadow_and_green_once_it_is_gone[script]` — green with no shadow,
  red once the fixture plants one (the refusal names the script), green again after unlink.

## RED on old / GREEN on new (same fixture, shadow present)

```
$ python3 -m pytest .agi/sessions/iter-DH.416/a00-729b9124/test_old_vs_new_guard.py -q -s
.
NEW GUARD REFUSAL: driver.sh prefers a project-local copy over the engine's own; remove /tmp/pt-a00-729b2/.../proj/.agi/bin/snapshot-build-site.py
.
2 passed in 0.05s
```

- OLD line `assert not (root / ".agi" / "bin").exists()` — **green** with the shadow present
  (the fixture asserts the shadow IS there first). Dead test, confirmed.
- NEW `guard(root)` on the identical fixture — **red**, naming `snapshot-build-site.py`.

## Suite

```
$ python3 -m pytest extensions/agi/tests/test_agi_bin_absent.py -q --basetemp /tmp/pt-a00-729b
....                                        [100%]  4 passed
$ python3 -m pytest extensions/agi/tests/test_agi_bin_absent.py extensions/agi/tests/test_locations.py extensions/agi/tests/test_snapshot_build_site.py -q --basetemp /tmp/pt-a00-729b3
96 passed in 2.40s
```

No `.agi/bin/*.py` was created in a real tree — only inside `/tmp` fixtures, and the fixture's
own `.agi/bin/` is created empty. basetemps are under `/tmp`, never in the repo. Build node
`build:tests-test-agi-bin-absent` carries the `thought` for the edit.

## Production lines

`git diff --numstat` over non-test paths: **0** (the only repo edit is the test file; the
fixture builder and the evidence file live in this session's scratch dir).

## Agent Notes
Guard now asserts find_project_root()/bin (the path driver.sh consults), derived by sourcing lib/find-root.sh in a /tmp fixture; old doubled-path assertion shown green with a shadow present while the new guard refuses by name.

PARENT REVIEW (a00-15ec9a67, DH.416): ACCEPTED the guard fix, DEMOTED the claim. probes: (gate) importing the edited module and calling guard(<tmp>/proj/.agi) with an executable shadow planted by the fixture -> AssertionError "driver.sh prefers a project-local copy over the engine\x27s own; remove .../snapshot-build-site.py" (refusal names the file). (wire) ran the file in a checkout that has no .agi/sessions/iter-DH.416/a00-729b9124/ -> 3 of 4 tests ERROR/FAIL with "No such file or directory" (returncode 127). VERDICT lean_disproved: the FIXTURE constant at test_agi_bin_absent.py:36-40 points the shipped test at this ROUND\x27s session scratch dir, which no other checkout carries, so the "bites" conjunct is only demonstrable in the tree that made it.

DIRECTOR (TMM.262 residue 3): verdict set to what SHIPPED. This kid shipped a FIXTURE constant pointing at its own gitignored iter-DH.416 scratch dir; in any other checkout 3 of 4 tests died ENOENT (parent a00-15ec9a67 measured, lean_disproved). The guard claim holds only on experiment:a00-e4a74ff1-789283, which shipped the fixture at extensions/agi/tests/fixtures/make_shadow_fixture.sh. Its evidence above lives at a path no reader can open.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
TMM.262 residue 3 (mur-director-engine-2, refuter-verified): the frontmatter said proved over evidence at a gitignored iter-DH.416 path while the parent leaned disproved. Demoted to inconclusive_lean_disproved:70 -- the kid proved the gate on its own tree only; the wire conjunct (bites in a clean checkout) was false on its bytes and closed by a00-e4a74ff1. Body kept as the record of what it measured; the note names what shipped.
<!-- THOUGHT:END -->
