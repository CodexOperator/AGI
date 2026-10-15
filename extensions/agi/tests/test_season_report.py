"""Proof for `season_report.py facts` (goal:g5.4.1, S1: council design 10-15, falsifiers F1 F3a-c F5 F6).

Every count is PINNED to the commit 5fa654a5f3 (the trunk at the 08:11Z ROLLOVER COMPLETE read), so a later retire cannot move it. The
heads come from a CAPTURED ls-remote (tests/fixtures/season_report/): no row touches the network. Each row has a MUTANT: a copy of
season_report.py with ONE line changed, run the same way, which must go RED.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
CLI = HERE.parent / "bin" / "season_report.py"
ROOT = HERE.parents[2]
HEADS = HERE / "fixtures" / "season_report" / "heads-20261015T1941Z.txt"
PIN = "5fa654a5f3"
NODES = ".agi/nodes"

pytestmark = pytest.mark.skipif(
    subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e", f"{PIN}^{{commit}}"], capture_output=True).returncode != 0,
    reason=f"{PIN} is not in this clone (a shallow checkout)")


def _git(repo: Path, *args: str) -> str:
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return r.stdout


def _facts_raw(*extra: str, cli: Path = CLI, repo: Path = ROOT, heads: Path = HEADS, season: str = "3") -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(cli), "--repo", str(repo), "facts", "--season", season, "--at", PIN,
                           "--heads-file", str(heads), *extra], capture_output=True)


def _facts(**kw) -> dict:
    r = _facts_raw(**kw)
    assert r.returncode == 0, r.stderr.decode()
    return json.loads(r.stdout)


def _mutant(tmp_path: Path, old: str, new: str) -> Path:
    text = CLI.read_text()
    assert text.count(old) == 1, f"mutant anchor not unique ({text.count(old)}): {old!r}"
    p = tmp_path / "season_report_mutant.py"
    p.write_text(text.replace(old, new))
    return p


def _world(repo: Path) -> tuple[str, str]:
    """What `facts` must leave alone: every ref, and the working tree's status."""
    refs = hashlib.sha1(_git(repo, "for-each-ref").encode()).hexdigest()
    return refs, _git(repo, "status", "--porcelain")


@pytest.fixture(scope="module")
def pinned() -> dict:
    return _facts()


# ---- F1: byte-equal reruns ---------------------------------------------------------------------------------------------------
def test_f1_two_runs_are_byte_equal_and_a_clock_in_the_json_mutant_is_red(tmp_path: Path):
    a, b = _facts_raw(), _facts_raw()
    assert a.returncode == 0 and a.stdout == b.stdout, "F1: two facts runs differ"
    assert a.stdout.endswith(b"\n") and a.stdout.count(b"\n") > 50
    mut = _mutant(tmp_path, '        "at": sha,\n', '        "at": sha, "now": time.time_ns(),\n')
    m1, m2 = _facts_raw(cli=mut), _facts_raw(cli=mut)
    assert m1.returncode == 0 and m1.stdout != m2.stdout, "MUTANT (a clock in the JSON) must be RED: its two runs must differ"


# ---- F3a: active_by_dir == an independent ls-tree count ----------------------------------------------------------------------------
def _indep_live_paths() -> list[str]:
    names = _git(ROOT, "ls-tree", "-r", "--name-only", PIN, "--", NODES).split("\n")
    return [n for n in names if n.endswith(".md") and not n.startswith(f"{NODES}/deprecated/")]


def test_f3a_active_by_dir_equals_an_independent_ls_tree_count_and_dropping_geometry_is_red(tmp_path: Path, pinned: dict):
    indep = len(_indep_live_paths())
    assert indep == 5706, "the pin moved: 5,706 live node files at 5fa654a5f3"
    assert pinned["counts"]["active_by_dir"] == indep
    assert pinned["counts"]["deprecated_by_dir"] == 239
    mut = _mutant(tmp_path, '        stem = "/".join(parts[3:])[:-3]\n',
                  '        if parts[2] == ".geometry":\n            continue\n        stem = "/".join(parts[3:])[:-3]\n')
    got = _facts(cli=mut)["counts"]["active_by_dir"]
    assert got == 5682 and got != indep, f"MUTANT (.geometry dropped) must be RED: {got} vs {indep}"


