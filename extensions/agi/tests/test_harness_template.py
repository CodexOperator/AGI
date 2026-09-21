"""Conjunct 2 of `hypothesis:harness-arg-builders-are-templates-only`: the
spawn argv for every harness is produced from a TOML template plus a thin
hook, and a FOURTH harness renders with no edit to rotate.py.

Fixture-only: no test starts a live harness. Both seat builders are compared
to a FROZEN LITERAL argv (the old hand-built shape), never to
`harness_template.render`: the builders ARE that render, so comparing the two
is a tautology that pins nothing about the seat argv.
"""
import ast
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

    got = rotate._build_harness_command(
        "claude-code", name="N", prompt_text="CARD", debug_file="D.LOG",
        model=model, effort=effort, settings=settings)
    assert got == expected


# ---------------------------------------------------------------------------
# goal:g7.31.2.3 -- the GENERAL gate: rotate.py stays orchestration.
#
# The old test here (goal:g7.27.1) asserted two hard-coded substrings,
# `_build_claude_command` and `_build_copilot_command`. It would NOT have
# caught `_build_grok_command`, `_build_grok_argv`, `_grok_command`, or an
# `if harness == "grok":` branch -- i.e. exactly the drift a FOURTH harness
# invites. These three detectors scan rotate.py's SOURCE via `ast` (so a
# docstring mention is not a builder) and report every offender BY NAME.

#: The ONE function allowed to build a harness argv (goal:g7.27/g7.29).
ARGV_SEAM = "_build_harness_command"

#: Every argv-suffixed def in rotate.py at the time of writing, each reviewed
#: as NOT a harness argv builder: two wrap the seam, the rest build tmux /
#: launch-wrapper / session-resume argvs. A NEW name in this shape is
#: reported, so this list grows by review, never by accident.
_ALLOWED_ARGV_HELPERS = frozenset({
    ARGV_SEAM,                       # the sole harness argv seam
    "_successor_command",            # wraps ARGV_SEAM
    "_assembled_successor_command",  # wraps ARGV_SEAM
    "_launch_wrapper_argv",          # launch-wrapper argv, not a harness
    "_wm_tool_argv",                 # tmux window-manager argv, not a harness
    "_ack_call_args",                # ack-call args, not a harness
    "_run_after_join_command",       # shell cmd run after join
    "_fork_resume_command",          # session-resume argv
})
_ARGV_SUFFIX = ("_command", "_argv", "_args")

#: Shipped harness ids whose literals already exist (the default validation
#: in `_validate_harness`, and the copilot watch-message branch). Any OTHER
#: literal is a fourth-harness decision -- the very thing that must not
#: reappear.
_SHIPPED_HARNESS_IDS = frozenset({"claude-code", "copilot-cli"})

#: Every id a per-harness branch could plausibly name, read off the shipped
#: template dir (`claude-code`, `copilot-cli`, `pi`) plus config.json's
#: declared harnesses (`pi-local`, `grok-bot`) plus the proposed `grok`. A
#: literal EQUAL to one of these in rotate.py CODE is an offender unless it
#: is shipped.
_KNOWN_HARNESS_IDS = _SHIPPED_HARNESS_IDS | frozenset(
    {"pi", "pi-local", "grok", "grok-bot"})

#: Underscore-delimited name tokens that make a def harness-specific even when
#: it lacks an argv suffix: `_grok_flags`, `_build_grok`, `_grok_cmd`. `code`
#: is deliberately NOT a token -- the live file legitimately has `_code_head`
#: and `_code_loaded_identity`.
_HARNESS_TOKENS = frozenset({"grok", "claude", "copilot", "pi"})


