"""goal:g7.16.1.1.6 part 2 -- the one-source census in `commands.py run verify`.

`commands.py run verify` runs `verification.py` (command:commands `verify`),
whose default level is `rotation`. The census is a built-in check appended by
`run_level` at rotation + full, beside `check_formation`:

  cell   config:census (.agi/nodes/.geometry/census.md), frontmatter
         census.scanned  repo-relative pathspecs the census greps
         census.exclude  repo-relative prefixes it skips (tests pin literals)
         census.rules    {rule: {home: <repo-relative file>, pattern: <ERE>}}
  check  verification.check_census(groot) -> CheckResult("census", ...)
         per rule: ONE definition, in its home -> PASS; a second -> FAIL naming
         the copy's file:line; none, or one outside the home -> FAIL; an
         unusable row or a grep that cannot look -> FAIL (closed); no cell ->
         SKIP. The cell's own file is never counted (it quotes every pattern).

The next rule is a config row, not code: no rule name, home or pattern is a
literal in verification.py (test_the_check_carries_no_rule_literal).

The check + cell landed in goal:g7.16.1.1.6.1; the strict-xfail marker is lifted.
"""
from __future__ import annotations

import inspect
import sys
from pathlib import Path

import pytest
import yaml

BIN = Path(__file__).resolve().parents[1] / "bin"
SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))
import verification  # noqa: E402

ENGINE_ROOT = Path(__file__).resolve().parents[3]

# Spelled in pieces so this file never carries a one-line definition of its
# own (the live cell also excludes the tests dir; belt and braces).
_B, _E = "THOUGHT:" + "BEGIN", "THOUGHT:" + "END"
THOUGHT_RULE = "thought-marker-regex"
MINT_RULE = "mint-id-assigner"
HOME_TOKEN_RULE = "anonymize-home-token"
HOME_LINT_RULE = "home-code-literal"
THOUGHT_HOME = "extensions/agi/bin/node_writer.py"
MINT_HOME = "extensions/agi/src/graph_core/identity.py"
HOME_TOKEN_HOME = "extensions/agi/bin/anonymize.py"
HOME_LINT_HOME = "extensions/agi/bin/paths.py"
THOUGHT_PATTERN = _B + ".*" + _E
MINT_PATTERN = (r'\[.mint_id.\] *= *mint|new_fm\[.mint_id.\] *=|'
                r'"mint_id": *mint_permanent_id')

# one definition each, at a known line (line 3 of each home)
THOUGHT_DEF = f'_THOUGHT_RE = re.compile(r"^<!--\\s*{_B}.*?^<!--\\s*{_E}\\s*-->")\n'
MINT_DEF = '    return {**fm, "mint_id": mint_permanent_id()}\n'


def _write(repo: Path, rel: str, text: str) -> None:
    f = repo / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text, "utf-8")


def _cell(repo: Path, rules: dict, *, scanned=None, exclude=None,
          body: str = "") -> None:
    fm = {"id": "config:census", "type": "config",
          "parents": ["goal:g7.16.1.1.6"],
          "census": {"scanned": scanned or ["extensions", "skills",
                                            ".agi/nodes/.geometry"],
                     "exclude": exclude if exclude is not None
                     else ["extensions/agi/tests"],
                     "rules": rules}}
    _write(repo, ".agi/nodes/.geometry/census.md",
           "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True)
           + "---\n# config:census\n" + body)


def _two_rules() -> dict:
    return {THOUGHT_RULE: {"home": THOUGHT_HOME, "pattern": THOUGHT_PATTERN},
            MINT_RULE: {"home": MINT_HOME, "pattern": MINT_PATTERN}}


@pytest.fixture
def repo(tmp_path):
    """A scratch repo (NOT a git repo: the census must see untracked copies)
    with one definition per rule, each at line 3 of its home."""
    r = tmp_path / "repo"
    _write(r, THOUGHT_HOME, "import re\n\n" + THOUGHT_DEF)
    _write(r, MINT_HOME, "def ensure_mint_id(fm):\n    pass\n" + MINT_DEF)
    _write(r, "skills/agi-node-write/SKILL.md",
           f"prose naming {_B} and, on its own line,\n{_E}\n")
    # the tests dir pins literals on purpose; the cell excludes it
    _write(r, "extensions/agi/tests/test_x.py", "X = '" + THOUGHT_DEF.strip()
           .replace("'", '"') + "'\n")
    _cell(r, _two_rules(),
          body=f"The rows quote every pattern: `{THOUGHT_PATTERN}`.\n")
    (r / ".agi" / "nodes").mkdir(parents=True, exist_ok=True)
    return r


