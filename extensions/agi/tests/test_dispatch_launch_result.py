"""Focused tests for dispatch's adapter-neutral launch result seam."""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
spec = importlib.util.spec_from_file_location("dispatch_launch_result", BIN / "dispatch.py")
dispatch = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = dispatch
spec.loader.exec_module(dispatch)


class FakeProcess:
    pid = 4242


def test_launch_round_reports_created_process_without_pretending_pane(tmp_path, monkeypatch):
    seen = {}

    def fake_popen(argv, **kwargs):
        seen["argv"] = argv
        seen["kwargs"] = kwargs
        return FakeProcess()

    monkeypatch.setattr(dispatch.subprocess, "Popen", fake_popen)
    result = dispatch._launch_round(["pi", "run"], tmp_path / "output.log", tmp_path, {"A": "1"})

    assert isinstance(result, dispatch.LaunchResult)
    assert result.created is True
    assert result.adapter == "subprocess"
    assert result.pane_id is None
    assert result.process.pid == 4242
    assert seen["kwargs"]["start_new_session"] is True
    assert seen["kwargs"]["cwd"] == str(tmp_path)


def test_only_configured_persistent_seat_selects_hold():
    assert dispatch._persistent_hold({"persistent": True}, "grok-seat") \
        is dispatch.tmux_hold
    assert dispatch._persistent_hold({"persistent": True}, None) is None
    assert dispatch._persistent_hold({}, "ordinary-seat") is None


def test_persistent_launch_uses_named_hold_and_refuses_popen(tmp_path, monkeypatch):
    seen = {}

    class FakeHold:
        @staticmethod
        def start(**kwargs):
            seen.update(kwargs)
            return {"process": FakeProcess(), "pane_id": "%7",
                    "created": True, "adapter": "tmux_hold"}

    def forbidden_popen(*args, **kwargs):
        raise AssertionError("persistent seat reached anonymous Popen")

    monkeypatch.setattr(dispatch.subprocess, "Popen", forbidden_popen)
    result = dispatch._launch_round(
        ["grok-bot"], tmp_path / "output.log", tmp_path, {"A": "1"},
        hold=FakeHold, pane_name="grok-seat")

    assert result.pane_id == "%7"
    assert result.adapter == "tmux_hold"
    assert result.created is True
    assert seen["pane_name"] == "grok-seat"
    assert seen["argv"] == ["grok-bot"]


def test_tmux_hold_founds_named_pane_without_fabricating_identity(tmp_path, monkeypatch):
    calls = []

    class Result:
        stdout = "%12\t4242\n"

    def fake_run(argv, **kwargs):
        calls.append((argv, kwargs))
        return Result()

    monkeypatch.setattr(dispatch.tmux_hold.subprocess, "run", fake_run)
    result = dispatch.tmux_hold.start(
        argv=["grok-bot", "run"], log_file=tmp_path / "output.log",
        cwd=tmp_path, env={"A": "1"}, pane_name="grok-seat")

    assert result["pane_id"] == "%12"
    assert result["process"].pid == 4242
    assert result["created"] is True
    assert calls[0][0][:4] == ["tmux", "new-session", "-d", "-s"]
    assert calls[0][0][4] == "grok-seat"
    assert calls[1][0][:3] == ["tmux", "list-panes", "-t"]


def test_open_round_probe_routes_persistent_pane_without_popen(tmp_path, monkeypatch):
    """The live dispatcher's launch seam returns a reusable pane identity."""
    class FakeProcess:
        pid = 909

    class FakeHold:
        @staticmethod
        def start(**kwargs):
            assert kwargs["pane_name"] == "grok-seat"
            return {"process": FakeProcess(), "pane_id": "%9",
                    "created": True, "adapter": "tmux_hold"}

    monkeypatch.setattr(dispatch.subprocess, "Popen",
                        lambda *a, **k: pytest.fail("persistent open used Popen"))
    first = dispatch._open_round_launch(
        ["grok-bot"], tmp_path / "output.log", tmp_path, {"A": "1"},
        None, hold=FakeHold, pane_name="grok-seat", mode="wb")
    second = dispatch._open_round_launch(
        ["grok-bot"], tmp_path / "output.log", tmp_path, {"A": "1"},
        None, hold=FakeHold, pane_name="grok-seat", mode="ab")
    assert (first.created, first.adapter, first.pane_id) == (True, "tmux_hold", "%9")
    assert (second.created, second.adapter, second.pane_id) == (True, "tmux_hold", "%9")


def test_persistent_restart_reattaches_same_pane_without_popen(tmp_path, monkeypatch):
    started, restarted = [], []

    class FakeProcess:
        pid = 700

    def start(**kwargs):
        started.append(kwargs)
        return {"process": FakeProcess(), "pane_id": "%7",
                "created": True, "adapter": "tmux_hold"}

    def restart(**kwargs):
        restarted.append(kwargs)
        return {"process": FakeProcess(), "pane_id": "%7",
                "created": False, "adapter": "tmux_hold"}

    monkeypatch.setattr(dispatch.subprocess, "Popen",
                        lambda *a, **k: pytest.fail("persistent restart used Popen"))
    monkeypatch.setattr(dispatch.tmux_hold, "start", start)
    monkeypatch.setattr(dispatch.tmux_hold, "restart", restart)
    first = dispatch._open_round_launch(
        ["grok-bot"], tmp_path / "output.log", tmp_path, {},
        None, hold=dispatch.tmux_hold, pane_name="grok-seat")
    # The process dies; the recorded pane survives and is the restart target.
    rec = {"launch_adapter": first.adapter, "pane_id": first.pane_id,
           "command": "grok-bot", "log_file": str(tmp_path / "output.log")}
    second = dispatch._persistent_restart(rec, tmp_path, "agent")
    assert first.created is True
    assert (second["pane_id"], second["created"], second["adapter"]) == (
        "%7", False, "tmux_hold")
    assert restarted[0]["pane_id"] == "%7"
    assert started and restarted


    calls = []
    monkeypatch.setattr(dispatch.subprocess, "Popen",
                        lambda argv, **kwargs: calls.append(kwargs) or FakeProcess())
    log = tmp_path / "output.log"

    dispatch._launch_round(["pi"], log, tmp_path, {}, mode="wb")
    dispatch._launch_round(["pi"], log, tmp_path, {}, mode="ab")

    assert log.read_bytes() == b""
    assert len(calls) == 2
