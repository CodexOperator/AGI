#!/usr/bin/env python3
"""sensei.py — the Master Sensei of the seat system (hypothesis:l3w4-master-sensei).

A training/tuning role. It keeps track of where agents fail, proposes a
harness/seat change to the failing role and its direct supervisor, and
applies it once both have replied after the proposal timestamp. It never
touches Belam or his advisors (tier-3 parents) without explicit owner
approval; for those it drafts a file and dms the liaison instead.

Two axes, deliberately non-circular: sanctuary-master rotates every Master
including the Sensei; the Sensei improves every Master including
sanctuary-master (safe because sanctuary-master's own `rotated_by` is
`quorum`, not the Sensei).

Usage (all read config:seats from the nearest graph root):

    sensei.py pick_worst --ledger PATH          # pure: worst row(s)
    sensei.py propose --target SEAT --change TX # dm seat + supervisor
    sensei.py   apply --target SEAT --node-id N --change TX --since TS \\
                      [--supervisor SEAT] [--owner-approved] [--dry-run]

The `ts` a `propose` prints is the `--since` handle for a matching `apply`.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

try:  # runs from extensions/agi/bin/ as part of the package
    from . import locations, node_writer, rotate, send as _send
except ImportError:  # runs as a plain script from a checkout
    import locations  # type: ignore
    import node_writer  # type: ignore
    import rotate  # type: ignore
    import send as _send  # type: ignore

SENSEI = "master-sensei"
ROOM_QUORUM = "tier3-quorum"  # the one room that reaches the prime's seat
LIAISON = "liaison"
DRAFTS_DIR = "sessions/sensei/drafts"  # relative to the GRAPH root (.agi/), like .agi/sessions/
MSG_PREFIX = "[sensei #propose] "

# Roles the Sensei may never change on its own authority. Belam is the
# prime; the advisors are the tier-3 parents embodying the visions. Both need
# the owner's explicit `--owner-approved` flag (owner 9).
PROTECTED_ROLES = {"prime_director", "parent"}


# ── seats loading ────────────────────────────────────────────────────────


def load_seats(root: Path) -> list[dict]:
    """Parse the `seats:` list out of config:seats's frontmatter.

    Uses node_writer.find_node_file so the row file is located exactly the
    way every other reader locates it, then a minimal YAML list parse (the
    seats schema is flat JSON objects on lines, so a document split of the
    `seats:` block is enough).
    """
    nf = node_writer.find_node_file(root, "config:seats")
    if nf is None:
        return []
    text = nf.read_text(encoding="utf-8")
    fm = text.split("---", 2)[1] if text.startswith("---") else ""
    in_seats = False
    rows: list[dict] = []
    for line in fm.splitlines():
        if line.strip().startswith("seats:"):
            in_seats = True
            continue
        if in_seats:
            if line.strip().startswith("-"):
                import json as _json

                payload = line.strip()[1:].strip()
                try:
                    rows.append(_json.loads(payload))
                except Exception:
                    continue
            elif line.strip() and not line.startswith((" ", "-")):
                break  # next frontmatter key
        elif line.strip().startswith(("locations:", "edited_by:", "thought")):
            pass
    return rows


def seat_row(rows: list[dict], name: str) -> dict | None:
    for r in rows:
        if (r.get("name") or "").strip() == name:
            return r
    return None


# ── supervisor resolution ────────────────────────────────────────────────


def _direct_supervisor(row: dict) -> tuple[str, str] | None:
    """Which thread the seat's direct supervisor lives on.

    `rotated_by in {quorum, advisor, prime}` reaches the prime's seat through
    the one room (owner 4: no seat but the quorum reaches Belam) — returns
    `("room", "tier3-quorum")`. Any other named `rotated_by` is a dm to that
    seat — `("dm", <name>)`. No `rotated_by` means no supervisor thread.
    """
    rotated_by = (row.get("rotated_by") or "").strip()
    if rotated_by in ("quorum", "advisor", "prime"):
        return ("room", ROOM_QUORUM)
    if rotated_by:
        return ("dm", rotated_by)
    return None


def _required_threads(row: dict | None, target: str,
                      supervisor_flag: str | None) -> list[tuple[str, str]]:
    """The threads that must show a reply before an apply proceeds.

    A seat row contributes its own dm plus its supervisor thread; an
    ephemeral target (no row in config:seats) contributes only the supervisor
    thread, which must come from `--supervisor` (there is no role dm to ping).
    """
    if row is None:
        if not supervisor_flag:
            raise ValueError(
                f"ephemeral target {target!r} has no seat row; "
                f"--supervisor SEAT is required")
        return [("dm", supervisor_flag)]
    threads: list[tuple[str, str]] = [("dm", target)]
    sup = _direct_supervisor(row)
    if sup is not None:
        threads.append(sup)
    return threads


# ── pick_worst ───────────────────────────────────────────────────────────


def load_ledger_rows(path: Path) -> list[dict]:
    """Read a failure ledger file into `pick_worst`-shaped rows.

    Failures.py `ledger()` writes an indented JSON **array** (and the
    `aggregate()` step writes the `seat_or_role/fail_rate/failed` rate table
    the same way), while any hand-made or legacy file may be JSONL (one
    record per line). This reads both: try the whole file as one JSON array
    (or object), fall back to JSONL. Returns [] for an empty or unreadable
    file.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []
    if not text.strip():
        return []
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        data = None
    if isinstance(data, list):
        return [r for r in data if isinstance(r, dict)]
    if isinstance(data, dict):
        # tolerate a bare object / the failure-rates table
        if isinstance(data.get("rows"), list):
            return [r for r in data["rows"] if isinstance(r, dict)]
        return [data]
    rows: list[dict] = []
    for ln in text.splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            obj = json.loads(ln)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            rows.append(obj)
    return rows



