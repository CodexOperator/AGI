#!/usr/bin/env python3
"""ONE shared path reader for the local-maxxing experiment chains.

Every filesystem path these scripts rely on is a named variable under `paths`
in the nearest enclosing `.agi/config.json` (goal:g14 / hypothesis:lm-every-
experiment-path-is-a-config-variable). A RELATIVE value resolves from the repo
root -- the directory holding that `.agi/`; an absolute value is returned
unchanged. `box.root` is deliberately NOT consulted: it names another box.

    python3 .agi/context/local-maxxing/paths.py <key>   # -> resolved value
    from the importable accessor: paths.get("<key>")    # when imported

Shell callers:  V="$(python3 .agi/context/local-maxxing/paths.py <key>)"
Python callers must reach this file by a path DISCOVERED from __file__, never
by a new absolute literal.
"""
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_CACHE = {}


def repo_root(start=None):
    """Walk up to the nearest ancestor holding .agi/config.json."""
    p = os.path.abspath(start or _HERE)
    while True:
        if os.path.isfile(os.path.join(p, ".agi", "config.json")):
            return p
        parent = os.path.dirname(p)
        if parent == p:
            raise RuntimeError("no .agi/config.json above %s" % (start or _HERE))
        p = parent


def _paths():
    root = repo_root()
    if root not in _CACHE:
        with open(os.path.join(root, ".agi", "config.json"), encoding="utf-8") as fh:
            _CACHE[root] = json.load(fh).get("paths") or {}
    return root, _CACHE[root]


def get(key):
    """Resolved value of paths.<key>; relative values anchored at the repo root."""
    root, table = _paths()
    if key not in table:
        raise KeyError("paths.%s is not defined in %s/.agi/config.json"
                       % (key, root))
    val = table[key]
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
