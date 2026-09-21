---
id: experiment:a00-66b5e112-residue-fixes
mint_id: e824a60242664029a30c34bf2edb157a
type: experiment
parents:
  - hypothesis:a00-1cbef27c-4bceb5
next_edges: []
edited_by: a00-66b5e112
line_ceiling: 40
loop: goal:g7.31.3.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: d6cab089b0206e6a
season: 2
title: "DT.45 residue fixes: countable fork markers, import-guard wire probe, cli.py:1136 citation"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-66b5e112-residue-fixes

## Round

DT.45 corrective residue round on `goal:g7.31.3.2`. Node-only edits; no
production file touched (`production_lines: 0`). Checkout `a00-bbcb43fa`;
scratch and raw transcript: `.agi/sessions/iter-DT.45/a00-66b5e112/`.

Fixes closed:

1. **Fork claim markers countable** — `hypothesis:a00-1cbef27c-4bceb5` claim
   items `1./2./3.` -> `(1)/(2)/(3)`, so `_claim_conjunct_numbers` counts them.
2. **Probative wire probe** — `hypothesis:a00-37392a90-0d3366` `probes[2]`
   replaced with an import guard; prose restated in that node and in
   `experiment:a00-37392a90-cli-transcript`.
3. **Citation** — `cli.py:1114` -> `cli.py:1136` for `_CLAIM_ITEM_RE`.

## Exact commands and observed output

### Fix 1 — markers now counted

```
$ python3 extensions/agi/bin/write.py hypothesis:a00-1cbef27c-4bceb5 'replace body 10:18 -'   # (1)/(2)/(3)
$ python3 -c "import sys; sys.path.insert(0,'extensions/agi/bin'); from pathlib import Path; import cli; print(cli._claim_conjunct_numbers(Path('.agi/nodes/hypothesis/a00-1cbef27c-4bceb5.md')))"
[1, 2, 3]
```

Pre-fix this printed `[]`.

### Fix 2 — import-guard wire probe (probative)

```
$ python3 -c "import sys,builtins,runpy; sys.argv=['workflow.py','run','review','--dry-run']; _o=builtins.__import__; builtins.__import__=lambda n,*a,**k:(_ for _ in ()).throw(AssertionError('workflow imported '+n)) if (n=='dispatch' or n.startswith('dispatch.')) else _o(n,*a,**k); runpy.run_path('extensions/agi/bin/workflow.py',run_name='__main__')"
[run-key] review
[credential] mint per-run
[dispatch] global-checks :: role=global model=deepseek/deepseek-v4.1-flash effort=medium
[dispatch] review :: role=reviewer model=deepseek/deepseek-v4.1-flash effort=medium
[summary] workflow=review harness=pi stages=2 via dispatch.py kids
exit=0
```

The guard raises `AssertionError` on any `dispatch` import; none happened.
The old probe (`PYTHONPATH=<poison> workflow.py ...`) could not fail because
`workflow.py:72-73` inserts its own directory first on `sys.path`, so the
PYTHONPATH copy could never shadow the real `dispatch.py`.

Static half:

```
$ grep -nE 'import dispatch|from dispatch' extensions/agi/bin/workflow.py
$ echo $?
1
```

### Fix 3 — citation

`sed -n '1136p' extensions/agi/bin/cli.py` prints
`_CLAIM_ITEM_RE = re.compile(r"\(\s*(\d+)\s*\)")`; `:1114` is unrelated code.

## Evidence

- Raw transcript: `.agi/sessions/iter-DT.45/a00-66b5e112/transcript.txt`.
- Probe JSON built by `.agi/sessions/iter-DT.45/a00-66b5e112/build_probes.py`.
- `python3 -m pytest extensions/agi/tests/test_cli.py -q -k "probe or conjunct"`
  (see transcript for the selected-test count).

## Verdict

All three fixes verified on the built bytes; the routing claim is unchanged.
