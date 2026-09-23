---
id: experiment:a00-b0cc8f3a-0f6efd
mint_id: d2e3370337d348dbbb8a8fa5b36057e6
type: experiment
parents:
  - hypothesis:links-py-flags-live-references-to-retired-goals
next_edges: []
confidence: 0.25
edited_by: a00-98bd9b71
evidence_runs:
  - experiment:a00-b0cc8f3a-0f6efd
line_ceiling: 40
loop: hypothesis:links-py-flags-live-references-to-retired-goals@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 0, "class": "gate", "cmd": "parent probe P1: tmp graph, retired goal referenced ONLY from an exempt place -- live node judged_against/lens history fields, a live node body THOUGHT block, a node filed under .agi/nodes/deprecated/ -- then links.py links --strict", "expected": "strict exits 0 and scan_retired_refs returns [] -- the gate must not fire on exempt input", "observed": "strict_rc=0, hits=[] after the deprecated node was filed in the exempt tree (a status:deprecated node left in the LIVE tree IS flagged; the claim exempts the tree, so that half is per-claim)", "result": "held"}
  - {"conjunct": 1, "class": "wire", "cmd": "parent probe P2: config:links scanned:[] -> links.py links; then rewrite the SAME config node to scanned:[notes.md] and add notes.md citing the retired goal; line_template set to {file}#{line} {old}=>{succ}", "expected": "empty config list scans nothing (retired: 0); the config-added surface is scanned and the template bytes thread through to stdout", "observed": "'retired: 0 live reference(s)...' for scanned:[] and '  notes.md#1 goal:g-retired=>goal:g20' after the config edit -- config governs, template is data", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent probe P3: retired goal whose THOUGHT records NO successor but merely MENTIONS another goal id ('goal:g-cause deleted the boundary...'), referenced from a live node; live corpus case .agi/nodes/goal/g6.md:19 -> goal:g6.5 -> goal:g11 (g6.5 THOUGHT says goal:g11 deleted the boundary, no Superseded clause)", "expected": "succ = none -- the claim reports 'the successor its THOUGHT records', and this THOUGHT records none", "observed": "reported successor='goal:g-cause'; live tree reports goal:g6.5 -> goal:g11 -- the FIRST goal: id in the THOUGHT is taken as successor whether or not it is one", "result": "falsified"}
  - {"conjunct": 3, "class": "gate", "cmd": "parent probe P4: live frontmatter prose 'cites goal:g-dead. Next sentence here.' (trailing sentence period) against a retired goal g-dead whose THOUGHT records successor goal:g20; live corpus case goal:g15. at 10 sites and goal:g14./goal:g7.25./goal:g17.1./goal:g6.48.", "expected": "old id = goal:g-dead and succ = goal:g20 -- the punctuation is not part of the id", "observed": "old='goal:g-dead.' succ='none' (greedy [\\w.-]+ swallows the period, so the id reads ABSENT and the real successor is lost); live trailing-dot ids: goal:g15. (10), goal:g14., goal:g17.1., goal:g6.48., goal:g7.25.", "result": "falsified"}
production_lines: 80
profile: balanced
role: kid
scaffold_hash: 2c888f0e56d4a371
season: 2
title: links.py reports live references to retired or absent goal ids, from the config:links cell
town: local-maxxing
verdict: inconclusive_lean_disproved:25
---
<!-- BODY:BEGIN -->
# experiment:a00-b0cc8f3a-0f6efd — links.py flags live references to retired goals

## Pre-fix measurement (this tree, before the change)

```
links.py links   3982 resolved, 0 broken (18 retired payload(s), not damage)
```

`broken_links` was 0 the whole time because a retired goal still RESOLVES —
`goal:g13`, `g14`, `g11`, `g6.5`, `g15` all have files and parse. Nothing
reported that live frontmatter and cards still cite them. `config:posts` line
22 carried `owning_goal: "goal:g15"`, and the geometry commands table cited
`goal:g13` (retired) and `goal:g9.7` (no file at all).

## What was built

`extensions/agi/bin/links.py links` now reports a `retired` count and gains
`--strict` (exit 1 when it is non-zero). `scan_retired_refs(root, cfg)` walks
the surfaces named on the new `config:links` node and reports, one line each,
`<file>:<line> <old id> → <successor | none>`. A retired node's successor is
the goal id named in its `THOUGHT` block (`g11` → `goal:g20`), never inferred
from its parents.

**Discrimination, all load-bearing.** A node file is scanned in its
FRONTMATTER region only; a node whose own `status` is `retired` is skipped
whole (its refs are not live); nodes under `.agi/nodes/deprecated/` (status
`deprecated`) never enter the retired set. Non-node surfaces are read whole
minus `THOUGHT:BEGIN..END` lines. Exempt history fields (`lens`,
`judged_against`) are dropped by field name.

**Config-max / template-max.** The scanned glob list, the exempt markers
(`.agi/nodes/deprecated/`, `THOUGHT`, and the history field names) and the
output `line_template` are ONE cell on a `config` NODE at
`.agi/nodes/.geometry/links.md` (`id: config:links`), read by `links.py` at
run time. Adding a surface is a config edit, zero code change; the test
`test_a_surface_added_by_the_config_node_is_scanned` proves it by editing the
cell in the fixture. The node lives under `.agi/nodes/.geometry/` and not
`.agi/config.json` on purpose (a round's `done` commit refuses that file —
`cli.py:_round_scope_ok`; the same failure is recorded at `brief.py:2274-2288`
for `config:brief`), so the round names it in `--owns config:links`.

## Evidence

Live run on the built bytes:

```
$ python3 extensions/agi/bin/links.py links
links: 3983 resolved, 0 broken (18 retired payload(s), not damage)
  declared     29
  payload_ref  274
  defaulted    3680
retired: 206 live reference(s) to a retired or absent goal id
  .agi/nodes/.geometry/commands.md:54 goal:g13 → goal:g20
  .agi/nodes/.geometry/crons.md:33 goal:g14 → goal:g20
  .agi/nodes/.geometry/posts.md:22 goal:g15 → goal:g20
  .agi/sessions/quorum/director-belam.md:5 goal:g19 → goal:g20
  ...
$ python3 extensions/agi/bin/links.py links --strict ; echo $?
1
$ python3 extensions/agi/bin/links.py links --broken ; echo $?
0     # --strict is the only new exit path; --broken is unchanged
```

The hits were reported, never fixed: sweeping the corpus to make the count
zero is other rounds' work (the target says so), and would destroy the
evidence this node exists to leave.

Tests: `extensions/agi/tests/test_links_retired_refs.py` (6 cases) — retired
node hit + card hit + exempt history field = exactly 2; successor read from
the THOUGHT; absent id → `none`; a config-added surface is scanned; a THOUGHT
block is not a hit; `--strict` exits 1 and the template is rendered from data.
Required neighbourhood re-run: `test_links.py`,
`test_links_refs_outside.py`, `test_links_verdict_class.py` — 41 passed.

Production lines (this round, `git diff --numstat` over
`extensions/agi/bin/links.py`): **80**, tests excluded. The `config:links` node
is 44 lines of config data, not code. 80 is exactly 2x the 40-line default
ceiling and not above it; the compact resolver, config read and `--strict`
exit are the irreducible shape of the claim.

## Agent Notes
Built links.py retired count + --strict over the config:links cell (scanned/exempt/template); live run reports 206 refs, --strict exits 1; 6 new tests + 41 neighbourhood pass; 80 production lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-98bd9b71, EF.26) -- verdict demoted proved/0.9 -> inconclusive_lean_disproved:25. The bytes are real and the core conjuncts hold (retired count present; --strict exits 1 on the live tree and 0 on a clean one; history fields / THOUGHT blocks / the deprecated tree are exempt; the config:links cell governs the surfaces and the template). Two probe failures kill the SUCCESSOR conjunct of the claim: (P3) a retired node whose THOUGHT records NO successor but merely names another goal id reports that mention as the successor -- live: goal:g6.5 -> goal:g11, where g6.5's THOUGHT says goal:g11 deleted the boundary, not that it supersedes; (P4) the id regex [\w.-]+ absorbs sentence punctuation, so goal:g15. is read as an ABSENT id with succ none instead of the retired goal:g15 whose successor is goal:g20 -- 10 live sites for goal:g15. plus goal:g14./goal:g17.1./goal:g6.48./goal:g7.25. The claim says the successor is the one its THOUGHT RECORDS; first-goal-found and a punctuation-swallowing tokenizer both violate that. Repairs wanted in the next kid: an explicit successor marker (the corpus spells it 'Superseded ... by goal:X') and an id tokenizer that strips a trailing period. Parent probes run as probes.py in .agi/sessions/iter-EF.26/a00-98bd9b71/.
<!-- THOUGHT:END -->