# ---- F3b: active_by_status == an independent git grep -L ---------------------------------------------------------------------------
def test_f3b_active_by_status_equals_an_independent_git_grep_l(pinned: dict):
    out = _git(ROOT, "grep", "-L", "-E", "^status: *\"?deprecated\"?[ \t]*$", PIN, "--", f"{NODES}/*.md", f":(exclude){NODES}/deprecated/*")
    indep = len([ln for ln in out.split("\n") if ln])
    assert indep == 5700
    assert pinned["counts"]["active_by_status"] == indep


# ---- F3c: the mismatch list == |F3a - F3b| == 6 --------------------------------------------------------------------------------------
def test_f3c_the_mismatch_list_has_six_ids_and_dropping_the_list_is_red(tmp_path: Path, pinned: dict):
    c = pinned["counts"]
    assert len(c["status_dir_mismatch"]) == 6 == c["active_by_dir"] - c["active_by_status"]
    assert c["status_dir_mismatch"] == sorted(["doc:lm-town-trajectory", "experiment:a00-3a7d5c8c-46ee39", "experiment:a01-545f623d-6d71d2",
                                               "hypothesis:a00-500a23f5-f8c142", "hypothesis:a00-655e37e2-87cfb0", "hypothesis:a01-98e872ef-bd5f40"])
    mut = _mutant(tmp_path, '"status_dir_mismatch": sorted(mismatch),', '"status_dir_mismatch": [],')
    m = _facts(cli=mut)["counts"]
    assert len(m["status_dir_mismatch"]) == 0 != c["active_by_dir"] - c["active_by_status"], "MUTANT (list dropped) must be RED: 0 vs 6"


# ---- F5 NEGATIVE: facts changes no ref and no working-tree status ------------------------------------------------------------------------
def test_f5_facts_leaves_every_ref_and_the_status_unchanged_and_a_ref_writing_mutant_is_red(tmp_path: Path):
    # the live repo's refs move under other posts' commits, so the ref digest is proved on a FROZEN throwaway clone (below);
    # the status of THIS checkout is proved in place
    status = _git(ROOT, "status", "--porcelain")
    assert _facts_raw().returncode == 0
    assert _git(ROOT, "status", "--porcelain") == status, "F5: facts changed the working-tree status"
    # the mutant writes a ref: only ever into a THROWAWAY shared clone, never the live repo
    clone = tmp_path / "clone"
    subprocess.run(["git", "clone", "-q", "-n", "--shared", str(ROOT), str(clone)], check=True, capture_output=True)
    mut = _mutant(tmp_path, '    tree = read_tree(repo, sha)\n', '    _git(repo, "update-ref", "refs/mutant/x", sha)\n    tree = read_tree(repo, sha)\n')
    w0 = _world(clone)
    assert _facts_raw(repo=clone).returncode == 0 and _world(clone) == w0, "the unmutated script must leave the clone alone"
    assert _facts_raw(cli=mut, repo=clone).returncode == 0
    assert _world(clone) != w0, "MUTANT (facts writes a ref) must be RED: the refs digest must change"


# ---- F6: the type rows sum to active_by_dir -----------------------------------------------------------------------------------------------
def test_f6_the_type_rows_sum_to_active_by_dir_and_dropping_other_is_red(tmp_path: Path, pinned: dict):
    c = pinned["counts"]
    rows = c["type_rows"]
    assert sum(r["nodes"] for r in rows) == c["active_by_dir"], "F6: the rows must sum to active_by_dir"
    assert rows[-1] == {"type": "other", "label": "other (6 types)", "types": 6, "nodes": 110, "pct": "4.6"}
    assert len(rows) == 10 and sum(c["by_type"].values()) == c["active_by_dir"]
    mut = _mutant(tmp_path, "    if rest:\n", "    if False:\n")
    m = _facts(cli=mut)["counts"]
    gap = m["active_by_dir"] - sum(r["nodes"] for r in m["type_rows"])
    assert gap == 110 != 0, f"MUTANT (the other row dropped) must be RED: the rows then miss {gap} nodes"


