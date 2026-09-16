"""Tests for bin/ws_raw.py -- the raw WebSocket adapter. `hypothesis:ws-raw-zero-injection-adapter`.

What these guard, in the order the hypothesis's falsifiers name them:

1. sha identity: a raw and a chat stream through the adapter are byte-equal
   to a direct httpx stream at temperature 0 / seed 7 / cache_prompt false.
2. Zero injection is a measurement, not a promise: llama-server's
   `--log-prompts-dir` capture for each request is byte-equal to the caller's
   prompt (raw) or the `/apply-template` render of the caller's messages
   (chat) -- with a positive control so a broken grep cannot pass.
3. Cancel frees the slot: a client that closes mid-stream leaves
   `/slots[0].is_processing` false within 2 s.
4. The allowlist and the static key are the only surface: an unknown param
   or a wrong key closes 1008 with an `{error}` frame.
5. Import purity: importing ws_raw pulls in no harness module.

Run ALONE (never the bare directory):
    ~/.venv-lm/bin/python -m pytest extensions/agi/tests/test_ws_raw.py -q

The server fixture skips if llama-server or the GGUF is absent, or if the
running interpreter lacks websockets/httpx.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

pytest.importorskip("websockets")
pytest.importorskip("httpx")

import httpx  # noqa: E402
import websockets  # noqa: E402

import ws_raw  # noqa: E402
from ws_raw_client import adapter_stream, direct_stream  # noqa: E402

KEY = "sk-ws-raw-test"
PROMPT = "Count from one to twenty."
MODES = ("raw", "chat")
PAIRS = int(os.environ.get("WS_RAW_N", "2"))
MARKERS = ("CLAUDE.md", "Prayer", "Belam", "CONSTITUTION HEAD",
           "agi-tree map", "THOUGHT:BEGIN")


def _free_ports(n: int) -> list[int]:
    """n distinct free loopback ports in 18400-18499 (one scan, no repeats)."""
    ports: list[int] = []
    for port in range(18400, 18500):
        if len(ports) == n:
            break
        with socket.socket() as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                ports.append(port)
    if len(ports) < n:
        raise RuntimeError("no free ports in 18400-18499")
    return ports


def _llama_binary() -> str | None:
    for cand in (os.environ.get("WS_RAW_LLAMA"),
                 str(Path.home() / "src/llama.cpp/build/bin/llama-server")):
        if cand and Path(cand).exists():
            return cand
    return shutil.which("llama-server")


def _gguf() -> str | None:
    cand = os.environ.get("WS_RAW_GGUF") or str(
        Path.home() / ".cache/lm-models/Qwen3-0.6B-Q8_0.gguf")
    return cand if Path(cand).exists() else None


def _wait_health(base: str, timeout: float = 120.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = httpx.get(base + "/health", timeout=2.0)
            if r.status_code == 200:
                return
        except httpx.HTTPError:
            pass
        time.sleep(0.5)
    raise RuntimeError("llama-server did not become healthy")


def _wait_port_closed(port: int, timeout: float = 10.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        with socket.socket() as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return True
        time.sleep(0.2)
    return False


@pytest.fixture(scope="module")
def servers(tmp_path_factory):
    binary, model = _llama_binary(), _gguf()
    if not binary or not model:
        pytest.skip("llama-server binary or Qwen3-0.6B-Q8_0.gguf absent")
    tmp = tmp_path_factory.mktemp("ws_raw")
    capture = tmp / "capture"
    capture.mkdir()
    llama_port, ws_port = _free_ports(2)
    base = "http://127.0.0.1:%d" % llama_port
    llama = subprocess.Popen([
        binary, "-m", model, "--host", "127.0.0.1", "--port", str(llama_port),
        "-np", "1", "-c", "2048", "-t", "4", "--reasoning-format", "none",
        "--no-warmup", "--api-key", KEY, "--log-prompts-dir", str(capture),
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ws_proc = None
    try:
        _wait_health(base)
        env = dict(os.environ, WS_RAW_KEY=KEY)
        ws_proc = subprocess.Popen([
            sys.executable, str(BIN / "ws_raw.py"), "--port", str(ws_port),
            "--backend", "cpu=" + base,
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
        deadline = time.time() + 15
        while time.time() < deadline:
            with socket.socket() as s:
                if s.connect_ex(("127.0.0.1", ws_port)) == 0:
                    break
            time.sleep(0.2)
        else:
            raise RuntimeError("ws_raw did not bind")
        yield {"base": base, "url": "ws://127.0.0.1:%d/v1/stream" % ws_port,
               "capture": capture, "llama_port": llama_port, "ws_port": ws_port}
    finally:
        for proc in (ws_proc, llama):
            if proc and proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    proc.kill()
        assert _wait_port_closed(llama_port), "llama-server port still open"


def body_for(mode: str, tokens: int = 32) -> dict:
    params = {"temperature": 0, "seed": 7}
    if mode == "raw":
        params["n_predict"] = tokens
        return {"prompt": PROMPT, "stream": True, "cache_prompt": False,
                **params}
    params["max_tokens"] = tokens
    return {"messages": [{"role": "user", "content": PROMPT}], "stream": True,
            "cache_prompt": False, **params}


def payload_for(mode: str, tokens: int = 32) -> dict:
    params = {"temperature": 0, "seed": 7}
    if mode == "raw":
        params["n_predict"] = tokens
    else:
        params["max_tokens"] = tokens
    return params, (PROMPT if mode == "raw"
                    else [{"role": "user", "content": PROMPT}])


@pytest.mark.parametrize("mode", MODES)
def test_sha_identity_direct_vs_adapter(servers, mode):
    params, payload = payload_for(mode)
    shas = {"direct": set(), "adapter": set()}
    for _ in range(PAIRS):
        text, _, n, _ = asyncio.run(
            direct_stream(servers["base"], mode, body_for(mode), KEY))
        shas["direct"].add(hashlib.sha256(text.encode()).hexdigest())
        assert n >= 16, "direct stream too short to be a real comparison"
        text, _, n, _ = asyncio.run(
            adapter_stream(servers["url"], mode, KEY, "cpu", payload, params))
        shas["adapter"].add(hashlib.sha256(text.encode()).hexdigest())
        assert n >= 16, "adapter stream too short to be a real comparison"
    assert len(shas["direct"]) == 1 and shas["direct"] == shas["adapter"], (
        "temp-0 sha mismatch: direct=%s adapter=%s"
        % (shas["direct"], shas["adapter"]))


def test_captures_are_caller_bytes_with_positive_control(servers):
    capture = servers["capture"]
    for f in capture.glob("*.txt"):
        f.unlink()
    for mode in MODES:
        params, payload = payload_for(mode)
        asyncio.run(adapter_stream(servers["url"], mode, KEY, "cpu", payload, params))
    files = sorted(capture.glob("*.txt"))
    assert len(files) == 2, "expected one capture per adapter request, got %d" % len(files)
    renders = {}
    for mode in MODES:
        expected = PROMPT if mode == "raw" else httpx.post(
            servers["base"] + "/apply-template",
            json={"messages": [{"role": "user", "content": PROMPT}]},
            headers={"Authorization": "Bearer " + KEY}, timeout=10,
        ).json()["prompt"]
        renders[mode] = expected
    bodies = [f.read_text() for f in files]
    # one capture per mode; order-insensitive, byte-exact
    assert sorted(bodies) == sorted(renders.values()), (
        "capture != caller bytes/template render: %r" % bodies)
    blob = "\n".join(bodies)
    hits = [m for m in MARKERS if m in blob]
    assert hits == [], "harness marker(s) in capture: %s" % hits
    # positive control: the same markers must hit on a real brief
    control = subprocess.run(
        [sys.executable, str(BIN / "brief.py"), "head", "--tier", "kid"],
        capture_output=True, text=True)
    control_text = control.stdout + control.stderr
    assert any(m in control_text for m in MARKERS), (
        "positive control failed: brief.py head --tier kid matched no marker "
        "-- the grep above proves nothing")


def test_cancel_frees_the_slot(servers):
    params, _ = payload_for("raw", tokens=400)
    asyncio.run(_cancel_after(servers["url"], 3, params))
    deadline = time.time() + 2.0
    while time.time() < deadline:
        slots = httpx.get(servers["base"] + "/slots",
                          headers={"Authorization": "Bearer " + KEY},
                          timeout=5).json()
        if slots and slots[0]["is_processing"] is False:
            return
        time.sleep(0.1)
    pytest.fail("slot still processing 2 s after the client closed")


async def _cancel_after(url: str, n: int, params: dict) -> None:
    frame = {"mode": "raw", "backend": "cpu", "key": KEY, "prompt": PROMPT,
             "params": params}
    async with websockets.connect(url) as ws:
        await ws.send(json.dumps(frame))
        seen = 0
        async for raw in ws:
            if json.loads(raw).get("token"):
                seen += 1
                if seen >= n:
                    break  # leaving the context closes the socket mid-stream


def test_unknown_param_closes_1008(servers):
    code, msg = asyncio.run(_bad_frame(servers["url"], {
        "mode": "raw", "backend": "cpu", "key": KEY, "prompt": PROMPT,
        "params": {"temperature": 0, "system_prompt": "you are helpful"},
    }))
    assert code == 1008 and "system_prompt" in msg["error"]


def test_bad_key_closes_1008(servers):
    code, msg = asyncio.run(_bad_frame(servers["url"], {
        "mode": "raw", "backend": "cpu", "key": "wrong", "prompt": PROMPT,
        "params": {"temperature": 0},
    }))
    assert code == 1008 and msg["error"] == "bad_key"


def test_header_auth_admits_without_key_field(servers):
    """`Authorization: Bearer <key>` with no `key` field is ADMITTED.

    websockets 15.0.1 serves via websockets.asyncio.server, whose handler
    gets a ServerConnection with the handshake Request at ws.request -- the
    old ws.request_headers attribute does not exist there. This is the
    regression guard for that exact near-miss.
    """
    # no credential at all is still refused
    code, msg = asyncio.run(_bad_frame(servers["url"], {
        "mode": "raw", "backend": "cpu", "prompt": PROMPT,
        "params": {"temperature": 0, "n_predict": 4},
    }))
    assert code == 1008 and msg["error"] == "bad_key"
    # the header alone is enough
    text, n, err = asyncio.run(_stream_with_headers(
        servers["url"],
        {"mode": "raw", "backend": "cpu", "prompt": PROMPT,
         "params": {"temperature": 0, "seed": 7, "n_predict": 8}},
        {"Authorization": "Bearer " + KEY}))
    assert err is None, "header auth refused: %r" % err
    assert n >= 4, "header auth admitted but streamed %d tokens" % n


async def _stream_with_headers(url: str, frame: dict, headers: dict):
    async with websockets.connect(url, additional_headers=headers) as ws:
        await ws.send(json.dumps(frame))
        n, err = 0, None
        async for raw in ws:
            msg = json.loads(raw)
            if "error" in msg:
                err = msg["error"]
                break
            if msg.get("token"):
                n += 1
            if msg.get("done"):
                break
        return None, n, err


async def _bad_frame(url: str, frame: dict):
    """Send a frame the adapter must refuse; return (close code, error frame)."""
    async with websockets.connect(url) as ws:
        await ws.send(json.dumps(frame))
        msg = json.loads(await ws.recv())
        try:
            await ws.recv()
        except websockets.ConnectionClosed as exc:
            rcvd = getattr(exc, "rcvd", None)
            return (rcvd.code if rcvd is not None else exc.code), msg
        raise AssertionError("adapter did not close after an {error} frame")


def test_import_purity():
    """`import ws_raw` must pull in no harness module."""
    script = (
        "import sys, json\n"
        "sys.path.insert(0, %r)\n"
        "import ws_raw\n"
        "bad = sorted(m for m in sys.modules if m.split('.')[0] in "
        "{'brief', 'dispatch', 'adapters', 'hooks', 'cli'})\n"
        "print(json.dumps(bad))\n"
    ) % str(BIN)
    out = subprocess.run([sys.executable, "-c", script], capture_output=True,
                         text=True, cwd=str(BIN))
    assert out.returncode == 0, out.stderr
    assert json.loads(out.stdout) == [], (
        "ws_raw imported harness module(s): %s" % out.stdout.strip())
