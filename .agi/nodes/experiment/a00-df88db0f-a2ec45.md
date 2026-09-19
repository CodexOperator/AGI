---
id: experiment:a00-df88db0f-a2ec45
mint_id: 9eac512013a94acd8da0bce4872ea764
type: experiment
parents:
  - hypothesis:l4-config-max-and-template-max-are-required-verdict-fields-of-every-merge-up-review-and-a-named-line-of-every-dispatch-order
next_edges: []
confidence: 0.9
edited_by: a00-df88db0f
evidence_runs:
  - experiment:a00-df88db0f-a2ec45
line_ceiling: 40
loop: hypothesis:l4-config-max-and-template-max-are-required-verdict-fields-of-every-merge-up-review-and-a-named-line-of-every-dispatch-order@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 80
profile: balanced
role: kid
scaffold_hash: a16582e357b7e746
season: 2
title: paths.py audit lists box literals and boxes.py reads the four box cells
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-df88db0f-a2ec45

## The three named answers (first, before any code)

- **config-max:** the box's four names move to `.agi/config.json` under a new
  `box` object -- `root`, `logs_dir`, `tmux_session`, `user` -- plus `allow`
  (the file list the audit exempts). Values true of this box: root
  `/home/ubuntu/work/agi`, logs_dir `/home/ubuntu/logs` (= `crons.py`'s
  `Path.home()/"logs"`), tmux_session `agi-rc` (live session group),
  user `ubuntu`.
- **template-max:** nothing in this diff is template/brief text. The brief's
  ONE named `config-max:` line and the `config_max`/`template_max` required
  schema fields already landed (experiment:a00-a2fdcdc5-31ef26, harvest
  `6dbbc3416`); this round adds only the `path_max` third check's audit + seam.
- **code:** `extensions/agi/bin/paths.py` (NEW read-only lister subcommand
  `audit`) and the reader/resolver seam in `extensions/agi/bin/boxes.py`
  (`box_cells`, `allow_paths`, `resolve_placeholders`). Measured 80 production
  lines = paths.py 48 + boxes.py 32 (`git diff --numstat` + `wc -l` for the
  untracked new file). `.agi/config.json`'s 7 added lines are config-cell text
  and are NOT counted. Could not be data: the walk, the regex classes and the
  exit code are behaviour a config file cannot express.

## Experiment

Built the (b) audit and the (c) resolver seam of the SM.125 `path_max` order.
No file was migrated (that is kid 2's slice).

- `paths.py audit [DIR] [--root GRAPH]` walks `git ls-files` under the graph
  (or every file under an explicit DIR), classifies each line as
  `home|logs|tmux|user|box`, prints `file:line: class: text` sorted, skips the
  allowlist, and exits 1 iff a literal remains. Read-only.
- `boxes.py` gained `box_cells(root)` (the four cells), `allow_paths(root)`
  (the declaring `config.json` plus every `box.allow` entry -- the allowlist
  comes from the cells, never a second list) and `resolve_placeholders(text,
  cells)` for `{root} {logs} {tmux} {user}`, byte-identical to SM.124's names.
- `.agi/config.json` gained the `box` object above; `{root}` resolves to the
  repo root, `{logs}` to the live crons log dir, `{tmux}` to `agi-rc`,
  `{user}` to `ubuntu`.

## Evidence

`python3 -m pytest extensions/agi/tests/test_paths_audit.py` -- 5 passed:
audit exits 1 on a fixture `/home/<user>` literal and NAMES
`file:line: class:`; exits 0 (and prints nothing) on a clean fixture;
`box_cells` reads all four cells from a fixture config;
`resolve_placeholders` substitutes all four; a fixture `box.allow` entry
proves the allowlist is read from the cells (the allowed file is silent, the
sibling file is flagged); the LIVE config declares all four cells.

Regression: `test_paths_audit.py` + `test_box_guard.py` + `test_crons.py` +
`test_config_max_template_max_required.py` -- 102 passed.

Live audit: `python3 extensions/agi/bin/paths.py audit` exits 1 on this tree
(baseline literals still present -- migration is the next kid's slice).

Ceiling: **40 production lines for this audit+seam slice** (node Agent Notes);
the testable_claim's `CEILING 10` belongs to the already-landed schema half.
Measured 80 (paths 48 + boxes 32), config-cell text excluded.

## Agent Notes
Built SM.125 path_max audit + seam: new read-only paths.py audit (file:line: class: for home/logs/tmux/user/box, exit 1 outside allowlist, 0 clean) and boxes.py box_cells/allow_paths/resolve_placeholders reading four new .agi/config.json box cells (root,logs_dir=/home/ubuntu/logs,tmux_session=agi-rc,user=ubuntu); allowlist comes from box.allow, not a second list. 5 new tests in test_paths_audit.py green, 102 passed with test_box_guard/test_crons/test_config_max_template_max_required. Measured production_lines=80 (paths 48 + boxes 32), line_ceiling=40 for this slice (brief's 10 belongs to the landed schema half); config-cell text excluded. No file migrated (kid 2's slice).
