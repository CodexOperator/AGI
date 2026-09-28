"""PASS 8 items 5+8: a tracked probe must DERIVE its repo root, never declare one.

The hardcoded-path guard (extensions/agi/tests/test_retired_box_prefix.py) scans
bin/ hooks/ briefs/ tests/ + .agi/config.json only, so tracked evidence under
datasets/ is structurally outside it (item 8: an uncovered class in a deliberate
exemption, not a guard failure). This test closes the class for THIS ROUND's
probes. Repo-wide the class is still OPEN -- a first pass of this file found the
same literal in datasets/serving-sweep/2026-09-23-ub/parent-probe-a00-67c8a71a/
probe_q8.py and in datasets/osc-band/2026-09-23-kquant/a00-86466b78/
probe_{sensitivity,higher_bits}.py; those are other rounds' evidence and are out
of this kid's file scope. Widen ROUNDS when those are fixed.

Runs on the DEFAULT python3 -- no numpy, no torch, no model.
"""
import ast
import os

HERE = os.path.dirname(os.path.abspath(__file__))          # .agi/context/local-maxxing/osc
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
ROUNDS = ("osc-band/2026-09-24-qknorm/a00-bcea484d-probes",)
BANNED = ("/.agi/", "/datasets/osc-band/")


def _py_files():
    for rel in ROUNDS:
        for dirpath, dirnames, filenames in os.walk(os.path.join(REPO, "datasets", rel)):
            dirnames[:] = [d for d in dirnames if d != "__pycache__"]
            for f in sorted(filenames):
                if f.endswith(".py"):
                    yield os.path.join(dirpath, f)


def _absolute_path_literals(path):
    """Every string constant in `path` that reads as an absolute repo path."""
    with open(path) as f:
        tree = ast.parse(f.read(), filename=path)
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            s = node.value
            if s.startswith("/") and any(b in s for b in BANNED):
                yield node.lineno, s


def test_tracked_probes_carry_no_absolute_repo_path():
    files = list(_py_files())
    assert len(files) >= 2, files
    hits = [(p, lineno, s) for p in files for lineno, s in _absolute_path_literals(p)]
    assert not hits, "derive the root from __file__, do not declare it: " + repr(hits)


def test_probes_derive_the_root_from_their_own_location():
    for rel in ROUNDS:
        for name in sorted(os.listdir(os.path.join(REPO, "datasets", rel))):
            if not name.endswith(".py"):
                continue
            with open(os.path.join(REPO, "datasets", rel, name)) as f:
                src = f.read()
            assert "os.path.abspath(__file__)" in src, name
            assert "worktrees" not in src, name
