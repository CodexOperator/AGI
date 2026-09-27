#!/usr/bin/env python3
"""ws_raw_client.py -- client + measurement harness for ws_raw.py.

Two jobs, one file:
  1. stream one request and print the pieces and the timings row;
  2. `--measure N` runs N interleaved direct/adapter pairs per mode at
     matched load average and writes a JSONL row per leg:
     {mode, pair, leg, ttft_ms, tokens, tok_s, sha256, loadavg, mem_available}.

Direct and adapter legs send byte-identical bodies (temperature 0, seed 7,
cache_prompt false) so the sha256 of the concatenated content is comparable.

Usage:
    WS_RAW_KEY=secret python3 ws_raw_client.py --mode raw --prompt "hi"
    WS_RAW_KEY=secret python3 ws_raw_client.py --measure 10 --out rows.jsonl
"""

import argparse
import asyncio
import hashlib
import json
import os
import sys

import httpx
import websockets


def loadavg():
    one, five, fifteen = os.getloadavg()
    return {"l1": round(one, 2), "l5": round(five, 2), "l15": round(fifteen, 2)}


def mem_available_kb():
    try:
        with open("/proc/meminfo") as fh:
            for line in fh:
                if line.startswith("MemAvailable:"):
                    return int(line.split()[1])
    except OSError:
        pass
    return None


def params_for(mode, tokens):
    if mode == "raw":
        return {"temperature": 0, "seed": 7, "n_predict": tokens}
    return {"temperature": 0, "seed": 7, "max_tokens": tokens}


async def direct_stream(base, mode, body, key=None):
    """Return (text, ttft_ms, n_tokens, elapsed_ms)."""
    url = base + ("/completion" if mode == "raw" else "/v1/chat/completions")
    headers = {"Authorization": "Bearer " + key} if key else {}
    text, first, t0 = [], None, None
    loop = asyncio.get_event_loop()
    t0 = loop.time()
    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("POST", url, json=body, headers=headers) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if not line.startswith("data:"):
                    continue
                data = line[5:].strip()
                if not data or data == "[DONE]":
                    continue
                payload = json.loads(data)
                if mode == "raw":
                    piece = payload.get("content") or ""
                else:
                    choices = payload.get("choices") or [{}]
                    piece = (choices[0].get("delta") or {}).get("content") or ""
                if piece:
                    if first is None:
                        first = loop.time()
                    text.append(piece)
    end = loop.time()
    ttft = None if first is None else (first - t0) * 1000.0
    return "".join(text), ttft, len(text), (end - t0) * 1000.0


async def adapter_stream(url, mode, key, backend, prompt_or_messages, params):
    frame = {"mode": mode, "backend": backend, "key": key, "params": params}
    if mode == "raw":
        frame["prompt"] = prompt_or_messages
    else:
        frame["messages"] = prompt_or_messages
    text, first = [], None
    loop = asyncio.get_event_loop()
    t0 = loop.time()
    async with websockets.connect(url, max_size=8 * 1024 * 1024) as ws:
        await ws.send(json.dumps(frame))
        async for raw in ws:
            msg = json.loads(raw)
            if "error" in msg:
                raise RuntimeError(msg["error"])
            if msg.get("reasoning"):
                continue
            piece = msg.get("token") or ""
            if piece:
                if first is None:
                    first = loop.time()
                text.append(piece)
            if msg.get("done"):
                break
    end = loop.time()
    ttft = None if first is None else (first - t0) * 1000.0
    return "".join(text), ttft, len(text), (end - t0) * 1000.0