def pick_worst(rows: list[dict]) -> dict | None:
    """The worst `(seat_or_role, model)` group from the failure ledger.

    Pure. Each input row is a ledger row with `seat_or_role`, `model`,
    `fail_rate` and `failed` keys. Groups by `(seat_or_role, model)`; the
    worst fail rate wins; ties break by higher failure count, then by seat
    name for a stable answer. Returns one representative row, or None for no
    rows.
    """
    best: dict | None = None
    for r in rows:
        rate = r.get("fail_rate", 0.0) or 0.0
        if best is None:
            best = dict(r)
            continue
        if rate > (best.get("fail_rate", 0.0) or 0.0):
            best = dict(r)
        elif rate == (best.get("fail_rate", 0.0) or 0.0):
            b_count = best.get("failed", 0) or 0
            if (r.get("failed", 0) or 0) > b_count:
                best = dict(r)
            elif (r.get("failed", 0) or 0) == b_count:
                if (r.get("seat_or_role", "") or "") < (
                        best.get("seat_or_role", "") or ""):
                    best = dict(r)
    return best


# ── reply checking / timestamps ──────────────────────────────────────────


def _normts(ts: str) -> str:
    ts = (ts or "").strip()
    return ts.replace("Z", "+00:00") if ts.endswith(("Z", "z")) else ts


def _after(block_ts: str, since: str) -> bool:
    """True when block_ts is strictly after `since`. Both ISO; lexicographic
    compare after a Z→+00:00 normalisation keeps pure-UTC stamps aligned."""
    return bool(_normts(block_ts) > _normts(since))


def _has_reply(croot: Path, thread: tuple[str, str], since: str, *,
               me: str = SENSEI) -> bool:
    """A block after `since` sent by someone other than the Sensei himself."""
    kind, name = thread
    if kind == "room":
        path = _send._room_path(croot, name)
    else:
        a, b, _ = _send._dm_pair(me, name)
        path = _send._dm_path(croot, me, name)
    for b in _send._read_conv(path):
        if not _after(b.get("ts", ""), since):
            continue
        sender = (b.get("from") or "").strip()
        if sender not in ("", me):
            return True
    return False


# ── wake-audit ────────────────────────────────────────────────────────────
# The section-2 measurement master-sensei's whole duty runs on (owner
# 2026-09-11 12:4xZ order; hypothesis:l3w4-master-sensei): run the
# startup-wake classification that the seat has been doing by hand every
# rotation. Reads the seat's LIVE config:rotations template fresh each run —
# never a hardcoded list (hypothesis:sensei-wake-audit-subcommand).

CATEGORY_NAMES = {
    "a": "re-derives a fact already in ## facts or a first_turn output",
    "b": "a read a first_turn entry could pre-run but doesn't yet",
    "c": "protocol learning (-h, source/log grepping)",
    "d": "real work (window stops here)",
}


def _norm_cmd(cmd: str) -> str:
    """Whitespace-normalised command for matching (tabs/newlines, padding)."""
    return " ".join((cmd or "").split())


def _read_rotations(root: Path) -> tuple[str, str]:
    """The frontmatter text and the `## facts` body of config:rotations.

    Returns `("", "")` when the node is absent. The facts body is used for
    the classifier's category-(a) text mentions only; the first_turn list is
    the load-bearing part and is parsed by `_extract_first_turn`."""
    nf = node_writer.find_node_file(root, "config:rotations")
    if nf is None:
        return "", ""
    text = nf.read_text(encoding="utf-8")
    fm = text.split("---", 2)[1] if text.startswith("---") else ""
    # facts section: everything under `## facts` up to the next `## ` heading
    body = text.split("<!-- BODY:BEGIN -->", 1)[-1] if "<!-- BODY:BEGIN -->" in text else text
    facts = ""
    if "## facts" in body:
        _f = body.split("## facts", 1)[1]
        facts = _f.split("\n## ", 1)[0]
    return fm, facts


def _extract_first_turn(fm: str, role: str) -> list[dict]:
    """`templates.<role>.startup.first_turn` as a list of dicts.

    Minimal dedicated parser (the frontmatter is YAML-ish JSON-on-lines, the
    same shape load_seats already walks by hand): locate `templates:` then
    the `  <role>:` key at two-space indent, then the `      first_turn:`
    key, then collect every `        - {...}` item until the list dedents.
    Blank/missing role or node -> []. Never falls back to another role's
    template: an absent role returns [] and the caller refuses loudly.
    """
    lines = fm.splitlines()
    in_templates = False
    role_idx = None
    for idx, ln in enumerate(lines):
        if ln.strip() == "templates:":
            in_templates = True
            continue
        if in_templates and ln == f"  {role}:":
            role_idx = idx
            break
    if role_idx is None:
        return []
    entries: list[dict] = []
    in_ft = False
    for ln in lines[role_idx + 1:]:
        stripped = ln.strip()
        if not in_ft:
            if stripped == "startup:":
                continue
            if stripped == "first_turn:":
                in_ft = True
                continue
            continue
        # inside first_turn: items are `        - {...}` (8-space indent)
        if ln.startswith("        - "):
            payload = ln[len("        - "):].strip()
            import json as _json
            try:
                o = _json.loads(payload)
            except Exception:
                continue
            if isinstance(o, dict):
                entries.append(o)
            continue
        # any line that is not a deeper list item closes the list
        if stripped and not ln.startswith("          "):
            break
    return entries


def _first_turn_label(cmd: str, seat: str, entries: list[dict]) -> str | None:
    """The first_turn entry whose `cmd` the call re-runs, or None.

    Matching is deliberate and loose where templates are: the `{seat}` and any
    other `{...}` placeholder becomes one `\\S+` token (rotate-self substitutes
    them at runtime, so a live call carries the real seat/worktree/repo here),
    the template is cut at the first `;` and drained of `| head -N` display
    tails (real seats truncate output), then the template is required to match
    as a prefix of the call's command. Labels are the load-bearing output —
    category (a) is a re-derive of a first_turn output only when a template
    label actually matches."""
    nc = _norm_cmd(cmd)
    if not nc:
        return None
    for e in entries:
        tpl = _norm_cmd((e.get("cmd") or "").replace("{seat}", seat))
        if not tpl:
            continue
        first_seg = tpl.split(";", 1)[0]
        first_seg = re.sub(r"\s*\|\s*head(\s+-?\d+)?$", "", first_seg)
        # fold any remaining `{...}` placeholders (worktree/repo/...) to one token
        parts = re.split(r"\{[^}]+\}", first_seg)
        toks = [re.escape(p) for p in parts]
        pattern = r"\S+".join(toks) if len(parts) > 1 else re.escape(first_seg)
        if re.match(r"^" + pattern, nc):
            return e.get("label")
    return None