def _argv_builder_offenders(source: str) -> list[str]:
    """Names of functions in `source` whose name says "argv builder" -- via
    an argv suffix (`*_command`/`*_argv`/`*_args`) OR a harness-token in an
    underscore-delimited word (`_grok_flags`, `_build_grok`, `_grok_cmd`) --
    but which are neither the seam nor an allowlisted non-harness helper.
    The token set excludes `code`, so the live `_code_head` is untouched.
    """
    tree = ast.parse(source)
    return sorted({
        node.name for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name not in _ALLOWED_ARGV_HELPERS
        and (node.name.endswith(_ARGV_SUFFIX)
             or set(node.name.split("_")) & _HARNESS_TOKENS)
    })


def _mentions_harness(node) -> bool:
    """True when `node` reads the harness id -- by NAME `harness`, or via
    `getattr(args, 'harness', None)`. A WORD test, not a substring: the
    unparsed `harness_template.role_source(...)` must not match (its only
    `harness` token is `harness_template`)."""
    import re
    return "harness" in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", ast.unparse(node))


def _string_constants(node) -> list[str]:
    return [n.value for n in ast.walk(node)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)]


def _harness_branch_offenders(source: str) -> list[str]:
    """Harness-id literals decided against a harness READ, whatever the LHS
    shape. Flagged: a string constant compared with `==`/`!=` whose OTHER
    operand reads the harness (`getattr(args, 'harness', None) == 'grok'`),
    and every KNOWN harness id inside a container tested by `in`/`not in`
    against such a read (`harness in ('grok', 'x')` reports `grok`, not the
    harmless neighbouring `x`). Shipped ids stay allowed.

    HEURISTIC, NOT EXHAUSTIVE, on purpose: the container arm is intersected
    with `_KNOWN_HARNESS_IDS`, so a genuinely NOVEL id sitting in a container
    (`harness in ('newharness', 'x')`) is invisible to this arm -- only the
    literal scan could see it, and only if the id is known to it too. A
    novel id smuggled into a membership test is still gate-blind; extend
    `_KNOWN_HARNESS_IDS` when a new harness is proposed. The `==`/`!=` arm
    is NOT narrowed: a bare comparison against a harness read names the id
    directly, so any string there is a harness decision."""
    tree = ast.parse(source)
    found = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Compare):
            continue
        operands = [node.left, *node.comparators]
        for i, op in enumerate(node.ops):
            left, right = operands[i], operands[i + 1]
            if isinstance(op, (ast.Eq, ast.NotEq)):
                for const, other in ((right, left), (left, right)):
                    if isinstance(const, ast.Constant) and \
                            isinstance(const.value, str) and \
                            _mentions_harness(other):
                        found.add(const.value)
            if isinstance(op, (ast.In, ast.NotIn)) and \
                    not isinstance(left, ast.Constant) and \
                    _mentions_harness(left):
                # NARROW (DH.28): only KNOWN ids are harness decisions; a
                # harmless neighbouring string in the container is not.
                found.update(set(_string_constants(right))
                             & _KNOWN_HARNESS_IDS)
    return sorted(found - _SHIPPED_HARNESS_IDS)


def _docstring_const_ids(tree) -> set[int]:
    """`id()` of every docstring Constant node, so the literal scan can skip
    them: documenting a retired harness id must not fail the suite."""
    ids = set()
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if isinstance(body, list) and body and \
                isinstance(body[0], ast.Expr) and \
                isinstance(body[0].value, ast.Constant) and \
                isinstance(body[0].value.value, str):
            ids.add(id(body[0].value))
    return ids


def _harness_id_literal_offenders(source: str) -> list[str]:
    """Known harness ids appearing as bare string literals in `source` CODE
    other than the shipped two -- `"grok"` anywhere but a docstring is a
    per-harness decision smuggled past the branch gate."""
    tree = ast.parse(source)
    docstrings = _docstring_const_ids(tree)
    return sorted({
        node.value for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and id(node) not in docstrings
        and node.value in _KNOWN_HARNESS_IDS
        and node.value not in _SHIPPED_HARNESS_IDS
    })


