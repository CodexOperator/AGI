from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[3]
MODULE = ROOT / "extensions/agi/bin/prose_templates.py"


def _load():
    spec = importlib.util.spec_from_file_location("prose_templates", MODULE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_rotation_alert_templates_are_byte_identical():
    mod = _load()
    assert mod.render("rotation_alert", "at_or_over_title") == "## ⚠️  ROTATION OWED NOW — at or over the line"
    assert mod.render("rotation_alert", "imperative") == (
        "ROTATE NOW: (a) write the card wholesale now, (b) run python3 "
        "extensions/agi/bin/rotate.py rotate; nothing else this turn"
    )
    assert mod.render("rotation_alert", "beneath_title") == "## ⚠️  approaching rotation"
    assert mod.render("rotation_alert", "defer_prefix") == "rotation deferred: merge-up in flight"
    assert mod.render(
        "rotation_alert", "at_or_over_body",
        suffix="\n\nRotation spawned in the background for this seat (rotate-out ZERO calls); the stops line is landing on its card. The command below inspects/rotates by hand if needed.",
    ) == (
        "This session is at or over its rotation line. Rotate NOW. If you were mid-round, hand off cleanly first."
        "\n\nRotation spawned in the background for this seat (rotate-out ZERO calls); the stops line is landing on its card. The command below inspects/rotates by hand if needed."
    )
    assert mod.render(
        "rotation_alert", "beneath_body", fraction=0.4444, threshold=0.47,
        percent=94.55, pct=44,
    ) == (
        "Approaching rotation (0.4444 of 0.470 window (94.55% of the line)). "
        "Crossed band 44% of threshold. Keep working; at the line run rotate.py rotate yourself."
    )


def test_missing_field_is_named():
    mod = _load()
    try:
        mod.render("rotation_alert", "beneath_body", fraction=0.4, threshold=0.5)
    except mod.TemplateFieldError as exc:
        assert "percent" in str(exc)
    else:
        raise AssertionError("missing field did not raise TemplateFieldError")