def _census(repo: Path):
    return verification.check_census(repo / ".agi")


# --- (1) listed by run verify, PASS on one definition per rule ---------------

def test_one_definition_per_rule_passes(repo):
    r = _census(repo)
    assert r.name == "census"
    assert r.status == "PASS", (r.note, r.message)
    assert r.number == {"rules": 2}


@pytest.mark.parametrize("level", ["rotation", "full"])
def test_run_verify_lists_the_census(monkeypatch, repo, level):
    """`commands.py run verify` == verification.py at its default level."""
    monkeypatch.setattr(verification, "run_check",
                        lambda g, n, v: verification.CheckResult(n, "PASS", 0.0))
    results = verification.run_level(repo / ".agi", level, suite=False,
                                     verbose=False)
    census = [x for x in results if x.name == "census"]
    assert len(census) == 1 and census[0].status == "PASS", census


def test_no_cell_is_a_skip(repo):
    (repo / ".agi/nodes/.geometry/census.md").unlink()
    assert _census(repo).status == "SKIP"


def test_the_live_cell_carries_the_first_two_rows_and_passes():
    """Goal Falsifier 1: the census PASSes with at least the THOUGHT-marker
    and mint-id-assigner rows, on the engine's own bytes."""
    groot = ENGINE_ROOT / ".agi"
    if not (groot / "nodes" / ".geometry").is_dir():
        pytest.skip("engine checkout carries no .agi/nodes/.geometry")
    import node_writer
    cell = node_writer.find_node_file(groot, "config:census")
    assert cell is not None, "config:census is not in .agi/nodes/.geometry"
    fm = yaml.safe_load(node_writer.split_frontmatter(
        cell.read_text("utf-8"))[0])
    rules = fm["census"]["rules"]
    assert {THOUGHT_RULE, MINT_RULE} <= set(rules)
    # goal:g7.16.1.1.6.2 -- two named homes, not one shared def
    assert {HOME_TOKEN_RULE, HOME_LINT_RULE} <= set(rules)
    assert rules[HOME_TOKEN_RULE]["home"] == HOME_TOKEN_HOME
    assert rules[HOME_LINT_RULE]["home"] == HOME_LINT_HOME
    assert "extensions/agi/tests" in fm["census"]["exclude"]
    r = verification.check_census(groot)
    assert r.status == "PASS", (r.note, r.message)
    assert r.number["rules"] >= 4


def test_a_scratch_home_token_copy_fails_naming_the_file():
    """goal:g7.16.1.1.6.2 Falsifier 2: a third home-path regex under bin
    makes the live census FAIL, naming that file:line."""
    groot = ENGINE_ROOT / ".agi"
    if not (groot / "nodes" / ".geometry").is_dir():
        pytest.skip("engine checkout carries no .agi/nodes/.geometry")
    scratch = ENGINE_ROOT / "extensions/agi/bin/zz_census_home_scratch.py"
    try:
        scratch.write_text("HOME_PATH_RE = _home_path_re()\n", encoding="utf-8")
        r = verification.check_census(groot)
        assert r.status == "FAIL", (r.note, r.message)
        blob = f"{r.note}\n{r.message}"
        assert "zz_census_home_scratch.py" in blob, blob
        assert HOME_TOKEN_RULE in blob, blob
    finally:
        scratch.unlink(missing_ok=True)


# --- (2) NEGATIVE: a second definition FAILs naming the copy's file:line -----

def test_a_second_thought_marker_regex_fails_naming_the_copy(repo):
    _write(repo, "extensions/agi/bin/links.py",
           "import re\n# a local copy\n\n\n" + THOUGHT_DEF)
    r = _census(repo)
    assert r.status == "FAIL"
    blob = f"{r.note}\n{r.message}"
    assert "extensions/agi/bin/links.py:5" in blob, blob
    assert THOUGHT_RULE in blob


