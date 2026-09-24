#!/usr/bin/env python3
"""OSC.12 draft-free n-gram speculation on the served Qwen3.5-9B-Q4_K_M (router's image/args): build|t1|full|analyze|margins. Fresh container per arm, model_args_9b minus --port, host 0.0.0.0 (bridge net; host side is 127.0.0.1), -fa on, --spec-type <arm> at DEFAULT parameters. The CALLER stops and restores llama-server; this script never touches it. Repo paths via paths.get_local (rule 13); out-of-repo model and JIT roots resolve through paths.py proposed box cells."""
import ast, glob, json, math, os, re, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = HERE
while not os.path.isfile(ROOT + "/.agi/config.json"): ROOT = os.path.dirname(ROOT)
sys.path.insert(0, ROOT + "/.agi/context/local-maxxing"); import paths
IMG = "ghcr.io/ggml-org/llama.cpp:server-cuda"; MODELS = paths.get("served_models_dir"); CACHE = paths.get("cuda_jit_cache_dir")
MODEL = "/models/Qwen3.5-9B-Q4_K_M.gguf"; MNAME = "Qwen3.5-9B-Q4_K_M"
OUT = paths.get_local("specdec_out_dir"); LOG = OUT + "/logs"
ARMS = ["none", "ngram-simple", "ngram-map-k", "ngram-map-k4v", "ngram-mod", "ngram-cache", "none-LAST"]
BASE = ["--cache-reuse", "8", "--host", "0.0.0.0", "--jinja", "--alias", MNAME, "--fit", "on", "--model", MODEL, "--parallel", "1", "-fa", "on"]
T975 = 2.068658   # t_0.975, df=23 (24 paired requests)
NODES = ("04dc76fc-10e9a3 527993c5-67867c 86466b78-c8d14f e03d8dd2-02d831 3b543674-ac032a 297e744f-32087d "
         "4698c6f8-56f4c9 f256db1a-73ee5b 30ac1417-72aa81 df53894e-fabe8f 3caaf6eb-9065ef").split()
PIN = "fe31bddee875c5d9da0bb9f46840ab1b559ddacf"   # the round's base: prompts are built from the graph AS DISPATCHED, so later node / serve edits never move them (mur-15)
def _git(rel): return subprocess.run(["git", "-C", ROOT, "show", PIN + ":" + rel], capture_output=True, check=True).stdout.decode("utf-8", "replace")
def _read(rel, a, b): return "\n".join(_git(rel).splitlines()[a - 1:b])
def _funcs():
 o = []
 ls_tree = subprocess.run(["git", "-C", ROOT, "ls-tree", PIN, ".agi/context/local-maxxing/serve/"], capture_output=True, text=True, check=True).stdout
 for rel in sorted(l.split("\t")[1] for l in ls_tree.splitlines() if " blob " in l and l.endswith(".py")):
  src = _git(rel); ls = src.splitlines()
  o += [(rel, n.name, "\n".join(ls[n.lineno - 1:n.end_lineno])) for n in ast.parse(src).body if isinstance(n, ast.FunctionDef)]
 return o
def build_prompts():
 E = [("Below is a section of a committed experiment node. Apply this one-line change: append the line `<!-- reviewed -->` as the last line. Return the whole revised text, nothing else.\n\n" + _read(".agi/nodes/experiment/a00-%s.md" % n, 12, 70), 2048) for n in NODES[:8]]
 C = [("Write a pytest unit test for this committed function (names only, no fixtures needed). Return only the test code.\n\n" + s, 512) for _, _, s in _funcs()[:8]]
 D = [("Digest this committed experiment node in at most 8 lines, plain text.\n\n" + _read(".agi/nodes/experiment/a00-%s.md" % n, 1, 120), 384) for n in NODES[3:11]]
 return sorted([{"class": c, "id": "%s%d" % (c, i + 1), "max_tokens": m, "text": t} for c, g in (("E", E), ("C", C), ("D", D)) for i, (t, m) in enumerate(g)], key=lambda p: p["id"])
def prompts_jsonl(): return "".join(json.dumps(p, sort_keys=True, separators=(",", ":")) + "\n" for p in build_prompts())
def cargs(spec, port, nm=None):
 return (["docker", "run", "--rm", "-d", "--name", nm or "sd_" + spec, "--gpus", "all", "-v", MODELS + ":/models:ro",
          "-v", OUT + ":/out", "-v", CACHE + ":/root/.nv/ComputeCache", "-p", "127.0.0.1:%d:%d" % (port, port),
          "--entrypoint", "/app/llama-server", IMG] + BASE + ["--spec-type", "none" if spec.startswith("none") else spec,
          "--port", str(port), "-lv", "3", "--log-file", "/out/logs/%s.log" % (nm or "sd_" + spec)])