# ── `## facts` re-derive detection (g15, hypothesis:l4-wake-audit-reads-
# ── facts-and-defaults-to-the-latest-record) ────────────────────────────
# The audit's category (a) used to match ONLY the first_turn template cmds, so a
# wake that re-derived a fact by ITS OWN command shape was counted as (d) real
# work. The `## facts` bullets in config:rotations cite the exact command shape
# that establishes each fact (F1 = `rotate.py status --seat <seat> --record
# latest`, F2 = whois / grep of seats.md, ...), so the classifier now parses
# those bullets and matches a call against the cited shapes the same way it
# matches first_turn templates.

_FACT_LABEL_RE = re.compile(r"^-\s*(F\d+)\b", re.IGNORECASE)


def _parse_facts(facts_text: str) -> list[tuple[str, list[str]]]:
    """Parse the `## facts` body into `(F-label, [command-shape...])` pairs.

    A bullet is `- F1 (...) : prose with cmd-shape citations enclosed in
    backticks.` The label is
    the `F<N>` right after the dash; the shapes are the backtick spans. A span
    counts as matchable only when it looks like a command: it carries whitespace
    (multi-token) or is a bare known tool token. A bare path like
    `config:rotations` cannot prefix-match a command and is ignored; a bare
    `ps`/`tmux`/`whois` must match (the whole point of F1/F2's by-hand reads)."""
    out: list[tuple[str, list[str]]] = []
    cur_label: str | None = None
    cur_shapes: list[str] = []
    for ln in facts_text.splitlines():
        s = ln.strip()
        if not s:
            continue
        m = _FACT_LABEL_RE.match(s)
        if m:
            if cur_label:
                out.append((cur_label, cur_shapes))
            cur_label = m.group(1).upper()
            cur_shapes = []
        for span in re.findall(r"`([^`]+)`", s):
            shape = _norm_cmd(span)
            if not shape:
                continue
            if " " in shape:
                cur_shapes.append(shape)
            elif shape in ("ps", "tmux", "whois", "git", "ls", "cat",
                           "grep", "sed", "rg", "find", "tail", "head"):
                cur_shapes.append(shape)
    if cur_label:
        out.append((cur_label, cur_shapes))
    return out


def _shape_prefix_matches(shape: str, nc: str) -> bool:
    """Prefix-match a fact command shape against a normalized call command.

    Folds `{...}` and `<...>` placeholders to one `\\S+` token (the same loose
    rule `_first_turn_label` uses); a bare single-token shape (`ps`, `tmux`) is
    word-bounded so it matches `ps -o pid` but never `psql`/`ps -C`'s cousins."""
    parts = re.split(r"\{[^}]+\}|<[^>]+>", shape)
    toks = [re.escape(p) for p in parts]
    pattern = r"\S+".join(toks) if len(parts) > 1 else re.escape(shape)
    if " " not in shape:
        pattern = r"\b" + pattern + r"(?=\s|$)"
    return bool(re.match(r"^" + pattern, nc))


def _fact_label(cmd: str, facts: list[tuple[str, list[str]]]) -> str | None:
    """The `F<N>` label of the fact whose cited command shape the call re-derives."""
    nc = _norm_cmd(cmd)
    if not nc:
        return None
    for label, shapes in facts:
        for sh in shapes:
            if _shape_prefix_matches(sh, nc):
                return label
    return None


# ── rotation-record transcript resolution (g15: --gen optional, defaults to
# ── the seat's LATEST rotation record; env / newest-.jsonl unreachable without
# ── an explicit --transcript) ────────────────────────────────────────────

def _rotation_records(root: Path, seat: str) -> list[Path]:
    """`sessions/rotations/<seat>.*.json` for a seat, newest-last."""
    d = locations.shared_sessions_dir(root) / rotate.ROTATIONS_DIR_NAME
    if not d.is_dir():
        return []
    return sorted(d.glob(f"{seat}.*.json"))


def _record_transcript(rec: dict) -> Path | None:
    """The transcript a rotation record names on its own, or None.

    Checked in order: the record's `session_log` (direct path), the
    `handover.session_log`, the `handover.join.transcript` (the name every
    LIVE rotation record carries), then
    `observations.c_readback_log_path` WHEN it is a CC `.jsonl` (a legacy
    debug `.log` is not tool_use-parseable, so naming it would make the audit
    silently read nothing)."""
    for key in ("session_log",):
        v = rec.get(key)
        if v:
            return Path(str(v)).expanduser()
    ho = rec.get("handover")
    if isinstance(ho, dict):
        v = ho.get("session_log")
        if v:
            return Path(str(v)).expanduser()
        j = ho.get("join") or {}
        if isinstance(j, dict):
            v = j.get("transcript")
            if v:
                return Path(str(v)).expanduser()
    obs = rec.get("observations")
    if isinstance(obs, dict):
        v = obs.get("c_readback_log_path")
        if v and str(v).lower().endswith(".jsonl"):
            return Path(str(v)).expanduser()
    return None


def _record_matches_gen(rec: dict, gen: int) -> bool:
    """Whether a rotation record belongs to generation `gen`.

    A rotate-self record's `observations.b_generation.after` is the generation
    THIS rotation produced (the successor's); `before` is the predecessor's and
    is not the record's own generation, so only `after` / a top-level
    `gen_after` match."""
    if rec.get("gen_after") == gen:
        return True
    obs = rec.get("observations")
    if isinstance(obs, dict):
        b = obs.get("b_generation")
        if isinstance(b, dict) and b.get("after") == gen:
            return True
    return False


