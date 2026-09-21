#!/usr/bin/env python3
"""_shim.py — filtered output for the raw hardware tools (SM.122).

Runs the REAL tool (resolved past this shims directory) and drops the physical
lines: board/product/serial/host/MAC/IP. Class-level GPU memory survives,
never a model name. An absent tool is a clean no-op, never an error.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

DROP = re.compile(
    r"(serial|uuid|product|board|vendor|manufactur|hostname|\bMAC\b|"
    r"link/ether|inet6?\s+\d)", re.I)
IPV4_OR_MAC = re.compile(
    r"([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}|\b\d{1,3}(\.\d{1,3}){3}\b")


def _real(tool: str) -> str | None:
    here = Path(__file__).resolve().parent
    path = os.pathsep.join(
        p for p in os.environ.get("PATH", "").split(os.pathsep)
        if p and Path(p).resolve() != here)
    return shutil.which(tool, path=path)


def main(argv: list[str]) -> int:
    tool, args = argv[0], argv[1:]
    exe = _real(tool)
    if not exe:
        print(f"shim: {tool} absent on this box")
        return 0
    if tool == "nvidia-smi" and not args:
        out = subprocess.run(
            [exe, "--query-gpu=memory.total", "--format=csv,noheader,nounits"],
            capture_output=True, text=True)
        nums = [x for x in (out.stdout or "").split() if x.isdigit()]
        print("gpu: present")
        print("gpu_memory_mib: " +
              (str(sum(int(n) for n in nums)) if nums else "unreadable"))
        return 0
    out = subprocess.run([exe, *args], capture_output=True, text=True)
    for line in (out.stdout or "").splitlines():
        if DROP.search(line) or IPV4_OR_MAC.search(line):
            continue
        print(line)
    return out.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
