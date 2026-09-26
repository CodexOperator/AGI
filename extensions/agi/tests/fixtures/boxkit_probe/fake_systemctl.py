"""A systemctl that answers PER (manager, unit) and RECORDS every argv.

Two doors to the same brain, so the read-verb recording is identical whether the
box can fork or not:

  * as a script (the usual path) -- the executable the probe is handed as
    `--systemctl`;
  * as `answer(argv, log)` in-process, for boxes where RLIMIT_NPROC is below the
    live process count and every fork returns EAGAIN (measured on this box:
    `prlimit --nproc=300` + 1005 live procs in user@).

A WRONG-MANAGER ask answers `infinity`, which is what the real box does for
user@<uid>.service asked of the USER manager -- the DH.434 defect this probe
exists to kill.  A stub that answers every (manager, unit) pair the same is the
near miss and is banned.
"""
from __future__ import annotations
import json, os


def answer(argv, log: str) -> str:
    with open(log, "a") as fh:
        fh.write(json.dumps(list(argv)) + "\n")
    fact = json.loads(os.environ["PROBE_FACTORY"])
    mgr = "user" if "--user" in argv else "system"
    rest = [a for a in argv if a != "--user"]
    verb, unit = rest[0], rest[-1]
    props = rest[rest.index("-p") + 1].split(",") if "-p" in rest else []
    if verb == "is-active":
        return "active\n" if fact.get(mgr, {}).get(unit) else "inactive\n"
    if verb != "show":
        return ""                      # a mutation verb is never answered
    out = []
    for prop in props:
        val = fact.get(mgr, {}).get(unit, {}).get(prop)
        out.append("infinity" if val is None else str(val))
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    import sys
    sys.stdout.write(answer(sys.argv[1:], os.environ["PROBE_CALLS"]))
