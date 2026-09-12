#!/usr/bin/env python3
"""handoff.py — claim HANDOFF.md sections to read and to write
(`hypothesis:l3w4-handoff-sections-claimable`).

The engine's own `HANDOFF.md` is ~232KB of live scratchpad every cold reader is
told to read first — roughly 46,000 tokens of fixed context tax per seat per
session. That tax is the reason a seat has stayed a one-at-a-time luxury: a
Sonnet seat that reads the whole file has spent much of its usable context
before doing anything. The owner's ask (2026-09-08): *"Each one can claim a
section of handoff to read to conserve individual context space."* A quorum of
seats becomes affordable only when a seat reads its sections, not the file.

This module makes the file's sections **claimable** both to read and to write,
without changing the document format in any way — `cat HANDOFF.md` still yields
exactly the bytes it yields today. It borrows the two proven shapes in the
engine rather than inventing a third locking scheme:

- **Liveness + lease files** from `spawn_budget.py` (goal:g4.8 item 3): a claim
  is a lease file in a gitignored dir, mutated under an `fcntl.flock` lock, and
  reclaimed lazily when the holder pid dies. No release path can leak a claim,
  because a claim is only *believed* while its holder process is alive.
- **Per-reader, non-destructive reads** from `send.py`: reading a section never
  changes the file; a claim is a permission the reader holds, and `release`
  gives it back.

Two halves, the second deliberately the harder one:

1. **Claim to read.** `claim SECT --holder me` serves SECT alone with its byte
   and estimated-token cost, so a seat spends only that. The prime never needs
   a claim: `--prime` reads any section or the whole file.
2. **Claim to write.** A section has at most ONE write holder at a time. `write`
   verifies the caller holds the write claim and **refuses loudly, naming the
   holder** otherwise; the actual read-modify-write of the file takes an
   exclusive lock so two concurrent writers to *different* sections both
   survive, each patching only its own byte range. `--force` reclaims a claim
   whose holder is dead/stale.

The prime stays exempt and stays exempt: `--prime` (or `--holder prime`) reads
whole and writes whole without claiming anything.

Sections are addressed by their `## ` level-2 header text (e.g. `## §4 Traps to
carry (L3)`), never by a position, so a claim survives a rewrite that reorders
or renumbers as long as the header text it names is still present. A `write`
whose first line no longer matches the claimed header is refused — the address
is the header, and a header that moved is a different address.
"""
from __future__ import annotations

import argparse
import errno
import fcntl
import json
import os
import re
import sys
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path

import locations  # NOQA: E402

#: Rough English token estimate — 1 token ~= 4 bytes. Good enough for the
#: "how much context did that section cost me" comparison the claim is about;
#: a real tokenizer is out of scope for a conserving-read, not an accounting.
_TOKENS_PER_BYTE = 4

#: Staleness TTL fallback when a claim names no live pid.
STALE_TTL_S = 3600

HEADING_RE = re.compile(r"(?m)^## (?P<name>[^\r\n]*)[\r\n]?")


# ---------------------------------------------------------------------------
# Locating the handoff and the claims dir
# ---------------------------------------------------------------------------

def handoff_path(root: Path) -> Path:
    """`HANDOFF.md` at the repo root, like rotate.py.

    `HANDOFF.md` is the deliberate exception that lives at the repo root
    (next to `GOALS.md`), not inside the `.agi/` graph dir. `find_project_root`
    resolves to the graph dir, so the handoff is at `repo_root(graph) / "HANDOFF.md"`
    under G11; under the legacy layout repo_root is the identity.
    """
    base = locations.find_project_root(Path(root).resolve())
    if base is None:
        base = Path(root).resolve()
    return locations.repo_root(base) / "HANDOFF.md"


def claims_dir(root: Path) -> Path:
    """`<graph>/sessions/.handoff-claims/` — gitignored session scratch.

    Under `sessions/` (gitignored except `rotations/`), exactly like
    `spawn_budget`'s `.spawn-budget`, so claims never enter the branch.
    """
    base = locations.find_project_root(Path(root).resolve())
    if base is None:
        base = Path(root).resolve()
    return base / locations.SESSIONS_DIR_NAME / ".handoff-claims"


