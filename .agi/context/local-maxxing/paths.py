#!/usr/bin/env python3
"""ONE shared path reader for the local-maxxing experiment chains.

Every filesystem path these scripts rely on is a named variable under
`paths.local_maxxing` in the nearest enclosing `.agi/config.json`
(goal:g5 / hypothesis:lm-every-experiment-path-is-a-config-variable).

Values are REPO-RELATIVE (they resolve against `box.root`, the config's own
box root -- never the nearest `.agi`, never cwd, never this file's location).
A value may carry the placeholders `{root}` (= `box.root`) and `{pi_home}` /
`{claude_home}` (from `locations.*`); any other `box.*` / `locations.*` string
cell is available under its own bare name too. After substitution an absolute
value is returned unchanged; a relative one is joined onto `box.root`.

The one exception is get_local() (OSC.01): the same value, but a relative one
is joined onto the CHECKOUT holding the `.agi/config.json` it read -- for the
inputs and outputs a round keeps in its own worktree, and on a box whose
`box.root` cell is stale.

    python3 .agi/context/local-maxxing/paths.py <key>          # -> resolved value
    python3 .agi/context/local-maxxing/paths.py --local <key>  # -> checkout-anchored
    from the importable accessor: paths.get("<key>") / paths.get_local("<key>")

Unknown key -> message on stderr, exit 1.

Shell callers:  none exist yet (mur-director-thought-3); one would call  V="$(python3 .agi/context/local-maxxing/paths.py <key>)"
Python callers reach this file by a path DISCOVERED from `__file__`
(walk up to the `.agi/config.json`, then into its `context/local-maxxing/`),
never by a new absolute literal.
"""
import json
import os
import re
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
NAMESPACE = "local_maxxing"
_CACHE = {}

PROPOSED_BOX_ROOTS = {
    "models_dir": "/data/ml/models",     # proposed box.models_dir
    "ml_scratch_dir": "/data/ml/scratch",  # proposed box.ml_scratch_dir
    "ml_venv_dir": "/data/ml/.venv",     # proposed box.ml_venv_dir
    "ml_tools_dir": "/data/ml/tools",    # proposed box.ml_tools_dir
}


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
    cells = dict(PROPOSED_BOX_ROOTS)
    cells.update(cfg.get("locations") or {})
    cells.update(cfg.get("box") or {})
    return {"{%s}" % k: v for k, v in cells.items() if isinstance(v, str)}


def _substitute(doc, value):
    for name, repl in _placeholders(doc).items():
        value = value.replace(name, repl)
    unresolved = re.search(r"\{([^}]+)\}", value)
    if unresolved:
        raise KeyError("unresolved path placeholder: %s" % unresolved.group(1))
    return value


def get(key):
    """Resolved value of paths.local_maxxing.<key>; relative values anchored at box.root."""
    cfg, doc = _config()
    table = ((doc.get("paths") or {}).get(NAMESPACE)) or {}
    if key not in table:
        raise KeyError("paths.%s.%s is not defined in %s"
                       % (NAMESPACE, key, cfg))
    val = _substitute(doc, table[key])
    root = (doc.get("box") or {}).get("root")
    if not root:
        raise KeyError("box.root is not defined in %s" % cfg)
    return val if os.path.isabs(val) else os.path.normpath(os.path.join(root, val))


def checkout_root(start=None):
    """Dir holding the .agi/ that config_path() resolved -- not box.root."""
    return os.path.dirname(os.path.dirname(config_path(start)))


def main_checkout_root(start=None):
    """Main checkout containing this checkout's shared git directory."""
    checkout = checkout_root(start)
    try:
        common = subprocess.check_output(
            ["git", "-C", checkout, "rev-parse", "--path-format=absolute", "--git-common-dir"],
            text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return checkout
    return os.path.dirname(os.path.abspath(common))


def get_local(key):
    """Like get(), but relative values anchor at the CHECKOUT THE CONFIG WAS READ FROM.

    get() anchors at box.root, which is a per-box absolute path and can be stale or
    point at the main checkout while this code runs in a worktree. get_local() keeps
    get()'s placeholder substitution but resolves repo-relative values against the
    checkout that owns the .agi/config.json it just read. Absolute values unchanged.
    """
    cfg, doc = _config()
    table = ((doc.get("paths") or {}).get(NAMESPACE)) or {}
    if key not in table:
        raise KeyError("paths.%s.%s is not defined in %s" % (NAMESPACE, key, cfg))
    val = _substitute(doc, table[key])
    return val if os.path.isabs(val) else os.path.normpath(os.path.join(checkout_root(), val))


# alias: some callers read naturally as paths.resolve("k")
resolve = get


def main(argv):
    args = list(argv[1:])
    fn = get
    if args and args[0] == "--local":
        fn = get_local
        args = args[1:]
    if len(args) != 1:
        sys.stderr.write("usage: paths.py [--local] <key>\n")
        return 2
    try:
        print(fn(args[0]))
    except KeyError as exc:
        sys.stderr.write("%s\n" % exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
