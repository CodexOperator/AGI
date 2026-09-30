#!/usr/bin/env python3
"""magic_pane_lifecycle.py — spawn/attach hooks → runner tick/consume (g7.16.1.7.3.6+); stand-up/rotate wire (g7.16.1.7.3.7); pane-id×rotation falsifiers (g7.16.1.7.3.8).

Wire the pane runner into **real pane lifecycle** without requiring live tmux
attach: a dry/fixture path proves spawn→consume and attach→tick. Pi extension
events (`session_start` / `before_agent_start` / `tool_result`) mirror CC hooks
(SessionStart / UserPromptSubmit / PostToolUse) and route into these hooks.

Owner (goal:g7.16.1.7.3): ONE pane per post ROW survives rotation; idle receives
within a tick; busy holds mid-turn. ACT: runner surfaces tool_call_turn renders
(tool RETURN IS the message).

Messaging adapter (`adapters.magic_pane` / g7.32.2*) and `send.py` stay
untouched. Live tmux attach stays deferred unless a dry path cannot prove the
contract (standup-wire + pane-id×rotation falsifiers prove it dry).
ONE-pi free lane via `free_lane_probe` / pi_adapter + pi.toml.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import magic_pane_inject as inj
import magic_pane_runner as run

ACTIVE_ROUTE = run.ACTIVE_ROUTE  # tool_call_turn
LIFECYCLE_HOOKS = ("spawn", "attach")

# Pi extension events → lifecycle action (CC-compat mirror from inject SoT).
PI_LIFECYCLE_MAP: dict[str, str] = {
    "session_start": "spawn_or_attach",  # first register = spawn; else attach
    "before_agent_start": "mark_busy",  # mid-turn hold
    "tool_result": "mark_idle_and_tick",  # turn boundary → drain
}

# Default first-turn kind on spawn (engine first_turn_docs).
SPAWN_EVENT_KIND = "first_turn_docs"


class MagicPaneLifecycleError(ValueError):
    """Lifecycle refused: bad pane pin, unknown hook, or dry-path violation."""


def _pane_path(root: Path, post_id: str) -> Path:
    import magic_pane_poll as poll

    poll.validate_post_id(post_id)
    return Path(root) / "posts" / post_id / "pane.json"


def get_pane(root: Path, post_id: str) -> dict[str, Any] | None:
    """Read the registered pane pin for a post (fixture/local refs only)."""
    p = _pane_path(root, post_id)
    if not p.is_file():
        return None
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise MagicPaneLifecycleError(f"pane.json must be object: {p}")
    return data


def register_pane(
    root: Path,
    post_id: str,
    pane_id: str,
    *,
    generation: int = 0,
    dry: bool = True,
) -> dict[str, Any]:
    """Write the pane pin. dry=True is the default — never touches live tmux."""
    if not isinstance(pane_id, str) or not pane_id.strip():
        raise MagicPaneLifecycleError("pane_id must be a non-empty str")
    if not dry:
        raise MagicPaneLifecycleError(
            "live tmux attach deferred (goal:g7.16.1.7.3.6); use dry=True "
            "or a fixture runner seam"
        )
    import magic_pane_poll as poll

    poll.validate_post_id(post_id)
    path = _pane_path(root, post_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "post_id": post_id,
        "pane_id": pane_id.strip(),
        "generation": int(generation),
        "dry": True,
        "live_tmux": False,
    }
    path.write_text(json.dumps(row, indent=2) + "\n", encoding="utf-8")
    return row


def on_spawn(
    root: Path,
    post_id: str,
    *,
    pane_id: str,
    body: str | None = None,
    routes: dict[str, Any] | None = None,
    path: Path | None = None,
    dry: bool = True,
    generation: int = 0,
) -> dict[str, Any]:
    """Spawn hook: register pane pin, then runner.consume(first_turn_docs).

    Dry/fixture path — no live tmux. Returns action=spawn + render turns.
    """
    existing = get_pane(root, post_id)
    if existing is not None:
        raise MagicPaneLifecycleError(
            f"pane already registered for {post_id!r} as "
            f"{existing.get('pane_id')!r}; use on_attach for handoff"
        )
    pin = register_pane(
        root, post_id, pane_id, generation=generation, dry=dry
    )
    msg = body if body is not None else f"SPAWN:{post_id}:first_turn_docs"
    turns = run.consume(
        root,
        post_id,
        SPAWN_EVENT_KIND,
        msg,
        busy=False,
        routes=routes,
        path=path,
    )
    return {
        "action": "spawn",
        "hook": "spawn",
        "pane": pin,
        "turns": turns,
        "event_kind": SPAWN_EVENT_KIND,
        "dry": True,
        "live_tmux": False,
    }


def on_attach(
    root: Path,
    post_id: str,
    *,
    pane_id: str,
    routes: dict[str, Any] | None = None,
    path: Path | None = None,
    dry: bool = True,
    bump_generation: bool = True,
) -> dict[str, Any]:
    """Attach hook: SAME pane_id must survive; then runner.tick drains queue.

    Rotation handoff reuses the pin (owner: pids rotate, panes stay). A
    different pane_id is refused (second pane / orphan). Dry — no live tmux.
    """
    if not dry:
        raise MagicPaneLifecycleError(
            "live tmux attach deferred (goal:g7.16.1.7.3.6); use dry=True"
        )
    existing = get_pane(root, post_id)
    if existing is None:
        raise MagicPaneLifecycleError(
            f"no pane registered for {post_id!r}; call on_spawn first"
        )
    want = pane_id.strip() if isinstance(pane_id, str) else ""
    have = str(existing.get("pane_id") or "")
    if want != have:
        raise MagicPaneLifecycleError(
            f"pane_id survival failed for {post_id!r}: registered {have!r}, "
            f"attach offered {want!r} (ONE pane per post row)"
        )
    gen = int(existing.get("generation") or 0)
    if bump_generation:
        gen += 1
    pin = register_pane(root, post_id, have, generation=gen, dry=True)
    # ensure idle so tick drains (attach = turn boundary for the successor)
    run.mark_idle(root, post_id)
    turns = run.tick(root, post_id, busy=False)
    return {
        "action": "attach",
        "hook": "attach",
        "pane": pin,
        "turns": turns,
        "dry": True,
        "live_tmux": False,
    }


def handle_pi_event(
    root: Path,
    post_id: str,
    event: str,
    *,
    pane_id: str | None = None,
    body: str = "",
    routes: dict[str, Any] | None = None,
    path: Path | None = None,
    dry: bool = True,
) -> dict[str, Any]:
    """Route a pi extension event into lifecycle hooks (CC-compat mirror).

    session_start → spawn (if unregistered) or attach (if pin exists)
    before_agent_start → mark_busy (hold mid-turn)
    tool_result → mark_idle + tick (turn boundary drain)
    """
    action = PI_LIFECYCLE_MAP.get(event)
    if action is None:
        raise MagicPaneLifecycleError(
            f"unknown pi lifecycle event {event!r}; known: "
            f"{sorted(PI_LIFECYCLE_MAP)}"
        )
    if action == "spawn_or_attach":
        if not isinstance(pane_id, str) or not pane_id.strip():
            raise MagicPaneLifecycleError(
                "session_start requires pane_id (dry fixture pin)"
            )
        if get_pane(root, post_id) is None:
            return on_spawn(
                root,
                post_id,
                pane_id=pane_id,
                body=body or None,
                routes=routes,
                path=path,
                dry=dry,
            )
        return on_attach(
            root,
            post_id,
            pane_id=pane_id,
            routes=routes,
            path=path,
            dry=dry,
        )
    if action == "mark_busy":
        run.mark_busy(root, post_id)
        return {
            "action": "mark_busy",
            "hook": "before_agent_start",
            "pi_event": event,
            "turns": [],
            "dry": True,
            "live_tmux": False,
        }
    if action == "mark_idle_and_tick":
        run.mark_idle(root, post_id)
        turns = run.tick(root, post_id, busy=False)
        return {
            "action": "mark_idle_and_tick",
            "hook": "tool_result",
            "pi_event": event,
            "turns": turns,
            "dry": True,
            "live_tmux": False,
        }
    raise MagicPaneLifecycleError(f"unhandled action {action!r}")


# stand_up modes (rotate.STAND_UP_MODES) → lifecycle action
STAND_UP_SPAWN_MODES = frozenset({"spawn"})
STAND_UP_ATTACH_MODES = frozenset({"rotate", "recover", "restart"})
STAND_UP_LIFECYCLE_MODES = STAND_UP_SPAWN_MODES | STAND_UP_ATTACH_MODES


def dry_pane_id(post_id: str) -> str:
    """Stable dry fixture pane pin — survives spawn→rotate without live tmux."""
    import magic_pane_poll as poll

    poll.validate_post_id(post_id)
    return f"dry:{post_id}"


def from_stand_up(
    root: Path,
    post_id: str,
    mode: str,
    *,
    pane_id: str | None = None,
    body: str | None = None,
    routes: dict[str, Any] | None = None,
    path: Path | None = None,
    dry: bool = True,
) -> dict[str, Any]:
    """Wire stand-up/rotate paths → on_spawn / on_attach (dry-safe).

    goal:g7.16.1.7.3.7 — called from ``rotate.stand_up`` after a successful
    body() and from dry-run spawn/rotate paths that skip the launch lock.
    Never requires live tmux; dry=False refuses (deferred).

    Mapping:
      spawn              → on_spawn (or on_attach if a pin already lingered)
      rotate/recover/restart → on_attach (or on_spawn if no pin yet)
    Default pane_id = ``dry:{post}`` so ONE id survives spawn→rotate in fixtures.
    """
    if mode not in STAND_UP_LIFECYCLE_MODES:
        raise MagicPaneLifecycleError(
            f"unknown stand_up mode {mode!r}; known: "
            f"{sorted(STAND_UP_LIFECYCLE_MODES)}"
        )
    if not dry:
        raise MagicPaneLifecycleError(
            "live tmux attach deferred (goal:g7.16.1.7.3.7); use dry=True"
        )
    offered = pane_id.strip() if isinstance(pane_id, str) and pane_id.strip() else None
    existing = get_pane(root, post_id)

    if mode in STAND_UP_SPAWN_MODES:
        if existing is not None:
            # pin lingered across a re-seat — survive the SAME pane_id
            out = on_attach(
                root,
                post_id,
                pane_id=str(existing.get("pane_id") or ""),
                routes=routes,
                path=path,
                dry=True,
            )
            out["stand_up_mode"] = mode
            out["wired_from"] = "stand_up"
            return out
        pid = offered or dry_pane_id(post_id)
        out = on_spawn(
            root,
            post_id,
            pane_id=pid,
            body=body,
            routes=routes,
            path=path,
            dry=True,
        )
        out["stand_up_mode"] = mode
        out["wired_from"] = "stand_up"
        return out

    # attach-family modes
    if existing is None:
        pid = offered or dry_pane_id(post_id)
        out = on_spawn(
            root,
            post_id,
            pane_id=pid,
            body=body,
            routes=routes,
            path=path,
            dry=True,
        )
        out["stand_up_mode"] = mode
        out["wired_from"] = "stand_up"
        return out
    have = str(existing.get("pane_id") or "")
    # survival: attach with registered id (ignore a mismatched offer)
    if offered is not None and offered != have:
        raise MagicPaneLifecycleError(
            f"pane_id survival failed for {post_id!r}: registered {have!r}, "
            f"stand_up({mode}) offered {offered!r}"
        )
    out = on_attach(
        root,
        post_id,
        pane_id=have,
        routes=routes,
        path=path,
        dry=True,
    )
    out["stand_up_mode"] = mode
    out["wired_from"] = "stand_up"
    return out



def orphan_pane_census(
    root: Path, post_id: str | None = None
) -> dict[str, Any]:
    """Census dry pane pins under ``posts/*/pane.json``.

    An orphan is: (a) more than one pane pin file for a post directory, or
    (b) a post whose registered pane_id is empty/missing. With the one-file
    pin layout, (a) is structural (only ``pane.json``); we also track that
    the census sees exactly one pin per post. Returns counts + pin rows.
    """
    posts_root = Path(root) / "posts"
    pins: list[dict[str, Any]] = []
    orphans: list[str] = []
    if posts_root.is_dir():
        for post_dir in sorted(p for p in posts_root.iterdir() if p.is_dir()):
            pid = post_dir.name
            if post_id is not None and pid != post_id:
                continue
            candidates = sorted(post_dir.glob("pane*.json"))
            if len(candidates) > 1:
                orphans.append(pid)
            for c in candidates:
                try:
                    data = json.loads(c.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError):
                    orphans.append(pid)
                    continue
                if not isinstance(data, dict):
                    orphans.append(pid)
                    continue
                pane = str(data.get("pane_id") or "")
                if not pane:
                    orphans.append(pid)
                pins.append(
                    {
                        "post_id": pid,
                        "pane_id": pane,
                        "generation": int(data.get("generation") or 0),
                        "path": str(c.relative_to(root)),
                    }
                )
    orphan_ids = sorted(set(orphans))
    return {
        "pins": pins,
        "orphans": orphan_ids,
        "orphan_count": len(orphan_ids),
        "pin_count": len(pins),
        "dry": True,
        "live_tmux": False,
    }


def prove_pane_rotations(
    root: Path,
    post_id: str,
    n: int = 3,
    *,
    pane_id: str | None = None,
    routes: dict[str, Any] | None = None,
    path: Path | None = None,
    dry: bool = True,
    enqueue_rotation_prompt: bool = True,
) -> dict[str, Any]:
    """Close parent falsifier #2 dry: n rotations → ONE pane_id, 0 orphans.

    goal:g7.16.1.7.3.8 — spawn once via ``from_stand_up(spawn)``, then ``n``
    rotate attaches. Asserts the same pane_id survives, generation == n, and
    ``orphan_pane_census`` reports 0 orphans for the post. Optionally enqueues
    a ``rotation_prompt`` before each rotate so attach tick drains a
    tool_call_turn (rotation event shape through the pane).

    dry=True only; dry=False refuses (live tmux still deferred — dry closes
    this falsifier).
    """
    if not dry:
        raise MagicPaneLifecycleError(
            "live tmux attach deferred (goal:g7.16.1.7.3.8); dry path closes "
            "pane-id\timesrotation falsifiers — use dry=True"
        )
    if not isinstance(n, int) or n < 1:
        raise MagicPaneLifecycleError("n must be an int >= 1 (falsifier uses 3)")

    if get_pane(root, post_id) is not None:
        raise MagicPaneLifecycleError(
            f"prove_pane_rotations expects a fresh post; {post_id!r} already pinned"
        )

    spawn_out = from_stand_up(
        root,
        post_id,
        "spawn",
        pane_id=pane_id,
        body=f"SPAWN:{post_id}:rotation-proof",
        routes=routes,
        path=path,
        dry=True,
    )
    first_id = str(spawn_out["pane"]["pane_id"])
    generations: list[int] = [int(spawn_out["pane"].get("generation") or 0)]
    rotate_outs: list[dict[str, Any]] = []
    drained_tags: list[str] = []

    for i in range(n):
        if enqueue_rotation_prompt:
            run.mark_busy(root, post_id)
            run.deliver(
                root,
                post_id,
                "rotation_prompt",
                f"ROTATE-{i + 1}",
                routes=routes,
                path=path,
            )
            held = run.tick(root, post_id)
            if held:
                raise MagicPaneLifecycleError(
                    f"busy hold failed before rotate {i + 1}: drained {held!r}"
                )
        out = from_stand_up(
            root,
            post_id,
            "rotate",
            pane_id=first_id,
            routes=routes,
            path=path,
            dry=True,
        )
        pid = str(out["pane"]["pane_id"])
        if pid != first_id:
            raise MagicPaneLifecycleError(
                f"pane_id survival failed at rotate {i + 1}: "
                f"expected {first_id!r}, got {pid!r}"
            )
        gen = int(out["pane"].get("generation") or 0)
        generations.append(gen)
        if enqueue_rotation_prompt:
            turns = out.get("turns") or []
            if not turns:
                raise MagicPaneLifecycleError(
                    f"rotate {i + 1} drained no turns (expected rotation_prompt)"
                )
            tag = turns[0].get("kind_tag")
            drained_tags.append(str(tag))
            if tag != "engine.rotation_prompt":
                raise MagicPaneLifecycleError(
                    f"rotate {i + 1} kind_tag {tag!r} != engine.rotation_prompt"
                )
        rotate_outs.append(out)

    final_gen = generations[-1]
    if final_gen != n:
        raise MagicPaneLifecycleError(
            f"generation after {n} rotates expected {n}, got {final_gen}"
        )

    census = orphan_pane_census(root, post_id)
    if census["orphan_count"] != 0:
        raise MagicPaneLifecycleError(
            f"orphans after rotations: {census['orphans']!r}"
        )
    if census["pin_count"] != 1:
        raise MagicPaneLifecycleError(
            f"expected exactly 1 pin for {post_id!r}, got {census['pin_count']}"
        )
    if census["pins"][0]["pane_id"] != first_id:
        raise MagicPaneLifecycleError(
            f"census pane_id {census['pins'][0]['pane_id']!r} != {first_id!r}"
        )

    return {
        "action": "prove_pane_rotations",
        "post_id": post_id,
        "pane_id": first_id,
        "rotations": n,
        "generations": generations,
        "final_generation": final_gen,
        "orphans": census["orphans"],
        "orphan_count": 0,
        "pin_count": 1,
        "drained_kind_tags": drained_tags,
        "spawn": spawn_out,
        "rotates": rotate_outs,
        "census": census,
        "dry": True,
        "live_tmux": False,
        "falsifier": (
            "three rotations \u2192 ONE pane_id, 0 orphans (parent g7.16.1.7.3 #2)"
        ),
    }



def free_lane_probe() -> dict[str, str]:
    """ONE-pi free lane (no second pi template) — same SoT as runner/cutover."""
    return run.free_lane_probe()


def pi_adapter_probe() -> dict[str, Any]:
    """Maximize pi adapter: load + confirm REQUIRED surface (no OPTIONAL_PANE).

    Deliberately does NOT add pane_* to pi (g7.32.3: pi omits OPTIONAL_PANE;
    lifecycle lives here, not on the adapter pane interface).
    """
    import adapters

    pi = adapters.load("pi")
    iface = adapters.pane_interface(pi)
    lane = free_lane_probe()
    return {
        "harness": "pi",
        "adapter": lane["adapter"],
        "template": lane["template"],
        "row": lane["row"],
        "required_ok": all(callable(getattr(pi, n, None)) for n in adapters.REQUIRED),
        "pane_interface": list(iface),  # must be empty for pi
        "lifecycle_hooks": list(LIFECYCLE_HOOKS),
        "note": (
            "lifecycle hooks live in magic_pane_lifecycle (not OPTIONAL_PANE); "
            "pi keeps REQUIRED-only so g7.32.3 holds"
        ),
    }


def main(argv: list[str] | None = None) -> int:
    """CLI: ``probe-lane`` | ``probe-pi``."""
    import argparse

    p = argparse.ArgumentParser(prog="magic_pane_lifecycle")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("probe-lane", help="ONE-pi free lane probe")
    sub.add_parser("probe-pi", help="pi adapter + lifecycle surface probe")
    args = p.parse_args(argv)
    if args.cmd == "probe-lane":
        print(json.dumps(free_lane_probe(), indent=2))
        return 0
    if args.cmd == "probe-pi":
        print(json.dumps(pi_adapter_probe(), indent=2))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
