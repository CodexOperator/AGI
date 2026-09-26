#!/usr/bin/env python3
"""commands.py — the engine's standard commands, resolved from the graph.

`goal:g1.10`. Everything else about a run is declared — metrics, dispatch,
harnesses, schemas, cron cadences, the spawn budget, credentials. **The
commands an operator actually types were declared nowhere.** They lived in
`CLAUDE.md` prose, in `SKILL.md`'s table, in `QUICKSTART.md`, and in whatever
the last session's `HANDOFF.md` happened to write down — four copies that drift
independently, which is the shape `goal:s17` names and this repo has already
paid for once with the ancestor walk restated eleven times.

`.agi/nodes/.geometry/commands.md` is the one declaration.
`bin/commands.py` is the one resolver. **Editing the node is the change** —
the same relationship `crons.md` has to `crons.py`, copied deliberately rather
than reinvented, because that shape is already running.

## Two readers, and the second is why the node is allowed to exist

`goal:g10.2`'s rule is that a `.geometry` node must be the input a code path
resolves against, never documentation about one. This module is the first
reader; `render-context.py` is the second, writing the declared set into
`context/INJECTION.md` so every agent is **handed** the commands instead of
remembering them. A command table nothing reads is a fourth copy of the prose.

## Substitution, and why there are no absolute paths in the node

`<root>` becomes the resolved graph root and `<engine>` the engine checkout.
A table full of one box's absolute `.../extensions/agi/bin/...` would be a
table that stops working on the next clone, which is exactly the machine-specific state
`goal:g8.2` keeps out of the graph.

## argv, never a shell string

A shell string invites `&&`, pipes and quoting, and then the node stops being
data and becomes a program this resolver has to interpret. `goal:g9.7`'s
argument, one layer down: the form a human reads and the form the engine runs
have to be the same object.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import locations  # noqa: E402

#: Where the declaration lives, relative to the graph root. Beside `crons.md`,
#: in the same `.geometry/` directory, because they are the same kind of fact.
COMMANDS_NODE_REL = Path("nodes") / ".geometry" / "commands.md"

#: The engine checkout: this file is `<engine>/extensions/agi/bin/commands.py`.
ENGINE_ROOT = Path(__file__).resolve().parent.parent.parent.parent


def engine_for(graph_root: Path) -> Path:
    """The engine checkout that OWNS `graph_root` — not the running script's.

    `<engine>` must be substituted from the engine enclosing the GRAPH that
    declared the command, never from wherever the runner happens to live. A
    `verification.py` run from a worktree with `--root` at the main checkout
    used to substitute `<engine>` from the worktree while reading the main
    checkout's graph — TWO trees in one report, silent
    (hypothesis:l4-verification-counts-and-engine-root).

    In the unified single-repo layout the repo holding `.agi` also carries
    `extensions/agi/bin/commands.py`, so the engine is the nearest ancestor
    of the graph root that has that file. When no such ancestor exists (a
    project that cloned the engine in under a layout we cannot walk), we fall
    back to THIS script's engine and let the caller NAME both roots so the
    fallback is visible — resolution when we can, honesty when we cannot.
    """
    root = Path(graph_root).resolve()
    for cand in (root, *root.parents):
        if (cand / "extensions" / "agi" / "bin" / "commands.py").is_file():
            return cand
    return ENGINE_ROOT


class CommandError(RuntimeError):
    """A command was asked for that the graph does not declare."""


@dataclass(frozen=True)
class Command:
    """One declared command, with both raw and substituted argv."""

    name: str
    argv: list[str]
    raw_argv: list[str]
    about: str = ""
    cwd: str = ""
    raw_cwd: str = ""
    workflow: str = ""
    owner_only: bool = False

    def shell(self, *, placeholders: bool = False) -> str:
        """Render the command as a shell string.

        placeholders=False (default) emits the fully substituted argv — the form
        that actually runs on this checkout. placeholders=True preserves the
        `<root>` / `<engine>` tokens from the declaration so rendered docs stay
        clone-agnostic (goal:g8.2).
        """
        import shlex
        argv = self.raw_argv if placeholders else self.argv
        return " ".join(shlex.quote(a) for a in argv)


def _load_node(root: Path) -> dict:
    """The declaration's frontmatter, or `{}` when there is no node.

    Absent is a supported state: a project that has not minted a commands node
    resolves an empty table and every caller degrades to knowing nothing,
    which is exactly where every project was before this goal.
    """
    path = Path(root) / COMMANDS_NODE_REL
    if not path.is_file():
        return {}
    try:
        from graph_core.persistence import frontmatter as fm_reader
        return dict(fm_reader.load_node_file(path).frontmatter)
    except Exception as exc:
        # A node that EXISTS and will not load is a different fact from one
        # that is absent, and the first version of this function returned `{}`
        # for both -- so a missing `src/` on `sys.path` reported "no commands
        # declared" about a node sitting right there, fully parseable. Absence
        # is silent because it is normal; a failure to read something present
        # is never normal.
        print(f"WARN: {path} exists but could not be read: "
              f"{type(exc).__name__}: {exc}", file=sys.stderr)
        return {}


def _substitute(value: str, root: Path, engine: Path | None = None) -> str:
    return (str(value)
            .replace("<root>", str(Path(root).resolve()))
            .replace("<engine>", str(engine if engine is not None
                                else engine_for(root)))
            .replace("<stub>", str(locations.streamer_stub(root)))
            .replace("<home>", str(Path.home())))


def load(root) -> dict[str, Command]:
    """Every declared command, keyed by name. Never raises."""
    root = Path(root)
    fm = _load_node(root)
    engine = engine_for(root)
    out: dict[str, Command] = {}
    for name, spec in (fm.get("commands") or {}).items():
        if not isinstance(spec, dict):
            continue
        argv = spec.get("argv")
        if not isinstance(argv, list) or not argv:
            # A command with no argv is a note, not a command. Skipped rather
            # than half-resolved, because a Command that cannot run is worse
            # than an absent one -- it looks available.
            continue
        substituted = [_substitute(a, root, engine) for a in argv]
        raw_cwd = str(spec.get("cwd") or str(root))
        out[str(name)] = Command(
            name=str(name),
            argv=substituted,
            raw_argv=[str(a) for a in argv],
            about=str(spec.get("about") or ""),
            cwd=_substitute(raw_cwd, root, engine),
            raw_cwd=raw_cwd,
            workflow=str(spec.get("workflow") or ""),
            owner_only=bool(spec.get("owner_only")),
        )
    return out


def workflows(root) -> dict[str, list[str]]:
    """Named, ordered sequences of command names."""
    fm = _load_node(Path(root))
    out: dict[str, list[str]] = {}
    for name, seq in (fm.get("workflows") or {}).items():
        if isinstance(seq, list):
            out[str(name)] = [str(s) for s in seq]
    return out


def ordered_workflows(root) -> set[str]:
    """Which workflows are a SEQUENCE rather than a set.

    Rendered into `INJECTION.md`, so an unordered inspection set described as
    "in this order" would be a false instruction delivered to every agent.
    """
    value = _load_node(Path(root)).get("ordered") or []
    return {str(v) for v in value} if isinstance(value, list) else set()


#: The closed set a manifest entry's `side_effects` may name (a typo here is a
#: choice a proposer would act on, so the set is data a test can see).
SIDE_EFFECTS = ("read", "graph-write", "comms", "spawn", "spend",
                "network", "destructive", "box-write", "long-running")

#: The ONE never-proposable set beside `SIDE_EFFECTS`: a verb that spends,
#: spawns, destroys, writes box state outside the graph (crontab, systemd
#: units, a git hook, the env file) or never exits on its own is never offered.
#: `_entry` forces `proposable: false` for any of these, so the floor cannot be
#: lowered by a node edit; `propose` refuses a supplied arg that declares one.
NEVER_PROPOSABLE = frozenset({"spawn", "spend", "destructive",
                              "box-write", "long-running"})


def _derived_cli_verb(raw: list[str]) -> tuple[str, str]:
    """`cli`/`verb` read off an entry's own argv when it declares neither."""
    for i, arg in enumerate(raw):
        base = str(arg).rsplit("/", 1)[-1]
        if base.endswith((".py", ".sh")):
            rest = [str(a) for a in raw[i + 1:]]
            return base, (rest[0] if rest else "")
    return (str(raw[0]) if raw else "", str(raw[1]) if len(raw) > 1 else "")