def _latest_record(root: Path, seat: str,
                   gen: int | None = None) -> tuple[Path, dict] | None:
    """The seat's latest rotation record (or the latest matching `gen`).

    Files are named `<seat>.<UTC timestamp>.json` so sorted name order is time
    order, the same rule `rotate.py status --record latest` uses. Parses JSON;
    a record that does not parse is skipped, not fatal."""
    files = _rotation_records(root, seat)
    matches = [f for f in files]
    if gen is not None:
        matches = []
        for p in reversed(files):
            try:
                doc = json.loads(p.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                continue
            if _record_matches_gen(doc, gen):
                matches.append((p, doc))
        if not matches:
            return None
        return matches[0]
    for p in reversed(files):
        try:
            return p, json.loads(p.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
    return None


def _resolve_wake_transcript(root: Path, seat: str, gen: int | None,
                             transcript_path: Path | None) -> tuple[Path | None, str]:
    """The transcript the wake audit reads, in the g15 order:

      1. an explicit `--transcript PATH` (must exist)
      2. the seat's rotation record — `--gen N` selects the record for gen N,
         no `--gen` means the LATEST record — via the record's OWN
         `session_log`/session id. The env / newest-.jsonl fallbacks of
         `rotate.resolve_transcript` are UNREACHABLE here by construction.

    Returns `(path, source)`. `(None, source)` means the record/transcript was
    absent; `source` names it so the caller can refuse with the name (never a
    silent fall-through)."""
    if transcript_path is not None:
        lp = Path(transcript_path).expanduser().resolve()
        return (lp, "explicit") if lp.exists() else (None, "explicit-missing")
    rec = _latest_record(root, seat, gen=gen)
    if rec is None:
        if gen is not None:
            return None, f"no rotation record for {seat!r} gen {gen}"
        return None, f"no rotation record for seat {seat!r}"
    rec_path, doc = rec
    src = f"record:{rec_path.name}"
    lp = _record_transcript(doc)
    if lp is None:
        return None, f"{src} names no transcript"
    return lp, src


def _is_protocol_learning(cmd: str, tool: str) -> bool:
    """Category c: `-h`/`--help`, or grep/rg/sed over a SOURCE file or a
    transcript/log — learning a tool's surface instead of doing work. Config
    nodes (.md) are NOT source/logs: grepping the seat registry by hand is a
    by-hand read (b), not protocol learning.

    A `sed -i` / `sed --in-place` is an EDIT of a source file, not a read-only
    learn — it belongs to (d) real work, never (c) (g15: sensei.py sed -i
    counted as learning)."""
    low = _norm_cmd(cmd).lower()
    if re.search(r"(\s-h(\s|$)|--help)", low):
        return True
    # in-place source edits are work, not learning (the whole point of (4) in
    # hypothesis:l4-wake-audit-reads-facts-and-defaults-to-the-latest-record)
    if re.search(r"\bsed\b.*(--in[-_ ]?place|-i)\b", low):
        return False
    return bool(re.search(
        r"(grep|rg|sed)\b.*\.(py|sh|log|js)(\b|[^ ])", low)) or bool(
        re.search(r"(grep|rg|sed)\b.*(rotate\.py|write\.py|send\.py|sensei\.py)", low))


def _is_byhand_read(cmd: str, tool: str) -> bool:
    """Category b: a read/action the seat does BY HAND that a template entry
    (first_turn or after_join) already covers — ps/tmux process-tree checks,
    listing sessions/rotation records, reading a record/bootstrap json, the
    ListAgents/ToolSearch join, the `rotate.py ack` and `meter --pin` the
    service performs after_join, and grepping the seat-registry config node."""
    nc = _norm_cmd(cmd).lower()
    if re.search(r"\bps(\s|$)", nc) or re.search(r"\btmux\b", nc):
        return True
    if re.search(r"sessions/rotations|claude/projects", nc):
        return True
    if re.search(r"(ls|cat|sed|grep)\b.*(sessions|rotations|bootstrap|\.ack\.json|\.meter|seats\.md)", nc):
        return True
    if re.search(r"rotate\.py ack|rotate\.py meter --pin", nc):
        return True
    if re.search(r"\bwhois\b", nc) or tool in ("ListAgents", "ToolSearch"):
        return True
    return False


def classify_call(cmd: str, tool: str, seat: str,
                  entries: list[dict] | None = None,
                  facts: list[tuple[str, list[str]]] | None = None) -> tuple[str, str | None]:
    """One assistant tool_use call across the four wake categories.

    Returns `(category, label)`. Category precedence: protocol learning (c)
    beats a first_turn re-derive (a) — learning the tool is not re-deriving a
    fact — and a first_turn/fact re-derive (a) beats a hand-read (b).
    c only when `-h`/`--help` or a source/log grep; a when the call's command
    re-runs a configured first_turn cmd (label = the entry) or re-derives a
    `## facts` bullet's own cited command shape (label = `F<N>`); b when it is
    a hand-read a startup entry could pre-run; d otherwise (real work)."""
    label = _first_turn_label(cmd, seat, entries or [])
    if _is_protocol_learning(cmd, tool):
        return "c", label
    if label is not None:
        return "a", label
    if facts:
        f_label = _fact_label(cmd, facts)
        if f_label is not None:
            return "a", f_label
    if _is_byhand_read(cmd, tool):
        return "b", None
    return "d", None


def _summarize_tool_input(inp) -> str:
    """A short input summary for one tool_use block (first ~110 chars)."""
    if isinstance(inp, str):
        s = inp
    elif isinstance(inp, dict):
        s = json.dumps(inp, sort_keys=True)
    else:
        s = str(inp)
    s = " ".join(s.split())
    return s[:110] + ("…" if len(s) > 110 else "")


def _synthesize_read_cmd(tool: str, inp) -> str:
    """A Bash-like cmd string for a NON-Bash tool's own input, so the shared
    classifier's byhand-read (b) / work (d) rules can judge the read by its
    paths (g15 req 3). Read carries a `path`; Grep a `pattern` + `path` list;
    Glob `pattern`/`path` lists. A tool that is neither Bash nor Read/Grep/
    Glob (Edit/Write) is real work (d) and is handled by the caller, never
    here."""
    if not isinstance(inp, dict):
        return ""
    parts: list[str] = []
    if tool == "Grep":
        p = inp.get("pattern")
        if p:
            parts.append(str(p))
    for key in ("pattern", "path", "paths"):
        v = inp.get(key)
        if isinstance(v, list):
            parts.extend(str(x) for x in v)
        elif isinstance(v, str) and v:
            parts.append(v)
    return " ".join(parts)


def _path_is_hand_read(s: str) -> bool:
    """Whether a NON-Bash tool's path names a file a first_turn entry or after-
    join step already pre-runs — a by-hand read (b), never real work. Mirrors
    the file-path signals `_is_byhand_read` keys on for Bash commands."""
    low = _norm_cmd(s).lower()
    return bool(
        "seats.md" in low
        or "sessions/rotations" in low
        or "claude/projects" in low
        or "bootstrap" in low
        or low.endswith(".ack.json")
        or "/.meter" in low or low.endswith(".meter")
    )


def _iter_tool_uses(path: Path):
    """Yield `(tool, input_dict)` for every assistant tool_use in a CC JSONL
    transcript, in file order, tolerating corrupt lines (errors=replace)."""
    for _idx, tool, inp in _iter_assistant_tool_uses(path):
        yield tool, inp


def _iter_assistant_tool_uses(path: Path):
    """Yield `(line_index, tool, input_dict)` for every assistant tool_use.

    Shared low-level read behind both `_iter_tool_uses` (wake-audit) and the
    rotate-out window scanner (which needs the line offset to start after the
    last real input). line_index is the jsonl offset (0-based). One JSONL
    line may carry several tool_use blocks; each yields its own row.
    """
    with open(path, encoding="utf-8", errors="replace") as fh:
        for ln_idx, line in enumerate(fh):
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ev.get("type") != "assistant":
                continue
            content = ev.get("message", {}).get("content")
            if not isinstance(content, list):
                continue
            for b in content:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    yield ln_idx, b.get("name", "?"), b.get("input") or {}


def _tool_uses_after(path: Path, start_line: int):
    """The subset of `_iter_tool_uses` on jsonl lines at/after `start_line`.

    Used for the rotate-out window: every assistant tool_use after the last
    real user input, to the end of the predecessor's transcript.
    """
    for idx, tool, inp in _iter_assistant_tool_uses(path):
        if idx >= start_line:
            yield tool, inp


def _last_real_input(path: Path) -> tuple[int, str | None]:
    """The last user turn that is NOT a tool_result (a merge-up reply, an
    owner/Prime turn). Returns `(line_index, timestamp|None)`; (-1, None)
    when the transcript has no real user turn (the whole head is the window).
    """
    last_idx = -1
    last_ts = None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for ln_idx, line in enumerate(fh):
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ev.get("type") != "user":
                continue
            content = ev.get("message", {}).get("content")
            if isinstance(content, str):
                # Plain-string content = human-authored text (a merge-up
                # reply, an owner/Prime turn). A non-empty string IS a real
                # input; empty/whitespace-only is not (and is never counted).
                has_text = bool(content.strip())
            elif isinstance(content, list):
                # A REAL input is one that carries human-authored text, not
                # just tool_result feedback. A user turn may hold both a text
                # block and tool_result blocks; the text decides. Contents
                # that are plain strings are uniformly text.
                has_text = any(
                    (isinstance(b, dict) and b.get("type") == "text"
                     and (b.get("text") or "").strip())
                    or isinstance(b, str)
                    for b in content)
            else:
                continue
            if not has_text:
                continue  # tool_result-only feedback / empty, not a real input
            last_idx = ln_idx
            ts = ev.get("timestamp") or ev.get("message", {}).get("timestamp")
            if ts:
                last_ts = str(ts)
    return last_idx, last_ts


#: Non-Bash tools whose OWN input names the file(s) a wake reads by hand.
_READLIKE_TOOLS = ("Read", "Grep", "Glob")
#: Tools whose input is an EDIT/WRITE of a file — always real work (d),
#: regardless of whether the path is one a first_turn entry pre-runs.
_WRITELIKE_TOOLS = ("Edit", "Write", "WriteFile", "MultiEdit",
                    "NotebookEdit")


def wake_audit(root: Path, seat: str, gen: int | None,
               transcript_path: Path | None) -> tuple[int, list[dict], dict]:
    """Run the classification over the seat's wake transcript.

    Returns `(exit_code, per_call_rows, counts)` so the CLI body and the tests
    share one implementation. Reads the LIVE config:rotations template AND the
    `## facts` bullets for the seat's role. The transcript is resolved in the
    g15 order (explicit --transcript, else the seat's LATEST rotation record's
    own session_log — never the env / newest-.jsonl fallbacks). The window
    runs from the first assistant tool_use to the first call classifiable as
    real work (category d, excluded)."""
    rows = load_seats(root)
    row = seat_row(rows, seat)
    if row is None:
        print(f"ERR: no seat row for {seat!r} in config:seats", file=sys.stderr)
        return 2, [], {}
    role = (row.get("role") or "").strip()
    fm, facts_text = _read_rotations(root)
    if not fm:
        print("ERR: config:rotations not found; cannot classify a wake",
              file=sys.stderr)
        return 2, [], {}
    entries = _extract_first_turn(fm, role)
    if not entries:
        print(f"ERR: no templates.{role}.startup.first_turn in config:rotations "
              f"(role {role!r} has no template; refusing to fall back to "
              f"another role's)", file=sys.stderr)
        return 2, [], {}
    facts = _parse_facts(facts_text)

    log_path, source = _resolve_wake_transcript(root, seat, gen, transcript_path)
    if log_path is None:
        print(f"ERR: cannot audit a wake for seat {seat!r}: {source}; "
              f"pass --transcript PATH or let the seat's rotation record "
              f"name its session_log", file=sys.stderr)
        return 2, [], {}
    if not log_path.exists():
        print(f"ERR: transcript {log_path} does not exist ({source})",
              file=sys.stderr)
        return 2, [], {}

    calls: list[dict] = []
    counts = {"a": 0, "b": 0, "c": 0, "d": 0}
    window_end = None
    for tool, inp in _iter_tool_uses(log_path):
        if tool in _WRITELIKE_TOOLS:
            cat, label, cmd = "d", None, ""
        elif tool in _READLIKE_TOOLS:
            # non-Bash Read/Grep/Glob are judged by their OWN paths: a covered
            # path is a by-hand read (b), anything else is real work (d). Such
            # calls carry no command, so they never match a first_turn/fact
            # re-derive (a) nor protocol learning (c).
            cmd = _synthesize_read_cmd(tool, inp)
            cat, label = ("b", None) if _path_is_hand_read(cmd) else ("d", None)
        else:
            cmd = inp.get("command", "") if isinstance(inp, dict) else ""
            cat, label = classify_call(cmd, tool, seat, entries, facts)
        calls.append({"tool": tool, "cmd": cmd, "cat": cat,
                      "summary": _summarize_tool_input(inp), "label": label,
                      "source": source})
        counts[cat] += 1
        if cat == "d":
            window_end = len(calls)
            break
    return 0, calls, counts


def cmd_wake_audit(root: Path, args) -> int:
    code, calls, counts = wake_audit(root, args.seat, args.gen,
                                     Path(args.transcript) if args.transcript else None)
    if code != 0:
        return code
    gen_label = args.gen if args.gen is not None else "latest"
    print(f"sensei.py wake-audit --seat {args.seat} --gen {gen_label} "
          f"(role {seat_row(load_seats(root), args.seat)['role']})")
    print(f"window: first assistant tool_use -> first real work "
          f"({len(calls)} calls scanned, cut at the first category d)")
    print(f"counts: a={counts['a']} b={counts['b']} c={counts['c']} d={counts['d']}")
    print(f"  (d counts the cut call itself; only a/b/c span the wake window)")
    print(f"transcript: {calls[0]['source'] if calls else '?'}")
    for i, c in enumerate(calls, 1):
        lbl = f" <{c['label']}>" if c["label"] else ""
        print(f"  {i:>2} [{c['cat']}] {c['tool']}: {c['summary']}{lbl}")
    if not calls:
        print("  (no assistant tool_use found in the transcript)")
    return 0


# ── rotate-out-audit ──────────────────────────────────────────────────────
# The mirror of wake-audit over the OUTGOING predecessor, instead of the
# incoming successor (goal:g15.13 / hypothesis
# :l4-rotate-out-audit-mirrors-wake-audit-over-the-predecessor-window): same
# classifier (`classify_call` and its helpers), different window — every
# assistant tool_use from the predecessor's LAST real input (a merge-up reply
# / an owner/Prime turn, never a tool_result) to the end of ITS OWN
# transcript, resolved from the rotation records, never the newest slug-dir
# transcript (that one is the successor's).


# (merge SL1.01 x L4.240: renamed from `_rotation_records` — the wake-audit side
#  defines a Path-list reader under that name; this one returns (path, record).)
def _seat_rotation_records(root: Path, seat: str) -> list[tuple[Path, dict]]:
    """`(path, record)` for every rotation record whose `seat` field equals
    `seat`, sorted by record filename (the timestamp-ordered glob). Matches
    on the record's own `seat` field, so `belam-S1-L4-*` names never leak
    onto a bare `belam` query."""
    rot = Path(root) / "sessions" / "rotations"
    if not rot.is_dir():
        return []
    out: list[tuple[Path, dict]] = []
    for p in sorted(rot.glob("*.json")):
        try:
            rec = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(rec, dict):
            continue
        if (str(rec.get("seat") or "").strip()) != seat:
            continue
        out.append((p, rec))
    return out


def _gen_bounds(rec: dict) -> tuple[int | None, int | None]:
    """`(b_generation.before, b_generation.after)`; tolerant of the field
    living at top level or under `observations`."""
    bg = rec.get("observations", {})
    if isinstance(bg, dict):
        bg = bg.get("b_generation")
    if not isinstance(bg, dict):
        bg = rec.get("b_generation")
    if not isinstance(bg, dict):
        return None, None
    before = bg.get("before")
    after = bg.get("after")
    return (before if isinstance(before, int) else None,
            after if isinstance(after, int) else None)


def _fallback_pids(rec: dict) -> list[int]:
    """Pids to try as `~/.claude/sessions/<pid>.json` for the predecessor
    transcript: the outgoing record's `s12_self_reap.chain` and its
    `handover.reap_own_pid.pid`."""
    pids: list[int] = []
    s12 = rec.get("s12_self_reap")
    if isinstance(s12, dict) and isinstance(s12.get("chain"), list):
        pids += [p for p in s12["chain"] if isinstance(p, int)]
    rop = rec.get("handover")
    if isinstance(rop, dict):
        rop = rop.get("reap_own_pid")
    if isinstance(rop, dict) and isinstance(rop.get("pid"), int):
        pids.append(rop["pid"])
    return pids


def _resolve_predecessor_transcript(
        root: Path, seat: str, gen: int, records: list[tuple[Path, dict]],
        explicit: str | None) -> tuple[Path | None, str]:
    """Resolve the OUTGOING predecessor's transcript `--gen N`.

    Resolution order (never the newest slug-dir transcript — that one is the
    successor's, and it would be a named false positive): (1) explicit
    `--transcript`; (2) the previous record of the same seat whose
    `b_generation.after == N` — it carries the `handover.join.transcript` of
    gen N joining; (3) `~/.claude/sessions/<pid>.json` for a pid in the
    OUTGOING record's `s12_self_reap.chain`/`handover.reap_own_pid`.
    Returns `(path|None, reason)`; None when nothing resolved."""
    if explicit:
        return Path(explicit), "explicit --transcript"
    for _p, rec in records:
        bf, af = _gen_bounds(rec)
        if af == gen:
            join = rec.get("handover", {})
            if isinstance(join, dict):
                join = join.get("join")
            if isinstance(join, dict) and join.get("transcript"):
                return (Path(str(join["transcript"])),
                        f"previous record b_generation.after=={gen} "
                        "handover.join.transcript")
    # fallback: the pid chain of the record that rotated gen N out
    out_rec = next((rec for _p, rec in records
                    if (rec.get("observations", {}).get("b_generation", {})
                        or {}).get("before") == gen
                    or rec.get("b_generation", {}).get("before") == gen),
                   None)
    home = Path.home()
    for pid in _fallback_pids(out_rec) if out_rec else []:
        cand = home / ".claude" / "sessions" / f"{pid}.json"
        if cand.is_file():
            return cand, f"~/.claude/sessions/{pid}.json " \
                         "/ s12_self_reap.chain"
    return None, "no predecessor transcript resolved"


def rotate_out_audit(root: Path, seat: str, gen: int | None,
                     transcript_path: Path | None) -> tuple[int, list[dict], dict, dict]:
    """Classify the outgoing predecessor's calls from its last real input to
    the record's `recorded_at` (mirror of `wake_audit`).

    Returns `(exit_code, per_call_rows, counts, window)`. Reuses
    `classify_call`/`_iter_tool_uses`/_is_protocol_learning — refactored
    shared, never copied. `--gen` defaults to the latest record's
    `b_generation.before` (the most recent rotation). Window = every
    assistant tool_use after the last real user turn to the transcript end;
    category (d) rows are the genuine decisions (card edit, rotate-self,
    ack, one-line report) and are NOT a cut point here."""
    rows = load_seats(root)
    row = seat_row(rows, seat)
    if row is None:
        print(f"ERR: no seat row for {seat!r} in config:seats", file=sys.stderr)
        return 2, [], {}, {}
    role = (row.get("role") or "").strip()
    fm, facts = _read_rotations(root)
    if not fm:
        print("ERR: config:rotations not found; cannot classify a rotate-out",
              file=sys.stderr)
        return 2, [], {}, {}
    entries = _extract_first_turn(fm, role)
    if not entries:
        print(f"ERR: no templates.{role}.startup.first_turn in config:rotations "
              f"(role {role!r} has no template; refusing to fall back to "
              f"another role's)", file=sys.stderr)
        return 2, [], {}, {}

    records = _seat_rotation_records(root, seat)
    if not records:
        print(f"ERR: no rotation records under sessions/rotations for seat "
              f"{seat!r}", file=sys.stderr)
        return 2, [], {}, {}

    if gen is None:
        gen = _gen_bounds(records[-1][1])[0]
        if gen is None:
            print("ERR: cannot default --gen: the latest record has no "
                  "b_generation.before", file=sys.stderr)
            return 2, [], {}, {}

    # the record that rotated gen N OUT narrows resolution + gives recorded_at
    out_rec = next((rec for _p, rec in records
                    if _gen_bounds(rec)[0] == gen), None)
    if out_rec is None:
        print(f"ERR: no rotation record with b_generation.before == {gen} "
              f"for seat {seat!r}", file=sys.stderr)
        return 2, [], {}, {}
    recorded_at = out_rec.get("recorded_at") or ""

    log_path, source = _resolve_predecessor_transcript(
        root, seat, gen, records,
        str(transcript_path) if transcript_path else None)
    if log_path is None:
        print(f"ERR: no predecessor transcript resolved for seat {seat!r} "
              f"gen {gen} ({source}); pass --transcript PATH", file=sys.stderr)
        return 2, [], {}, {}
    if not log_path.is_file():
        print(f"ERR: predecessor transcript not found: {log_path} "
              f"({source})", file=sys.stderr)
        return 2, [], {}, {}

    start_idx, start_ts = _last_real_input(log_path)
    calls: list[dict] = []
    counts = {"a": 0, "b": 0, "c": 0, "d": 0}
    for tool, inp in _tool_uses_after(log_path, start_idx):
        cmd = inp.get("command", "") if isinstance(inp, dict) else ""
        cat, label = classify_call(cmd, tool, seat, entries)
        calls.append({"tool": tool, "cmd": cmd, "cat": cat,
                      "summary": _summarize_tool_input(inp), "label": label})
        counts[cat] += 1
    window = {"gen": gen, "start_line": start_idx, "start_ts": start_ts,
              "recorded_at": recorded_at, "source": source,
              "log_path": str(log_path)}
    return 0, calls, counts, window


def cmd_rotate_out_audit(root: Path, args) -> int:
    code, calls, counts, window = rotate_out_audit(
        root, args.seat, args.gen,
        Path(args.transcript) if args.transcript else None)
    if code != 0:
        return code
    row = seat_row(load_seats(root), args.seat)
    print(f"sensei.py rotate-out-audit --seat {args.seat} --gen {window['gen']} "
          f"(role {row['role']})")
    print(f"predecessor transcript: {window['log_path']} "
          f"({window['source']})")
    end = window["recorded_at"]
    print(f"window: [last real input {window['start_line']} "
          f"{window['start_ts'] or '(no ts)'} -> {end or 'record end'}] "
          f"{len(calls)} calls")
    print(f"counts: a={counts['a']} b={counts['b']} c={counts['c']} "
          f"d={counts['d']}")
    print(f"  (a=duplicates a rotate-self step/record field; b=hand poll/read; "
          f"c=protocol learning; d=genuine decision)")
    for i, c in enumerate(calls, 1):
        lbl = f" <{c['label']}>" if c["label"] else ""
        print(f"  {i:>2} [{c['cat']}] {c['tool']}: {c['summary']}{lbl}")
    if not calls:
        print("  (no assistant tool_use after the last real input)")
    return 0


# ── apply_note (the one place write.py can be reached from) ──────────────


def apply_note(root: Path, node_id: str, change: str) -> str:
    """`write.py <node> "note SENSEI: <change>"` — the exact once-only write."""
    proc = subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parent / "write.py"),
         node_id, f"note SENSEI: {change}", "--root", str(root)],
        capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"write.py failed ({proc.returncode}): "
            f"{proc.stderr.strip() or proc.stdout.strip()}")
    return (proc.stdout.strip() or proc.stderr.strip())


