#!/usr/bin/env python3
"""anonymize.py — physical-token guard at the write seam (SM.122)."""
from __future__ import annotations
import argparse, ipaddress, json, os, pwd, re, socket, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import envfile, locations
DMI = Path("/sys/class/dmi/id")
DMI_FILES = ("board_name", "board_serial", "board_vendor", "product_name",
             "product_serial", "product_uuid", "chassis_serial")
SECRETS_NODE = Path("nodes") / ".geometry" / "secrets.md"
CLASSES = ("hostname", "ip", "mac", "board", "secret", "home")
MIN_TOKEN = 4
#: ONE spelling of a home-directory path, ANY box (goal:g7.16.1.2.1): the
#: rotation-record writer rewrites it and the check (R3) reuses it. A BARE
#: home counts too (bundle 2 residue 46). The segment is a user name
#: ([\w-][\w.-]*: never a dot-dir), so `/home/,`, `/home/.cache/` and `/home/<seg>/`
#: never match; group 1 keeps the `/` or nothing. The roots are DERIVED
#: (SM residue 128: a home outside /home and /Users passed the gate): the two
#: conventional roots + the config cell `anonymize.home_roots` (path prefixes a
#: user-name segment follows) + this box's own login homes, from pwd and $HOME.
def _home_path_re(root=None):
    roots = ["/home/", "/Users/"]
    try:
        base = root or locations.find_project_root(Path(__file__).resolve().parent)
        cfg = locations.config_path(base) if base else None
        if cfg is not None and cfg.is_file():
            cell = json.loads(cfg.read_text(encoding="utf-8")).get("anonymize") or {}
            roots += [r for r in (cell.get("home_roots") or [])
                      if isinstance(r, str) and r.startswith("/") and len(r) > 1]
    except (OSError, ValueError, TypeError, AttributeError):
        pass  # an unreadable cell leaves the conventional roots
    dirs = {p.pw_dir.rstrip("/") for p in pwd.getpwall()
            if 1000 <= p.pw_uid < 65534}
    dirs.add((os.environ.get("HOME") or "").rstrip("/"))
    # a login home at depth >= 2 not already under a root: /, /nonexistent drop
    dirs = sorted((d for d in dirs if d.count("/") >= 2
                   and not d.startswith(tuple(roots))), key=len, reverse=True)
    alts = [re.escape(r) + r"[\w-][\w.-]*" for r in roots] + \
        [re.escape(d) + r"(?![\w.-])" for d in dirs]
    return re.compile("(?:" + "|".join(alts) + r")(/?)")
HOME_PATH_RE = _home_path_re()
def home_relative(text, home=None):
    """`text` with this box's HOME written `~` and any other box's home
    directory written `<home>/`: no home path survives, any box."""
    home = (os.path.expanduser("~") if home is None else home).rstrip("/")
    if len(home) > 1:
        text = re.sub(re.escape(home) + r"(?![\w.-])", "~", text)
    return HOME_PATH_RE.sub(r"<home>\1", text)
def _run(argv):
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return ""
    return p.stdout if p.returncode == 0 else ""
def _secret_tokens(root):
    from frontmatter import split_frontmatter
    import yaml
    keys = set()
    # `root` is whatever the caller was handed -- the installed hook passes
    # the SOURCE (repo) root, the tests pass a graph root. The secrets node
    # lives under the GRAPH root, so resolve it rather than assuming the two
    # are the same directory; assuming it made the hook check ZERO secret
    # values (goal:g15.29.16).
    graph = locations.shared_project_root(root) or locations.find_project_root(root)
    node = Path(graph or root) / SECRETS_NODE
    if node.is_file():
        parts = split_frontmatter(node.read_text(encoding="utf-8"))
        fm = (yaml.safe_load(parts[0]) if parts else None) or {}
        for f in ("required_keys", "optional_keys", "forbidden_keys"):
            keys.update(str(k) for k in (fm.get(f) or []))
        # `required_any` is a list of GROUPS; a key named only inside one is
        # still a key this node names, so its env value belongs in the denylist.
        for group in (fm.get("required_any") or []):
            if isinstance(group, list):
                keys.update(str(k) for k in group)
    env = envfile.read_env(envfile.resolve(root).env_file)
    return [("secret", env[k]) for k in keys if env.get(k)]
