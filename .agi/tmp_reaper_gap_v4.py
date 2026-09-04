#!/usr/bin/env python3
"""
EXPERIMENT: 30s reaper window gap.

The reaper polls for max_wait_s=30 then exits. Agents that die AFTER the
reaper exits are invisible. A continuous reaper (timeout_s-based) stays
alive until all agents are terminal.

We simulate staggered agent deaths using a time-aware adapter.
"""
import json, sys, tempfile
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "extensions" / "agi" / "bin"))
import dispatch
import completion


class _TimeAwareAdapter:
    """is_alive returns True for a pid only if sim_time < death_time[pid]."""
    def __init__(self):
        self.death_times = {}   # pid -> death time (seconds from epoch)
        self.restart_calls = []
        self.sim_now = 0.0

    def is_alive(self, pid):
        return self.sim_now < self.death_times.get(pid, float('inf'))

    def restart(self, **kw):
        self.restart_calls.append(kw)
        return None


def _setup(project_dir, agents):
    """Create agent dirs, agent.json, and manifest.json."""
    iter_dir = project_dir / "sessions" / "iter-999"
    iter_dir.mkdir(parents=True)
    for rec in agents:
        d = iter_dir / rec["id"]
        d.mkdir(parents=True)
        (d / "agent.json").write_text(json.dumps(rec))
    manifest = {"iter": 999, "started_at": 100, "timeout_seconds": 600,
                "agents": [{"id": a["id"], "slot": a["slot"], "pid": a["pid"],
                            "status": a["status"], "started_at": a["started_at"],
                            "tier": a["tier"]} for a in agents]}
    (iter_dir / "manifest.json").write_text(json.dumps(manifest))
    return iter_dir


def _check(iter_dir):
    """Count terminal vs running agents from manifest."""
    m = json.loads((iter_dir / "manifest.json").read_text())
    terminal = {"done", "pending", "hung-healed", "failed", "done-unreported"}
    caught = sum(1 for e in m.get("agents", []) if e.get("status") in terminal)
    running = sum(1 for e in m.get("agents", []) if e.get("status") == "running")
    return caught, running


def simulate(max_wait_s, label):
    """Create agents that die at staggered times and run the reaper.

    Return (caught, missed_seen, total). 'missed_seen' = agents that were
    alive during the reaper window and NOT caught.
    """
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / ".agi").mkdir(parents=True)
        (root / ".agi" / "config.json").write_text("{}")
        (root / ".agi" / "nodes" / "hypothesis").mkdir(parents=True)

        # We track elapsed simulated seconds with time.time().
        # Agents die as sim_time passes:
        #   Agent A (pid=5000): dies at sim_time=0.5  (early death)
        #   Agent B (pid=5001): dies at sim_time=0.5  (early death)
        #   Agent C (pid=5002): dies at sim_time=15   (mid death, within 30s)
        #   Agent D (pid=5003): dies at sim_time=45   (LATE death, after 30s)
        # The reaper with max_wait_s=1 and poll_interval=0.2
        # will do about 5 polls (0, 0.2, 0.4, 0.6, 0.8) then exit.
        # 
        # With time mock, we advance time by poll_interval each iteration.
        # We set the adapter's sim_now to the current mock time.
        # Agents die when sim_now >= their death_time.

        agents = [
            {"id": "a00-early",  "slot": 0, "pid": 5000, "status": "running",
             "started_at": 100, "tier": "kid", "node_id": "", "restart_count": 0},
            {"id": "a01-early2", "slot": 1, "pid": 5001, "status": "running",
             "started_at": 100, "tier": "kid", "node_id": "", "restart_count": 0},
            {"id": "a02-mid",    "slot": 2, "pid": 5002, "status": "running",
             "started_at": 100, "tier": "kid", "node_id": "", "restart_count": 0},
            {"id": "a03-late",   "slot": 3, "pid": 5003, "status": "running",
             "started_at": 100, "tier": "kid", "node_id": "", "restart_count": 0},
        ]
        iter_dir = _setup(root, agents)
        adapter = _TimeAwareAdapter()
        adapter.death_times = {5000: 0.5, 5001: 0.5, 5002: 15, 5003: 45}
        pids = [5000, 5001, 5002, 5003]

        # mock time.time to advance by poll_interval each loop iteration
        # The reaper loop does:
        #   deadline = time() + max_wait_s
        #   while time() < deadline:
        #       ... checks (time() used to read current time)
        #       time.sleep(5)  <- we mock to 0
        # So we need time() to:
        #   1. Return progressively larger values
        #   2. Simulate agent death by setting adapter.sim_now = time()

        sim_t = [0.0]  # mutable for closure
        poll_interval = 0.2  # each iteration advances sim time by this much

        def advance_time():
            val = sim_t[0]
            sim_t[0] += poll_interval
            adapter.sim_now = val
            return val

        # Generate as many time values as needed for the loop
        # max_wait_s/poll_interval iterations + 2 for entry + exit
        n_iters = int(max_wait_s / poll_interval) + 2
        time_values = [0.0 + i * poll_interval for i in range(n_iters)]

        with mock.patch.object(completion, 'is_complete', return_value=False):
            with mock.patch('dispatch.time.sleep', lambda s: None):
                with mock.patch('dispatch.time.time', side_effect=time_values + [9999.0]):
                    dispatch._reaper_phase(
                        root=root, iter_dir=iter_dir, adapter=adapter,
                        timeout_s=600, max_wait_s=max_wait_s,
                        cap=5, cfg={})

        # Read results
        caught, running = _check(iter_dir)
        missed_outside = 0
        detected_inside = 0

        for a in agents:
            aid = a["id"]
            pid = a["pid"]
            path = iter_dir / aid / "agent.json"
            rec = json.loads(path.read_text())
            status = rec.get("status", "")
            death_t = adapter.death_times[pid]

            if status in ("failed", "done-unreported"):
                detected_inside += 1
            elif status == "running":
                # Agent was alive during reaper's window and died after exit
                if death_t <= max_wait_s:
                    pass  # should have been caught
                else:
                    missed_outside += 1

        return detected_inside, missed_outside, len(agents)


