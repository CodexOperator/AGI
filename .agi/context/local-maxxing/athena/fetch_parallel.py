#!/usr/bin/env python3
"""Parallel byte-range fetch for the athena A/B models (TM.20 Kid B).
Beats a bursty egress throttle with MANY independent curl -r segments per file.
Segments are absolute-offset files, resumable: a finished segment persists and
is skipped on restart; an unfinished one is re-fetched whole via -C - inside its
range. Reassemble with `cat seg_* > final` in order. Holds exact sizes + the
OFFICIAL sha256 from the HF API per file (curl writes lfs oid + size).
Run: python3 fetch_parallel.py start | status | reassemble <model>
"""
import subprocess, sys, os, json, time, urllib.request, urllib.parse

WORK = "/data/ml/models"
FILES = {
  "athena": {
    "repo": "slashreboot/athena-class-model-a",
    "file": "Athena-Class-31B-Model-A-Q8_0.gguf",
    "final": "Athena-Class-31B-Model-A-Q8_0.gguf",
    "segs": 24,
  },
  "base": {
    "repo": "unsloth/gemma-4-31B-it-GGUF",
    "file": "gemma-4-31B-it-Q4_K_M.gguf",
    "final": "gemma-4-31B-it-Q4_K_M.gguf",
    "segs": 16,
  },
}
URLBASE = "https://huggingface.co/"

def api_meta(repo, file):
    # HF API tree returns an entry with lfs oid (sha256) and size per file.
    want = urllib.parse.quote(file)
    url = f"{URLBASE}api/models/{repo}/tree/main" + ("?recursive=true&expand=true")
    with urllib.request.urlopen(url, timeout=120) as r:
        data = json.loads(r.read())
    for it in data:
        if it.get("path") == file:
            sz = it["size"]
            if "lfs" in it:
                return it["lfs"]["oid"], it["lfs"]["size"]
            return None, sz
    return None, None

def resolve_url(repo, file):
    return f"{URLBASE}{repo}/resolve/main/{urllib.parse.quote(file)}"

def segs_of(name):
    f = FILES[name]
    return int(f["segs"])

def segpath(name, i):
    f = FILES[name]
    return os.path.join(WORK, f"{f['file']}.seg{i:03d}")

def run(cur):
    cmd = ["python3", os.path.abspath(__file__)] + cur
    for name in FILES:
        _, final_size = api_meta(FILES[name]["repo"], FILES[name]["file"])
        if not final_size:
            print(f"[ERR] no size for {name}", flush=True); continue
        FILES[name]["size"] = final_size
        print(f"[{name}] final_size={final_size}", flush=True)
    return 0

def start():
    procs = []
    for name, f in FILES.items():
        n = segs_of(name)
        base = n // segs_of(name) * 0  # noop
        seg = final_size_of(name) // n
        url = resolve_url(f["repo"], f["file"])
        for i in range(n):
            sp = segpath(name, i)
            if os.path.exists(sp) and os.path.getsize(sp) == seg_size(name, i):
                print(f"[{name}] seg{i:03d} done, skip", flush=True); continue
            # R3 fix: lo/hi derive from seg_size (divmod: first r segs one byte
            # longer) so ranges agree with seg_size/reassemble/status. Old
            # floor-range segs were one byte short -> sha256 false-fail.
            lo = sum(seg_size(name, j) for j in range(i))
            hi = lo + seg_size(name, i) - 1
            # stale partial seg -> wipe (range restart is cleaner than resume-in-range)
            if os.path.exists(sp):
                os.remove(sp)
            cmd = ["nohup", "curl", "-sL", "-C", "-", "--range", f"{lo}-{hi}",
                   "-o", sp, url]
            # -C - overrides --range start; keep both: -C - lets a mid-range resume,
            # --range binds the upper bound so a finished seg never overruns.
            p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL, start_new_session=True)
            procs.append((name, i, sp, lo, hi, p.pid))
            print(f"[{name}] seg{i:03d} pid={p.pid} [{lo}-{hi}]", flush=True)
            time.sleep(0.6)  # stagger so a burst is not all grabbed by one file's first segs
    print(f"Spawned {len(procs)} segment curls. Poll with 'status'.", flush=True)

def seg_size(name, i):
    f = FILES[name]
    n = segs_of(name)
    sz = final_size_of(name)
    q, r = divmod(sz, n)
    if i < r: return q + 1
    return q

def final_size_of(name): return FILES[name].get("size")

def status():
    for name, f in FILES.items():
        n = segs_of(name)
        done = 0; have = 0
        for i in range(n):
            sp = segpath(name, i)
            want = seg_size(name, i) if "size" in FILES[name] else None
            if os.path.exists(sp):
                sz = os.path.getsize(sp)
                have += sz
                if want and sz >= want: done += 1
        tot = final_size_of(name)
        print(f"[{name}] {have}/{tot} bytes ({100.0*have/tot:.1f}%), segs_done={done}/{n}", flush=True)
    return 0

def reassemble(name):
    f = FILES[name]
    n = segs_of(name)
    parts = [segpath(name, i) for i in range(n)]
    # verify all present + correct size
    for i, p in enumerate(parts):
        want = seg_size(name, i)
        if not os.path.exists(p) or os.path.getsize(p) < want:
            print(f"[{name}] seg{i:03d} MISSING/short ({os.path.exists(p)}, have {os.path.getsize(p) if os.path.exists(p) else 0}/{want})", flush=True)
            return 1
    out = os.path.join(WORK, f["final"])
    with open(out, "wb") as dest:
        for p in parts:
            with open(p, "rb") as src:
                dest.write(src.read())
    print(f"[{name}] reassembled -> {out} ({os.path.getsize(out)} bytes)", flush=True)
    return 0

META = os.path.join(WORK, "fetch_meta.json")

def load_meta():
    if os.path.exists(META):
        m = json.load(open(META))
        for k, v in m.items():
            FILES[k]["size"] = v["size"]
            FILES[k]["segs"] = v["segs"]
            FILES[k]["final"] = v["final"]
            FILES[k]["sha256"] = v.get("sha256")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "start"
    if cmd == "start":
        # resolve sizes first
        for name in FILES:
            oid, sz = api_meta(FILES[name]["repo"], FILES[name]["file"])
            FILES[name]["size"] = sz
            FILES[name]["sha256"] = oid
            print(f"[{name}] size={sz} sha256={oid}", flush=True)
        start()
        # persist meta for status/reassemble
        json.dump({k: {"size": v["size"], "segs": v["segs"], "final": v["final"],
                       "sha256": v.get("sha256")} for k, v in FILES.items()},
                  open(META, "w"))
        print("meta -> " + META, flush=True)
        print("reassemble with: python3 fetch_parallel.py reassemble <athena|base>", flush=True)
    elif cmd == "status":
        load_meta(); status()
    elif cmd == "reassemble":
        load_meta(); reassemble(sys.argv[2])
    else:
        print("usage: start|status|reassemble <model>")