#!/usr/bin/env python3
"""OpenRouter shim so the UNCHANGED HumanEval runner.py can drive the reference.

Injects the bearer key, drops llama.cpp's `chat_template_kwargs`, and expresses
thinking-off the OpenRouter way (`reasoning.enabled=false`). Logs each response's
`usage` to usage_log.jsonl. Usage: proxy.py [port]  (default 8787).
"""
import json, os, sys, urllib.error, urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

URL = "https://openrouter.ai/api/v1/chat/completions"
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "usage_log.jsonl")


class H(BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(n))
        body.pop("chat_template_kwargs", None)
        body["reasoning"] = {"enabled": False}
        req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"]})
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                out = r.read()
            with open(LOG, "a") as f:
                f.write(json.dumps(json.loads(out).get("usage", {})) + "\n")
            self.send_response(200)
        except urllib.error.HTTPError as e:
            out = e.read()
            self.send_response(e.code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", int(sys.argv[1]) if len(sys.argv) > 1 else 8787), H).serve_forever()