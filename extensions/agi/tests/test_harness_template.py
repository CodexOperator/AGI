"""Conjunct 2 of `hypothesis:harness-arg-builders-are-templates-only`: the
spawn argv for every harness is produced from a TOML template plus a thin
hook, and a FOURTH harness renders with no edit to rotate.py.

Fixture-only: no test starts a live harness. The copilot expected argv is
frozen (a literal), while claude is compared directly to
`rotate._build_claude_command` — no copied literals for the claude shape.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import harness_template
from agi.bin import rotate


COPILOT_MATRIX = [
    (None, None, []),
    ("auto", None, []),
    (None, "high", []),
    ("auto", "high", []),
    (None, None, ["--foo", "bar"]),
    ("auto", "high", ["--x"]),
]


@pytest.mark.parametrize("model,effort,extra", COPILOT_MATRIX)
def test_copilot_template_renders_frozen_argv(model, effort, extra):
    """Byte-for-byte against the shape rotate.py built by hand until now:
    `copilot [--model M] [--effort E] --allow-all --remote [extra...] -i P`."""
    expected = ["/x/copilot"]
    if model:
        expected += ["--model", model]
    if effort:
        expected += ["--effort", effort]
    expected += ["--allow-all", "--remote", *extra, "-i", "CARD"]

    got = harness_template.render(
        "copilot-cli", prompt="CARD", model=model, effort=effort,
        bin_path="/x/copilot", extra_args=extra)
    assert got == expected
    # and NOT claude's shape
    assert "--debug-file" not in got and "--remote-control" not in got


CLAUDE_MATRIX = [
    (None, None, None),
    ("m1", None, None),
    (None, "e1", None),
    ("m1", "e1", {"a": 1}),
    ("m1", "e1", "ultracode"),
]


@pytest.mark.parametrize("model,effort,settings", CLAUDE_MATRIX)
def test_claude_template_matches_build_claude_command(model, effort, settings):
    """The format must express claude-code exactly: multi-token flag, JSON
    value, positional-last prompt. Production claude is NOT rewired."""
    expected = rotate._build_claude_command(
        "N", "CARD", "D.LOG", model=model, effort=effort, settings=settings)
    got = harness_template.render(
        "claude-code", prompt="CARD", name="N", debug_file="D.LOG",
        model=model, effort=effort, settings=settings)
    assert got == expected


def test_available_includes_shipped_harnesses():
    ids = harness_template.available()
    assert "copilot-cli" in ids
    assert "claude-code" in ids


def test_copilot_builder_is_now_template_backed():
    """The production builder equals the render, and the old flag literals
    are gone from it."""
    got = rotate._build_copilot_command(
        prompt_text="CARD", model="auto", bin_path="/x/copilot",
        extra_args=["--z"])
    assert got == harness_template.render(
        "copilot-cli", prompt="CARD", model="auto", bin_path="/x/copilot",
        extra_args=["--z"])


def test_unknown_template_is_a_named_error():
    with pytest.raises(harness_template.UnknownHarnessError) as exc:
        harness_template.load("does-not-exist")
    assert "does-not-exist" in str(exc.value)


FAKE = """\
id = "fake-harness"
bin = "fakebin"

[[argv]]
flag = "--tier"
slot = "model"

[[argv]]
const = "--static"

[[argv]]
spread = "extra_args"

[[argv]]
slot = "prompt"
"""


def test_synthetic_fourth_harness_renders_without_editing_rotate(
        tmp_path, monkeypatch):
    """The direct measurement of falsifier conjunct 2: drop a new `.toml` in
    the template dir and it renders — no rotate.py edit, no allowlist."""
    (tmp_path / "fake-harness.toml").write_text(FAKE)
    monkeypatch.setattr(harness_template, "template_dir", lambda: tmp_path)
    # rotate imports the module under its bare name (house style), so the same
    # file is a second module object there; patch both references.
    monkeypatch.setattr(rotate.harness_template, "template_dir", lambda: tmp_path)

    got = harness_template.render(
        "fake-harness", prompt="CARD", model="strong", bin_path="fakebin",
        extra_args=["-v"])
    assert got == ["fakebin", "--tier", "strong", "--static", "-v", "CARD"]
    assert "fake-harness" in harness_template.available()
    # Buildability follows the template: rotate accepts it with no allowlist.
    assert rotate._validate_harness(None, "fake-harness")[0] == 0


def test_template_vocabulary_has_no_scripting_escape_hatch(tmp_path,
                                                           monkeypatch):
    """A key outside the declarative vocabulary is a hard error, so a
    template can never become a program."""
    (tmp_path / "evil.toml").write_text(
        'id = "evil"\nbin = "e"\n[[argv]]\nscript = "import os"\n')
    monkeypatch.setattr(harness_template, "template_dir", lambda: tmp_path)
    with pytest.raises(harness_template.HarnessTemplateError):
        harness_template.load("evil")

def test_build_harness_command_dispatches_on_template(tmp_path, monkeypatch):
    """`_build_harness_command` must BUILD a fourth harness from its template,
    not silently fall through to claude (the hole kid 1 left open). Asserting
    the BUILT argv, not `_validate_harness`'s return code."""
    (tmp_path / "fake-harness.toml").write_text(FAKE)
    monkeypatch.setattr(harness_template, "template_dir", lambda: tmp_path)
    monkeypatch.setattr(rotate.harness_template, "template_dir", lambda: tmp_path)

    got = rotate._build_harness_command(
        "fake-harness", name="N", prompt_text="CARD", debug_file="D.LOG",
        model="strong")
    assert got == ["fakebin", "--tier", "strong", "--static", "CARD"]
    assert got[0] != "claude"


def test_build_harness_command_refuses_unknown_never_claude(monkeypatch):
    """An id with no template raises by name -- never a silent claude argv."""
    # rotate imports the module under its bare name, so its exception class
    # is a second object; assert against the class the builder actually raises.
    with pytest.raises(rotate.harness_template.UnknownHarnessError):
        rotate._build_harness_command(
            "no-such-harness", name="N", prompt_text="CARD", debug_file="D.LOG")


def test_claude_production_path_reaches_render(monkeypatch):
    """The claude production build must go THROUGH harness_template.render,
    not an inline argv (parent probe on conjunct 1)."""
    seen = {}

    def sentinel(harness_id, **kw):
        seen["id"] = harness_id
        seen["kw"] = kw
        return ["sentinel"]

    monkeypatch.setattr(rotate.harness_template, "render", sentinel)
    got = rotate._build_harness_command(
        None, name="N", prompt_text="CARD", debug_file="D.LOG", model="m",
        settings={"a": 1})
    assert got == ["sentinel"]
    assert seen["id"] == "claude-code"
    assert seen["kw"]["name"] == "N"
    assert seen["kw"]["settings"] == {"a": 1}
