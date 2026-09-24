"""Session capture at rotation (goal:g14.14.8).

Four fixtures, no more:

(a) a fixture transcript carrying a synthetic secret of EVERY pattern class
    scrub.py catches lands with zero remaining candidates -- scrub actually
    ran, through the shared module, not a second redactor;
(b) a fixture with no secrets lands byte-identical modulo the scrub pass;
(c) label.json equals the real `config:posts` row for the seat;
(d) a capture that raises (missing path / obstructed landing dir) does NOT
    propagate past the non-blocking wrapper -- a rotation is never failed by
    its own capture.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate  # noqa: E402


ROW = {
    "name": "adv-local-maxxing",
    "role": "parent",
    "harness": "claude-code",
    "model": "claude-opus-5",
    "provider": "anthropic",
    "town": "local-maxxing",
    "box": "local-town",
}

#: one synthetic secret per scrub.py pattern class.
SECRETS = (
    "ip dotted 10.20.30.40\n"
    "ip hex 0a141e28\n"
    "ip decimal 3232235521\n"
    "sk key sk-or-v1-abcdef1234567890\n"
    "openrouter OPENROUTER_API_KEY\n"
    "email alice@example.com\n"
    "longhex 0123456789abcdef0123456789abcdef01234567\n"
)


def _root(tmp_path):
    graph = tmp_path / ".agi"
    graph.mkdir()
    return graph


def _transcript(tmp_path, name, text):
    p = tmp_path / f"{name}.jsonl"
    p.write_text(text, encoding="utf-8")
    return p


def test_capture_scrubs_every_pattern_class(tmp_path):
    root = _root(tmp_path)
    src = _transcript(tmp_path, "sess-a", SECRETS)
    dest = rotate.capture_session_transcript(
        root, seat="s", row=ROW, transcript_path=src)
    assert dest is not None
    landed = (dest / "transcript.jsonl").read_text(encoding="utf-8")
    scrub = rotate._load_scrub_module(root)
    assert scrub.recheck(landed) == []
    for secret in ("10.20.30.40", "0a141e28", "3232235521",
                   "sk-or-v1-abcdef1234567890", "OPENROUTER_API_KEY",
                   "alice@example.com",
                   "0123456789abcdef0123456789abcdef01234567"):
        assert secret not in landed


def test_capture_clean_transcript_lands_unchanged(tmp_path):
    root = _root(tmp_path)
    raw = '{"type":"user","text":"no secrets here"}\n'
    src = _transcript(tmp_path, "sess-b", raw)
    dest = rotate.capture_session_transcript(
        root, seat="s", row=ROW, transcript_path=src)
    scrub = rotate._load_scrub_module(root)
    scrubbed, counts = scrub.redact_text(raw)
    assert scrubbed == raw
    assert counts == {}
    assert (dest / "transcript.jsonl").read_text(encoding="utf-8") == raw


def test_capture_label_matches_row(tmp_path):
    root = _root(tmp_path)
    src = _transcript(tmp_path, "sess-c", "{}\n")
    dest = rotate.capture_session_transcript(
        root, seat="s", row=ROW, transcript_path=src)
    label = json.loads((dest / "label.json").read_text(encoding="utf-8"))
    for k in ("role", "harness", "model", "provider", "name", "town", "box"):
        assert label[k] == ROW[k]
    assert label["session_id"] == "sess-c"
    assert label["transcript_source"] == "explicit"
    assert "scrub_redactions" in label


def test_capture_error_never_propagates(tmp_path):
    root = _root(tmp_path)
    # a nonexistent transcript path -> the wrapper swallows the read error
    assert rotate._capture_session_safe(
        root, seat="s", row=ROW,
        transcript_path=tmp_path / "missing.jsonl") is None
    # an obstructed landing dir (a FILE where the role dir must be)
    blocked_row = dict(ROW, role="blocked")
    blocked = tmp_path / "datasets" / "sessions" / "blocked"
    blocked.parent.mkdir(parents=True, exist_ok=True)
    blocked.write_text("not a dir\n", encoding="utf-8")
    src = _transcript(tmp_path, "sess-d", "clean\n")
    assert rotate._capture_session_safe(
        root, seat="s", row=blocked_row, transcript_path=src) is None