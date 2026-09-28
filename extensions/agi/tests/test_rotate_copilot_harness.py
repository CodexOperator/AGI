"""Conjunct 6 of `hypothesis:l4-copilot-cli-is-a-third-harness-with-the-same-
hooks-as-claude-code-and-pi`: `rotate.py`'s ONE launch path carries a THIRD
harness.

All fixture-only: no test starts a live `copilot`. The copilot argv is either
read from a dry-run string or built by `_build_copilot_command` directly; the
config rows are written into a tmp graph root, so a copy of the live model
list would not certify anything.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate


def _fake_bin(tmp_path, name):
    """A REAL, never-spawned harness binary.

    A path-shaped `bin` cell that does not exist now REFUSES by name
    (`hypothesis:harness-bin-absolute-token-free-bins-refused-by-name`), so a
    literal like `/fake/bin/copilot` can no longer stand in for a configured
    cell. Every call site here is a dry run -- no binary is ever executed.
    """
    p = tmp_path / "fake" / "bin" / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    p.chmod(0o755)
    return str(p)


def _root_with_harnesses(tmp_path, copilot_models, claude_models=None):
    """A tmp graph root whose `config.json` declares the two harness rows."""
    root = tmp_path / "graph"
    root.mkdir()
    (root / "config.json").write_text(json.dumps({
        "harnesses": {
            "claude-code": {
                "adapter": "claude_code",
                "models": claude_models or {"director": "claude-fable-5-1"},
            },
            "copilot-cli": {
                "adapter": "copilot_cli",
                "bin": _fake_bin(tmp_path, "copilot"),
                "models": copilot_models,
            },
        }
    }))
    return root


def test_copilot_spawn_builds_interactive_argv(tmp_path, capsys):
    """harness=copilot-cli -> `copilot --model M --allow-all --remote -i <card>`,
    and NOTHING from the claude remote-control shape."""
    prompt = tmp_path / "p.md"
    prompt.write_text("You are {name}\n")
    root = _root_with_harnesses(tmp_path, {"director": "auto"})

    rc, shell = rotate.spawn_window(
        name="cop-post", tier="director", prompt_file=str(prompt),
        dry_run=True, harness="copilot-cli", root=root)

    out = capsys.readouterr().out
    assert rc == 0
    assert out.strip() == shell
    assert f"{_fake_bin(tmp_path, 'copilot')} --model auto --allow-all --remote -i " in out
    assert "You are cop-post" in out
    assert "--debug-file" not in out
    assert "claude " not in out


def test_claude_spawn_is_byte_identical_when_harness_absent(tmp_path, capsys):
    """harness absent -> today's `claude --remote-control` line, unchanged."""
    prompt = tmp_path / "p.md"
    prompt.write_text("You are {name}\n")
    root = _root_with_harnesses(tmp_path, {"director": "auto"})

    rc, shell = rotate.spawn_window(
        name="cc-post", tier="director", prompt_file=str(prompt),
        dry_run=True, root=root)

    assert rc == 0
    assert "claude --remote-control cc-post" in shell
    assert "--permission-mode bypassPermissions" in shell
    assert "--debug-file" in shell
    assert "--model claude-fable-5-1" in shell
    assert "copilot" not in shell


def test_explicit_harness_claude_code_matches_absent(tmp_path, capsys):
    """`--harness claude-code` is the same line as no harness at all."""
    prompt = tmp_path / "p.md"
    prompt.write_text("You are {name}\n")
    root = _root_with_harnesses(tmp_path, {"director": "auto"})

    _, absent = rotate.spawn_window(
        name="cc-a", tier="director", prompt_file=str(prompt),
        dry_run=True, root=root)
    capsys.readouterr()
    _, explicit = rotate.spawn_window(
        name="cc-a", tier="director", prompt_file=str(prompt),
        dry_run=True, root=root, harness="claude-code")

    assert explicit == absent


def test_copilot_model_comes_from_its_own_row_never_claude(tmp_path, capsys):
    """The model is `harnesses.copilot-cli.models[tier]`; the claude-code row
    is not consulted (a claude name in a copilot argv would be a silent bug)."""
    prompt = tmp_path / "p.md"
    prompt.write_text("card\n")
    root = _root_with_harnesses(
        tmp_path, {"director": "gpt-copilot-x"},
        claude_models={"director": "claude-fable-5-1"})

    rc, shell = rotate.spawn_window(
        name="p", tier="director", prompt_file=str(prompt),
        dry_run=True, harness="copilot-cli", root=root)

    assert rc == 0
    assert "--model gpt-copilot-x" in shell
    assert "claude-fable-5-1" not in shell
    assert _fake_bin(tmp_path, "copilot") in shell


