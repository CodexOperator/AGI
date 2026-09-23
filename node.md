---
id: experiment:a00-0b75e6d7-ca53bd
mint_id: cafa4c797a0442cca838912374dcab53
type: experiment
parents:
  - hypothesis:path-and-cron-audits-cover-what-they-declare
next_edges: []
confidence: 0.9
edited_by: a00-d79d90c4
evidence_runs:
  - experiment:a00-0b75e6d7-ca53bd
line_ceiling: 40
loop: hypothesis:path-and-cron-audits-cover-what-they-declare@s2
model: deepseek/deepseek-v4.1-flash
probes: "PROBE-A (wire, conjunct 1): temp git repo, graph at repo/.agi, a /home literal under extensions/agi/bin; paths.files(graph,None) returned the repo-top extensions path and findings reported \"extensions/agi/bin/x.py:1: home\"; locations.repo_root(graph)==repo. Holds. PROBE-B (gate, conjunct 2): graph with ONE unset cell (user) -> paths.findings raised ValueError \"missing box cells: user\", naming only the unset cell; control (all cells set, clean dir) returned []; main() rc==2. Holds. PROBE-C (wire, conjunct 3): a fixture [box].md whose placeholders maps the nonliteral token t->tmux_session drove resolve_placeholders(\"{t}|{r}\") to \"T|R\" and box_cell_names read the schema fields. The changed bytes are live. Holds. PROBE-C2 (edge, caveat only): a graph with NO [box].md now yields box_cells()=={} and findings()==[] (fail-open) -- recorded as caveat, not a refutation (pre-fix findings also returned [] there; the schema is committed)."
production_lines: 26
profile: balanced
role: kid
scaffold_hash: 298d60879ace6a6f
season: 2
title: paths/boxes audits reach the repo top and fail closed by name
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-0b75e6d7-ca53bd

## Experiment

Built the three conjuncts of `hypothesis:path-and-cron-audits-cover-what-they-declare`
that live in the paths/boxes file family. Pre-fix bytes saved to
`.agi/sessions/iter-EF.27/a00-0b75e6d7/{paths,boxes,test_paths_audit}.prefix.py`
(note: the files did not exist at `merge-base 6590c73`, so the pre-fix bytes are
HEAD `1fac7e7`, copied before any edit).

### Conjunct 1 — wire: no-dir audit reaches the repo top

`files(root, None)` ran `git ls-files` with `cwd=root`, and `main()`'s default
`--root` is `<repo>/.agi`; so a bare `paths.py audit` listed only the graph's
own tracked files. Fix: resolve `top = locations.repo_root(root)` and list /
join against that same repo top.

### Conjunct 2 — gate: findings() fails closed by name

`findings()` returned a clean `[]` when a box cell was unset (`cells.get(key) or ""`);
only `main()` refused. Fix: `findings()` raises `ValueError("missing box cells: ...")`
naming every unset cell; `main()` keeps its own pre-check and exit 2, so live
behaviour is unchanged.

### Conjunct 3 — auth/gate: boxes.py reads cells AND placeholders from [box].md

`boxes.py` re-declared `_BOX_CELLS` and `_PLACEHOLDERS`; the placeholder map
existed only as comments in `[box].md`, and `_graph()` wrote no `[box].md`.
Fix: `placeholders:` is now a real frontmatter mapping on
`.agi/context/schemas/[box].md`; `boxes._box_schema()` parses it once;
`box_cell_names()` reads `fields`, `resolve_placeholders(text, cells, root)`
reads the declared map; both literals deleted. `_graph()` now writes the schema
fixture so the existing tests exercise the schema path, not a fallback.

## Evidence

RED on the pre-fix production bytes (4 new tests, full transcript in
`.agi/sessions/iter-EF.27/a00-0b75e6d7/red.txt`):

```
FAILED test_findings_refuses_unset_cells_by_name
  > with pytest.raises(ValueError):
  E Failed: DID NOT RAISE ValueError           # findings() returned [] clean
FAILED test_audit_without_dir_reaches_the_repo_top
  > assert rc == 1, (rc, out)
  E AssertionError: (0, '')                     # no-dir audit saw only .agi/
FAILED test_box_schema_declares_the_placeholder_map
  E AssertionError: {'logs': 'logs_dir', ...}   # placeholders not real fields
FAILED test_resolve_placeholders_follows_the_schema_mapping
  E TypeError: resolve_placeholders() takes 2 positional arguments but 3
4 failed, 9 deselected
```

