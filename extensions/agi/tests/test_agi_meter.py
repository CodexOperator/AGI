"""G10: agi-meter reads the newest transcript line WITH .message.usage, not the last line."""
import json, os, re, subprocess
from pathlib import Path

GEO = Path(__file__).resolve().parents[3] / ".agi/nodes/.geometry"
U = lambda n: {"type": "assistant", "message": {"usage": {"input_tokens": n, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}}}
SYS = {"type": "system", "subtype": "bridge"}

def piece(name):
    return re.search(rf"^### {name} .*?\n~~~\w*\n(.*?)^~~~", (GEO / "engine-post.md").read_text(), re.S | re.M)[1]


def run(tmp_path, lines, hook=None, window=1000, trunk="HEAD"):
    sh = tmp_path / "m.sh"
    sh.write_text(piece("agi-meter"))
    tr = tmp_path / "t.jsonl"
    tr.write_text("".join((l if isinstance(l, str) else json.dumps(l)) + "\n" for l in lines))
    j = json.dumps(dict(transcript_path=str(tr), **(hook or {})))
    # hermetic to what is INSTALLED (SM's finding 22:5xZ 10-25, alive's lens 22:48Z): the meter runs agi-mem / agi-atomize / agi-notice from
    # PATH, and the conftest strips every AGI_* var. agi-mem is the TREE UNDER TEST's piece (a stub that prints nothing would pass the
    # meter's silent rows whatever the real one prints) run against a scratch engine repo whose posts.md it can read, AGI_TRUNK naming a ref
    # that repo has; atomize / notice are stubs (they are not under test here).
    stubs = tmp_path / "stubs"
    stubs.mkdir(exist_ok=True)
    (stubs / "agi-mem").write_text(piece("agi-mem"))
    for name in ("agi-atomize", "agi-notice"):
        (stubs / name).write_text("#!/bin/sh\ncat >/dev/null 2>&1\nexit 0\n")
    for f in stubs.iterdir():
        f.chmod(0o755)
    eng = tmp_path / "eng"
    if not eng.exists():
        g = eng / ".agi" / "nodes" / ".geometry"
        g.mkdir(parents=True)
        (g / "posts.md").write_text('---\nid: config:posts\nposts:\n  - {"name": "p", "mem": "none"}\n---\n')
        for c in (["init", "-q", "."], ["config", "core.hooksPath", "/dev/null"], ["add", "-A", ".agi"],
                  ["-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", "commit", "-qm", "x"]):
            subprocess.run(["git", "-C", str(eng)] + c, check=True, capture_output=True)
    env = dict(os.environ, AGI_WINDOW=str(window), AGI_ROTATE_PCT="50", AGI_ENGINE=str(eng), AGI_TRUNK=trunk,
               AGI_POST="p", HOME=str(tmp_path), PATH=f"{stubs}:{os.environ.get('PATH', '')}")
    return subprocess.run(["sh", str(sh)], input=j, env=env, capture_output=True, text=True)


def test_a_last_line_no_usage_earlier_over_the_line(tmp_path):
    r = run(tmp_path, [U(900), SYS])
    assert r.returncode == 0 and "At the line (900/1000)" in r.stdout


def test_b_under_the_line_is_silent(tmp_path):
    r = run(tmp_path, [U(100), SYS])
    assert r.returncode == 0 and r.stdout == ""


def test_c_tokens_in_hook_wins(tmp_path):
    assert "(900/1000)" in run(tmp_path, [U(100), SYS], {"tokens": 900}).stdout
    assert run(tmp_path, [U(900), SYS], {"tokens": 100}).stdout == ""


def test_d_no_usage_line_is_silent_exit_0(tmp_path):
    r = run(tmp_path, [SYS, {"type": "user"}, "not json"])
    assert r.returncode == 0 and r.stdout == ""


def test_e_text_mentioning_usage_is_skipped(tmp_path):
    txt = {"type": "assistant", "message": {"content": [{"type": "text", "text": 'the "usage" word'}]}}
    assert "(900/1000)" in run(tmp_path, [U(900), txt, SYS]).stdout


def test_null_field_counts_as_zero(tmp_path):
    assert "(900/1000)" in run(tmp_path, [{"message": {"usage": {"input_tokens": 900, "cache_read_input_tokens": None}}}]).stdout


def test_non_object_usage_is_skipped(tmp_path):
    bad = [{"message": {"usage": v}} for v in ("x", [1], 7)] + [{"message": "s"}, 5]
    assert "(900/1000)" in run(tmp_path, [U(900)] + bad + [SYS]).stdout


def test_scan_stops_at_first_valid_usage_line(tmp_path):  # the scan stops at the newest VALID usage line from the end
    poison = {"message": {"usage": {"input_tokens": "a", "cache_read_input_tokens": "b"}}}
    r = run(tmp_path, [poison] * 3 + [SYS, U(900)])
    assert r.returncode == 0 and "(900/1000)" in r.stdout


def test_poison_reached_first_is_skipped_not_fatal(tmp_path):
    poison = {"message": {"usage": {"input_tokens": "a", "cache_read_input_tokens": "b"}}}
    r = run(tmp_path, [U(900), poison, SYS])
    assert r.returncode == 0 and "(900/1000)" in r.stdout and r.stderr == ""


def test_string_cache_field_counts_zero(tmp_path):
    r = run(tmp_path, [U(100), {"message": {"usage": {"input_tokens": 900, "cache_read_input_tokens": "b", "cache_creation_input_tokens": 5}}}], window=1800)
    assert "(905/1800)" in r.stdout and r.stderr == ""


def test_f_the_trees_agi_mem_on_an_unreadable_trunk_warns_once_and_the_meter_goes_on(tmp_path):
    """alive 22:48Z: the interaction that broke is asserted, not hidden. With AGI_TRUNK naming no ref, the tree's agi-mem prints its ONE
    `[mem] warn` line on the meter's stdout (rc 0 by agi-mem's design) and the meter still speaks; with a readable trunk it is silent."""
    r = run(tmp_path, [U(100), SYS], trunk="nosuchref")
    assert r.returncode == 0
    assert r.stdout == "[mem] warn: posts.md unreadable at nosuchref (the turn goes on)\n"
    r = run(tmp_path, [U(900), SYS], trunk="nosuchref")
    assert r.returncode == 0 and "At the line (900/1000)" in r.stdout and r.stdout.count("[mem] warn") == 1
