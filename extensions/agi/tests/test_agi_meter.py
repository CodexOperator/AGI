"""G10: agi-meter reads the newest transcript line WITH .message.usage, not the last line."""
import json, os, re, subprocess
from pathlib import Path

GEO = Path(__file__).resolve().parents[3] / ".agi/nodes/.geometry"
U = lambda n: {"type": "assistant", "message": {"usage": {"input_tokens": n, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}}}
SYS = {"type": "system", "subtype": "bridge"}

def run(tmp_path, lines, hook=None, window=1000):
    sh = tmp_path / "m.sh"
    sh.write_text(re.search(r"^### agi-meter .*?\n~~~\w*\n(.*?)^~~~", (GEO / "engine-post.md").read_text(), re.S | re.M)[1])
    tr = tmp_path / "t.jsonl"
    tr.write_text("".join((l if isinstance(l, str) else json.dumps(l)) + "\n" for l in lines))
    j = json.dumps(dict(transcript_path=str(tr), **(hook or {})))
    env = dict(os.environ, AGI_WINDOW=str(window), AGI_ROTATE_PCT="50")
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
