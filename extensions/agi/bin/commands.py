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
A table full of `/home/ubuntu/work/agi/...` would be a table that stops
working on the next clone, which is exactly the machine-specific state
`goal:g8.2` keeps out of the graph.

## argv, never a shell string

A shell string invites `&&`, pipes and quoting, and then the node stops being
data and becomes a program this resolver has to interpret. `goal:g9.7`'s
argument, one layer down: the form a human reads and the form the engine runs
have to be the same object.
"""
from __future__ import annotations

import json
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


def _substitute(value: str, root: Path) -> str:
    return (str(value)
            .replace("<root>", str(Path(root).resolve()))
            .replace("<engine>", str(ENGINE_ROOT)))


def load(root) -> dict[str, Command]:
    """Every declared command, keyed by name. Never raises."""
    root = Path(root)
    fm = _load_node(root)
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
        substituted = [_substitute(a, root) for a in argv]
        raw_cwd = str(spec.get("cwd") or str(root))
        out[str(name)] = Command(
            name=str(name),
            argv=substituted,
            raw_argv=[str(a) for a in argv],
            about=str(spec.get("about") or ""),
            cwd=_substitute(raw_cwd, root),
            raw_cwd=raw_cwd,
            workflow=str(spec.get("workflow") or ""),
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


def run(root, name: str, extra: list[str] | None = None) -> int:
    """Run one declared command. Returns its exit code.

    Deliberately thin: this resolves and executes, it does not capture, retry
    or interpret. A resolver that starts making decisions about a command's
    output has become the program the node exists to avoid being.
    """
    cmd = get(root, name)
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
    ap.add_argument("action", choices=["list", "show", "run", "json"],
                    nargs="?", default="list")
    ap.add_argument("name", nargs="?", help="command name, for show/run")
    ap.add_argument("extra", nargs="*", help="extra args appended to run")
    ap.add_argument("--root", default=".", help="any path inside the project")
    ap.add_argument("--workflow", "-w", default=None,
                    help="run a declared workflow instead of a single command")
    ap.add_argument("--from", dest="start_from", default=None,
                    help="resume workflow from this step (skip prior steps)")
    args = ap.parse_args(argv)

    root = locations.find_project_root(Path(args.root).resolve())
    if root is None:
        print(f"ERR: not an agi project: {args.root}", file=sys.stderr)
        return 1

    if args.action == "json":
        print(json.dumps({n: {"argv": c.argv, "about": c.about,
                              "workflow": c.workflow}
                          for n, c in sorted(load(root).items())}, indent=2))
        return 0

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
