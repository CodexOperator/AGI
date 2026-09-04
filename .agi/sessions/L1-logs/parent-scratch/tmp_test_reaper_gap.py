#!/usr/bin/env python3
"""Test: does the 30s reaper max_wait_s leave a gap that misses agent deaths?

Simulates agent lifecycle where some agents die within 30s and some after.
Current reaper (max_wait_s=30) should catch only the first group.
A continuous reaper (timeout_s-based) would catch both.

Metric: reaper_detection_rate = detected_deaths / total_deaths
Higher is better. Current architecture bounded at 30s → expected ~0.5 for
staggered deaths spanning 0-60s.
"""
import json
import os
import random
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "extensions" / "agi" / "bin"))

import dispatch  # noqa: E402


class _ControlledAdapter:
    """Adapter that reports `is_alive` based on a per-pid death_time dictionary.

    Each pid has a death_time (seconds since epoch). Before that time,
    `is_alive(pid)` returns True; after, False. This lets us simulate
    staggered agent deaths without real processes or real time.
    """
    def __init__(self, death_times: dict[int, float]):
        self.death_times = death_times
        self.restart_calls = []

    def is_alive(self, pid: int) -> bool:
        now = time.time()
        return self.death_times.get(pid, float('inf')) > now

    def restart(self, **kw):
        self.restart_calls.append(kw)
        pid = kw.get("agent_record", {}).get("pid", 0)
        # Return a new fake pid for the restarted process
        return pid + 10000


def simulate(current_max_wait: int, timeout_s: int = 600) -> tuple[int, int, int, int]:
    """Run _reaper_phase with staggered agent deaths.

    Returns (total_agents, died_after_reaper, died_during_reaper, restarted).
    """
    with tempfile.TemporaryDirectory() as td:
        iter_dir = Path(td) / "sessions" / "iter-1"
        iter_dir.mkdir(parents=True)

        # Create N agents with staggered death times
        n_agents = 10
        death_times = {}
        agents = []
        config_json = {}

        # Agents die at: 5, 10, 15, 20, 25, 35, 40, 45, 50, 55 seconds
        # Reaper runs for max_wait_s = current_max_wait (default 30 on main)
        # First 5 die within the window, last 5 die after
        for i in range(n_agents):
            pid = 1000 + i
            death_delay = 5 + i * 5  # 5, 10, 15, 20, 25, 30, 35, 40, 45, 50
            death_times[pid] = time.time() + death_delay

            agent_id = f"a{i:02d}-test"
            agent_dir = iter_dir / agent_id
            agent_dir.mkdir(parents=True)

            rec = {
                "id": agent_id,
                "slot": i,
                "pid": pid,
                "status": "running",
                "started_at": int(time.time()),
                "tier": "kid",
            }
            (agent_dir / "agent.json").write_text(json.dumps(rec))
            agents.append(rec)

        # Write manifest with all agents
        manifest = {
            "iter": 1,
            "started_at": int(time.time()),
            "timeout_seconds": timeout_s,
            "agents": agents,
        }
        (iter_dir / "manifest.json").write_text(json.dumps(manifest))

        adapter = _ControlledAdapter(death_times)

        # Run reaper with a max_wait_s that limits how long we watch
        # Use 5s poll interval to keep test fast — agents die faster in sim
        dispatch._reaper_phase(
            root=Path(td),
            iter_dir=iter_dir,
            adapter=adapter,
            timeout_s=timeout_s,
            max_wait_s=current_max_wait,
            cap=10,
            cfg={"reaper": {"max_restarts": 1}},
        )

        # Read final manifest to see what was detected
        final = json.loads((iter_dir / "manifest.json").read_text())

        died_during = 0
        died_after = 0
        restarted = 0
        terminal_statuses = {"done", "pending", "hung-healed", "failed"}

        for entry in final.get("agents", []):
            agent_json = iter_dir / entry["id"] / "agent.json"
            if agent_json.exists():
                rec = json.loads(agent_json.read_text())
                status = rec.get("status", "")
                if status == "failed" and "restarted" in rec.get("fail_reason", ""):
                    restarted += 1
                elif status in terminal_statuses:
                    died_during += 1
                elif status == "running":
                    # Agent was never checked — reaper already exited
                    pid = int(rec.get("pid", 0))
                    death_delay = [d for p, d in death_times.items() if p == pid]
                    if death_delay:
                        death_time_elapsed = time.time() - time.time()  # now
                        died_after += 1

        if died_during or died_after or restarted:
            pass

        return n_agents, died_during, died_after, restarted


def main():
    print("=== Experiment: 30s Reaper Window Gap ===")
    print("Simulating 10 agents with staggered death times (5-55s)\n")

    # Test 1: current 30s max_wait
    print("--- Test 1: current reaper (max_wait_s=30) ---")
    n, during, after, restarted = simulate(current_max_wait=30)
    detected = during + restarted
    missed = n - detected
    print(f"Total agents: {n}")
    print(f"Detected (died during reaper window): {detected}")
    print(f"Missed (died after reaper exited): {missed}")
    coverage_current = detected / n if n > 0 else 0

    # Test 2: continuous reaper (timeout_s=600)
    print("\n--- Test 2: continuous reaper (timeout_s=600, max_wait_s=600) ---")
    n, during, after, restarted = simulate(current_max_wait=600, timeout_s=600)
    detected = during + restarted
    missed = n - detected
    coverage_continuous = detected / n if n > 0 else 0
    print(f"Total agents: {n}")
    print(f"Detected (during continuous window): {detected}")
    print(f"Missed: {missed}")

    print(f"\n=== RESULTS ===")
    print(f"Current (30s): detection_rate={coverage_current:.2f}")
    print(f"Continuous (600s): detection_rate={coverage_continuous:.2f}")
    print(f"Improvement: +{(coverage_continuous - coverage_current)*100:.0f}%")

    return 0 if coverage_continuous > coverage_current else 1


if __name__ == "__main__":
    sys.exit(main())