def rbody(text, mt, n_probs=0):
 b = {"model": MNAME, "messages": [{"role": "user", "content": text}], "max_tokens": mt, "temperature": 0, "chat_template_kwargs": {"enable_thinking": False}}
 return b | ({"n_probs": n_probs} if n_probs else {})
def post(port, text, key, mt=8, n_probs=0):
 p = OUT + "/req_%s.json" % key; json.dump(rbody(text, mt, n_probs), open(p, "w"))
 r = subprocess.run(["curl", "-s", "--max-time", "2400", "-X", "POST", "http://127.0.0.1:%d/v1/chat/completions" % port,
                     "-H", "Content-Type: application/json", "-d", "@" + p], capture_output=True, text=True)
 try: return json.loads(r.stdout)
 except Exception: return {"_parse_error": r.stdout[:400]}
def up(port, name, tmo=420):
 t0 = time.time()
 while time.time() - t0 < tmo:
  if subprocess.run(["curl", "-sf", "--max-time", "3", "http://127.0.0.1:%d/health" % port], capture_output=True).returncode == 0: return round(time.time() - t0, 1)
  if subprocess.run(["docker", "inspect", "-f", "{{.State.Running}}", name], capture_output=True, text=True).stdout.strip() != "true": return None
  time.sleep(2)
 return None
def mem(): return int(next(l.split()[1] for l in open("/proc/meminfo") if l.startswith("MemAvailable")))
def quiet(tmo=600, gap=60):   # OSC.11: a contended baseline produced a fake +27 pct; wait for a quiet box
 time.sleep(gap)
 t0 = time.time()
 while time.time() - t0 < tmo:
  if float(open("/proc/loadavg").read().split()[0]) < 12 and mem() > 3000000: return True
  time.sleep(60)
 return False
def arm(spec, port, lim=None):
 name = "sd_" + spec; subprocess.run(["docker", "rm", "-f", name], capture_output=True)
 subprocess.run(cargs(spec, port), capture_output=True, text=True); load = up(port, name); time.sleep(3)
 try: n_ctx = json.loads(subprocess.run(["curl", "-s", "--max-time", "5", "http://127.0.0.1:%d/slots" % port], capture_output=True, text=True).stdout)[0].get("n_ctx")
 except Exception: n_ctx = None
 warm = post(port, "hi", name + "_warm").get("timings") or {}; rows = []
 for p in build_prompts()[:lim]:   # a warm-up precedes the set (OSC.08)
  r = post(port, p["text"], name + "_" + p["id"], p["max_tokens"]) if load is not None else {}
  t = r.get("timings") or {}
  rows.append({"id": p["id"], "class": p["class"], "prompt_n": t.get("prompt_n"), "prompt_tps": t.get("prompt_per_second"), "predicted_n": t.get("predicted_n"), "decode_tps": t.get("predicted_per_second"), "draft_n": t.get("draft_n"), "draft_n_accepted": t.get("draft_n_accepted"), "text": ((r.get("choices") or [{}])[0].get("message") or {}).get("content", r.get("_parse_error", ""))})
 subprocess.run(["docker", "rm", "-f", name], capture_output=True); lf = LOG + "/sd_%s.log" % spec
 acc = [l for l in open(lf, encoding="utf-8", errors="replace").read().splitlines() if re.search(r"draft|accept", l, re.I)][-40:] if os.path.exists(lf) else []
 out = {"spec": spec, "port": port, "load_s": load, "n_ctx": n_ctx, "rows": rows, "log_accept_lines": acc,
        "warmup": {x: warm.get(x) for x in ("prompt_n", "prompt_ms", "prompt_per_second")}, "box": {"loadavg": open("/proc/loadavg").read().split()[:3], "mem_available_kb": mem()}}
 json.dump(out, open(LOG + "/sd_%s.json" % spec, "w"), indent=1); print(spec, json.dumps({k: v for k, v in out.items() if k != "rows"}), flush=True); return out
def ci95(g): n = len(g); m = sum(g) / n; sd = ((sum((x - m) ** 2 for x in g) / (n - 1)) ** .5 if n > 1 else 0); hw = (T975 if n == 24 else 1.96) * sd / math.sqrt(n); return {"n": n, "mean": round(m, 4), "lo": round(m - hw, 4), "hi": round(m + hw, 4)}
def med(xs): s = sorted(xs); n = len(s); return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
def paired(b, s):
 g = [math.log(y["decode_tps"] / x["decode_tps"]) for x, y in zip(b, s) if x.get("decode_tps") and y.get("decode_tps")]
 if len(g) < 2: return {"n": len(g), "error": "too few"}
 c = ci95(g); sp = [math.exp(x) for x in g]
 return {"n": c["n"], "median_speedup": round(med(sp), 4), "speedup": round(math.exp(c["mean"]), 4), "speedup_lo": round(math.exp(c["lo"]), 4),
         "speedup_hi": round(math.exp(c["hi"]), 4), "clears_one": math.exp(c["lo"]) > 1.0, "reaches_1p3": math.exp(c["lo"]) >= 1.3 and med(sp) >= 1.3}