# ---------------------------------------------------------------------------
# Section addressing
# ---------------------------------------------------------------------------

def parse_sections(text: str) -> list[dict]:
    """Split `text` into level-2 sections, each addressed by its header text.

    Returns dicts with `name` (header text after `## `), `start` (byte offset
    of the `## ` line) and `end` (byte offset of the next `## ` line, or EOF).
    `text` is the full section including its header line. Content before the
    first `## ` (the `# SESSION HANDOFF —` preamble) is the prime's envelope
    and is not claimable.
    """
    marks = [(m.start(), m.group("name").strip()) for m in HEADING_RE.finditer(text)]
    out = []
    for i, (start, name) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
        out.append({"name": name, "start": start, "end": end,
                    "text": text[start:end], "bytes": end - start})
    return out


def section_by_name(secs: list[dict], name: str) -> dict | None:
    for s in secs:
        if s["name"] == name:
            return s
    return None


def estimate_tokens(byte_count: int) -> int:
    return max(1, byte_count // _TOKENS_PER_BYTE)


def norm_section(section: str) -> str:
    """Accept a section name with or without its `## ` printed prefix.

    `sections` prints `## <name>` and `claim`/`read`/`write` address a section
    by its bare name; the tool's own output must be copy-pasteable back into
    its own next command (SD.16 friction a). A bare name has no leading `## `
    and is returned unchanged.
    """
    return re.sub(r"^##\s*", "", section).strip()


def _holder_opts(subp, *, required=False):
    """Add `--holder` (canonical) and `--seat` (alias) to a subcommand.

    Every other seat-aware entry point spells it `--seat`; `handoff.py` alone
    used `--holder`. Both write to the same dest so a seat may use either.

    `required` is enforced by the CALLER, never by argparse: marking
    `--holder` required makes argparse demand that exact spelling and reject
    `--seat`, which defeats the alias on the one subcommand that used it
    (measured on `release`, SD.16). The flag stays optional here and the
    handler refuses a missing holder by name.
    """
    subp.add_argument("--holder", help="seat holding the claim")
    subp.add_argument("--seat", "--post", dest="holder",
                      help="alias for --holder")


# ---------------------------------------------------------------------------
# Claims (lease files + flock), following spawn_budget
# ---------------------------------------------------------------------------

def _claim_path(d: Path, section: str, holder: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", f"{holder}__{section}")
    return d / f"{safe}.claim"


def _read_claims(d: Path) -> list[tuple[Path, dict]]:
    if not d.exists():
        return []
    out = []
    for p in sorted(d.glob("*.claim")):
        try:
            out.append((p, json.loads(p.read_text())))
        except (json.JSONDecodeError, OSError):
            out.append((p, {}))
    return out


def _claim_stale(rec: dict) -> bool:
    """A claim is stale when nothing has refreshed it within the TTL.

    The holder is a durable seat identity (`--holder`) that outlives the one
    CLI command that claimed it, so the claiming process's own pid dying is NOT
    staleness — a claim-then-work-then-release seat would otherwise be stale
    before its first write. `claimed_at` is touched on every claim and on every
    write by that holder, so an active seat stays fresh and an abandoned
    claim (holder gone > STALE_TTL_S) is reclaimable with `--force`. The pid
    is recorded as information for the reclaim, never as the judge.
    """
    claimed = float(rec.get("claimed_at", 0) or 0)
    return (time.time() - claimed) > STALE_TTL_S


def _touch_claim(root: Path, section: str, holder: str) -> None:
    """Refresh a holder's claim on `section` so active use never goes stale."""
    d = claims_dir(root)
    with _claims_lock(d):
        for p, rec in _read_claims(d):
            if (rec.get("section") == section and rec.get("holder") == holder):
                rec["claimed_at"] = time.time()
                _write_json(p, rec)
                return


def claim(root: Path, section: str, holder: str, *, write: bool = False,
          force: bool = False, pid: int | None = None) -> dict:
    """Register a read (default) or write claim on `section` for `holder`.

    Returns the claim dict on success, or a dict with `error` describing the
    refusal. A section may host many READ claims but at most ONE WRITE claim;
    a write claim conflicts with everything else on that section. `force`
    reclaims a conflicting claim whose holder is dead/stale.
    """
    d = claims_dir(root)
    text = handoff_path(root).read_text()
    if section_by_name(parse_sections(text), section) is None:
        return {"error": f"no section named {section!r} present in HANDOFF.md"}
    with _claims_lock(d):
        recs = _read_claims(d)
        for _, existing in recs:
            if existing.get("section") != section:
                continue
            if existing.get("holder") == holder:
                continue
            if existing.get("kind") != "write" and not write:
                # another reader on the same section is fine (reads share)
                continue
            if _claim_stale(existing) and force:
                # a dead/stale holder is reclaimable under --force
                continue
            return {"error": f"section {section!r} already held by "
                             f"{existing.get('holder')} ({existing.get('kind')})"}
        rec = {
            "section": section,
            "holder": holder,
            "kind": "write" if write else "read",
            "pid": int(pid or os.getpid()),
            "claimed_at": time.time(),
        }
        _write_json(_claim_path(d, section, holder), rec)
        return rec


def release(root: Path, section: str, holder: str) -> bool:
    d = claims_dir(root)
    with _claims_lock(d):
        for p, rec in _read_claims(d):
            if rec.get("section") == section and rec.get("holder") == holder:
                p.unlink(missing_ok=True)
                return True
    return False


def show_claims(root: Path) -> list[dict]:
    d = claims_dir(root)
    recs = [r for _, r in _read_claims(d) if r.get("section")]
    for r in recs:
        r["stale"] = _claim_stale(r)
    return recs


def _write_json(path: Path, rec: dict) -> None:
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".claim.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as fh:
            json.dump(rec, fh)
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


@contextmanager
def _claims_lock(d: Path):
    """Exclusive lock over the claims dir, so claim/release are atomic.

    Separate from the file lock that serialises the write, so a claim
    mutation never blocks on a slow writer and vice-versa.
    """
    d.mkdir(parents=True, exist_ok=True)
    lock_path = d / ".lock"
    with open(lock_path, "w") as fh:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh.fileno(), fcntl.LOCK_UN)


@contextmanager
def _file_lock(root: Path):
    """Exclusive flock on a lock file beside the handoff.

    Serialises the whole read-modify-write, so two writers on DIFFERENT
    sections both survive: each re-reads after the other's atomic replace and
    patches only its own byte range. The lock file lives in the gitignored
    claims dir, never beside `HANDOFF.md`, so `cat HANDOFF.md` is unaffected.
    """
    d = claims_dir(root)
    d.mkdir(parents=True, exist_ok=True)
    lock_path = d / ".file.lock"
    with open(lock_path, "w") as fh:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh.fileno(), fcntl.LOCK_UN)