def test_a_second_mint_id_assigner_fails_naming_the_copy(repo):
    _write(repo, "extensions/agi/bin/backfill-mint-ids.py",
           "def backfill(fm):\n" + MINT_DEF.replace("return", "fm =", 1))
    r = _census(repo)
    assert r.status == "FAIL"
    blob = f"{r.note}\n{r.message}"
    assert "extensions/agi/bin/backfill-mint-ids.py:2" in blob, blob
    assert MINT_RULE in blob


def test_a_copy_outside_bin_is_still_a_copy(repo):
    """The census scans every declared surface, not only bin/ (verdict:dg2-d:
    a falsifier over bin alone FAILs a correct build and misses a src copy)."""
    _write(repo, "skills/agi/SKILL.md", "```\n" + THOUGHT_DEF + "```\n")
    r = _census(repo)
    assert r.status == "FAIL"
    assert "skills/agi/SKILL.md:2" in f"{r.note}\n{r.message}"


def test_the_one_definition_outside_its_home_fails(repo):
    (repo / MINT_HOME).write_text("def ensure_mint_id(fm):\n    pass\n", "utf-8")
    _write(repo, "extensions/agi/bin/node_writer_mint.py", MINT_DEF)
    r = _census(repo)
    assert r.status == "FAIL"
    blob = f"{r.note}\n{r.message}"
    assert "extensions/agi/bin/node_writer_mint.py:1" in blob and MINT_RULE in blob


def test_zero_definitions_fails_the_home_moved_without_its_row(repo):
    (repo / THOUGHT_HOME).write_text("import re\n", "utf-8")
    r = _census(repo)
    assert r.status == "FAIL"
    assert THOUGHT_RULE in f"{r.note}\n{r.message}"


def test_an_unusable_row_fails_closed(repo):
    rules = _two_rules()
    rules["broken"] = {"home": THOUGHT_HOME, "pattern": "(unclosed"}
    _cell(repo, rules)
    r = _census(repo)
    assert r.status == "FAIL"
    assert "broken" in f"{r.note}\n{r.message}"


# --- (3) the rules come from the cell; none is a literal in the check --------

def test_the_next_rule_is_a_config_row_not_code(repo):
    rules = _two_rules()
    rules["widget-parser"] = {"home": "extensions/agi/bin/widget.py",
                              "pattern": r"def parse_widget\("}
    _cell(repo, rules)
    _write(repo, "extensions/agi/bin/widget.py", "def parse_widget(x):\n    pass\n")
    r = _census(repo)
    assert (r.status, r.number) == ("PASS", {"rules": 3}), (r.note, r.message)
    _write(repo, "extensions/agi/bin/other.py", "\n\ndef parse_widget(y):\n")
    r = _census(repo)
    assert r.status == "FAIL"
    blob = f"{r.note}\n{r.message}"
    assert "widget-parser" in blob and "extensions/agi/bin/other.py:3" in blob


def test_the_scanned_and_excluded_surfaces_are_cell_data(repo):
    """The tests dir is skipped because the CELL says so, not the code."""
    assert _census(repo).status == "PASS"
    _cell(repo, _two_rules(), exclude=[])
    r = _census(repo)
    assert r.status == "FAIL"
    assert "extensions/agi/tests/test_x.py:1" in f"{r.note}\n{r.message}"


def test_the_check_carries_no_rule_literal():
    src = inspect.getsource(verification.check_census)
    for name, fn in vars(verification).items():
        if name.startswith("_census") and callable(fn):
            src += inspect.getsource(fn)
    module = inspect.getsource(verification)
    for literal in (THOUGHT_RULE, MINT_RULE, HOME_TOKEN_RULE, HOME_LINT_RULE,
                    THOUGHT_HOME, MINT_HOME, HOME_TOKEN_HOME, HOME_LINT_HOME,
                    "node_writer.py", "graph_core/identity.py",
                    "mint_permanent_id", _B, _E):
        assert literal not in src, f"rule literal {literal!r} in check_census"
        assert literal not in module, f"rule literal {literal!r} in verification.py"
    # the scanned/excluded surfaces are cell data too (a comment elsewhere in
    # the module may name the tests dir; the check itself may not)
    for literal in ("extensions/agi/tests", '"skills"', '"extensions"'):
        assert literal not in src, f"surface literal {literal!r} in check_census"
