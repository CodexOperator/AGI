---
id: experiment:a00-5798cb0f-5efc3a
mint_id: 0da2b0e9ad0f4137bab5faa8bfa6603a
type: experiment
parents:
  - hypothesis:l4-config-max-and-template-max-are-required-verdict-fields-of-every-merge-up-review-and-a-named-line-of-every-dispatch-order
next_edges: []
confidence: 0.9
edited_by: a00-fa1b89d2
evidence_runs:
  - experiment:a00-5798cb0f-5efc3a
line_ceiling: 10
loop: hypothesis:l4-config-max-and-template-max-are-required-verdict-fields-of-every-merge-up-review-and-a-named-line-of-every-dispatch-order@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "re-run the parent's original falsifier against the fixed bytes: fixture [box].md declaring fields root,logs,tmux_session,user, config box.logs='/srv/x/logs', literal '/srv/x/logs/a.log'", "expected": "the declared cell's literal is REPORTED (rc 1, class logs) -- the class must never go dark behind a disagreeing declaration", "observed": "rc=1, '<src>/a.py:1: logs: log = /srv/x/logs/a.log'", "result": "PASS"}
  - {"conjunct": 1, "class": "wire", "cmd": "live-declaration regression: schema fields root,logs_dir,tmux_session,user; literals for logs_dir / tmux_session / user", "expected": "logs_dir -> class logs, tmux_session -> class tmux, user -> class user; embedded substring '/srv/x/logs2' NOT flagged", "observed": "rc=1 logs; rc=1 tmux; rc=1 user; '/srv/x/logs2' rc=0", "result": "PASS"}
  - {"conjunct": 1, "class": "wire", "cmd": "declared cell name containing no underscore ('logs'), literal matching", "expected": "class label derived from the whole key ('logs'), still reported", "observed": "rc=1, class logs", "result": "PASS"}
  - {"conjunct": 1, "class": "gate", "cmd": "divergent declaration with NO config cells, literal present", "expected": "fail-closed gate still refuses (rc 2), naming the declared keys", "observed": "rc=2, 'missing box cells: logs, root, tmux_session, user'", "result": "PASS"}
  - {"conjunct": 1, "class": "wire", "cmd": "python3 bin/paths.py audit --root <live .agi>", "expected": "live baseline unchanged, rc 1", "observed": "rc=1, 10763 findings", "result": "PASS"}
  - {"conjunct": 1, "class": "auth", "cmd": "library-boundary probe: paths.findings(graph with box:{}, src with a tmux literal) called directly, bypassing main()", "expected": "the audit's engine should not report clean silently either", "observed": "returns [] -- the fail-closed exit-2 gate lives only in main(), so a direct findings() caller (no live caller today; the planned standing-suite gate would have to route through main()) still sees a silent clean pass", "result": "RESIDUE -- not a falsifier of this kid's narrow claim (no current caller), recorded for the standing-gate slice"}
production_lines: 4
profile: balanced
role: kid
scaffold_hash: 8cfe02367010c237
season: 2
title: paths.py audit derives its class names from [box].md, never a second literal list
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-5798cb0f-5efc3a

## Experiment

SM.125 slice 3 follow-up, residue 3b: the classifier's cell names were a
SECOND hardcoded list. `boxes.py` was migrated to read cell names from
`context/schemas/[box].md`, but `paths.py` `classify()` still carried
`(("logs","logs_dir"),("tmux","tmux_session"),("user","user"))`. A declaration
naming the cell `logs` (not `logs_dir`) set the fail-closed gate with that
name, then went silent in the classifier: rc 0, clean, with the declared
cell's literal right there on the line.

**Pre-fix probe F (red, measured before the change):** a fixture graph whose
`[box].md` declares `logs`, `config.json` box has `logs: /srv/x/logs`, and
`src/a.py` contains `log = '/srv/x/logs/a.log'` returned **rc=0, empty output**
-- the exact silent-clean failure slice 3 existed to kill. Reproduced in the
new test before the fix (failed `assert 0 == 1`).

**Fix (built, then proved):** `findings()` now builds the classifier's pairs
from the one declaration:

```python
classes = [(k.split("_")[0], k) for k in boxes.box_cell_names(root) if k != "root"]
```

and passes them to `classify(line, cells, classes)`, which iterates `classes`.
No cell-key literal list remains in paths.py; the label is derived from the
declared key's head word (`logs_dir`->`logs`, `tmux_session`->`tmux`,
`user`->`user`). `root` stays the separate `box` substring check, and the
fail-closed exit 2 plus the boundary regex are untouched.

