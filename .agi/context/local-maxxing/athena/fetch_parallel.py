#!/usr/bin/env python3
"""Parallel byte-range fetch for the athena A/B models (TM.20 Kid B).
Beats a bursty egress throttle with MANY independent curl -r segments per file.
Segments are absolute-offset files, resumable: a finished segment persists and
is skipped on restart; an unfinished one is re-fetched whole via -C - inside its
range. Reassemble with `cat seg_* > final` in order. Holds exact sizes + the
OFFICIAL sha256 from the HF API per file (curl writes lfs oid + size).
Run: python3 fetch_parallel.py start | status | reassemble <model>
"""
import subprocess, sys, os, json, time, shutil, urllib.request, urllib.parse
from datetime import datetime
from zoneinfo import ZoneInfo

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

# TM.33 schedule (owner 2026-09-18 03:2xZ): the aggregate cap is a time-of-day
# schedule on America/New_York wall clock -- 1.5 MB/s inside [02:00, 06:00),
# else 0.5 MB/s. zoneinfo zone NAME, never a fixed UTC offset, so DST is right.
# per-curl rate = aggregate // total segments (~40 run concurrently). A set
# FETCH_LIMIT_RATE is a manual per-curl override / rollback and wins.
DEFAULT_AGG = 0.5 * 1_000_000
PEAK_AGG = 1.5 * 1_000_000
PEAK_START, PEAK_END = 2, 6
NY = ZoneInfo("America/New_York")
PAUSE_FILE = os.path.join(WORK, "fetch.pause")
CURL_RATE = os.environ.get("FETCH_LIMIT_RATE")

def aggregate_limit(now=None):
    """Aggregate bytes/s allowed right now; `now` (aware) is for tests."""
    t = (now or datetime.now(NY)).astimezone(NY)
    return PEAK_AGG if PEAK_START <= t.hour < PEAK_END else DEFAULT_AGG

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

def seg_size(name, i):
    f = FILES[name]
    n = segs_of(name)
    sz = final_size_of(name)
    q, r = divmod(sz, n)
    if i < r: return q + 1
    return q

def final_size_of(name): return FILES[name].get("size")

def total_segments():
    return sum(segs_of(n) for n in FILES)

