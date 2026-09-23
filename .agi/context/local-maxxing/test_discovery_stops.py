"""Fix (a): every discovery loop STOPS at the filesystem root instead of spinning.

The four scripts used `while not isfile(...): p = dirname(p)`; at `/`,
`os.path.dirname("/") == "/"`, so the loop never ends. Each now calls the
`_find_ancestor(start, *rels)` helper defined in its own source, which raises
FileNotFoundError once it reaches the root.

The helper is loaded straight from each script's REAL source via `ast` (the
three probe runners import numpy/httpx/websockets, which are not installed
here, so importing them would fail before discovery even runs).
"""
import ast
import os
import tempfile
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

# script -> the name(s) its loop walks up for
SCRIPTS = {
    "datasets/kid-sft/build_corpus.py": ".agi/config.json",
    ".agi/context/local-maxxing/kidc_verdict_corpus_trainability.py": "paths.py",
    ".agi/context/local-maxxing/ws-raw/run_gpu_probe.py": "paths.py",
    ".agi/context/local-maxxing/ws-raw/run_kidC.py": "paths.py",
}


def _load_find_ancestor(rel):
    """Compile `_find_ancestor` out of the real script source, no heavy imports."""
    path = os.path.join(REPO, rel)
    with open(path, encoding="utf-8") as fh:
        tree = ast.parse(fh.read(), filename=path)
    fn = next(n for n in tree.body
              if isinstance(n, ast.FunctionDef) and n.name == "_find_ancestor")
    ns = {"os": os}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), path, "exec"), ns)
    return ns["_find_ancestor"]


class DiscoveryStopsAtRoot(unittest.TestCase):
    def test_each_script_stops_with_named_error(self):
        start = os.path.join(os.path.abspath(os.sep), "no-such-dir-a00-xyz", "deep")
        for rel, wanted in SCRIPTS.items():
            fn = _load_find_ancestor(rel)
            # simulate "the name exists nowhere above" deterministically
            with mock.patch("os.path.exists", return_value=False):
                with self.assertRaises(FileNotFoundError) as cm:
                    fn(start, wanted)
            self.assertIn(wanted, str(cm.exception), rel)
            self.assertIn(start, str(cm.exception), rel)

    def test_returns_the_nearest_dir_that_holds_the_name(self):
        with tempfile.TemporaryDirectory() as td:
            for wanted in (".agi/config.json", "paths.py"):
                rel = os.path.join("datasets", "kid-sft", "build_corpus.py")
                fn = _load_find_ancestor(rel)
                marker = os.path.join(td, wanted)
                os.makedirs(os.path.dirname(marker), exist_ok=True)
                open(marker, "w").close()
                deep = os.path.join(td, "a", "b")
                os.makedirs(deep, exist_ok=True)
                self.assertEqual(fn(deep, wanted), os.path.abspath(td))


if __name__ == "__main__":
    unittest.main()
