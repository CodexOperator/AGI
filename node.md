---
id: mvp:zoom-runtime-contract
mint_id: 77a49bc9337f4f5cb4f46c0429621db5
type: mvp
parents:
  - goal:s8
confidence: 0.95
edited_by: season.py
evidence_runs: []
season: 1
subgraph: false
tags:
  - s8
  - zoom
thought_session: season
title: Runtime-aware completion contract in zoom.py
---
## Sites found

**Three locations emit the completion block:**

1. **Line 374** (inside `_compose_big` return f-string): The big-level (whole-graph) completion block with verdict/confidence/node-id/notes
2. **Line 427** (inside `_compose_small` function, building lines list): The small-level (legacy 2-hop) completion block
3. **Line 528** (inside `_render_level` function, building lines list): The numeric-level (1-3) completion block

## The change, as applicable code

### 1. Add `--runtime` argument to argparse in `main()` (after line 287)

**Current (lines 272-288):**
```python
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project_root")
    ap.add_argument("iter_n", type=int)
    ap.add_argument("agent_id")
    ap.add_argument(
        "--level",
        choices=["1", "2", "3", "4", "5", "big", "small"],
        required=True,
    )
    ap.add_argument(
        "--target",
        default=None,
        help="node id. Bounds the subtree at levels 1-3 (optional there); "
             "required for legacy --level small; ignored by big/4/5.",
    )
    args = ap.parse_args()
```

**Replace with:**
```python
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project_root")
    ap.add_argument("iter_n", type=int)
    ap.add_argument("agent_id")
    ap.add_argument(
        "--level",
        choices=["1", "2", "3", "4", "5", "big", "small"],
        required=True,
    )
    ap.add_argument(
        "--target",
        default=None,
        help="node id. Bounds the subtree at levels 1-3 (optional there); "
             "required for legacy --level small; ignored by big/4/5.",
    )
    ap.add_argument(
        "--runtime",
        choices=["pi", "cc"],
        default=None,
        help="Runtime dispatch mode: 'pi' for pi-runtime dispatch, 'cc' for Claude Code. "
             "If not specified, defaults to 'cc' if config has cc_dispatch key, else 'pi'.",
    )
    args = ap.parse_args()
```

### 2. Add runtime defaulting logic in `main()` (after line 288, before line 290)

**Current (line 288-290):**
```python
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
```

**Replace with:**
```python
    args = ap.parse_args()

    # Default runtime based on config
    if args.runtime is None:
        root_for_config = Path(args.project_root).resolve()
        cfg_path = config_path(root_for_config)
        if cfg_path is not None:
            try:
                cfg = json.loads(cfg_path.read_text())
                args.runtime = "cc" if "cc_dispatch" in cfg else "pi"
            except Exception:
                args.runtime = "pi"
        else:
            args.runtime = "pi"
    else:
        root_for_config = None

    root = Path(args.project_root).resolve()
```

### 3. Add the shared helper function (insert before `_compose_big` function, around line 359)

```python
def _completion_block(
    runtime: str,
    iter_n: int,
    agent_id: str,
    verdict: str = "<verdict_state>",
    confidence: str = "<0.0-1.0>",
    node_id_expr: str = "<new_or_extended_node_id>",
    notes: str = "<one-line>",
) -> str:
    """Generate the completion contract block for either pi or cc runtime.
    
    When runtime is 'pi', emits the cli.py done command.
    When runtime is 'cc', emits the DONE report format.
    """
    if runtime == "cc":
        return (
            f"DONE iter-{iter_n:03d}/{agent_id}\n"
            f"caveats: <optional, one line>\n"
            f"struggles: <optional, one line>\n"
            f"\n"
            f"Do not commit. Do not push. Do not call cli.py. The parent reviews your\n"
            f"node and owns all git."
        )
    else:  # pi
        return (
            f"python3 <plugin>/bin/cli.py done {iter_n} {agent_id} \\\n"
            f"  --verdict {verdict} --confidence {confidence} \\\n"
            f"  --node-id {node_id_expr} \\\n"
            f'  --notes "{notes}"'
        )
```

### 4. Update `_compose_big` to use the helper (lines 359-382)

**Current:**
```python
def _compose_big(inject_text: str, args: argparse.Namespace) -> str:
    return f"""# autoresearch-tree iteration {args.iter_n} — agent {args.agent_id}

## Zoom Level: BIG (legacy alias for numeric level {LEGACY_LEVEL_MAP['big']} — {LEVEL_INFO[LEGACY_LEVEL_MAP['big']]['name']})
You are exploring the WHOLE graph. Pick a high-level idea or new chain to extend.
Bias: introduce a fresh idea, fork an under-explored chain, or seed a new domain.

{inject_text}

## Your Task
1. Decide: extend longest chain, fork mid-chain, or start fresh idea.
2. Pick or create one node id (idea/hypothesis/experiment/mvp/outcome).
3. Run the experiment / implement the MVP / write the outcome.
4. When done, signal completion:
   ```
   python3 <plugin>/bin/cli.py done {args.iter_n} {args.agent_id} \\
     --verdict <proved|disproved|inconclusive_lean_proved:N|inconclusive_lean_disproved:N|pending> \\
     --confidence <0.0-1.0> \\
     --node-id <new_or_extended_node_id> \\
     --notes "<one-line>"
   ```

If stuck >2 attempts on same approach → write a `pending` verdict and stop.
"""
```

