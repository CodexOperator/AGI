#!/usr/bin/env python3
"""ws_raw.py -- raw WebSocket relay in front of a llama-server.

Zero injection is a construction here, not a policy:
  * the first frame is parsed against a per-mode ALLOWLIST; an unknown
    top-level key or param closes 1008 with an {error} frame
  * the request body is built from allowlisted fields only; chat messages
    are forwarded verbatim (no system turn, no chat_template_kwargs unless
    the caller sent it)
  * static key compared with hmac.compare_digest; mismatch closes 1008
  * one httpx stream, one ws.send per SSE event -> a slow client throttles
    the relay; backpressure is cancel, never an unbounded buffer
  * client close exits the httpx context -> the backend socket closes
  * binds 127.0.0.1 only

Allowed imports: asyncio, hmac, json, os, sys, httpx, websockets.
Nothing from the harness (no brief, dispatch, adapters, hooks) may be
imported -- tests/test_ws_raw.py asserts that on sys.modules.

Usage:
    WS_RAW_KEY=secret python3 ws_raw.py --port 18431 \
        --backend cpu=http://127.0.0.1:18430

First frame (JSON object):
    {"mode": "raw"|"chat", "backend": "cpu", "key": "...",
     "prompt": "...",                    # raw
     "messages": [{"role": "...", ...}], # chat, forwarded verbatim
     "key_env": "CLOUD_API_KEY",         # optional: backend key from this env var
     "params": {"temperature": 0, "seed": 7, "max_tokens": 16, ...}}

Server frames: {"token": "..."} | {"token": "", "done": true, "usage": ...,
"timings": {...}, "stop_type": ...} | {"error": "..."}.  Chat reasoning
deltas arrive as {"reasoning": "..."}.
"""

import asyncio
import hmac
import json
import os
import sys

import httpx
import websockets

RAW_ALLOW = {
    "n_predict", "temperature", "seed", "n_probs", "stop", "top_k", "top_p",
    "min_p", "presence_penalty", "frequency_penalty", "repeat_penalty",
    "logit_bias", "grammar",
}
CHAT_ALLOW = {
    "max_tokens", "temperature", "seed", "stop", "top_k", "top_p", "min_p",
    "presence_penalty", "frequency_penalty", "repeat_penalty", "logprobs",
    "top_logprobs", "chat_template_kwargs", "logit_bias", "grammar", "model",
}
TOP_ALLOW = {"mode", "key", "backend", "model", "prompt", "messages",
             "params", "key_env"}
FIXED = {"stream": True, "cache_prompt": False}


def _parse_args(argv):
    opts = {"port": 18431, "host": "127.0.0.1", "backends": {}}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--port":
            opts["port"] = int(argv[i + 1]); i += 2
        elif a == "--backend":
            name, url = argv[i + 1].split("=", 1)
            opts["backends"][name] = url.rstrip("/"); i += 2
        else:
            raise SystemExit("unknown flag: %s" % a)
    return opts


def _body(mode, frame, params):
    if mode == "raw":
        if "prompt" not in frame or not isinstance(frame["prompt"], str):
            raise ValueError("raw mode needs a string prompt")
        return {"prompt": frame["prompt"], **FIXED, **params}
    msgs = frame.get("messages")
    if not isinstance(msgs, list) or not msgs:
        raise ValueError("chat mode needs a non-empty messages list")
    return {"messages": msgs, **FIXED, **params}


def _endpoint(mode, base):
    return base + ("/completion" if mode == "raw" else "/v1/chat/completions")


def _events(mode, payload):
    """Yield (token, reasoning, extra) from one parsed SSE payload."""
    if mode == "raw":
        yield payload.get("content") or "", None, {
            "logprobs": payload.get("completion_probabilities"),
            "stop": bool(payload.get("stop")),
            "stop_type": payload.get("stop_type"),
        }
        return
    choices = payload.get("choices") or []
    if not choices:
        yield "", None, {"logprobs": None, "stop": False, "stop_type": None}
        return
    ch = choices[0]
    delta = ch.get("delta") or {}
    yield delta.get("content") or "", delta.get("reasoning_content"), {
        "logprobs": ch.get("logprobs"),
        "stop": ch.get("finish_reason") is not None,
        "stop_type": ch.get("finish_reason"),
    }


async def _error(ws, msg, code=1008):
    try:
        await ws.send(json.dumps({"error": msg}))
    except websockets.ConnectionClosed:
        pass
    await ws.close(code, msg[:120])


