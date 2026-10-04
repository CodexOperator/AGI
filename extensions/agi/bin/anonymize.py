#!/usr/bin/env python3
"""anonymize.py — physical-token guard at the write seam (SM.122)."""
from __future__ import annotations
import argparse, functools, ipaddress, json, os, pwd, re, socket, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import envfile, locations
DMI = Path("/sys/class/dmi/id")
DMI_FILES = ("board_name", "board_serial", "board_vendor", "product_name",
             "product_serial", "product_uuid", "chassis_serial")
SECRETS_NODE = Path("nodes") / ".geometry" / "secrets.md"
CLASSES = ("hostname", "ip", "mac", "board", "secret", "home", "email", "hardware")
#: CLASSES with NO token source: `scan()` judges them by pattern, so
#: box_tokens() can never carry one. A "every class reached" row subtracts
#: THIS constant rather than naming a class (dg6-04 residue 5).
SCAN_ONLY_CLASSES = ("email",)
MIN_TOKEN = 4
#: ONE spelling of a home-directory path, ANY box (goal:g7.16.1.2.1): the
#: rotation-record writer rewrites it and the check (R3) reuses it. A BARE
#: home counts too (bundle 2 residue 46). The segment is a user name
#: ([\w-][\w.-]*: never a dot-dir), so `/home/,`, `/home/.cache/` and `/home/<seg>/`
#: never match; group 1 keeps the `/` or nothing. The roots are DERIVED
#: (SM residue 128: a home outside /home and /Users passed the gate): the two
#: conventional roots + the config cell `anonymize.home_roots` (path prefixes a
#: user-name segment follows) + this box's own login homes, from pwd and $HOME.
@functools.lru_cache(maxsize=None)   # once per PROCESS, not once per string leaf
def _project(start):
    return locations.find_project_root(Path(start).resolve())


def _anonymize_cell(root=None, live=False):
    """THE ONE `anonymize` cell read: home_roots, hardware and user_roots. No
    `root` reads NO cell -- a caller that never named a project never gets this
    repo's -- unless `live` (the import-time HOME_PATH_RE) asks for it."""
    if not root and not live:
        return {}
    try:
        base = _project(root or Path(__file__).resolve().parent)
        cfg = locations.config_path(base) if base else None
        if cfg is not None and cfg.is_file():
            cell = json.loads(cfg.read_text(encoding="utf-8")).get("anonymize") or {}
            if isinstance(cell, dict):
                return cell
    except (OSError, ValueError, TypeError, AttributeError):
        pass  # an unreadable cell leaves every rule at its conventional default
    return {}
def _prefix_roots(cell, key):
    return [r for r in (cell.get(key) or [])
            if isinstance(r, str) and r.startswith("/") and len(r) > 1]
def _root_prefix_re(roots):
    r"""`prefix` + ONE user-name segment (`[\w-][\w.-]*`, so `<user>` never
    matches) -- the builder the home cell and the user_roots cell share."""
    if not roots:
        return None
    return re.compile("(?:" + "|".join(re.escape(r) + r"[\w-][\w.-]*"
                                        for r in roots) + ")")
def _user_path_re(root=None):
    return _root_prefix_re(_prefix_roots(_anonymize_cell(root), "user_roots"))
def _home_path_re(root=None):
    roots = ["/home/", "/Users/"] + _prefix_roots(
        _anonymize_cell(root, live=True), "home_roots")
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
#: ONE spelling of an email address (goal:g1.31.5.1.2). The non-personal shapes
#: that may appear (reserved example domains, key-type names, systemd units) are
#: the config cell `anonymize.email_allow`: a list of regexes, each FULL-matched
#: (case-insensitive) against one address. No cell = nothing allowed.
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
def _email_allow(root=None):
    out = []
    try:
        base = _project(root or Path(__file__).resolve().parent)
        cfg = locations.config_path(base) if base else None
        if cfg is not None and cfg.is_file():
            cell = json.loads(cfg.read_text(encoding="utf-8")).get("anonymize") or {}
            for r in cell.get("email_allow") or []:
                if isinstance(r, str) and r:
                    out.append(re.compile(r, re.IGNORECASE))
    except (OSError, ValueError, TypeError, AttributeError, re.error):
        pass  # an unreadable cell allows nothing: fail closed
    return out
#: the public spelling of `_email_allow`, for readers outside this module
#: (reds.py's range gate -- the cell, never a copy of the rule).
email_allow = _email_allow
def has_email(text, allow=None):
    """True when `text` carries an address that no `email_allow` entry covers."""
    allow = _email_allow() if allow is None else allow
    return any(not any(a.fullmatch(m.group(0)) for a in allow)
               for m in EMAIL_RE.finditer(text))
def home_relative(text, home=None, root=None):
    """`text` with this box's HOME written `~` and any other box's home
    directory written `<home>/`: no home path survives, any box. Given a
    `root`, the user segment after an `anonymize.user_roots` prefix is written
    `<user>` too -- the ONLY substitutions this makes; nothing rewrites a
    `hardware` fragment."""
    home = (os.path.expanduser("~") if home is None else home).rstrip("/")
    if len(home) > 1:
        text = re.sub(re.escape(home) + r"(?![\w.-])", "~", text)
    text = HOME_PATH_RE.sub(r"<home>\1", text)
    for pre in _prefix_roots(_anonymize_cell(root), "user_roots"):
        text = re.sub(re.escape(pre) + r"[\w-][\w.-]*",
                      lambda m, pre=pre: pre + "<user>", text)
    return text
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
    rule = _anonymize_cell(root).get("hardware") or {}
    rule = rule if isinstance(rule, dict) else {}
    fixture = os.environ.get("AGI_ANONYMIZE_FIXTURE")
    if fixture:
        data = json.loads(Path(fixture).read_text(encoding="utf-8"))
        plain = [(c, str(v)) for c in CLASSES if c != "hardware"
                 for v in data.get(c, [])]
        return plain + _hw_tokens(data.get("hardware", []), rule) + home
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
    return toks + _hw_tokens(_hw_source_names(rule), rule) + \
        _secret_tokens(root) + home
