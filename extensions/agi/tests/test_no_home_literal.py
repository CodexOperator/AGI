"""`goal:g15.29.2` — no engine script may carry a `/home/<user>/` literal.

A home path is a value that belongs in a `box.*` cell (config-max): the same
script on another box must resolve the home from config, never carry the first
box's home in its bytes. This is the committed falsifier for
`hypothesis:engine-code-carries-no-home-user-literal`; it is RED on the
pre-fix bytes (`heal.py:3112`, `pi_edit_forgiveness.py:108`,
`unify.py:401-402`) and GREEN once each resolves through its cell or the
resolved home.

Prose is not a literal: docstrings and `#` comments are excluded, because a
docstring may *discuss* a home path without carrying one. Real string
constants — including `Path("/home/...")` arguments — are what this scans.
"""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

#: A path-shaped `/home/<name>/`, never the bare word or prose sentence.
_HOME_LITERAL = re.compile(r"/home/[A-Za-z0-9._-]+/")


def _string_constants(source: str, path: Path):
    """(lineno, value) for every real string literal, docstrings excluded."""
    tree = ast.parse(source, filename=str(path))
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef,
                             ast.AsyncFunctionDef)):
            body = getattr(node, "body", [])
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                docstrings.add(id(body[0].value))
    for node in ast.walk(tree):
        if (isinstance(node, ast.Constant) and isinstance(node.value, str)
                and id(node) not in docstrings):
            yield node.lineno, node.value


def test_no_home_user_literal_in_engine_bin_scripts():
    offenders = []
    for path in sorted(BIN.rglob("*.py")):
        parts = set(path.relative_to(BIN).parts)
        if "tests" in parts or "fixtures" in parts:
            continue
        for lineno, value in _string_constants(path.read_text(encoding="utf-8"), path):
            if _HOME_LITERAL.search(value):
                offenders.append(f"{path.relative_to(BIN)}:{lineno}: {value!r}")
    assert offenders == [], (
        "home-user literal in engine code; move it to a box.* cell or the "
        "resolved home (config-max, goal:g15.29.2):\n" + "\n".join(offenders))
