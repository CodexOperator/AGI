---
id: hypothesis:a00-6c0fde58-e25ca1
mint_id: 0e17c5941a5f42c89618c4f04892019c
type: hypothesis
parents:
  - goal:g7.33.14
next_edges: []
confidence: 0.75
edited_by: a00-3b546363
evidence_runs:
  - hypothesis:a00-6c0fde58-e25ca1
loop: goal:g7.33.14@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 01748ade4a94c628
season: 2
testable_claim: paths.classify returns [] for a line carrying this box root (/data/work/agi) or its real logs_dir, while returning box/logs/user hits for the committed foreign cells; disproved if findings() has a second gate that already flags a local root literal
title: paths audit classifies on the committed cells, so it is blind to this box and loud on a foreign one
town: core
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# hypothesis:a00-6c0fde58-e25ca1

## Claim (testable)

`extensions/agi/bin/paths.py`'s per-box audit is **keyed on the committed
`box` cells, so it is structurally blind to the literals of the box it runs
on and loud only on the literals of whichever box the shared `config.json`
names**. The committed cells name a foreign box (`/home/ubuntu/work/agi`,
user `ubuntu`); this box is `belam` at `/data/work/agi`. Therefore the audit's
`box` / `logs` / `user` / `tmux` classes fire on the wrong truth and cannot
fire on this box's.

**Would prove it:** `paths.classify` returns `[]` for a line carrying this
box's real root or its real logs dir, while returning a hit for the committed
foreign values; and `paths.py audit`'s whole output is explained by the
foreign cells alone.

**Would disprove it:** any second gate in `findings()` (the allow list, a
`HOME_RE` catch-all, a different cell source) that already flags a this-box
root literal, or a `cells_for_this_box`-style overlay already in the tree.

## MEASURED — this box, 2026-09-25, agent a00-6c0fde58

Cells as committed (`.agi/config.json`, identical in the main checkout):

```
box: {root: /home/ubuntu/work/agi, logs_dir: /home/ubuntu/logs,
      tmux_session: agi-rc, user: ubuntu, allow: []}
this box: whoami=belam  HOME=/home/belam  root=/data/work/agi
```

`paths.classify` (`paths.py:18-24`) with those live cells:

| line | classes |
|---|---|
| `ROOT = "/data/work/agi"` | **`[]`** |
| `logs live in /data/work/agi/logs` | **`[]`** |
| `ROOT = "/home/ubuntu/work/agi"` | `home, user, box` |
| `user: ubuntu` | `user` |
| `LOGS=/home/ubuntu/logs` | `home, logs, user` |
| `HOME=/home/belam` | `home` |

The `box` class is a regex on the cell VALUE (`re.escape(v)` against the
line), so a foreign cell value cannot match a local literal by construction.
`HOME_RE` catches anything under a home directory — which is why the box is not
*totally* dark, only dark: `/data/work/agi` has no home component, so this
box's root and logs dir are the two cells with **no** fallback class at all.

`paths.py audit` over the tree, by class:

```
5904 home   4800 user   2751 box   1074 tmux   19 logs   (0 this-box)
```

14,548 hits, every one of them explained by the foreign cells. And the
complementary check: `grep -rl /data/work/agi extensions/ skills/ .claude/`
(excluding `__pycache__`) returns **nothing** — so the `box` class has never
once fired on a real hit in this tree. It is pure noise keyed to another
machine, and the noise is what buries the signal.

## The design consequence (a lean, not a proof)

The tempting one-line repair — make `boxes.box_cells()` prefer the running
box's truth — is **wrong for the wrong reason, and the engine already says
so**. `crons.py:477-481` states it in a docstring and then does not use
`box_cells` at all: it computes `{root}` / `{logs_dir}` from what the
renderers already computed, "never `boxes.box_cells(root)`, whose live cells
belong to a foreign box". So the distrust is already encoded once, in prose,
in one call site.

Readers of the cells, complete (measured by grep over `extensions/`):