def test_copilot_row_without_tier_falls_back_to_director(tmp_path, capsys):
    prompt = tmp_path / "p.md"
    prompt.write_text("card\n")
    root = _root_with_harnesses(tmp_path, {"director": "auto"})

    rc, shell = rotate.spawn_window(
        name="p", tier="parent", prompt_file=str(prompt),
        dry_run=True, harness="copilot-cli", root=root)

    assert rc == 0
    assert "--model auto" in shell


def test_build_harness_command_dispatch():
    cop = rotate._build_harness_command(
        "copilot-cli", name="n", prompt_text="card", debug_file="d.log",
        model="auto", bin_path="/x/copilot")
    assert cop == ["/x/copilot", "--model", "auto", "--allow-all", "--remote",
                   "-i", "card"]
    claude = rotate._build_harness_command(
        None, name="n", prompt_text="card", debug_file="d.log", model="m")
    assert claude[0] == "claude"
    assert "--remote-control" in claude
    assert claude[-1] == "card"


def test_cmd_spawn_passes_harness_through(monkeypatch, tmp_path, capsys):
    """`spawn --harness copilot-cli` reaches spawn_window's `harness` kwarg."""
    root = _root_with_harnesses(tmp_path, {"director": "auto"})
    prompt = tmp_path / "p.md"
    prompt.write_text("card\n")
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    called = {}
    monkeypatch.setattr(
        rotate, "spawn_window",
        lambda **kw: called.update(kw) or (0, ""))

    rc = rotate.main(["spawn", "--name", "x", "--harness", "copilot-cli",
                      "--tier", "director", "--prompt-file", str(prompt),
                      "--dry-run"])

    assert rc == 0
    assert called.get("harness") == "copilot-cli"


def test_cmd_loop_passes_harness_through(monkeypatch, tmp_path, capsys):
    """`loop --harness copilot-cli` reaches spawn_window's `harness` kwarg."""
    root = _root_with_harnesses(tmp_path, {"director": "auto"})
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    called = {}
    monkeypatch.setattr(
        rotate, "spawn_window",
        lambda **kw: called.update(kw) or (0, ""))

    from types import SimpleNamespace
    rc = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=True, role="director", name="belam-x",
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=None,
        debug_file=None, dry_run=True, timeout=1,
        successor_argv=None, seat=None, harness="copilot-cli",
    ), root)

    assert rc == 0
    assert called.get("harness") == "copilot-cli"


def test_unknown_harness_is_refused_by_name(tmp_path, capsys):
    """A typo in `--harness` must NOT fall back to claude: rc != 0, an empty
    shell_cmd, and the declared list named on stderr. This is the defect kid 3's
    gate probe found (`does-not-exist` silently seated a claude post)."""
    prompt = tmp_path / "p.md"
    prompt.write_text("card\n")
    root = _root_with_harnesses(tmp_path, {"director": "auto"})

    rc, shell = rotate.spawn_window(
        name="bogus", tier="director", prompt_file=str(prompt),
        dry_run=True, harness="does-not-exist", root=root)

    err = capsys.readouterr().err
    assert rc != 0
    assert shell == ""
    assert "no harness 'does-not-exist' in config" in err
    assert "declared: ['claude-code', 'copilot-cli']" in err


def test_unknown_harness_refused_with_no_config_root(tmp_path, capsys):
    """With no config to consult (`root is None`) only the two known ids are
    accepted; anything else is refused by name, never a claude fallback."""
    prompt = tmp_path / "p.md"
    prompt.write_text("card\n")

    rc, shell = rotate.spawn_window(
        name="bogus", tier="director", prompt_file=str(prompt),
        dry_run=True, harness="copilot_cli", root=None)

    err = capsys.readouterr().err
    assert rc != 0
    assert shell == ""
    assert "no harness 'copilot_cli' in config" in err
    assert "'claude-code'" in err and "'copilot-cli'" in err


def test_known_harness_accepted_with_no_config_root(tmp_path, capsys):
    """`copilot-cli` with root is None is accepted and still builds copilot."""
    prompt = tmp_path / "p.md"
    prompt.write_text("card\n")

    rc, shell = rotate.spawn_window(
        name="cop", tier="director", prompt_file=str(prompt),
        dry_run=True, harness="copilot-cli", root=None)

    assert rc == 0
    assert "--allow-all" in shell
    assert "-i " in shell
    assert "--remote-control" not in shell