# ---------------------------------------------------------------------------
# The read path — serve a claimed section, cheaply
# ---------------------------------------------------------------------------

def read_section(root: Path, section: str, holder: str | None = None, *,
                 prime: bool = False, whole: bool = False) -> dict:
    """Serve one section (or the whole file) with its cost, or refuse.

    A non-prime must hold a claim on the section it reads. `--prime` (or a
    holder of `prime`) may read anything, whole or section, without claiming.
    Never mutates the file.
    """
    path = handoff_path(root)
    text = path.read_text()
    secs = parse_sections(text)
    if whole:
        return {"section": "<whole>", "bytes": len(text),
                "tokens": estimate_tokens(len(text)), "text": text}
    sec = section_by_name(secs, section)
    if sec is None:
        return {"error": f"no section named {section!r} present in HANDOFF.md"}
    if not (prime or (holder or "").lower() == "prime"):
        allowed = any(
            r.get("section") == section and r.get("holder") == holder
            and not r.get("stale")
            for r in show_claims(root)
        )
        if not allowed:
            return {"error": f"{holder} does not hold a claim on section "
                             f"{section!r}; claim it first"}
    return {"section": section, "bytes": sec["bytes"],
            "tokens": estimate_tokens(sec["bytes"]), "text": sec["text"]}


