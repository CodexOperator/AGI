"""GitHub Copilot CLI harness adapter.

Copilot CLI is authenticated by the local GitHub login, so it does not need
an OpenRouter provisioning key.  The adapter deliberately keeps the same
dispatch contract as the pi and Claude Code adapters: dispatch owns leases,
brief assembly, and lifecycle; this module only spells the command and
environment for one child.
"""
from __future__ import annotations

import os
from pathlib import Path

import brief
import locations

NAME = "copilot-cli"
DEFAULT_BIN = "copilot"


def resolve_bin(harness: dict) -> str:
    return os.environ.get("COPILOT_BIN") or harness.get("bin") or DEFAULT_BIN


def model_args(harness: dict, tier: str) -> list[str]:
    models = harness.get("models") or {}
    if not models:
        return []
    if tier not in models:
        raise KeyError(
            f"harness {NAME!r} declares no model for tier {tier!r}; "
            f"known tiers: {sorted(models)}"
        )
    model = models[tier]
    return ["--model", str(model).strip()] if str(model).strip() else []


def list_models(harness: dict) -> dict[str, str]:
    """Return the configured tier-to-model listing for status and diagnostics."""
    return {
        str(tier): str(model)
        for tier, model in (harness.get("models") or {}).items()
        if str(model).strip()
    }


def transcript_path(*, sess_dir: Path, agent_id: str | None = None) -> Path:
    """Return the child log path used as its transcript by dispatch."""
    return Path(sess_dir) / "output.log"


def child_env(*, harness: dict, base: dict[str, str],
              tier: str | None = None) -> dict[str, str]:
    env = dict(base)
    env.update({k: str(v) for k, v in (harness.get("env") or {}).items()})
    return env


def build_command(
    *,
    harness: dict,
    tier: str,
    context_file: str,
    agent_id: str,
    iter_n: int,
    sess_dir: Path,
    scaffold: dict | None = None,
    cli_py: str | Path = "",
    skill_prompt: Path | None = None,
    dispatch_py: str | Path = "",
    source_root: str | Path | None = None,
    target: str | None = None,
    parallel: int = 1,
    max_live: int = 1,
    kid_ceiling: int | None = None,
    addendum: str | None = None,
    brief_tier: str | None = None,
    role: str | None = None,
    ladder_tier: int | None = None,
    project_root: str | Path | None = None,
) -> list[str]:
    """Build a non-interactive Copilot CLI invocation with the full brief."""
    btier = brief_tier or tier
    parts: list[str] = []
    context = Path(context_file)
    if not brief.survival_selected() and context.exists():
        parts.append(context.read_text(encoding="utf-8"))
    parts.extend(brief.assemble(
        tier=btier, agent_id=agent_id, iter_n=iter_n, cli_py=cli_py,
        dispatch_py=dispatch_py, scaffold=scaffold, target=target,
        parallel=parallel, max_live=max_live, session_dir=Path(sess_dir),
        source_root=source_root, kid_ceiling=kid_ceiling, addendum=addendum,
        project_root=project_root,
    ))
    if skill_prompt is not None and Path(skill_prompt).exists():
        parts.append(Path(skill_prompt).read_text(encoding="utf-8"))
    prompt = "\n\n".join(part.rstrip("\n") for part in parts if part)
    args = [resolve_bin(harness), "--prompt", prompt, "--allow-all",
            "--output-format", str(harness.get("output_format") or "json"),
            "--no-color"]
    args += model_args(harness, tier)
    effort = harness.get("effort")
    if isinstance(effort, dict):
        effort = effort.get(tier)
    if effort:
        args += ["--effort", str(effort)]
    root = project_root or source_root
    if root:
        args += ["--add-dir", str(locations.repo_root(Path(root)))]
    args += [str(value) for value in (harness.get("extra_args") or [])]
    return args


def is_alive(pid: int) -> bool:
    try:
        with open(f"/proc/{pid}/stat", encoding="utf-8") as fh:
            if fh.read().rsplit(") ", 1)[1].split()[0] == "Z":
                return False
    except (OSError, IndexError, ValueError):
        pass
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def restart(**kwargs) -> int | None:
    import json
    import subprocess
    import time

    agent_record = kwargs.get("agent_record") or {}
    sess_dir = Path(kwargs["sess_dir"])
    command = build_command(**{
        key: value for key, value in kwargs.items()
        if key not in {"agent_record"}
    })
    log_file = sess_dir / "output.log"
    cwd = Path(agent_record.get("worktree") or sess_dir.parent.parent.parent)
    try:
        with log_file.open("ab") as log:
            proc = subprocess.Popen(
                command, stdout=log, stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL, start_new_session=True,
                cwd=str(cwd), env=child_env(
                    harness=kwargs["harness"], base=dict(os.environ),
                    tier=kwargs.get("tier")),
            )
    except OSError:
        return None
    agent_record.update({
        "pid": proc.pid,
        "status": "restarted",
        "restarted_at": int(time.time()),
    })
    (sess_dir / "agent.json").write_text(
        json.dumps(agent_record, indent=2), encoding="utf-8")
    return proc.pid


def needs_credential(harness: dict) -> bool:
    return False