def test_declared_but_unbuildable_harness_refused(tmp_path, capsys):
    """A declared harness rotate.py has no builder for (`pi`) must not silently
    fall to the claude branch -- same cost defect, one name further out."""
    prompt = tmp_path / "p.md"
    prompt.write_text("card\n")
    root = _root_with_harnesses(tmp_path, {"director": "auto"})
    cfg = json.loads((root / "config.json").read_text())
    cfg["harnesses"]["pi"] = {"adapter": "pi", "models": {"kid": "x"}}
    (root / "config.json").write_text(json.dumps(cfg))

    rc, shell = rotate.spawn_window(
        name="p", tier="director", prompt_file=str(prompt),
        dry_run=True, harness="pi", root=root)

    err = capsys.readouterr().err
    assert rc != 0
    assert shell == ""
    assert "cannot build it" in err
    assert "bogus" not in err


# --- the resolution SOURCE is template data (hypothesis:harness-arg-builders-
# are-templates-only). The harness NAME must not branch the resolution; the
# template's `[roles] source` decides it. `_wire_template_dir` flips that field
# and shows the SAME harness follow a DIFFERENT source -- the falsifier that a
# hidden name branch survives.


def _wire_template_dir(tmp_path, copilot_source):
    """A copy of the shipped templates with copilot's `roles.source` flipped."""
    import re
    import shutil
    td = tmp_path / ("tmpl-" + copilot_source)
    td.mkdir()
    real = (Path(rotate.__file__).resolve().parent.parent
            / "templates" / "harness")
    for p in real.glob("*.toml"):
        shutil.copy(p, td / p.name)
    cop = td / "copilot-cli.toml"
    cop.write_text(re.sub(r'source = "row"',
                          f'source = "{copilot_source}"', cop.read_text()))
    return td


def _add_ladder(root, model):
    geom = root / "nodes" / ".geometry"
    geom.mkdir(parents=True, exist_ok=True)
    (geom / "ladder.md").write_text(
        "---\nroles:\n  - role: director\n"
        f"    model: {model}\n    effort: ladder-effort\n"
        "    tier: 2\nclosed: false\n---\n# ladder\n")


def _patch_templates(monkeypatch, td):
    monkeypatch.setattr(rotate.harness_template, "template_dir", lambda: td)
    import agi.bin.harness_template as ht
    monkeypatch.setattr(ht, "template_dir", lambda: td)


def test_copilot_resolution_follows_the_declared_source_not_its_name(
        tmp_path, capsys, monkeypatch):
    """WIRE PROBE: flip `[roles] source` and copilot's resolved model flips with
    it. `row` -> its own config row; `ladder` -> the shared ladder. If flipping
    the FIELD changes nothing, the branch moved into a helper, not into data."""
    prompt = tmp_path / "p.md"
    prompt.write_text("card\n")
    root = _root_with_harnesses(tmp_path, {"director": "ROW-MODEL"})
    _add_ladder(root, "LADDER-MODEL")

    _patch_templates(monkeypatch, _wire_template_dir(tmp_path, "ladder"))
    rc, from_ladder = rotate.spawn_window(
        name="p", tier="director", prompt_file=str(prompt), dry_run=True,
        harness="copilot-cli", root=root)
    capsys.readouterr()

    _patch_templates(monkeypatch, _wire_template_dir(tmp_path, "row"))
    rc2, from_row = rotate.spawn_window(
        name="p", tier="director", prompt_file=str(prompt), dry_run=True,
        harness="copilot-cli", root=root)

    assert rc == 0 and rc2 == 0
    assert "--model LADDER-MODEL" in from_ladder
    assert "--model ROW-MODEL" in from_row
    assert from_ladder != from_row