def _entry(name, argv, m, cli, verb, side, prop, purpose=""):
    """One choice-set entry; `m` (the node's metadata) overrides every default."""
    e = {"name": name, "cli": str(m.get("cli") or cli),
         "verb": str(m.get("verb") or verb), "argv": list(argv),
         "args": list(m.get("args") or []),
         "purpose": str(m.get("purpose") or m.get("reason") or purpose),
         "side_effects": str(m.get("side_effects") or side),
         "proposable": bool(m.get("proposable", prop))}
    if m.get("reason"):
        e["reason"] = str(m["reason"])
    if e["side_effects"] in NEVER_PROPOSABLE:
        e["proposable"] = False          # spend/spawn/destructive/box-write/long-running
    return e


def manifest(root) -> dict[str, dict]:
    """The ONE machine-readable choice set, from `command:commands` alone.

    Declared commands join their `manifest:` metadata (or derive `cli`/`verb`
    from their own argv); every `excluded:` verb is included with
    `proposable: false` and its reason. Read-only: it resolves the node and
    returns data, never running or writing anything.
    """
    fm = _load_node(Path(root))
    dec, exc = fm.get("manifest") or {}, fm.get("excluded") or {}
    out: dict[str, dict] = {}
    for name, c in load(root).items():
        m = dec.get(name) if isinstance(dec.get(name), dict) else {}
        out[name] = _entry(name, c.raw_argv, m, *_derived_cli_verb(c.raw_argv),
                           "read", True, c.about)
    for name, m in {**dec, **exc}.items():
        if name in out or not isinstance(m, dict):
            continue
        cli, verb = name.split(":", 1)[0], name.split(":", 1)[-1]
        out[name] = _entry(name, [str(a) for a in (m.get("argv") or [])], m,
                           cli, verb, "graph-write", name not in exc)
    return out


