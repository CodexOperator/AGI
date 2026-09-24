"""Conjunct 2 of `hypothesis:harness-arg-builders-are-templates-only`: the
spawn argv for every harness is produced from a TOML template plus a thin
hook, and a FOURTH harness renders with no edit to rotate.py.

Fixture-only: no test starts a live harness. Both seat builders are compared
to a FROZEN LITERAL argv (the old hand-built shape), never to
`harness_template.render`: the builders ARE that render, so comparing the two
is a tautology that pins nothing about the seat argv.
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import harness_template
from agi.bin import rotate
from agi.bin.adapters import pi_adapter


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
def test_claude_builder_renders_frozen_argv(model, effort, settings):
    """The PRODUCTION claude builder equals the OLD hand-built argv
    (rotate.py@8b6dcea1f), written out here as a literal: multi-token flag,
    JSON value, positional-last prompt. This pins the seat shape, so a
    dropped/renamed flag in claude-code.toml fails this test; asserting
    `== harness_template.render(...)` could not, since the builder IS that
    call."""
    expected = ["claude", "--remote-control", "N", "--permission-mode",
                "bypassPermissions", "--debug-file", "D.LOG"]
    if model:
        expected += ["--model", model]
    if effort:
        expected += ["--effort", effort]
    if settings:
        expected += ["--settings", json.dumps(settings)]
    expected.append("CARD")

    got = rotate._build_claude_command(
        "N", "CARD", "D.LOG", model=model, effort=effort, settings=settings)
    assert got == expected


def test_available_includes_shipped_harnesses():
    ids = harness_template.available()
    assert "copilot-cli" in ids
    assert "claude-code" in ids


@pytest.mark.parametrize("model,effort,extra", COPILOT_MATRIX)
def test_copilot_builder_renders_frozen_argv(model, effort, extra):
    """The PRODUCTION copilot builder equals the OLD hand-built argv
    (rotate.py@8b6dcea1f), the same literal shape frozen above. A dropped or
    renamed seat flag in copilot-cli.toml fails this; `== render(...)` could
    not, since the builder IS that call."""
    expected = ["/x/copilot"]
    if model:
        expected += ["--model", model]
    if effort:
        expected += ["--effort", effort]
    expected += ["--allow-all", "--remote", *extra, "-i", "CARD"]

    got = rotate._build_copilot_command(
        prompt_text="CARD", model=model, effort=effort,
        bin_path="/x/copilot", extra_args=extra)
    assert got == expected


# --- hypothesis:harness-template-emit-refuses-an-unknown-slot -----------
# An element whose `slot`/`when`/`spread` names a value outside the render
# vocabulary was silently dropped at emit (`values.get` -> None -> []). It is
# now refused BY NAME at check time, in top-level argv AND in a shape.

def test_unknown_slot_is_refused_by_name_at_check_time(tmp_path, monkeypatch):
    (tmp_path / "bad.toml").write_text(
        'id = "bad"\nbin = "b"\n[[argv]]\nflag = "--model"\n'
        'slot = "modell"\n')
    monkeypatch.setattr(harness_template, "template_dir", lambda: tmp_path)
    with pytest.raises(harness_template.HarnessTemplateError) as exc:
        harness_template.load("bad")
    assert "unknown slot 'modell'" in str(exc.value)


def test_unknown_when_is_refused_by_name_at_check_time(tmp_path, monkeypatch):
    (tmp_path / "bad.toml").write_text(
        'id = "bad"\nbin = "b"\n[[argv]]\nconst = "--verbose"\n'
        'when = "verbos"\n')
    monkeypatch.setattr(harness_template, "template_dir", lambda: tmp_path)
    with pytest.raises(harness_template.HarnessTemplateError) as exc:
        harness_template.load("bad")
    assert "unknown when 'verbos'" in str(exc.value)


def test_unknown_slot_inside_a_shape_is_refused(tmp_path, monkeypatch):
    (tmp_path / "bad.toml").write_text(
        'id = "bad"\nbin = "b"\n[shapes.d]\nargv = ['
        '{flag = "--x", slot = "nope"}]\n')
    monkeypatch.setattr(harness_template, "template_dir", lambda: tmp_path)
    with pytest.raises(harness_template.HarnessTemplateError) as exc:
        harness_template.load("bad")
    assert "unknown slot 'nope'" in str(exc.value)
    assert "shapes.d" in str(exc.value)


def test_known_slot_and_when_still_render(tmp_path, monkeypatch):
    """Regression guard: the known vocabulary is unchanged -- a known slot
    emits its flag/value and a known `when` still gates emission."""
    (tmp_path / "ok.toml").write_text(
        'id = "ok"\nbin = "b"\n[[argv]]\nflag = "--model"\n'
        'slot = "model"\n[[argv]]\nconst = "--verbose"\n'
        'when = "verbose"\n[[argv]]\nslot = "prompt"\n')
    monkeypatch.setattr(harness_template, "template_dir", lambda: tmp_path)
    assert harness_template.render(
        "ok", bin_path="b", prompt="P", model="m", verbose=True) == [
            "b", "--model", "m", "--verbose", "P"]
    assert harness_template.render(
        "ok", bin_path="b", prompt="P", model="m") == [
            "b", "--model", "m", "P"]


def test_render_vocabulary_matches_the_values_dict(tmp_path, monkeypatch):
    """One source of truth: every render() keyword is in RENDER_VOCABULARY
    and the emitted values dict has no key outside it."""
    import inspect
    params = set(inspect.signature(harness_template.render).parameters) - {
        "harness_id", "shape", "bin_path"}
    assert params == set(harness_template.RENDER_VOCABULARY)


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


# ------------------------------------------- pi: the dispatch-path harness


def test_pi_template_renders_the_flag_shape():
    """pi's headless argv, frozen: provider/model/thinking, `-p --mode json`,
    the spread prompt entries, then the positional closing line."""
    got = harness_template.render(
        "pi", prompt="CARD", bin_path="/x/pi", provider="openrouter",
        model="kid-m", thinking="medium",
        extra_args=["--append-system-prompt", "S"])
    assert got == ["/x/pi", "--provider", "openrouter", "--model", "kid-m",
                   "--thinking", "medium", "-p", "--mode", "json",
                   "--append-system-prompt", "S", "CARD"]
    # Absent keys emit NO flag, so pi's own settings keep winning.
    bare = harness_template.render("pi", prompt="CARD", bin_path="/x/pi")
    assert bare == ["/x/pi", "-p", "--mode", "json", "CARD"]


def test_pi_adapter_production_path_reaches_render(monkeypatch, tmp_path):
    """pi_adapter.build_command must render pi.toml, not build flags inline."""
    seen = {}

    def sentinel(harness_id, **kw):
        seen["id"] = harness_id
        return ["sentinel", *kw["extra_args"]]

    monkeypatch.setattr(pi_adapter.harness_template, "render", sentinel)
    monkeypatch.setenv("AGI_PI_TRAJECTORY_BYPASS", "1")
    got = pi_adapter.build_command(
        harness={"adapter": "pi", "models": {"kid": "m"}}, tier="kid",
        context_file="/tmp/ctx.md", agent_id="a00-x", iter_n=1,
        sess_dir=tmp_path, cli_py="/x/cli.py")
    assert seen["id"] == "pi"
    assert got[0] == "sentinel"
    assert pi_adapter.model_args({"models": {"kid": "m"}}, "kid") == \
        ["--model", "m"]


def test_pi_template_is_dispatch_only_not_a_rotate_seat():
    """`rotate = false` keeps pi out of the rotate seat set while its template
    is still available to the dispatch-path adapter."""
    assert "pi" in harness_template.available()
    assert harness_template.load("pi").get("rotate") is False
    assert "pi" not in rotate._known_harnesses()
    assert rotate._validate_harness(None, "pi")[0] == 1


def test_shipped_templates_declare_their_role_source():
    """The seat path reads WHERE role cells come from off the template:
    claude-code says `ladder`, copilot-cli says `row`, and an omitted field
    defaults to `ladder` (claude's unchanged behaviour)."""
    assert harness_template.role_source("claude-code") == "ladder"
    assert harness_template.role_source("copilot-cli") == "row"
    assert harness_template.load("pi").get("roles") is None  # omitted -> ladder
    assert harness_template.ROLE_SOURCES == ("ladder", "row")


# ------------------- per-template fail isolation in `_known_harnesses`
# (hypothesis:harness-arg-builders-are-templates-only). ONE malformed template
# used to abort the whole comprehension and collapse the buildable set to
# `("claude-code",)`, so a bad unrelated file made `copilot-cli`
# unlaunchable with the WRONG reason. Each template now fails alone.

BROKEN = 'id = "broken"\nbin = "broken"\n[[argv]]\nscript = "import os"\n'


def _seat_dir_with_broken(tmp_path, broken_name="broken",
                          break_claude=False):
    """Real templates + one malformed file whose name is caller-chosen."""
    import shutil
    td = tmp_path / f"seat-{broken_name}-{break_claude}"
    td.mkdir()
    real = harness_template.template_dir()
    for p in real.glob("*.toml"):
        shutil.copy(p, td / p.name)
    (td / f"{broken_name}.toml").write_text(BROKEN)
    if break_claude:
        (td / "claude-code.toml").write_text(BROKEN)
    return td


def _patch_seat_dir(monkeypatch, td):
    monkeypatch.setattr(harness_template, "template_dir", lambda: td)
    monkeypatch.setattr(rotate.harness_template, "template_dir", lambda: td)


def test_broken_template_excludes_only_itself_and_is_named(
        tmp_path, monkeypatch, capsys):
    """Falsifier 1: real claude-code + real copilot-cli + a malformed file.
    Both real harnesses stay buildable; the broken one is excluded and NAMED.
    Pre-fix this returned `("claude-code",)`."""
    _patch_seat_dir(monkeypatch, _seat_dir_with_broken(tmp_path))

    known = rotate._known_harnesses()
    err = capsys.readouterr().err

    assert "claude-code" in known
    assert "copilot-cli" in known
    assert "broken" not in known
    assert "'broken'" in err and "malformed" in err
    assert "HarnessTemplateError" in err
    assert err.count("ERR:") == 1  # quiet about the healthy files


def test_broken_sibling_does_not_unbuild_copilot(tmp_path, monkeypatch,
                                                 capsys):
    """Falsifier 2: with `broken.toml` present, the validator ACCEPTS
    copilot-cli and the builder still emits copilot argv. Pre-fix the
    validator refused it -- the live cost."""
    _patch_seat_dir(monkeypatch, _seat_dir_with_broken(tmp_path))
    root = tmp_path / "graph"
    root.mkdir()
    (root / "config.json").write_text(json.dumps({"harnesses": {
        "claude-code": {"adapter": "claude_code"},
        "copilot-cli": {"adapter": "copilot_cli", "bin": "/x/copilot"},
    }}))
    capsys.readouterr()

    assert rotate._validate_harness(root, "copilot-cli")[0] == 0
    got = rotate._build_harness_command(
        "copilot-cli", name="n", prompt_text="CARD", debug_file="D.LOG",
        model="auto", bin_path="/x/copilot")
    assert got == ["/x/copilot", "--model", "auto", "--allow-all",
                   "--remote", "-i", "CARD"]


def test_broken_claude_does_not_remove_copilot(tmp_path, monkeypatch,
                                               capsys):
    """Falsifier 3 (reverse): a malformed `claude-code.toml` must not remove
    `copilot-cli`. No 'the default survived so we are fine'."""
    _patch_seat_dir(monkeypatch,
                    _seat_dir_with_broken(tmp_path, broken_name="junk",
                                          break_claude=True))
    known = rotate._known_harnesses()
    capsys.readouterr()
    assert "copilot-cli" in known
    assert "claude-code" not in known


def test_unknown_id_still_refused_and_whole_enum_fallback(
        tmp_path, monkeypatch, capsys):
    """Falsifier 4: an unknown id is still refused BY NAME, and a failure of
    `available()` ITSELF (no enumeration at all) still yields the documented
    `("claude-code",)` fallback -- a distinction the old code could not make."""
    _patch_seat_dir(monkeypatch, _seat_dir_with_broken(tmp_path))
    assert rotate._validate_harness(None, "does-not-exist")[0] == 1
    assert "does-not-exist" in capsys.readouterr().err

    def boom():
        raise OSError("template dir vanished")
    monkeypatch.setattr(rotate.harness_template, "available", boom)
    assert rotate._known_harnesses() == ("claude-code",)
    assert "cannot enumerate" in capsys.readouterr().err


def test_load_all_reports_broken_by_name_and_keeps_siblings(tmp_path,
                                                            monkeypatch):
    """The reader itself: `load_all()` returns `(loaded, broken)`; a broken id
    is in `broken` with its error text, its siblings are in `loaded`."""
    _patch_seat_dir(monkeypatch, _seat_dir_with_broken(tmp_path))
    loaded, broken = rotate.harness_template.load_all()
    assert "claude-code" in loaded and "copilot-cli" in loaded
    assert "broken" not in loaded
    assert "broken" in broken and "HarnessTemplateError" in broken["broken"]


def test_unknown_role_source_is_a_named_error(tmp_path, monkeypatch):
    (tmp_path / "weird.toml").write_text(
        'id = "weird"\nbin = "w"\n[roles]\nsource = "cosmic"\n')
    monkeypatch.setattr(harness_template, "template_dir", lambda: tmp_path)
    with pytest.raises(harness_template.HarnessTemplateError) as exc:
        harness_template.role_source("weird")
    assert "unknown roles.source 'cosmic'" in str(exc.value)


def test_non_table_roles_is_a_named_error(tmp_path, monkeypatch):
    """`roles` as a bare string (not a `[roles]` table) is refused BY NAME by
    both `load` and its reader `role_source` -- never a bare AttributeError
    escaping the seat path's `except HarnessTemplateError` catch."""
    (tmp_path / "bad.toml").write_text(
        'id = "bad"\nbin = "b"\nroles = "ladder"\n')
    monkeypatch.setattr(harness_template, "template_dir", lambda: tmp_path)
    with pytest.raises(harness_template.HarnessTemplateError) as exc:
        harness_template.load("bad")
    assert "roles is not a table" in str(exc.value)
    with pytest.raises(harness_template.HarnessTemplateError) as exc:
        harness_template.role_source("bad")
    assert "roles is not a table" in str(exc.value)


@pytest.mark.parametrize("literal", ['"xyz"', "3", '{a = "b"}'])
def test_non_list_argv_is_a_named_error(tmp_path, monkeypatch, literal):
    """A non-list top-level `argv` -- a string, number or inline table -- is
    refused BY NAME, never a TypeError from iterating an int nor a silently
    accepted string/dict that `render()` then walks as tokens."""
    (tmp_path / "bad.toml").write_text(
        f'id = "bad"\nbin = "b"\nargv = {literal}\n')
    monkeypatch.setattr(harness_template, "template_dir", lambda: tmp_path)
    with pytest.raises(harness_template.HarnessTemplateError) as exc:
        harness_template.load("bad")
    assert "argv is not a list" in str(exc.value)


def test_non_table_shapes_is_a_named_error(tmp_path, monkeypatch):
    """`shapes` as a bare string (not `[shapes.<name>]` tables) is refused BY
    NAME, never an AttributeError from calling `.items()` on a str."""
    (tmp_path / "bad.toml").write_text(
        'id = "bad"\nbin = "b"\nshapes = "x"\n')
    monkeypatch.setattr(harness_template, "template_dir", lambda: tmp_path)
    with pytest.raises(harness_template.HarnessTemplateError) as exc:
        harness_template.load("bad")
    assert "shapes is not a table" in str(exc.value)


@pytest.mark.parametrize("literal", ['"xyz"', "3", '{a = "b"}'])
def test_non_list_shape_argv_is_a_named_error(tmp_path, monkeypatch, literal):
    """A non-list `shapes.<name>.argv` is refused BY NAME, same discipline as
    the top-level one -- `render(..., shape=...)` must never iterate
    a string, number or dict-as-tokens."""
    (tmp_path / "bad.toml").write_text(
        f'id = "bad"\nbin = "b"\n[shapes.d]\nargv = {literal}\n')
    monkeypatch.setattr(harness_template, "template_dir", lambda: tmp_path)
    with pytest.raises(harness_template.HarnessTemplateError) as exc:
        harness_template.load("bad")
    assert "shapes.d.argv is not a list" in str(exc.value)


def test_render_expands_a_home_token_bin_through_the_one_resolver(
        tmp_path, monkeypatch):
    """Round 3 of hypothesis:harness-bin-paths-resolve-per-box: `render()` has
    no graph root, so a raw `~/.npm-global/bin/...` cell in the template is
    expanded against the CURRENT HOME. Pre-fix the raw `~` literal reached
    argv[0] and `Popen` died with FileNotFoundError('~/...') naming nothing."""
    home = tmp_path / "home"
    bindir = home / ".npm-global" / "bin"
    bindir.mkdir(parents=True)
    fake = bindir / "pi"
    fake.write_text("#!/bin/sh\n", encoding="utf-8")
    fake.chmod(0o755)
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("HOME_HARNESS_BIN", raising=False)

    td = tmp_path / "tmpl"
    td.mkdir()
    (td / "home-harness.toml").write_text(
        'id = "home-harness"\nbin = "~/.npm-global/bin/pi"\n'
        '[[argv]]\nslot = "prompt"\n')
    monkeypatch.setattr(harness_template, "template_dir", lambda: td)

    got = harness_template.render("home-harness", prompt="CARD")
    assert got == [str(fake), "CARD"]


#: (harness id, the ONE env var its adapter owns) -- round 3b of
#: hypothesis:harness-bin-paths-resolve-per-box. The hyphenated ids must map
#: to the CONVENTIONAL name (`CLAUDE_BIN`/`COPILOT_BIN`), never a second
#: derived `<ID>_BIN` convention that only render() honours.
ADAPTER_OVERRIDES = [
    ("claude-code", "CLAUDE_BIN"),
    ("copilot-cli", "COPILOT_BIN"),
    ("pi", "PI_BIN"),
]

_REFUSED_DERIVED = ("CLAUDE_CODE_BIN", "COPILOT_CLI_BIN")


@pytest.mark.parametrize("harness,env_var", ADAPTER_OVERRIDES)
def test_render_honours_the_adapters_one_env_override(
        harness, env_var, tmp_path, monkeypatch):
    """`render()` must consult the SAME override the adapter's `resolve_bin`
    does, so a box that exports the documented var gets it in argv[0]. Pre-fix
    the hyphenated ids derived `$CLAUDE_CODE_BIN`/`$COPILOT_CLI_BIN` and
    silently ignored the conventional name on the live seat path."""
    fake = tmp_path / "the-binary"
    fake.write_text("#!/bin/sh\n", encoding="utf-8")
    fake.chmod(0o755)
    for name in ("CLAUDE_BIN", "COPILOT_BIN", "PI_BIN", *_REFUSED_DERIVED):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv(env_var, str(fake))

    assert harness_template.render(harness, prompt="CARD")[0] == str(fake)


@pytest.mark.parametrize("harness,env_var", ADAPTER_OVERRIDES)
def test_render_ignores_a_second_derived_override_name(
        harness, env_var, tmp_path, monkeypatch):
    """The derived `<ID>_BIN` is not a name any adapter uses; honouring it
    instead of the adapter's var is the round-3b defect. With ONLY the derived
    name set the bare template cell (not on PATH) must come through unchanged."""
    fake = tmp_path / "the-binary"
    fake.write_text("#!/bin/sh\n", encoding="utf-8")
    fake.chmod(0o755)
    derived = harness.upper().replace("-", "_") + "_BIN"
    if derived == env_var:
        pytest.skip("single-word harness has no second convention")
    for name in ("CLAUDE_BIN", "COPILOT_BIN", "PI_BIN", *_REFUSED_DERIVED):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv(derived, str(fake))

    got = harness_template.render(harness, prompt="CARD")[0]
    assert got != str(fake)
    assert got == harness_template.load(harness)["bin"]  # the bare cell


def test_every_adapter_exports_the_env_var_it_resolves():
    """ONE name per harness: the module constant `harness_template._first_arg`
    reads is the same string the adapter's own `resolve_bin` passes."""
    import importlib

    for adapter_name, expected in (("pi", "PI_BIN"),
                                   ("claude_code", "CLAUDE_BIN"),
                                   ("copilot_cli", "COPILOT_BIN"),
                                   ("grok_bot", "GROK_BOT_BIN")):
        mod = importlib.import_module(f"agi.bin.adapters.{adapter_name}_adapter")
        assert mod.ENV_VAR == expected


# --- hypothesis:harness-argv-refuses-an-unknown-encoding ----------------
# `_check_parts` validated `slot`/`when`/`spread` but not `encoding`; `_emit`
# turned ANY non-json encoding into plain `str()`. A typo'd
# `encoding = "json5"` therefore emitted the wrong bytes silently. The
# encoding vocabulary is now closed and checked by name, and the unknown
# `spread` refusal gets its own pin (R-EF50 M4).

def test_unknown_encoding_is_refused_by_name_at_check_time(tmp_path, monkeypatch):
    (tmp_path / "bad.toml").write_text(
        'id = "bad"\nbin = "b"\n[[argv]]\nflag = "--settings"\n'
        'slot = "settings"\nencoding = "json5"\n')
    monkeypatch.setattr(harness_template, "template_dir", lambda: tmp_path)
    with pytest.raises(harness_template.HarnessTemplateError) as exc:
        harness_template.load("bad")
    assert "unknown encoding 'json5'" in str(exc.value)


def test_unknown_encoding_inside_a_shape_is_refused(tmp_path, monkeypatch):
    (tmp_path / "bad.toml").write_text(
        'id = "bad"\nbin = "b"\n[shapes.d]\nargv = ['
        '{flag = "--settings", slot = "settings", encoding = "yaml"}]\n')
    monkeypatch.setattr(harness_template, "template_dir", lambda: tmp_path)
    with pytest.raises(harness_template.HarnessTemplateError) as exc:
        harness_template.load("bad")
    assert "unknown encoding 'yaml'" in str(exc.value)
    assert "shapes.d" in str(exc.value)


def test_known_json_encoding_still_renders(tmp_path, monkeypatch):
    """Regression guard: the closed vocabulary keeps the one live encoding."""
    (tmp_path / "ok.toml").write_text(
        'id = "ok"\nbin = "b"\n[[argv]]\nflag = "--settings"\n'
        'slot = "settings"\nencoding = "json"\n')
    monkeypatch.setattr(harness_template, "template_dir", lambda: tmp_path)
    assert harness_template.render(
        "ok", bin_path="b", prompt="P", settings={"a": 1}) == [
            "b", "--settings", '{"a": 1}']


def test_unknown_spread_is_refused_by_name_at_check_time(tmp_path, monkeypatch):
    """The pin R-EF50 M4 asked for: an unknown `spread` is refused, and the
    message names the bad token."""
    (tmp_path / "bad.toml").write_text(
        'id = "bad"\nbin = "b"\n[[argv]]\nspread = "extra"\n')
    monkeypatch.setattr(harness_template, "template_dir", lambda: tmp_path)
    with pytest.raises(harness_template.HarnessTemplateError) as exc:
        harness_template.load("bad")
    assert "unknown spread 'extra'" in str(exc.value)
