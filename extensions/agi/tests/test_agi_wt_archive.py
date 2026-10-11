"""RuntimeDirectoryPreserve: the unit keeps the post's runtime dir (the node trees) across a restart. The archive-ref rows (f1, f2, r1, r2, m1, m3, g83) moved to agi-turn.t.sh (g6, g8, x1, x4, x4b, x5, x6)."""
from pathlib import Path

GEO = Path(__file__).resolve().parents[3] / ".agi/nodes/.geometry"


def test_f3_unit_keeps_runtime_dir_across_restart():
    u = (GEO / "engine-root.md").read_text()
    assert "RuntimeDirectory=agi-%i\nRuntimeDirectoryPreserve=restart\n" in u