async def measure(args):
    rows = []
    for mode in ("raw", "chat"):
        params = params_for(mode, args.tokens)
        for pair in range(1, args.pairs + 1):
            for leg in ("direct", "adapter"):
                if leg == "direct":
                    if mode == "raw":
                        body = {"prompt": args.prompt, "stream": True,
                                "cache_prompt": False, **params}
                    else:
                        body = {"messages": [{"role": "user", "content": args.prompt}],
                                "stream": True, "cache_prompt": False, **params}
                    out = await direct_stream(args.backend_url, mode, body, args.key)
                else:
                    payload = args.prompt if mode == "raw" else [
                        {"role": "user", "content": args.prompt}]
                    out = await adapter_stream(
                        args.url, mode, args.key, args.backend_name, payload, params)
                text, ttft, ntokens, elapsed = out
                row = {
                    "mode": mode, "pair": pair, "leg": leg,
                    "ttft_ms": None if ttft is None else round(ttft, 2),
                    "tokens": ntokens,
                    "tok_s": None if not elapsed else round(ntokens / (elapsed / 1000.0), 3),
                    "sha256": hashlib.sha256(text.encode()).hexdigest()[:16],
                    "text": text,
                    "loadavg": loadavg(),
                    "mem_avail_kb": mem_available_kb(),
                }
                rows.append(row)
                if args.out:
                    with open(args.out, "a") as fh:
                        fh.write(json.dumps(row) + "\n")
                print(json.dumps({k: v for k, v in row.items() if k != "text"}),
                      flush=True)
    return rows


def report(rows):
    """Median TTFT overhead and tok/s ratio per mode, plus sha summary."""
    from statistics import median
    ok = True
    for mode in ("raw", "chat"):
        pairs = {}
        for r in rows:
            if r["mode"] == mode:
                pairs.setdefault(r["pair"], {})[r["leg"]] = r
        deltas, ratios, shas = [], [], {"direct": set(), "adapter": set()}
        for pair in sorted(pairs):
            d, a = pairs[pair].get("direct"), pairs[pair].get("adapter")
            if not (d and a) or d["ttft_ms"] is None or a["ttft_ms"] is None:
                continue
            deltas.append(a["ttft_ms"] - d["ttft_ms"])
            if d["tok_s"]:
                ratios.append(a["tok_s"] / d["tok_s"])
            shas["direct"].add(d["sha256"])
            shas["adapter"].add(a["sha256"])
        md = median(deltas) if deltas else None
        mr = median(ratios) if ratios else None
        same = shas["direct"] == shas["adapter"]
        print("[%s] pairs=%d median_ttft_delta_ms=%s median_tok_s_ratio=%s "
              "sha_sets_equal=%s" % (mode, len(deltas),
                                     None if md is None else round(md, 1),
                                     None if mr is None else round(mr, 3), same))
        if md is None or md > 50 or mr is None or mr < 0.9 or not same:
            ok = False
    return ok


async def stream_once(args):
    if args.mode == "raw":
        body = {"prompt": args.prompt, "stream": True, "cache_prompt": False,
                **params_for("raw", args.tokens)}
        text, ttft, n, el = await direct_stream(args.backend_url, "raw", body, args.key)
    else:
        body = {"messages": [{"role": "user", "content": args.prompt}],
                "stream": True, "cache_prompt": False, **params_for("chat", args.tokens)}
        text, ttft, n, el = await direct_stream(args.backend_url, "chat", body, args.key)
    print(json.dumps({"leg": "direct", "ttft_ms": ttft, "tokens": n, "text": text}))
    payload = args.prompt if args.mode == "raw" else [{"role": "user", "content": args.prompt}]
    text, ttft, n, el = await adapter_stream(
        args.url, args.mode, args.key, args.backend_name, payload,
        params_for(args.mode, args.tokens))
    print(json.dumps({"leg": "adapter", "ttft_ms": ttft, "tokens": n, "text": text}))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="ws://127.0.0.1:18431/v1/stream")
    ap.add_argument("--backend-url", default="http://127.0.0.1:18430")
    ap.add_argument("--backend-name", default="cpu")
    ap.add_argument("--key", default=os.environ.get("WS_RAW_KEY", ""))
    ap.add_argument("--mode", default="raw", choices=["raw", "chat"])
    ap.add_argument("--prompt", default="Count from one to twenty.")
    ap.add_argument("--tokens", type=int, default=32)
    ap.add_argument("--measure", dest="pairs", type=int, default=0)
    ap.add_argument("--out")
    args = ap.parse_args()

    if args.pairs:
        rows = asyncio.run(measure(args))
        ok = report(rows)
        sys.exit(0 if ok else 1)
    asyncio.run(stream_once(args))


if __name__ == "__main__":
    main()