Production diff: 4 added / 3 removed lines in `extensions/agi/bin/paths.py`
(`git diff --numstat`), under the 10-line ceiling.

## Evidence

**1. Red first -- new test failed against the pre-fix bytes:**

```
E       AssertionError: (0, '')
E       assert 0 == 1
test_paths_audit.py::test_declared_cell_name_drives_the_classifier
1 failed, 8 passed in 0.14s
```

**2. Green after the fix -- the three named files:**

```
python3 -m pytest extensions/agi/tests/test_paths_audit.py \
  extensions/agi/tests/test_box_guard.py \
  extensions/agi/tests/test_config_max_template_max_required.py -q
22 passed in 1.96s
```

(was 21 passed / 8 in paths_audit; the new case is the +1.)

**3. Probe F by hand after the fix** -- fixture graph declaring `logs`, all
four cells set, three matching literals:

```
$ python3 extensions/agi/bin/paths.py audit <src> --root <graph>
src/a.py:1: logs: log = '/srv/x/logs/a.log'
src/a.py:2: tmux: t = 'box-session'
src/a.py:3: user: u = 'boxuser'
rc=1
```

Non-zero, and it names each finding's class. The declaration drives the
classifier.

**4. No regression on the probed-correct halves:**

- `test_unset_cells_refuse_a_clean_pass` still green -- unset declared cell
  exits 2 and names the missing cells.
- `test_path_shaped_logs_dir_literal_is_caught` still green -- the
  path-shaped cell + boundary regex still reports `logs`.
- `python3 extensions/agi/bin/paths.py audit --root .agi` on the live tree:
  `rc=1` (baseline literals not migrated; a later slice).

**Caveats.** The label is the declared key's head word (`split("_")[0]`). A
future declaration whose class label is not the head of its key (e.g. a cell
`log_directory` wanting label `logs`) would take the key itself as the label
rather than a wrong one -- acceptable per the brief's single-map allowance,
but it is a derivation rule, not a declared mapping. The live `[box].md`
four names classify exactly as before.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-fa1b89d2, iter 141): ACCEPTED, verdict proved.

(1) WHAT THE BRIEF SAID: "Make extensions/agi/bin/paths.py derive the cell
names it classifies from the same declaration boxes.py reads -- no second
literal list of cell key names in paths.py. The schema's declared key set must
DRIVE the classifier, so a declaration and the code can never disagree about
which names exist."

(2) WHAT THE BYTES DO: findings() now builds
    classes = [(k.split("_")[0], k) for k in boxes.box_cell_names(root) if k != "root"]
(paths.py:25) and classify() iterates that list (paths.py:15-19). The only
surviving literal in paths.py is the class LABEL derivation, not the name set:
the names come from box_cell_names(), which reads context/schemas/[box].md.
I re-ran the parent's own falsifier by hand against these bytes -- a fixture
whose [box].md declares `logs` (not `logs_dir`) with the cell set and the
literal '/srv/x/logs/a.log' now exits 1 and names class `logs` (was rc 0,
silent, on the previous version). Live names regression is byte-for-byte the
old behaviour: logs_dir->logs, tmux_session->tmux, user->user, and the
embedded-substring case '/srv/x/logs2' is still refused. The fail-closed exit 2
survives a divergent declaration (names the declared keys).

(3) THE NEAR MISS: a fix that keeps a hardcoded
(("logs","logs_dir"),...) tuple for the live schema and merely ADDS a schema
read for the divergent case satisfies the words and leaves the exact
disagreement this slice exists to kill -- the gate keyed on the declaration,
the classifier keyed on code. This version avoids it by making the declaration
the source of the name SET, and the code contributes only the label transform.

(4) DEVIATION FROM A STANDING RULE: none. Scope is 4 production lines in
paths.py + 21 test lines, under the 10-line ceiling I set on the node before
the spawn.

RESIDUE (recorded as an `auth` probe, not a falsifier): paths.findings() called
as a library -- bypassing main() -- still returns [] silently when the box
cells are unset, because the exit-2 gate lives only in main(). There is NO live
caller today (only tests import paths), and the planned "audit run in the suite
= the standing gate" routes through main() as every existing test does, which is
why this is a note for that slice and not a demotion of this claim. The big
un-delivered piece remains the migration of the measured baseline (10763 live
findings) to the seam, which both briefs explicitly deferred.
<!-- THOUGHT:END -->

## Agent Notes
paths.py classify() now derives its cell keys from boxes.box_cell_names([box].md); pre-fix probe F returned rc=0 on a schema declaring 'logs', post-fix rc=1 naming logs/tmux/user, 4 production lines, 22 tests green
