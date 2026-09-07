"""hypothesis:l2-bin-help-smoke — catch unimported names in main() paths.

Every script under extensions/agi/bin with a --help flag must exit 0 and emit
non-empty stdout. Scripts that legitimately lack --help are listed explicitly
(rather than skipped silently) so a script that acquires --help later is
tested without anyone remembering to update this list.

The trigger: L2.06 added spawn_gate.py and dispatch.py referenced it in main()
without an import. 1539 tests passed; every parent spawn died with NameError.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"

#: Scripts that lack --help handling, with a one-line reason each.
#: These are listed explicitly rather than skipped silently, so the list
#: shrinks rather than grows when --help is added.
NO_HELP = {
    "node_writer.py": "library module, not a CLI tool; no --help",
}


def _scripts() -> list[Path]:
    """All *.py files directly under bin/, excluding __pycache__ and _private."""
    scripts: list[Path] = []
    for f in sorted(BIN.iterdir()):
        name = f.name
        if not f.is_file() or not name.endswith(".py"):
            continue
        if name.startswith("_"):
            continue
        if name == "__init__.py":
            continue
        scripts.append(f)
    return scripts


@pytest.mark.parametrize("script", _scripts(), ids=lambda p: p.name)
def test_help_smoke(script: Path) -> None:
    name = script.name
    if name in NO_HELP:
        pytest.skip(f"{name}: {NO_HELP[name]}")

    result = subprocess.run(
        [sys.executable, str(script), "--help"],
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, (
        f"{name} --help exited {result.returncode}.\n"
        f"stderr: {result.stderr[:500]}"
    )
    assert len(result.stdout.strip()) > 0, (
        f"{name} --help produced empty stdout (exit 0 though)"
    )