def per_segment_rate(now=None):
    return int(max(1, aggregate_limit(now) // max(1, total_segments())))

def seg_lo(name, i):
    return sum(seg_size(name, j) for j in range(i))

def commit_rem(sp, rem, start, end):
    """Append a .rem range to its segment, then drop it. A short .rem is a valid
    contiguous prefix (curl -f writes no body on HTTP errors), so appending it is
    byte-exact and nothing downloaded is ever discarded. sp only grows."""
    n = min(_have(rem), end - start + 1)
    if n > 0 and os.path.exists(rem):
        with open(rem, "rb") as s, open(sp, "ab") as d:
            while n > 0:
                b = s.read(min(n, 1 << 20))
                if not b: break
                d.write(b); n -= len(b)
    if os.path.exists(rem):
        os.remove(rem)
    return 0

def resume_range(lo, hi, have):
    """Byte-exact resume: (start,end) still to fetch, or None if [lo,hi] complete."""
    if have >= hi - lo + 1:
        return None
    return (lo + max(0, have), hi)

def _have(sp):
    return os.path.getsize(sp) if os.path.exists(sp) else 0

def _totals():
    have = tot = 0
    for name in FILES:
        for i in range(segs_of(name)):
            sp = segpath(name, i)
            have += _have(sp) + _have(sp + ".rem"); tot += seg_size(name, i)
    return have, tot

def supervise(poll=15, progress=60.0):
    """Restart dead segment curls (remaining bytes -> .rem, appended on success);
    one progress line per `progress` s to fetch.log. Never deletes segment bytes."""
    handles, last, prev = {}, 0.0, _totals()[0]
    rate0 = int(CURL_RATE) if CURL_RATE else per_segment_rate()
    print("supervise: cap=%.2f MB/s per_curl=%d B/s segments=%d tz=America/New_York" % (
        rate0 * total_segments() / 1e6, rate0, total_segments()), flush=True)
    rate = None
    while True:
        paused = os.path.exists(PAUSE_FILE)
        want = int(CURL_RATE) if CURL_RATE else per_segment_rate()
        if paused or want != rate:
            for p, rem, s, e in list(handles.values()):
                p.terminate()
            if not paused and rate is not None:
                print("rate %d -> %d B/s/curl (agg %.2f MB/s)" % (
                    rate, want, aggregate_limit() / 1e6), flush=True)
            rate = want
        for name in FILES:
            url = resolve_url(FILES[name]["repo"], FILES[name]["file"])
            for i in range(segs_of(name)):
                sp = segpath(name, i); want_sz = seg_size(name, i)
                h = handles.get((name, i))
                if h:
                    p, rem, s, e = h
                    if p.poll() is None:
                        continue
                    commit_rem(sp, rem, s, e); handles.pop((name, i))
                elif os.path.exists(sp + ".rem"):
                    # orphan .rem from a supervisor restart: bytes are a valid prefix
                    commit_rem(sp, sp + ".rem", seg_lo(name, i) + _have(sp),
                               seg_lo(name, i) + want_sz - 1)
                if paused:
                    continue
                r = resume_range(seg_lo(name, i), seg_lo(name, i) + want_sz - 1, _have(sp))
                if r is None:
                    continue
                rem = sp + ".rem"
                if os.path.exists(rem):
                    os.remove(rem)
                logf = open(sp + ".log", "ab")
                handles[(name, i)] = (subprocess.Popen(
                    ["curl", "-fsL", "--limit-rate", str(rate), "--range", f"{r[0]}-{r[1]}", "-o", rem, url],
                    stdout=logf, stderr=subprocess.STDOUT, start_new_session=True),
                    rem, r[0], r[1])
        now = time.time()
        if now - last >= progress:
            have, tot = _totals()
            rate = (have - prev) / max(1.0, now - last) / 1e6
            eta = (tot - have) / (rate * 1e6) / 3600 if rate > 0 else float("inf")
            line = "%s have=%d/%d (%.1f%%) %.2f MB/s eta=%.1fh" % (
                time.strftime("%H:%M:%S", time.gmtime()), have, tot,
                100.0 * have / tot, rate, eta)
            print(line, flush=True)
            with open(os.path.join(WORK, "fetch.log"), "a") as fl:
                fl.write(line + "\n")
            last, prev = now, have
        if _totals()[0] >= _totals()[1]:
            print("supervise: all segments complete", flush=True); return
        time.sleep(poll)

def _athena_bytes():
    return sum(_have(segpath(n, i)) + _have(segpath(n, i) + ".rem")
               for n in FILES for i in range(segs_of(n)))

def _egress_bytes():
    try:
        iface = subprocess.run(["ip", "route", "get", "1.1.1.1"], capture_output=True,
                               text=True).stdout.split()[4]
        for line in open("/proc/net/dev"):
            if line.split(":")[0].strip() == iface:
                return int(line.split(":")[1].split()[8])
    except Exception:
        return None
    return None

def cmd_pause(window=60, noise=1 << 16, poll=5.0):
    """Issue the pause (sentinel the supervisor honours), then measure athena's
    own segment-byte growth for `window` s. PASS iff it grew <= noise bytes
    (floor 64 KiB over the window, ~1 KiB/s). The interface total is printed
    for context only: a second fetch (bonsai) shares the box, so the
    athena-attributable number is the one this command certifies."""
    open(PAUSE_FILE, "w").close()
    print("pause: sentinel written; waiting for athena segments to quiesce", flush=True)
    prev = _athena_bytes()
    for _ in range(12):
        time.sleep(poll)
        cur = _athena_bytes()
        if cur == prev:
            break
        prev = cur
    a0, t0, e0 = _athena_bytes(), time.time(), _egress_bytes()
    time.sleep(window)
    dt = time.time() - t0
    grew, e1 = _athena_bytes() - a0, _egress_bytes()
    print("pause: athena egress %.0fs = %d B (%.0f B/s)" % (dt, grew, grew / dt), flush=True)
    if e0 is not None and e1 is not None:
        print("pause: interface egress = %.0f B/s" % ((e1 - e0) / dt), flush=True)
    ok = grew <= noise
    print("pause: %s (noise floor %d B over %.0fs)" % ("PASS" if ok else "FAIL", noise, dt), flush=True)
    return 0 if ok else 1

def cmd_resume():
    if os.path.exists(PAUSE_FILE):
        os.remove(PAUSE_FILE)
    print("resume: sentinel removed; run `python3 fetch_parallel.py supervise` if not running", flush=True)
    return 0

def status():
    print("effective cap=%.2f MB/s per_curl=%d tz=America/New_York" % (
        (int(CURL_RATE) * total_segments() / 1e6) if CURL_RATE else aggregate_limit() / 1e6,
        int(CURL_RATE) if CURL_RATE else per_segment_rate()), flush=True)
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
        json.dump({k: {"size": v["size"], "segs": v["segs"], "final": v["final"],
                       "sha256": v.get("sha256")} for k, v in FILES.items()},
                  open(META, "w"))
        print("meta -> " + META, flush=True)
        supervise()
    elif cmd == "supervise":
        load_meta(); supervise()
    elif cmd == "status":
        load_meta(); status()
    elif cmd == "reassemble":
        load_meta(); reassemble(sys.argv[2])
    elif cmd == "pause":
        load_meta(); sys.exit(cmd_pause(*map(int, sys.argv[2:4])))
    elif cmd == "resume":
        load_meta(); sys.exit(cmd_resume())
    else:
        print("usage: start|supervise|status|reassemble <model>|pause [window] [noise]|resume")