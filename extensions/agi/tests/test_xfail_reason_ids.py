"""Every strict xfail that waits on a build names the GOAL it waits on.

A `RED until ...` reason reads `goal:<id>: RED until ...` with an id that is a
node of this graph (links.frontmatter_rows), never a seat ("until DG3"): a
seat rotates, a goal is the tracker. Council [decision] alive 02:32:49Z 10-26
(the census tip after 3b).
"""
import ast
import re
import sys
from pathlib import Path

TESTS = Path(__file__).resolve().parent
ROOT = TESTS.parents[2]
sys.path.insert(0, str(ROOT / "extensions" / "agi" / "bin"))
import links  # noqa: E402

SHAPE = re.compile(r"^goal:(\S+): RED until ")
STRICT_UNREAD = object()   # strict= is not a literal: the decorator cannot be read as strict or not


def _value(node, names):
    """A reason expression's text: literals, implicit concatenation, `+`, and
    module-level string names; anything else is None (not read)."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Name):
        return names.get(node.id)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        a, b = _value(node.left, names), _value(node.right, names)
        return a + b if a is not None and b is not None else None
    return None


def strict_reasons(src):
    """(line, reason) of every `xfail(strict=True, reason=...)` in `src`; a
    `strict=` that is not a literal (strict=S) yields (line, STRICT_UNREAD)."""
    tree = ast.parse(src)
    names = {}
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            v = _value(n.value, names)
            if v is not None:
                names[n.targets[0].id] = v
    out = []
    for n in ast.walk(tree):
        if not (isinstance(n, ast.Call) and getattr(n.func, "attr", None) == "xfail"):
            continue
        kw = {k.arg: k.value for k in n.keywords}
        if "strict" in kw and not isinstance(kw["strict"], ast.Constant):
            out.append((n.lineno, STRICT_UNREAD))   # council crumb (sp, L262): never a silent skip
            continue
        if not (isinstance(kw.get("strict"), ast.Constant) and kw["strict"].value is True):
            continue
        r = _value(kw["reason"], names) if "reason" in kw else None
        out.append((n.lineno, r))
    return out


def offenders(files, ids):
    bad = []
    for f in files:
        for line, r in strict_reasons(Path(f).read_text(encoding="utf-8")):
            if r is STRICT_UNREAD:
                bad.append(f"{Path(f).name}:{line}: strict unread")
                continue
            if r is None:   # an f-string, a call, an imported name: unread is an offender, never a skip (council fix-forward, alive 20:54:18Z 10-27)
                bad.append(f"{Path(f).name}:{line}: reason unread")
                continue
            if "RED until" not in r:
                continue
            m = SHAPE.match(r)
            if not m or f"goal:{m.group(1)}" not in ids:
                bad.append(f"{Path(f).name}:{line}: {r[:90]}")
    return bad


def _ids():
    return {fm.get("id") for fm in links.frontmatter_rows(ROOT / ".agi" / "nodes").values()}


def test_every_red_until_reason_names_a_goal_of_this_graph():
    files = sorted(TESTS.glob("test_*.py"))
    assert len(files) > 100
    reasons = [r for f in files for _, r in strict_reasons(f.read_text(encoding="utf-8")) if isinstance(r, str) and "RED until" in r]
    assert len(reasons) >= 9, reasons
    assert offenders(files, _ids()) == []


def test_mutant_a_seat_named_reason_is_RED(tmp_path):
    f = tmp_path / "test_m.py"
    f.write_text('import pytest\n_X = "bundle 4 W2a: RED until DG3 builds it"\n'
                 '@pytest.mark.xfail(strict=True, reason=_X + " (x.py:1)")\ndef test_a(): pass\n'
                 '@pytest.mark.xfail(strict=True, reason="goal:g0.does.not.exist: RED until x")\ndef test_b(): pass\n'
                 '@pytest.mark.xfail(strict=True, reason="goal:g4.18.7.1: RED until "\n    "x is built")\ndef test_c(): pass\n')
    bad = offenders([f], _ids())
    assert [b.split(":")[1] for b in bad] == ["3", "5"], bad


def test_mutant_an_unreadable_reason_is_RED_by_name(tmp_path):
    f = tmp_path / "test_u.py"
    f.write_text('import pytest\nfrom x import SEAT\n'
                 '@pytest.mark.xfail(strict=True, reason=f"RED until {SEAT} builds it")\ndef test_a(): pass\n'
                 '@pytest.mark.xfail(strict=True, reason=SEAT)\ndef test_b(): pass\n'
                 '@pytest.mark.xfail(strict=True)\ndef test_c(): pass\n')
    assert offenders([f], _ids()) == ["test_u.py:3: reason unread", "test_u.py:5: reason unread",
                                      "test_u.py:7: reason unread"]


def test_mutant_a_non_literal_strict_is_RED_by_name(tmp_path):
    f = tmp_path / "test_s.py"
    f.write_text('import pytest\nS = True\n'
                 '@pytest.mark.xfail(strict=S, reason=f"RED until {S}")\ndef test_a(): pass\n'
                 '@pytest.mark.xfail(strict=False, reason="RED until a seat")\ndef test_b(): pass\n')
    assert offenders([f], _ids()) == ["test_s.py:3: strict unread"]
