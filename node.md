---
id: mvp:a01-7031af17-449ecb-r11
mint_id: 15f0620d29e14073bd4466037413dfa4
type: mvp
parents:
  - hyp:a01-7031af17-449ecb
next_edges:
  - verdict:a01-7031af17-449ecb-r11
confidence: 1.0
edited_by: season.py
season: 1
tags:
  - graph-core
  - R11
  - path-safety
  - mvp
thought_session: season
title: "graph-core/R11 MVP: Wire PathValidator Into Loader"
---
# mvp:a01-7031af17-449ecb-r11

## What This Is

A minimal patch that wires `safe_path()` from `src/graph_core/paths.py` into `load_directory` so that every file path opened by the loader is validated against the project root before use.

## Input Shape

```python
# src/graph_core/loader.py — load_directory signature unchanged
def load_directory(base: Path) -> tuple[Graph, list[LoadedNode]]:
    ...
```

## Output Shape

Same signature, same return type. Path validation happens inside the function before each `path.read_bytes()` or `nf = load_node_file(p)` call.

## Behavior

- `load_node_file` calls `safe_path(p)` before opening `p`
- Or: `load_directory` wraps its file list with `safe_path` validation
- If any file path escapes the project root: `PathOutsideProjectError` raised with filename

## Edge Cases

- Symbolic links that resolve outside: caught (resolve happens inside validate)
- Relative paths like `../../etc/passwd`: caught (relative_to fails)
- Absolute paths: caught by `validate()` on the resolved path
- File not found (but path is valid): loader continues, file skipped

## Code Diff

```diff
# src/graph_core/loader.py (conceptual)
+ from .paths import safe_path

  def load_directory(base: Path) -> tuple[Graph, list[LoadedNode]]:
+     safe_path(base)  # validate root dir
      for p in base.rglob("*"):
          if p.is_file() and _is_node_file(p):
+             safe_path(p)  # validate each file before opening
              ...
```