def render_manifest(root) -> str:
    """`manifest()` as deterministic JSON: two calls agree byte for byte."""
    return json.dumps(manifest(root), indent=2, sort_keys=True)


#: Placeholders that name no declared arg and stay for the runner to fill:
#: `<engine>`/`<root>`/`<home>` are resolved by `load`, `<node-id>` by the
#: verb itself. Anything else left after substitution is unmapped -- refuse.
KEPT_METAVARS = frozenset({"engine", "root", "home", "stub", "node-id",
                           "project_root"})
_PLACEHOLDER_RE = re.compile(r"<([^<>]+)>")


def _coerce(value, arg):
    """The declared `type` applied to one propose value."""
    if str(arg.get("type") or "str") == "bool":
        return str(value).lower() in ("true", "1", "yes")
    return str(value)


#: How a supplied arg with no `<name>` in `argv` lands, read from the node's
#: `placement` map: `option` -> `[flag, value]`, `switch` -> flag when true,
#: `const` -> the flag its value selects, `positional` -> the bare value.
#: `placement: {defaults: true}` opts a graph into `--<name>` / bool-as-switch
#: defaults; entries override per arg, or per `"<entry>.<arg>"`. A renamed
#: flag fails a committed drift test that introspects each CLI's argparse at
#: TEST time -- `propose` never imports, execs or patches one.
_PLACEMENT_KINDS = ("option", "switch", "const", "positional")


def _split_arity(spec):
    """`(mode, size)` from a placement's `arity`, or `(None, 0)` when it
    declares none (a single value). `many` -> one flag, every value;
    `append`/`append:N` -> the flag repeated, N values each; `"<N>"` -> one
    flag and N values; anything else -> a single value."""
    s = str(spec or "").strip()
    if s in ("many", "+", "*"):
        return "many", 0
    if s.startswith("append"):
        _, _, tail = s.partition(":")
        return "append", int(tail) if tail.isdigit() else 1
    if s.isdigit() and int(s) > 1:
        return "nargs", int(s)
    return None, 1 if s else 0


def _resolve_placement(name, arg, entry, rules):
    """`(kind, flag, const, consts, arity)` for a declared arg, or None when
    the node declares no placement for it and has not opted into the defaults.
    `arity` is the declared multi-value spelling, or None when undeclared."""
    spec = rules.get(f"{entry}.{name}") or rules.get(name)
    if not isinstance(spec, dict):
        if not rules.get("defaults"):
            return None
        spec = {"kind": "switch" if str(arg.get("type") or "str") == "bool"
                else "option", "flag": "--" + str(name).replace("_", "-")}
    kind = str(spec.get("kind") or "option")
    if kind not in _PLACEMENT_KINDS:
        return None
    return (kind, str(spec.get("flag") or ""), spec.get("const"),
            dict(spec.get("consts") or {}), spec.get("arity"))


