#!/usr/bin/env python3
"""boxes.py — which BOX a checkout is, and whether a posts row belongs to it.

A "box" is a machine (or clone) that runs its own crontab and its own seats.
A `config:posts` row may carry a `box` cell naming whose box its `pid`/`window`
cells are true of; a row without the cell belongs to the graph's default box.
`AGI_BOX` in the resolved env names THIS box (box-local by construction); unset
falls back to the `default_box` cell on the posts node.

This is a DIFFERENT `box` from `rotate.py`'s `_box_fact()` (a machine load
snapshot `{loadavg, cores}` stored under `rec["box"]` in rotation records).
Same word, unrelated meanings, different places — do not merge them.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

class BoxSchemaError(ValueError):
    """A graph whose `[box].md` cannot declare what this reader needs."""


# The engine's OWN [box].md: fallback for a graph with none of its own.
_ENGINE_BOX_SCHEMA = (Path(__file__).resolve().parents[3] / ".agi" /
                      "context" / "schemas" / "[box].md")
# A bare `{token}` absent from the map is a stray; a shell `$`-reference
# (`${PATH}`, `${VAR:-x}`) is legal syntax and must never be convicted.
_STRAY_TOKEN = re.compile(r"(?<!\$)\{[A-Za-z_][A-Za-z0-9_]*\}")


def graph_root(root: Path) -> Path:
    """`root` itself when it IS a graph, else the nearest enclosing graph.

    Every other reader in the tree resolves its root with locations.py; this
    one did not, so a REPO root read an EMPTY cell set silently -- the exact
    render `resolve_placeholders` refuses to produce. `root` is returned
    unchanged when it already holds a config, and when nothing is found, so
    an existing caller sees no change.
    """
    start = Path(root).resolve()
    if (start / "config.json").is_file():
        return start
    import locations
    found = locations.find_project_root(start)
    return Path(found).resolve() if found else start


def box_schema_path(root: Path) -> Path:
    """The one declaration: context/schemas/[box].md under the graph root."""
    return graph_root(root) / "context" / "schemas" / "[box].md"


def _schema_at(p: Path) -> dict:
    """Parsed frontmatter of the `[box].md` at `p`; {} when `p` is absent."""
    import frontmatter, yaml
    parts = frontmatter.split_frontmatter(p.read_text(encoding="utf-8")) if p.is_file() else None
    return (yaml.safe_load(parts[0]) or {}) if parts else {}


def _box_schema(root: Path) -> dict:
    """Parsed frontmatter of context/schemas/[box].md -- the one declaration."""
    return _schema_at(box_schema_path(root))


def require_box_cells(root: Path) -> tuple[str, ...]:
    """The declared cell names, or refuse naming `[box].md`.

    An absent `[box].md` (or one declaring no `fields`) used to read as an
    empty cell set, hiding the audit's silence. Fail closed instead.
    """
    names = box_cell_names(root)
    if not names:
        raise BoxSchemaError(
            f"{box_schema_path(root)} declares no box cells "
            f"(absent, or no `fields:` map)")
    return names


def _box(root: Path) -> dict:
    try:
        data = json.loads((graph_root(root) / "config.json").read_text(encoding="utf-8"))
        return data.get("box") or {}
    except Exception:  # noqa: BLE001 -- absent/unreadable config: no cells
        return {}


def box_cell_names(root: Path) -> tuple[str, ...]:
    """The cell names from the `fields` mapping in [box].md -- the one declaration."""
    return tuple((_box_schema(root).get("fields") or {}).keys())


def box_cells(root: Path) -> dict:
    """The `box` cells true of this box: root, logs_dir, tmux_session, user."""
    box = _box(root)
    return {k: str(box.get(k) or "") for k in box_cell_names(root)}


def allow_paths(root: Path) -> list[str]:
    """The declaring config plus every `box.allow` entry, from the cells."""
    return ["config.json"] + [str(x) for x in (_box(root).get("allow") or [])]


def scan_prefixes(root: Path) -> list[str]:
    """The `box.scan` cell: path prefixes (repo-relative) the whole-repo audit reads.
    Empty = every tracked file. A record under `.agi/sessions` or `datasets/` is
    generated on this box and never copied to another, so it is not scanned."""
    return [str(x) for x in (_box(root).get("scan") or [])]


def resolve_placeholders(text: str, cells: dict, root: Path) -> str:
    """Substitute `{token}` from `cells` using the mapping declared in [box].md.

    The declaration is the graph's own `[box].md`; a graph with NO schema
    falls back to the engine's own. A PRESENT schema without a `placeholders:`
    map, a missing or EMPTY cell, or an undeclared `{token}` each refuse by name.
    """
    p = box_schema_path(root)
    if not p.is_file() and _ENGINE_BOX_SCHEMA.is_file():
        p = _ENGINE_BOX_SCHEMA
    mapping = _schema_at(p).get("placeholders")
    if not mapping:
        raise BoxSchemaError(f"{p} declares no `placeholders:` map")
    for name, key in mapping.items():
        token = "{" + name + "}"
        if token not in text:
            continue
        if key not in (cells or {}):
            raise BoxSchemaError(
                f"{p}: placeholder {token} maps to cell `{key}`, which this "
                f"caller did not supply")
        value = str(cells[key])
        if not value.strip():
            raise BoxSchemaError(
                f"{p}: placeholder {token} maps to cell `{key}`, which this "
                f"caller supplied EMPTY -- an empty render is the bug this "
                f"resolver exists to prevent")
        text = text.replace(token, value)
    stray = _STRAY_TOKEN.search(text)
    if stray:
        raise BoxSchemaError(
            f"{p}: `{stray.group(0)}` is not declared in `placeholders:`")
    return text


def default_box(root: Path) -> str:
    """The `default_box` cell on the config:posts node; '' when undeclared."""
    import frontmatter
    import yaml
    path = Path(root) / "nodes" / ".geometry" / "posts.md"
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    parted = frontmatter.split_frontmatter(text)
    if not parted:
        return ""
    fm = yaml.safe_load(parted[0]) or {}
    return str(fm.get("default_box") or "").strip()


def this_box(root: Path) -> str:
    """AGI_BOX from the resolved env, else the box's own env file.

    NO `default_box` fallback: that cell is the posts node's DOCUMENTATION of
    its home box, never a locality fallback. An unset AGI_BOX REFUSES -- a
    silent default read every boxless row as `core-town` and so as foreign
    (hypothesis:every-live-row-carries-its-own-box-and-an-unset-box-is-
    refused, belam 00:35Z 09-27).
    """
    import envfile
    val = os.environ.get("AGI_BOX", "").strip()
    if not val:
        val = envfile.read_env(envfile.resolve(root).env_file).get("AGI_BOX", "").strip()
    if not val:
        raise RuntimeError(
            f"no AGI_BOX in the env and none in the box env file under "
            f"{root} — this graph cannot say which box it is (`default_box` "
            f"is documentation, never a fallback)"
        )
    return val


def row_is_local(root: Path, row: dict) -> bool:
    """True when `row` NAMES this box on its own `box` cell.

    An EMPTY or UNKNOWN row box is NOT local on any DECLARED box and
    `'(default)'` is never a match. The ONE retained fail-open: a graph that
    declares no box AT ALL stays a single-box graph (a dev graph must not go
    dark), but a row that DOES name a box there is foreign -- unprovable.
    """
    own = str((row or {}).get("box") or "").strip()
    try:
        here = this_box(root)
    except Exception:  # noqa: BLE001 -- an undeclared box proves nothing
        return not own
    return bool(own) and own == here

if __name__ == "__main__":
    import argparse
    argparse.ArgumentParser(description=__doc__.splitlines()[0]).parse_args()


# --- AA1: geometry `box` CLI invoke (no box_mail / no send.py) -----------------
# Mail is git-ref `box`; keygen recovery is agi-out fresh+restart.

KEYGEN_LINE = (
    "touch ~/.fresh && systemctl restart agi-post@{seat}.service  "
    "# agi-out does out-line keygen; never send.py"
)
PRIME = "belam"
WHOIS_NOT_AUTHORIZED = 2  # send.WHOIS_NOT_AUTHORIZED
SEAT_KEY_MODE = 0o600


class BoxSendError(RuntimeError):
    pass


def comms_root(root: Path, override=None) -> Path:
    if override:
        return Path(override)
    return Path(root) / "comms"


def _box_bin() -> str:
    import os
    home = os.environ.get("HOME", "")
    cand = Path(home) / "bin" / "box"
    if cand.is_file():
        return str(cand)
    post = os.environ.get("AGI_POST", "")
    if post:
        p = Path(f"/var/lib/agi/{post}/bin/box")
        if p.is_file():
            return str(p)
    return "box"


def _box_env(sender: str) -> dict:
    import os
    env = os.environ.copy()
    env["AGI_POST"] = sender
    env.setdefault(
        "AGI_TRUNK",
        os.environ.get("AGI_TRUNK", "core/season2/et-grok-pilot"),
    )
    return env


def box_send(root, to: str, text: str, sender: str | None = None, **_kw) -> None:
    """Send via geometry `box send TO` (stdin = body)."""
    import os
    import subprocess
    sender = sender or os.environ.get("AGI_POST") or PRIME
    cwd = Path(root)
    if cwd.name == ".agi":
        cwd = cwd.parent
    proc = subprocess.run(
        [_box_bin(), "send", to],
        input=text if text.endswith("\n") else text + "\n",
        text=True,
        capture_output=True,
        env=_box_env(sender),
        cwd=str(cwd),
    )
    if proc.returncode != 0:
        raise BoxSendError(
            (proc.stderr or "").strip() or f"box send failed rc={proc.returncode}"
        )


# Inbox/DM/room/wake stay on deprecated send (conversation channel SoT).
# Geometry git-ref mail is box_send above — do NOT route inbox through box CLI.
def send(root, to: str, text: str, sender: str | None = None, **kw) -> None:
    return _deprecated_send().send(root, to, text, sender=sender, **kw)


def send_dm(croot, me: str, other: str, text: str, sender: str | None = None, **kw):
    return _deprecated_send().send_dm(croot, me, other, text, sender, **kw)


def send_room(croot, room: str, text: str, sender: str | None = None, **kw) -> None:
    return _deprecated_send().send_room(croot, room, text, sender=sender, **kw)


def wake(root, seat: str) -> None:
    return _deprecated_send().wake(root, seat)


def rewind_read_cursors(*_a, **_k):
    return []


def _locally_loaded_rows(root) -> list:
    return _deprecated_send()._locally_loaded_rows(root)


def _resolve_rows(rows, ref, claim=None):
    return _deprecated_send()._resolve_rows(rows, ref, claim=claim)


def whois(root, token: str, claim: str | None = None):
    return _deprecated_send().whois(root, token, claim=claim)


def _deprecated_send():
    """Return the ONE deprecated-send archival module object.

    gate-t: live bin/send.py is a fail-closed stub→box (mail SoT = box only).
    Load deprecated/bin/send.py for non-mail archival helpers (whois/mint/…).
    Prefer sys.modules["send"] only when tests already patched a real module
    (not the fail-closed stub).
    """
    import importlib.util
    import sys
    existing = sys.modules.get("send")
    if existing is not None and not getattr(existing, "__gate_t_retired_stub__", False):
        # A test-patched or archival-loaded module — not the fail-closed stub.
        if getattr(existing, "whois", None) is not None:
            return existing
    sp = Path(__file__).resolve().parent.parent / "deprecated" / "bin" / "send.py"
    spec = importlib.util.spec_from_file_location("_agi_deprecated_send", sp)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load deprecated send: {sp}")
    mod = importlib.util.module_from_spec(spec)
    agi = Path(__file__).resolve().parent.parent
    for p in (str(agi / "bin"), str(agi / "src")):
        if p not in sys.path:
            sys.path.insert(0, p)
    sys.modules["_agi_deprecated_send"] = mod
    spec.loader.exec_module(mod)
    # Do NOT register as mail SoT name "send" for live callers — archival only.
    # Tests that `import send` expecting whois may still setdefault after patch.
    sys.modules.setdefault("send", mod)
    return mod

def _mint_seat_key(root, seat: str, scheme=None, stage: bool = False):
    return _deprecated_send()._mint_seat_key(root, seat, scheme, stage=stage)


def _row_write_submit(*_a, **_k):
    return _deprecated_send()._row_write_submit(*_a, **_k)


def _seat_key_path(root: Path, seat: str) -> Path:
    import locations
    return Path(locations.shared_sessions_dir(root)) / "seats" / f"{seat}.key"


def _main_graph_root(root: Path) -> Path:
    import locations
    graph = locations.find_project_root(root) or root
    main = locations.git_common_root(graph)
    main_graph = locations.find_project_root(main) if main else None
    return main_graph or graph


def _now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


def _comms_config(root: Path) -> dict:
    return {}


def _row_is_quiet(root: Path, to: str) -> bool:
    return False



def __getattr__(name: str):
    """Forward unknown attrs to deprecated send (DM paths, sign helpers, …)."""
    if name.startswith("__"):
        raise AttributeError(name)
    try:
        return getattr(_deprecated_send(), name)
    except AttributeError as e:
        raise AttributeError(f"module 'boxes' has no attribute {name!r}") from e
