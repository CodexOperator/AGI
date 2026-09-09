#!/usr/bin/env python3
"""SD.10 DENOMINATOR RESOLUTION (item 75) — measure both denominators fresh.

DENOM A: pi parent/kid post-survival argv via pi_adapter.build_command,
         profile=full and profile=survival.
DENOM B: CC-seat cold files — size + o200k token count of HANDOFF.md,
         CLAUDE.md, skills/agi/SKILL.md, and brief.py's assembled head.

Uses /usr/bin/python3.12 which has tiktoken (trap 0z).
"""
import sys, os, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "extensions" / "agi" / "bin"))

import tiktoken
ENC = tiktoken.get_encoding("o200k_base")
def tok(t: str) -> int:
    return len(ENC.encode(t or ""))

if os.environ.get("PYTHON_EXE"):
    import sys as _s
    _s.stderr.write(f"note: running under {_s.executable}\n")

from adapters import pi_adapter

def build(tier: str, profile: str):
    os.environ["AGI_BRIEF_PROFILE"] = profile
    harness = {"name": "pi", "adapter": "pi_adapter", "env": {}}
    ctx = ROOT / ".agi" / "context" / "INJECTION.md"
    ctx_s = str(ctx) if ctx.is_file() else "/nonexistent"
    sess = Path(tempfile.mkdtemp())
    argv = pi_adapter.build_command(
        harness=harness, tier=tier, context_file=ctx_s,
        agent_id="a00-denom", iter_n="SD.10", sess_dir=sess,
        cli_py=str(ROOT/"extensions/agi/bin/cli.py"),
        skill_prompt=ROOT/"extensions/agi/lib/agent-prompt.md",
        scaffold={"path": "/tmp/x.md", "node_type": "experiment",
                  "node_id": "experiment:a00-denom", "parent": "hypothesis:l3w4-context-load-minimal"},
        dispatch_py=str(ROOT/"extensions/agi/bin/dispatch.py"),
        source_root=str(ROOT),
    )
    return argv

def argv_tokens(argv) -> dict:
    """Token-count each --append-system-prompt segment (file vs inline)."""
    segs = []
    for i, a in enumerate(argv):
        if a == "--append-system-prompt":
            val = argv[i+1] if i+1 < len(argv) else None
            n = 0; kind = "inline"
            if val and 0 < len(val) < 4096:
                try:
                    p = Path(val)
                    if p.is_file():
                        n = tok(p.read_text(encoding="utf-8"))
                        kind = "FILE:" + p.name
                    else:
                        n = tok(val); kind = "inline"
                except OSError:
                    n = tok(val); kind = "inline"
            segs.append((kind, n))
    total = sum(n for _, n in segs)
    return total, segs

print("=== DENOM A: pi argv injected tokens, o200k, python3.12 ===")
for profile in ("full", "survival"):
    for tier in ("kid", "parent", "director", "prime_director"):
        argv = build(tier, profile)
        total, segs = argv_tokens(argv)
        detail = " ".join(f"{k}={n}" for k, n in segs)
        print(f"  {profile:9s} {tier:15s} total={total:6d}  [{detail}]")
# restore
os.environ["AGI_BRIEF_PROFILE"] = "full"

print("\n=== DENOM B: CC-seat cold files, bytes + o200k tokens ===")
import brief as _brief
head = _brief._build_head(tier="director")  # prayers-only head
files = {
    "HANDOFF.md (current)": ROOT / "HANDOFF.md",
    "CLAUDE.md (current)": ROOT / "CLAUDE.md",
    "skills/agi/SKILL.md": ROOT / "skills" / "agi" / "SKILL.md",
    "constitution head (director, prayers-only)": None,
}
for label, p in files.items():
    content = head if p is None else p.read_text(encoding="utf-8")
    print(f"  {label:45s} bytes={len(content.encode('utf-8')):7d} tok={tok(content):6d}")