# ---------------------------------------------------------------------------
# The write path — patch ONLY the held section, refuse otherwise
# ---------------------------------------------------------------------------

def write_section(root: Path, section: str, content: str,
                  holder: str | None = None, *, prime: bool = False) -> dict:
    """Replace the SINGLE section `section` with `content`, or refuse.

    Requirements, all enforced:
    - the caller holds a live WRITE claim on `section` (or is `--prime`);
    - `content`'s first line is a `## ` header naming the claimed section;
    - the section still resolves in the current file.

    On refusal the dict carries `error` naming the current holder.
    """
    path = handoff_path(root)
    is_prime = prime or (holder or "").lower() == "prime"
    if not is_prime:
        held = False
        names: list[str] = []
        for r in show_claims(root):
            if r.get("section") == section and r.get("kind") == "write":
                names.append(str(r.get("holder")))
                if r.get("holder") == holder and not r.get("stale"):
                    held = True
        if not held:
            who = names[0] if names else "(none — claim the section for write first)"
            return {"error": f"{holder} does not hold the WRITE claim on section "
                             f"{section!r}; held by {who}"}
        # refresh the claim so active writing never goes stale mid-batch
        _touch_claim(root, section, holder)

    first_line = re.match(r"^## (?P<name>[^\r\n]*)", content)
    if not first_line or first_line.group("name").strip() != section:
        got = first_line.group(0) if first_line else "<not a ## line>"
        return {"error": f"content first line must be a `## ` header naming "
                         f"{section!r} exactly, got {got!r}"}

    with _file_lock(root):
        text = path.read_text()
        sec = section_by_name(parse_sections(text), section)
        if sec is None:
            return {"error": f"section {section!r} no longer present; "
                             f"refusing to write to a moved address"}
        # Splice in the caller's section VERBATIM. Only guard the boundary:
        # if the new section does not end in a newline and a following `## `
        # section is adjacent, insert one so the section cannot swallow the
        # next header. Verbatim + guard means writing a section back with its
        # own original text is byte-identical to not writing at all.
        tail = text[sec["end"]:]
        need = "" if (content.endswith("\n") or not tail.startswith("##")) else "\n"
        new = text[:sec["start"]] + content + need + tail
        _atomic_write(path, new)
    return {"section": section, "bytes": len(new), "ok": True}


