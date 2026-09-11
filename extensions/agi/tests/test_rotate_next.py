"""rotate.py next -- the DRIVEN (operator) startup path
(hypothesis:l4-startup-is-one-script-or-a-driven-prompt, operator round).

`next --seat S` PRINTS exactly one literal command per call — the next
`startup` step from the SAME template the automated rotate-self path runs
(first_turn then after_join), placeholders resolved with the SAME
`_resolve_startup_placeholders` — and advances only on a recorded success
(`--record-ok`). It NEVER runs a command; the operator does. Hermetic —
fixtures only, no real spawn, no tmux, no graph."""
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate  # noqa: E402


@pytest.fixture
def graph(tmp_path):
    """A hermetic project graph dir: `nodes/` + a rotations.md template whose
    `director` role carries a 3-step startup (2 first_turn + 1 after_join). The
    first command is placeholder-spam on purpose, so the "no {placeholder}"
    constraint ([e]) is exercised by every printed step."""
    g = tmp_path / "graph"
    (g / "nodes" / ".geometry").mkdir(parents=True)
    body = {
        "director": {
            "startup": {
                "first_turn": [
                    {"label": "rot-record",
                     "cmd": "python3 extensions/agi/bin/rotate.py whois "
                            "--seat {seat} --ref {succ_ref} --gen {gen}"},
                    {"label": "seat-row",
                     "cmd": "python3 extensions/agi/bin/send.py whois "
                            "{succ_ref} --claim {seat}"},
                ],
                "after_join": [
                    {"label": "pin",
                     "cmd": "python3 extensions/agi/bin/rotate.py meter "
                            "--pin {pin_ref} --session-log {succ_transcript}"},
                ],
            }
        }
    }
    dumped = yaml.safe_dump(body, sort_keys=False)
    # indent ONE level under the `templates:` key, or `director` parses as a
    # sibling of `templates` instead of its child (empty template => refuse)
    indented = "  " + dumped.replace("\n", "\n  ")
    (g / "nodes" / ".geometry" / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\n"
        "templates:\n" + indented + "---\n", encoding="utf-8")
    return g


def _args(graph, *, record=None, js=False, role="director", template=None):
    return SimpleNamespace(seat="sanctuary-director", role=role,
                           template=template, record=record, json=js,
                           gen=None, succ_name=None, tmux_session="agi-rc",
                           root=str(graph))


def _run(graph, capsys, **kw):
    rc = rotate.cmd_next(_args(graph, **kw), graph)
    return rc, capsys.readouterr().out


def test_a_fresh_seat_prints_first_command_verbatim(graph, capsys):
    rc, out = _run(graph, capsys)
    assert rc == 0
    assert out.strip() == ("python3 extensions/agi/bin/rotate.py whois "
                           "--seat sanctuary-director --ref  --gen 1")


def test_b_record_ok_advances_to_second(graph, capsys):
    _run(graph, capsys)                 # prints step 0
    rc, out = _run(graph, capsys, record="ok")  # step 0 ok -> step 1
    assert rc == 0
    assert out.strip() == ("python3 extensions/agi/bin/send.py whois  "
                           "--claim sanctuary-director")


def test_c_recorded_failure_reprints_same_step(graph, capsys):
    _, first = _run(graph, capsys)
    _, after = _run(graph, capsys, record="fail")   # step 0 marked fail
    assert after.strip() == first.strip()
    # a plain `next` after the failure still offers the SAME step, not the next
    _, again = _run(graph, capsys)
    assert again.strip() == first.strip()


def test_d_exhausted_list_says_so_once(graph, capsys):
    for _ in range(3):
        _run(graph, capsys, record="ok")   # 3rd ok -> exhausted
    rc, out = _run(graph, capsys)
    assert rc == 0
    assert out.count("STARTUP DONE") == 1
    assert out.strip().splitlines() == [rotate.STARTUP_DONE_LINE]
    # a repeat call still says done on one line, still exit 0 (not an error)
    rc2, out2 = _run(graph, capsys, record="ok")
    assert rc2 == 0 and len(out2.strip().splitlines()) == 1


def test_e_printed_command_has_no_unresolved_placeholder(graph, capsys):
    # walk every step; each printed line must carry no leftover {placeholder}
    for _ in range(3):
        rc, out = _run(graph, capsys, record="ok")
        assert rc == 0
        assert "{" not in out and "}" not in out, out


def test_f_json_shape(graph, capsys):
    _, out = _run(graph, capsys, js=True)
    env = json.loads(out)
    assert env["seat"] == "sanctuary-director"
    assert env["complete"] is False
    assert env["index"] == 0
    assert env["label"] == "rot-record"
    assert env["phase"] == "first_turn"
    assert env["steps_total"] == 3 and env["steps_done"] == 0
    assert "cmd" in env and "{" not in env["cmd"]
    # exhaust -> a single-line complete:true object
    for _ in range(3):
        _run(graph, capsys, record="ok")
    _, dout = _run(graph, capsys, js=True)
    done = json.loads(dout)
    assert done["complete"] is True
    assert done["steps_done"] == done["steps_total"] == 3