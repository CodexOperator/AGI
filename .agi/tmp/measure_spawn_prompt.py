"""Measure rotate.py's successor-spawn-prompt assembly (SD.08).

Rotate.py-focused slice of hypothesis:l3w4-context-load-minimal:
measure the rotation spawn prompt (constitution head + successor brief body)
for the three rotation paths, broken down head vs body, tokens AND bytes.
Method: tiktoken o200k_base, same as the sibling SKILL.md/INJECTION.md round.
"""
import sys, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]   # worktree root (cwd)
sys.path.insert(0, str(ROOT / "extensions" / "agi" / "bin"))

import tiktoken
ENC = tiktoken.get_encoding("o200k_base")

def tok(text: str) -> int:
    return len(ENC.encode(text))

import brief

DEFAULT_PROMPT_FILE = (ROOT / "extensions" / "agi" / "briefs"
                       / "prime-director-successor.md")
body = DEFAULT_PROMPT_FILE.read_text(encoding="utf-8")

head = brief._build_head(tier="prime_director", project_root=None)

# 1) plain rotate-self rotation (prime successor brief file)
prompt = brief.successor_prompt(tier="prime_director", body=body, project_root=None)

# 2) loop rotation = same prompt + the continuation line appended via extra=
continuation = (
    "ROTATION CONTINUATION: if the handoff needs no change, answer "
    "exactly the single word `continue` and stop. Otherwise reply with "
    "the exact diff you would make."
)
prompt_loop = prompt + "\n\n" + continuation

# 3) spawn (bare launcher, prime path also uses DEFAULT_PROMPT_FILE;
#    a non-prime seat spawn uses the assembled brief via _assembled_successor_command;
#    measure that too for completeness)
asmb = "\n\n".join(brief.assemble(tier="parent", agent_id="demo-parent", iter_n=0,
    dispatch_py="extensions/agi/bin/dispatch.py", cli_py="extensions/agi/bin/cli.py"))

print("=== head (brief._build_head, prime_director) ===")
print("tokens:", tok(head), " bytes:", len(head.encode()))
print()
print("=== body (prime-director-successor.md) ===")
print("tokens:", tok(body), " bytes:", len(body.encode()))
print()
print("=== successor_prompt (plain rotate-self) ===")
print("tokens:", tok(prompt), " bytes:", len(prompt.encode()))
print("head share:", round(100*tok(head)/tok(prompt),1), "% tokens")
print()
print("=== loop rotation (prompt + continuation) ===")
print("tokens:", tok(prompt_loop), " bytes:", len(prompt_loop.encode()))
print("continuation tokens:", tok(continuation))
print()
print("=== non-prime spawn via assembled brief (tier=parent) ===")
print("tokens:", tok(asmb), " bytes:", len(asmb.encode()))
print()