GREEN on the built bytes:

```
$ python3 -m pytest extensions/agi/tests/test_paths_audit.py -q
13 passed in 0.12s
```

Cross-file coverage (`boxes.py`/`paths.py` consumers):

```
$ python3 -m pytest test_box_guard.py test_send.py test_paths_audit.py -q
349 passed, 11 warnings in 32.74s
```

Live dogfood — the audit now reaches `extensions/agi/bin` (2489 findings there),
which it could not see before:

```
$ python3 extensions/agi/bin/paths.py audit ; echo rc=$?
rc=1   # 13810 findings, 2489 under extensions/agi/bin
```

## Measured production lines

`git diff --numstat` (additions; test file excluded):

```
8	2	.agi/context/schemas/[box].md
11	13	extensions/agi/bin/boxes.py
7	2	extensions/agi/bin/paths.py
```

26 additions total (43 add+del), ceiling 40 — under the 2x stop (80).

## Caveats

- With the literals gone, a graph whose `[box].md` schema is ABSENT yields
  `box_cell_names() == ()`, so `findings()` sees no unset cell and can pass
  silently. That is fail-open in a layout the live repo does not use (its
  schema is committed); naming it here rather than reintroducing a hardcoded
  fallback.
- `resolve_placeholders` now requires `root`; its only callers are tests.

## Agent Notes
paths.py no-dir audit resolves locations.repo_root and lists the repo top; findings() raises naming unset box cells; boxes.py reads cell names + placeholder map from [box].md with _BOX_CELLS/_PLACEHOLDERS deleted. 4 new tests RED pre-fix, 13/13 GREEN post-fix, 349 passed with box_guard+send.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-d79d90c4, tier parent) on the bytes at HEAD b56b1a10f. (1) THE INSTRUCTION SAID: "paths.py audit with no dir lists every tracked repo file (git ls-files from the repo top, not from .agi) ... paths.findings refuses by name when a box cell is unset ... boxes.py reads its cell names and placeholder keys from the [box] schema instead of the literals ... with test_paths_audit.py fixture writing a [box].md". (2) WHAT THE MACHINE DOES: I read the diff (paths.py files() now resolves locations.repo_root(root) and joins git ls-files output against that same top, paths.py:12-14; findings() raises ValueError naming unset cells before the scan, paths.py:27-30; boxes.py drops _BOX_CELLS/_PLACEHOLDERS for _box_schema(root) reading fields and placeholders, boxes.py:20-25,36,52-55; [box].md carries a real placeholders: mapping; _graph() writes the schema fixture) and I BUILT AND RAN three probes. PROBE-A (wire, conjunct 1): temp git repo, graph at repo/.agi, a /home literal in extensions/agi/bin/x.py, paths.files(graph,None) returned the extensions path and findings reported x.py:1: home -- the audit now reaches the repo top. PROBE-B (gate, conjunct 2): config with user unset -> paths.findings raised "missing box cells: user" naming only the unset cell; control all-cells-set on a clean dir returned []; main() still exits 2. PROBE-C (wire, conjunct 3): a schema whose placeholders maps the NONLITERAL token t to tmux_session drove resolve_placeholders to "T|R", and box_cell_names read the schema fields -- the changed bytes are live, not a stub. (3) THE NEAR MISS: leaving findings() fail-closed only in main() satisfies the words while a direct caller still gets a silent [] -- the kid put the refusal in findings() itself, which is the conjunct. (4) CAVEAT (recorded, not demoted): with the literals deleted, a graph whose [box].md is ABSENT yields box_cell_names() empty and box_cells() empty, so findings() returns [] (PROBE-C2). That is fail-open, but not a regression for this conjunct: pre-fix findings() also returned [] on that layout; the schema is committed in this repo and in every engine clone, and the claim explicitly requires the literals gone. VERDICT: all three conjuncts hold; the kid built rather than measured.
<!-- THOUGHT:END -->

kid 1 (a00-0b75e6d7): three paths/boxes conjuncts built and probed -- repo-top no-dir audit, findings() fails closed by name, boxes.py reads cells+placeholders from [box].md. Parent ran PROBE-A/B/C; all hold. One caveat (absent [box].md is fail-open) recorded, not demoted.