def propose(root, name: str, args: dict | None = None) -> list[str]:
    """Validate `args` against the entry and RETURN its argv — NEVER run it.

    Substitution is ONE PASS over the declared args only: an undeclared key
    substitutes nothing, a value containing `<x>` is never re-scanned, and an
    argv that would still hold an unmapped placeholder -- or a supplied arg
    with no `<name>` to land in -- REFUSES by name. It never returns an
    incomplete argv for a proposer to run.
    """
    entry = manifest(root).get(name)
    if entry is None:
        raise CommandError(f"no command {name!r} in the choice set")
    if not entry.get("proposable"):
        raise CommandError(
            f"{name!r} is not proposable: {entry.get('reason') or 'declared'}")
    given = dict(args or {})
    declared = {str(a.get("name") or ""): a for a in entry.get("args") or []}
    values: dict[str, str] = {}
    for n, arg in declared.items():
        if n not in given:
            if arg.get("required"):
                raise CommandError(f"{name!r}: missing required arg {n!r}")
            continue
        if str(arg.get("side_effects") or "") in NEVER_PROPOSABLE:
            raise CommandError(
                f"{name!r}: arg {n!r} is never proposable "
                f"(side effect {arg['side_effects']!r})")
        v = _coerce(given[n], arg)
        if (arg.get("choices") or []) and v not in arg["choices"]:
            raise CommandError(
                f"{name!r}: arg {n!r}={v!r} not in {arg['choices']}")
        values[n] = str(v)
    template = " ".join(str(t) for t in entry["argv"])
    # A supplied arg with no `<name>` lands as the CLI's OWN flag or
    # positional, read from the node's `placement` data -- a value with no
    # declared placement REFUSES BY NAME, never a silent drop.
    rules = _load_node(Path(root)).get("placement") or {}
    extra: list[str] = []
    positional: list[str] = []
    for n in values:
        value = values[n]
        if f"<{n}>" in template:
            continue
        placed = _resolve_placement(n, declared[n], name, rules)
        if placed is None:
            raise CommandError(
                f"{name!r}: cannot place arg {n!r}; argv has no <{n}> and the "
                f"node declares no placement for it")
        kind, flag, const, consts, arity = placed
        if kind == "positional":
            positional.append(value)
        elif kind == "switch":
            if value == "True" and flag and flag not in entry["argv"]:
                extra.append(flag)
        elif kind == "const":
            token = consts.get(value)
            if token is None and const is not None and str(const) == value:
                token = flag
            if token is None:
                raise CommandError(
                    f"{name!r}: cannot place arg {n!r}={value!r}; no const "
                    f"selects it")
            if token not in entry["argv"]:
                extra.append(token)
        elif flag:                       # option: flag + value(s)
            mode, size = _split_arity(arity)
            vals = ([_coerce(v, declared[n]) for v in given[n]]
                    if isinstance(given[n], (list, tuple)) else [value])
            if mode is None and len(vals) > 1:
                raise CommandError(
                    f"{name!r}: arg {n!r} got {len(vals)} values but its "
                    f"placement declares one -- declare an arity to place "
                    f"them all")
            if mode == "nargs" and len(vals) != size:
                raise CommandError(
                    f"{name!r}: arg {n!r} needs {size} values, got {len(vals)}")
            if mode == "append" and size and len(vals) % size:
                raise CommandError(
                    f"{name!r}: arg {n!r} needs multiples of {size} values, "
                    f"got {len(vals)}")
            groups = ([vals[i:i + size] for i in range(0, len(vals), size)]
                      if mode == "append" else [vals])
            for group in groups:
                if flag not in entry["argv"]:
                    extra += [flag] + group
        else:
            raise CommandError(
                f"{name!r}: cannot place arg {n!r}; node declares no flag for it")
    # The leftover set is read off the TEMPLATE, before any substitution --
    # never off the output. A caller value that merely LOOKS like a
    # placeholder (`<foo>`, `<div>x</div>`) is data and lands untouched; only
    # a placeholder the template itself never mapped is unmapped.
    leftover = sorted(n for n in set(_PLACEHOLDER_RE.findall(template))
                      if n not in values and n not in KEPT_METAVARS)
    if leftover:
        raise CommandError(
            f"{name!r}: unmapped placeholder <{leftover[0]}> -- argv cannot "
            f"complete; declare the arg or fix the template")

    def _fill(match: "re.Match") -> str:
        return values.get(match.group(1), match.group(0))

    # ONE pass: a substituted value is never rescanned.
    return [_PLACEHOLDER_RE.sub(_fill, str(t))
            for t in entry["argv"]] + extra + positional