# ── subcommand bodies ────────────────────────────────────────────────────


def cmd_propose(root: Path, croot: Path, args) -> int:
    rows = load_seats(root)
    row = seat_row(rows, args.target)
    if args.change is None or not args.change.strip():
        print("ERR: --change TEXT is required", file=sys.stderr)
        return 2
    if row is None and not args.supervisor:
        print(f"ERR: no seat row for {args.target!r} and no --supervisor "
              f"given; nothing to propose against", file=sys.stderr)
        return 2
    threads = _required_threads(row, args.target, args.supervisor)
    text = f"{MSG_PREFIX}{args.change.strip()}"
    import datetime as _dt
    ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for kind, name in threads:
        if kind == "room":
            _send.send_room(croot, name, text, SENSEI)
        else:
            _send.send_dm(croot, SENSEI, name, text, SENSEI)
        print(f"  proposed -> {kind} {name}")
    print(ts)
    return 0


def cmd_apply(root: Path, croot: Path, args) -> int:
    rows = load_seats(root)
    row = seat_row(rows, args.target)
    if row is None and not args.supervisor:
        print(f"ERR: no seat row for {args.target!r} and no --supervisor "
              f"given", file=sys.stderr)
        return 2
    if row is None and not args.node_id:
        print("ERR: ephemeral apply needs --node-id to write its note into",
              file=sys.stderr)
        return 2
    if not args.since:
        print("ERR: --since TS is required (the ts a propose printed)",
              file=sys.stderr)
        return 2
    if args.change is None or not args.change.strip():
        print("ERR: --change TEXT is required", file=sys.stderr)
        return 2

    threads = _required_threads(row, args.target, args.supervisor)
    missing = [f"{k}:{n}" for k, n in threads
               if not _has_reply(croot, (k, n), args.since)]
    if missing:
        print("REFUSED: no reply after since on: " + ", ".join(missing),
              file=sys.stderr)
        return 3

    protected = row is not None and (
        (row.get("role") or "").strip() in PROTECTED_ROLES
        or int(row.get("tier", 0) or 0) >= 3)
    if protected and not args.owner_approved:
        return _draft_for_owner(root, croot, args, threads)
    node_id = args.node_id or (row.get("owning_goal") or "") or args.target
    if args.dry_run:
        print(f"[dry-run] write.py {node_id} 'note SENSEI: {args.change}'")
        return 0
    out = apply_note(root, node_id, args.change)
    print(f"APPLIED: {node_id} <- SENSEI note")
    for ln in out.splitlines():
        print(f"  {ln}")
    return 0