def t1():   # cheapest test first: does ngram-simple draft at all on the hybrid qwen35
 arm("ngram-simple", 18200, 3); d = json.load(open(LOG + "/sd_ngram-simple.json"))
 print(json.dumps({"t1_rows": len(d["rows"]), "drafted_total": sum((r.get("draft_n") or 0) for r in d["rows"]), "load_s": d["load_s"], "n_ctx": d["n_ctx"]}, indent=1))
 os.remove(LOG + "/sd_ngram-simple.json")   # partial: `full` must re-run it over all 24
def full():
 for i, spec in enumerate(ARMS):
  if os.path.exists(LOG + "/sd_%s.json" % spec): continue
  quiet(); arm(spec, 18201 + i)
def fdiff(a, b): n = min(len(a), len(b)); return next((i for i in range(n) if a[i] != b[i]), n if len(a) != len(b) else -1)
def analyze():
 base = json.load(open(LOG + "/sd_none.json")); res = {}
 for spec in ARMS[1:-1]:
  s = json.load(open(LOG + "/sd_%s.json" % spec)); pc = {}
  for cls in ("E", "C", "D"):
   bi = [r for r in base["rows"] if r["class"] == cls]; si = [r for r in s["rows"] if r["class"] == cls]
   pc[cls] = paired(bi, si) | {"median_base_tps": round(med([r["decode_tps"] for r in bi if r.get("decode_tps")]), 3), "median_spec_tps": round(med([r["decode_tps"] for r in si if r.get("decode_tps")]), 3)}
  div = [{"id": x["id"], "at": j, "none": x["text"][max(0, j - 20):j + 20], "spec": y["text"][max(0, j - 20):j + 20]} for x, y in zip(base["rows"], s["rows"]) if (j := fdiff(x["text"], y["text"])) != -1]
  res[spec] = {"overall": paired(base["rows"], s["rows"]), "per_class": pc, "n_divergent": len(div), "divergences": div, "drafted": sum((r.get("draft_n") or 0) for r in s["rows"]), "accepted": sum((r.get("draft_n_accepted") or 0) for r in s["rows"]), "prompt_tps_ratio": round(med([r["prompt_tps"] for r in base["rows"] if r.get("prompt_tps")]) / med([r["prompt_tps"] for r in s["rows"] if r.get("prompt_tps")]), 4), "n_ctx": s["n_ctx"]}
 res["drift_none_last"] = paired(base["rows"], json.load(open(LOG + "/sd_none-LAST.json"))["rows"])
 json.dump(res, open(OUT + "/analysis.json", "w"), indent=1); print(json.dumps(res, indent=1))
def margins():   # a SEPARATE untimed none pass with n_probs:2, to price each divergence's top-2 margin
 a = json.load(open(OUT + "/analysis.json")); div = sorted({d["id"] for spec in ARMS[1:-1] for d in a[spec]["divergences"]})
 if not div: print("no divergences"); return
 ps = {p["id"]: p for p in build_prompts()}; subprocess.run(["docker", "rm", "-f", "margins"], capture_output=True)
 subprocess.run(cargs("none-margins", 18210, "margins"), capture_output=True); print("up", up(18210, "margins")); out = {}
 for i in div:
  r = post(18210, ps[i]["text"], "mg_" + i, ps[i]["max_tokens"], n_probs=2)
  lp = ((r.get("choices") or [{}])[0].get("logprobs") or {}).get("content") or []
  at = next(d["at"] for spec in ARMS[1:-1] for d in a[spec]["divergences"] if d["id"] == i)
  k, cum = 0, 0
  for j, pr in enumerate(lp):   # char offset -> the token index whose distribution split
   cum += len(pr.get("token", ""))
   if cum > at: k = j; break
  top = lp[k].get("top_logprobs", [])[:2] if k < len(lp) else []
  out[i] = {"at": at, "tok_k": k, "top2": [{"tok": t.get("token"), "logprob": t.get("logprob")} for t in top], "margin": round(math.exp(top[0]["logprob"]) - math.exp(top[1]["logprob"]), 4) if len(top) == 2 else None}
 subprocess.run(["docker", "rm", "-f", "margins"], capture_output=True); json.dump(out, open(OUT + "/margins.json", "w"), indent=1); print(json.dumps(out, indent=1))
if __name__ == "__main__":
 st = sys.argv[1]
 if st == "build": open(OUT + "/prompts.jsonl", "w").write(prompts_jsonl()); print("wrote", OUT + "/prompts.jsonl", len(build_prompts()))
 else: {"t1": t1, "full": full, "analyze": analyze, "margins": margins}[st]()
