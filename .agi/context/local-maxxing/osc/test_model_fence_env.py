"""Falsifiers 1-3 of hypothesis:a-no-model-round-refuses-a-model-load-in-every-process-it-spawns.

The env-fence half: a no-model round puts `extensions/agi/fence/` on PYTHONPATH,
so EVERY python process it starts installs the refusal at interpreter start --
the parent, a kid, a GRANDCHILD -- from the ONE table the .agi/context conftest
also uses.

Stand-ins only: no real torch/transformers is installed or imported here, no
weights dir is opened, no network, no hub id is resolved (the id below is a
string the stand-in records, never fetches).
"""

import os
import pathlib
import re
import subprocess
import sys
import textwrap

import pytest

_FENCE_DIR = pathlib.Path(__file__).resolve().parents[4] / "extensions" / "agi" / "fence"
_TABLE = _FENCE_DIR.parent / "model_fence.py"

# Stand-in `transformers` in the REAL shape: the loader is a classmethod on a
# class held by a SUBMODULE, and it RECORDS instead of loading.
_STANDIN = {
    "transformers/__init__.py": "",
    "transformers/models/__init__.py": "",
    "transformers/models/llama.py": textwrap.dedent(
        """
        CALLS = []


        class AutoModelForCausalLM:
            @classmethod
            def from_pretrained(cls, name, **kw):
                CALLS.append(name)
                return "RECORDED"
        """),
}

# One probe, run as a child and again as a grandchild: import the stand-in, call
# the loader, report REFUSED-<ExcName>-CALLS=<n> or NOT-REFUSED.
_PROBE = textwrap.dedent(
    """
    import transformers.models.llama as L
    try:
        L.AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-8B")
        print("NOT-REFUSED")
    except BaseException as exc:
        print("REFUSED-%s-CALLS=%d" % (type(exc).__name__, len(L.CALLS)))
    """)


@pytest.fixture
def standin_tree(tmp_path):
    for rel, text in _STANDIN.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    return tmp_path


def _fenced_env(standin_tree, *, with_src_dir):
    """The env a no-model round inherits: the fence dir on PYTHONPATH, the
    stand-ins beside it, and NOTHING else from this test process's PYTHONPATH.

    `with_src_dir=False` also puts `extensions/agi` on PYTHONPATH, so the fence
    resolves the table by `import model_fence`. `True` withholds it, so the fence
    must fall back to AGI_MODEL_FENCE_SRC -- two resolutions, ONE table."""
    table_dir = "" if with_src_dir else str(_FENCE_DIR.parent)
    return {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "HOME": os.environ.get("HOME", "/tmp"),
        "PYTHONPATH": os.pathsep.join([str(_FENCE_DIR), str(standin_tree), table_dir]),
        "AGI_MODEL_FENCE_SRC": str(_TABLE),
    }


def _run(env, code, extra_env=None):
    return subprocess.run([sys.executable, "-c", code], capture_output=True,
                          text=True, timeout=120, env={**env, **(extra_env or {})})


def test_f1_a_fenced_child_refuses_the_standin_loader(standin_tree):
    """Falsifier 1: the TMM.228 call, in a process that inherited the fenced env.
    Refused AT THE CALL, and the stand-in's recorder never ran (CALLS=0)."""
    for with_src_dir in (True, False):
        r = _run(_fenced_env(standin_tree, with_src_dir=with_src_dir), _PROBE)
        assert "REFUSED-ModelLoadRefused-CALLS=0" in r.stdout, (with_src_dir, r.stdout, r.stderr)


def test_f2_a_grandchild_of_the_fenced_env_is_still_fenced(standin_tree):
    """Falsifier 2: the child does not fence itself -- it only INHERITS. So the
    grandchild (python spawning python) must refuse on its own, with the fence
    installed at ITS interpreter start."""
    parent = textwrap.dedent(
        """
        import subprocess, sys
        r = subprocess.run([sys.executable, "-c", %r], capture_output=True, text=True)
        sys.stdout.write(r.stdout)
        """ % _PROBE)
    r = _run(_fenced_env(standin_tree, with_src_dir=True), parent)
    assert "REFUSED-ModelLoadRefused-CALLS=0" in r.stdout, (r.stdout, r.stderr)


def test_f1_the_same_env_does_not_refuse_when_the_fence_is_withheld(standin_tree):
    """The control, so f1 is not vacuous: with NO fence dir and no
    AGI_MODEL_FENCE_SRC the same probe RECORDS -- the refusal is the fence's."""
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"),
           "PYTHONPATH": str(standin_tree), "AGI_MODEL_FENCE_SRC": ""}
    r = _run(env, _PROBE)
    assert "NOT-REFUSED" in r.stdout, (r.stdout, r.stderr)


# Falsifier 3: the table exists ONCE. A mechanical scan over named files -- the
# engine's own package (one directory, walked with os.walk, never `grep -r`,
# `find` or `rg` over the repo root or .agi/) plus this conftest's. What is
# forbidden is a SECOND of the OWNING definitions: the dict literal, the
# refusal stub, the allow-list check, the patcher. A `def allow_model_load`
# FIXTURE in the conftest is a re-export of the shared one, not a second table.
_SCAN_DIRS = (pathlib.Path(__file__).resolve().parents[4] / "extensions" / "agi",
              pathlib.Path(__file__).resolve().parents[2])   # extensions/agi, .agi/context
_TABLE_DEF = re.compile(r"^REFUSED\s*=\s*\{|^def (_stub|_declared_ok|_patch_one)\(")


def _defs(path):
    return [(i + 1, line) for i, line in enumerate(path.read_text().splitlines())
            if _TABLE_DEF.match(line)]


def test_f3_the_loader_table_is_defined_exactly_once():
    hits = {}
    for d in _SCAN_DIRS:
        for p in sorted(d.rglob("*.py")):
            if "tests" in p.parts or p.name.startswith("test_"):   # a test may NAME it
                continue
            for n, line in _defs(p):
                hits.setdefault(str(p.relative_to(d)), []).append((n, line))
    named = {k: v for k, v in hits.items() if v}
    assert set(named) == {"model_fence.py"}, named        # the ONE owner, one file
    tables = [n for n, line in named["model_fence.py"] if line.startswith("REFUSED")]
    assert len(tables) == 1, named                       # exactly one table literal
    # the conftest RE-EXPORTS the table; it defines none of it
    assert "REFUSED = model_fence.REFUSED" in (_SCAN_DIRS[1] / "conftest.py").read_text()