# ---- the other sources, pinned ---------------------------------------------------------------------------------------------------------------
def test_posts_cells_close_and_ledger_read_at_the_pin(pinned: dict):
    assert pinned["at"].startswith(PIN) and pinned["season"] == 3
    assert (pinned["posts_named"], pinned["trunk_cells"]) == (33, 14)
    assert pinned["trunks"] == {"core/season3/main": 14}
    assert pinned["cells"]["ladder_current_season"] == "3" and pinned["cells"]["opened"] == "2026-10-15T06:23:30Z"
    assert pinned["close"]["value"] == "2026-10-15T06:24:17Z" and pinned["close"]["signed"] is True
    assert pinned["close"]["label"].startswith("season 2 closed")
    led = pinned["ledger"]
    assert led["commits"] == led["signed"] + led["unsigned"] and led["signed"] > 0
    assert {"L20", "L22", "L23", "S20", "S22", "S23"} <= set(led["names"])
    assert pinned["goals"]["total"] == 699 and pinned["goals"]["by_season_status"]["3:horizon"] == 2


def test_heads_and_archives_come_from_the_captured_file_by_the_named_rule(pinned: dict):
    g = pinned["grid"]
    assert g["read_time"] == "2026-10-15T19:41:33Z"
    assert len(g["heads"]) == 20 and g["archives_total"] == 43
    assert [a["name"] for a in g["archives"]] == [
        "core-main-pre-20261015T0809Z", "local-maxxing/season2/main", "sanctuary-main-pre-20261015T0809Z", "sanctuary/season2/main", "season2/main",
        "streaming-suite-main-pre-20261015T0809Z", "streaming-suite/season2/main", "web-app-suite-main-pre-20261015T0809Z", "web-app-suite/season2/main"]
    assert all(h["short"] == h["sha"][:10] for h in g["heads"] + g["archives"])


def test_a_heads_file_without_a_read_time_first_line_is_refused_rc2(tmp_path: Path):
    bad = tmp_path / "heads.txt"
    bad.write_text("dc7ec920bafd2c117a269beb3356988f4f3ec859\trefs/heads/master\n")
    r = _facts_raw(heads=bad)
    assert r.returncode == 2 and r.stdout == b"" and b"read time" in r.stderr


def test_box_facts_absent_reads_not_recorded_and_a_present_value_carries_its_provenance(tmp_path: Path, pinned: dict):
    assert all(v == {"value": "not recorded"} for v in pinned["box"].values()) and len(pinned["box"]) == 7
    ok = tmp_path / "box.json"
    ok.write_text(json.dumps({"run_rc": {"value": 0, "command": "season.py rollover --global --apply", "reader_uid": "agi-belam",
                                         "read_time": "2026-10-15T06:24:00Z"}}))
    b = json.loads(_facts_raw("--box-facts", str(ok)).stdout)["box"]
    assert b["run_rc"] == {"value": 0, "command": "season.py rollover --global --apply", "reader_uid": "agi-belam", "read_time": "2026-10-15T06:24:00Z"}
    assert b["pin"] == {"value": "not recorded"}
    for bad in ({"run_rc": {"value": 0}}, {"run_rc": 0}, {"not_a_key": {"value": 1, "command": "c", "reader_uid": "u", "read_time": "t"}}):
        p = tmp_path / "bad.json"
        p.write_text(json.dumps(bad))
        r = _facts_raw("--box-facts", str(p))
        assert r.returncode == 2 and r.stdout == b"", bad


def test_the_script_and_its_fixture_name_no_host_and_no_home_path():
    for p in (CLI, HEADS):
        for needle in ("/home/", "/var/lib/agi", "/data/work"):
            assert needle not in p.read_text(), (p.name, needle)


# ---- P1: the template's slots all resolve against the facts it is rendered from ----------------------------------------------------------
TEMPLATE = HERE.parent / "templates" / "season_report" / "report.html"
_TOKEN = re.compile(r"\{\{(#rows |/rows|#media|/media)?\s*([^}|]*?)\s*(?:\|(\w+))?\}\}")
_ROW_NARRATIVE = {"role"}          # a heads row's role column is written by the narrative, not read from facts


def _resolve(root, path: str):
    cur = root
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return KeyError
        cur = cur[part]
    return cur


