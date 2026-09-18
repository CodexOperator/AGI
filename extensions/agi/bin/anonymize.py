#!/usr/bin/env python3
"""anonymize.py — physical-token guard at the write seam (SM.122)."""
from __future__ import annotations
import argparse, json, os, re, socket, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import envfile, locations
DMI = Path("/sys/class/dmi/id")
DMI_FILES = ("board_name", "board_serial", "board_vendor", "product_name",
             "product_serial", "product_uuid", "chassis_serial")
SECRETS_NODE = Path("nodes") / ".geometry" / "secrets.md"
CLASSES = ("hostname", "ip", "mac", "board", "secret")
MIN_TOKEN = 4
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
    node = Path(root) / SECRETS_NODE
    if node.is_file():
        parts = split_frontmatter(node.read_text(encoding="utf-8"))
        fm = (yaml.safe_load(parts[0]) if parts else None) or {}
        for f in ("required_keys", "optional_keys", "forbidden_keys"):
            keys.update(str(k) for k in (fm.get(f) or []))
    env = envfile.read_env(envfile.resolve(root).env_file)
    return [("secret", env[k]) for k in keys if env.get(k)]
def box_tokens(root):
    """[(class, value)] of physical identifiers; a fake box under a fixture."""
    fixture = os.environ.get("AGI_ANONYMIZE_FIXTURE")
    if fixture:
        data = json.loads(Path(fixture).read_text(encoding="utf-8"))
        return [(c, str(v)) for c in CLASSES for v in data.get(c, [])]
    toks = [("hostname", socket.gethostname()), ("hostname", socket.getfqdn())]
    for line in (_run(["ip", "-o", "addr"]) + _run(["ip", "-o", "link"])).splitlines():
        m = re.search(r"inet6?\s+([0-9a-fA-F:.]+)", line)
        if m:
            toks.append(("ip", m.group(1)))
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
    return toks + _secret_tokens(root)
def scan(text, tokens):
    """The CLASSES present in `text` — never a value."""
    return sorted({c for c, v in tokens if len(v) >= MIN_TOKEN and v in text})
def cmd_check(root, text, diff_file):
    if diff_file:
        text = Path(diff_file).read_text(encoding="utf-8")
    elif text is None:
        text = _run(["git", "-C", str(locations.source_root(root)),
                     "diff", "--cached", "-U0"])
    hits = scan(text or "", box_tokens(root))
    if hits:
        print("REFUSED: text carries " + ", ".join(hits) +
              " token(s) read from this box — use the box alias (SM.122)",
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
