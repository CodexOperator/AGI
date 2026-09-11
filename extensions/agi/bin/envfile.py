#!/usr/bin/env python3
"""Where this project's credentials live, and which keys it requires.

**The path is graph content, not a constant in a script (goal:g1.8, goal:g10.2).**
`nodes/.geometry/secrets.md` declares where the env file sits, where its
committed template sits, and which keys must, may, and must never appear in it.
This module is the one reader; `driver.sh` and `bin/env-get.sh` both go through
it rather than each spelling `.env` themselves.

That is the whole point of a geometry node: a filesystem fact stated once, in
the graph, versioned like every other thought — rather than a literal repeated
across a shell script, a Python script and a doc, which is the shape that
drifts. `[config]`'s schema said this type was waiting on "a code path that
reads more than one field"; this is that path, and it reads five.

## The asymmetry this exists to protect

    .env.example    committed, has a build node, has a grid ref     SHAPE
    .env            gitignored, mode 0600, never leaves the box     VALUE

Changing a value is invisible to git and to the grid **by construction**,
because a version history of a secret is a leak with a changelog. Changing the
shape — a key added, retired, or re-explained — lands in a tracked file and is
versioned like anything else. Neither half is a gap.

## CLI

    envfile.py --what env-file        # absolute path, or nothing if unresolvable
    envfile.py --what template        # absolute path to the committed shape
    envfile.py --check                # report missing/forbidden keys; exit 1 if bad
    envfile.py --json                 # everything resolved, machine-readable

`--check` never prints a value, only key names and lengths. Nothing in this
file writes to the env file: setting a secret is the one step that stays
manual, and it stays manual on purpose.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations  # noqa: E402

import yaml

#: Relative to the project root `locations.find_project_root` resolves — the
#: same `.geometry/` directory `crons.md` lives in, reached the same way.
SECRETS_NODE_REL = Path("nodes") / ".geometry" / "secrets.md"

#: Used when the node is absent. Deliberately the same values the node ships
#: with, so a project that has not minted one yet still resolves — but see
#: `Resolution.from_node`: the caller is told which of the two it got, because
#: "the graph said so" and "the fallback guessed" are not the same claim.
DEFAULT_ENV_FILE = "<source_root>/.env"
DEFAULT_TEMPLATE = "<source_root>/.env.example"

#: Keys that must never appear in an env file, whatever the node says. This is
#: not a policy this module invents — `dispatch.py` scrubs exactly these from
#: pi child environments so subagents cannot bill the interactive Claude Code
#: subscription. Setting one in `.env` re-adds that leak from *below* the
#: scrub, where nothing checks. Kept here as a floor so a project cannot drop
#: the protection by editing its own node.
ALWAYS_FORBIDDEN = (
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_BASE_URL",
)

#: Forbidden PRIVATE-KEY patterns (extensions/agi/bin/envfile.py). The seat-
#: keys layer (hypothesis:l4-a-seat-signs-with-a-swappable-scheme) writes
#: private seeds ONLY under sessions/seats -- never into .env -- and this
#: floor refuses a private-key line that lands here anyway. Stated as exact
#: regexes so the rule is reviewable:
#:
#:   * a KEY NAME whose final token is a private-key name -- suffix
#:     ``_PRIV_HEX`` (the exact cell envfile must refuse) or ``PRIVATE_KEY``:
#:         (?i).+_(?:PRIV_HEX)$     -- e.g. MY_SEAT_PRIV_HEX
#:         (?i).+PRIVATE_KEY$       -- e.g. SSH_PRIVATE_KEY
#:
#:   * a VALUE that is exactly 64 hex chars (the hex shape of a 32-byte
#:     Ed25519 seed) on a line whose KEY NAME mentions KEY:
#:         (?i)KEY                    -- the key name gate
#:         ^[0-9a-fA-F]{64}$          -- the value shape


#: Regex for a private-key KEY NAME (case-insensitive): the name ends in the
#: ``_PRIV_HEX`` or ``PRIVATE_KEY`` token.
_FORBIDDEN_KEY_NAME = re.compile(r".+_(?:PRIV_HEX)$|.+PRIVATE_KEY$",
                                 re.IGNORECASE)
#: Regex for the value shape of a hex-encoded 32-byte seed: exactly 64 hex.
_HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")
#: Key-name gate for the value rule: the name must mention KEY (so an
#: ordinary 64-hex config value under a non-KEY name is not refused).
_FORBIDDEN_KEY_MENTION = re.compile(r"(?i)KEY")


def _line_is_forbidden_key(key: str, value: str) -> bool:
    """True when a KEY=value line is a private-key that must never be in .env.

    Clause 1 (by name): the key ends in ``_PRIV_HEX`` or ``PRIVATE_KEY``.
    Clause 2 (by value): the value is exactly 64 hex chars AND the key name
    mentions KEY (a key containing KEY holding a hex seed). Never echoes the
    value; the caller reports only that the line is forbidden and which rule.
    """
    if _FORBIDDEN_KEY_NAME.search(key):
        return True
    if _FORBIDDEN_KEY_MENTION.search(key) and _HEX64.fullmatch(value or ""):
        return True
    return False


class SecretsError(Exception):
    """A problem with the node or the paths it declares.

    Raised, printed by `main()`, exit 1. Never swallowed: `goal:g1.5`'s whole
    complaint is that setup fails silently in both directions, so a resolver
    that quietly returns the wrong path is worse than one that refuses.
    """


# --- reading the node ---------------------------------------------------


def _parse_frontmatter(path: Path) -> dict:
    """Frontmatter as a dict. Same `split("---", 2)` shape as `crons.py`."""
    text = path.read_text(encoding="utf-8")
    if not text.strip().startswith("---"):
        raise SecretsError(f"{path}: no YAML frontmatter (expected a leading `---`)")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise SecretsError(f"{path}: unterminated frontmatter block (only one `---`)")
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        raise SecretsError(f"{path}: malformed YAML frontmatter — {exc}") from exc
    if not isinstance(fm, dict):
        raise SecretsError(f"{path}: frontmatter must be a YAML mapping")
    return fm


def _expand(template: str, root: Path) -> Path:
    """Substitute the `<...>` roots a geometry `path` is written in terms of.

    The schema is explicit that a declared `path` is a *shape*, never an
    absolute path — it ships with the engine and must not encode one machine's
    layout (goal:g8.2). So the node says `<source_root>/.env` and this is where
    that becomes a real path, asking `locations` rather than recomputing.
    """
    cfg = locations.load_config(root)
    subs = {
        "<source_root>": str(locations.source_root(root, cfg)),
        "<repo_root>": str(locations.repo_root(root)),
        "<graph_root>": str(root),
    }
    out = template
    for token, value in subs.items():
        out = out.replace(token, value)
    if "<" in out:
        raise SecretsError(
            f"unresolved placeholder in declared path {template!r} — "
            f"known tokens are {', '.join(sorted(subs))}"
        )
    return Path(out)


class Resolution:
    """Everything the node declares, resolved against one project root."""

    def __init__(self, root: Path, fm: dict | None, node_path: Path):
        self.root = Path(root)
        self.node_path = node_path
        self.from_node = fm is not None
        fm = fm or {}
        locs = fm.get("locations") or {}

        def _path_of(name: str, default: str) -> str:
            entry = locs.get(name) or {}
            declared = entry.get("path") if isinstance(entry, dict) else None
            return declared if isinstance(declared, str) and declared.strip() else default

        self.env_file = _expand(_path_of("env_file", DEFAULT_ENV_FILE), self.root)
        self.template = _expand(_path_of("env_template", DEFAULT_TEMPLATE), self.root)
        self.required_keys = [str(k) for k in (fm.get("required_keys") or [])]
        self.optional_keys = [str(k) for k in (fm.get("optional_keys") or [])]
        # The node may extend the floor; it can never lower it.
        declared_forbidden = [str(k) for k in (fm.get("forbidden_keys") or [])]
        self.forbidden_keys = sorted(set(declared_forbidden) | set(ALWAYS_FORBIDDEN))

    def as_dict(self) -> dict:
        return {
            "from_node": self.from_node,
            "node": str(self.node_path),
            "env_file": str(self.env_file),
            "env_file_exists": self.env_file.is_file(),
            "template": str(self.template),
            "template_exists": self.template.is_file(),
            "required_keys": self.required_keys,
            "optional_keys": self.optional_keys,
            "forbidden_keys": self.forbidden_keys,
        }


def resolve(start: Path | str | None = None) -> Resolution:
    """Resolve the secrets geometry for the project enclosing `start`.

    Anchored to the SHARED project root, never a per-worktree fork
    (`hypothesis:l3w4-branch-shared-state`). `.env` is gitignored and exists
    only in the main checkout, so a call from inside a `--branch` worktree
    (cwd `.agi/worktrees/<agent>`) must resolve the main checkout's `.env`
    through `git_common_root`, or the credential lookup is silently
    unrunnable -- the defect that blocked whole kids under `--branch`.
    `shared_project_root` is the identity in the main checkout, so
    non-worktree calls are unchanged.
    """
    root = locations.shared_project_root(start)
    if root is None:
        raise SecretsError(
            f"no agi project found from {start or os.getcwd()} — "
            f"nothing to resolve a secrets geometry against"
        )
    node_path = Path(root) / SECRETS_NODE_REL
    fm = _parse_frontmatter(node_path) if node_path.is_file() else None
    return Resolution(Path(root), fm, node_path)


# --- reading the env file, without ever printing a value -----------------


def read_env(path: Path) -> dict[str, str]:
    """Parse `KEY=value` lines. Not a shell: no expansion, no substitution.

    Deliberately more restrictive than `source`-ing the file, because this
    parser's output is only ever used to answer "is this key set", never to
    build an environment. `driver.sh` still sources the real file for that, so
    a project that needs shell syntax there keeps it.
    """
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export "):].lstrip()
        key, _, value = line.partition("=")
        key = key.strip()
        if not key:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        out[key] = value
    return out


# --- credential validity (hypothesis:l4-a-check-that-answers-a-
# question-it-is-not-asking, ITEM 1): presence is not usability ------------
#
# `--check` used to assert only that a required key NAME is present (non-empty)
# and then print "ok". That answers "did the key land?" and never "is this key
# usable?". The owner revoked a key that `--check` still called ok. This adds
# ONE authenticated call that distinguishes PRESENT from USABLE:
#   - provider returns HTTP 401/403  -> the key is DEAD (fail-closed, a problem)
#   - provider returns HTTP 200      -> the key is VALID (a note)
#   - network error / timeout / 5xx  -> UNKNOWN (fail-open, a note, never dead)
# A 401 is evidence the credential is dead; an unreachable API is evidence of
# nothing. Conflating them turns a guard into an outage, so they are reported
# differently. The verifier is a module-level function so tests can stub it
# without touching the network; `--check` is the only caller that asks for
# verification, so the plain form `driver.sh` calls every pass stays offline.


def _provider_for(key: str) -> tuple[str | None, str]:
    """Map a key VALUE to (provider, provider_key_name).

    Never prints or returns the value itself. Returns `(None, reason)` when
    the value does not name a provider we can validate, so an unknown key
    shape is reported as UNKNOWN, never as valid and never as dead.
    """
    if key.startswith("sk-or-"):
        return ("openrouter", "OPENROUTER_API_KEY")
    return (None, "no verifier for this key's prefix")


def _verify_openrouter(key: str, timeout: float = 5.0) -> tuple[str, str]:
    """One authenticated call to OpenRouter's key endpoint.

    Returns `(status, detail)` with status one of `"valid"`, `"dead"`, or
    `"unknown"`. Fail-closed on an explicit 401/403; fail-open on anything
    that is not a credential verdict (timeout, URLError, 5xx).
    """
    import urllib.error
    import urllib.request

    def _req(url: str) -> tuple[int, str]:
        r = urllib.request.Request(
            url, headers={"Authorization": f"Bearer {key}"}
        )
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            return resp.status, resp.read(512).decode("utf-8", "replace")

    try:
        code, _body = _req("https://openrouter.ai/api/v1/key")
        if code == 200:
            return ("valid", f"provider accepted it (HTTP {code})")
        if code in (401, 403):
            return ("dead", f"provider rejected it (HTTP {code})")
        return ("unknown", f"provider returned HTTP {code}")
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            return ("dead", f"provider rejected it (HTTP {exc.code})")
        return ("unknown", f"provider returned HTTP {exc.code}")
    except Exception as exc:  # URLError, TimeoutError, socket errors -- no verdict
        return ("unknown", f"could not reach the provider ({type(exc).__name__})")


_VERIFIERS = {"openrouter": _verify_openrouter}


def _verify_provider_key(key: str) -> tuple[str, str]:
    """Validate one key value. `(status, detail)`, status in
    `valid | dead | unknown`. Module-level so tests can substitute it."""
    provider, reason = _provider_for(key)
    if provider is None:
        return ("unknown", reason)
    fn = _VERIFIERS.get(provider)
    if fn is None:
        return ("unknown", f"no verifier registered for {provider}")
    return fn(key)


def set_key(res: "Resolution", name: str) -> int:
    """Read one secret from the terminal and write it into the env file.

    The value never appears in argv, in shell history, on screen, or in this
    process's output -- `getpass` reads it straight from the tty. That is the
    whole point: a secret pasted onto a command line is a secret in
    `~/.bash_history`, in `ps`, and in any recording of the terminal, which
    matters here because this box is about to be livestreamed.

    Every existing line for `name` is replaced, not appended to. A duplicated
    key in a `.env` is a real hazard rather than an untidiness: which value
    wins depends on the parser, and this repo's own file carried
    OPENROUTER_API_KEY twice before this verb existed.
    """
    import getpass
    import os
    import tempfile

    path = Path(res.env_file)
    if not sys.stdin.isatty():
        print("ERR: --set reads the value from a terminal, and stdin is not one.\n"
              "     Run it from an interactive ssh session. Never pipe a secret in:\n"
              "     a piped secret is a secret in your shell history.",
              file=sys.stderr)
        return 1

    value = getpass.getpass(f"paste value for {name} (input hidden): ").strip()
    if not value:
        print("ERR: empty value; nothing written.", file=sys.stderr)
        return 1
    again = getpass.getpass("paste it once more to confirm: ").strip()
    if value != again:
        print("ERR: the two entries differ; nothing written.", file=sys.stderr)
        return 1

    existing = path.read_text(encoding="utf-8").splitlines() if path.is_file() else []
    out: list[str] = []
    replaced = 0
    for raw in existing:
        line = raw.strip()
        candidate = line[len("export "):].lstrip() if line.startswith("export ") else line
        key = candidate.partition("=")[0].strip() if "=" in candidate else ""
        if key == name:
            replaced += 1
            if replaced == 1:
                out.append(f"{name}={value}")
            continue
        out.append(raw)
    if replaced == 0:
        out.append(f"{name}={value}")

    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".env.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write("\n".join(out).rstrip("\n") + "\n")
        os.chmod(tmp, 0o600)
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise

    where = "replaced" if replaced else "added"
    dupes = f", dropped {replaced - 1} duplicate line(s)" if replaced > 1 else ""
    print(f"[secrets] {where} {name} in {path} ({len(value)} chars{dupes}); mode 0600")
    print("[secrets] the value was not printed and is not in your shell history.")
    return 0


def check(res: Resolution, verify: bool = False) -> tuple[list[str], list[str]]:
    """`(problems, notes)` — neither ever contains a secret value.

    Problems fail `--check`; notes are worth saying but are not failures.

    When `verify` is true, each present required key is subjected to ONE
    authenticated call (see the validity section above): a dead key becomes a
    PROBLEM, a network failure becomes an UNKNOWN note, and a live key a note.
    Kept off by default so the plain form `driver.sh` calls every pass stays
    offline; only `--check` asks for validation.
    """
    problems: list[str] = []
    notes: list[str] = []

    if not res.from_node:
        notes.append(
            f"no secrets node at {res.node_path} — using built-in defaults. "
            f"Mint one so the path is graph content (goal:g10.2)."
        )
    if not res.template.is_file():
        notes.append(f"no template at {res.template} — the shape is undeclared")

    if not res.env_file.is_file():
        problems.append(
            f"missing {res.env_file} — copy {res.template.name} to it, "
            f"chmod 600, and fill in: {', '.join(res.required_keys) or '(no keys declared)'}"
        )
        return problems, notes

    mode = stat.S_IMODE(res.env_file.stat().st_mode)
    if mode != 0o600:
        notes.append(f"{res.env_file} is mode {mode:03o}, expected 600 — chmod 600 it")

    env = read_env(res.env_file)
    for key in res.required_keys:
        value = env.get(key, "")
        if not value:
            problems.append(f"{key} is missing or empty in {res.env_file}")
    if verify:
        for key in res.required_keys:
            value = env.get(key, "")
            if not value or not value.strip():
                continue  # already reported missing/empty above
            status, detail = _verify_provider_key(value)
            if status == "dead":
                problems.append(
                    f"{key} is present but NOT USABLE — {detail}. Presence is not "
                    f"validity: the file says it is there, the provider refuses it."
                )
            elif status == "unknown":
                notes.append(
                    f"{key}: could not be verified ({detail}) — treated as present, "
                    f"not confirmed usable"
                )
            else:
                notes.append(f"{key}: validated against the provider ({detail})")
    # Optional keys are reported as PRESENT/absent, never as problems, and
    # never by value -- the name and the length are enough to answer "did the
    # key I just wrote land?" without putting a secret on a terminal that is
    # very likely being screen-shared or logged. `OPENROUTER_PROVISIONING_KEY`
    # is the case this was added for (goal:g1.11): it is optional by design, so
    # `--check` said nothing about it and there was no way to confirm a write
    # short of reading the file.
    for key in res.optional_keys:
        value = env.get(key, "")
        if value:
            notes.append(f"{key} is set ({len(value)} chars)")
        else:
            notes.append(f"{key} is not set (optional)")

    for key in res.forbidden_keys:
        if env.get(key):
            problems.append(
                f"{key} is set in {res.env_file} and must never be — dispatch.py "
                f"scrubs it from pi children so subagents cannot bill the Claude "
                f"Code subscription; setting it here re-adds the leak below the scrub"
            )

    # Private-key pattern floor (hypothesis:l4-a-seat-signs-with-a-swappable-
    # scheme, clause (2)): a NAME ending in _PRIV_HEX / PRIVATE_KEY, or a
    # 64-hex VALUE under a KEY-mentioning name. Reported by which rule, never
    # by value -- a secret must never reach a logged/screen-shared terminal.
    for key, value in env.items():
        if _line_is_forbidden_key(key, value):
            rule = ("key name"
                    if _FORBIDDEN_KEY_NAME.search(key)
                    else "64-hex value under a KEY-named key")
            problems.append(
                f"{key} is set in {res.env_file} and looks like a PRIVATE KEY "
                f"({rule}) — private seeds belong in sessions/seats, never "
                f"in .env. Refused by the envfile.py forbidden-key floor."
            )
    return problems, notes


# --- cli ----------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Resolve and check this project's secret file (goal:g1.8).")
    ap.add_argument("start", nargs="?", default=None,
                    help="directory to resolve from (default: cwd)")
    ap.add_argument("--what", choices=["env-file", "template", "node"],
                    help="print one path and nothing else")
    ap.add_argument("--check", action="store_true",
                    help="report missing or forbidden keys; exit 1 on a problem")
    ap.add_argument("--json", action="store_true", help="emit the whole resolution")
    ap.add_argument("--set", metavar="NAME",
                    help="prompt on the terminal for NAME's value and write it "
                         "into the env file, replacing any existing lines for "
                         "it; the value is never echoed, never in argv, never "
                         "in shell history")
    args = ap.parse_args(argv)

    try:
        res = resolve(args.start)
    except SecretsError as exc:
        print(f"ERR: {exc}", file=sys.stderr)
        return 1

    if args.set:
        return set_key(res, args.set)

    if args.what:
        print({"env-file": res.env_file, "template": res.template,
               "node": res.node_path}[args.what])
        return 0

    if args.json:
        print(json.dumps(res.as_dict(), indent=2))
        return 0

    problems, notes = check(res, verify=args.check)
    for note in notes:
        print(f"[secrets] note: {note}")
    for problem in problems:
        print(f"[secrets] PROBLEM: {problem}", file=sys.stderr)
    if not problems:
        keys = ", ".join(res.required_keys) or "(none declared)"
        print(f"[secrets] ok: {res.env_file} satisfies required keys: {keys}")
    return 1 if problems and args.check else 0


if __name__ == "__main__":
    raise SystemExit(main())