**Replace with:**
```python
def _compose_big(inject_text: str, args: argparse.Namespace) -> str:
    completion = _completion_block(
        args.runtime,
        args.iter_n,
        args.agent_id,
        verdict="<proved|disproved|inconclusive_lean_proved:N|inconclusive_lean_disproved:N|pending>",
    )
    if args.runtime == "cc":
        completion_section = f"When done, report exactly:\n\n{completion}"
    else:
        completion_section = f"When done, signal completion:\n   ```\n   {completion}\n   ```"
    
    return f"""# autoresearch-tree iteration {args.iter_n} — agent {args.agent_id}

## Zoom Level: BIG (legacy alias for numeric level {LEGACY_LEVEL_MAP['big']} — {LEVEL_INFO[LEGACY_LEVEL_MAP['big']]['name']})
You are exploring the WHOLE graph. Pick a high-level idea or new chain to extend.
Bias: introduce a fresh idea, fork an under-explored chain, or seed a new domain.

{inject_text}

## Your Task
1. Decide: extend longest chain, fork mid-chain, or start fresh idea.
2. Pick or create one node id (idea/hypothesis/experiment/mvp/outcome).
3. Run the experiment / implement the MVP / write the outcome.
4. {completion_section}

If stuck >2 attempts on same approach → write a `pending` verdict and stop.
"""
```

### 5. Update `_compose_small` to use the helper (lines 425-431)

**Current (lines 420-435):**
```python
    lines.extend([
        "",
        "## Your Task",
        f"Extend or fork from `{target}`. Stay tight — don't wander to other chains.",
        "Acceptable: spawn one child node (hyp from idea, exp from hyp, mvp from exp, outcome from mvp).",
        "When done, signal completion:",
        "```",
        f"python3 <plugin>/bin/cli.py done {args.iter_n} {args.agent_id} \\",
        "  --verdict <verdict_state> --confidence <0.0-1.0> \\",
        f"  --node-id <new_node_id> --parent {target} \\",
        '  --notes "<one-line>"',
        "```",
        "",
        "If stuck >2 attempts → write `pending` verdict and stop.",
    ])
```

**Replace with:**
```python
    completion = _completion_block(
        args.runtime,
        args.iter_n,
        args.agent_id,
        node_id_expr=f"<new_node_id> --parent {target}",
    )
    if args.runtime == "cc":
        lines.extend([
            "",
            "## Your Task",
            f"Extend or fork from `{target}`. Stay tight — don't wander to other chains.",
            "Acceptable: spawn one child node (hyp from idea, exp from hyp, mvp from exp, outcome from mvp).",
            "When done, report exactly:",
            "",
            completion,
            "",
            "If stuck >2 attempts → write `pending` verdict and stop.",
        ])
    else:  # pi
        lines.extend([
            "",
            "## Your Task",
            f"Extend or fork from `{target}`. Stay tight — don't wander to other chains.",
            "Acceptable: spawn one child node (hyp from idea, exp from hyp, mvp from exp, outcome from mvp).",
            "When done, signal completion:",
            "```",
            completion,
            "```",
            "",
            "If stuck >2 attempts → write `pending` verdict and stop.",
        ])
```

### 6. Update `_render_level` to use the helper (lines 524-541)

**Current (lines 524-541):**
```python
    lines.extend([
        "Acceptable: spawn one child node (hyp from idea, exp from hyp, mvp from exp, outcome from mvp).",
        "When done, signal completion:",
        "```",
        f"python3 <plugin>/bin/cli.py done {args.iter_n} {args.agent_id} \\",
        "  --verdict <verdict_state> --confidence <0.0-1.0> \\",
    ])
    node_id_line = "  --node-id <new_node_id>"
    if target:
        node_id_line += f" --parent {target}"
    node_id_line += " \\"
    lines.append(node_id_line)
    lines.extend([
        '  --notes "<one-line>"',
        "```",
        "",
        "If stuck >2 attempts → write `pending` verdict and stop.",
    ])
```

**Replace with:**
```python
    node_id_expr = "<new_node_id>"
    if target:
        node_id_expr += f" --parent {target}"
    completion = _completion_block(
        args.runtime,
        args.iter_n,
        args.agent_id,
        node_id_expr=node_id_expr,
    )
    if args.runtime == "cc":
        lines.extend([
            "Acceptable: spawn one child node (hyp from idea, exp from hyp, mvp from exp, outcome from mvp).",
            "When done, report exactly:",
            "",
            completion,
            "",
            "If stuck >2 attempts → write `pending` verdict and stop.",
        ])
    else:  # pi
        lines.extend([
            "Acceptable: spawn one child node (hyp from idea, exp from hyp, mvp from exp, outcome from mvp).",
            "When done, signal completion:",
            "```",
            completion,
            "```",
            "",
            "If stuck >2 attempts → write `pending` verdict and stop.",
        ])
```

## Existing tests that touch this

**One test asserts on the completion block:**
- `test_legacy_big_keeps_original_whole_graph_content` (line 247) — checks for `"cli.py done" in text`

This test will continue to pass because:
1. The test fixture sets `agi-tree.config.json` without a `cc_dispatch` key
2. The runtime will default to `"pi"`
3. The pi runtime emits the `cli.py done` block as before
4. No code path changes for existing callers that don't specify `--runtime`

## Baseline

test_zoom.py **22 passed** before any change