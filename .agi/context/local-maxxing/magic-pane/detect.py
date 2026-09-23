#!/usr/bin/env python3
"""Magic-pane chunk 1 STRICT retest (census only). A segment counts only if its tool call PRODUCES a known form; a read or mention is never a form. Prose = thinking_delta+text_delta before toolcall_start; form read only from the paired toolcall_end. <40 whitespace (\\S+) prose units -> dropped, counted per class. Model measurement is deferred (corpus insufficient); the 78-line measured harness is recoverable from grid/git history."""
import json, glob, re, os, collections
LAB = ["write_note", "write_set", "dm", "merge_up", "dispatch", "bench_jsonl", "node_write"]
OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../datasets/magic-pane"))
# MAIN, not derived from __file__: this script (like spawn_budget.py) must anchor to the ONE
# tree that holds every worktree as a sibling under .agi/worktrees/*, not to whichever worktree
# happens to run it -- deriving from __file__ here would only scan the caller's own (usually
# empty) nested .agi/worktrees/, silently undercounting (mur-mp-01 residue: flagged, not solved,
# since a real fix needs a shared root resolver, not a per-script guess -- see bin/locations.py).
ROOT = "/data/work/agi"
PI = [f"{ROOT}/.agi/worktrees/*/.agi/sessions/iter-*/*/output.log", f"{ROOT}/.agi/sessions/iter-*/*/output.log"]
LIVE = {os.path.basename(p)[:-6] for p in glob.glob(f"{ROOT}/.agi/sessions/.spawn-budget/*.lease")}  # a leased agent's stream is not recorded -- NOT a reproducible census: which streams are still growing changes minute to minute (mur-mp-01: 39 -> 49 on a rerun 49min later); excluded_live_agents below names the exact set this run used
def tok(s): return re.findall(r"\S+", s)
def strict(name, args):
    a = args or {}; p = str(a.get("path") or ""); c = a.get("command") or ""
    if name in ("write", "edit", "create"): return "node_write" if "/nodes/" in p else ("bench_jsonl" if p.endswith(".jsonl") else None)
    if name != "bash": return None
    if re.search(r"bin/write\.py|python3\s+[^\n]*write\.py", c):
        v = re.search(r"write\.py\s+\S+\s+(.{0,300})", c, re.S)
        return None if not v else next((l for l, rx in (("write_note", r"\bnote\b"), ("node_write", r"\bcreate\b"), ("write_set", r"\bset\b")) if re.search(rx, v.group(1))), None)
    if re.search(r"send\.py\s+(send|dm)\b", c): return "dm"
    for m in re.finditer(r"dispatch\.py\s+([^\n|;&]*)", c):
        if "--help" not in m.group(1) and (re.search(r"[A-Z]+\.[0-9]+", m.group(1)) or "--detach" in m.group(1)): return "dispatch"
    if re.search(r">>\s*\S*\.jsonl|tee\s+[^\n|]*\.jsonl|open\([^)]*\.jsonl[^)]*[\"'](a|w)", c) or (".jsonl" in c and re.search(r"json\.dump\w*\(", c)): return "bench_jsonl"
    return None
def extract():
    segs, drop = [], collections.Counter()
    for path in sorted(sum((glob.glob(x) for x in PI), [])):
        if "iter-MP.01" in path or any("/%s/" % a in path for a in LIVE): continue
        buf, pend, k = "", {}, 0
        for line in open(path, encoding="utf-8", errors="replace"):
            if '"message_update"' not in line: continue
            try: ev = json.loads(line).get("assistantMessageEvent") or {}
            except ValueError: continue
            t, ci = ev.get("type"), ev.get("contentIndex")
            if t in ("thinking_delta", "text_delta"): buf += ev.get("delta") or ""
            elif t == "toolcall_start": pend[ci] = buf; buf = ""
            elif t == "toolcall_end":
                prose, tc = pend.pop(ci, ""), ev.get("toolCall") or {}
                lab = strict(tc.get("name"), tc.get("arguments"))
                if not lab: continue
                if len(tok(prose)) < 40: drop[lab] += 1; continue
                k += 1; segs.append({"id": f"pi-{path.split('/sessions/')[-1][:-11]}-{k}", "label": lab, "prose": prose, "form": (tc.get("arguments") or {}).get("command", "")[:200]})
    return segs, drop
def main():
    segs, drop = extract(); os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "segments.jsonl"), "w").writelines(json.dumps(s) + "\n" for s in segs)
    hist = collections.Counter(s["label"] for s in segs); n = len(segs)
    metrics = {"strict": True, "n_real_segments": n, "label_histogram": dict(hist.most_common()), "dropped_short_prose": dict(drop.most_common()), "dropped_total": sum(drop.values()),
               "missing_classes": [l for l in LAB if hist[l] == 0], "thin_classes": [l for l in LAB if 0 < hist[l] < 5], "majority_baseline": round(max(hist.values()) / n, 4) if n else None,
               "corpus_sufficient": n >= 200, "measurements": [], "measured": False,
               "excluded_live_agents": sorted(LIVE)}  # audit trail for the non-reproducible census (mur-mp-01 residue): exactly which streams this run treated as still-growing
    json.dump(metrics, open(os.path.join(OUT, "metrics_strict.json"), "w"), indent=1)
    print(json.dumps({k: metrics[k] for k in ("n_real_segments", "label_histogram", "dropped_total", "missing_classes", "corpus_sufficient")}))
if __name__ == "__main__": main()