def get(root, name: str) -> Command:
    """One command by name. Raises `CommandError` naming what is available."""
    table = load(root)
    if name not in table:
        known = ", ".join(sorted(table)) or "(none declared)"
        raise CommandError(
            f"no command {name!r} in {COMMANDS_NODE_REL}. Declared: {known}. "
            f"Add it to the node — editing the node IS the change (goal:g1.10)."
        )
    return table[name]


def _actor() -> str:
    """The actor running this process: `$AGI_ACTOR`, else `$USER`, else
    `unknown`. The same resolution `write.py:_default_actor` uses, so the
    owner gate here and the role resolution there agree on who is who."""
    return os.environ.get("AGI_ACTOR") or os.environ.get("USER") or "unknown"


def run(root, name: str, extra: list[str] | None = None) -> int:
    """Run one declared command. Returns its exit code.

    Deliberately thin: this resolves and executes, it does not capture, retry
    or interpret. A resolver that starts making decisions about a command's
    output has become the program the node exists to avoid being.

    One decision it DOES make, and only when the declaration asks: an
    `owner_only: true` command (the stream `panic`) is refused for every
    actor other than `owner`, before any subprocess call. The refusal is
    machine-readable (names the flag honoured) and non-zero, so the stream
    stays live -- a non-owner asking for `panic` gets no whisper.
    """
    cmd = get(root, name)
    if cmd.owner_only:
        actor = _actor()
        if actor != "owner":
            print(
                f"REFUSED: {name!r} is owner_only; actor {actor!r} is not "
                f"the owner. Nothing was executed, the stream is untouched.",
                file=sys.stderr,
            )
            return 3
    argv = list(cmd.argv) + list(extra or [])
    return subprocess.call(argv, cwd=cmd.cwd or None)


def run_workflow(root, workflow_name: str, start_from: str | None = None) -> int:
    """Run an ordered workflow: execute each step in sequence, stop on failure.

    Returns the failing step's exit code, or 0 if all steps pass.
    Reports which step broke and its exit code to stderr.

    Exit code 2 means the workflow itself was not found in the declaration.
    """
    flow_map = workflows(root)
    ordered_set = ordered_workflows(root)

    if workflow_name not in flow_map:
        known = ", ".join(sorted(flow_map)) or "(none declared)"
        print(f"ERR: no workflow {workflow_name!r}. Declared: {known}.",
              file=sys.stderr)
        return 2

    if workflow_name not in ordered_set:
        print(f"ERR: workflow {workflow_name!r} is unordered "
              f"(a set, not a sequence); cannot execute in order.",
              file=sys.stderr)
        return 2

    steps = flow_map[workflow_name]
    start_idx = 0
    if start_from is not None:
        if start_from in steps:
            start_idx = steps.index(start_from)
        else:
            print(f"ERR: step {start_from!r} not in workflow "
                  f"{workflow_name!r}. Steps: {steps}.", file=sys.stderr)
            return 2

    for step in steps[start_idx:]:
        code = run(root, step)
        if code != 0:
            try:
                cmd = get(root, step)
                print(f"FAIL: step {step!r} exited {code}", file=sys.stderr)
                print(f"  re-run: {cmd.shell()}", file=sys.stderr)
            except CommandError:
                print(f"FAIL: step {step!r} exited {code} "
                      f"(no further detail — not in declaration)",
                      file=sys.stderr)
            return code



def render_for_injection(root, limit: int = 0) -> list[str]:
    """The declared commands as `INJECTION.md` lines.

    This is the reader that makes the node worth having: an agent is *handed*
    the commands rather than told to remember them. Grouped by workflow so the
    order carries meaning — a bare alphabetical list would lose the one thing
    a workflow declares.
    """
    table = load(root)
    if not table:
        return []
    lines = ["## standard commands (declared in `.geometry/commands.md`)"]
    flows = workflows(root)
    ordered = ordered_workflows(root)
    seen: set[str] = set()
    for flow_name, names in flows.items():
        members = [table[n] for n in names if n in table]
        if not members:
            continue
        suffix = " — in this order:" if flow_name in ordered else ":"
        lines.append(f"- **{flow_name}**{suffix}")
        for cmd in members:
            seen.add(cmd.name)
            lines.append(f"  - `{cmd.shell(placeholders=True)}`"
                         + (f" — {cmd.about}" if cmd.about else ""))
    loose = [c for n, c in sorted(table.items()) if n not in seen]
    if loose:
        lines.append("- standalone:")
        for cmd in loose:
            lines.append(f"  - `{cmd.shell(placeholders=True)}`"
                         + (f" — {cmd.about}" if cmd.about else ""))
    if limit and len(lines) > limit:
        lines = lines[:limit] + [f"  … {len(table)} declared in total"]
    return lines