| reader | what it wants the cell to be |
|---|---|
| `paths.py:26`, `paths.py:50` (this node's subject) | **this** box's truth — a classifier |
| `unify.py:413` `_real_repos` | the *other* box's real repo, a thing to forbid — it already adds git's own answer (`_git_common_root()`), so a repair would only ADD a path to the forbidden set, never break it |
| `allow_paths` (`boxes.py:85`) | policy, not a location — must not be "repaired" |
| `crons.py:492` | already bypasses `box_cells` |

So the shape that follows is a **second** named reader,
`boxes.cells_for_this_box(root)` = committed cells overlaid with the running
box's own `root` / `logs_dir` / `user`, adopted by `paths.py` at its two call
sites and nothing else — rather than a rewrite of `box_cells`, which would
silently change what `unify`'s guard forbids. This is a design lean at ~70%,
not a measurement: nothing here proves the overlay is the right seam, only
that the current one is measurably blind.

## The cheap first step this names

A test asserting `classify` flags this box's root under `cells_for_this_box`
is a 3-line test in `test_paths_audit.py` and fails today. The 14,548-hit
noise needs a `--quiet`/exit-code contract before the audit can be trusted as
a gate at all; that is a second node, not this one.

## Falsifier for this node

1. `python3 -c` over `paths.classify` with this box's real root → `[]`
   reproduces (it did, 2026-09-25).
2. `grep -rl /data/work/agi extensions/ skills/ .claude/` (no `__pycache__`)
   → 0 hits, so the `box` class has no true positive to find here.
3. Disproof would be a second gate in `findings()` I did not find, or an
   existing `cells_for_this_box` in the tree. Grep found neither.

## Agent Notes
MEASURED: paths.classify keys on committed box cells, so it returns [] for this box's root/logs_dir and fires only on the foreign ubuntu cells (audit: 14548 hits, 0 this-box); names boxes.cells_for_this_box as the reader to adopt, not a box_cells rewrite.

## Agent Notes
backfilled testable_claim; measurement stands

PARENT PROBES (a00-3b546363, DH.365, run by me against the BYTES, not the result file).

PROBE 1 (gate, REPRODUCES the claim). I rebuilt the cells the way paths.py main() does (root = the .agi dir, which is what box_schema_path expects) and re-ran classify by hand:
  classify('ROOT = "/data/work/agi"')            -> []
  classify('REPO=/data/work/agi')                  -> []
  classify('cd /data/work/agi && true')            -> []
  classify('x=Path("/data/work/agi/extensions")') -> []
  classify('REPO = "/home/ubuntu/work/agi"')      -> ['home','box','user','box']
  classify('LOGS=/home/ubuntu/logs')               -> ['home','logs','user']
  classify('user: ubuntu')                         -> ['user']
  classify('tmux: agi-rc')                         -> ['tmux']
The claim holds. The disprover clause is also answered: findings() has NO second gate that catches a local root, and boxes has no cells_for_this_box (hasattr -> False).

PROBE 2 (wire) -- THE FINDING THAT WEAKENS THIS NODE. Nothing calls the audit. grep for paths.findings / 'paths.py audit' / 'import paths' across extensions/ and .claude/ returns hits ONLY in extensions/agi/tests/test_paths_audit.py (lines 126, 131, 230). No engine module, no hook, no dispatch path, no loop step invokes it. So the classifier being blind is currently OBSERVABLE IN NOTHING: the 14.5k hits are printed to whoever types the command by hand and are read by no gate. The node's 'cheap first step this names' (a 3-line classify test) therefore certifies a function no production caller reaches.

PROBE 3 (auth -- the live defect, and it is mine, in MY file scope). boxes.box_cells() is documented 'the box cells true of this box' and boxes.py:_box reads (root)/config.json. Handed a REPO root -- which is exactly what the root CELL names, a repo root, not a graph root -- it returns {} SILENTLY:
  box_schema_path('/data/work/agi/.agi/worktrees/a00-3b546363') -> .../context/schemas/[box].md  is_file()=False
  box_cells(that repo root) -> {}
  box_cells(Path('.agi'))    -> {'root': '/home/ubuntu/work/agi', 'logs_dir': '/home/ubuntu/logs', 'tmux_session': 'agi-rc', 'user': 'ubuntu'}
So the SAME audit, from the SAME tree, is 14568 home-only hits from a repo root and the full class set from a graph root, and nothing anywhere says which root the argument wants. This directly contradicts the doctrine three functions below in the same file (boxes.py:110-114): 'which this caller supplied EMPTY -- an empty render is the bug this resolver exists to prevent'. box_cells IS that empty render, and it returns {} instead of refusing by name.
NEAR MISS this beats: 'the audit is keyed on the committed cells, so it is blind to this box' is true only for the graph-root call. A one-line fix that overlays this-box truth into box_cells would, from a repo-root call, still classify NOTHING -- the overlay would be written into a dict that is then discarded by the empty class list.

PROBE 4 (small, real). classify() returns 'box' TWICE for a foreign root -- ['home','box','user','box'] -- because the classes loop (paths.py:20) adds box for key 'root' and the tail (paths.py:24) adds it again on the same cells.get('root'). A lister that double-reports its own primary class is a lister nobody can count hits from.

VERDICT: the claim as stated is supported and its stated disprover is refuted, but the node is carried on a self-cited evidence_runs (a hypothesis citing itself; the citation rule is an EXPERIMENT's privilege) and the fix it sketches is aimed at a caller that does not exist. Kept as a lean, not promoted to proved.
