#!/usr/bin/env python3
"""magic_pane_runner.py — pane runner consumes cutover.deliver (goal:g7.16.1.7.3.5).

ACT surface of the magic pane (goal:g7.16.1.7.3):
  - inbound ONLY via ``magic_pane_cutover.deliver`` (inject → poll enqueue)
  - ``tick`` / ``consume`` drain local poll into ONE render turn per delivery
  - tool RETURN IS the message; channel dm|engine + kind_tag
  - live hook uninstall surgically removes legacy SessionStart /
    UserPromptSubmit delivery commands from a Claude settings.json

Owner falsifier 4: after cutover + this leaf, zero engine events arrive via
send-keys nudge, hook paste, or a second messaging route.

Messaging adapter (``adapters.magic_pane`` / g7.32.2*) and ``send.py`` stay
untouched. Pane owns no transport. Live tmux attach stays deferred.
ONE-pi free lane via ``free_lane_probe`` / pi_adapter + pi.toml.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import magic_pane_cutover as cut
import magic_pane_inject as inj
import magic_pane_poll as poll

ACTIVE_ROUTE = cut.ACTIVE_ROUTE  # tool_call_turn

# Legacy delivery hooks that may still be registered under CC settings.
# Map: substring match in hook command → legacy route name (census).
LEGACY_HOOK_COMMAND_MARKERS: tuple[tuple[str, str, str], ...] = (
    # (settings hook event, command substring, legacy route)
    ("SessionStart", "cc-session-start", "session_start_hook_paste"),
    ("UserPromptSubmit", "rotation_alert", "user_prompt_submit_meter"),
)

DEFAULT_LIVE_SETTINGS = Path.home() / ".claude" / "settings.json"


class MagicPaneRunnerError(ValueError):
    """Runner refused: bad delivery, settings, or off-path call."""


def deliver(
    root: Path,
    post_id: str,
    event_kind: str,
    body: str,
    *,
    routes: dict[str, Any] | None = None,
    path: Path | None = None,
) -> Path:
    """Inbound THE path — thin wrap of cutover.deliver (inject→poll)."""
    return cut.deliver(root, post_id, event_kind, body, routes=routes, path=path)


def render_turn(delivery: dict[str, Any]) -> dict[str, Any]:
    """One pane render turn from a poll delivery.

    ``message`` (== tool_return) is what the tool RETURN carries — the message.
    Shape stays tool_call_turn; channel dm|engine; kind_tag = {channel}.{kind}.
    """
    if not isinstance(delivery, dict):
        raise MagicPaneRunnerError("delivery must be a dict")
    if delivery.get("target_route") != ACTIVE_ROUTE:
        raise MagicPaneRunnerError(
            f"delivery target_route must be {ACTIVE_ROUTE!r}, got "
            f"{delivery.get('target_route')!r}"
        )
    if delivery.get("message_is") != "tool_return":
        raise MagicPaneRunnerError("delivery.message_is must be tool_return")
    channel = delivery.get("channel")
    if channel not in inj.CHANNELS:
        raise MagicPaneRunnerError(f"channel must be dm|engine, got {channel!r}")
    kind_tag = delivery.get("kind_tag")
    if not isinstance(kind_tag, str) or not kind_tag.startswith(f"{channel}."):
        raise MagicPaneRunnerError(f"bad kind_tag: {kind_tag!r}")
    body = delivery.get("tool_return")
    if body != delivery.get("body") or not isinstance(body, str):
        raise MagicPaneRunnerError("body and tool_return must be identical str")
    return {
        "inject_shape": "tool_call_turn",
        "target_route": ACTIVE_ROUTE,
        "channel": channel,
        "kind_tag": kind_tag,
        "event_kind": delivery.get("event_kind"),
        "message": body,  # tool RETURN IS the message
        "tool_return": body,
        "body": body,
        "message_is": "tool_return",
    }


def tick(
    root: Path,
    post_id: str,
    *,
    busy: bool | None = None,
) -> list[dict[str, Any]]:
    """Drain ready cutover deliveries into pane render turns (local refs only).

    Busy → []; idle → one render turn per pending envelope (exactly-once).
    """
    deliveries = poll.poll(root, post_id, busy=busy)
    return [render_turn(d) for d in deliveries]


def consume(
    root: Path,
    post_id: str,
    event_kind: str,
    body: str,
    *,
    busy: bool = False,
    routes: dict[str, Any] | None = None,
    path: Path | None = None,
) -> list[dict[str, Any]]:
    """deliver via cutover then tick once (idle by default).

    Convenience for tests / one-shot: enqueue then surface as render turns.
    If ``busy=True``, enqueue still happens but tick returns [] (held).
    """
    deliver(root, post_id, event_kind, body, routes=routes, path=path)
    return tick(root, post_id, busy=busy)


def mark_busy(root: Path, post_id: str) -> None:
    poll.mark_busy(root, post_id)


def mark_idle(root: Path, post_id: str) -> None:
    poll.mark_idle(root, post_id)


def refuse_legacy(route: str) -> None:
    """Gate the four parent-measured legacy names (incl. non-hook ones)."""
    cut.refuse_legacy_delivery(route)


def plan_hook_uninstall(settings: dict[str, Any]) -> dict[str, Any]:
    """Compute surgical removals; never wipe unrelated hooks."""
    hooks = settings.get("hooks")
    if not isinstance(hooks, dict):
        return {
            "removals": [],
            "kept": 0,
            "legacy_found": [],
            "already_clean": True,
            "hooks_after": {},
        }
    removals: list[dict[str, str]] = []
    kept = 0
    new_hooks: dict[str, list] = {}
    for event, matchers in hooks.items():
        if not isinstance(matchers, list):
            new_hooks[event] = matchers
            continue
        new_matchers: list[Any] = []
        for matcher in matchers:
            if not isinstance(matcher, dict):
                new_matchers.append(matcher)
                continue
            old_list = list(matcher.get("hooks") or [])
            new_list: list[Any] = []
            for h in old_list:
                if not isinstance(h, dict) or h.get("type") != "command":
                    new_list.append(h)
                    kept += 1
                    continue
                cmd = h.get("command")
                legacy = None
                if isinstance(cmd, str):
                    for ev, marker, leg in LEGACY_HOOK_COMMAND_MARKERS:
                        if event == ev and marker in cmd:
                            legacy = leg
                            break
                if legacy:
                    removals.append(
                        {
                            "event": event,
                            "command": cmd,
                            "legacy_route": legacy,
                            "replaced_by": ACTIVE_ROUTE,
                        }
                    )
                else:
                    new_list.append(h)
                    kept += 1
            if new_list:
                m2 = dict(matcher)
                m2["hooks"] = new_list
                new_matchers.append(m2)
        if new_matchers:
            new_hooks[event] = new_matchers
    return {
        "removals": removals,
        "kept": kept,
        "legacy_found": sorted({r["legacy_route"] for r in removals}),
        "already_clean": len(removals) == 0,
        "hooks_after": new_hooks,
    }


def live_hook_uninstall(
    settings_path: Path | None = None,
    *,
    apply: bool = True,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Surgically uninstall legacy delivery hooks from a Claude settings.json.

    Idempotent: second call reports already_clean. Unrelated hooks preserved.
    When the file is missing, returns missing=True (not an error — nothing to
    uninstall). ``apply=False`` or ``dry_run=True`` plans only.
    """
    path = Path(settings_path) if settings_path is not None else DEFAULT_LIVE_SETTINGS
    result: dict[str, Any] = {
        "path": str(path),
        "apply": bool(apply) and not dry_run,
        "missing": False,
        "already_clean": False,
        "removals": [],
        "kept": 0,
        "legacy_found": [],
        "written": False,
    }
    if not path.is_file():
        result["missing"] = True
        result["already_clean"] = True
        result["note"] = "settings file absent — nothing to uninstall"
        return result

    raw = path.read_text(encoding="utf-8")
    try:
        settings = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError as e:
        raise MagicPaneRunnerError(f"settings.json not JSON: {path}: {e}") from e
    if not isinstance(settings, dict):
        raise MagicPaneRunnerError(f"settings.json root must be object: {path}")

    plan = plan_hook_uninstall(settings)
    result["removals"] = plan["removals"]
    result["kept"] = plan["kept"]
    result["legacy_found"] = plan["legacy_found"]
    result["already_clean"] = plan["already_clean"]

    if plan["already_clean"]:
        result["note"] = "no legacy delivery hooks present"
        return result

    if dry_run or not apply:
        result["note"] = "plan only (not written)"
        return result

    new_settings = dict(settings)
    after = plan["hooks_after"]
    if after:
        new_settings["hooks"] = after
    else:
        new_settings.pop("hooks", None)

    bak = path.with_suffix(path.suffix + ".bak-magic-pane-runner")
    if not bak.exists():
        bak.write_text(raw, encoding="utf-8")
        result["backup"] = str(bak)
    path.write_text(json.dumps(new_settings, indent=2) + "\n", encoding="utf-8")
    result["written"] = True
    result["note"] = f"removed {len(plan['removals'])} legacy delivery hook(s)"
    return result


def free_lane_probe() -> dict[str, str]:
    """ONE-pi free lane (no second pi template) — same SoT as cutover/inject."""
    return cut.free_lane_probe()


def main(argv: list[str] | None = None) -> int:
    """CLI: ``uninstall-hooks [--dry-run] [--settings PATH]``."""
    import argparse

    p = argparse.ArgumentParser(prog="magic_pane_runner")
    sub = p.add_subparsers(dest="cmd", required=True)
    u = sub.add_parser("uninstall-hooks", help="live legacy delivery hook uninstall")
    u.add_argument("--settings", type=Path, default=None)
    u.add_argument("--dry-run", action="store_true")
    u.add_argument("--no-apply", action="store_true", help="plan only")
    args = p.parse_args(argv)
    if args.cmd == "uninstall-hooks":
        out = live_hook_uninstall(
            args.settings,
            apply=not args.no_apply,
            dry_run=args.dry_run,
        )
        print(json.dumps(out, indent=2))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
