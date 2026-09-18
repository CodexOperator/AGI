#!/usr/bin/env python3
"""workflow_note.py — PostToolUse hook that closes the record for a native
Claude Code Workflow tool call.

hypothesis:l4-same-harness-handback-a-claude-code-caller-gets-one-exact-native-
workflow-call-every-engine-js-is-registered-and-a-hook-closes-the-record

When Claude Code's Workflow tool runs one of this repo's `agi-*.js` scripts,
the handback line workflow.py printed already appended a tracked row with
`harness_id: []` — workflow.py never runs the script, so it cannot see the id
the harness mints. Only a hook that sees the tool RESULT closes the loop: it
reverse-maps the tool's `name` to the config key through the manifest `script`
field, finds the LAST open (`harness_id == []`) row of that workflow, and
shells out to the ONE `workflow.py note <run_key> --harness-id <id>` verb.

It fires in EVERY Claude Code session on this box, so it must never fail the
tool it is attached to: anything it does not understand is a NAMED one-line
stderr message and exit 0 — never a traceback, never a non-zero exit. The
`workflow.py note` refusal in an unrelated project ("no .agi project root") is
swallowed the same way.

Assumed tool_response shape: nobody has a real sample, so a short ordered list
of plausible keys (`runId`, `run_id`, `id`) is checked and the FIRST present
string is taken. tool_input is `{"name": ..., "args": ...}`, exactly the object
the model was told to call it with.
"""

import json
import subprocess
import sys
from pathlib import Path

#: Plausible keys for the harness-minted id in tool_response, in order.
HARNESS_ID_KEYS = ("runId", "run_id", "id")


class HookSkip(Exception):
    """A named reason this payload is not one we can close the record for."""


def _project_root(cwd: str) -> Path | None:
    """The nearest enclosing `.agi` dir holding a config, else None (silent
    outside a project — the hook runs everywhere on this box)."""
    try:
        d = Path(cwd).resolve()
    except (OSError, TypeError):
        return None
    for anc in (d, *d.parents):
        if anc.name == ".agi" and (anc / "config.json").is_file():
            return anc
        inner = anc / ".agi" / "config.json"
        if inner.is_file():
            return inner.parent
    return None


def _engine_root(graph_root: Path) -> Path:
    """The repo root that carries extensions/agi/workflows, walking up from the
    graph root (`.agi` is one level under it)."""
    cand = graph_root
    for _ in range(6):
        if (cand / "extensions" / "agi" / "workflows").is_dir():
            return cand
        cand = cand.parent
        if cand == cand.parent:
            break
    return graph_root


def _key_for_script(repo: Path, name: str) -> str | None:
    """Reverse-map a registered workflow NAME (`agi-round-review`) to its config
    key (`review`) by scanning the manifests for `script == <name>.js`. The key
    and the script stem diverge for review/drafting, so this is a field read,
    never a string heuristic."""
    wf = repo / "extensions" / "agi" / "workflows"
    want = f"{name}.js"
    for mf in sorted(wf.glob("*.json")):
        try:
            m = json.loads(mf.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if m.get("script") == want and m.get("name"):
            return str(m["name"])
    return None


def _sessions_dir(graph_root: Path) -> Path:
    """The graph's ONE shared workflow-sessions dir; routed through the shared
    project root when it resolves (the same rule `_track_run` uses)."""
    try:
        bin_dir = Path(__file__).resolve().parents[1] / "bin"
        sys.path.insert(0, str(bin_dir))
        import locations  # noqa: PLC0415 — lazy, engine-optional
        shared = locations.shared_project_root(graph_root)
        if shared:
            return Path(shared) / "sessions" / "workflows"
    except Exception:  # noqa: BLE001
        pass
    return graph_root / "sessions" / "workflows"


def _harness_id(tool_response) -> str:
    """The harness-minted id, or a named skip."""
    if not isinstance(tool_response, dict):
        raise HookSkip("tool_response is not an object")
    for k in HARNESS_ID_KEYS:
        v = tool_response.get(k)
        if isinstance(v, str) and v:
            return v
    raise HookSkip(
        "no harness id in tool_response (tried " + ", ".join(HARNESS_ID_KEYS) + ")")


def plan_note(payload, graph_root: Path) -> tuple[str, str]:
    """`(run_key, harness_id)` for the tracked row this tool call opened, or a
    named `HookSkip`. Pure: reads files, spawns nothing, so a test drives it
    directly with a fixture payload and a fixture tree."""
    if not isinstance(payload, dict):
        raise HookSkip("payload is not a JSON object")
    if payload.get("tool_name") != "Workflow":
        raise HookSkip(f"tool_name {payload.get('tool_name')!r} is not Workflow")
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        raise HookSkip("tool_input is not an object")
    name = tool_input.get("name")
    if not isinstance(name, str) or not name:
        raise HookSkip("tool_input.name is missing")
    hid = _harness_id(payload.get("tool_response"))
    key = _key_for_script(_engine_root(graph_root), name)
    if key is None:
        raise HookSkip(f"name {name!r} is not a registered workflow")
    path = _sessions_dir(graph_root) / f"{key}.jsonl"
    if not path.is_file():
        raise HookSkip(f"no tracked runs file for {key!r}")
    run_key = None
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if row.get("harness_id") == [] and row.get("run_key"):
            run_key = str(row["run_key"])   # LAST open row wins
    if run_key is None:
        raise HookSkip(f"no open (unnoted) row for {key!r}")
    return run_key, hid


def _note(run_key: str, harness_id: str) -> None:
    """Shell out to the ONE note verb. Kept as a module seam so a test proves
    the argv without ever spawning a real workflow.py."""
    bin_dir = Path(__file__).resolve().parents[1] / "bin"
    subprocess.run(
        [sys.executable, str(bin_dir / "workflow.py"), "note", run_key,
         "--harness-id", harness_id],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30,
    )


def main(text: str) -> int:
    """Read one PostToolUse envelope, note if it is ours, exit 0 always."""
    try:
        payload = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        print("workflow_note: payload is not JSON; skipping", file=sys.stderr)
        return 0
    cwd = payload.get("cwd") if isinstance(payload, dict) else None
    graph_root = _project_root(cwd) if isinstance(cwd, str) else None
    if graph_root is None:
        print("workflow_note: no .agi project root from cwd; skipping",
              file=sys.stderr)
        return 0
    try:
        run_key, harness_id = plan_note(payload, graph_root)
    except HookSkip as exc:
        print(f"workflow_note: {exc}; skipping", file=sys.stderr)
        return 0
    except Exception as exc:  # noqa: BLE001 — a hook must never fail the tool
        print(f"workflow_note: unexpected {type(exc).__name__}: {exc}; skipping",
              file=sys.stderr)
        return 0
    try:
        _note(run_key, harness_id)
    except Exception as exc:  # noqa: BLE001 — the note refusal is swallowed too
        print(f"workflow_note: note failed ({type(exc).__name__}: {exc}); "
              f"skipping", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.stdin.read()))