def main():
    print("=" * 60)
    print("EXPERIMENT: Reaper 30s window gap")
    print("=" * 60)
    print()
    print("Agents with staggered death times:")
    print("  a00-early  (pid=5000): dies at sim_time=0.5")
    print("  a01-early2 (pid=5001): dies at sim_time=0.5")
    print("  a02-mid    (pid=5002): dies at sim_time=15  (within 30s)")
    print("  a03-late   (pid=5003): dies at sim_time=45  (AFTER 30s)")
    print()

    # Test 1: bounded (max_wait_s=1 -> 0.2s within window, rest dies after)
    c1, m1, n1 = simulate(max_wait_s=1, label="bounded")
    coverage1 = c1 / n1 if n1 > 0 else 0
    print(f"Bounded (max_wait_s=1):")
    print(f"  Detected: {c1}/{n1}  Missed (died after window): {m1}/{n1}")
    print(f"  Coverage: {coverage1:.2f}")
    print()

    # Test 2: continuous (max_wait_s=60)
    c2, m2, n2 = simulate(max_wait_s=60, label="continuous")
    coverage2 = c2 / n2 if n2 > 0 else 0
    print(f"Continuous (max_wait_s=60):")
    print(f"  Detected: {c2}/{n2}  Missed: {m2}/{n2}")
    print(f"  Coverage: {coverage2:.2f}")
    print()

    print("=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Bounded coverage:     {coverage1:.2f}")
    print(f"Continuous coverage:  {coverage2:.2f}")
    print(f"Improvement:          +{(coverage2 - coverage1)*100:.0f}%")
    gap = coverage2 - coverage1
    print(f"Gap confirmed:        {'YES' if gap > 0 else 'NO'}")
    print()

    # Key insight: agents dying at 45s (after max_wait_s=1 but within max_wait_s=60)
    print("KEY INSIGHT: With max_wait_s=30 (current), agent a03-late")
    print("dying at sim_time=45 would be MISSED because the reaper")
    print("already exited at sim_time=30. A continuous reaper with")
    print("timeout_s=600 would catch it.")
    print()

    print(f"METRIC bounded_coverage={coverage1}")
    print(f"METRIC continuous_coverage={coverage2}")
    print(f"METRIC coverage_gap={gap}")

    json.dump({
        "bounded": {"detected": c1, "missed": m1, "coverage": coverage1},
        "continuous": {"detected": c2, "missed": m2, "coverage": coverage2},
        "gap": gap,
    }, open("/tmp/reaper_gap_final.json", "w"))
    print(f"\nSaved to /tmp/reaper_gap_final.json")

    return 0


if __name__ == "__main__":
    sys.exit(main())