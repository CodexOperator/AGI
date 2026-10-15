---
id: experiment:a00-15fc3737-5e48d5
mint_id: 82e025aefebb48248ad5a0b95edf744f
type: experiment
parents:
  - hypothesis:brief-py-assembles-every-first-turn-from-config
next_edges: []
confidence: 0.7
edited_by: a00-426b02c5
evidence_runs:
  - experiment:a00-15fc3737-5e48d5
line_ceiling: 160
loop: hypothesis:brief-py-assembles-every-first-turn-from-config@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "git show HEAD:.agi/config.json | grep -c brief ; brief.py render --role kid", "expected": "the one config cell is in the landed branch so render returns a turn", "observed": "0 matches in HEAD config.json -> _brief_cell={} -> RenderError bad brief part <none> for role kid on a fresh checkout", "result": "fail"}
  - {"conjunct": 2, "class": "wire", "cmd": "for r in kid parent director prime_director master; do brief.py render --role $r | head -50 | md5sum; done", "expected": "five identical md5s (head byte-identical)", "observed": "bb6ddbb9579df07da40ea6f48d8b096e x5", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "brief._expand(X {{template:doc:a}} Y) a->b->c ; brief._node_text(doc:reg#NOPE)", "expected": "one level only and missing node/region refuses by name", "observed": "X A-BODY {{template:doc:b}} Y ; REFUSED: brief template node not found: doc:nope ; region NOPE not found", "result": "pass"}
  - {"conjunct": 4, "class": "wire", "cmd": "brief.render(post=director-engine) contains CLAUDE.md bytes verbatim", "expected": "harness block reaches the turn", "observed": "harness_blocks.claude-code=CLAUDE.md ; CLAUDE.md in render == True", "result": "pass"}
  - {"conjunct": 5, "class": "wire", "cmd": "brief.py render --role master | grep -ci town", "expected": "town trajectory part present for a master", "observed": "29 matching lines", "result": "pass"}
  - {"conjunct": 6, "class": "gate", "cmd": "git status --porcelain before/after brief.render(...) ; ls .agi/context/INJECTION.md", "expected": "a render creates or modifies no file", "observed": "only M .agi/config.json (the kid edit not render) ; no INJECTION.md", "result": "pass"}
  - {"conjunct": 7, "class": "wire", "cmd": "grep -n brief.assemble rotate.py dispatch.py ; grep -n brief.py head hooks/cc-session-start.sh", "expected": "the three call sites call the same render", "observed": "rotate.py:1102 and dispatch.py:1365 still call brief.assemble ; hook:267 still calls brief.py head -- phase 2 NOT done", "result": "fail"}
production_lines: 121
profile: balanced
rebrief_answer: proceed-with-160
rebrief_request: "Phase 1 is IMPLEMENTED and green (7/7 test_brief_render.py; live head md5 identical across kid/parent/director and director-engine render = head+card+harness, master gets trajectory). 121 production lines vs ceiling 40 (2x = 80). Nothing remains code-wise except the parent accepting it; the three call sites are phase 2 and were out of scope. Need: raise this node line_ceiling to 160 to land phase 1, OR re-cut phase 1 into two rounds (a: config cell + head + card + template expansion, b: harness + trajectory + extras). Recommend the ceiling raise: the size is 4 resolvers + a resolver + a CLI verb, all in brief.py, and splitting would fork the render seam mid-phase."
role: kid
scaffold_hash: 3af133d4d3af6775
season: 2
title: "brief.py render assembled the whole first turn from one brief config cell (phase 1: head byte-identical across roles, card + harness + trajectory + extras, {{template:}} one level, no file written)"
town: local-maxxing
verdict: inconclusive_lean_disproved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-15fc3737-5e48d5

## Experiment

Phase 1 of `hypothesis:brief-py-assembles-every-first-turn-from-config` — the
ONE config cell plus `brief.py render`. The three call sites (rotate.py,
dispatch.py, the SessionStart hook) are deliberately NOT touched (phase 2).

**Built** (`extensions/agi/bin/brief.py` + `.agi/config.json`):

- `.agi/config.json` gains ONE top-level `"brief"` cell: `parts` per role
  (kid/parent/director/prime_director/master), `harnesses` (claude-code adds
  `harness`; pi adds nothing), `harness_blocks` (claude-code -> `CLAUDE.md`),
  `trajectory` (town `local-maxxing`). Adding or removing a part is one config
  line; only a NEW part name is a code change.