def _atomic_write(path: Path, text: str) -> None:
    d = path.parent
    fd, tmp = tempfile.mkstemp(dir=str(d), prefix=".handoff.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as fh:
            fh.write(text)
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".", help="any path inside the project")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_s = sub.add_parser("sections", help="list stable sections with byte/token cost")
    p_s.add_argument("--whole", action="store_true", help="also print whole-file cost")

    p_c = sub.add_parser("claim", help="claim a section (read) or --write it")
    p_c.add_argument("section")
    _holder_opts(p_c)
    p_c.add_argument("--write", action="store_true")
    p_c.add_argument("--force", action="store_true")

    p_r = sub.add_parser("release", help="release a claim")
    p_r.add_argument("section")
    _holder_opts(p_r, required=True)

    p_rd = sub.add_parser("read", help="read one claimed section (or --whole)")
    p_rd.add_argument("section", nargs="?")
    _holder_opts(p_rd)
    p_rd.add_argument("--prime", action="store_true")
    p_rd.add_argument("--whole", action="store_true")

    p_w = sub.add_parser("write", help="replace one held section (see --help)")
    p_w.add_argument("section")
    _holder_opts(p_w)
    p_w.add_argument("--prime", action="store_true")
    p_w.add_argument("--content", help="inline new section text")
    p_w.add_argument("--content-file", type=Path)
    p_w.add_argument("--stdin", action="store_true", help="read new text from stdin")

    p_sh = sub.add_parser("show", help="show current claims")

    args = ap.parse_args(argv)
    root = Path(args.root).resolve()

    # `sections` prints `## <name>`; `claim`/`read`/`write` address a section
    # by its bare name. Accept the tool's own printed form (SD.16 friction a).
    if hasattr(args, "section") and args.section:
        args.section = norm_section(args.section)

    try:
        if args.cmd == "sections":
            path = handoff_path(root)
            text = path.read_text()
            secs = parse_sections(text)
            print(f"file: {path}")
            print(f"  whole: {len(text)} bytes  ~{estimate_tokens(len(text))} tokens")
            for s in secs:
                print(f"  {s['bytes']:>8} B  ~{estimate_tokens(s['bytes']):>6} tok  "
                      f"## {s['name']}")
            return 0

        if args.cmd == "claim":
            if not args.holder:
                print("REFUSED: claim needs --holder <seat> (or --seat)",
                      file=sys.stderr)
                return 1
            res = claim(root, args.section, args.holder, write=args.write,
                        force=args.force)
            if "error" in res:
                print(f"REFUSED: {res['error']}", file=sys.stderr)
                return 1
            served = read_section(root, args.section, args.holder,
                                  prime=args.holder.lower() == "prime")
            print(f"claimed {res['kind']} ## {args.section} for {args.holder}")
            print(f"  {served.get('bytes')} B  ~{served.get('tokens')} tokens")
            print("----")
            print(served.get("text", ""))
            return 0

        if args.cmd == "release":
            # argparse no longer enforces --holder (it would reject the
            # --seat alias), so the handler refuses it by name, as the other
            # subcommands already do.
            if not args.holder:
                print("REFUSED: release needs --holder <seat> (or --seat)",
                      file=sys.stderr)
                return 1
            ok = release(root, args.section, args.holder)
            if ok:
                print(f"released ## {args.section} ({args.holder})")
            else:
                print(f"no live claim by {args.holder} on {args.section}",
                      file=sys.stderr)
            return 0 if ok else 1

        if args.cmd == "read":
            if not (args.holder or args.prime or args.whole):
                print("REFUSED: read needs --holder <seat> (or --prime / --whole)",
                      file=sys.stderr)
                return 1
            res = read_section(root, args.section or "", args.holder,
                               prime=args.prime, whole=args.whole)
            if "error" in res:
                print(f"REFUSED: {res['error']}", file=sys.stderr)
                return 1
            print(f"served {res['section']}: {res['bytes']} B / "
                  f"~{res['tokens']} tokens")
            print("----")
            print(res["text"])
            return 0

        if args.cmd == "write":
            if not (args.holder or args.prime):
                print("REFUSED: write needs --holder <seat> (or --prime)",
                      file=sys.stderr)
                return 1
            if not (args.content or args.content_file or args.stdin):
                print("write needs --content, --content-file or --stdin",
                      file=sys.stderr)
                return 2
            if args.content:
                content = args.content
            elif args.content_file:
                content = args.content_file.read_text()
            else:
                content = sys.stdin.read()
            res = write_section(root, args.section, content, args.holder,
                                prime=args.prime)
            if "error" in res:
                print(f"REFUSED: {res['error']}", file=sys.stderr)
                return 1
            print(f"wrote ## {args.section}: file now {res['bytes']} bytes")
            return 0

        if args.cmd == "show":
            recs = show_claims(root)
            if not recs:
                print("no live claims")
                return 0
            for r in recs:
                stale = " STALE" if r.get("stale") else ""
                print(f"  {r['holder']:<12} {r['kind']:<5} ## {r['section']}{stale}")
            return 0
    except FileNotFoundError as exc:
        print(f"ERR: {exc}", file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())