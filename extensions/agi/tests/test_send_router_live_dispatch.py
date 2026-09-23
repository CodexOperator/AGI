"""The clause-(2) mechanism: a registered send-verb transport is DISPATCHED.

Kid 1's router could register a row but the live `send` verb never reached it:
`choose` raised AmbiguousTransport against the inbox catch-all, and even a
forced choice fell through the literal `if transport == ...` branches. This
test registers a send-verb transport FIRST (ahead of the catch-all), runs the
real `main()`, and asserts its dispatch ran while the built-in inbox writer did
not -- which is what "a new transport is a table row" has to mean.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import send_router  # noqa: E402

spec = importlib.util.spec_from_file_location("send_live", BIN / "send.py")
send_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(send_mod)


def _inbox_shaped(a):
    return (getattr(a, "room", None) is None
            and getattr(a, "dm_to", None) is None)


def test_registered_transport_is_dispatched_by_the_live_send_verb(
        tmp_path, monkeypatch):
    root = tmp_path / "project"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    (root / "sessions").mkdir(parents=True)
    monkeypatch.chdir(root)

    dispatched = []
    builtin = []

    def stub_dispatch(root_, croot, sender, args):
        dispatched.append(list(args.send_args))
        return 0

    monkeypatch.setattr(send_mod, "send", lambda *a, **k: builtin.append(a))
    monkeypatch.setattr(send_mod.last_act, "touch_env", lambda *a, **k: None)

    send_router.register("stub-inbox", "stub", _inbox_shaped, verb="send",
                         dispatch=stub_dispatch, first=True, replace=True)
    try:
        rc = send_mod.main(["--from", "alive", "send", "p1", "hello"])
    finally:
        send_router.TRANSPORTS.pop("stub-inbox", None)
        send_router._RUN.pop("stub-inbox", None)

    assert rc == 0
    assert dispatched == [["p1", "hello"]], "registered dispatch never ran"
    assert builtin == [], "built-in inbox writer ran for a registered transport"