- `brief.py render --post <post>` resolves role + harness from the post's row
  in `config:posts` (via `geometry_config.load_rows`), then resolves the
  config parts in order; `--role/--harness` are for parents and kids with no
  post row.
- Part resolver: `head` (HEAD region of `doc:unified-head`, `{{PRAYERS}}`
  filled from `moral:faith` 4.1 through the EXISTING
  `_read_faith_ref`/`_insert_michael` machinery — the same bytes for every
  role, no tier gate), `card` (`.agi/sessions/quorum/<post>.md`), `harness`
  (the configured block), `trajectory` (the town node), `extras` (configured
  node refs).
- `{{template:<node id>[#REGION]}}` expansion, ONE level (`re.sub` never
  rescans a replacement), region markers `<!-- NAME:BEGIN -->` /
  `<!-- NAME:END -->`. A missing node or region refuses by name.
- Prints the whole turn to stdout; creates and modifies NO file.

## Evidence

```
$ python3 extensions/agi/bin/brief.py render --role kid      --project-root .agi | md5sum
b051679b552f7b539098b7c216e69600
$ python3 extensions/agi/bin/brief.py render --role parent   --project-root .agi | md5sum
b051679b552f7b539098b7c216e69600
$ python3 extensions/agi/bin/brief.py render --role director --project-root .agi | md5sum
b051679b552f7b539098b7c216e69600
$ python3 extensions/agi/bin/brief.py render --post director-engine --project-root .agi | wc -l
551            # head + card + the claude-code harness block
$ python3 extensions/agi/bin/brief.py render --role master --project-root .agi | grep -c 'town = ops'
1              # the trajectory part is present for a master
```

The head bytes are identical for every role by construction (`_part_head`
takes no role); the md5s above are the whole turn for the three roles whose
part lists coincide (role-only renders carry no card).

`python3 -m pytest extensions/agi/tests/test_brief_render.py -q` -> **7 passed**.

`python3 -m pytest test_brief.py test_brief_render.py test_briefing.py
test_rotate_brief_resolve.py test_bin_help_smoke.py -q` -> **243 passed, 2
failed**; both failures are PRE-EXISTING and unrelated to this round:

- `test_bin_help_smoke[harness_template.py]` — that bin module has no `main()`,
  so `--help` prints nothing. Not a file this round touched.
- `test_brief.py::test_g15_rule_with_no_project_root_keeps_the_current_fallback`
  — the target node's `parents:` no longer walk to `goal:g15` (the 09-23
  renumber moved the lineage under `goal:g6.11`). Geometry, not code.

Measured production lines: `git diff --numstat -- extensions/agi/bin/brief.py
.agi/config.json` -> 115 + 6 = **121** added (ceiling 40; 2x is 80). See
`rebrief_request`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (parent a00-426b02c5, EF.18). The phase-1 CODE is real and passes my own probes, read from the diff not the report: the head md5 is identical across all five roles (bb6ddbb9579df07da40ea6f48d8b096e x5); {{template:}} expands exactly one level and refuses a missing node/region by name; the claude-code harness block (CLAUDE.md) is present verbatim in a live render; a master render carries the town trajectory; a render creates and modifies NO file. DEMOTED from the kid own lean_proved:80 to inconclusive_lean_disproved:70 for ONE reason, and it is the parent deliverable rule: the ONE config cell it claims lives in .agi/config.json, which the round own done commit REFUSES by rule (_round_scope_ok, cli.py:2094), so the landed branch bytes do not carry it and brief.py render raises RenderError on a fresh checkout of this branch. The code is not wrong; the deliverable is not in the diff. Two live conjuncts remain open (conjunct 7: rotate.py:1102, dispatch.py:1365 still call brief.assemble; hook:267 still calls brief.py head) and are phase 2, carried to the next kid. Overage disclosed by the kid: 121 production lines vs a 40 ceiling; answered proceed-with-160 because the size is 4 resolvers + a resolver + a CLI verb in one file, and splitting would fork the render seam mid-phase.
<!-- THOUGHT:END -->

## Agent Notes
Phase 1 built + green: one config cell + brief.py render (head byte-identical across roles, card, harness, trajectory, extras; {{template:}} one level; writes no file). 121 production lines vs 40 ceiling -> rebrief_request recorded; call sites are phase 2.

Phase 1 accepted-with-residue: resolver + render + 7 green tests verified by parent probes; demoted lean_disproved:70 because the one brief config cell is uncommittable by a round own done (cli.py:2094) and absent from the branch diff. rebrief answered: proceed, line_ceiling 160. Phase 2 (three call sites) open.
