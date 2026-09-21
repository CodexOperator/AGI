#!/usr/bin/env python3
"""TEL.01 probe: can a KV span be re-injected at a SHIFTED position on the resident 9B?

Read-only. Stdlib only. Writes kv-surface-<utc>.json next to itself.
Usage: probe_kv_surface.py           # surface probe (routes + slot actions)
       probe_kv_surface.py --cache   # + 3-request cache_prompt shift probe
"""
import datetime, json, pathlib, sys, urllib.error, urllib.request
BASE, MODEL = "http://127.0.0.1:8080", "Qwen3.5-9B-Q4_K_M"
HERE = pathlib.Path(__file__).resolve().parent
ACTIONS = ["save", "restore", "erase", "shift", "seq_add", "seq_rm", "seq_cp",
           "truncate", "keep"]
ROUTES = ["/kv", "/seq", "/sequence", "/cache", "/kv-cache", "/apply-template"]


def req(method, path, body=None, timeout=180):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(BASE + path, data=data, method=method,
                               headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r, timeout=timeout) as f:
            return f.status, f.read(20000).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read(20000).decode("utf-8", "replace")
    except Exception as e:              # refused / timeout / bad json
        return -1, repr(e)


def words(tag, n):
    return " ".join(f"{tag}{i}" for i in range(n))


def cache_probe():
    """3 completions: does cache_prompt reuse S at a SHIFTED position?"""
    A, S, B, X = words("alpha", 80), words("sigma", 150), words("omega", 20), words("xi", 80)
    out = []
    for label, prompt in (("r1_A_S_B", A + " " + S + " " + B),
                          ("r2_A_S_B_repeat", A + " " + S + " " + B),
                          ("r3_X_S_B_shifted", X + " " + S + " " + B)):
        st, body = req("POST", "/completion", {"model": MODEL, "prompt": prompt,
                                               "temperature": 0, "n_predict": 1,
                                               "cache_prompt": True})
        try:
            t = json.loads(body).get("timings", {})
            out.append({"req": label, "status": st, "cache_n": t.get("cache_n"),
                        "prompt_n": t.get("prompt_n"), "prompt_ms": t.get("prompt_ms"),
                        "prompt_per_second": t.get("prompt_per_second")})
        except Exception:
            out.append({"req": label, "status": st, "body": body[:600]})
    return out

def main():
    rec = {"utc": datetime.datetime.utcnow().isoformat() + "Z", "base": BASE,
           "model": MODEL}
    rec["v1_models"] = dict(zip(("status", "body"), req("GET", "/v1/models")))
    rec["slots"] = dict(zip(("status", "body"), req("GET", f"/slots?model={MODEL}")))
    rec["slot_actions"] = {a: dict(zip(("status", "body"),
                                       req("POST", f"/slots/0?action={a}", {"model": MODEL})))
                           for a in ACTIONS}
    rec["routes"] = {r: req("GET", r)[0] for r in ROUTES}
    if "--cache" in sys.argv:
        rec["cache_probe"] = cache_probe()
    p = HERE / f"kv-surface-{datetime.datetime.utcnow():%Y%m%dT%H%M%SZ}.json"
    p.write_text(json.dumps(rec, indent=2))
    print(p)
    print(json.dumps(rec["slot_actions"], indent=2)[:2000])
    if rec.get("cache_probe"):
        print(json.dumps(rec["cache_probe"], indent=2))

if __name__ == "__main__":
    main()