#: the raw-tool shims (SM.122): hardware facts come from `shims/<tool>`, never
#: the raw tool off PATH; an absent shim is an absent source.
SHIMS = Path(__file__).resolve().parents[1] / "shims"
_HW_CACHE = {}  # per process: the cell's sources -> the names they yielded
def _hw_source_names(rule):
    """Names read LIVE, once per process, from the cell's sources: an argv
    source runs that tool's SHIM (one name per line), a `@path` source reads
    that file's `field:` lines."""
    key = json.dumps(rule.get("sources") or [], sort_keys=True, default=str)
    if key not in _HW_CACHE:
        _HW_CACHE[key] = _read_hw_sources(rule)
    return list(_HW_CACHE[key])
def _read_hw_sources(rule):
    names = []
    for src in rule.get("sources") or []:
        if not (isinstance(src, list) and src and isinstance(src[0], str)):
            continue
        if not src[0].startswith("@"):
            shim = SHIMS / Path(src[0]).name
            if shim.is_file():
                names += [ln.strip() for ln in
                          _run([str(shim), *map(str, src[1:])]).splitlines()
                          if ln.strip()]
            continue
        field = src[1] if len(src) > 1 and isinstance(src[1], str) else ""
        try:
            lines = Path(src[0][1:]).read_text(encoding="utf-8",
                                               errors="replace").splitlines()
        except OSError:
            continue
        picked = [ln.split(":", 1)[1].strip() for ln in lines
                  if ln.lower().startswith(field.lower() + ":")]
        # ONE bare value line, and only from a file with NO colon line at all:
        # a MIXED file is keyed, not bare (dh347)
        bare = [ln.strip() for ln in lines if ln.strip() and ":" not in ln]
        names += picked or (bare[:1] if bare and
                            not any(":" in ln for ln in lines) else [])
    return names
def _hw_fragments(name, min_words, core_digits):
    """NAME -> every run of >= min_words consecutive words holding a word of
    >= core_digits digits: a 2-word FRAGMENT of a model name is the leak."""
    words = re.findall(r"[A-Za-z0-9]+", str(name))
    return [" ".join(run)
            for i in range(len(words))
            for j in range(i + min_words, len(words) + 1)
            for run in [words[i:j]]
            if any(w.isdigit() and len(w) >= core_digits for w in run)]
def _hw_tokens(names, rule):
    """(class, fragment) pairs; the cell carries the RULE, never a name."""
    min_words = int(rule.get("min_words") or 2)
    core_digits = int(rule.get("core_digits") or 3)
    return [("hardware", f) for n in names or []
            for f in _hw_fragments(n, min_words, core_digits)]
def _hw_frag_re(fragments):
    r"""Fragments case-insensitive, words joined by `[\s_-]+` and bounded, so
    a class label (`GPU9990U`) and a bare number never match."""
    alts = [r"[\s_-]+".join(re.escape(w) for w in f.split()) for f in fragments]
    return re.compile(r"(?<![\w-])(?:" + "|".join(alts) + r")(?![\w-])", re.I)
def scan(text, tokens, email_allow=None, root=None):
    """The CLASSES present in `text` — never a value. Beside the token list,
    TWO generic classes: ANY box's home directory (HOME_PATH_RE, R1's
    definition) is `home`, placeholders `<home>/`, `~/` never match; and a path
    prefix a user-name segment follows OUTSIDE a home (`anonymize.user_roots`)
    is `user`."""
    hits = {c for c, v in tokens
            if c != "hardware" and len(v) >= MIN_TOKEN and v in text}
    frags = [v for c, v in tokens if c == "hardware" and len(v) >= MIN_TOKEN]
    if frags and _hw_frag_re(frags).search(text):
        hits.add("hardware")
    if HOME_PATH_RE.search(text):
        hits.add("home")
    if has_email(text, email_allow):
        hits.add("email")
    # user_roots is kept OUT of HOME_PATH_RE: the committed-bytes home test
    # keeps its scope
    user = _user_path_re(root)
    if user is not None and user.search(text):
        hits.add("user")
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
#: what a refused writer is told, per class -- only what the code substitutes:
#: home_relative() rewrites `home` and (given the root) `user`; nothing rewrites
#: `hardware` or `email`, so those say so.
ADVICE = {
    "home": "write <home>/ or ~/ (anonymize.home_relative does it)",
    "user": "write the user segment as <user> (anonymize.home_relative(text, root=ROOT) does it)",
    "hardware": "name the part by class, never its model (nothing rewrites it: edit by hand)",
    "email": "write <email> (nothing rewrites it: edit by hand)",
}
def cmd_check(root, text, diff_file):
    if diff_file:
        text = added_lines(Path(diff_file).read_text(encoding="utf-8"))
    elif text is None:
        text = added_lines(_run(["git", "-C", str(locations.source_root(root)),
                                 "diff", "--cached", "-U0"]))
    if locations.shared_project_root(root) is None:
        print("anonymize: no denylist source, skipped")
        return 0
    hits = scan(text or "", box_tokens(root), _email_allow(root), root)
    if hits:
        print("REFUSED: text carries " + ", ".join(hits) +
              " (a home path from ANY box, an email address, or a token read from this box)"
              " — " + "; ".join(ADVICE[c] for c in hits if c in ADVICE) +
              "; or use the box alias (SM.122)", file=sys.stderr)
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
