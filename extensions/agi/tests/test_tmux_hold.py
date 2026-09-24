"""The held restart gives a fresh pane private-server env, never tmux-server inheritance."""
from __future__ import annotations
import io, json, os, shutil, signal, subprocess, sys, time
from pathlib import Path
import pytest
BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
from adapters import pi_adapter, tmux_hold

@pytest.fixture
def fake_tmux(tmp_path, monkeypatch):
    state=tmp_path/"state.json"
    def run(argv, *, env, **kw):
        cmd=argv[3:]
        if cmd[:1]==["kill-server"]:
            state.unlink(missing_ok=True); out=""
        elif cmd[:1]==["new-session"]:
            state.write_text(json.dumps({"pid":321,"dead":0,"env":env,"argv":list(map(str,cmd))})); out="321\n"
        elif cmd[:1]==["display-message"] and state.exists():
            s=json.loads(state.read_text()); out=f"{s['pid']} {s['dead'] if len(cmd)>3 else ''}\n"
        else: out=""
        return subprocess.CompletedProcess(argv, 0, out, "")
    monkeypatch.setattr(tmux_hold.subprocess, "run", run)
    return state

def env():
    return {"PATH": os.environ["PATH"], "HARNESS_MARKER": "client-new"}

def test_initial_pane_uses_exact_env_without_secret_argv(fake_tmux, tmp_path):
    e=env()
    with (tmp_path/"held.log").open("ab") as log:
        assert tmux_hold.start_held(["pi","run"], e, cwd=tmp_path, pane_name="agi-a", log_file=log)==321
    got=json.loads(fake_tmux.read_text()); assert got["env"]==e
    assert "client-new" not in " ".join(got["argv"])

def test_live_pane_is_reattached_without_respawn(fake_tmux, tmp_path):
    e=env()
    with (tmp_path/"x").open("ab") as log:
        assert tmux_hold.start_held(["pi"],e,cwd=tmp_path,pane_name="agi-a",log_file=log)==321
        before=json.loads(fake_tmux.read_text())
        assert tmux_hold.start_held(["other"],e,cwd=tmp_path,pane_name="agi-a",log_file=log)==321
    assert json.loads(fake_tmux.read_text())==before

def test_dead_pane_respawns_with_fresh_server_env(fake_tmux, tmp_path):
    e=env()
    with (tmp_path/"x").open("ab") as log:
        tmux_hold.start_held(["pi"],e,cwd=tmp_path,pane_name="agi-a",log_file=log)
        s=json.loads(fake_tmux.read_text()); s["dead"]=1; fake_tmux.write_text(json.dumps(s))
        e["HARNESS_MARKER"]="replacement"
        assert tmux_hold.start_held(["pi"],e,cwd=tmp_path,pane_name="agi-a",log_file=log)==321
    assert json.loads(fake_tmux.read_text())["env"]==e

def test_missing_tmux_falls_back_to_sanitized_popen(tmp_path, monkeypatch):
    monkeypatch.setenv("PATH", str(tmp_path/"empty")); (tmp_path/"empty").mkdir()
    class P:
        pid=123
    seen={}
    monkeypatch.setattr(tmux_hold.subprocess,"Popen",lambda *a,**kw: seen.update(args=a,kwargs=kw) or P())
    with (tmp_path/"x").open("ab") as log:
        assert tmux_hold.start_held(["pi"],env(),cwd=tmp_path,pane_name="agi-a",log_file=log)==123
    assert seen["kwargs"]["env"]==env()

@pytest.mark.skipif(shutil.which("tmux") is None, reason="tmux is not installed")
def test_real_tmux_initial_and_dead_replacement_get_fresh_env(tmp_path):
    """Execute the pane shell, rather than mocking new-session's return value."""
    pane = f"real-test-{os.getpid()}-{tmp_path.name}"
    socket = tmux_hold._socket(pane)
    first, second = tmp_path / "first", tmp_path / "second"
    e = {"PATH": os.environ["PATH"], "HARNESS_MARKER": "first"}
    assert "OPENROUTER_API_KEY" not in e
    log = tmp_path / "held.log"
    def child(marker):
        return ["sh", "-c", f'printf "%s" "$HARNESS_MARKER" > "$1"; sleep 30', "child", str(marker)]
    try:
        with log.open("ab") as fh:
            pid = tmux_hold.start_held(child(first), e, cwd=tmp_path, pane_name=pane, log_file=fh)
            assert pid > 0
            for _ in range(20):
                if first.exists():
                    break
                time.sleep(0.05)
            assert first.read_text() == "first"
            os.kill(pid, signal.SIGKILL)
            time.sleep(0.1)
            e = {**e, "HARNESS_MARKER": "second"}
            replacement = tmux_hold.start_held(child(second), e, cwd=tmp_path, pane_name=pane, log_file=fh)
            assert replacement > 0
            for _ in range(20):
                if second.exists():
                    break
                time.sleep(0.05)
            assert second.read_text() == "second"
    finally:
        subprocess.run(["tmux", "-L", socket, "kill-server"], capture_output=True, check=False)


def test_restart_uses_held_path_and_live_config_declares_opt_in(tmp_path, fake_tmux, monkeypatch):
    sess=tmp_path/"sess"; sess.mkdir(); monkeypatch.setattr(pi_adapter,"build_command",lambda **kw:["pi","run"])
    monkeypatch.setattr(pi_adapter,"child_env",lambda **kw:env()); monkeypatch.setenv("HOLD_PANE","1")
    assert pi_adapter.restart(harness={},tier="kid",context_file="x",agent_id="a",iter_n=1,sess_dir=sess)==321
    assert json.loads(fake_tmux.read_text())["env"]==env()
    root=Path(__file__).resolve().parents[3]; cfg=json.loads((root/".agi/config.json").read_text())
    assert cfg["hold_pane"]=={"enabled":False,"env_override":"HOLD_PANE"}
    monkeypatch.delenv("HOLD_PANE"); assert not tmux_hold.enabled()
