#!/usr/bin/env python3.12
"""benchmark.py — Ollama-based chain quality judgment.

Judges whether an autoresearch chain extension is worth continuing.
Outputs: continue | close | branch
Writes chain_id to closed_chains.txt when judgment is close.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

try:
    import ollama
except ImportError:
    print("ERR: ollama package not installed (pip install ollama)", file=sys.stderr)
    sys.exit(1)

DEFAULT_MODEL = "qwen3:4b"
CLOSED_CHAINS_FILE = "closed_chains.txt"


def _find_root() -> Path:
    d = Path.cwd().resolve()
    while d != d.parent:
        if (d / "autoresearch-tree.config.json").exists():
            return d
        d = d.parent
    print("ERR: no autoresearch-tree.config.json found from cwd up", file=sys.stderr)
    sys.exit(1)


def _load_chain(root: Path, chain_id: str) -> dict | None:
    """Load chain node file by id (format: type:slug)."""
    if ":" not in chain_id:
        return None
    node_type, slug = chain_id.split(":", 1)
    type_dir = node_type.replace("-", "_")
    node_file = root / "nodes" / type_dir / f"{slug}.md"
    if not node_file.exists():
        return None
    return {"path": str(node_file), "type": node_type, "slug": slug}


def _parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse markdown frontmatter. Returns (fm_dict, body)."""
    lines = content.splitlines()
    if not lines or lines[0] != "---":
        return {}, content
    end = 1
    for i in range(1, len(lines)):
        if lines[i] == "---":
            end = i
            break
    fm_lines = lines[1:end]
    body = "\n".join(lines[end + 1 :])
    fm = {}
    for line in fm_lines:
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip()
    return fm, body


def _build_judge_prompt(chain_file: Path, chain_id: str) -> str:
    """Build prompt for the LLM judge."""
    content = chain_file.read_text()
    fm, body = _parse_frontmatter(content)

    parent_info = ""
    if "parents" in fm:
        parent_info = f"\nParents: {fm['parents']}"

    return f"""You are a research quality judge. Evaluate this autoresearch chain node and decide whether to CONTINUE, CLOSE, or BRANCH.

Chain node: {chain_id}
Type: {fm.get("type", "unknown")}
Status: {fm.get("status", "unknown")}
Confidence: {fm.get("confidence", "N/A")}
Verdict: {fm.get("verdict", "N/A")}{parent_info}

--- Body ---
{body}
--- End ---

Rate quality on:
1. Evidence strength (0-10): Is there real data, logs, or outputs?
2. Signal clarity (0-10): Is there a clear finding or is it vague?
3. Momentum (0-10): Does this lead somewhere new or is it stalled?

Respond ONLY with one of:
  CONTINUE  — strong evidence, clear signal, good momentum. Keep extending.
  CLOSE     — weak evidence, vague results, or hit a dead end. Stop this branch.
  BRANCH    — interesting but uncertain. Worth exploring multiple directions.

Your response must be exactly one word: CONTINUE, CLOSE, or BRANCH"""


def judge_chain(chain_id: str, model: str = DEFAULT_MODEL, timeout: int = 120) -> str:
    """Call Ollama to judge a chain. Returns: continue|close|branch."""
    root = _find_root()
    chain = _load_chain(root, chain_id)
    if not chain:
        print(f"ERR: chain not found: {chain_id}", file=sys.stderr)
        sys.exit(1)

    prompt = _build_judge_prompt(Path(chain["path"]), chain_id)

    try:
        response = ollama.generate(
            model=model,
            prompt=prompt,
            options={
                "timeout": timeout,
                "temperature": 0.1,
                "num_predict": 50,
                "think": False,
            },
        )
    except Exception as e:
        print(f"ERR: ollama call failed: {e}", file=sys.stderr)
        sys.exit(1)

    raw = response["response"].strip().lower()

    if "continue" in raw:
        return "continue"
    elif "close" in raw:
        return "close"
    elif "branch" in raw:
        return "branch"
    else:
        # Fallback: treat ambiguous as close
        print(f"WARN: ambiguous judge output '{raw}', defaulting to close", file=sys.stderr)
        return "close"


def write_closed_chain(chain_id: str) -> None:
    """Append chain_id to closed_chains.txt."""
    root = _find_root()
    out = root / CLOSED_CHAINS_FILE
    with open(out, "a") as f:
        f.write(f"{chain_id}\n")


def main() -> int:
    ap = argparse.ArgumentParser(description="Ollama-based chain quality judgment")
    ap.add_argument("chain_id", help="Chain node id (type:slug)")
    ap.add_argument(
        "--model", default=DEFAULT_MODEL, help=f"Ollama model (default: {DEFAULT_MODEL})"
    )
    ap.add_argument(
        "--timeout", type=int, default=120, help="Timeout in seconds (default: 120)"
    )
    ap.add_argument(
        "--dry-run", action="store_true", help="Print judgment without side effects"
    )
    args = ap.parse_args()

    verdict = judge_chain(args.chain_id, model=args.model, timeout=args.timeout)

    if args.dry_run:
        print(f"{verdict.upper()}: {args.chain_id}")
        return 0

    print(verdict)

    if verdict == "close":
        write_closed_chain(args.chain_id)
        print(f"chain closed: {args.chain_id}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