def box_tokens(root):
    """[(class, value)] of physical identifiers; a fake box under a fixture.

    The box user's home path is ENVIRONMENT, not hardware, so it rides both
    paths (goal:g7.16.1.1.3): a fixture box still has the caller's HOME.
    """
    home = [("home", os.environ.get("HOME") or "")]
    fixture = os.environ.get("AGI_ANONYMIZE_FIXTURE")
    if fixture:
        data = json.loads(Path(fixture).read_text(encoding="utf-8"))
        return [(c, str(v)) for c in CLASSES for v in data.get(c, [])] + home
    toks = [("hostname", socket.gethostname()), ("hostname", socket.getfqdn())]
    for line in (_run(["ip", "-o", "addr"]) + _run(["ip", "-o", "link"])).splitlines():
        m = re.search(r"inet6?\s+([0-9a-fA-F:.]+)", line)
        if m:
            addr = m.group(1)
            try:
                parsed = ipaddress.ip_address(addr)
            except ValueError:
                parsed = None
            # loopback/link-local are identical on every box, not identifiers
            if parsed is None or not (parsed.is_loopback or parsed.is_link_local):
                toks.append(("ip", addr))
        m = re.search(r"link/ether\s+([0-9a-fA-F:]{17})", line)
        if m:
            toks.append(("mac", m.group(1)))
    for f in DMI_FILES:
        try:
            v = (DMI / f).read_text(encoding="utf-8").strip()
        except OSError:
            continue
        if v:
            toks.append(("board", v))
    return toks + _secret_tokens(root) + home
def scan(text, tokens):
    """The CLASSES present in `text` — never a value. Beside the token list,
    ONE generic class: ANY box's home directory (HOME_PATH_RE, R1's
    definition) is `home`; the placeholders `<home>/`, `~/` never match."""
    hits = {c for c, v in tokens if len(v) >= MIN_TOKEN and v in text}
    if HOME_PATH_RE.search(text):
        hits.add("home")
    return sorted(hits)
def added_lines(text):
    """A unified diff -> what it ADDS: every '+' line inside a hunk (content
    starting '++' included) plus the post-image PATHS: '+++ b/', 'rename
    to'/'copy to', 'Binary files ... and b/<path> differ', and the 'diff
    --git' b/ side ONLY when 'new file mode' follows (a new empty or binary
    file prints no '+++'). Removed lines, pre-image paths and a deletion's
    header are text leaving the repo: a scrub must never refuse itself. Any
    other text is returned unchanged."""
    lines = text.splitlines()
    if not any(l.startswith(("@@", "diff --git")) for l in lines):
        return text
    out, hunk, head = [], False, ""
    for l in lines:
        if l.startswith("diff --git"):
            hunk, head = False, l.split(" b/", 1)[-1]
        elif l.startswith("@@"):
            hunk = True
        elif hunk:
            if l.startswith("+"):
                out.append(l[1:])
        elif l.startswith("+++ ") and l != "+++ /dev/null":
            out.append(l[4:])
        elif l.startswith(("rename to ", "copy to ")):
            out.append(l)
        elif l.startswith("new file mode"):
            out.append(head)
        elif l.startswith("Binary files ") and l.endswith(" differ"):
            post = l[:-len(" differ")].rsplit(" and ", 1)[-1]
            if post != "/dev/null":
                out.append(post)
    return "\n".join(out)
def cmd_check(root, text, diff_file):
    if diff_file:
        text = added_lines(Path(diff_file).read_text(encoding="utf-8"))
    elif text is None:
        text = added_lines(_run(["git", "-C", str(locations.source_root(root)),
                                 "diff", "--cached", "-U0"]))
    if locations.shared_project_root(root) is None:
        print("anonymize: no denylist source, skipped")
        return 0
    hits = scan(text or "", box_tokens(root))
    if hits:
        print("REFUSED: text carries " + ", ".join(hits) +
              " (a home path from ANY box, or a token read from this box)"
              " — write <home>/ or ~/, or use the box alias (SM.122)",
              file=sys.stderr)
        return 1
    print(f"anonymize: ok — no box-derived physical token in {len(text or '')} bytes")
    return 0
def cmd_install_hook(root, hooks_dir):
    if hooks_dir:
        hooks = Path(hooks_dir)
    else:
        src = locations.git_common_root(locations.source_root(root))
        hooks = src / ".git" / "hooks"
    dest = hooks / "pre-commit"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and "anonymize" not in dest.read_text(encoding="utf-8",
                                                          errors="replace"):
        print(f"REFUSED: {dest} exists and is not the anonymize hook",
              file=sys.stderr)
        return 1
    dest.write_text("#!/usr/bin/env bash\n# SM.122 box-local guard — never tracked.\n"
                    f"exec {sys.executable} {Path(__file__).resolve()} check --root "
                    f"{locations.source_root(root)}\n", encoding="utf-8")
    dest.chmod(0o755)
    print(f"installed anonymize pre-commit hook at {dest}")
    return 0
def main(argv=None):
    ap = argparse.ArgumentParser(description="SM.122 physical-token guard")
    ap.add_argument("verb", choices=["check", "install-hook"])
    for k in ("--root", "--text", "--diff-file", "--hooks-dir"):
        ap.add_argument(k)
    a = ap.parse_args(argv)
    root = Path(a.root) if a.root else locations.find_project_root()
    if root is None:
        print("no agi project found", file=sys.stderr)
        return 2
    if a.verb == "check":
        return cmd_check(root, a.text, a.diff_file)
    return cmd_install_hook(root, a.hooks_dir)
if __name__ == "__main__":
    sys.exit(main())
