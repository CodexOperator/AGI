#!/usr/bin/env python3
"""
EXPERIMENT: demonstrate the 30s reaper window gap.

The reaper polls for max_wait_s=30 then exits. If an agent is still alive
when the reaper exits, its future death is invisible. A continuous monitor
(timeout_s-based) would stay alive until ALL agents are terminal.

We test: bounded vs continuous reaper behavior.
"""
import json, sys, tempfile
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "extensions" / "agi" / "bin"))
import dispatch
import completion


class _FakeAdapter:
    def __init__(self):
        self.restart_calls = []
    def is_alive(self, pid):
        return True   # All agents always alive during reaper
    def restart(self, **kw):
        self.restart_calls.append(kw)
        return None


def _setup(project_dir, agent_count=3):
    """Create a minimal session with N running agents."""
    iter_dir = project_dir / "sessions" / "iter-999"
    iter_dir.mkdir(parents=True)

    agents = []
    for i in range(agent_count):
        aid = f"a{i:02d}-agent"
        pid = 5000 + i
        d = iter_dir / aid
        d.mkdir(parents=True)
        rec = {"id": aid, "slot": i, "pid": pid, "status": "running",
               "started_at": 100, "tier": "kid", "node_id": "",
               "context_file": str(d / "ctx.md"), "target": "",
               "restart_count": 0}
        (d / "agent.json").write_text(json.dumps(rec))
        agents.append(rec)

    m = {"iter": 999, "started_at": 100, "timeout_seconds": 600,
         "agents": [{"id": a["id"], "slot": a["slot"], "pid": a["pid"],
                      "status": a["status"], "started_at": a["started_at"],
                      "tier": a["tier"]} for a in agents]}
    (iter_dir / "manifest.json").write_text(json.dumps(m))
    return iter_dir, agents


def _check(iter_dir):
    """Count terminal (caught) vs running (missed) agents."""
    m = json.loads((iter_dir / "manifest.json").read_text())
    terminal = {"done", "pending", "hung-healed", "failed", "done-unreported"}
    caught = sum(1 for e in m.get("agents", []) if e.get("status") in terminal)
    running = sum(1 for e in m.get("agents", []) if e.get("status") == "running")
    return caught, running


def run_simulation(max_wait_s, label):
    """Run _reaper_phase with spec'd max_wait_s. Return (caught, running, n)."""
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        # Minimal project structure
        (root / ".agi").mkdir(parents=True)
        (root / ".agi" / "config.json").write_text("{}")
        (root / ".agi" / "nodes" / "hypothesis").mkdir(parents=True)

        iter_dir, agents = _setup(root, agent_count=3)
        adapter = _FakeAdapter()

        with mock.patch.object(completion, 'is_complete', return_value=False):
            with mock.patch('dispatch.time.sleep', lambda s: None):
                mock_times = [0.0, 0.0, 0.0, max_wait_s + 1.0, max_wait_s + 1.0]
                ti = iter(mock_times)
                with mock.patch('dispatch.time.time', side_effect=lambda: next(ti)):
                    dispatch._reaper_phase(
                        root=root, iter_dir=iter_dir, adapter=adapter,
                        timeout_s=600, max_wait_s=max_wait_s,
                        cap=5, cfg={})

        caught, running = _check(iter_dir)
        return caught, running, len(agents)


def main():
    import json as json_mod
    print("=" * 60)
    print("EXPERIMENT: Reaper window gap")
    print("=" * 60)
    print()
    print("All agents are alive (is_alive=True) throughout.")
    print("Reaper detects nothing and exits at max_wait_s.")
    print("Gap: if an agent dies AFTER the reaper exits, it's invisible.")
    print()

    # Sim 1: current 30s bound
    c1, r1, n1 = run_simulation(max_wait_s=30, label="bounded (30s)")
    print(f"Bounded (max_wait_s=30):")
    print(f"  Caught: {c1}/{n1}")
    print(f"  Running/not caughtt: {r1}/{n1}")
    print(f"  -> Agent lives >30s: reaper exits before death")
    print()

    # Sim 2: continuous 600s bound
    c2, r2, n2 = run_simulation(max_wait_s=600, label="continuous (600s)")
    print(f"Continuous (max_wait_s=600):")
    print(f"  Caught: {c2}/{n2}")
    print(f"  Running/not caught: {r2}/{n2}")
    print(f"  -> Reaper stays alive for 600s, catches any death")
    print()

    bounded_coverage = c1 / n1
    continuous_coverage = c2 / n2

    print("=" * 60)
    print(f"Bounded coverage: {bounded_coverage:.2f}")
    print(f"Continuous coverage: {continuous_coverage:.2f}")
    print(f"Improvement: {(continuous_coverage - bounded_coverage)*100:.0f}%")
    print(f"Hypothesis: {'SUPPORTED' if bounded_coverage < continuous_coverage else 'NOT SUPPORTED'}")
    print()

    # Agent that dies AFTER reaper exits is invisible with bounded reaper
    # but would be caught by continuous reaper
    coverage_gap = continuous_coverage - bounded_coverage
    print(f"METRIC bounded_coverage={bounded_coverage}")
    print(f"METRIC continuous_coverage={continuous_coverage}")
    print(f"METRIC coverage_gap={coverage_gap}")

    result = {
        "bounded_coverage": bounded_coverage,
        "continuous_coverage": continuous_coverage,
        "coverage_gap": coverage_gap,
    }
    result_path = Path("/tmp/reaper_gap_clean.json")
    result_path.write_text(json_mod.dumps(result))
    print(f"Result written to {result_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())