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
    {flag = "--tools", spread = "tools"}        # variadic: flag + a list
    {const = "--allow-all"}
    {const = "--verbose", when = "verbose"}     # emit only when slot is truthy
    {spread = "extra_args"}                     # splice a caller list
    {slot = "prompt"}                           # positional (last)

The template ALSO declares where its SEAT model/effort/settings come from,
under `[roles] source = "..."` — `ladder` (the shared roles ladder, then
`harnesses.claude-code`, then `DEFAULT_CC_ROLES`) or `row` (THIS harness's own
`harnesses.<id>` config row). Closed vocabulary, same discipline as the argv
keys; a template that omits it is `ladder`.

Shapes: an optional `[shapes.<name>]` table holds its own `argv`, selected by
`render(..., shape="<name>")`; the top-level `argv` stays the default. This is
how ONE binary's rotate SEAT shape and headless DISPATCH shape live in one
file (hypothesis:harness-arg-builders-are-templates-only).
"""
from __future__ import annotations

import json
import tomllib
from pathlib import Path

TEMPLATES_SUBPATH = ("extensions", "agi", "templates", "harness")
_ALLOWED_KEYS = {"flag", "slot", "const", "encoding", "spread", "when"}

#: Where a seat's model/effort/settings come from. Closed vocabulary: a
#: template that omits `[roles] source` is `ladder` (claude-code's behaviour).
ROLE_SOURCES = ("ladder", "row")


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
    argv = data.get("argv", [])
    if not isinstance(argv, list):
        raise HarnessTemplateError(
            f"{path}: argv is not a list (got {type(argv).__name__}: "
            f"{argv!r}); write argv = [ ... ]")
    _check_parts(path, argv)
    roles = data.get("roles")
    if roles is not None and not isinstance(roles, dict):
        raise HarnessTemplateError(
            f"{path}: roles is not a table (got {type(roles).__name__}: "
            f"{roles!r}); write [roles] source = ...")
    shapes = data.get("shapes")
    if shapes is not None and not isinstance(shapes, dict):
        raise HarnessTemplateError(
            f"{path}: shapes is not a table (got {type(shapes).__name__}: "
            f"{shapes!r}); write [shapes.<name>]")
    for name, shape in (shapes or {}).items():
        if not isinstance(shape, dict):
            raise HarnessTemplateError(f"{path}: shape {name!r} is not a table")
        shape_argv = shape.get("argv", [])
        if not isinstance(shape_argv, list):
            raise HarnessTemplateError(
                f"{path}: shapes.{name}.argv is not a list (got "
                f"{type(shape_argv).__name__}: {shape_argv!r})")
        _check_parts(path, shape_argv, label=f"shapes.{name}")
    return data


def load_all() -> tuple[dict[str, dict], dict[str, str]]:
    """Parse every available template, ISOLATING per-file failure.

    Returns `(loaded, broken)`: `loaded` maps a harness id to its parsed
    template, `broken` maps a failing id to its error text. ONE malformed
    template removes only ITSELF from the result, never its siblings
    (hypothesis:harness-arg-builders-are-templates-only); naming the broken
    ids is the caller's job. An exception from `available()` itself still
    propagates -- that is the whole-enumeration failure, not a file's.
    """
    loaded: dict[str, dict] = {}
    broken: dict[str, str] = {}
    for hid in available():
        try:
            loaded[hid] = load(hid)
        except Exception as exc:
            broken[hid] = f"{type(exc).__name__}: {exc}"
    return loaded, broken


def _check_parts(path: Path, parts: list, label: str = "argv") -> None:
    """Refuse any token outside the declarative vocabulary, in a shape too."""
    for i, part in enumerate(parts):
        if not isinstance(part, (str, dict)):
            raise HarnessTemplateError(f"{path}: {label}[{i}] is not a token")
        if isinstance(part, dict):
            bad = set(part) - _ALLOWED_KEYS
            if bad:
                raise HarnessTemplateError(
                    f"{path}: {label}[{i}] has non-template key(s) {sorted(bad)}; "
                    f"allowed: {sorted(_ALLOWED_KEYS)}")


def role_source(harness_id: str) -> str:
    """The declared `[roles] source`; an unknown source is a NAMED error.

    The one reader the seat path uses to learn WHERE its model/effort/settings
    come from, so `spawn_window` owns no harness-NAME branch
    (hypothesis:harness-arg-builders-are-templates-only).
    """
    roles = load(harness_id).get("roles") or {}
    if not isinstance(roles, dict):
        raise HarnessTemplateError(
            f"{harness_id}: roles is not a table (got "
            f"{type(roles).__name__}: {roles!r}); write [roles] source = ...")
    source = roles.get("source", "ladder")
    if source not in ROLE_SOURCES:
        raise HarnessTemplateError(
            f"{harness_id}: unknown roles.source {source!r}; "
            f"known: {list(ROLE_SOURCES)}")
    return source


def _emit(part, values: dict) -> list[str]:
    if isinstance(part, str):
        return [part]
    if part.get("when") and not values.get(part["when"]):
        return []
    if "spread" in part:
        vals = [str(v) for v in (values.get(part["spread"]) or [])]
        # A variadic flag (flag + list); empty list emits NEITHER, or
        # `--mcp-config` would swallow the next token.
        if not vals:
            return []
        return [str(part["flag"]), *vals] if "flag" in part else vals
    if "const" in part:
        toks = [str(part["const"])]
    else:
        val = values.get(part.get("slot"))
        if val is None or val == "":
            return []
        toks = [json.dumps(val) if part.get("encoding") == "json"
                else str(val)]
    return [str(part["flag"]), *toks] if "flag" in part else toks


def render(harness_id: str, *, prompt=None, model=None, effort=None,
           bin_path=None, settings=None, extra_args=None,
           name=None, debug_file=None, provider=None, thinking=None,
           shape=None, model_args=None, output_format=None, verbose=None,
           budget=None, prompt_file=None, repo_root=None, mcp=None,
           tools=None, allowed=None, disallowed=None, closing=None) -> list[str]:
    """The argv for `harness_id`, from its template alone.

    `shape` selects an optional `[shapes.<name>]` argv instead of the
    top-level one; an unknown shape is a named error, never a silent fall
    back to the default argv.
    """
    tmpl = load(harness_id)
    parts = tmpl.get("argv", [])
    if shape is not None:
        shapes = tmpl.get("shapes") or {}
        if shape not in shapes:
            raise HarnessTemplateError(
                f"{harness_id}: no shape {shape!r}; known: {sorted(shapes)}")
        parts = (shapes[shape] or {}).get("argv", [])
    values = {"prompt": prompt, "model": model, "effort": effort,
              "settings": settings, "extra_args": extra_args,
              "name": name, "debug_file": debug_file,
              "provider": provider, "thinking": thinking,
              "model_args": model_args, "output_format": output_format,
              "verbose": verbose, "budget": budget,
              "prompt_file": prompt_file, "repo_root": repo_root, "mcp": mcp,
              "tools": tools, "allowed": allowed, "disallowed": disallowed,
              "closing": closing}
    args = [str(bin_path or tmpl.get("bin") or harness_id)]
    for part in parts:
        args.extend(_emit(part, values))
    return args