def main(argv: list[str] | None = None) -> int:
    """`commands.py list|show <name>|run <name> [--] args...`"""
    import argparse

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("action",
                    choices=["list", "show", "run", "json", "manifest",
                             "propose"],
                    nargs="?", default="list")
    ap.add_argument("name", nargs="?", help="command name, for show/run")
    ap.add_argument("extra", nargs="*", help="extra args appended to run")
    ap.add_argument("--args", dest="args_json", default=None,
                    help="JSON object of propose args")
    ap.add_argument("--root", default=".", help="any path inside the project")
    ap.add_argument("--workflow", "-w", default=None,
                    help="run a declared workflow instead of a single command")
    ap.add_argument("--from", dest="start_from", default=None,
                    help="resume workflow from this step (skip prior steps)")
    # 🔴 `parse_known_args`, NOT `parse_args`, and the choice is decided by a
    # measurement rather than by taste (hypothesis:
    # l4-the-command-runner-eats-its-passengers-flag, experiment
    # a00-914a9ae6-ee1f1e). `extra` is `nargs="*"`, so argparse claimed any
    # leading `-`-prefixed token for the WRAPPER: `commands.py run links
    # --dry-run` printed `commands.py: error: unrecognized arguments` and
    # `commands.py`'s own usage block, handing a reader debugging a flag they
    # typed for `links.py` the wrong program's manual. The error lied about
    # whose problem it was. Any leading dash did it, not only `--long`.
    #
    # The trade-off the fix had to settle was what happens to the WRAPPER's
    # own flags after the name, and the round measured it instead of guessing:
    # `commands.py run links --root /tmp` already printed `ERR: not an agi
    # project: /tmp` — after-name wrapper binding was the status quo, and an
    # accidental one. `parse_known_args` PRESERVES it (known wrapper flags
    # still bind to the wrapper wherever they appear, unknown ones forward)
    # and removes only the error; `argparse.REMAINDER` would have forwarded
    # `--root /x` to the target and changed behaviour nobody asked to change.
    #
    # `--` keeps working exactly as before: argparse strips it and everything
    # after lands in `extra`, which is what `main`'s docstring promises and
    # what callers may already rely on. This is the same defect
    # `test_pass_through_flags_reach_the_command_not_the_router` guards for
    # the `agi` verb router — "the router eating its passenger's mail".
    args, forwarded = ap.parse_known_args(argv)
    if forwarded:
        args.extra = list(args.extra) + forwarded

    root = locations.find_project_root(Path(args.root).resolve())
    if root is None:
        print(f"ERR: not an agi project: {args.root}", file=sys.stderr)
        return 1

    if args.action == "json":
        print(json.dumps({n: {"argv": c.argv, "about": c.about,
                              "workflow": c.workflow}
                          for n, c in sorted(load(root).items())}, indent=2))
        return 0

    if args.action == "manifest":
        print(render_manifest(root))
        return 0

    if args.action == "propose":
        if not args.name:
            print("ERR: propose needs a command name", file=sys.stderr)
            return 2
        try:
            payload = json.loads(args.args_json) if args.args_json else {}
            print(json.dumps(propose(root, args.name, payload)))
            return 0
        except (CommandError, json.JSONDecodeError) as exc:
            print(f"ERR: {exc}", file=sys.stderr)
            return 2 if isinstance(exc, json.JSONDecodeError) else 1

    if args.action == "list":
        table = load(root)
        if not table:
            print(f"no commands declared at {COMMANDS_NODE_REL}")
            return 0
        width = max(len(n) for n in table)
        for flow, names in workflows(root).items():
            print(f"[{flow}]")
            for n in names:
                if n in table:
                    print(f"  {n:{width}}  {table[n].about}")
        listed = {n for names in workflows(root).values() for n in names}
        loose = sorted(set(table) - listed)
        if loose:
            print("[standalone]")
            for n in loose:
                print(f"  {n:{width}}  {table[n].about}")
        return 0

    if args.action == "run" and args.workflow:
        return run_workflow(root, args.workflow, start_from=args.start_from)

    if not args.name:
        print(f"ERR: {args.action} needs a command name", file=sys.stderr)
        return 2
    try:
        if args.action == "show":
            print(get(root, args.name).shell())
            return 0
        return run(root, args.name, args.extra)
    except CommandError as exc:
        print(f"ERR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