def _template_problems(text: str, facts: dict) -> list[str]:
    """The slot grammar legend (an HTML comment) is not part of the page. Every slot is `facts.*` (a scalar that exists), `narr.*`, `media.*` (both inside {{#media}} only for media), or `row.*` inside a loop."""
    out, stack, media = [], [], 0
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    for m in _TOKEN.finditer(text):
        kind, path, flt = m.group(1), m.group(2), m.group(3)
        if kind == "#rows ":
            if path.startswith("facts."):
                lst = _resolve(facts, path[6:])
                if not isinstance(lst, list) or not lst:
                    out.append(f"rows over {path}: not a non-empty list in the facts")
                stack.append(lst[0] if isinstance(lst, list) and lst else {})
            elif path.startswith("narr."):
                stack.append(None)
            else:
                out.append(f"rows over {path}: must be facts.* or narr.*")
                stack.append(None)
        elif kind == "/rows":
            if not stack:
                out.append("{{/rows}} without an open loop")
            else:
                stack.pop()
        elif kind == "#media":
            media += 1
        elif kind == "/media":
            media -= 1
        elif path.startswith("facts."):
            v = _resolve(facts, path[6:])
            if v is KeyError or isinstance(v, (dict, list)):
                out.append(f"{path}: unresolved or not a scalar")
            elif flt == "n" and not isinstance(v, int):
                out.append(f"{path}|n: not an integer")
        elif path.startswith("row."):
            if not stack:
                out.append(f"{path}: outside a loop")
            elif stack[-1] is not None and path[4:] not in stack[-1] and path[4:] not in _ROW_NARRATIVE:
                out.append(f"{path}: the facts row has no such field")
        elif path.startswith("media."):
            if media <= 0:
                out.append(f"{path}: media slot outside {{{{#media}}}}")
        elif not path.startswith("narr."):
            out.append(f"unknown slot {m.group(0)}")
    if stack:
        out.append("a {{#rows}} loop is never closed")
    if media != 0:
        out.append("{{#media}} is unbalanced")
    return out


def test_p1_every_template_slot_resolves_in_the_facts_and_a_typo_mutant_is_red(pinned: dict):
    text = TEMPLATE.read_text()
    assert _template_problems(text, pinned) == []
    assert len(_TOKEN.findall(text)) > 50
    bad = text.replace("{{facts.counts.active_by_dir|n}}", "{{facts.counts.active_by_dr|n}}")
    assert bad != text and _template_problems(bad, pinned) != [], "MUTANT (a typo'd slot) must be RED"
    bad2 = text.replace("{{/rows}}\n  </ol>", "  </ol>", 1)
    assert bad2 != text
    assert _template_problems(bad2, pinned) != [], "MUTANT (an unclosed loop) must be RED"
    bad3 = text.replace("{{#media}}\n  <div", "  <div", 1)
    assert bad3 != text
    assert _template_problems(bad3, pinned) != [], "MUTANT (an unbalanced media block) must be RED"


def test_p1_the_template_carries_no_typed_sha_and_no_seed_number_and_keeps_the_player_inside_the_media_block():
    text = TEMPLATE.read_text()
    standing = re.sub(r"\{\{.*?\}\}", "", text)
    assert not re.search(r"\b[0-9a-f]{7,40}\b", standing), "a typed sha outside a slot"
    for seed in ("2a8056bcb5", "420e00ae9c", "5fa654a5f3", "5,706", "06:24", "08:10Z", "grok", "song-b.mp3", "Lyria"):
        assert seed not in text, f"seed literal {seed!r} left in the template"
    # the player: its <audio>, its button and its <script> exist ONLY between {{#media}} and {{/media}}
    outside = re.sub(r"\{\{#media\}\}.*?\{\{/media\}\}", "", text, flags=re.S)
    for tag in ("<audio", 'id="play"', "<script", "class=\"player\""):
        assert tag not in outside, f"{tag} sits outside the media block"
    assert "<style>" in text and "--accent:#0d6b62" in text, "the seed's style block is kept"
    assert "<title>Season {{facts.season}} Rollover</title>" in text


def test_p1_a_player_outside_the_media_block_mutant_is_red():
    text = TEMPLATE.read_text()
    mut = text.replace("{{#media}}\n  <div class=\"player\"", "  <div class=\"player\"", 1)
    outside = re.sub(r"\{\{#media\}\}.*?\{\{/media\}\}", "", mut, flags=re.S)
    assert 'class="player"' in outside, "MUTANT (player pulled out of the media block) must be RED"
