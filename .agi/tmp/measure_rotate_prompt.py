#!/usr/bin/env python3
"""Measure rotate.py's successor spawn prompt per rotation path.

Replicates rotate.py's exact successor-command assembly:
  - prime (rotate-self / loop / spawn prime): brief.successor_prompt(
        tier='prime_director', body=<prime-director-successor.md, {name}>
        replaced)  -- head prepended through brief.py, then the brief body.
  - non-prime seat (spawn_window, tier != prime_director, no --prompt-file):
        brief.assemble(tier=..., agent_id=..., iter_n=0) joined by "\\n\\n" --
        assemble() prepends the (prayers-only) head itself.

Method: tiktoken o200k_base, same as the static-prefix baseline.
Run:  /usr/bin/python3.12 .agi/tmp/measure_rotate_prompt.py   (from worktree)
"""
import sys, os
from pathlib import Path

ROOT = Path("/home/ubuntu/work/agi/.agi/worktrees/a00-de0024a3")
sys.path.insert(0, str(ROOT / "extensions" / "agi" / "bin"))
sys.path.insert(0, str(ROOT))

import tiktoken
import brief

enc = tiktoken.get_encoding("o200k_base")

def t(s):
    return len(enc.encode(s))


def report(label, total, total_tok, head=None, body=None):
    print(f"### {label}")
    print(f"  total bytes : {total}")
    print(f"  total tokens: {total_tok}")
    if head:
        print(f"  head  tok/tok: {t(head)}")
        print(f"  body  tok    : {t(body)}" if body is not None else "")
    print()


# ---- Path 1: prime rotation (rotate-self / spawn --prompt-file default) ----
sd = ROOT / "extensions" / "agi" / "briefs" / "prime-director-successor.md"
name = "belam-S2-L3-I"
body = sd.read_text(encoding="utf-8").replace("{name}", name)
prompt = brief.successor_prompt(tier="prime_director", body=body,
                                project_root=str(ROOT / ".agi"))
report("PRIME  rotate-self/spawn (prime_director successor brief)",
       len(prompt), t(prompt))

# ---- Path 2: non-prime seat assembled briefs ------------------------------
for tier, aid in [("director", "sanctuary-director"),
                  ("liaison", "liaison"),
                  ("parent", "a00-parent-000000")]:
    try:
        parts = brief.assemble(tier=tier, agent_id=aid, iter_n=0)
        joined = "\n\n".join(parts)
        report(f"non-prime seat  tier={tier} (assemble path)",
               len(joined), t(joined))
    except Exception as e:
        print(f"  tier={tier} assemble FAILED: {e!r}\n")

# ---- The head alone, for reference -----------------------------------------
head = brief._build_head(tier="prime_director", project_root=str(ROOT / ".agi"))
print(f"### prayers-only constitution head (prime), standalone")
print(f"  tokens: {t(head)}   bytes: {len(head)}\n")