def test_fourth_harness_resolves_from_its_own_row_with_no_rotate_edit(
        tmp_path, capsys, monkeypatch):
    """A synthetic fourth template declaring `source = "row"` resolves its model
    from its own `harnesses.<id>` config row; rotate.py is not touched."""
    td = tmp_path / "tmpl4"
    td.mkdir()
    fake4 = _fake_bin(tmp_path, "fake4")
    (td / "fake4.toml").write_text(
        f'id = "fake4"\nbin = "{fake4}"\n'
        '[roles]\nsource = "row"\n'
        '[[argv]]\nflag = "--model"\nslot = "model"\n'
        '[[argv]]\nslot = "prompt"\n')
    _patch_templates(monkeypatch, td)
    prompt = tmp_path / "p.md"
    prompt.write_text("card\n")
    root = tmp_path / "graph"
    root.mkdir()
    (root / "config.json").write_text(json.dumps({"harnesses": {
        "fake4": {"adapter": "x", "bin": fake4,
                  "models": {"director": "ROW4"}}}}))

    rc, shell = rotate.spawn_window(
        name="p", tier="director", prompt_file=str(prompt), dry_run=True,
        harness="fake4", root=root)
    assert rc == 0
    assert "--model ROW4" in shell


def test_bogus_role_source_is_a_named_error_never_a_default(
        tmp_path, capsys, monkeypatch):
    """A template declaring an unknown `roles.source` fails closed by name."""
    td = tmp_path / "tmplbogus"
    td.mkdir()
    (td / "bogus.toml").write_text(
        'id = "bogus"\nbin = "/fake/bin/bogus"\n'
        '[roles]\nsource = "cosmic"\n'
        '[[argv]]\nslot = "prompt"\n')
    _patch_templates(monkeypatch, td)
    prompt = tmp_path / "p.md"
    prompt.write_text("card\n")
    root = tmp_path / "graph"
    root.mkdir()
    (root / "config.json").write_text(json.dumps({"harnesses": {
        "bogus": {"adapter": "x"}}}))

    rc, shell = rotate.spawn_window(
        name="p", tier="director", prompt_file=str(prompt), dry_run=True,
        harness="bogus", root=root)
    err = capsys.readouterr().err
    assert rc != 0
    assert shell == ""
    assert "unknown roles.source 'cosmic'" in err


def test_non_table_roles_refuses_the_seat_by_name_not_a_crash(
        tmp_path, capsys, monkeypatch):
    """A top-level `roles = "ladder"` (not a `[roles]` table) must reach the
    seat path's `except HarnessTemplateError` catch: rc != 0, empty command,
    `ERR:` on stderr -- never an AttributeError escaping the named refusal."""
    td = tmp_path / "tmplnontable"
    td.mkdir()
    (td / "nontable.toml").write_text(
        'id = "nontable"\nbin = "/fake/bin/nontable"\n'
        'roles = "ladder"\n'
        '[[argv]]\nslot = "prompt"\n')
    _patch_templates(monkeypatch, td)
    prompt = tmp_path / "p.md"
    prompt.write_text("card\n")
    root = tmp_path / "graph"
    root.mkdir()
    (root / "config.json").write_text(json.dumps({"harnesses": {
        "nontable": {"adapter": "x"}}}))

    rc, shell = rotate.spawn_window(
        name="p", tier="director", prompt_file=str(prompt), dry_run=True,
        harness="nontable", root=root)
    err = capsys.readouterr().err
    assert rc != 0
    assert shell == ""
    assert "roles is not a table" in err


def test_copilot_spawn_bin_is_home_expanded_before_argv(tmp_path, monkeypatch,
                                                        capsys):
    """Round 3 of hypothesis:harness-bin-paths-resolve-per-box: the row's
    `~/.npm-global/bin/copilot` cell reaches the spawn argv as the EXPANDED
    path under the current HOME, not the raw `~` literal that Popen dies on."""
    monkeypatch.delenv("COPILOT_BIN", raising=False)
    home = tmp_path / "home"
    bindir = home / ".npm-global" / "bin"
    bindir.mkdir(parents=True)
    fake = bindir / "copilot"
    fake.write_text("#!/bin/sh\n", encoding="utf-8")
    fake.chmod(0o755)
    monkeypatch.setenv("HOME", str(home))

    root = tmp_path / "graph"
    root.mkdir()
    (root / "config.json").write_text(json.dumps({"harnesses": {
        "copilot-cli": {"adapter": "copilot_cli",
                        "bin": "~/.npm-global/bin/copilot",
                        "models": {"director": "auto"}}}}))
    prompt = tmp_path / "p.md"
    prompt.write_text("card\n")
    capsys.readouterr()

    rc, shell = rotate.spawn_window(
        name="p", tier="director", prompt_file=str(prompt),
        dry_run=True, harness="copilot-cli", root=root)

    assert rc == 0, capsys.readouterr().err
    assert str(fake) in shell, shell
    assert "~/.npm-global" not in shell, shell
