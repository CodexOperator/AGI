"""Parent negative probes for hypothesis:l4-spawn-without-name-defaults-to-the-
seat-row-name-for-every-non-prime-post. One probe per claim conjunct, run by
the parent against the FINAL built bytes. Import rotate, call the real
cmd_spawn, monkeypatch only spawn_window (the I/O edge) so we can see the name
handed to the launcher AND read the dry-run stdout line.

Not a pytest file: run `python3 .agi/tmp/probe_spawn_name.py`.
"""
import io
import json
import sys
import contextlib
from argparse import Namespace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "extensions" / "agi" / "bin"))
import rotate  # noqa: E402

CAPTURED = []


def fake_spawn(**kw):
    CAPTURED.append(kw)
    return 0, "echo ok"


rotate.spawn_window = fake_spawn


def make_root(tmp):
    root = tmp / "root"
    nodes = root / "nodes" / ".geometry"
    nodes.mkdir(parents=True, exist_ok=True)
    (root / "sessions").mkdir(parents=True, exist_ok=True)
    rows = [
        {"name": "director-post", "role": "director", "model": "x"},
        {"name": "prime-win", "role": "prime_director", "model": "y"},
        {"name": "nokey-post"},  # exists, NO role cell
    ]
    body = "---\nid: config:seats\ntype: config\nseats:\n"
    for r in rows:
        body += "  - " + json.dumps(r) + "\n"
    body += "---\n"
    (nodes / "seats.md").write_text(body, encoding="utf-8")
    (root / "windows.txt").write_text("belam-S1\n", encoding="utf-8")
    return root


def run(root, **over):
    CAPTURED.clear()
    base = dict(name=None, tier="director", model=None, effort=None,
                settings=None, prompt_file=None, successor_argv=None,
                seat=None, tmux_session="t", window_path=str(root / "windows.txt"),
                pid=None, no_autopsy=False, ask_diff=False, dry_run=True)
    base.update(over)
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = rotate.cmd_spawn(Namespace(**base), root)
    return rc, out.getvalue(), err.getvalue()


def printed_name(out):
    for ln in out.splitlines():
        if ln.startswith("spawn name: "):
            return ln.split("spawn name: ", 1)[1].strip().strip("'")
    return None


def main():
    import tempfile
    fails = []
    with tempfile.TemporaryDirectory() as td:
        root = make_root(Path(td))

        # P1 (conjunct 1, wire): non-prime director seat + no --name -> name==seat,
        # and the name handed to the LAUNCHER is the same as the printed one.
        rc, out, err = run(root, seat="director-post")
        got_launcher = CAPTURED[-1]["name"] if CAPTURED else None
        got_print = printed_name(out)
        if got_launcher != "director-post":
            fails.append(f"P1 launcher name={got_launcher!r} != 'director-post'")
        if got_print != "director-post":
            fails.append(f"P1 printed name={got_print!r} != 'director-post'")
        if str(got_launcher).startswith("belam"):
            fails.append(f"P1 got a belam numeral for a non-prime seat: {got_launcher!r}")

        # P2 (conjunct 2, auth): the PRIME row the claim does NOT authorise to
        # the row name, plus no-seat, must both keep the belam derive.
        rc, out, err = run(root, seat="prime-win")
        if CAPTURED[-1]["name"].startswith("belam") is False:
            fails.append("P2 prime seat lost its belam numeral: "
                         f"{CAPTURED[-1]['name']!r}")
        if CAPTURED[-1]["name"] == "prime-win":
            fails.append("P2 prime seat named after the row (not authorised)")
        rc, out, err = run(root)
        if CAPTURED[-1]["name"].startswith("belam") is False:
            fails.append("P2 no-seat changed: "
                         f"{CAPTURED[-1]['name']!r}")

        # P3 (conjunct 3, gate): a row present with NO role cell must fall to
        # derive AND name why in one line -- never silently take the row name.
        rc, out, err = run(root, seat="nokey-post")
        if CAPTURED[-1]["name"].startswith("belam") is False:
            fails.append("P3 roleless seat did not derive: "
                         f"{CAPTURED[-1]['name']!r}")
        if CAPTURED[-1]["name"] == "nokey-post":
            fails.append("P3 roleless seat took the row name")
        lines = [ln for ln in err.splitlines() if "role cell" in ln]
        if len(lines) != 1:
            fails.append(f"P3 expected exactly one reason line, got {lines!r}")

        # P4 (conjunct 4, wire): the dry-run name line exists and is not a
        # hardcoded string -- it tracks the seat (draw runs to prove it).
        rc, out1, _ = run(root, seat="director-post")
        rc, out2, _ = run(root, seat="prime-win")
        if printed_name(out1) == printed_name(out2):
            fails.append("P4 dry-run name line does not track the resolved name")

        # extra: --name always wins
        rc, out, err = run(root, seat="director-post", name="explicit")
        if CAPTURED[-1]["name"] != "explicit":
            fails.append(f"--name lost to seat: {CAPTURED[-1]['name']!r}")

    if fails:
        print("PROBES: FAIL")
        for f in fails:
            print("  -", f)
        return 1
    print("PROBES: PASS (P1 wire name==seat; P2 prime+no-seat derive; "
          "P3 roleless derive + one line; P4 dry-run tracks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
