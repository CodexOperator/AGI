#!/usr/bin/env python3
"""send_router_audit.py -- frozen instrument for goal:g7.32.4 clause (1).

Pure-stdlib AST walk over a Python target: every ABSOLUTE import of module
root `rotate` or `dispatch` (top-level AND nested -- an `import rotate` inside
a function body counts) AND every RELATIVE sibling import that names one of
those roots (`from . import rotate`, `from . import dispatch`). This is the
measuring instrument the thin-router refactor is judged against, and it
carries no policy of its own.

NAMED BLIND SPOT: DYNAMIC imports are NOT seen -- `importlib.import_module`,`__import__` and `exec` can reach `rotate`/`dispatch` at runtime with no
import node in the AST. The audit's zero is a claim about static imports
only, never about runtime reachability.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOTS = ("rotate", "dispatch")


def audit(path):
    """Every rotate/dispatch import in `path`, sorted dicts carrying line,
    module, names (imported symbols) and function (enclosing def or
    `<module>`)."""
    tree = ast.parse(Path(path).read_text(encoding="utf-8"),
                     filename=str(path))
    found = []

    def walk(node, func="<module>"):
        for child in ast.iter_child_nodes(node):
            inner = func
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef,
                                  ast.ClassDef)):
                inner = child.name
            if isinstance(child, ast.Import):
                for alias in child.names:
                    if alias.name.split(".")[0] in ROOTS:
                        found.append({"line": child.lineno, "function": func,
                                      "module": alias.name.split(".")[0],
                                      "names": [alias.name]})
            elif isinstance(child, ast.ImportFrom):
                mod = (child.module or "").split(".")[0]
                if mod in ROOTS:
                    found.append({"line": child.lineno, "function": func,
                                  "module": mod,
                                  "names": [a.name for a in child.names]})
                elif child.level or not child.module:
                    # A relative import with no module part (`from . import
                    # rotate`) has `module is None`; the root lives in the
                    # ALIAS name instead. Report each matching alias as its
                    # own finding, with `module` set to the alias root.
                    for a in child.names:
                        root = a.name.split(".")[0]
                        if root in ROOTS:
                            found.append({"line": child.lineno,
                                          "function": func, "module": root,
                                          "names": [a.name]})
            walk(child, inner)

    walk(tree)
    return sorted(found, key=lambda f: (f["line"], f["module"]))


def main():
    args = sys.argv[1:]
    if args and args[0] in ("-h", "--help"):
        print("usage: send_router_audit.py [TARGET.py]"
              "  (default: send.py beside this script)")
        return 0
    target = (Path(args[0]) if args
              else Path(__file__).resolve().parent / "send.py")
    for f in audit(target):
        print(f"{f['line']}\t{f['function']}\t{f['module']}\t"
              f"{','.join(f['names'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
