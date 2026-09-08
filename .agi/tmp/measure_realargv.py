#!/usr/bin/env python3
"""Measure what a REAL kid argv actually injects (SD.08 KID-4), fixed.

build_command appends three kinds of segment after `--append-system-prompt`:
  (a) a real file path (context_file=INJECTION.md, skill_prompt=agent-prompt.md)
  (b) an inline string (brief segments, closing line)
Distinguish them and token-count each. Determine if skills/agi/SKILL.md content
is ever present in the argv.
"""
import sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "extensions" / "agi" / "bin"))

import tiktoken
ENC = tiktoken.get_encoding("o200k_base")
def tok(t): return len(ENC.encode(t))

from adapters import pi_adapter

def measure(tier="kid"):
    harness = {"name": "pi", "adapter": "pi_adapter", "env": {}}
    ctx = ROOT / ".agi" / "context" / "INJECTION.md"
    ctx_s = str(ctx) if ctx.is_file() else "/nonexistent"
    sess = Path(tempfile.mkdtemp())
    argv = pi_adapter.build_command(
        harness=harness, tier=tier, context_file=ctx_s,
        agent_id="a00-test", iter_n="SD.08", sess_dir=sess,
        cli_py=str(ROOT/"extensions/agi/bin/cli.py"),
        skill_prompt=ROOT/"extensions/agi/lib/agent-prompt.md",
        scaffold={"path": "/tmp/x.md", "node_type": "experiment",
                  "node_id": "experiment:a00-test", "parent": "hypothesis:x"},
        dispatch_py=str(ROOT/"extensions/agi/bin/dispatch.py"),
        source_root=str(ROOT),
    )
    total = 0
    segs = []
    for i, a in enumerate(argv):
        if a == "--append-system-prompt":
            val = argv[i+1] if i+1 < len(argv) else None
            is_file = False
            if val and len(val) > 0 and len(val) < 4096:
                try:
                    is_file = Path(val).is_file()
                except OSError:
                    is_file = False
            if is_file:
                content = Path(val).read_text(encoding="utf-8")
                n = tok(content)
                segs.append((n, "FILE = " + val))
            else:
                n = tok(val) if val else 0
                head = (val or "").replace("\n", " ")[:70]
                segs.append((n, "INLINE = " + head))
    total = sum(n for n, _ in segs)
    print(f"=== {tier}: {total} total injected tokens over {len(segs)} segments ===")
    for n, s in sorted(segs, reverse=True):
        print(f"  {n:6d}  {s}")

for t in ("kid", "parent", "director", "prime_director"):
    measure(t)
skill = (ROOT/"skills/agi/SKILL.md").read_text(encoding="utf-8")
print(f"\nskills/agi/SKILL.md itself = {tok(skill)} tok if it were injected (it is NOT in build_command argv)")