#!/usr/bin/env python3
"""Resumable HumanEval arm runner. One sample/problem, greedy, thinking off, 512 tok.

Usage: runner.py <arm> <base_url> <model_id> <outdir> [limit]

Dataset: path from $HUMANEVAL if set, else the installed `human_eval` package's
bundled HumanEval.jsonl.gz. Results dir: <outdir> arg, else $ABC_OUTDIR, else the
directory this script lives in. NO worktree-absolute paths anywhere.
Writes <outdir>/<arm>.completions.jsonl (harness input) and <arm>.raw.jsonl (audit).
Skips task_ids already in the completions file (resumable).
"""
import gzip, json, os, re, sys, time, urllib.request

ARM, BASE, MODEL = sys.argv[1], sys.argv[2], sys.argv[3]
OUTDIR = sys.argv[4] if len(sys.argv) > 4 else os.environ.get(
    "ABC_OUTDIR", os.path.dirname(os.path.abspath(__file__)))
LIMIT = int(sys.argv[5]) if len(sys.argv) > 5 else 164

def human_eval_path():
    p = os.environ.get("HUMANEVAL")
    if p:
        return p
    import human_eval.data as d
    return os.path.join(os.path.dirname(os.path.abspath(d.__file__)),
                        "data", "HumanEval.jsonl.gz")

os.makedirs(OUTDIR, exist_ok=True)
COMP = os.path.join(OUTDIR, ARM + ".completions.jsonl")
RAW = os.path.join(OUTDIR, ARM + ".raw.jsonl")
done = set()
if os.path.exists(COMP):
    for line in open(COMP):
        if line.strip():
            done.add(json.loads(line)["task_id"])

problems = []
with gzip.open(human_eval_path(), "rt") as f:
    for line in f:
        problems.append(json.loads(line))
problems.sort(key=lambda p: p["task_id"])
print(f"[{ARM}] {len(problems)} problems, {len(done)} already done", flush=True)

# ONE fixed user template for all arms -- byte-recorded.
INSTR = ("Complete the following Python function. Write the complete function "
         "including its signature. Output only the code in a single ```python "
         "code block, no explanation.\n\n```python\n{p}\n```\n")

def extract_code(text):
    m = re.search(r"```(?:python)?\s*\n(.*?)```", text, re.S)
    if m:
        return m.group(1)
    return text

def completion_from(prompt, raw):
    code = extract_code(raw)
    p = prompt.strip("\n")
    c = code
    idx = c.find(p)
    if idx != -1 and idx < 40:
        c = c[idx + len(p):]
    if re.search(r"^\s*def\s+\w+\s*\(", c) and p not in c:
        lines = c.split("\n")
        for i, ln in enumerate(lines):
            if re.match(r"^\s*def\s+\w+\s*\(", ln):
                if i + 1 < len(lines):
                    indent = re.match(r"^(\s*)", lines[i + 1]).group(1)
                    c = "\n" + "\n".join(lines[i + 1:])
                    if indent == "":
                        c = "\n" + "\n".join("    " + x if x.strip() else x
                                              for x in lines[i + 1:])
                break
    return c

def call(prompt):
    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": INSTR.format(p=prompt)}],
        "temperature": 0.0, "top_k": 1, "top_p": 1.0, "seed": 1234,
        "max_tokens": 512, "stream": False,
        "chat_template_kwargs": {"enable_thinking": False},
    }
    req = urllib.request.Request(BASE + "/v1/chat/completions",
                                 data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=600) as r:
        resp = json.load(r)
    dt = time.time() - t0
    ch = resp["choices"][0]
    return (ch["message"]["content"] or ""), dt, ch.get("finish_reason")

n_new = 0
for prob in problems:
    tid = prob["task_id"]
    if tid in done:
        continue
    if n_new >= LIMIT:
        break
    try:
        raw, dt, finish = call(prob["prompt"])
    except Exception as e:
        print(f"[{ARM}] {tid} ERROR {e}", flush=True)
        time.sleep(2)
        continue
    comp = completion_from(prob["prompt"], raw)
    with open(COMP, "a") as f:
        f.write(json.dumps({"task_id": tid, "completion": comp}) + "\n")
    with open(RAW, "a") as f:
        f.write(json.dumps({"task_id": tid, "raw": raw, "prompt": prob["prompt"],
                            "secs": round(dt, 2), "finish": finish}) + "\n")
    n_new += 1
    print(f"[{ARM}] {n_new:3d} {tid} {dt:6.1f}s finish={finish} "
          f"comp_chars={len(comp)}", flush=True)
print(f"[{ARM}] done, {n_new} new completions this pass", flush=True)
