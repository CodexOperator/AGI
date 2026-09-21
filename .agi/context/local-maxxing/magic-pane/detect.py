#!/usr/bin/env python3
"""Magic-pane chunk 1: zero-shot form detection from the first N prose tokens. Prose = thinking_delta+text_delta emitted before toolcall_start; label read ONLY from toolcall_end args. Drop <40 whitespace tokens of pre-form prose. Sources: every recorded pi output.log (not this round's live one) + .agi/comms/season-2 blocks. Token unit = \\S+ run. Two prompt conditions: `fixed` (label list in LAB order) and `shuffled` (per-segment deterministic shuffle, which removes the model's first-label position bias)."""
import json, glob, re, os, time, random, urllib.request, collections, statistics
LAB = ["write_note", "write_set", "dm", "merge_up", "dispatch", "bench_jsonl", "node_write"]
DEF = {"write_note": "write.py <node> 'note ...'", "write_set": "write.py <node> 'set <field> ...'", "dm": "send a direct message (send.py)",
       "merge_up": "emit a [merge-up] line", "dispatch": "spawn a kid (dispatch.py) or close a round (cli.py done)",
       "bench_jsonl": "write a bench .jsonl row", "node_write": "create or edit a node under .agi/nodes/"}
OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../datasets/magic-pane"))
PI = ["/data/work/agi/.agi/worktrees/*/.agi/sessions/iter-*/*/output.log", "/data/work/agi/.agi/sessions/iter-*/*/output.log"]
RULES = [("write_note", r"write\.py\s+\S+\s+'?\"?note\b"), ("write_set", r"write\.py\s+\S+\s+'?\"?set\b"), ("dm", r"\bsend\.py\s+(?:send|dm)\b"),
         ("merge_up", r"\[merge-up\]"), ("dispatch", r"\bdispatch\.py\b|cli\.py\s+done\b"), ("bench_jsonl", r"\.jsonl"), ("node_write", r"\.agi/nodes/\S+\.md")]

def tok(s): return re.findall(r"\S+", s)
def label_of(name, args):
    a = args or {}; s = (a.get("command") or "") + " " + str(a.get("path") or "")
    for lab, rx in RULES:
        if re.search(rx, s): return lab
    return "node_write" if name in ("edit", "write", "create") and "/nodes/" in str(a.get("path")) else None
def extract():
    segs, dropped = [], 0
    for path in sorted(sum((glob.glob(p) for p in PI), [])):
        if "a00-aecd4776" in path: continue
        sess, buf, pend, k = path.split("/sessions/")[-1][:-11], "", {}, 0
        for line in open(path, encoding="utf-8", errors="replace"):
            if '"message_update"' not in line: continue
            try: ev = json.loads(line).get("assistantMessageEvent") or {}
            except ValueError: continue
            t, ci = ev.get("type"), ev.get("contentIndex")
            if t in ("thinking_delta", "text_delta"): buf += ev.get("delta") or ""
            elif t == "toolcall_start": pend[ci] = buf; buf = ""
            elif t == "toolcall_end":
                prose = pend.pop(ci, ""); tc = ev.get("toolCall") or {}
                lab = label_of(tc.get("name"), tc.get("arguments"))
                if not lab: continue
                if len(tok(prose)) < 40: dropped += 1; continue
                a = tc.get("arguments") or {}; k += 1
                segs.append({"id": f"pi-{sess}-{k}", "source": "pi", "session": sess.rstrip("/"), "label": lab,
                             "prose": prose, "form": (a.get("command") or a.get("path") or json.dumps(a))[:300]})
    for path in sorted(glob.glob("/data/work/agi/.agi/comms/season-2/*/*.md")):
        txt = open(path, encoding="utf-8", errors="replace").read()
        for i, m in enumerate(re.finditer(r"^---\n(.*?)\n\n(.*?)(?=\n---\n|\Z)", txt, re.S)):
            body = m.group(2).strip()
            if not body or len(tok(body)) < 40: dropped += 1; continue
            segs.append({"id": f"comms-{os.path.basename(path)}-{i}", "source": "comms", "session": "comms/" + os.path.basename(path),
                         "label": "merge_up" if "[merge-up]" in body.split("\n", 1)[0] else "dm", "prose": body,
                         "form": body.split("\n", 1)[0][:120]})
    return segs, dropped
def call(order, prose, n):
    sysmsg = "Classify which structured form an agent is about to emit from only the first part of its streamed prose. Answer with exactly ONE lowercase label. Labels: " + "; ".join(f"{l}={DEF[l]}" for l in order)
    body = json.dumps({"model": "Qwen3.5-9B-Q4_K_M", "temperature": 0, "max_tokens": 8, "chat_template_kwargs": {"enable_thinking": False},
                       "messages": [{"role": "system", "content": sysmsg}, {"role": "user", "content": " ".join(tok(prose)[:n])}]}).encode()
    req = urllib.request.Request("http://127.0.0.1:8080/v1/chat/completions", data=body, headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=180) as f: low = json.load(f)["choices"][0]["message"]["content"].strip().lower()
    return next((l for l in order if l in low), "UNPARSED"), time.time() - t0
def main():
    segs, dropped = extract(); os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "segments.jsonl"), "w").writelines(json.dumps(s) + "\n" for s in segs)
    reports, plines = [], []
    for cond, shuf in (("fixed", 0), ("shuffled", 1)):
        rnd = random.Random(20260921)
        for n in (40, 80):
            preds = []
            for s in segs:
                order = LAB[:]
                if shuf: rnd.shuffle(order)
                p, dt = call(order, s["prose"], n); preds.append((s, p, dt))
                plines.append(json.dumps({"id": s["id"], "condition": cond, "N": n, "gold": s["label"], "pred": p, "latency_s": round(dt, 3), "source": s["source"]}))
            gold = collections.Counter(s["label"] for s in segs); lat = sorted(t for _, _, t in preds)
            by = lambda src: round(sum(s["label"] == p for s, p, _ in preds if s["source"] == src) / max(1, sum(1 for s, _, _ in preds if s["source"] == src)), 4)
            rep = {"condition": cond, "N": n, "n_segments": len(segs), "dropped_short_prose": dropped, "top1_accuracy": round(sum(s["label"] == p for s, p, _ in preds) / len(preds), 4),
                   "majority_baseline": round(max(gold.values()) / len(segs), 4), "median_latency_s": round(statistics.median(lat), 3),
                   "p95_latency_s": round(lat[int(0.95 * len(lat)) - 1], 3), "label_histogram": dict(gold.most_common()), "per_source_accuracy": {"pi": by("pi"), "comms": by("comms")},
                   "confusion": {f"{g}->{p}": c for (g, p), c in collections.Counter((s["label"], p) for s, p, _ in preds).most_common()}}
            reports.append(rep); print(json.dumps({k: rep[k] for k in ("condition", "N", "n_segments", "top1_accuracy", "majority_baseline", "median_latency_s", "p95_latency_s")}))
    open(os.path.join(OUT, "predictions.jsonl"), "w").write("\n".join(plines) + "\n")
    json.dump(reports, open(os.path.join(OUT, "metrics.json"), "w"), indent=1)
if __name__ == "__main__": main()
