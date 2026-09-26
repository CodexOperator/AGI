"""Box-wide ONE-model slot: run a model-loading command under an exclusive flock.

TMM.198 (a)+(b): a room claim is information, never the gate. Every model-running
command in a swarm runs as

    python3 .agi/context/local-maxxing/model_slot.py -- <command ...>

The lock path is paths.local_maxxing.model_slot_lock, resolved against the MAIN
checkout (paths.main_checkout_root), so every worktree on the box contends for
the same file. Inside the lock, right before the command starts, MemAvailable
(/proc/meminfo) must be >= values.local_maxxing.model_slot_min_avail_gib; the
slot holder re-reads it every --poll seconds up to --wait, then gives up with
exit 75 (EX_TEMPFAIL). The lock is released by the kernel when this process
exits, including an OOM kill of the scope.
"""
import argparse, fcntl, json, os, subprocess, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402

TEMPFAIL = 75


def lock_path():
    rel = json.load(open(paths.config_path()))["paths"]["local_maxxing"]["model_slot_lock"]
    return rel if os.path.isabs(rel) else os.path.join(paths.main_checkout_root(), rel)


def min_avail_gib():
    return float(json.load(open(paths.config_path()))["values"]["local_maxxing"]["model_slot_min_avail_gib"])


def mem_available_gib(meminfo="/proc/meminfo"):
    for line in open(meminfo):
        if line.startswith("MemAvailable:"):
            return int(line.split()[1]) / (1024 * 1024)
    raise RuntimeError("MemAvailable not in %s" % meminfo)


def wait_for_memory(floor, wait_s, poll_s, read=mem_available_gib, sleep=time.sleep, clock=time.monotonic):
    """True once read() >= floor, False if wait_s passes first. Called INSIDE the lock."""
    end = clock() + wait_s
    while True:
        if read() >= floor:
            return True
        if clock() >= end:
            return False
        sleep(poll_s)


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--wait", type=float, default=1800.0, help="max seconds to wait for memory once holding the slot")
    p.add_argument("--poll", type=float, default=10.0)
    p.add_argument("cmd", nargs=argparse.REMAINDER)
    a = p.parse_args(argv)
    cmd = a.cmd[1:] if a.cmd[:1] == ["--"] else a.cmd
    if not cmd:
        p.error("no command given")
    path = lock_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a+") as fh:
        print("[model-slot] waiting for %s" % path, file=sys.stderr, flush=True)
        fcntl.flock(fh, fcntl.LOCK_EX)
        floor = min_avail_gib()
        if not wait_for_memory(floor, a.wait, a.poll):
            print("[model-slot] MemAvailable %.2f GiB < %.2f GiB after %.0f s -- not starting"
                  % (mem_available_gib(), floor, a.wait), file=sys.stderr, flush=True)
            return TEMPFAIL
        fh.seek(0); fh.truncate(); fh.write("pid=%d cmd=%s\n" % (os.getpid(), cmd[0])); fh.flush()
        print("[model-slot] held, MemAvailable %.2f GiB >= %.2f" % (mem_available_gib(), floor), file=sys.stderr, flush=True)
        return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(main())
