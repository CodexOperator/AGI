#!/usr/bin/env python3
"""magic_pane_parent_falsifiers.py — parent g7.16.1.7.3 falsifiers #1+#3+#4 (g7.16.1.7.3.9).

Close three parent falsifiers on one dry/fixture leaf:

1) idle multi-event tool_call_turn — memory_alarm + message_receipt +
   rotation_prompt each arrive on an idle post as one render shape
   (tool_call_turn; message_is=tool_return; kind_tag={channel}.{event_kind}).
3) N-post single box-fetch — N posts polling share ONE box network pull per
   fetch interval; pane poll watches LOCAL refs only (never N fetches).
4) negative legacy-route zero — zero engine events via the four legacy routes
   after cutover; route_table shows exactly one active route per event kind.

Messaging adapter (adapters.magic_pane / g7.32.2*) and send.py stay
untouched. Live tmux attach stays deferred. ONE-pi free lane + pi_adapter
REQUIRED-only. Parent goal:g7.16.1.7.3 stays horizon (falsifier #2 closed by
.3.8; this leaf closes #1+#3+#4 — parent complete remains a separate act).
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Callable

import magic_pane_cutover as cut
import magic_pane_inject as inj
import magic_pane_poll as poll

ACTIVE_ROUTE = cut.ACTIVE_ROUTE  # tool_call_turn
LEGACY_ROUTES = cut.LEGACY_ROUTES

# Parent falsifier #1 event set (idle multi-event).
IDLE_MULTI_EVENT_KINDS: tuple[str, ...] = (
    "memory_alarm",
    "message_receipt",
    "rotation_prompt",
)


class MagicPaneParentFalsifierError(ValueError):
    """Parent falsifier proof refused."""


# ---------------------------------------------------------------------------
# Box fetch — ONE network pull for the box; panes poll local refs only.
# ---------------------------------------------------------------------------

_box_network_hook: Callable[[], None] | None = None


def set_box_network_hook(hook: Callable[[], None] | None) -> None:
    """Test seam: counts real box network pulls. Production leaves None."""
    global _box_network_hook
    _box_network_hook = hook


def _box_dir(root: Path) -> Path:
    return Path(root) / "box"


def _remote_inbox(root: Path) -> Path:
    """Staged remote envelopes awaiting the ONE box fetch (not local pane queues)."""
    return _box_dir(root) / "remote_inbox"


def _box_state_path(root: Path) -> Path:
    return _box_dir(root) / "fetch_state.json"


def _read_box_state(root: Path) -> dict[str, Any]:
    sp = _box_state_path(root)
    if not sp.is_file():
        return {"fetch_count": 0, "last_fetch_at": None, "fetched_posts": []}
    data = json.loads(sp.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise MagicPaneParentFalsifierError(f"bad box fetch_state: {sp}")
    return data


def _write_box_state(root: Path, state: dict[str, Any]) -> None:
    sp = _box_state_path(root)
    sp.parent.mkdir(parents=True, exist_ok=True)
    sp.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def stage_remote(
    root: Path,
    post_id: str,
    event_kind: str,
    body: str,
    *,
    routes: dict[str, Any] | None = None,
    path: Path | None = None,
) -> Path:
    """Park an inject envelope in the box remote inbox (pre-fetch; no network).

    Does NOT touch local pane queues and does NOT count as a network pull.
    """
    poll.validate_post_id(post_id)
    data = routes if routes is not None else cut.load_cutover(path)
    env = inj.build_envelope(event_kind, body, routes=data, path=path)
    if env["target_route"] != ACTIVE_ROUTE:
        raise MagicPaneParentFalsifierError("staged envelope off cutover path")
    inbox = _remote_inbox(root)
    inbox.mkdir(parents=True, exist_ok=True)
    seq = len(list(inbox.glob("*.json")))
    name = f"{time.time_ns()}-{seq:04d}-{post_id}.json"
    name = name.replace(":", "_").replace("/", "_")
    dest = inbox / name
    payload = {
        "post_id": post_id,
        "envelope": env,
        "staged_at": time.time(),
    }
    dest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return dest


def box_fetch(root: Path) -> dict[str, Any]:
    """THE one network pull for the box — move remote inbox to local pane queues.

    Invokes the box network hook exactly once per call (spy for falsifier #3).
    Pane poll never calls this; N posts share this single pull.
    """
    if _box_network_hook is not None:
        _box_network_hook()

    inbox = _remote_inbox(root)
    moved: list[dict[str, Any]] = []
    if inbox.is_dir():
        for f in sorted(inbox.glob("*.json"), key=lambda p: p.name):
            data = json.loads(f.read_text(encoding="utf-8"))
            post_id = data["post_id"]
            env = poll.validate_envelope(data["envelope"])
            local = poll.enqueue(Path(root), post_id, env)
            moved.append(
                {
                    "post_id": post_id,
                    "kind_tag": env["kind_tag"],
                    "local_path": str(local),
                    "remote_name": f.name,
                }
            )
            f.unlink()

    state = _read_box_state(root)
    state["fetch_count"] = int(state.get("fetch_count") or 0) + 1
    state["last_fetch_at"] = time.time()
    posts = sorted({m["post_id"] for m in moved})
    prev = list(state.get("fetched_posts") or [])
    state["fetched_posts"] = sorted(set(prev) | set(posts))
    _write_box_state(root, state)

    return {
        "action": "box_fetch",
        "fetch_count": state["fetch_count"],
        "moved": moved,
        "moved_count": len(moved),
        "posts": posts,
        "network_pulls_this_call": 1,
    }


def box_fetch_count(root: Path) -> int:
    return int(_read_box_state(root).get("fetch_count") or 0)


# ---------------------------------------------------------------------------
# Falsifier #1 — idle multi-event tool_call_turn
# ---------------------------------------------------------------------------

def prove_idle_multi_event(
    root: Path,
    post_id: str,
    *,
    kinds: tuple[str, ...] | list[str] | None = None,
    routes: dict[str, Any] | None = None,
    path: Path | None = None,
) -> dict[str, Any]:
    """Parent falsifier #1: idle post receives each kind as a tool_call_turn.

    Enqueues via cutover.deliver (THE path), ensures idle, polls once, asserts
    one delivery per kind with the one render shape + kind_tag.
    """
    data = routes if routes is not None else cut.load_cutover(path)
    use_kinds = tuple(kinds) if kinds is not None else IDLE_MULTI_EVENT_KINDS
    if not use_kinds:
        raise MagicPaneParentFalsifierError("kinds must be non-empty")

    poll.mark_idle(root, post_id)
    if poll.is_busy(root, post_id):
        raise MagicPaneParentFalsifierError(f"post {post_id!r} still busy")

    expected_tags: list[str] = []
    for kind in use_kinds:
        body = f"IDLE-MULTI:{kind}"
        cut.deliver(root, post_id, kind, body, routes=data, path=path)
        row = inj.row_for_kind(data, kind)
        expected_tags.append(str(row["kind_tag"]))

    got = poll.poll(root, post_id, busy=False)
    if len(got) != len(use_kinds):
        raise MagicPaneParentFalsifierError(
            f"idle multi-event expected {len(use_kinds)} turns, got {len(got)}"
        )
    for delivery, kind, tag in zip(got, use_kinds, expected_tags):
        if delivery.get("target_route") != ACTIVE_ROUTE:
            raise MagicPaneParentFalsifierError(
                f"{kind}: target_route {delivery.get('target_route')!r}"
            )
        if delivery.get("message_is") != "tool_return":
            raise MagicPaneParentFalsifierError(
                f"{kind}: message_is {delivery.get('message_is')!r}"
            )
        if delivery.get("inject_shape") != "tool_call_turn":
            raise MagicPaneParentFalsifierError(
                f"{kind}: inject_shape {delivery.get('inject_shape')!r}"
            )
        if delivery.get("kind_tag") != tag:
            raise MagicPaneParentFalsifierError(
                f"{kind}: kind_tag {delivery.get('kind_tag')!r} != {tag!r}"
            )
        if delivery.get("tool_return") != f"IDLE-MULTI:{kind}":
            raise MagicPaneParentFalsifierError(
                f"{kind}: tool_return mismatch {delivery.get('tool_return')!r}"
            )
        if delivery.get("body") != delivery.get("tool_return"):
            raise MagicPaneParentFalsifierError(f"{kind}: body != tool_return")

    if poll.pending_count(root, post_id) != 0:
        raise MagicPaneParentFalsifierError("queue not drained after idle poll")

    return {
        "action": "prove_idle_multi_event",
        "post_id": post_id,
        "kinds": list(use_kinds),
        "kind_tags": expected_tags,
        "deliveries": got,
        "count": len(got),
        "idle": True,
        "falsifier": (
            "parent g7.16.1.7.3 #1 — idle multi-event tool_call_turn "
            "(memory_alarm · message_receipt · rotation_prompt)"
        ),
    }


# ---------------------------------------------------------------------------
# Falsifier #3 — N-post single box-fetch
# ---------------------------------------------------------------------------

def prove_n_post_single_box_fetch(
    root: Path,
    post_ids: list[str] | tuple[str, ...],
    *,
    routes: dict[str, Any] | None = None,
    path: Path | None = None,
    event_kind: str = "message_receipt",
) -> dict[str, Any]:
    """Parent falsifier #3: N posts poll after ONE box network fetch.

    Stages one envelope per post in the box remote inbox, calls box_fetch
    once (network_pulls==1), then each pane poll drains LOCAL refs only
    (pane network spy stays 0). N must be >= 2.
    """
    data = routes if routes is not None else cut.load_cutover(path)
    posts = list(post_ids)
    if len(posts) < 2:
        raise MagicPaneParentFalsifierError(
            "N-post single box-fetch requires N>=2 posts"
        )
    for p in posts:
        poll.validate_post_id(p)

    box_calls = {"n": 0}
    pane_calls = {"n": 0}

    def box_spy() -> None:
        box_calls["n"] += 1

    def pane_spy() -> None:
        pane_calls["n"] += 1

    set_box_network_hook(box_spy)
    poll.set_network_fetch_hook(pane_spy)
    try:
        for i, post in enumerate(posts):
            stage_remote(
                root,
                post,
                event_kind,
                f"NPOST:{post}:{i}",
                routes=data,
                path=path,
            )

        for post in posts:
            if poll.pending_count(root, post) != 0:
                raise MagicPaneParentFalsifierError(
                    f"local queue pre-fetch not empty for {post!r}"
                )
        remote_n = len(list(_remote_inbox(root).glob("*.json")))
        if remote_n != len(posts):
            raise MagicPaneParentFalsifierError(
                f"remote inbox expected {len(posts)}, got {remote_n}"
            )

        fetch_out = box_fetch(root)
        if box_calls["n"] != 1:
            raise MagicPaneParentFalsifierError(
                f"box network pulls expected 1, got {box_calls['n']}"
            )
        if fetch_out["fetch_count"] != 1:
            raise MagicPaneParentFalsifierError(
                f"box fetch_count expected 1, got {fetch_out['fetch_count']}"
            )
        if fetch_out["moved_count"] != len(posts):
            raise MagicPaneParentFalsifierError(
                f"moved_count {fetch_out['moved_count']} != N={len(posts)}"
            )

        deliveries_by_post: dict[str, list[dict[str, Any]]] = {}
        for post in posts:
            poll.mark_idle(root, post)
            got = poll.poll(root, post, busy=False)
            if len(got) != 1:
                raise MagicPaneParentFalsifierError(
                    f"post {post!r} expected 1 delivery after box_fetch, got {len(got)}"
                )
            if got[0].get("target_route") != ACTIVE_ROUTE:
                raise MagicPaneParentFalsifierError(
                    f"post {post!r} off-route {got[0].get('target_route')!r}"
                )
            deliveries_by_post[post] = got

        if pane_calls["n"] != 0:
            raise MagicPaneParentFalsifierError(
                f"pane poll invoked network fetch {pane_calls['n']} times (must be 0)"
            )
        if box_fetch_count(root) != 1:
            raise MagicPaneParentFalsifierError(
                f"box_fetch_count drifted to {box_fetch_count(root)}"
            )
    finally:
        set_box_network_hook(None)
        poll.set_network_fetch_hook(None)

    return {
        "action": "prove_n_post_single_box_fetch",
        "n_posts": len(posts),
        "posts": posts,
        "box_network_pulls": 1,
        "pane_network_pulls": 0,
        "fetch": fetch_out,
        "deliveries": deliveries_by_post,
        "falsifier": (
            "parent g7.16.1.7.3 #3 — N posts on one box polling = 1 network "
            "fetch (the box's), never N"
        ),
    }


# ---------------------------------------------------------------------------
# Falsifier #4 — negative legacy-route zero
# ---------------------------------------------------------------------------

def prove_legacy_route_zero(
    root: Path,
    post_id: str = "post:legacy-zero",
    *,
    routes: dict[str, Any] | None = None,
    path: Path | None = None,
) -> dict[str, Any]:
    """Parent falsifier #4: zero engine events via legacy routes after cutover.

    - Every LEGACY_ROUTE raises on refuse_legacy_delivery / assert_not_legacy.
    - route_table: exactly one active_route=tool_call_turn per event kind;
      legacy names appear only under legacy_bypassed.
    - After attempting every legacy entrypoint, the post queue has 0 pending
      and 0 delivered via legacy (cutover.deliver remains the only path).
    """
    data = routes if routes is not None else cut.load_cutover(path)
    poll.validate_post_id(post_id)

    before_pending = poll.pending_count(root, post_id)
    before_delivered = int(
        poll._read_state(root, post_id).get("delivered") or 0  # noqa: SLF001
    )

    refused: list[str] = []
    for name in sorted(LEGACY_ROUTES):
        try:
            cut.refuse_legacy_delivery(name, post=post_id, body="LEGACY-PROBE")
        except cut.MagicPaneCutoverError:
            refused.append(name)
        else:
            raise MagicPaneParentFalsifierError(
                f"legacy route {name!r} did not raise (expected bypass)"
            )
        try:
            cut.assert_not_legacy(name)
        except cut.MagicPaneCutoverError:
            pass
        else:
            raise MagicPaneParentFalsifierError(
                f"assert_not_legacy({name!r}) did not raise"
            )

    if set(refused) != set(LEGACY_ROUTES):
        raise MagicPaneParentFalsifierError(
            f"refused set {refused!r} != LEGACY_ROUTES"
        )

    table = cut.route_table(data=data)
    kinds = [row["event_kind"] for row in table]
    if len(kinds) != len(set(kinds)):
        raise MagicPaneParentFalsifierError(f"duplicate kinds in route_table: {kinds}")
    for row in table:
        if row["active_route"] != ACTIVE_ROUTE:
            raise MagicPaneParentFalsifierError(f"non-active row: {row}")
        for legacy in row["legacy_bypassed"]:
            if legacy not in LEGACY_ROUTES:
                raise MagicPaneParentFalsifierError(
                    f"unknown legacy in table: {legacy!r}"
                )
            st = cut.legacy_status(legacy, data=data)
            if st["status"] != "bypassed" or st["replaced_by"] != ACTIVE_ROUTE:
                raise MagicPaneParentFalsifierError(f"legacy status bad: {st}")

    after_pending = poll.pending_count(root, post_id)
    after_delivered = int(
        poll._read_state(root, post_id).get("delivered") or 0  # noqa: SLF001
    )
    if after_pending != before_pending:
        raise MagicPaneParentFalsifierError(
            f"legacy probes mutated pending: {before_pending} -> {after_pending}"
        )
    if after_delivered != before_delivered:
        raise MagicPaneParentFalsifierError(
            f"legacy probes delivered events: {before_delivered} -> {after_delivered}"
        )

    cut.deliver(root, post_id, "memory_alarm", "VIA-CUTOVER", routes=data, path=path)
    poll.mark_idle(root, post_id)
    got = poll.poll(root, post_id, busy=False)
    if len(got) != 1 or got[0].get("tool_return") != "VIA-CUTOVER":
        raise MagicPaneParentFalsifierError(
            f"cutover positive control failed: {got!r}"
        )

    return {
        "action": "prove_legacy_route_zero",
        "post_id": post_id,
        "legacy_routes_refused": refused,
        "legacy_events_delivered": 0,
        "route_table_kinds": kinds,
        "active_route": ACTIVE_ROUTE,
        "cutover_positive_control": got[0],
        "falsifier": (
            "parent g7.16.1.7.3 #4 — negative legacy-route zero after cutover; "
            "census route_table one active route per event kind"
        ),
    }


# ---------------------------------------------------------------------------
# Combined proof + lane probes
# ---------------------------------------------------------------------------

def prove_parent_falsifiers_134(
    root: Path,
    *,
    idle_post: str = "post:idle-multi",
    n_posts: list[str] | None = None,
    legacy_post: str = "post:legacy-zero",
    routes: dict[str, Any] | None = None,
    path: Path | None = None,
) -> dict[str, Any]:
    """Run parent falsifiers #1 + #3 + #4 in one dry proof (g7.16.1.7.3.9)."""
    data = routes if routes is not None else cut.load_cutover(path)
    posts = n_posts or [f"post:n{i}" for i in range(1, 4)]  # N=3 default
    f1 = prove_idle_multi_event(root, idle_post, routes=data, path=path)
    f3 = prove_n_post_single_box_fetch(root, posts, routes=data, path=path)
    f4 = prove_legacy_route_zero(root, legacy_post, routes=data, path=path)
    return {
        "action": "prove_parent_falsifiers_134",
        "goal": "goal:g7.16.1.7.3.9",
        "falsifiers_closed": [1, 3, 4],
        "idle_multi_event": f1,
        "n_post_single_box_fetch": f3,
        "legacy_route_zero": f4,
        "dry": True,
        "live_tmux": False,
        "parent_stays_horizon": True,
        "note": (
            "parent g7.16.1.7.3 stays horizon until an explicit complete act; "
            "falsifier #2 closed by .3.8; this leaf closes #1+#3+#4"
        ),
    }


def free_lane_probe() -> dict[str, str]:
    """ONE-pi free lane (no second pi template)."""
    return cut.free_lane_probe()


def pi_adapter_probe() -> dict[str, Any]:
    """Maximize pi adapter: REQUIRED surface only (no OPTIONAL_PANE)."""
    import adapters

    pi = adapters.load("pi")
    iface = adapters.pane_interface(pi)
    lane = free_lane_probe()
    return {
        "harness": "pi",
        "adapter": lane["adapter"],
        "template": lane["template"],
        "row": lane["row"],
        "required_ok": all(
            callable(getattr(pi, n, None)) for n in adapters.REQUIRED
        ),
        "pane_interface": list(iface),  # must be empty for pi
        "note": (
            "parent-falsifier proofs live in magic_pane_parent_falsifiers "
            "(not OPTIONAL_PANE); pi keeps REQUIRED-only so g7.32.3 holds"
        ),
    }


def main(argv: list[str] | None = None) -> int:
    import argparse

    p = argparse.ArgumentParser(prog="magic_pane_parent_falsifiers")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("probe-lane", help="ONE-pi free lane probe")
    sub.add_parser("probe-pi", help="pi adapter REQUIRED-only probe")
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
