"""The pi harness. `goal:g4.6`.

**Moved, not rewritten.** `pi_model_args` and `_build_pi_args` lived inline in
`dispatch.py`; their behaviour here is identical, and `tests/test_dispatch.py`
asserts it with its assertions unchanged. Every comment explaining a defect
those functions already fix travels with them, because the defect is a property
of the pi CLI, not of where the code sat:

  - `agent_dispatch.provider/model/thinking` became real pi flags on
    2026-08-31. Until then `_build_pi_args` read the config and used none of
    it, so every kid ran whatever `~/.pi/agent/settings.json` said while the
    key that claims to choose the model chose nothing.
  - A parentless node (a fresh `idea`, which the schema allows) has
    `parent == ""`, and interpolating it produced a command ending in a bare
    `--parent`, which argparse rejects. Emit the flag only with a value.
  - Omitted keys stay omitted rather than defaulting here, so a project that
    configures none of them keeps pi's own settings winning.
  - Without `-p` the final positional prompt starts pi's *interactive TUI*,
    which on a spawned non-TTY process renders nothing and never exits: the
    agent record says `status: running` with a permanently empty `output.log`
    until the timeout fires (observed 2026-09-01, iter 1). `-p` = process the
    prompt and exit, which is the only mode that works headless.
"""
from __future__ import annotations

import os
from pathlib import Path

import brief

NAME = "pi"

#: Fallback only. `harness["bin"]`, then $PI_BIN, then this.
DEFAULT_BIN = "/home/ubuntu/.npm-global/bin/pi"


def resolve_bin(harness: dict) -> str:
    """$PI_BIN wins over config, which wins over the built-in default.

    Env-over-config is deliberate and is the pre-existing behaviour: $PI_BIN is
    how a machine with pi installed somewhere else runs the loop without
    editing a tracked config file.
    """
    return os.environ.get("PI_BIN") or harness.get("bin") or DEFAULT_BIN


def model_args(harness: dict, tier: str) -> list[str]:
    """`provider` / `models[tier]` / `thinking` -> real pi flags.

    `thinking` is the reasoning-effort dial `goal:g4.2` asks for -- pi accepts
    off|minimal|low|medium|high|xhigh -- and is passed for the same reason the
    model is: a model name alone does not say how hard to think.

    A tier missing from `models` is an error naming both the tier and the
    harness. It never falls back to the other tier's model, because tiering the
    model is the entire point of having tiers -- a silent fallback would make a
    parent quietly run on the kid's cheap model and look like it worked.
    """
    args: list[str] = []
    provider = harness.get("provider")
    if isinstance(provider, str) and provider.strip():
        args += ["--provider", provider.strip()]

    models = harness.get("models") or {}
    if models:
        if tier not in models:
            raise KeyError(
                f"harness {harness.get('adapter', NAME)!r} declares no model for "
                f"tier {tier!r}; known tiers: {sorted(models)}"
            )
        model = models[tier]
        if isinstance(model, str) and model.strip():
            args += ["--model", model.strip()]

    thinking = harness.get("thinking")
    if isinstance(thinking, str) and thinking.strip():
        args += ["--thinking", thinking.strip()]
    return args


def child_env(*, harness: dict, base: dict[str, str],
              tier: str | None = None) -> dict[str, str]:
    """The environment the pi process runs in.

    pi needs nothing added; what it needs is the Anthropic credentials taken
    away, and `base` arrives already scrubbed by the shared policy in
    `dispatch.scrubbed_env`. Kept as a real function rather than omitted so the
    interface is uniform -- a harness that DOES need to inject a key has an
    obvious place to do it, and no caller has to ask which adapters have one.
    """
    extra = harness.get("env") or {}
    return {**base, **{k: str(v) for k, v in extra.items()}}


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
    target: str | None = None,
    parallel: int = 1,
    max_live: int = 1,
    brief_tier: str | None = None,
    session_dir: Path | None = None,
    # hypothesis:l3-pi-adapter-role-kwarg -- dispatch.py passes role= and
    # ladder_tier= to EVERY adapter since hypothesis:l3-cc-tools-by-tier
    # (iter-L3.13); only the claude-code adapter uses them (its tool bundle
    # is per role). pi has no tool bundle, so they are accepted and unused --
    # the alternative was every pi spawn dying on a TypeError at the call
    # site, which is what happened to the first tier-0 parent of wave 3.
    role: str | None = None,
    ladder_tier: int | None = None,
) -> list[str]:
    """The argv that starts one pi agent."""
    # hypothesis:l3-pi-install-patch-not-durable -- the L3.38 edit-tool
    # forgiveness patch lives in the SHARED pi install outside this repo, so a
    # `pi` upgrade silently drops it and every kid quietly pays the lost turn
    # again. This is the repo-owned, durable half: at every spawn (and every
    # restart, which also funnels through build_command) gate the installed
    # tool -- re-applying the patch when an upgrade dropped it, and failing
    # LOUDLY naming the fix when re-apply cannot be anchored. Set
    # AGI_PI_FORGIVENESS_BYPASS=1 to disable the gate on an unusual host.
    import pi_edit_forgiveness as _pi_fg
    _fg_status, _fg_detail = _pi_fg.ensure_pi_edit_forgiveness()
    if _fg_status == "fail":
        raise RuntimeError(
            "pi edit tool is missing the L3.38 edits-forgiveness patch and the "
            "repo could not re-apply it automatically; refusing to spawn kids "
            f"who will each waste a turn. {_fg_detail} Fix: repair pi upstream, "
            "or re-apply the _normalizeEditsShapes patch (see "
            "extensions/agi/bin/pi_edit_forgiveness.py). "
            "Set AGI_PI_FORGIVENESS_BYPASS=1 to override."
        )
    if _fg_status == "patched":
        import sys as _sys
        print(_fg_detail, file=_sys.stderr)

    args = [resolve_bin(harness)]
    args += model_args(harness, tier)
    # Headless: process the prompt and exit. Without this flag the prompt is
    # fed to the interactive TUI, which hangs forever off a TTY (empty log).
    args += ["-p"]
    # pi loads a system-prompt file by PLAIN PATH: resolvePromptInput() is
    # `existsSync(input) ? readFileSync(input) : input`. An `@` prefix fails
    # the stat and pi appends the PATH STRING as literal text instead — so
    # every pi agent ran without its rendered graph context, silently, until
    # 2026-09-08 (hypothesis:l3-pi-context-never-delivered). Measured: 79
    # bytes of pathname where a real kid's context.md was 16654 bytes.
    args += ["--append-system-prompt", str(context_file)]
    # goal:g1.9 -- the brief is assembled once, by tier, outside every harness.
    # This adapter decides only how to SPELL a segment on pi's command line.
    # It used to inline the kid brief here, which is why `--tier parent`
    # selected the parent model correctly and then handed it a kid's job.
    # hypothesis:l3w3-advisor-brief — `brief_tier` lets a spawn keep the
    # model tier (parent) while assembling a different tier's brief (advisor).
    _btier = brief_tier or tier
    _sess = session_dir or sess_dir
    for seg in brief.assemble(
        tier=_btier, agent_id=agent_id, iter_n=iter_n, cli_py=cli_py,
        dispatch_py=dispatch_py, scaffold=scaffold, target=target,
        parallel=parallel, max_live=max_live, session_dir=_sess,
    ):
        args += ["--append-system-prompt", seg]
    if skill_prompt is not None and Path(skill_prompt).exists():
        args.extend(["--append-system-prompt", str(skill_prompt)])
    args.append(brief.closing_line(_btier, agent_id, iter_n))
    return args


