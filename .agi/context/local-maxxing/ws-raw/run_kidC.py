#!/usr/bin/env python3
"""Kid C probe runner: auth fix, n_probs carriage, top_logprobs carriage,
backend switch (cpu2 + gpu), all against the on-disk ws_raw.py.

Writes .agi/context/local-maxxing/ws-raw/kidB_logprobs.jsonl (raw) and
prints a JSON summary.  CPU servers on 184xx, one per --log-prompts-dir.
"""
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
MODEL = str(Path.home() / ".cache/lm-models/Qwen3-0.6B-Q8_0.gguf")
LLAMA = str(Path.home() / "src/llama.cpp/build/bin/llama-server")
KEY = "sk-ws-raw-test"
PROMPT = "Count from one to twenty."
GPU_KEY = "local"

import asyncio


def free_ports(n):
    ports = []
    for p in range(18400, 18500):
        if len(ports) == n:
            break
        with socket.socket() as s:
            if s.connect_ex(("127.0.0.1", p)) != 0:
                ports.append(p)
    assert len(ports) == n, ports
    return ports


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


async def stream(url, frame, headers=None):
    msgs = []
    async with websockets.connect(url, additional_headers=headers, max_size=8 << 20) as ws:
        await ws.send(json.dumps(frame))
        async for raw in ws:
            m = json.loads(raw)
            msgs.append(m)
            if "error" in m or m.get("done"):
                break
    return msgs


def text_of(msgs):
    return "".join(m.get("token") or "" for m in msgs if not m.get("done"))


