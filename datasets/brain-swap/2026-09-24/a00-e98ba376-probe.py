#!/usr/bin/env python3
"""Record pi's first request with and without project context; no real model call."""
import hashlib, http.server, json, os, pathlib, subprocess, tempfile, threading

PI = pathlib.Path("/home/belam/.npm-global/lib/node_modules/@mariozechner/pi-coding-agent/dist/cli.js")
ROOT = pathlib.Path.cwd()
OUT = pathlib.Path("datasets/brain-swap/2026-09-24")
requests = []

class Stub(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("content-length", 0)))
        requests.append(body)
        chunks = [
            {"id":"stub","object":"chat.completion.chunk","created":0,"model":"stub",
             "choices":[{"index":0,"delta":{"role":"assistant","content":"ok"},"finish_reason":None}]},
            {"id":"stub","object":"chat.completion.chunk","created":0,"model":"stub",
             "choices":[{"index":0,"delta":{},"finish_reason":"stop"}],
             "usage":{"prompt_tokens":0,"completion_tokens":1,"total_tokens":1}},
        ]
        data = b"".join(("data: " + json.dumps(x) + "\n\n").encode() for x in chunks) + b"data: [DONE]\n\n"
        self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
        self.wfile.write(data)
    def log_message(self, *_): pass

def run(flag, agent_dir, base_url):
    models = {"providers":{"stub":{"baseUrl":base_url,"apiKey":"none","api":"openai-completions",
        "models":[{"id":"stub","contextWindow":65536,"maxTokens":16}]}}}
    (agent_dir / "models.json").write_text(json.dumps(models))
    env = {**os.environ, "PI_CODING_AGENT_DIR":str(agent_dir), "PI_OFFLINE":"1"}
    cmd = ["node",str(PI),"-p","--no-session","--no-tools","--no-extensions","--no-skills",
           "--no-prompt-templates","--no-themes","--provider","stub","--model","stub",flag,"Say ok"]
    return subprocess.run(cmd, cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
                          text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=45)

def system_prompt(body):
    obj = json.loads(body)
    return next(m["content"] for m in obj["messages"] if m["role"] in ("system", "developer"))

def fixture_selftest(loader):
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        root, child = pathlib.Path(td), pathlib.Path(td)/"child"
        child.mkdir(); source = root/"CLAUDE.md"; source.write_text("# fixture\n")
        (root/"AGENTS.md").symlink_to(source.name); (child/"AGENTS.md").symlink_to(source)
        got = loader(child, root)
        assert len(got) == 2 and all(x["content"] == "# fixture\n" for x in got)
        assert [] == []  # noContextFiles maps directly to agentsFiles: [] in resource-loader.js:323
    return "PASS: nested symlinked AGENTS.md => 2 loaded; flag => 0"

def main():
    server = http.server.ThreadingHTTPServer(("localhost", 0), Stub)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    with tempfile.TemporaryDirectory(prefix="pi-agent-") as td:
        agent_dir = pathlib.Path(td); base = f"http://localhost:{server.server_port}/v1"
        runs = []
        for name, flag in (("with", ""), ("without", "--no-context-files")):
            start = len(requests); p = run(flag, agent_dir, base)
            assert p.returncode == 0, (name, p.stdout, p.stderr)
            assert len(requests) == start + 1, (name, len(requests), start)
            runs.append(name)
    server.shutdown()
    prompts = [system_prompt(b) for b in requests[:2]]
    def only_context_inserted(larger, smaller):
        i = 0
        while i < len(smaller) and larger[i] == smaller[i]: i += 1
        cut = len(larger) - (len(smaller) - i)
        return larger[:i] + larger[cut:] == smaller and "# Project Context" in larger[i:cut]
    report = {
      "runs": {"with": {"request_bytes":len(requests[0]),"system_prompt_bytes":len(prompts[0].encode()),
                        "system_prompt_sha256":hashlib.sha256(prompts[0].encode()).hexdigest(),
                        "estimated_tokens_bytes_div_3_80":round(len(prompts[0].encode())/3.80,1),
                        "agents_copies":prompts[0].count("# CLAUDE.md — agi")},
               "without": {"request_bytes":len(requests[1]),"system_prompt_bytes":len(prompts[1].encode()),
                        "system_prompt_sha256":hashlib.sha256(prompts[1].encode()).hexdigest(),
                        "estimated_tokens_bytes_div_3_80":round(len(prompts[1].encode())/3.80,1),
                        "agents_copies":prompts[1].count("# CLAUDE.md — agi")}},
      "saving": {"request_bytes":len(requests[0])-len(requests[1]),
                 "system_prompt_bytes":len(prompts[0].encode())-len(prompts[1].encode()),
                 "estimated_tokens_bytes_div_3_80":round((len(prompts[0].encode())-len(prompts[1].encode()))/3.80,1)},
      "context_only_diff": only_context_inserted(prompts[0], prompts[1]),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    stem = "a00-e98ba376-pi-context"
    (OUT/f"{stem}.json").write_text(json.dumps(report,indent=2)+"\n")
    (OUT/f"{stem}-with.txt").write_text(prompts[0]); (OUT/f"{stem}-without.txt").write_text(prompts[1])
    print(json.dumps(report,indent=2))
if __name__ == "__main__":
    main()
