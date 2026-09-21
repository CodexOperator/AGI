"""DT.35 probe: re-measure the grok-bot-cli@0.3.1 SOURCE-read env set.

The prior round claimed the set was EXACTLY 22 names (20 literal
``process.env.<NAME>`` dot-accesses + 2 ``truthyEnv("...")`` literals) and
excluded three names that 0.3.1 reads through ALIASED DEFAULT-PARAMETER
reads, which no dot-access grep can see:

  * ``CODEX_HOME``    -- ``codex-bridge.js:27-28``:
        ``codexSocketPath(env = process.env)`` then ``env.CODEX_HOME``
  * ``APPDATA``       -- ``app-session.js:104-110``:
        ``grokBotAppDataPath(home, platform, env = {})`` then ``env.APPDATA``,
        called from ``grokBotGatewayDescriptorPath(..., env = process.env)``
  * ``XDG_CONFIG_HOME`` -- same ``app-session.js:104-110`` site

This probe runs FOUR scans over a 0.3.1 ``src`` tree and reports the union:

  (a) literal ``process.env.<NAME>`` dot-accesses
  (b) ``truthyEnv("<NAME>")`` string literals (computed accessor)
  (c) any ``env.<NAME>`` read through a parameter alias (the missed class)
  (d) any other dynamic read: ``process.env[...]`` computed site,
      ``...process.env`` spread, destructuring, ``Reflect`` on process.env

Usage::

    python3 probe_dt35.py <path-to-grok-bot-cli/src>

Exit 0 when the union reproduces >= 25 names and contains the three aliased
names; exit 1 otherwise.
"""
import re
import sys
from pathlib import Path

DOT = re.compile(r"process\.env\.([A-Za-z_][A-Za-z0-9_]*)")
ALIAS = re.compile(r"\benv\.([A-Za-z_][A-Za-z0-9_]*)")
TRUTHY = re.compile(r'truthyEnv\("([A-Za-z_][A-Za-z0-9_]*)"\)')
COMPUTED = re.compile(r"process\.env\[")
DYNAMIC = re.compile(r"\.\.\.process\.env|=\s*process\.env\b|Reflect\.")
ALIASED_DECL = re.compile(r"=\s*process\.env\b")

ALIASED_NAMES = {"CODEX_HOME", "APPDATA", "XDG_CONFIG_HOME"}


def read_all(src: Path) -> str:
    return "\n".join(p.read_text() for p in sorted(src.glob("*.js")))


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    src = Path(argv[1])
    blob = read_all(src)

    dot = set(DOT.findall(blob))
    truthy = set(TRUTHY.findall(blob))
    alias = {n for n in ALIAS.findall(blob) if n not in dot}
    computed_sites = COMPUTED.findall(blob)
    dynamic_sites = DYNAMIC.findall(blob)
    alias_decls = ALIASED_DECL.findall(blob)

    union = dot | truthy | alias

    print("(a) dot-accesses        :", len(dot))
    print("(b) truthyEnv literals  :", len(truthy), sorted(truthy))
    print("(c) aliased env.<NAME>  :", len(alias), sorted(alias))
    print("(d) computed sites      :", len(computed_sites))
    print("(d) =process.env decls  :", sorted(alias_decls))
    print("(d) spread/Reflect      :", len(dynamic_sites))
    print("UNION                   :", len(union))
    print("aliased names present   :", sorted(ALIASED_NAMES & union))
    print("AGI_MODEL in union      :", "AGI_MODEL" in union)
    print("MODEL in any name       :", any("MODEL" in n.upper() for n in union))
    print("UNION names             :")
    for n in sorted(union):
        print("   ", n)

    ok = (len(union) >= 25
          and ALIASED_NAMES <= union
          and "AGI_MODEL" not in union
          and not any("MODEL" in n.upper() for n in union))
    print("PROBE:", "pass" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))