def main():
    ports = free_ports(3)
    (p1, p2, wsp) = ports
    cap1, cap2 = OUT / "cap1", OUT / "cap2"
    for c in (cap1, cap2):
        if c.exists():
            for f in c.glob("*.txt"):
                f.unlink()
        c.mkdir(parents=True, exist_ok=True)
    procs = []
    result = {}

    def start_llama(port, cap):
        return subprocess.Popen([
            LLAMA, "-m", MODEL, "--host", "127.0.0.1", "--port", str(port),
            "-np", "1", "-c", "2048", "-t", "4", "--reasoning-format", "none",
            "--no-warmup", "--api-key", KEY, "--log-prompts-dir", str(cap),
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        procs.append(start_llama(p1, cap1))
        procs.append(start_llama(p2, cap2))
        wait_health("http://127.0.0.1:%d" % p1)
        wait_health("http://127.0.0.1:%d" % p2)
        env = dict(os.environ, WS_RAW_KEY=KEY, LOCAL_TOWN_KEY=GPU_KEY)
        wsproc = subprocess.Popen([
            sys.executable, str(BIN / "ws_raw.py"), "--port", str(wsp),
            "--backend", "cpu=http://127.0.0.1:%d" % p1,
            "--backend", "cpu2=http://127.0.0.1:%d" % p2,
            "--backend", "gpu=http://127.0.0.1:18080",
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
        procs.append(wsproc)
        end = time.time() + 15
        while time.time() < end:
            with socket.socket() as s:
                if s.connect_ex(("127.0.0.1", wsp)) == 0:
                    break
            time.sleep(0.2)
        else:
            raise RuntimeError("ws_raw did not bind")
        url = "ws://127.0.0.1:%d/v1/stream" % wsp

        # ---- 1. header auth: Authorization Bearer, NO key field ----
        for mode in ("raw", "chat"):
            if mode == "raw":
                fr = {"mode": "raw", "backend": "cpu", "prompt": PROMPT,
                      "params": {"temperature": 0, "seed": 7, "n_predict": 8}}
            else:
                fr = {"mode": "chat", "backend": "cpu",
                      "messages": [{"role": "user", "content": PROMPT}],
                      "params": {"temperature": 0, "seed": 7, "max_tokens": 8}}
            msgs = asyncio.run(stream(url, fr,
                                      {"Authorization": "Bearer " + KEY}))
            err = next((m["error"] for m in msgs if "error" in m), None)
            result["auth_header_" + mode] = {
                "admitted": err is None,
                "error": err,
                "content_tokens": sum(1 for m in msgs if m.get("token")),
            }
        # negative: no key at all still refused
        msgs = asyncio.run(stream(url, {
            "mode": "raw", "backend": "cpu", "prompt": PROMPT,
            "params": {"temperature": 0, "n_predict": 4}}))
        result["auth_no_key_refused"] = any("error" in m for m in msgs)

        # ---- 2. raw n_probs=5 carriage + sha vs n_probs=0 ----
        rows = []
        base_sha = None
        for req in range(2):
            fr = {"mode": "raw", "backend": "cpu", "key": KEY, "prompt": PROMPT,
                  "params": {"temperature": 0, "seed": 7, "n_predict": 24,
                             "n_probs": 5}}
            msgs = asyncio.run(stream(url, fr))
            for i, m in enumerate(msgs):
                if not m.get("token"):
                    continue
                cp = (m.get("logprobs") or [])
                top = (cp[0].get("top_logprobs") or []) if cp else []
                amax = (max(top, key=lambda e: e["logprob"])["token"]
                        if top else None)
                rows.append({"req": req, "idx": i, "token": m["token"],
                             "n_entries": len(top), "argmax_token": amax,
                             "argmax_ok": amax == m["token"]})
            if req == 0:
                pass
        fr0 = {"mode": "raw", "backend": "cpu", "key": KEY, "prompt": PROMPT,
               "params": {"temperature": 0, "seed": 7, "n_predict": 24}}
        m0 = asyncio.run(stream(url, fr0))
        base_sha = hashlib.sha256(text_of(m0).encode()).hexdigest()[:16]
        np5_sha = hashlib.sha256("".join(r["token"] for r in rows
                                         if r["req"] == 0).encode()).hexdigest()[:16]
        np5_sha2 = hashlib.sha256("".join(r["token"] for r in rows
                                          if r["req"] == 1).encode()).hexdigest()[:16]
        with open(OUT / "kidB_logprobs.jsonl", "w") as fh:
            for r in rows:
                fh.write(json.dumps(r) + "\n")
        result["raw_nprobs"] = {
            "token_frames": len(rows),
            "argmax_ok": sum(1 for r in rows if r["argmax_ok"]),
            "n_entries_set": sorted({r["n_entries"] for r in rows}),
            "sha_nprobs0": base_sha, "sha_nprobs5_req0": np5_sha,
            "sha_nprobs5_req1": np5_sha2,
            "sha_unchanged": base_sha == np5_sha and base_sha == np5_sha2,
        }

        # ---- 3. chat top_logprobs=3 ----
        fr = {"mode": "chat", "backend": "cpu", "key": KEY,
              "messages": [{"role": "user", "content": PROMPT}],
              "params": {"temperature": 0, "seed": 7, "max_tokens": 24,
                         "logprobs": True, "top_logprobs": 3}}
        msgs = asyncio.run(stream(url, fr))
        content = [m for m in msgs if m.get("token")]
        with_lp = [m for m in content if m.get("logprobs")]
        result["chat_top_logprobs"] = {
            "content_deltas": len(content), "with_logprobs": len(with_lp),
            "sample": (with_lp[0]["logprobs"] if with_lp else None),
        }

        # ---- 4. backend switch cpu2: cap2 not cap1 ----
        def capcount(c):
            return len(list(c.glob("*.txt")))
        before1, before2 = capcount(cap1), capcount(cap2)
        fr = {"mode": "raw", "backend": "cpu2", "key": KEY, "prompt": PROMPT,
              "params": {"temperature": 0, "seed": 7, "n_predict": 8}}
        m = asyncio.run(stream(url, fr))
        after1, after2 = capcount(cap1), capcount(cap2)
        result["backend_switch_cpu2"] = {
            "admitted": not any("error" in x for x in m),
            "cap1_before": before1, "cap1_after": after1,
            "cap2_before": before2, "cap2_after": after2,
            "landed_on_cpu2_only": after2 == before2 + 1 and after1 == before1,
        }

        # ---- 5. gpu backend if :18080 listens ----
        gpu_listening = False
        with socket.socket() as s:
            gpu_listening = s.connect_ex(("127.0.0.1", 18080)) == 0
        result["gpu_listening"] = gpu_listening
        if gpu_listening:
            fr = {"mode": "chat", "backend": "gpu", "key": KEY,
                  "key_env": "LOCAL_TOWN_KEY",
                  "messages": [{"role": "user", "content": "Say hi."}],
                  "params": {"temperature": 0, "max_tokens": 16,
                             "model": "Qwen3.5-9B-Q4_K_M"}}
            m = asyncio.run(stream(url, fr))
            err = next((x["error"] for x in m if "error" in x), None)
            result["gpu_chat"] = {
                "admitted": err is None, "error": err,
                "content_tokens": sum(1 for x in m if x.get("token")),
                "reasoning_frames": sum(1 for x in m if x.get("reasoning")),
            }

        print("SUMMARY " + json.dumps(result, default=str))
        (OUT / "kidC_results.json").write_text(json.dumps(result, indent=2, default=str))
    finally:
        for p in reversed(procs):
            if p.poll() is None:
                p.terminate()
                try:
                    p.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    p.kill()
        print("port_closed p1=%s p2=%s ws=%s" % (
            port_closed(p1), port_closed(p2), port_closed(wsp)))


if __name__ == "__main__":
    main()
