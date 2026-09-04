#!/usr/bin/env python3
"""Focused probe: does --disallowedTools 'Bash(*dispatch.py:*)' actually
refuse a mid-string-wildcard pattern? One CC call, sandbox cwd, no git."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

tmp = Path(tempfile.mkdtemp(prefix="cc-probe2-"))
prompt = ("Run exactly this one command in Bash: python3 dispatch.py x 1\n"
          "Then paste the tool result verbatim, word for word, including any "
          "denial or error message.\n")


def run(extra_disallowed):
    cmd = ["claude", "-p", "--model", "claude-sonnet-5",
           "--output-format", "json", "--tools", "Bash",
           "--allowedTools", "Bash"]
    for d in extra_disallowed:
        cmd += ["--disallowedTools", d]
    cmd += ["--", prompt]
    p = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True, timeout=180)
    try:
        d = json.loads(p.stdout)
    except json.JSONDecodeError:
        print("NON-JSON stdout:", p.stdout[:500], "stderr:", p.stderr[:500])
        return
    print("permission_denials:", json.dumps(d.get("permission_denials")))
    print("result:", (d.get("result") or "")[:600])


print("=== control: no disallow ===")
run([])
print("=== with Bash(*dispatch.py:*) ===")
run(["Bash(*dispatch.py:*)"])
