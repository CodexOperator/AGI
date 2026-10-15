#!/usr/bin/env python3
"""Probe pi context duplication and the one-copy adapter; loopback only."""
import difflib, hashlib, http.server, importlib.util, json, os, pathlib, shutil, subprocess, tempfile, threading

ROOT = pathlib.Path.cwd()
AGENT_ID = "a00-206147f4"
HERE = pathlib.Path(__file__).resolve()
config = HERE.parents[3] / ".agi" / "config.json"
path_module_path = config.parent / "context" / "local-maxxing" / "paths.py"
spec = importlib.util.spec_from_file_location("local_maxxing_paths", path_module_path)
paths = importlib.util.module_from_spec(spec)
spec.loader.exec_module(paths)
OUT = pathlib.Path(paths.get_local("brain_swap_out_dir"))
CLAUDE = ROOT / "CLAUDE.md"
MARKER = "# CLAUDE.md — agi"
assert MARKER in CLAUDE.read_text(encoding="utf-8"), "stable CLAUDE marker missing"
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

def run(flags, agent_dir, base_url):
    models = {"providers":{"stub":{"baseUrl":base_url,"apiKey":"none","api":"openai-completions",
        "models":[{"id":"stub","contextWindow":65536,"maxTokens":16}]}}}
    (agent_dir / "models.json").write_text(json.dumps(models))
    env = {**os.environ, "PI_CODING_AGENT_DIR":str(agent_dir), "PI_OFFLINE":"1"}
    cmd = [shutil.which("pi"), "-p", "--no-session", "--no-tools", "--no-extensions",
           "--no-skills", "--no-prompt-templates", "--no-themes", "--provider", "stub",
           "--model", "stub", *flags, "Say ok"]
    return subprocess.run(cmd, cwd=ROOT, env=env, stdin=subprocess.DEVNULL, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)

def system_prompt(body):
    obj = json.loads(body)
    return next(m["content"] for m in obj["messages"] if m["role"] in ("system", "developer"))

def marker_copies(text):
    return text.count(MARKER)

def counter_selftest():
    for copies, expected in ((2, 2), (1, 1), (0, 0)):
        body = "\n".join([MARKER] * copies) + "\n"
        assert marker_copies(body) == expected
    return "PASS: toy 2 / 1 / 0 marker copies counted as 2 / 1 / 0"

def summarize(prompts, bodies):
    arms = {}
    for name, prompt in prompts.items():
        text = prompt
        arms[name] = {
            "request_bytes": len(bodies[name]), "system_prompt_bytes": len(text.encode()),
            "estimated_tokens_bytes_div_3_80": round(len(text.encode()) / 3.80, 1),
            "system_prompt_sha256": hashlib.sha256(text.encode()).hexdigest(),
            "claude_marker_copies": marker_copies(text),
        }
    default = prompts["default"]
    one_copy = prompts["one_copy"]
    source = CLAUDE.read_text(encoding="utf-8")
    assert default.count(source) == 2 and one_copy.count(source) == 1
    first = default.index(source)
    second = default.rindex(source) + len(source)
    context_start = default.index("# Project Context")
    prefix = default[:context_start]
    suffix = default[second:]
    one_prefix = one_copy[:one_copy.index(source)]
    one_suffix = one_copy[one_copy.index(source) + len(source):]
    framing = {
        "removed_project_context_preamble_bytes": first - context_start,
        "removed_between_copies_path_heading_bytes": len(default[first + len(source):default.rindex(source)]),
        "default_suffix": suffix,
        "one_copy_suffix": one_suffix,
        "unchanged_base_prefix": prefix == one_prefix,
    }
    other_moved = (
        framing["removed_project_context_preamble_bytes"] > 0 or
        framing["removed_between_copies_path_heading_bytes"] > 0 or suffix != one_suffix
    )
    saving = arms["default"]["estimated_tokens_bytes_div_3_80"] - arms["one_copy"]["estimated_tokens_bytes_div_3_80"]
    return arms, {"default_to_one_copy_estimated_token_saving": round(saving, 1),
                  "claude_payload_bytes_removed": len(source),
                  "only_duplicate_payload_moved": not other_moved,
                  "other_moved": framing if other_moved else None,
                  "unified_diff_hunk_count": sum(1 for line in difflib.unified_diff(
                      default.splitlines(), one_copy.splitlines(), n=0) if line.startswith("@@"))}

def main():
    assert counter_selftest() == "PASS: toy 2 / 1 / 0 marker copies counted as 2 / 1 / 0"
    server = http.server.ThreadingHTTPServer(("localhost", 0), Stub)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    with tempfile.TemporaryDirectory(prefix="pi-agent-") as td:
        agent_dir = pathlib.Path(td); base = f"http://localhost:{server.server_port}/v1"
        arm_flags = {
            "default": [],
            "no_context": ["--no-context-files"],
            "one_copy": ["--no-context-files", "--append-system-prompt", str(CLAUDE)],
        }
        prompts = {}
        for name, flags in arm_flags.items():
            start = len(requests); p = run(flags, agent_dir, base)
            assert p.returncode == 0, (name, p.stdout, p.stderr)
            assert len(requests) == start + 1, (name, len(requests), start)
            bodies[name] = requests[-1]
            prompts[name] = system_prompt(bodies[name])
            (OUT / f"{AGENT_ID}-{name}-request.json").write_bytes(bodies[name])
            (OUT / f"{AGENT_ID}-{name}-system.txt").write_text(prompts[name], encoding="utf-8")
    arms, diff = summarize(prompts, bodies)
    result = {"agent_id": AGENT_ID, "selftest": counter_selftest(), "arms": arms, "diff_summary": diff}
    (OUT / f"{AGENT_ID}-one-copy-results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    one = arms["one_copy"]
    assert arms["default"]["claude_marker_copies"] == 2
    assert one["claude_marker_copies"] == 1
    assert result["diff_summary"]["default_to_one_copy_estimated_token_saving"] >= 6500
    assert arms["no_context"]["claude_marker_copies"] == 0
    assert not diff["only_duplicate_payload_moved"]
    print("DISPROVED: copies/token conjuncts hold, but Project Context framing also moved")

if __name__ == "__main__":
    bodies = {}
    main()
