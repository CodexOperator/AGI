"""goal:g7.16.1.11.46.23 3b: node_read.py, the read-only reader of the four rotations.md first_turn exec lines.

The first_turn judge admits ANY `python3 extensions/..` script and never reads its arguments, so node_read's own
refusals are the whole guard (council decision alive 01:20:03Z 10-26, 3/3: R1 containment on the RESOLVED path, R2 id
grammar, R3 tracked only through ONE fixed git call, R4 unread is loud, R5 section/lines defined, R6 byte + F12).
Every refusal row has its mutant: the target prints 0 bytes and the one line starts `node_read:`.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
SCRIPT = BIN / "node_read.py"
REPO = Path(__file__).resolve().parents[3]
SECRET = "SECRET-TOKEN-1234"

ROT = """---
id: config:rotations
type: config
---
# config:rotations

## templates

t

## facts

> MEASURED facts.

- F1 one
- F2 two  (with  double  spaces)
- RETIRED, numbers only: F6.

## steps

> Declared by 0b.

## Agent Notes
"""
FACTS = "## facts\n\n> MEASURED facts.\n\n- F1 one\n- F2 two  (with  double  spaces)\n- RETIRED, numbers only: F6.\n"
SKILL = "---\nname: x\ndescription: >\n  one\n  two\n  three\n---\n# x\n"


def git(d, *a):
    return subprocess.run(["git", "-C", str(d), "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", *a],
                          check=True, capture_output=True, text=True)


def build_node(slug, ref, extra=""):
    return f"---\nid: build:{slug}\ntype: build\nbuild_kind: prose\nlocation: source_root\npayload_ref: {ref}\n{extra}---\n# build:{slug}\n"


@pytest.fixture()
def repo(tmp_path):
    d = tmp_path / "repo"
    (d / "extensions/agi/bin").mkdir(parents=True)
    shutil.copy(SCRIPT, d / "extensions/agi/bin/node_read.py")
    (d / ".agi/nodes/.geometry").mkdir(parents=True)
    (d / ".agi/nodes/build").mkdir(parents=True)
    (d / ".agi/nodes/doc").mkdir(parents=True)
    (d / "skills/x").mkdir(parents=True)
    (d / ".agi/nodes/.geometry/rotations.md").write_text(ROT)
    (d / "skills/x/SKILL.md").write_text(SKILL)
    (d / ".agi/nodes/build/skills-x-SKILL.md.md").write_text(build_node("skills-x-SKILL.md", "skills/x/SKILL.md"))
    (d / ".env").write_text(SECRET + "\n")
    (d / ".gitignore").write_text(".env\n")
    git(d, "init", "-q")
    git(d, "add", "-A")
    git(d, "commit", "-qm", "base")
    return d


def run(d, *args, path=None):
    env = {**os.environ}
    if path is not None:
        env["PATH"] = path
    r = subprocess.run([sys.executable, str(d / "extensions/agi/bin/node_read.py"), *args], cwd=d, capture_output=True,
                       text=True, env=env)
    return r.returncode, r.stdout, r.stderr


def refused(d, *args, path=None, why=None):
    rc, out, err = run(d, *args, path=path)
    assert rc == 1 and out.startswith("node_read: ") and out.count("\n") == 1, (rc, out, err)
    assert SECRET not in out + err, (out, err)
    if why:
        assert why in out, out
    return out


def add_build(d, slug, ref, commit=True):
    (d / f".agi/nodes/build/{slug}.md").write_text(build_node(slug, ref))
    if commit:
        git(d, "add", "-A")
        git(d, "commit", "-qm", slug)


# ---- ADMITS (R5: the section and lines definitions; R6: the bytes) -----------------------------------------
def test_section_is_the_heading_through_the_line_before_the_next_heading_trailing_blanks_dropped(repo):
    rc, out, _ = run(repo, "config:rotations", "section", "facts")
    assert rc == 0 and out == FACTS, repr(out)
    assert not out.endswith("\n\n") and "## steps" not in out


def test_section_bytes_equal_the_independent_sed_range_over_the_same_file(repo):
    want = subprocess.run(["sed", "-n", "/^## facts$/,/^- RETIRED, numbers only/p", ".agi/nodes/.geometry/rotations.md"],
                          cwd=repo, capture_output=True, text=True).stdout
    assert run(repo, "config:rotations", "section", "facts")[1] == want


def test_lines_are_FILE_relative_1_based_inclusive_of_a_build_nodes_payload(repo):
    rc, out, _ = run(repo, "build:skills-x-SKILL.md", "lines", "2:7")
    want = subprocess.run(["sed", "-n", "2,7p", "skills/x/SKILL.md"], cwd=repo, capture_output=True, text=True).stdout
    assert rc == 0 and out == want and out.startswith("name: x\n") and out.endswith("---\n")


def test_a_non_build_node_is_read_as_the_file_itself(repo):
    rc, out, _ = run(repo, "config:rotations", "lines", "1:3")
    assert rc == 0 and out == "---\nid: config:rotations\ntype: config\n"


def test_a_heading_inside_a_fenced_block_is_not_a_heading_and_a_subsection_stays_inside(repo):
    (repo / ".agi/nodes/doc/d.md").write_text("# d\n\n## A\n```\n## not a heading\n```\n### sub\ntext\n\n## B\nb\n")
    git(repo, "add", "-A"); git(repo, "commit", "-qm", "d")
    rc, out, _ = run(repo, "doc:d", "section", "A")
    assert rc == 0 and out == "## A\n```\n## not a heading\n```\n### sub\ntext\n", out
    refused(repo, "doc:d", "section", "not a heading", why="not found")


def test_a_retired_sibling_under_deprecated_resolves_second(repo):
    (repo / ".agi/nodes/deprecated/doc").mkdir(parents=True)
    (repo / ".agi/nodes/deprecated/doc/old.md").write_text("# old\n\n## S\nx\n")
    git(repo, "add", "-A"); git(repo, "commit", "-qm", "old")
    assert run(repo, "doc:old", "section", "S")[1] == "## S\nx\n"


def test_help_is_rc_0_anywhere_in_argv_so_the_first_turn_verb_parse_test_passes_and_a_bad_call_is_rc_2(repo):
    assert run(repo, "--help")[0] == 0
    assert run(repo, "config:rotations", "-h")[0] == 0           # `<script> <verb> -h`, the rotate-templates parse probe
    assert run(repo, "config:rotations")[0] == 2


# ---- R2 id grammar --------------------------------------------------------------------------------------
@pytest.mark.parametrize("bad", ["doc:../x", "doc:a/b", "../doc:x", "doc", "doc:", ":x", "doc:a b", "Doc:x", "doc:xy/"])
def test_R2_mutant_a_bad_id_is_refused_before_any_path_is_built(repo, bad):
    refused(repo, bad, "section", "a")


def test_R2_mutant_a_NUL_in_the_id_is_refused_in_process():
    sys.path.insert(0, str(BIN))
    import node_read  # noqa: PLC0415
    with pytest.raises(node_read.Refused):
        node_read.check_id("doc:a\x00b")


# ---- R1 containment on the RESOLVED path -----------------------------------------------------------------
@pytest.mark.parametrize("ref", ["../.env", ".env", "../../etc/hostname", "./../repo/.env"])
def test_R1_mutant_a_payload_ref_that_leaves_the_allowed_dirs_is_refused(repo, ref):
    add_build(repo, "evil", ref)
    refused(repo, "build:evil", "lines", "1:1")


def test_R1_mutant_an_absolute_payload_ref_is_refused(repo):
    add_build(repo, "abs", str(repo / ".env"))
    refused(repo, "build:abs", "lines", "1:1")
    add_build(repo, "abs2", "/etc/hostname")
    refused(repo, "build:abs2", "lines", "1:1", why="outside")


def test_R1_mutant_a_symlink_under_skills_to_a_file_outside_the_repo_is_refused(repo, tmp_path):
    outside = tmp_path / "outside.txt"
    outside.write_text(SECRET + "\n")
    os.symlink(outside, repo / "skills/x/link.md")
    git(repo, "add", "-A"); git(repo, "commit", "-qm", "link")
    add_build(repo, "viaLink".lower(), "skills/x/link.md")
    refused(repo, "build:vialink", "lines", "1:1", why="outside")


def test_R1_mutant_a_node_file_that_is_a_symlink_to_dotenv_is_refused(repo):
    os.symlink(repo / ".env", repo / ".agi/nodes/doc/envlink.md")
    git(repo, "add", "-A"); git(repo, "commit", "-qm", "envlink")
    refused(repo, "doc:envlink", "lines", "1:1", why="outside")


def test_R1_a_symlinked_card_that_resolves_to_its_doc_node_passes(repo):
    (repo / ".agi/nodes/doc/real.md").write_text("# real\n\n## S\nok\n")
    os.symlink("real.md", repo / ".agi/nodes/doc/alias.md")
    git(repo, "add", "-A"); git(repo, "commit", "-qm", "alias")
    assert run(repo, "doc:alias", "section", "S")[1] == "## S\nok\n"


def test_R1_mutant_a_dangling_payload_ref_link_is_refused(repo):
    os.symlink(repo / "skills/x/nowhere.md", repo / "skills/x/dangling.md")
    git(repo, "add", "-A"); git(repo, "commit", "-qm", "dangling")
    add_build(repo, "dang", "skills/x/dangling.md")
    refused(repo, "build:dang", "lines", "1:1", why="dangling")


def test_R1_a_payload_under_extensions_is_outside_the_allowed_dirs(repo):
    add_build(repo, "eng", "extensions/agi/bin/node_read.py")
    refused(repo, "build:eng", "lines", "1:1", why="outside")


# ---- R3 tracked only, ONE fixed git call -------------------------------------------------------------------
def test_R3_mutant_an_ignored_dotenv_inside_the_allowed_dirs_is_refused(repo):
    (repo / "skills/x/.env").write_text(SECRET + "\n")                  # ignored at any depth by .gitignore:1
    add_build(repo, "ienv", "skills/x/.env")
    refused(repo, "build:ienv", "lines", "1:1", why="not tracked")
    os.symlink(".env", repo / "skills/x/envlink.md")                    # reached by a link
    git(repo, "add", "-A"); git(repo, "commit", "-qm", "envlink2")
    add_build(repo, "ienv2", "skills/x/envlink.md")
    refused(repo, "build:ienv2", "lines", "1:1", why="not tracked")


def test_R3_mutant_an_untracked_node_file_is_refused(repo):
    (repo / ".agi/nodes/doc/loose.md").write_text("# loose\n\n## S\n" + SECRET + "\n")
    refused(repo, "doc:loose", "section", "S", why="not tracked")


def test_R3_mutant_a_tracked_file_plus_an_untracked_glob_named_file_reached_by_ref_is_refused(repo):
    (repo / "skills/abc.md").write_text("tracked\n")
    git(repo, "add", "-A"); git(repo, "commit", "-qm", "abc")
    (repo / "skills/a*").write_text(SECRET + "\n")                       # untracked, literally named `a*`
    add_build(repo, "globref", "skills/a*", commit=False)
    git(repo, "add", ".agi"); git(repo, "commit", "-qm", "globref")
    refused(repo, "build:globref", "lines", "1:1", why="not tracked")


def test_R3_the_literal_pathspec_row_bites_without_GIT_LITERAL_PATHSPECS_the_glob_file_reads(repo, tmp_path):
    (repo / "skills/abc.md").write_text("tracked\n")
    git(repo, "add", "-A"); git(repo, "commit", "-qm", "abc")
    (repo / "skills/a*").write_text(SECRET + "\n")
    add_build(repo, "globref", "skills/a*", commit=False)
    git(repo, "add", ".agi"); git(repo, "commit", "-qm", "globref")
    mut = repo / "extensions/agi/bin/node_read.py"
    src = mut.read_text()
    assert '"GIT_LITERAL_PATHSPECS": "1", ' in src
    mut.write_text(src.replace('"GIT_LITERAL_PATHSPECS": "1", ', ""))
    rc, out, _ = run(repo, "build:globref", "lines", "1:1")
    assert rc == 0 and SECRET in out, "the mutant (no literal pathspecs) must read the untracked glob-named file"


def test_R3_mutant_git_absent_from_PATH_is_refused_never_assumed_tracked(repo, tmp_path):
    empty = tmp_path / "nopath"
    empty.mkdir()
    refused(repo, "config:rotations", "section", "facts", path=str(empty), why="git did not run")


def test_R3_mutant_not_a_git_repo_is_refused(repo):
    shutil.rmtree(repo / ".git")
    refused(repo, "config:rotations", "section", "facts", why="not tracked")


# ---- R4 unread is loud -----------------------------------------------------------------------------------------
def test_R4_mutant_a_missing_heading_is_one_named_line_rc_1_never_an_empty_print(repo):
    out = refused(repo, "config:rotations", "section", "nosuch", why="'nosuch' not found")
    assert out.endswith("config:rotations\n")


def test_R4_mutant_a_duplicated_heading_is_refused_never_the_first_one(repo):
    (repo / ".agi/nodes/doc/dup.md").write_text("# dup\n\n## S\na\n\n## S\nb\n")
    git(repo, "add", "-A"); git(repo, "commit", "-qm", "dup")
    refused(repo, "doc:dup", "section", "S", why="found 2 times")


def test_R4_mutant_an_unresolved_id_a_range_past_eof_and_an_empty_range(repo):
    refused(repo, "doc:nosuchnode", "section", "S", why="does not resolve")
    refused(repo, "build:skills-x-SKILL.md", "lines", "2:99", why="past the end")
    refused(repo, "build:skills-x-SKILL.md", "lines", "5:3", why="is empty")
    refused(repo, "build:skills-x-SKILL.md", "lines", "0:3", why="is empty")
    refused(repo, "build:skills-x-SKILL.md", "lines", "a:b", why="must be A:B")


def test_R4_mutant_a_build_node_without_a_payload_ref_is_refused(repo):
    (repo / ".agi/nodes/build/bare.md").write_text("---\nid: build:bare\ntype: build\n---\n# build:bare\n")
    git(repo, "add", "-A"); git(repo, "commit", "-qm", "bare")
    refused(repo, "build:bare", "lines", "1:1", why="no payload_ref")


def test_R4_a_link_ref_is_the_fallback_for_a_prose_build_node(repo):
    (repo / ".agi/nodes/build/lr.md").write_text("---\nid: build:lr\ntype: build\nlink_ref: skills/x/SKILL.md\n---\n# build:lr\n")
    git(repo, "add", "-A"); git(repo, "commit", "-qm", "lr")
    assert run(repo, "build:lr", "lines", "2:2")[1] == "name: x\n"


# ---- R6: the live rotations.md exec lines: F12 in-process + the old bytes ---------------------------------------
def _live_node_read_cmds():
    t = (REPO / ".agi/nodes/.geometry/rotations.md").read_text(encoding="utf-8")
    return re.findall(r'"cmd": "(python3 extensions/agi/bin/node_read\.py[^"]*)"', t)


def test_R6_the_four_replaced_exec_lines_exist_and_no_write_py_read_is_left_in_rotations():
    cmds = _live_node_read_cmds()
    assert len(cmds) == 4, cmds
    t = (REPO / ".agi/nodes/.geometry/rotations.md").read_text(encoding="utf-8")
    assert not re.search(r"bin/write\.py (config|build):", t)


def test_R6_F12_every_replaced_exec_line_passes_the_first_turn_judge_in_process():
    sys.path.insert(0, str(BIN))
    import rotate  # noqa: PLC0415
    for c in _live_node_read_cmds():
        assert rotate._producing_refusal(c) is None, c


def test_R6_every_clause_reads_on_the_live_tree_and_the_facts_span_is_the_heading_to_the_line_before_the_next(tmp_path):
    for c in _live_node_read_cmds():
        for clause in c.split("; "):
            r = subprocess.run(clause, shell=True, cwd=REPO, capture_output=True, text=True)
            assert r.returncode == 0 and r.stdout.strip(), (clause, r.stdout[:200])
    lines = (REPO / ".agi/nodes/.geometry/rotations.md").read_text(encoding="utf-8").splitlines(keepends=True)
    s = lines.index("## facts\n")
    e = next(i for i in range(s + 1, len(lines)) if lines[i].startswith("## "))
    want = "".join(lines[s:e]).rstrip("\n") + "\n"
    got = subprocess.run([sys.executable, str(SCRIPT), "config:rotations", "section", "facts"], cwd=REPO,
                         capture_output=True, text=True).stdout
    assert got == want and got.startswith("## facts\n")
