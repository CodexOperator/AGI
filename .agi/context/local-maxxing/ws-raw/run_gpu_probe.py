#!/usr/bin/env python3
"""Kid D: is the GPU backend's zero content frames the endpoint's or the
adapter's?  Direct httpx vs ws_raw.py at the IDENTICAL request, plus the
chat_template_kwargs direction proof on a local CPU server with
--log-prompts-dir captures.

Writes kidC_gpu.jsonl (one JSON object per row) and prints SUMMARY.
Budget: 2 GPU generations, <= 16 max_tokens each.
"""
import asyncio
import hashlib
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import httpx
import websockets

ROOT = Path("/home/ubuntu/work/agi/.agi/worktrees/a00-2f819956")
BIN = ROOT / "extensions/agi/bin"
OUT = ROOT / ".agi/context/local-maxxing/ws-raw"
JOURNAL = OUT / "kidC_gpu.jsonl"
MODEL = str(Path.home() / ".cache/lm-models/Qwen3-0.6B-Q8_0.gguf")
LLAMA = str(Path.home() / "src/llama.cpp/build/bin/llama-server")

GPU = "http://127.0.0.1:18080"
GPU_KEY = os.environ.get("LOCAL_TOWN_KEY", "local")
GPU_MODEL = "Qwen3.5-9B-Q4_K_M"
WS_KEY = "sk-ws-raw-test"

MESSAGES = [{"role": "user", "content": "hi"}]
PARAMS = {"temperature": 0, "max_tokens": 16, "model": GPU_MODEL}


def loadavg():
    return open("/proc/loadavg").read().split()[:3]


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def journal(row):
    row["loadavg"] = loadavg()
    with open(JOURNAL, "a") as fh:
        fh.write(json.dumps(row, default=str) + "\n")
    print("ROW " + json.dumps(row, default=str))


def direct_chat(base, messages, params, key, extra=None):
    body = {"messages": messages, "stream": True, "cache_prompt": False,
            **params}
    if extra:
        body.update(extra)
    headers = {"Authorization": "Bearer " + key} if key else {}
    content, reasoning, finish = [], [], None
    with httpx.Client(timeout=None) as c:
        with c.stream("POST", base + "/v1/chat/completions", json=body,
                      headers=headers) as r:
            if r.status_code != 200:
                return {"status": r.status_code,
                        "error": r.read().decode("utf-8", "replace")[:400],
                        "content_deltas": 0, "reasoning_deltas": 0,
                        "finish_reason": None, "content_sha": sha("")}
            for line in r.iter_lines():
                if not line.startswith("data:"):
                    continue
                d = line[5:].strip()
                if not d or d == "[DONE]":
                    continue
                p = json.loads(d)
                for ch in p.get("choices") or []:
                    delta = ch.get("delta") or {}
                    if delta.get("content"):
                        content.append(delta["content"])
                    if delta.get("reasoning_content"):
                        reasoning.append(delta["reasoning_content"])
                    if ch.get("finish_reason"):
                        finish = ch["finish_reason"]
    return {"status": 200, "error": None,
            "content_deltas": len(content), "reasoning_deltas": len(reasoning),
            "finish_reason": finish,
            "content_sha": sha("".join(content)),
            "content": "".join(content)[:120],
            "reasoning_head": "".join(reasoning)[:120]}


async def adapter_stream(url, frame):
    msgs = []
    async with websockets.connect(url, max_size=8 << 20) as ws:
        await ws.send(json.dumps(frame))
        async for raw in ws:
            m = json.loads(raw)
            msgs.append(m)
            if "error" in m or m.get("done"):
                break
    return msgs