def _draft_for_owner(root: Path, croot: Path, args,
                     threads: list[tuple[str, str]]) -> int:
    """Protected target without --owner-approved: draft a file, dm liaison."""
    drafts = Path(root) / DRAFTS_DIR
    drafts.mkdir(parents=True, exist_ok=True)
    safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in args.target)
    path = drafts / f"{safe}.md"
    body = (f"# sensei draft — {args.target}\n\n"
            f"change: {args.change}\n"
            f"since:  {args.since}\n"
            f"threads: {', '.join(f'{k}:{n}' for k, n in threads)}\n"
            f"status: awaiting-owner-approval\n")
    path.write_text(body, encoding="utf-8")
    _send.send_dm(croot, SENSEI, LIAISON,
                  f"[sensei #draft] {args.target}: {args.change} (see {path})",
                  SENSEI)
    print(f"DRAFTED: {path}")
    print(f"DM → liaison (owner approval required: rerun with --owner-approved)")
    return 0


# ── CLI ──────────────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    root = locations.find_project_root(Path.cwd().resolve())
    if root is None:
        print("ERR: not inside an agi project", file=sys.stderr)
        return 1
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(root),
                    help="any path inside the project (default cwd)")
    ap.add_argument("--dry-run", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("pick_worst", help="worst ledger row(s)")
    p.add_argument("--ledger", default=None,
                   help="path to the failure-ledger rows file")
    p.add_argument("--rows", default=None, nargs="*",
                   help="inline JSON rows (for tests / tooling)")

    p = sub.add_parser("propose", help="ping a seat + its supervisor")
    p.add_argument("--target", required=True)
    p.add_argument("--change", default=None)
    p.add_argument("--supervisor", default=None)

    p = sub.add_parser("wake-audit",
                        help="classify a rotation wake's tool calls")
    p.add_argument("--seat", required=True)
    p.add_argument("--gen", type=int, default=None,
                   help="rotation-record generation to audit (default: the "
                        "seat's LATEST rotation record; the transcript comes "
                        "from that record's own session_log)")
    p.add_argument("--transcript", default=None,
                   help="explicit transcript path (overrides the seat's "
                        "rotation record; env/newest-.jsonl are never used)")

    p = sub.add_parser("rotate-out-audit",
                        help="classify the outgoing predecessor's rotate-out calls")
    p.add_argument("--seat", required=True)
    p.add_argument("--gen", type=int, default=None,
                   help="generation that ROTATED OUT (default: the latest "
                        "record's b_generation.before)")
    p.add_argument("--transcript", default=None,
                   help="explicit predecessor transcript path (else resolved "
                        "from the rotation records)")

    p = sub.add_parser("apply", help="apply once both threads reply")
    p.add_argument("--target", required=True)
    p.add_argument("--node-id", default=None,
                   help="build node to write the SENSEI note into")
    p.add_argument("--change", default=None)
    p.add_argument("--since", default=None)
    p.add_argument("--supervisor", default=None)
    p.add_argument("--owner-approved", action="store_true")

    args = ap.parse_args(argv)
    root = locations.find_project_root(Path(args.root).resolve()) or root
    croot = _send.comms_root(root)

    if args.cmd == "pick_worst":
        rows: list[dict] = []
        import json as _json
        for s in (args.rows or []):
            try:
                rows.append(_json.loads(s))
            except Exception:
                continue
        if args.ledger and Path(args.ledger).is_file():
            rows = load_ledger_rows(Path(args.ledger))
        worst = pick_worst(rows)
        if worst is None:
            print("no rows; nothing to pick")
            return 0
        print(_json.dumps(worst, sort_keys=True))
        return 0
    if args.cmd == "propose":
        return cmd_propose(root, croot, args)
    if args.cmd == "wake-audit":
        return cmd_wake_audit(root, args)
    if args.cmd == "rotate-out-audit":
        return cmd_rotate_out_audit(root, args)
    if args.cmd == "apply":
        return cmd_apply(root, croot, args)
    return 2


if __name__ == "__main__":
    sys.exit(main())