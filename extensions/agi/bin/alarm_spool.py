#!/usr/bin/env python3
"""alarm_spool.py -- ONE SPOOL PER SENDING SEAT: every alarm is a signed box message, and only the seat signs it.

goal:g7.16.1.11.20.2 (owner 21:1xZ-21:2xZ 10-11: "All alarms" on the new mail; council 3/3 21:3xZ: a seat's key signs
only in the seat's own uid, root signing as a seat is RED under .40.1 item 4).

  append  a plain JSON line {id, job, to, text, ts} appended to THIS uid's ~/alarm.spool. No key, no box, one write
          under PIPE_BUF so concurrent appenders (a root source's `runuser -u agi-<seat> -- ... append`, a cron row in
          the seat's uid) never interleave. Refuses beyond --max-lines (stderr, rc 3): the spool is bounded.
  drain   in the SENDING seat's own uid (refuses any other, rc 2): for every spooled line the box tool, run from ~/t, mails it to <to> with
          AGI_POST=<seat>, so the seat's own key signs. The message is `[alarm <job>] <text>` plus the trailers
          `Alarm-job: <job>` and `Alarm-id: <id>`, so a reader tells the seat's word from its machine.

EXACTLY ONCE. The spool is renamed to alarm.spool.draining before it is read (an appender recreates alarm.spool, so a
rewrite never races an append); a line that fails stays and is put back by APPEND after the pass, with one ~/.notice
line, and is retried next run. Before every send the seat's own refs/box/<seat>/<to> is searched for the line's
Alarm-id: a crash between the send and the unlink re-reads the line next run, finds the id, and sends nothing twice.
A drain that finds a lock held prints `[busy]` and does nothing (rc 0).
An APPENDER cannot be locked out (a root source must never wait on the seat), so it checks instead: after its write it compares
the inode behind its fd with the spool's (ENOENT = different); a different one means the drain moved the spool aside between the
open and the write, and the same line goes in again (a copy the drain already sent is a no-op, its Alarm-id is on the seat's ref).

DEAD LETTER. Each failed pass counts on the line (`tries`); at --max-tries (a config:crons cell) the line moves to
alarm.spool.dead with ONE ~/.notice line and is never retried: a reader that can never be reached (off-matrix, a
squatted ref) cannot hold the spool, or a minute-by-minute retry, for ever.
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import secrets
import subprocess
import sys
import time
from pathlib import Path

try:
    import geometry_config
except ImportError:      # the single-file copy installed under /opt/agi/bin has no engine beside it (a root source runs only `append` there, which has no --seat): the same plain store, without the deprecation notice
    class geometry_config:
        class SeatAction(argparse.Action):
            def __call__(self, parser, namespace, values, option_string=None):
                setattr(namespace, self.dest, values)

SPOOL_NAME = "alarm.spool"
DRAINING = SPOOL_NAME + ".draining"
LINE_MAX = 3800        # one write(2) under PIPE_BUF (4096): an O_APPEND write of this size is atomic
REAPPENDS = 5          # an append whose spool was drained under it goes in again this many times at most
GIT_LOOKBACK = 500     # messages of the seat's own out-ref searched for an Alarm-id


def home() -> Path:
    return Path(os.path.expanduser("~"))


def _uid_name() -> str:
    import pwd  # noqa: PLC0415
    return pwd.getpwuid(os.getuid()).pw_name


def spool_path() -> Path:
    return home() / SPOOL_NAME


def new_id(now: float) -> str:
    return f"{int(now):08x}-{secrets.token_hex(2)}"


def append(job: str, to: str, text: str, *, spool: Path | None = None, max_lines: int = 500,
           now: float | None = None) -> str | None:
    """None when appended, else WHY NOT. One O_APPEND write of one line."""
    spool = spool or spool_path()
    now = time.time() if now is None else now
    text = " ".join(str(text).split())
    while True:
        line = json.dumps({"id": new_id(now), "job": job, "to": to, "text": text,
                           "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))},
                          separators=(",", ":")) + "\n"
        if len(line.encode()) <= LINE_MAX or not text:
            break
        text = text[: max(0, len(text) - 200)]
    try:
        have = sum(1 for _ in spool.open("rb")) if spool.exists() else 0
        if have >= max_lines:
            return f"{spool} holds {have} lines (>= --max-lines {max_lines}): the drain is not keeping up"
        for _ in range(REAPPENDS):
            fd = os.open(spool, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
            try:
                os.write(fd, line.encode())
                # The drain renames the spool aside, reads it and unlinks it. A write through an fd opened BEFORE that rename
                # lands in a file about to be deleted (or already read): the inode behind the fd is no longer the spool's.
                # Then the SAME line (same Alarm-id) goes in again; a double the drain already sent is a no-op (the id is searched).
                try:
                    same = os.fstat(fd).st_ino == os.stat(spool).st_ino
                except FileNotFoundError:
                    same = False
            finally:
                os.close(fd)
            if same:
                return None
        return f"{spool} was replaced {REAPPENDS} times while appending"
    except OSError as exc:
        return f"{spool}: {exc}"


def message(rec: dict) -> str:
    return f"[alarm {rec['job']}] {rec['text']}\n\nAlarm-job: {rec['job']}\nAlarm-id: {rec['id']}\n"


def already_sent(tree: Path, seat: str, to: str, alarm_id: str) -> bool:
    """True when the seat's OWN out-ref already carries this Alarm-id (a send whose unlink never ran)."""
    try:
        r = subprocess.run(["git", "-C", str(tree), "log", f"refs/box/{seat}/{to}", "-n", str(GIT_LOOKBACK),
                            "--format=%B"], capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return False
    return r.returncode == 0 and f"Alarm-id: {alarm_id}" in r.stdout.splitlines()


def _send(seat: str, rec: dict, tree: Path, box_bin: Path) -> str | None:
    try:
        r = subprocess.run([str(box_bin), "send", rec["to"]], input=message(rec), capture_output=True, text=True,
                           timeout=60, cwd=tree, env={**os.environ, "AGI_POST": seat})
    except (OSError, subprocess.SubprocessError) as exc:
        return f"{box_bin} send {rec['to']} failed: {exc}"
    if r.returncode != 0:
        return f"{box_bin} send {rec['to']} exit {r.returncode}: {(r.stderr or r.stdout).strip()[:200]}"
    return None


def _notice(notice_bin: Path, line: str) -> None:
    try:
        subprocess.run([str(notice_bin), "add", line], capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"alarm_spool: ~/.notice line NOT written: {exc}", file=sys.stderr)


def drain(seat: str, *, max_tries: int, spool: Path | None = None, box_bin: Path = Path("/opt/agi/bin/box"),
          notice_bin: Path | None = None, tree: Path | None = None) -> int:
    me = _uid_name()
    if me != f"agi-{seat}":
        print(f"alarm_spool: uid {me} cannot drain {seat}'s spool (the drain must run as agi-{seat}: its key signs)",
              file=sys.stderr)
        return 2
    spool = spool or spool_path()
    draining = spool.with_name(spool.name + ".draining")
    tree = tree or home() / "t"
    notice_bin = notice_bin or home() / "bin" / "agi-notice"
    spool.parent.mkdir(parents=True, exist_ok=True)
    lock = os.open(spool.with_name(spool.name + ".lock"), os.O_WRONLY | os.O_CREAT, 0o600)
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print("alarm_spool: [busy] another drain holds the lock")
        return 0
    try:
        if not draining.exists():
            if not spool.exists() or spool.stat().st_size == 0:
                return 0
            os.rename(spool, draining)                       # appenders recreate `spool`: no rewrite ever races an append
        kept: list[str] = []
        for raw in draining.read_text().splitlines():
            try:
                rec = json.loads(raw)
                rec["id"], rec["job"], rec["to"], rec["text"]
            except (ValueError, KeyError, TypeError):
                _notice(notice_bin, f"[alarm-spool-bad] {raw[:120]}")
                print(f"alarm_spool: unreadable spool line dropped: {raw[:80]!r}", file=sys.stderr)
                continue
            if already_sent(tree, seat, rec["to"], rec["id"]):
                continue                                     # sent before a crash, never twice
            why = _send(seat, rec, tree, box_bin)
            if why is None:
                print(f"alarm_spool: sent {rec['id']} [alarm {rec['job']}] -> {rec['to']}")
                continue
            rec["tries"] = int(rec.get("tries", 0)) + 1
            if rec["tries"] >= max_tries:
                with spool.with_name(spool.name + ".dead").open("a") as dead:
                    dead.write(json.dumps(rec, separators=(",", ":")) + "\n")
                print(f"alarm_spool: {rec['id']} [alarm {rec['job']}] -> {rec['to']} DEAD after {rec['tries']} tries: {why}", file=sys.stderr)
                _notice(notice_bin, f"[alarm-dead] {rec['id']} {rec['job']} -> {rec['to']} after {rec['tries']} tries: {why}")
                continue
            kept.append(json.dumps(rec, separators=(",", ":")))
            print(f"alarm_spool: {rec['id']} [alarm {rec['job']}] -> {rec['to']} NOT sent, kept (try {rec['tries']} of {max_tries}): {why}", file=sys.stderr)
            if rec["tries"] == 1:                           # ONE notice per line per episode: the first failure (then [alarm-dead] at the end), not every failed minute
                _notice(notice_bin, f"[alarm-unsent] {rec['id']} {rec['job']} -> {rec['to']}: {why}")
        if kept:
            fd = os.open(spool, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
            try:
                os.write(fd, ("\n".join(kept) + "\n").encode())
            finally:
                os.close(fd)
        draining.unlink()
        return 0
    finally:
        os.close(lock)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    sub = ap.add_subparsers(dest="verb", required=True)
    ap_a = sub.add_parser("append", help="append one alarm line to this uid's spool (no key, no box)")
    ap_a.add_argument("--job", required=True)
    ap_a.add_argument("--to", required=True, help="the reader: the post the seat's drain mails it to")
    ap_a.add_argument("--text", required=True)
    ap_a.add_argument("--max-lines", type=int, required=True)
    ap_a.add_argument("--spool", type=Path, default=None)
    ap_d = sub.add_parser("drain", help="sign + box-send every spooled line, as the sending seat")
    ap_d.add_argument("--seat", "--post", action=geometry_config.SeatAction, required=True)
    ap_d.add_argument("--max-tries", type=int, required=True, help="failed passes before a line is dead-lettered to alarm.spool.dead")
    ap_d.add_argument("--spool", type=Path, default=None)
    ap_d.add_argument("--box-bin", type=Path, default=Path("/opt/agi/bin/box"))
    ap_d.add_argument("--notice-bin", type=Path, default=None)
    ap_d.add_argument("--tree", type=Path, default=None)
    a = ap.parse_args(argv)
    if a.verb == "append":
        why = append(a.job, a.to, a.text, spool=a.spool, max_lines=a.max_lines)
        if why:
            print(f"alarm_spool: NOT appended: {why}", file=sys.stderr)
            return 3
        return 0
    return drain(a.seat, max_tries=a.max_tries, spool=a.spool, box_bin=a.box_bin, notice_bin=a.notice_bin, tree=a.tree)


if __name__ == "__main__":
    sys.exit(main())
