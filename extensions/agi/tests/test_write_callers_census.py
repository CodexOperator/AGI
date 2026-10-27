"""The write.py CALLER CENSUS (goal:g7.16.1.11.46.23 falsifier item 1 + the v5 amendment; council alive 18:20:53Z 10-26 (a)).

A caller = a CODE call site of the node writer script (bin/ + "write" + ".py"): invoked with a verb, imported as a module, or its
path built from a name (a constant for it, the filename as a string, a trailing path segment). The neighbours (the module's
`_node` / `_guard` siblings, a name that merely ends in the same letters) are NOT callers (the word boundary).
Scope: extensions/, skills/, src/, .agi/nodes/.geometry/, CLAUDE.md, QUICKSTART.md (tracked files; node history and deprecated/ are history).

THE ROW: the census of the WHOLE tree must EQUAL ALLOWED, BY PATH (an exact set, never a count: one converted for one left
behind nets 0). ALLOWED is the retiring commit's (step 4) set: the writer script and its guard themselves, the tests of write.py, the
three COMMANDS table rows + commands.md, two stream_master corpus strings, and tests that name the script as TEXT. A new caller in any
other file reads RED here; step 4 shrinks ALLOWED to the empty set as it retires the rest.
"""
import subprocess
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SCOPE = ("extensions", "skills", "src", ".agi/nodes/.geometry", "CLAUDE.md", "QUICKSTART.md")
SKIP = ("extensions/agi/tests/fixtures/", ".agi/nodes/deprecated/")
_W = "wri" + "te"        # the patterns are built from parts so that THIS file is not a caller of itself
PAT = re.compile(
    r"(?<![A-Za-z_])(?:import " + _W + r"(?![A-Za-z_0-9])|from " + _W + r" import)"
    r"|(?<![A-Za-z_])" + _W + r"\.py +[a-z:]"
    r"|(?<![A-Za-z_])" + _W.upper() + r"_PY|[\"']" + _W + r"\.py[\"']|/" + _W + r"\.py")


UNREAD = "UNREAD:"       # prefix of a census entry whose file could not be read as utf-8 text (never in ALLOWED, so RED)


def census(root: Path) -> list[str]:
    """Sorted repo-relative paths under SCOPE with >= 1 caller line (git ls-files; every file when `root` is not a git tree). A file that cannot be read as utf-8 text is listed as UNREAD:<path>."""
    root = Path(root)
    r = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--", *SCOPE], capture_output=True, text=True)
    if r.returncode == 0 and r.stdout:
        files = [f for f in r.stdout.split("\0") if f]
    else:
        files = sorted(str(p.relative_to(root)) for s in SCOPE
                       for p in ((root / s).rglob("*") if (root / s).is_dir() else [root / s]) if p.is_file())
    out = []
    for f in files:
        if f.startswith(SKIP):
            continue
        try:
            text = (root / f).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            out.append(UNREAD + f)      # an unreadable file is UNREAD, never "not a caller": it reads RED against ALLOWED
            continue
        if any(PAT.search(line) for line in text.splitlines()):
            out.append(f)
    return sorted(out)


# the retiring commit's allowed set, BY PATH (the 3b re-cut's message names the same 68 paths)
ALLOWED_CODE = [
    '.agi/nodes/.geometry/commands.md',
    'CLAUDE.md',
    'QUICKSTART.md',
    'extensions/agi/bin/' + _W + '.py',
    'extensions/agi/bin/write_guard.py',
    'extensions/agi/src/stream_master/corpus.py',
    'extensions/agi/src/stream_master/relay.py',
    'skills/agi/SKILL.md',
]
ALLOWED_TESTS = [
    'extensions/agi/tests/agi-turn.t.sh',
    'extensions/agi/tests/graph-metrics.t.sh',
    'extensions/agi/tests/prereq-notice.t.sh',
    'extensions/agi/tests/skills-truth.t.sh',
    'extensions/agi/tests/test_board_job.py',
    'extensions/agi/tests/test_body_patch.py',
    'extensions/agi/tests/test_box_identity.py',
    'extensions/agi/tests/test_brief.py',
    'extensions/agi/tests/test_cli_done_kid_ceiling.py',
    'extensions/agi/tests/test_commands.py',
    'extensions/agi/tests/test_commands_manifest.py',
    'extensions/agi/tests/test_failures.py',
    'extensions/agi/tests/test_foreign_refusal_durability.py',
    'extensions/agi/tests/test_formation_readback.py',
    'extensions/agi/tests/test_graphweb.py',
    'extensions/agi/tests/test_grid.py',
    'extensions/agi/tests/test_hierarchy_seats.py',
    'extensions/agi/tests/test_links.py',
    'extensions/agi/tests/test_links_refs_outside.py',
    'extensions/agi/tests/test_nest.py',
    'extensions/agi/tests/test_post_rename.py',
    'extensions/agi/tests/test_rename_post.py',
    'extensions/agi/tests/test_research_review_mint_gate.py',
    'extensions/agi/tests/test_resolve_old_sha.py',
    'extensions/agi/tests/test_retire_place.py',
    'extensions/agi/tests/test_ring_cli_seam.py',
    'extensions/agi/tests/test_ring_gates_strict.py',
    'extensions/agi/tests/test_rings.py',
    'extensions/agi/tests/test_rotate.py',
    'extensions/agi/tests/test_rotate_handover.py',
    'extensions/agi/tests/test_rotate_startup.py',
    'extensions/agi/tests/test_rotate_verb.py',
    'extensions/agi/tests/test_rotation_alerts.py',
    'extensions/agi/tests/test_rotation_record.py',
    'extensions/agi/tests/test_skills_first_turn_entry.py',
    'extensions/agi/tests/test_stream_master_blind_measure.py',
    'extensions/agi/tests/test_thought_hygiene.py',
    'extensions/agi/tests/test_town_cell_write.py',
    'extensions/agi/tests/test_town_mint.py',
    'extensions/agi/tests/test_town_mint_final.py',
    'extensions/agi/tests/test_town_mint_lines.py',
    'extensions/agi/tests/test_untrusted_lane.py',
    'extensions/agi/tests/test_v8a_actor_seats.py',
    'extensions/agi/tests/test_verification.py',
    'extensions/agi/tests/test_veto_fail_closed.py',
    'extensions/agi/tests/test_viewport.py',
    'extensions/agi/tests/test_workflow.py',
    'extensions/agi/tests/test_write.py',
    'extensions/agi/tests/test_write_actor_rows.py',
    'extensions/agi/tests/test_write_answers_file.py',
    'extensions/agi/tests/test_write_build_kind.py',
    'extensions/agi/tests/test_write_commit_busy_index.py',
    'extensions/agi/tests/test_write_dotted_key.py',
    'extensions/agi/tests/test_write_guard.py',
    'extensions/agi/tests/test_write_master_sensei.py',
    'extensions/agi/tests/test_write_ring_cli.py',
    'extensions/agi/tests/test_write_schema_checked.py',
    'extensions/agi/tests/test_write_self_row.py',
    'extensions/agi/tests/test_write_sub.py',
    'extensions/agi/tests/test_write_veto_gate.py',
]
ALLOWED = sorted(ALLOWED_CODE + ALLOWED_TESTS)