def _render_call_owners(source: str) -> list[str]:
    """Functions in `source` that call `harness_template.render(...)` -- the
    template seam. Only the seam itself may."""
    tree = ast.parse(source)
    owners = []
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for node in ast.walk(fn):
            if isinstance(node, ast.Call) and \
                    isinstance(node.func, ast.Attribute) and \
                    node.func.attr == "render" and \
                    isinstance(node.func.value, ast.Name) and \
                    node.func.value.id == "harness_template":
                owners.append(fn.name)
    return sorted(set(owners))


def test_rotate_stays_orchestration_only():
    """goal:g7.31.2.3 falsifier: rotate.py grows ZERO new harness argv
    builders. Reports the offender by name rather than a bare assertion."""
    src = Path(rotate.__file__).read_text(encoding="utf-8")
    offenders = (_argv_builder_offenders(src)
                 + _harness_branch_offenders(src)
                 + _harness_id_literal_offenders(src)
                 + [o for o in _render_call_owners(src) if o != ARGV_SEAM])
    assert offenders == [], (
        "rotate.py grew a harness argv builder (goal:g7.31.2.3: "
        f"orchestration only, sole seam {ARGV_SEAM!r}). Offenders: "
        f"{offenders}")


def test_gate_flags_a_synthetic_grok_builder():
    """Non-vacuity: the gate must SEE an added builder. A gate that cannot
    fail is theater."""
    for name in ("_build_grok_command", "_build_grok_argv",
                 "_grok_command"):
        src = f"def {name}(*a, **k):\n    return ['grokbin']\n"
        offenders = _argv_builder_offenders(src)
        assert name in offenders, f"gate blind to {name}"


def test_gate_flags_a_synthetic_grok_branch():
    """Non-vacuity for per-harness BRANCHES: `if harness == "grok":` is a
    fourth-harness dispatch and is reported by its literal."""
    src = ('def f(harness):\n'
           '    if harness == "grok":\n'
           '        return ["grokbin"]\n')
    assert _harness_branch_offenders(src) == ["grok"]


def test_gate_flags_a_second_render_seam():
    """Non-vacuity: a second `harness_template.render` call outside the seam
    is reported by its enclosing function."""
    src = ("def _grok_command(harness):\n"
           "    return harness_template.render('grok')\n")
    assert _render_call_owners(src) == ["_grok_command"]


def test_gate_flags_getattr_harness_comparison():
    """Parent probe 1 (WIRE): the LIVE idiom at rotate.py:2191 is
    `getattr(args, "harness", None) == "copilot-cli"`, so a grok branch in
    the file's own style must not walk through. The old detector required a
    bare `harness` Name on the left and was BLIND to this."""
    src = ('def f(args):\n'
           '    if getattr(args, "harness", None) == "grok":\n'
           '        return ["grokbin"]\n')
    assert _harness_branch_offenders(src) == ["grok"]


def test_gate_flags_harness_membership_container():
    """Parent probe 2 (GATE): `harness in ("grok", "x")` is a membership
    dispatch; the unshipped KNOWN id is reported, and the harmless
    neighbouring `"x"` is NOT -- only known ids are harness decisions
    (DH.28 narrow: over-flagging `x` was a false positive)."""
    src = ('def f(harness):\n'
           '    if harness in ("grok", "x"):\n'
           '        return ["grokbin"]\n')
    assert _harness_branch_offenders(src) == ["grok"]


def test_gate_ignores_a_container_of_only_harmless_strings():
    """Non-vacuity in the other direction for the NARROWED container arm: a
    membership test whose container holds no known harness id is not a
    harness dispatch and must return [] -- otherwise the arm is just "flag
    every `in`". Also pins the documented blind spot: a novel id in a
    container is invisible."""
    src = ('def f(harness):\n'
           '    if harness in ("harmless", "also-harmless"):\n'
           '        return ["not-a-harness"]\n')
    assert _harness_branch_offenders(src) == []
    novel = ('def f(harness):\n'
             '    if harness in ("newharness", "x"):\n'
             '        return ["novel"]\n')
    assert _harness_branch_offenders(novel) == []  # documented blind spot