def adapter_metrics(msgs):
    content = [m["token"] for m in msgs if m.get("token")]
    reasoning = [m["reasoning"] for m in msgs if m.get("reasoning")]
    done = next((m for m in msgs if m.get("done")), None)
    err = next((m["error"] for m in msgs if "error" in m), None)
    return {"error": err, "content_deltas": len(content),
            "reasoning_deltas": len(reasoning),
            "finish_reason": (done or {}).get("stop_type"),
            "content_sha": sha("".join(content)),
            "content": "".join(content)[:120],
            "reasoning_head": "".join(reasoning)[:120],
            "tokens": (done or {}).get("tokens")}


def free_port():
    for p in range(18400, 18500):
        with socket.socket() as s:
            if s.connect_ex(("127.0.0.1", p)) != 0:
                return p
    raise RuntimeError("no free port")


def wait_health(base, timeout=120):
    end = time.time() + timeout
    while time.time() < end:
        try:
            if httpx.get(base + "/health", timeout=2).status_code == 200:
                return
        except httpx.HTTPError:
            pass
        time.sleep(0.4)
    raise RuntimeError("no health at " + base)


def port_closed(p, timeout=10):
    end = time.time() + timeout
    while time.time() < end:
        with socket.socket() as s:
            if s.connect_ex(("127.0.0.1", p)) != 0:
                return True
        time.sleep(0.2)
    return False


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if JOURNAL.exists():
        JOURNAL.unlink()
    proc = None
    summary = {}

    # ---------- 1. what model does :18080 actually serve ----------
    models = httpx.get(GPU + "/v1/models", timeout=10).json()
    ids = [m.get("id") for m in models.get("data", [])]
    args = [m.get("status", {}).get("args") for m in models.get("data", [])]
    summary["gpu_models"] = {"ids": ids, "args0": args[0] if args else None}
    journal({"probe": "gpu_models", "ids": ids, "args": args[0] if args else None})

    # ---------- 2. direct chat stream, no auth first ----------
    base = GPU
    direct = direct_chat(base, MESSAGES, PARAMS, "")
    if direct["status"] == 401:
        direct = direct_chat(base, MESSAGES, PARAMS, GPU_KEY)
        direct["auth"] = "bearer"
    else:
        direct["auth"] = "none"
    journal({"probe": "gpu_direct", "side": "direct", "body_params": PARAMS,
             **direct})

    # ---------- 3. same request through ws_raw.py ----------
    wsport = free_port()
    p = None
    proc = None
    wsproc = None
    env = dict(os.environ, WS_RAW_KEY=WS_KEY)
    wsproc = subprocess.Popen([
        sys.executable, str(BIN / "ws_raw.py"), "--port", str(wsport),
        "--backend", "gpu=" + GPU,
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    try:
        end = time.time() + 15
        while time.time() < end:
            with socket.socket() as s:
                if s.connect_ex(("127.0.0.1", wsport)) == 0:
                    break
            time.sleep(0.2)
        else:
            raise RuntimeError("ws_raw did not bind")
        url = "ws://127.0.0.1:%d/v1/stream" % wsport
        frame = {"mode": "chat", "backend": "gpu", "key": WS_KEY,
                 "messages": MESSAGES, "params": PARAMS}
        msgs = asyncio.run(adapter_stream(url, frame))
        ad = adapter_metrics(msgs)
        journal({"probe": "gpu_adapter", "side": "adapter", "body_params": PARAMS,
                 **ad})

        # ---------- 4. the comparison ----------
        cmp = {
            "direct_content": direct["content_deltas"],
            "adapter_content": ad["content_deltas"],
            "direct_reasoning": direct["reasoning_deltas"],
            "adapter_reasoning": ad["reasoning_deltas"],
            "direct_finish": direct["finish_reason"],
            "adapter_finish": ad["finish_reason"],
            "direct_sha": direct["content_sha"],
            "adapter_sha": ad["content_sha"],
            "sha_equal": direct["content_sha"] == ad["content_sha"],
            "both_zero_content": (direct["content_deltas"] == 0
                                  and ad["content_deltas"] == 0),
        }
        summary["gpu_compare"] = cmp
        journal({"probe": "gpu_compare", **cmp})

        # ---------- 5. chat_template_kwargs direction, CPU, captured ----------
        p = free_port()
        cap = OUT / "capD"
        cap.mkdir(parents=True, exist_ok=True)
        for f in cap.glob("*.txt"):
            f.unlink()
        proc = subprocess.Popen([
            LLAMA, "-m", MODEL, "--host", "127.0.0.1", "--port", str(p),
            "-np", "1", "-c", "2048", "-t", "4", "--reasoning-format", "none",
            "--no-warmup", "--jinja", "--api-key", WS_KEY,
            "--log-prompts-dir", str(cap),
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        cbase = "http://127.0.0.1:%d" % p
        wait_health(cbase)
        cpu_frame = {"mode": "chat", "backend": "cpu", "key": WS_KEY,
                     "messages": MESSAGES,
                     "params": {"temperature": 0, "max_tokens": 4}}
        cpu_url = "ws://127.0.0.1:%d/v1/stream" % wsport
        # adapter for cpu needs its own backend name
        wsproc.terminate()
        try:
            wsproc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            wsproc.kill()
        wsproc = subprocess.Popen([
            sys.executable, str(BIN / "ws_raw.py"), "--port", str(wsport),
            "--backend", "cpu=" + cbase,
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
        end = time.time() + 15
        while time.time() < end:
            with socket.socket() as s:
                if s.connect_ex(("127.0.0.1", wsport)) == 0:
                    break
            time.sleep(0.2)

        def capfiles():
            return sorted(cap.glob("*.txt"), key=lambda f: f.stat().st_mtime)

        before = len(capfiles())
        asyncio.run(adapter_stream(cpu_url, dict(cpu_frame)))
        after = capfiles()
        assert len(after) == before + 1, (before, len(after))
        cap_no_kw = after[-1].read_bytes()

        tmpl = httpx.post(cbase + "/apply-template",
                          json={"messages": MESSAGES},
                          headers={"Authorization": "Bearer " + WS_KEY},
                          timeout=30).json()
        render = tmpl.get("prompt", "")
        journal({"probe": "chat_template_kwargs", "which": "without",
                 "capture_sha": sha(cap_no_kw.decode("utf-8", "replace")),
                 "render_sha": sha(render),
                 "capture_equals_render": cap_no_kw == render.encode(),
                 "capture_head": cap_no_kw.decode("utf-8", "replace")[:160],
                 "render_head": render[:160]})

        before = len(capfiles())
        asyncio.run(adapter_stream(cpu_url, dict(
            cpu_frame, params={"temperature": 0, "max_tokens": 4,
                               "chat_template_kwargs": {"enable_thinking": False}})))
        after = capfiles()
        cap_kw = after[-1].read_bytes()
        journal({"probe": "chat_template_kwargs", "which": "with",
                 "capture_sha": sha(cap_kw.decode("utf-8", "replace")),
                 "capture_head": cap_kw.decode("utf-8", "replace")[:160],
                 "differs_from_no_kw": cap_kw != cap_no_kw})

        summary["chat_template_kwargs"] = {
            "capture_equals_apply_template": cap_no_kw == render.encode(),
            "kwarg_changes_render": cap_kw != cap_no_kw,
            "render": render[:200],
            "capture_head": cap_no_kw.decode("utf-8", "replace")[:200],
            "kw_capture_head": cap_kw.decode("utf-8", "replace")[:200],
        }
        print("SUMMARY " + json.dumps(summary, default=str))
        (OUT / "kidC_gpu_summary.json").write_text(
            json.dumps(summary, indent=2, default=str))
    finally:
        for pr in (proc, wsproc):
            if pr is not None and pr.poll() is None:
                pr.terminate()
                try:
                    pr.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    pr.kill()
        if p is not None:
            print("cpu_port_closed %s" % port_closed(p))
        print("ws_port_closed %s" % port_closed(wsport))


if __name__ == "__main__":
    main()
