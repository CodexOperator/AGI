#!/usr/bin/env python3
"""harness_template.py — a harness argv is DATA, not code.

hypothesis:harness-arg-builders-are-templates-only. A harness's spawn argv
is a post/harness template (TOML) plus, at most, a thin adapter hook; a
fourth harness adds a template and edits nothing in rotate.py.

The template is pure data: no eval, no exec, no embedded Python. `load`
rejects any argv key outside the small declarative vocabulary below, so a
"scripting escape hatch" is a hard error rather than a silently-ignored
field.

Element vocabulary (ordered `argv` array; a bare string is a literal token):

    {flag = "--model", slot = "model"}          # emit [flag, value]
    {flag = "--debug-file", slot = "debug_file"}# skip entirely when empty
    {flag = "--settings", slot = "settings", encoding = "json"}
    {flag = "--permission-mode", const = "bypassPermissions"}
    {const = "--allow-all"}
    {spread = "extra_args"}                     # splice a caller list
    {slot = "prompt"}                           # positional (last)
"""
from __future__ import annotations

import json
import tomllib
from pathlib import Path

TEMPLATES_SUBPATH = ("extensions", "agi", "templates", "harness")
_ALLOWED_KEYS = {"flag", "slot", "const", "encoding", "spread"}


class HarnessTemplateError(Exception):
    """A template is malformed, or a render slot is not expressible."""


class UnknownHarnessError(HarnessTemplateError):
    """A harness id with no template on disk — named, never a fallback."""


def template_dir() -> Path:
    """The `extensions/agi/templates/harness/` directory.

    Prefers the enclosing repo root (house `locations` style) and falls back
    to the engine's own tree — the templates ship with the loader, so the
    module-relative path is the durable one when the engine is cloned in.
    """
    try:
        import locations  # bin/ is on sys.path when rotate.py is imported
        root = locations.find_project_root()
        if root is not None:
            cand = locations.repo_root(Path(root)).joinpath(*TEMPLATES_SUBPATH)
            if cand.is_dir():
                return cand
    except Exception:
        pass
    return Path(__file__).resolve().parent.parent / "templates" / "harness"


def available() -> list[str]:
    """The harness ids with a template on disk, sorted."""
    return sorted(p.stem for p in template_dir().glob("*.toml"))


def load(harness_id: str) -> dict:
    """Parse `<harness_id>.toml`; raise a NAMED error for an unknown id."""
    path = template_dir() / f"{harness_id}.toml"
    if not path.is_file():
        raise UnknownHarnessError(
            f"no harness template {harness_id!r} in {template_dir()}; "
            f"available: {available()}")
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    for i, part in enumerate(data.get("argv", [])):
        if not isinstance(part, (str, dict)):
            raise HarnessTemplateError(f"{path}: argv[{i}] is not a token")
        if isinstance(part, dict):
            bad = set(part) - _ALLOWED_KEYS
            if bad:
                raise HarnessTemplateError(
                    f"{path}: argv[{i}] has non-template key(s) {sorted(bad)}; "
                    f"allowed: {sorted(_ALLOWED_KEYS)}")
    return data


def _emit(part, values: dict) -> list[str]:
    if isinstance(part, str):
        return [part]
    if "spread" in part:
        return [str(v) for v in (values.get(part["spread"]) or [])]
    if "const" in part:
        toks = [str(part["const"])]
    else:
        val = values.get(part.get("slot"))
        if val is None or val == "":
            return []
        toks = [json.dumps(val) if part.get("encoding") == "json"
                else str(val)]
    return [str(part["flag"]), *toks] if "flag" in part else toks


def render(harness_id: str, *, prompt, model=None, effort=None,
           bin_path=None, settings=None, extra_args=None,
           name=None, debug_file=None,
           provider=None, thinking=None) -> list[str]:
    """The argv for `harness_id`, from its template alone.

    `name` (the RC/session name) and `debug_file` are slots the claude-code
    shape needs; a harness whose template ignores them is unaffected.
    """
    tmpl = load(harness_id)
    values = {"prompt": prompt, "model": model, "effort": effort,
              "settings": settings, "extra_args": extra_args,
              "name": name, "debug_file": debug_file,
              "provider": provider, "thinking": thinking}
    args = [str(bin_path or tmpl.get("bin") or harness_id)]
    for part in tmpl.get("argv", []):
        args.extend(_emit(part, values))
    return args