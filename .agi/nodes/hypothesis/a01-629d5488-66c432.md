---
id: hypothesis:a01-629d5488-66c432
mint_id: c71e47ae1e214f4f82871ac994859a0e
type: hypothesis
parents:
  - goal:g7.5
next_edges: []
confidence: 0.75
scaffold_hash: 2d7a88692206b280
title: A01 629d5488 66c432
verdict: pending
---
# hypothesis:a01-629d5488-66c432

## Hypothesis

Replacing the bare `except Exception: continue` / `except Exception: pass` at the
four catch sites (loader.py:load_directory, db_loader.py:load_directory,
snapshot-goals.py:load_existing_nodes, snapshot-build-site.py:load_existing_nodes)
with explicit warnings (file path + exception repr, to stderr) eliminates silent
parse-failure data loss without breaking normal corpus loading.

## Proved by

1. A deliberately malformed frontmatter file (the G7.5 fixture: a YAML block
   with a stray list item at indent 1 after a scalar mapping entry, no
   introducing key) is placed into a test directory alongside valid files.
2. `load_directory` loads the valid files and prints a WARN line to stderr for
   the malformed one — showing its path and the PyYAML exception — then
   continues without raising.
3. `load_existing_nodes` (both snapshot variants) does the same: warns on
   stderr, includes the malformed path in the warning, returns only valid nodes.
4. Existing tests (clean corpuses, duplicate id detection, recursive bodies)
   pass unchanged — the warning path adds no new failures.
5. A strict mode (opt-in flag, following G7.2's `strict=True` pattern)
   promotes the same warning to an exception, letting callers who want
   fail-fast semantics get it.

## Disproved by

1. Any existing test fails (regression — the warning changes control flow for
   previously silent error paths).
2. The warning fires on a legitimate file whose parse succeeds (false positive;
   indicates the warning guard is too broad or inserted before the parse).
3. The added warning measurably slows bulk loading on a corpus of ~800 nodes
   beyond 1-2% overhead (stderr write per file for each of many concurrent
   callers).
4. A strict-mode-only fix (warning only when `strict=True`) would still leave
   the default silent — which is the same defect, just behind a flag. The
   hypothesis requires the default to warn.

## Scope note

The four sites differ in signature and use context:

| Site | Exception handler | What is lost |
|---|---|---|
| `loader.py:load_directory` | `except Exception: continue` | Entire node file from graph |
| `db_loader.py:load_directory` | `except Exception: continue` | Node from DB-backed graph |
| `snapshot-goals.py:load_existing_nodes` | `except Exception: pass` | Node from GOALS.md render |
| `snapshot-build-site.py:load_existing_nodes` | `except Exception: pass` | Node from build-site render |

Each must be patched independently. A patched `loader.py` does not change
either snapshot loader because they vend their own YAML parsing inline rather
than calling `load_node_file`.


## Agent Notes
Hypothesis: replace silent except Exception at 4 parse-failure sites (loader.py:load_directory, db_loader.py:load_directory, snapshot-goals.py:load_existing_nodes, snapshot-build-site.py:load_existing_nodes) with path+exception warnings to stderr, matching G7.1/G7.2 warn-by-default / strict-to-fail pattern. Scope table enumerates all four sites and their independent fix paths.
