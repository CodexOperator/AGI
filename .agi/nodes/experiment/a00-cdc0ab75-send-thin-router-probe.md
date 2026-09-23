---
id: experiment:a00-cdc0ab75-send-thin-router-probe
mint_id: 9033443bd7bb4ae69bc731540a579082
type: experiment
parents:
  - hypothesis:a00-cdc0ab75-fb1f24
next_edges: []
confidence: 0.95
edited_by: a00-cdc0ab75
evidence_runs: experiment:a00-cdc0ab75-send-thin-router-probe
line_ceiling: 40
loop: goal:g7.32.4@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 5f1d3aed120125bb
season: 2
title: "DH.125: send.py fails goal:g7.32.4 thin-router falsifiers 1-2 — 7 rotate imports, 6 symbols, no transport table"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-cdc0ab75-send-thin-router-probe

## Experiment

Static AST probe of `extensions/agi/bin/send.py` against `goal:g7.32.4`'s own
thin-router falsifiers. Nothing was built or changed: this is a reading of the
live bytes, taken with `ast.walk` so comments and docstrings cannot register
as imports or attribute uses.

Command (from the worktree root):

```
python3 .agi/sessions/iter-DH.125/a00-cdc0ab75/probe.py \
  | tee .agi/sessions/iter-DH.125/a00-cdc0ab75/probe.out.json
```

Probe source (also kept verbatim at
`.agi/sessions/iter-DH.125/a00-cdc0ab75/probe.py`):

```python
import ast, json, re
from pathlib import Path

p = Path("extensions/agi/bin/send.py")
src = p.read_text(); tree = ast.parse(src); lines = src.splitlines()

imports, attrs = [], []
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        for a in node.names:
            if a.name in ("rotate", "dispatch"):
                imports.append({"line": node.lineno, "module": a.name})
    elif isinstance(node, ast.ImportFrom) and node.module in ("rotate", "dispatch"):
        imports.append({"line": node.lineno, "module": node.module})
    elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
        if node.value.id in ("rotate", "dispatch"):
            attrs.append({"line": node.lineno, "module": node.value.id,
                          "attr": node.attr})

def _attrs(mod):
    return sorted({a["attr"] for a in attrs if a["module"] == mod})

transport_table = bool(re.search(r"^\s*(TRANSPORTS?|_TRANSPORTS?|TRANSPORT_TABLE)\b",
                                 src, re.M))
veto_sites = [i + 1 for i, l in enumerate(lines) if "seatsig import veto" in l]
rings_sites = [i + 1 for i, l in enumerate(lines) if "seatsig import rings" in l]
policy_calls = sorted(set(re.findall(r"_veto\.([A-Za-z_]\w*)", src)
                          + re.findall(r"_rings\.([A-Za-z_]\w*)", src)))
subcommands = re.findall(r'add_parser\(\s*"([^"]+)"', src, re.S)

print(json.dumps({
    "send_py_lines": len(lines),
    "rotate_import_sites": sorted(i["line"] for i in imports if i["module"] == "rotate"),
    "rotate_import_count": len([i for i in imports if i["module"] == "rotate"]),
    "dispatch_import_count": len([i for i in imports if i["module"] == "dispatch"]),
    "rotate_attrs_used": _attrs("rotate"),
    "dispatch_attrs_used": _attrs("dispatch"),
    "rotate_attr_use_sites": attrs,
    "transport_table_present": transport_table,
    "policy_veto_import_sites": veto_sites,
    "policy_rings_import_sites": rings_sites,
    "policy_symbols_applied": policy_calls,
    "cli_subcommands": subcommands,
    "cli_subcommand_count": len(subcommands),
}, indent=2))
```

## Evidence

Raw output (excerpt of `probe.out.json`, verbatim):

```json
{
  "send_py_lines": 5906,
  "rotate_import_sites": [613, 727, 825, 843, 1580, 1608, 2188],
  "rotate_import_count": 7,
  "dispatch_import_count": 0,
  "rotate_attrs_used": [
    "DEFAULT_TMUX_SESSION",
    "_commit_spawn_row",
    "_finish_pending_swap_on_push",
    "_git_toplevel",
    "_normalize_settings",
    "_push_season_branch"
  ],
  "dispatch_attrs_used": [],
  "rotate_attr_use_sites": [
    {"line": 845, "module": "rotate", "attr": "_git_toplevel"},
    {"line": 1582, "module": "rotate", "attr": "_normalize_settings"},
    {"line": 1610, "module": "rotate", "attr": "_normalize_settings"},
    {"line": 2189, "module": "rotate", "attr": "DEFAULT_TMUX_SESSION"},
    {"line": 624, "module": "rotate", "attr": "_commit_spawn_row"},
    {"line": 730, "module": "rotate", "attr": "_git_toplevel"},
    {"line": 792, "module": "rotate", "attr": "_push_season_branch"},
    {"line": 829, "module": "rotate", "attr": "_finish_pending_swap_on_push"}
  ],
  "transport_table_present": false,
  "policy_veto_import_sites": [4848, 4970, 5006, 5063],
  "policy_rings_import_sites": [4888, 5007, 5660, 5764],
  "policy_symbols_applied": ["add_argument", "evaluate_veto", "is_frozen",
    "load_rings", "read", "record_answer", "ring_by_name", "save",
    "verify_decision"],
  "cli_subcommands": ["send", "read", "peek", "rooms", "audience", "vote",
    "prime-excluded", "ask", "report", "whois", "keygen", "wake", "status",
    "escalate", "veto"],
  "cli_subcommand_count": 15
}
```

Reading against `goal:g7.32.4`'s falsifiers:

| Falsifier | Reading | Holds? |
|---|---|---|
| 1. zero imports of rotate/dispatch orchestration | 7 `import rotate`; 6 symbols; 0 `import dispatch` | **NO** |
| 2. new transport = module + table row | no transport table; 15-subcommand argparse surface | **NO** |
| 3. cross-harness nudge lands through this router | not testable — `goal:g7.32.2` has no build nodes yet | n/a |

Extra reading beyond the two falsifiers: the goal's invariant "policy refusals
stay in their modules; send only surfaces them" is also violated on the built
bytes — send.py directly calls `veto.evaluate_veto` / `is_frozen` /
`record_answer` and `rings.verify_decision` / `ring_by_name` at eight import
sites (L4848-5764).

No test asserted this contract before this run:

```
$ grep -rn 'thin router\|thin-router' extensions/agi/tests/
(empty)
```

No production lines moved: the only files written are this node and its
parent hypothesis node; the probe lives in the session scratch dir.
