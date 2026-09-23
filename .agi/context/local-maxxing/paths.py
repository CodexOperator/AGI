#!/usr/bin/env python3
"""ONE shared path reader for the local-maxxing experiment chains.

Every filesystem path these scripts rely on is a named variable under
`paths.local_maxxing` in the nearest enclosing `.agi/config.json`
(goal:g14 / hypothesis:lm-every-experiment-path-is-a-config-variable).

Values are REPO-RELATIVE (they resolve against `box.root`, the config's own
box root -- never the nearest `.agi`, never cwd, never this file's location).
A value may carry the placeholders `{root}` (= `box.root`) and `{pi_home}` /
`{claude_home}` (from `locations.*`); any other `box.*` / `locations.*` string
cell is available under its own bare name too. After substitution an absolute
value is returned unchanged; a relative one is joined onto `box.root`.

    python3 .agi/context/local-maxxing/paths.py <key>   # -> resolved value
    from the importable accessor: paths.get("<key>")    # when imported

Unknown key -> message on stderr, exit 1.

Shell callers:  V="$(python3 .agi/context/local-maxxing/paths.py <key>)"
Python callers reach this file by a path DISCOVERED from `__file__`
(walk up to the `.agi/config.json`, then into its `context/local-maxxing/`),
never by a new absolute literal.
"""
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
NAMESPACE = "local_maxxing"
_CACHE = {}


def config_path(start=None):
    """Walk up to the nearest ancestor holding .agi/config.json."""
    p = os.path.abspath(start or _HERE)
    while True:
        cfg = os.path.join(p, ".agi", "config.json")
        if os.path.isfile(cfg):
            return cfg
        parent = os.path.dirname(p)
        if parent == p:
            raise RuntimeError("no .agi/config.json above %s" % (start or _HERE))
        p = parent


def _config():
    cfg = config_path()
    if cfg not in _CACHE:
        with open(cfg, encoding="utf-8") as fh:
            _CACHE[cfg] = json.load(fh)
    return cfg, _CACHE[cfg]


def _placeholders(cfg):
    """`{name}` for every string cell in box.* and locations.*; box.root wins."""
    cells = {}
    cells.update(cfg.get("locations") or {})
    cells.update(cfg.get("box") or {})
    return {"{%s}" % k: v for k, v in cells.items() if isinstance(v, str)}


def get(key):
    """Resolved value of paths.local_maxxing.<key>; relative values anchored at box.root."""
    cfg, doc = _config()
    table = ((doc.get("paths") or {}).get(NAMESPACE)) or {}
    if key not in table:
        raise KeyError("paths.%s.%s is not defined in %s"
                       % (NAMESPACE, key, cfg))
    val = table[key]
    for name, repl in _placeholders(doc).items():
        val = val.replace(name, repl)
    root = (doc.get("box") or {}).get("root")
    if not root:
        raise KeyError("box.root is not defined in %s" % cfg)
    return val if os.path.isabs(val) else os.path.normpath(os.path.join(root, val))


# alias: some callers read naturally as paths.resolve("k")
resolve = get


def main(argv):
    if len(argv) != 2:
        sys.stderr.write("usage: paths.py <key>\n")
        return 2
    try:
        print(get(argv[1]))
    except KeyError as exc:
        sys.stderr.write("%s\n" % exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