def _auth_key(ws, frame):
    if isinstance(frame.get("key"), str):
        return frame["key"]
    # websockets 15 asyncio serve() hands the handler a ServerConnection
    # whose handshake Request is at ws.request (set in process_event before
    # the handler runs). The older sync implementation exposed
    # ws.request_headers; on this stack ws.request.headers is the live path.
    request = getattr(ws, "request", None)
    headers = getattr(request, "headers", None)
    if headers:
        auth = headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            return auth[7:]
    return None


async def handler(ws, opts, expected_key):
    try:
        raw = await ws.recv()
    except websockets.ConnectionClosed:
        return
    try:
        frame = json.loads(raw)
        if not isinstance(frame, dict):
            raise ValueError
    except Exception:
        await _error(ws, "bad_frame")
        return

    got = _auth_key(ws, frame)
    if not expected_key or got is None or not hmac.compare_digest(got, expected_key):
        await _error(ws, "bad_key")
        return

    mode = frame.get("mode")
    if mode not in ("raw", "chat"):
        await _error(ws, "bad_mode")
        return
    unknown = sorted(set(frame) - TOP_ALLOW)
    if unknown:
        await _error(ws, "unknown key(s): " + ", ".join(unknown))
        return
    params = frame.get("params") or {}
    if not isinstance(params, dict):
        await _error(ws, "params must be an object")
        return
    allow = RAW_ALLOW if mode == "raw" else CHAT_ALLOW
    bad = sorted(set(params) - allow)
    if bad:
        await _error(ws, "param not allowlisted: " + ", ".join(bad))
        return

    base = opts["backends"].get(frame.get("backend") or "cpu")
    if base is None:
        await _error(ws, "unknown backend: %r" % frame.get("backend"))
        return
    try:
        body = _body(mode, frame, params)
    except ValueError as exc:
        await _error(ws, str(exc))
        return

    # The same static key authenticates the caller and the backend, unless
    # the frame names an env var holding the backend's key (read at call
    # time, never stored) -- the one field the cloud backend needs.
    backend_key = got
    if isinstance(frame.get("key_env"), str):
        backend_key = os.environ.get(frame["key_env"], "")
    headers = {"Authorization": "Bearer " + backend_key} if backend_key else {}

    usage = None
    timings = None
    stop_type = None
    sent_tokens = 0
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", _endpoint(mode, base), json=body,
                                     headers=headers) as resp:
                if resp.status_code != 200:
                    text = (await resp.aread()).decode("utf-8", "replace")[:400]
                    await _error(ws, "backend %d: %s" % (resp.status_code, text), 1011)
                    return
                async for line in resp.aiter_lines():
                    if not line.startswith("data:"):
                        continue
                    data = line[5:].strip()
                    if not data or data == "[DONE]":
                        continue
                    try:
                        payload = json.loads(data)
                    except ValueError:
                        continue
                    usage = payload.get("usage", usage)
                    timings = payload.get("timings", timings)
                    for token, reasoning, extra in _events(mode, payload):
                        if extra["stop"]:
                            stop_type = extra["stop_type"] or "eos"
                        if reasoning:
                            await ws.send(json.dumps({"reasoning": reasoning}))
                        if token:
                            out = {"token": token}
                            if extra["logprobs"] is not None:
                                out["logprobs"] = extra["logprobs"]
                            await ws.send(json.dumps(out))
                            sent_tokens += 1
                    if payload.get("stop"):
                        await ws.send(json.dumps({
                            "token": "", "done": True, "usage": usage,
                            "timings": timings, "stop_type": stop_type,
                            "tokens": sent_tokens,
                        }))
                        return
    except websockets.ConnectionClosed:
        # caller went away: the httpx context exits here and the backend
        # socket closes with it. Cancel is explicit, not implicit queuing.
        return
    except httpx.HTTPError as exc:
        await _error(ws, "backend transport: %s" % exc, 1011)
        return

    await ws.send(json.dumps({
        "token": "", "done": True, "usage": usage, "timings": timings,
        "stop_type": stop_type, "tokens": sent_tokens,
    }))


async def main(argv):
    opts = _parse_args(argv)
    expected_key = os.environ.get("WS_RAW_KEY")
    if not expected_key:
        raise SystemExit("WS_RAW_KEY must be set (the static key)")
    if not opts["backends"]:
        opts["backends"]["cpu"] = "http://127.0.0.1:18430"

    async def _h(ws):
        return await handler(ws, opts, expected_key)

    async with websockets.serve(
        _h, opts["host"], opts["port"], max_size=8 * 1024 * 1024
    ):
        print("ws_raw listening on ws://%s:%d/v1/stream backends=%s"
              % (opts["host"], opts["port"], opts["backends"]), flush=True)
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