def is_alive(pid: int) -> bool:
    """Is the process with `pid` still running?

    `os.kill(pid, 0)` sends no signal; it only checks existence. Same pattern
    as `heal.py._pid_alive`, now part of the adapter interface so dispatch.py
    can detect dead agents without importing heal.py (goal:g4.7).
    """
    try:
        import os
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def _restart_cwd(sess_dir: Path, agent_record: dict | None) -> Path:
    """The working directory a restarted agent must be born into.

    `hypothesis:l3-branch-isolation-partial-break`. A `--branch` spawn's
    agent_record carries `worktree` (dispatch.py writes branch_ref["worktree"]
    into it), and the restarted process must re-enter THAT worktree or its
    relative source edits land in the MAIN checkout. The old default,
    `sess_dir.parent.parent.parent`, resolves iter_dir against the dispatch's
    OWN root -- for a top-level dispatch that root is the main checkout, so a
    reaped `--branch` parent was re-spawned with cwd = main, which is exactly
    the observed partial break (source edits in main, coherent worktree).

    A record with no usable `worktree` falls back to the historical derivation
    untouched, so non-branch restarts behave exactly as before.
    """
    if agent_record:
        wt = agent_record.get("worktree")
        if wt:
            worktree = Path(wt).resolve()
            if worktree.is_dir():
                return worktree
    return Path(sess_dir).parent.parent.parent


def restart(
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
    target: str | None = None,
    parallel: int = 1,
    max_live: int = 1,
    agent_record: dict | None = None,
    brief_tier: str | None = None,
) -> int | None:
    """Re-spawn a dead agent. Returns new pid, or None on failure.

    Same signature as `build_command` plus `agent_record` for logging. Rebuilds
    the identical argv and spawns in the same session directory, appending to
    the existing log. Designed for the inline reaper (goal:g4.7): detects dead
    agents, re-spawns them with the same context, and returns the new pid.
    """
    import json
    import os
    import shlex
    import subprocess
    import time

    args = build_command(
        harness=harness, tier=tier, context_file=context_file,
        agent_id=agent_id, iter_n=iter_n, sess_dir=sess_dir,
        scaffold=scaffold, cli_py=cli_py, skill_prompt=skill_prompt,
        dispatch_py=dispatch_py, target=target, parallel=parallel,
        max_live=max_live, brief_tier=brief_tier,
    )
    log_file = sess_dir / "output.log"
    env = child_env(harness=harness, base=dict(os.environ))
    try:
        with open(log_file, "ab") as logf:
            proc = subprocess.Popen(
                args,
                stdout=logf,
                stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
                start_new_session=True,
                cwd=str(_restart_cwd(sess_dir, agent_record)),
                env=env,
            )
    except OSError as exc:
        print(f"restart failed for {agent_id}: {exc}", file=import_sys_stderr())
        return None
    new_pid = proc.pid
    if agent_record is not None:
        agent_record["pid"] = new_pid
        agent_record["status"] = "restarted"
        agent_record["restarted_at"] = int(time.time())
        (sess_dir / "agent.json").write_text(json.dumps(agent_record, indent=2))
    return new_pid


def needs_credential(harness: dict) -> bool:
    """Pi agents authenticate through a minted OpenRouter key."""
    return True


def import_sys_stderr():
    """Lazy import to keep top-level scope clean."""
    import sys
    return sys.stderr
