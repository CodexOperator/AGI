

def test_confidence_percent_is_normalized_not_stored_raw():
    """A kid holding both scales at once passed the lean's integer percent to
    --confidence too, storing `confidence: 65.0` on a 0..1 field (2026-09-01).
    Mirror of the `:0.6` verdict bug found the session before."""
    import importlib.util
    import pytest
    from pathlib import Path
    bin_dir = Path(__file__).resolve().parents[1] / "bin"
    spec = importlib.util.spec_from_file_location("agi_cli", bin_dir / "cli.py")
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)

    assert cli._normalize_confidence(0.65) == 0.65
    assert cli._normalize_confidence(0.0) == 0.0
    assert cli._normalize_confidence(1.0) == 1.0
    assert cli._normalize_confidence(65) == 0.65
    assert cli._normalize_confidence(100) == 1.0
    for bad in (-1, 101, 1000):
        with pytest.raises(ValueError):
            cli._normalize_confidence(bad)