def test_gate_flags_underscored_token_builder():
    """Parent probe 3 (GATE): a plausible builder name that misses the argv
    suffix allowlist -- `_grok_flags` -- is still harness-specific code in
    rotate.py and must be reported."""
    src = 'def _grok_flags(h):\n    return ["--model", h]\n'
    assert _argv_builder_offenders(src) == ["_grok_flags"]


def test_gate_flags_unsuffixed_harness_named_builder():
    """Parent probe 4 (GATE): `_build_grok` has no `_command`/`_argv`/`_args`
    suffix at all; the harness token alone must be enough to report it."""
    src = "def _build_grok(*a, **k):\n    return ['grokbin']\n"
    assert _argv_builder_offenders(src) == ["_build_grok"]


def test_gate_flags_a_bare_grok_id_literal_but_not_a_docstring():
    """Rule B: `"grok"` in CODE is an offender even with no comparison
    around it; the same word inside a docstring is documentation and is
    ignored."""
    assert _harness_id_literal_offenders('X = "grok"\n') == ["grok"]
    assert _harness_id_literal_offenders(
        'def f():\n    """retired "grok" id"""\n    return 1\n') == []


def test_gate_leaves_legit_helpers_alone():
    """Non-vacuity in the other direction: the allowlisted, non-harness argv
    helpers and the shipped-id branch are NOT offenders, so the gate is not
    merely "flag every `_*_command`"."""
    src = ("def _build_harness_command(): ...\n"
           "def _successor_command(): ...\n"
           "def _assembled_successor_command(): ...\n"
           "def _launch_wrapper_argv(): ...\n"
           "def _wm_tool_argv(): ...\n")
    assert _argv_builder_offenders(src) == []
    assert _harness_branch_offenders(
        'def _validate_harness(harness):\n'
        '    if not harness or harness == "claude-code":\n'
        '        return 0\n') == []
    # the non-harness `'code'` token stays out of the harness-token set
    assert _argv_builder_offenders(
        "def _code_head(): ...\ndef _code_loaded_identity(): ...\n") == []
    # the shipped literal and the `harness_template.` call are not offenders
    assert _harness_id_literal_offenders('X = "claude-code"\n') == []
    assert _harness_branch_offenders(
        "h = harness_template.role_source(hid) == 'ladder'\n") == []


def test_gate_ignores_a_docstring_mention():
    """The gate reads DEFINITIONS, not text: documenting a retired builder by
    name must not fail the suite the way a naive substring grep would."""
    src = ('def f():\n'
           '    """no `if harness == "grok"` branch, no _build_grok_command"""\n'
           '    return 1\n')
    assert _argv_builder_offenders(src) == []
    assert _harness_branch_offenders(src) == []


def test_available_includes_shipped_harnesses():
    ids = harness_template.available()
    assert "copilot-cli" in ids
    assert "claude-code" in ids


@pytest.mark.parametrize("model,effort", [(None, None), ("auto", None),
                                         (None, "high"), ("auto", "high")])
def test_copilot_builder_renders_frozen_argv(model, effort):
    """The PRODUCTION copilot seat builder equals the OLD hand-built argv
    (rotate.py@8b6dcea1f), the same literal shape frozen above. A dropped or
    renamed seat flag in copilot-cli.toml fails this; `== render(...)` could
    not, since the builder IS that call. `extra_args` is not a production
    seat dimension (`_build_harness_command` does not accept it), so the
    render-level `COPILOT_MATRIX` above covers it."""
    expected = ["/x/copilot"]
    if model:
        expected += ["--model", model]
    if effort:
        expected += ["--effort", effort]
    expected += ["--allow-all", "--remote", "-i", "CARD"]

    got = rotate._build_harness_command(
        "copilot-cli", name="N", prompt_text="CARD", debug_file="D.LOG",
        model=model, effort=effort, bin_path="/x/copilot")
    assert got == expected


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