def test_the_whole_tree_census_equals_the_allowed_set_exactly():
    got = census(REPO)
    extra, missing = sorted(set(got) - set(ALLOWED)), sorted(set(ALLOWED) - set(got))
    assert got == ALLOWED, f"census {len(got)} vs allowed {len(ALLOWED)}; UNCONVERTED CALLER(S) outside the allowed set: {extra}; allowed but no longer a caller (shrink ALLOWED): {missing}"


def _tree(tmp_path, files):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    for rel, text in files.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "add", "-A"], check=True, capture_output=True)
    return tmp_path


def test_the_census_matches_each_kind_of_call_site(tmp_path):
    t = _tree(tmp_path, {
        "extensions/agi/bin/a.py": "import " + _W + "\n",
        "extensions/agi/bin/b.py": "from " + _W + " import main\n",
        "extensions/agi/bin/c.sh": "python3 x/" + _W + ".py goal:g1 read body\n",
        "extensions/agi/bin/d.py": "WRITE" + "_PY = 'x'\n",
        "extensions/agi/bin/e.js": "const p = '" + _W + ".py'\n",
        "extensions/agi/bin/f.py": "p = root / 'bin/" + _W + ".py'\n",
    })
    assert census(t) == sorted(f"extensions/agi/bin/{n}" for n in ("a.py", "b.py", "c.sh", "d.py", "e.js", "f.py"))


def test_the_census_does_not_flag_the_neighbours_of_the_word(tmp_path):
    t = _tree(tmp_path, {
        "extensions/agi/bin/ok1.py": "from node_writer import " + _W + "_node\nimport " + _W + "_guard\n",
        "extensions/agi/bin/ok2.py": "# the " + _W + " verb of node_writer\nre" + _W + ".py x\n",
        "extensions/agi/tests/fixtures/f.txt": "import " + _W + "\n",
        ".agi/nodes/deprecated/x.md": "import " + _W + "\n",
    })
    assert census(t) == []


def test_MUTANT_one_caller_left_unconverted_in_an_untouched_file_is_RED(tmp_path):
    base = {f: "x = 1\n" for f in ("extensions/agi/bin/one.py", "extensions/agi/bin/two.py")}
    allowed = []
    assert census(_tree(tmp_path / "a", base)) == allowed
    planted = dict(base, **{"extensions/agi/bin/two.py": "import " + _W + "\n"})
    got = census(_tree(tmp_path / "b", planted))
    assert got != allowed and got == ["extensions/agi/bin/two.py"]


def test_MUTANT_one_converted_for_one_left_behind_nets_zero_by_count_but_the_SET_differs(tmp_path):
    allowed = ["extensions/agi/bin/one.py"]
    a = _tree(tmp_path / "a", {"extensions/agi/bin/one.py": "import " + _W + "\n", "extensions/agi/bin/two.py": "x = 1\n"})
    assert census(a) == allowed
    b = _tree(tmp_path / "b", {"extensions/agi/bin/one.py": "x = 1\n", "extensions/agi/bin/two.py": "import " + _W + "\n"})
    got = census(b)
    assert len(got) == len(allowed) and got != allowed, "the same COUNT, a different caller: only the set equality sees it"


def test_an_unreadable_file_reads_UNREAD_not_not_a_caller(tmp_path):
    t = _tree(tmp_path, {"extensions/agi/bin/ok.py": "x = 1\n"})
    (t / "extensions/agi/bin/bin.dat").write_bytes(b"\xff\xfe import " + _W.encode() + b"\n")
    (t / "extensions/agi/bin/dangling").symlink_to(t / "nowhere")
    subprocess.run(["git", "-C", str(t), "add", "-A"], check=True, capture_output=True)
    got = census(t)
    assert got == [UNREAD + "extensions/agi/bin/bin.dat", UNREAD + "extensions/agi/bin/dangling"]
    assert got != [], "MUTANT (the old `continue`) returns [] here: an unreadable caller read as not-a-caller"
