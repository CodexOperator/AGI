"""Fix (b): the pi store-dir name is DERIVED from a root, never hard-coded.

`build_corpus.py` hard-coded pi's old store-dir name
`--home-ubuntu-work-agi-.agi-worktrees-<agent-id>--`. The real stores on this
box are `--data-work-agi-.agi-worktrees-<agent-id>--`, i.e. pi names a store
after its checkout dir ( /a/b -> --a-b-- ). `store_dir_name(root, agent_id)`
derives it from the root that discovery found, never from `box.root`.

Fixtures are temp roots only: no real pane, no unit, no process.
"""
import importlib.util
import os
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
_SPEC = importlib.util.spec_from_file_location(
    "build_corpus_undertest", os.path.join(HERE, "build_corpus.py"))
bc = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(bc)

AGENT = "a00-deadbeef"


def _expected(base):
    return "--" + base.strip("/").replace("/", "-") + "-" + AGENT + "--"


class StoreDirName(unittest.TestCase):
    def test_worktree_root_shares_the_worktrees_parent(self):
        with tempfile.TemporaryDirectory() as td:
            root = os.path.join(td, ".agi", "worktrees", "a00-12345678")
            os.makedirs(root)
            self.assertEqual(bc.store_dir_name(root, AGENT),
                             _expected(os.path.dirname(root)))

    def test_main_root_uses_its_own_worktrees_dir(self):
        with tempfile.TemporaryDirectory() as td:
            root = os.path.join(td, "repo")
            base = os.path.join(root, ".agi", "worktrees")
            os.makedirs(base)
            self.assertEqual(bc.store_dir_name(root, AGENT), _expected(base))

    def test_legacy_prefix_is_gone(self):
        with tempfile.TemporaryDirectory() as td:
            name = bc.store_dir_name(os.path.join(td, "x"), AGENT)
            self.assertNotIn("home-ubuntu-work-agi", name)
            self.assertTrue(name.startswith("--"))
            self.assertTrue(name.endswith(AGENT + "--"))


if __name__ == "__main__":
    unittest.main()
