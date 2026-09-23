"""Tests for bin/send_router_audit.py -- the goal:g7.32.4 clause (1)
instrument (send.py thin router: zero rotate/dispatch orchestration imports).

The scanner must see NESTED imports, not just top-level ones, because every
one of send.py's current couplings is a lazy `import rotate` inside a
function body -- a top-level-only scanner would report a clean file and
certify the exact defect the goal exists to remove.
"""

import importlib.util
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
SEND = BIN / "send.py"
spec = importlib.util.spec_from_file_location(
    "send_router_audit", BIN / "send_router_audit.py")
sra = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sra)


def _t(finding):
    return (finding["function"], finding["line"], finding["module"],
            tuple(finding["names"]))


# DEBT LEDGER -- DO NOT EDIT TO MAKE A FAILURE PASS.
# This constant is the exact set of rotate/dispatch imports in send.py as of
# the instrument's first run (2026-09-23). It exists so that every NEW
# coupling is a test failure and every REMOVED coupling is a required
# one-line ledger edit. When the ledger is empty, clause (1) has been reached
# and `test_clause_one_zero_coupling` below XPASSes -- that is the signal this
# refactor is done, and the signal this constant (and the xfail) may be
# retired.
CURRENT_INVENTORY = [
    ("_commit_push_seat_row", 613, "rotate", ("rotate",)),
    ("_commit_push_all_live", 727, "rotate", ("rotate",)),
    ("_run_pending_swap_completion", 825, "rotate", ("rotate",)),
    ("_all_live_origin_sync_line", 843, "rotate", ("rotate",)),
    ("_row_is_quiet", 1580, "rotate", ("rotate",)),
    ("_row_is_quiet_system", 1608, "rotate", ("rotate",)),
    ("_nudge_target", 2188, "rotate", ("rotate",)),
]


def test_scanner_sees_top_level_and_nested(tmp_path):
    src = (
        "import json\n"
        "import rotate\n"
        "from dispatch import spawn\n"
        "def outer():\n"
        "    import rotate\n"
        "    def inner():\n"
        "        from rotate import _git_toplevel\n"
        "    return inner\n"
        "class K:\n"
        "    def m(self):\n"
        "        import dispatch\n"
    )
    p = tmp_path / "sample.py"
    p.write_text(src, encoding="utf-8")
    got = sorted((_t(f) for f in sra.audit(p)), key=lambda t: t[1])
    assert got == [
        ("<module>", 2, "rotate", ("rotate",)),
        ("<module>", 3, "dispatch", ("spawn",)),
        ("outer", 5, "rotate", ("rotate",)),
        ("inner", 7, "rotate", ("_git_toplevel",)),
        ("m", 11, "dispatch", ("dispatch",)),
    ]


def test_scanner_clean_fixture_no_false_positives(tmp_path):
    p = tmp_path / "clean.py"
    p.write_text("import json\nfrom pathlib import Path\nimport os\n",
                 encoding="utf-8")
    assert sra.audit(p) == []


def test_send_inventory_matches_ledger():
    got = [_t(f) for f in sra.audit(SEND)]
    assert got == CURRENT_INVENTORY


@pytest.mark.xfail(reason="goal:g7.32.4 clause (1) not yet met: send.py still "
                          "imports rotate at 7 lazy sites (see "
                          "CURRENT_INVENTORY debit ledger)")
def test_clause_one_zero_coupling():
    assert sra.audit(SEND) == []
