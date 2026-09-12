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
    from . import locations, node_writer, rotate, send as _send, geometry_config
    from .frontmatter import split_frontmatter
except ImportError:  # runs as a plain script from a checkout
    import locations  # type: ignore
    import node_writer  # type: ignore
    import rotate  # type: ignore
    import send as _send  # type: ignore
    import geometry_config  # type: ignore
    from frontmatter import split_frontmatter  # type: ignore

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
    """Parse the `posts:` list out of config:posts's frontmatter (`config:seats`
    / `seats:` is the one-season alias).

    Resolves the row file through `geometry_config.resolve` so a migrated
    tree reads posts.md, then a minimal YAML list parse (the rows schema is
    flat JSON objects on lines, so a document split of the list block is
    enough).
    """
    path, list_key = geometry_config.resolve(root)
    if path is None or not Path(path).exists():
        return []
    text = Path(path).read_text(encoding="utf-8")
    parted = split_frontmatter(text)
    fm = parted[0] if parted else ""
    in_list = False
    rows: list[dict] = []
    for line in fm.splitlines():
        if line.strip().startswith(f"{list_key}:"):
            in_list = True
            continue
        if in_list:
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
    "s": "service-owed: an after_join step the service performs (does not cut the window)",
}


def _norm_cmd(cmd: str) -> str:
    """Whitespace-normalised command for matching (tabs/newlines, padding)."""
    return " ".join((cmd or "").split())


def _read_rotations(root: Path) -> tuple[str, str]:
    """The frontmatter text and the `## facts` body of config:rotations.

    Returns `("", "")` when the node is absent. The facts body feeds
    `_parse_facts` / `_fact_label`, which match a wake call against a
    re-derivable fact's CITED command shapes for category-(a) and SKIP the
    prescribed-act bullets (a call that performs an ordered act is work, never
    a re-derive); the role's first_turn list is the label side and is parsed
    by `_extract_first_turn`."""
    nf = node_writer.find_node_file(root, "config:rotations")
    if nf is None:
        return "", ""
    text = nf.read_text(encoding="utf-8")
    parted = split_frontmatter(text)
    fm = parted[0] if parted else ""
    # facts section: everything under `## facts` up to the next `## ` heading
    body = text.split("<!-- BODY:BEGIN -->", 1)[-1] if "<!-- BODY:BEGIN -->" in text else text
    facts = ""
    if "## facts" in body:
        _f = body.split("## facts", 1)[1]
        facts = _f.split("\n## ", 1)[0]
    return fm, facts


def _extract_template_list(fm: str, role: str, listkey: str) -> list[dict]:
    """`templates.<role>.startup.<listkey>` as a list of dicts.

    Minimal dedicated parser (the frontmatter is YAML-ish JSON-on-lines, the
    same shape load_seats already walks by hand): locate `templates:` then
    the `  <role>:` key at two-space indent, then the `      <listkey>:`
    key (a sibling of `first_turn` under `startup:`), then collect every
    `        - {...}` item until the list dedents. Blank/missing role or
    node -> []. Never falls back to another role's template: an absent role
    returns [] and the caller refuses loudly."""
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
    in_list = False
    for ln in lines[role_idx + 1:]:
        stripped = ln.strip()
        if not in_list:
            if stripped == "startup:":
                continue
            if stripped == f"{listkey}:":
                in_list = True
                continue
            continue
        # inside the list: items are `        - {...}` (8-space indent)
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


def _extract_first_turn(fm: str, role: str) -> list[dict]:
    """`templates.<role>.startup.first_turn`, the startup commands the
    SERVICE runs before spawn (their outputs become the successor's first
    input turn). Never falls back to another role's template."""
    return _extract_template_list(fm, role, "first_turn")


def _extract_after_join(fm: str, role: str) -> list[dict]:
    """`templates.<role>.startup.after_join` — the commands the SERVICE
    performs after the join (this is how a wake's by-hand `rotate.py ack` /
    `meter --pin` are recognised as service-owed (s)). Read fresh, never a
    hardcoded list beyond the two named steps (hypothesis:l4-wake-audit-
    reads-facts-and-defaults-to-the-latest-record, proposal (e) second half)."""
    return _extract_template_list(fm, role, "after_join")


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

#: Bare tool tokens a `## facts` bullet may cite as a whole command shape.
_BARE_FACT_TOOLS = ("ps", "tmux", "whois", "git", "ls", "cat",
                    "grep", "sed", "rg", "find", "tail", "head")

#: Next-word tails that mark a bare backtick tool as the grammatical SUBJECT of
#: a DESCRIPTIVE sentence ("`whois` matches by prefix on it", "`ack` takes a
#: ref") rather than a cited command shape — such a span is PROSE and must not
#: be a matchable shape. A bare tool that IS a cited command is followed instead
#: by a conjunction/continuation (`...`/` or `/`;`) or by the clause end
#: (goal:g15.13 / item 2's falsifier: F15's prose `whois` shadowing F2's).
_BARE_PRESCRIPTIVE_TAIL = {
    "matches", "match", "takes", "take", "is", "are", "was", "were",
    "be", "costs", "cost", "lands", "land", "reaches", "reach",
    "returns", "return", "prints", "print", "shows", "show", "says",
    "say", "uses", "use", "reads", "read", "writes", "write", "runs",
    "run", "means", "verb", "command", "tool", "syntax", "form",
}


def _bare_span_is_prose(line: str, after: int) -> bool:
    """Whether the backtick span ending at `after` is PROSE rather than a
    cited command. True when the token is the subject of a following
    descriptive verb/noun (see `_BARE_PRESCRIPTIVE_TAIL`); False otherwise, so
    a bare tool followed by a conjunction or the clause end is kept."""
    if after >= len(line):
        return False
    tail = line[after:].lstrip(" ,;:.!?(")
    if not tail:
        return False
    word = tail.split(" ", 1)[0].strip(")]}'\"")
    word = re.sub(r"[^A-Za-z]", "", word).lower()
    return word in _BARE_PRESCRIPTIVE_TAIL

#: A `## facts` bullet PRESCRIBES an act (the template ORDERS something the
#: successor must DO — the required ack) when its prose carries an order
#: marker. Performing a prescribed act is work, never a category-(a) re-derive,
#: so its cited shapes are excluded from re-derive matching (goal:g15.13 / the
#: classifier-is-derived claim).
_PRESCRIBE_RE = re.compile(
    r"\b(required|mandatory|prescribed|"
    r"must\s+(run|perform|do|ack|grant|write)|your one \w+\s+(?:required\s+)?act|"
    r"minimum wake|one \w+ decision)\b",
    re.IGNORECASE)


def _parse_facts(facts_text: str) -> list[tuple[str, list[str]]]:
    """Parse the `## facts` body into `(F-label, [command-shape...])` pairs.

    A bullet is `- F1 (...) : prose with cmd-shape citations enclosed in
    backticks.` The label is
    the `F<N>` right after the dash; the shapes are the backtick spans. A span
    counts as matchable only when it looks like a command: it carries whitespace
    (multi-token) or is a bare known tool token. A bare path like
    `config:rotations` cannot prefix-match a command and is ignored; a bare
    `ps`/`tmux`/`whois` must match (the whole point of F1/F2's by-hand reads).

    A bullet that PRESCRIBES an ordered act (`_PRESCRIBE_RE` in its prose) is a
    work-item, not a re-derivable fact: its shapes are dropped (`(F, [])`) so a
    call that performs the ordered act is never classified category-(a)."""
    out: list[tuple[str, list[str]]] = []
    cur_label: str | None = None
    cur_shapes: list[str] = []
    cur_prescribed = False

    def _flush():
        if cur_label is not None:
            # a prescribed act's shapes are NOT re-derive matchable
            out.append((cur_label, [] if cur_prescribed else cur_shapes))

    for ln in facts_text.splitlines():
        s = ln.strip()
        if not s:
            continue
        m = _FACT_LABEL_RE.match(s)
        if m:
            _flush()
            cur_label = m.group(1).upper()
            cur_shapes = []
            cur_prescribed = bool(_PRESCRIBE_RE.search(s))
        for m in re.finditer(r"`([^`]+)`", s):
            shape = _norm_cmd(m.group(1))
            if not shape:
                continue
            if " " in shape:
                cur_shapes.append(shape)
            elif shape in _BARE_FACT_TOOLS and not _bare_span_is_prose(s, m.end()):
                cur_shapes.append(shape)
    _flush()
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
        # a bare-token fact VERB (`whois`) may be cited WITHOUT the invocation
        # prefix (`python3 …/send.py whois`), so match it at any command
        # boundary, never just position 0 — but not as the ARGUMENT of a
        # leading filter verb (`grep whois`, `cat whois`) which is a search
        # over output, not a re-derive of the whois fact.
        for mm in re.finditer(r"(?<![A-Za-z0-9_])" + pattern + r"(?=\s|$)", nc):
            prev = nc[:mm.start()].rstrip()
            prev_word = prev.split()[-1] if prev.split() else ""
            if not prev_word:
                return True
            # a prev word that strips to NOTHING is a bare shell separator
            # (`;`, `&`, `|`), not a filter verb — the bare-verb re-derive stands.
            clean = prev_word.lstrip(";|& ")
            if not clean:
                return True
            if clean.split()[-1] not in _BARE_FACT_TOOLS:
                return True
        return False
    # multi-token shape: allow one optional engine-launch prefix
    # (`python3 <path>/send.py`) when the fact cites JUST the script
    # (`send.py whois <ref>`), so a live call that carries the invocation
    # prefix still re-derives the fact — the same loose fold `_first_turn_label`
    # applies to templates (goal:g15.13 / item 2).
    return bool(re.match(r"^(?:python3\s+\S*/)?" + pattern, nc))


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
    """Category c: `-h`/`--help`, or grep/rg/sed over a SOURCE FILE or a
    transcript/log — learning a tool's surface instead of doing work. Config
    nodes (.md) are NOT source/logs: grepping the seat registry by hand is a
    by-hand read (b), not protocol learning.

    A `sed -i` / `sed --in-place` is an EDIT of a source file (its OWN flag),
    not a read-only learn — it belongs to (d) real work, never (c) (g15:
    sensei.py sed -i counted as learning).

    The source/log TARGET must be a FILE ARGUMENT of the grep/sed/rg in the
    same pipe segment (a path or named script) — a grep over a piped OUTPUT
    (`send.py read … | grep -v …`) or over its own quoted pattern is not
    learning a source file (hypothesis:l4-the-audit-classifier-is-derived)."""
    low = _norm_cmd(cmd).lower()
    if re.search(r"(\s-h(\s|$)|--help)", low):
        return True
    # in-place source edits are work, not learning (the whole point of (4) in
    # hypothesis:l4-wake-audit-reads-facts-and-defaults-to-the-latest-record).
    # `-i` must be SED'S OWN flag: it directly follows the sed invocation with
    # no shell separator (`;`/`&&`/`|`) in between, so a later unrelated `-i`
    # (e.g. `… | grep -i foo`) is never attributed to sed.
    if re.search(r"\bsed\b[^;&|\n]*(--in[-_ ]?place|-i)\b", low):
        return False
    return _greps_a_source(low)


_SRC_SCRIPT_NAMES = {
    "rotate.py", "write.py", "send.py", "sensei.py", "commands.py",
    "spawn_budget.py", "provisioning.py", "snapshot-goals.py",
}


def _greps_a_source(low: str) -> bool:
    r"""Whether a grep/rg/sed command greps a SOURCE/LOG file target.

    The TARGET must be a file operand of the tool (a path ending in a
    source/log extension, or a named engine script) IN THE SAME PIPE SEGMENT
    before any `|`/`;`/`&&`. A grep whose only matches come from its own
    QUOTED pattern (`grep -vE '\.log$'`) or from a piped OUTPUT feed does not
    target a source file and is not protocol learning."""
    for mm in re.finditer(r"\b(grep|rg|sed)\b", low):
        seg = low[mm.end():]
        # quoted spans (patterns like `'^def \|…'`) are not file operands and
        # may contain `|`/`;` — neutralize them BEFORE splitting on command
        # separators, so a pipe inside a grep pattern is not read as a pipe.
        seg = re.sub(r"['\"][^'\"]*['\"]", " ", seg)
        # same pipe/command segment only (a later `| other`/`&& grep -i` is out)
        seg = re.split(r"[|;&]", seg)[0]
        if any(re.search(r"\.(py|sh|log|js)\b", t) or t in _SRC_SCRIPT_NAMES
               for t in seg.replace("=", " ").split()):
            return True
    return False


def _is_byhand_read(cmd: str, tool: str) -> bool:
    """Category b: a read/action the seat does BY HAND that a template entry
    (first_turn or after_join) already covers — ps/tmux process-tree checks,
    listing sessions/rotation records, reading a record/bootstrap json, the
    ListAgents/ToolSearch join, and grepping the seat-registry config node.
    The `rotate.py ack` / `meter --pin` steps are owned by category `s`
    (service-owed), handled before this rule is ever reached."""
    nc = _norm_cmd(cmd).lower()
    if re.search(r"\bps(\s|$)", nc) or re.search(r"\btmux\b", nc):
        return True
    if re.search(r"sessions/rotations|claude/projects", nc):
        return True
    if re.search(r"(ls|cat|sed|grep)\b.*(sessions|rotations|bootstrap|\.ack\.json|\.meter|seats\.md)", nc):
        return True
    if re.search(r"rotate\.py ack|rotate\.py meter --pin", nc):
        return True
    # a hand-run `send.py read {seat}` re-reads the inbox a startup first_turn
    # entry already covers — a by-hand read (b), never real work (d). A call
    # that matches the first_turn template exactly is already category (a)
    # (label beats b), so only the prefixed/piped variant lands here.
    if re.search(r"send\.py read", nc):
        return True
    if re.search(r"\bwhois\b", nc) or tool in ("ListAgents", "ToolSearch"):
        return True
    # a command that names seats.md / config:seats together with a read-ish
    # verb ANYWHERE (before or after a pipe: `git show ...seats.md | grep`)
    # is a by-hand read, never real work (master-sensei proposal (e) first
    # half). Config .md nodes are NOT source/logs, so this never reaches c.
    if re.search(r"\b(grep|rg|sed|awk|cat|git show)\b", nc) and re.search(
            r"(seats\.md|config:seats)", nc):
        return True
    return False


def _after_join_label(cmd: str, seat: str,
                      after_join: list[dict] | None) -> str | None:
    """The service-owed (s) label of a hand-redone after_join step, or None.

    The two named steps (`rotate.py ack`, `rotate.py meter --pin`) are always
    service-owed with their fixed labels; every other step must come from the
    live template's `startup.after_join` list (never a hardcoded list beyond
    the two named), matched with the same loose `{...}`-folding `_first_turn_`
    label uses."""
    nc = _norm_cmd(cmd)
    if not nc:
        return None
    low = nc.lower()
    if re.search(r"\brotate\.py\s+ack\b", low):
        return "ack"
    if re.search(r"\brotate\.py\s+meter\s+--pin\b", low):
        return "meter"
    for e in after_join or []:
        tpl = _norm_cmd((e.get("cmd") or "").replace("{seat}", seat))
        if not tpl:
            continue
        parts = re.split(r"\{[^}]+\}", tpl)
        toks = [re.escape(p) for p in parts]
        pattern = r"\S+".join(toks) if len(parts) > 1 else re.escape(tpl)
        if re.match(r"^" + pattern, nc):
            return e.get("label")
    return None


def classify_call(cmd: str, tool: str, seat: str,
                  entries: list[dict] | None = None,
                  facts: list[tuple[str, list[str]]] | None = None,
                  after_join: list[dict] | None = None) -> tuple[str, str | None]:
    """One assistant tool_use call across the wake categories.

    Returns `(category, label)`. Category precedence: protocol learning (c)
    beats a first_turn re-derive (a) — learning the tool is not re-deriving a
    fact — and a first_turn/fact re-derive (a) beats a service-owed (s), which
    beats a hand-read (b).
    c only when `-h`/`--help` or a source/log grep; a when the call's command
    re-runs a configured first_turn cmd (label = the entry) or re-derives a
    `## facts` bullet's own cited command shape (label = `F<N>`); s when it is
    a hand-redone after_join step (label = the step); b when it is a hand-read
    a startup entry could pre-run; d otherwise (real work)."""
    label = _first_turn_label(cmd, seat, entries or [])
    if _is_protocol_learning(cmd, tool):
        return "c", label
    if label is not None:
        return "a", label
    if facts:
        f_label = _fact_label(cmd, facts)
        if f_label is not None:
            return "a", f_label
    s_label = _after_join_label(cmd, seat, after_join)
    if s_label is not None:
        return "s", s_label
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


def _hand_read_paths(entries: list[dict], facts, seat: str) -> set:
    """Derive the set of by-hand-read PATH SIGNALS for a wake.

    Category (b) for a NON-Bash Read/Grep/Glob is "a file a configured step
    already pre-runs". That set is DERIVED, never a literal audit list: every
    signal traces to a role's first_turn entry or a `## facts` cited shape (the
    files/records those cmds read), plus the seat's OWN record / pin (meter) /
    ack / bootstrap / transcript locations (hypothesis:l4-the-audit-
    classifier-is-derived)."""
    signals: set[str] = set()

    def _scan(cmd: str) -> None:
        if not cmd:
            return
        low = cmd.lower()
        # a template NODE the command reads as a file (config:rotations, ...)
        for m in re.finditer(
                r"\b(?:config|doc|build|mvp|hypothesis|experiment|verdict|outcome|idea):[A-Za-z0-9_.\-]+",
                cmd):
            signals.add(m.group(0))
        # a rotate-self RECORD read — the seat's OWN record file is derived at
        # the bottom from the seat identity (`sessions/rotations/<seat>`), never
        # as a bare generic directory that would match every seat's record.
        # the seat REGISTRY a whois / seats.md read touches
        if re.search(r"\bwhois\b", low) or "seats.md" in low:
            signals.add("seats.md")
        # (the successor's transcript path is SESSION-id based, not seat-
        # derivable here, so no generic `claude/projects` signal is emitted —
        # the bare-substring falsifier of item 6 must stay empty)

    for e in (entries or []):
        _scan(e.get("cmd") or "")
    for _label, shapes in (facts or []):
        for sh in shapes:
            _scan(sh)
    # the seat's OWN locations, DERIVED from the seat identity + the sessions
    # layout (rotation record, ack, bootstrap, pin/meter) — never a bare
    # generic substring list (hypothesis:l4-the-audit-classifier-is-derived,
    # item 6's falsifier: a hand-read path list that is still literal).
    s = seat.lower()
    signals.add(f"sessions/rotations/{s}")        # the seat's rotation record
    signals.add(f"seats/{s}.ack.json")            # the seat's ack
    signals.add(f"seats/{s}.bootstrap.json")      # the seat's bootstrap
    signals.add(f"sessions/{s}.meter")            # the seat's pin / meter
    return signals


def _path_is_hand_read(s: str, signals: set) -> bool:
    """Whether a NON-Bash tool's path names a file a first_turn/fact entry or
    the seat's own locations already pre-run — a by-hand read (b), never real
    work. Mirrors the file-path signals of `_is_byhand_read`, but DERIVED from
    `_hand_read_paths` — never a literal hard-coded file list."""
    low = _norm_cmd(s).lower()
    if not low:
        return False
    return any(sig in low for sig in signals)


def classify_tool_use(tool: str, inp, seat: str,
                      entries: list[dict] | None,
                      facts: list[tuple[str, list[str]]] | None,
                      hand_paths: set,
                      after_join: list[dict] | None = None) -> tuple[str, str | None, str]:
    """The ONE tool-wrapper BOTH audits call (hypothesis:l4-the-wake-window-
    ends-at-the-ack-and-both-audits-share-one-tool-wrapper). Routes one
    assistant tool_use to `(cat, label, cmd)` by its OWN input shape —
    sharing `_synthesize_read_cmd`/`_path_is_hand_read` (Read/Grep/Glob),
    `_WRITELIKE_TOOLS` (Edit/Write -> d), anything else to `classify_call`
    with the Bash command and the parsed facts. wake_audit and
    rotate_out_audit MUST yield the same (cat, label) for the same tool_use;
    this wrapper is the guarantee (a tool_use the two audits classify
    differently is a falsifier)."""
    if tool in _WRITELIKE_TOOLS:
        # Edit/Write are WRITES: even onto a first_turn-covered path they are
        # real work (d), never a by-hand read (b).
        return "d", None, ""
    if tool in _READLIKE_TOOLS:
        # non-Bash Read/Grep/Glob are judged by their OWN paths: a covered
        # path is a by-hand read (b), anything else is real work (d). Such
        # calls carry no command, so they never match a first_turn/fact
        # re-derive (a) nor protocol learning (c).
        cmd = _synthesize_read_cmd(tool, inp)
        cat, label = ("b", None) if _path_is_hand_read(cmd, hand_paths) else ("d", None)
        return cat, label, cmd
    cmd = inp.get("command", "") if isinstance(inp, dict) else ""
    # `after_join` (L4.251, merged at the SL2#3 sync): a hand-redone
    # after_join step is service-owed (s) — passed through unchanged so both
    # audits keep yielding one (cat, label) for one tool_use.
    cat, label = classify_call(cmd, tool, seat, entries, facts, after_join)
    return cat, label, cmd


def _iter_tool_uses(path: Path):
    """Yield `(tool, input_dict)` for every assistant tool_use in a CC JSONL
    transcript, in file order, tolerating corrupt lines (errors=replace)."""
    for _idx, tool, inp, _ts in _iter_assistant_tool_uses(path):
        yield tool, inp


def _iter_assistant_tool_uses(path: Path):
    """Yield `(line_index, tool, input_dict, timestamp)` for every assistant
    tool_use in a CC JSONL transcript, in file order.

    Shared low-level read behind both `_iter_tool_uses` (wake-audit) and the
    rotate-out window scanner (which needs the line offset to start after the
    last real input AND the timestamp to bound the window by the record).
    line_index is the jsonl offset (0-based). One JSONL
    line may carry several tool_use blocks; each yields its own row. The
    timestamp is the event's `timestamp` (or message.timestamp), else None.
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
            ts = ev.get("timestamp") or (ev.get("message") or {}).get("timestamp")
            ts = str(ts) if ts else None
            for b in content:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    yield ln_idx, b.get("name", "?"), b.get("input") or {}, ts


def _tool_uses_after(path: Path, start_line: int, until_ts: str | None = None):
    """The subset of `_iter_tool_uses` whose jsonl line is at/after
    `start_line` and — when `until_ts` is given — at or before that timestamp.

    Used for the rotate-out window: every assistant tool_use after the last
    real user input (AT OR BEFORE the record), up to the record's `recorded_at`.
    A tool_use with NO timestamp is kept (cannot be proved after the bound),
    preserving legacy behavior for untimestamped fixture transcripts.
    """
    for idx, tool, inp, ts in _iter_assistant_tool_uses(path):
        if idx < start_line:
            continue
        if until_ts is not None and ts is not None and _normts(ts) > _normts(until_ts):
            continue
        yield tool, inp


def _last_real_input(path: Path,
                     not_after_ts: str | None = None) -> tuple[int, str | None]:
    """The last user turn that is NOT a tool_result (a merge-up reply, an
    owner/Prime turn). Returns `(line_index, timestamp|None)`; (-1, None)
    when the transcript has no real user turn (the whole head is the window).

    `not_after_ts` (the rotation record's `recorded_at`) bounds the search: a
    real input STRICTLY AFTER the record — a farewell turn after the rotation —
    cannot be the window start, so the window is bounded by the record, not by
    the transcript end (hypothesis:l4-the-audit-classifier-is-derived-and-the-
    window-is-bounded-by-the-record)."""
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
            ts = ev.get("timestamp") or ev.get("message", {}).get("timestamp")
            # a real input strictly AFTER the record's recorded_at (a farewell
            # turn after the rotation) cannot restart the window
            if (not_after_ts is not None and ts is not None
                    and _normts(str(ts)) > _normts(not_after_ts)):
                continue
            last_idx = ln_idx
            if ts:
                last_ts = str(ts)
    return last_idx, last_ts


#: Non-Bash tools whose OWN input names the file(s) a wake reads by hand.
_READLIKE_TOOLS = ("Read", "Grep", "Glob")
#: Tools whose input is an EDIT/WRITE of a file — always real work (d),
#: regardless of whether the path is one a first_turn entry pre-runs.
_WRITELIKE_TOOLS = ("Edit", "Write", "WriteFile", "MultiEdit",
                    "NotebookEdit")
#: How many calls after the ack the wake window will scan for the row commit
#: that seals the seating (`git commit` naming seats.md). F8's wake ends at
#: the ack INCLUSIVE; when the card edit + `git add seats.md && git commit`
#: land right after it (measured: belam 175816Z calls 20-22), the window
#: extends to that commit. A commit further out is the seat's REAL work, not
#: wake.
ROW_COMMIT_LOOKAHEAD = 3


def _is_ack_cmd(cmd: str) -> bool:
    """Whether a Bash command is the `rotate.py ack` wake act itself.
    Splits on shell separators so a `rotate.py ack --help` protocol probe
    (a segment carrying `-h`/`--help`) is never mistaken for the act — F8's
    wake act is the `ack --seat <S> --gen <N> --ref <R> continue|diff`
    invocation, never a usage read."""
    nc = _norm_cmd(cmd)
    for seg in re.split(r"[;&|]+", nc):
        m = re.search(r"rotate\.py\s+ack\b", seg)
        if m is None:
            continue
        after = seg[m.start():]
        if re.search(r"(--help|(?<!\w)-h(?=\s|$))", after):
            continue
        return True
    return False


def _is_row_commit(cmd: str) -> bool:
    """Whether a Bash command is the row commit that seals a seating: a
    `git commit` whose command names `seats.md` (the seat row)."""
    nc = _norm_cmd(cmd)
    return bool(re.search(r"\bgit\s+commit\b", nc)) and "seats.md" in nc


def wake_audit(root: Path, seat: str, gen: int | None,
               transcript_path: Path | None) -> tuple[int, list[dict], dict]:
    """Run the classification over the seat's wake transcript.

    Returns `(exit_code, per_call_rows, counts)` so the CLI body and the tests
    share one implementation. Reads the LIVE config:rotations template AND the
    `## facts` bullets for the seat's role. The transcript is resolved in the
    g15 order (explicit --transcript, else the seat's LATEST rotation record's
    own session_log — never the env / newest-.jsonl fallbacks). The window
    runs from the first assistant tool_use to the first call classifiable as
    real work (category d, excluded); service-owed (s) calls never cut it."""
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
    hand_paths = _hand_read_paths(entries, facts, seat)
    after_join = _extract_after_join(fm, role)

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
    counts = {"a": 0, "b": 0, "c": 0, "d": 0, "s": 0}
    # window bookkeeping: the ack call (F8's wake act) and the first
    # classifier-(d) call, both 1-based call indices over ALL transcript
    # calls scanned (before the window cut).
    ack_idx: int | None = None
    first_d_idx: int | None = None
    for tool, inp in _iter_tool_uses(log_path):
        cat, label, cmd = classify_tool_use(
            tool, inp, seat, entries, facts, hand_paths, after_join)
        calls.append({"tool": tool, "cmd": cmd, "cat": cat,
                      "summary": _summarize_tool_input(inp), "label": label,
                      "source": source})
        counts[cat] += 1
        idx = len(calls)
        if ack_idx is None and _is_ack_cmd(cmd):
            ack_idx = idx
        if first_d_idx is None and cat == "d":
            first_d_idx = idx

    # The window ends at the ack call INCLUSIVE (hypothesis:l4-the-wake-
    # window-ends-at-the-ack / F8: anything before the ack is wake); when the
    # row commit that seals the seating (`git commit` naming seats.md) lands
    # right after it, extend to that commit. No ack call keeps the old
    # first-(d) rule; no ack and no (d) runs the whole transcript. The reason
    # is reported machine-readably in the header area via `window_reason`.
    window_end = len(calls)
    reason = "transcript end"
    if ack_idx is not None:
        # Reconciled with L4.251 (service-owed `s`, merged at the SL2#3
        # sync): BEFORE the ack nothing cuts the window (a classifier-(d)
        # `git status` on a spawn seating is still wake — the 22/32-call
        # defect); AFTER the ack, hand-redone after_join steps (s) and hand
        # reads never cut it either — only the first (d) after the ack does,
        # inclusive, and the row commit that seals the seating is exactly
        # that (d) when it follows. No (d) after the ack = the window runs
        # to the transcript end (the ack was the last real act).
        end = len(calls)
        reason = f"ack call {ack_idx}" if end == ack_idx else \
            f"ack call {ack_idx}, transcript end {end}"
        for i in range(ack_idx + 1, len(calls) + 1):
            if calls[i - 1]["cat"] == "d":
                end = i
                if _is_row_commit(calls[i - 1]["cmd"]):
                    reason = f"ack call {ack_idx} + row commit {end}"
                else:
                    reason = f"ack call {ack_idx}, first (d) at {end}"
                break
        window_end = end
    elif first_d_idx is not None:
        window_end = first_d_idx
        reason = f"first (d) at {first_d_idx}"

    window_calls = calls[:window_end]
    window_counts = {"a": 0, "b": 0, "c": 0, "d": 0, "s": 0}
    for c in window_calls:
        window_counts[c["cat"]] += 1
    window_counts["window_reason"] = reason
    return 0, window_calls, window_counts


def redact_text(s: str) -> str:
    """Mask secrets / emails / message bodies in one printed summary or cmd.

    `--redact` is ON by default so the audit never pastes a key/token/email
    into a tracked report; `--no-redact` gives the local raw view. Order
    matters: message bodies go first (their whole text becomes
    `<redacted:message>`), then key/token shapes, then emails — each run once
    across the string so an earlier replacement can never be re-scanned and
    re-mangled by a later rule. Counts and categories are untouched.
    """
    text = s
    # message-shaped calls: keep the verb + recipient, mask the text arg
    m = re.search(
        r"(?is)(send\.py\s+(?:send|report|escalate)\s+\S+)(\s+.*)?$", text)
    if m and m.group(2) and m.group(2).strip():
        text = m.group(1) + " <redacted:message>"
    # a JSON dump's `"message": "..."` field (SendMessage & friends)
    text = re.sub(r'("message"\s*:\s*")[^"]*(")',
                  r"\1<redacted:message>\2", text)
    # key / token shapes
    for pat, rep in (
        (re.compile(r"sk-or-v1-[A-Za-z0-9_-]+"), "<redacted:key>"),
        (re.compile(r"\bsk-[A-Za-z0-9]{20,}"), "<redacted:key>"),
        (re.compile(r"\bghp_[A-Za-z0-9]+"), "<redacted:key>"),
        (re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]+"), "<redacted:key>"),
        (re.compile(r"\b[A-Za-z0-9_.]+=[A-Za-z0-9+/]{40,}"), "<redacted:key>"),
        (re.compile(r"\b[0-9a-fA-F]{32,}\b"), "<redacted:key>"),
    ):
        text = pat.sub(rep, text)
    # emails
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
                  "<redacted:email>", text)
    return text


def cmd_wake_audit(root: Path, args) -> int:
    code, calls, counts = wake_audit(root, args.seat, args.gen,
                                     Path(args.transcript) if args.transcript else None)
    if code != 0:
        return code
    redact = getattr(args, "redact", True)
    gen_label = args.gen if args.gen is not None else "latest"
    print(f"sensei.py wake-audit --seat {args.seat} --gen {gen_label} "
          f"(role {seat_row(load_seats(root), args.seat)['role']})")
    print(f"window: first assistant tool_use -> ack / first real work "
          f"({len(calls)} calls scanned, {counts.get('window_reason', '?')})")
    print(f"counts: a={counts['a']} b={counts['b']} c={counts['c']} d={counts['d']}")
    print(f"  window_end: {counts.get('window_reason')}")
    s_labels = [c["label"] for c in calls if c["cat"] == "s" and c["label"]]
    print(f"service-owed: s={counts['s']} ({', '.join(s_labels)})")
    print(f"  (d counts the cut call itself; only a/b/c span the wake window "
          f"and s is service-owed, outside the window)")
    print(f"transcript: {calls[0]['source'] if calls else '?'}")
    for i, c in enumerate(calls, 1):
        lbl = f" <{c['label']}>" if c["label"] else ""
        summary = redact_text(c["summary"]) if redact else c["summary"]
        print(f"  {i:>2} [{c['cat']}] {c['tool']}: {summary}{lbl}")
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
    rot = locations.shared_sessions_dir(root) / rotate.ROTATIONS_DIR_NAME
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
    transcript: the outgoing record's `s12_self_reap.chain` — the ONE reap
    section (g15.25 (c): the `handover.reap_own_pid` stand-in is retired)."""
    pids: list[int] = []
    s12 = rec.get("s12_self_reap")
    if isinstance(s12, dict) and isinstance(s12.get("chain"), list):
        pids += [p for p in s12["chain"] if isinstance(p, int)]
    return pids


def _resolve_predecessor_transcript(
        root: Path, seat: str, gen: int, records: list[tuple[Path, dict]],
        explicit: str | None,
        registry_dir: str | None = None) -> tuple[Path | None, str]:
    """Resolve the OUTGOING predecessor's transcript `--gen N`.

    Resolution order (never the newest slug-dir transcript — that one is the
    successor's, and it would be a named false positive): (1) explicit
    `--transcript`; (2) the previous record of the same seat whose
    `b_generation.after == N` — it carries the `handover.join.transcript` of
    gen N joining; (3) `~/.claude/sessions/<pid>.json` for a pid in the
    OUTGOING record's `s12_self_reap.chain` (the ONE reap section — the
    `handover.reap_own_pid` stand-in is retired, g15.25 (c)), resolved
    through `rotate.transcript_from_registry` (the registry file is content,
    never itself the transcript — returning it would read 0 calls and exit 0,
    a silent false negative).
    Returns `(path|None, reason)`. A registry file that parses and NAMES a
    derived transcript that is absent resolves to `(None, "registry <f> names
    <p>")` — a NAMED REFUSAL the caller must print (never a quiet `0 calls`)."""
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
    reg_dir = Path(registry_dir or rotate.REGISTRY_DEFAULT_DIR).expanduser()
    for pid in _fallback_pids(out_rec) if out_rec else []:
        cand = reg_dir / f"{pid}.json"
        if cand.is_file():
            derived = rotate.transcript_from_registry(cand)
            if derived is None:
                # registry unreadable or lacks cwd+sessionId: nothing nameable
                continue
            if derived.is_file():
                return derived, f"{cand.name} / s12_self_reap.chain"
            # registry parses and NAMES a transcript path that is ABSENT:
            # a named refusal — never a silent `0 calls` exit 0.
            return None, f"registry {cand.name} names {derived}"
    return None, "no predecessor transcript resolved"


def rotate_out_audit(root: Path, seat: str, gen: int | None,
                     transcript_path: Path | None,
                     registry_dir: str | None = None
                     ) -> tuple[int, list[dict], dict, dict]:
    """Classify the outgoing predecessor's calls from its last real input to
    the record's `recorded_at` (mirror of `wake_audit`).

    Returns `(exit_code, per_call_rows, counts, window)`. Reuses
    `classify_call`/`_iter_tool_uses`/_is_protocol_learning — refactored
    shared, never copied. `--gen` defaults to the latest record's
    `b_generation.before` (the most recent rotation). Window = every
    assistant tool_use after the last real user turn AT OR BEFORE the record's
    `recorded_at`, up to `recorded_at` (NOT the transcript end — a farewell
    turn and its calls after the rotation are excluded, belam gen IX);
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
    # BOTH audits share ONE tool wrapper (hypothesis:l4-the-wake-window-ends-
    # at-the-ack-and-both-audits-share-one-tool-wrapper): same parsed facts
    # and derived hand-read paths, so a tool_use classifies identically here
    # and on the wake side. `facts` from _read_rotations is the facts_text
    # string; `_parse_facts` turns it into the re-derive shapes.
    facts_list = _parse_facts(facts)
    hand_paths = _hand_read_paths(entries, facts_list, seat)

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
    until_ts = recorded_at or None

    log_path, source = _resolve_predecessor_transcript(
        root, seat, gen, records,
        str(transcript_path) if transcript_path else None,
        registry_dir=registry_dir)
    if log_path is None:
        if source.startswith("registry "):
            print(f"ERR: {source}, absent", file=sys.stderr)
        else:
            print(f"ERR: no predecessor transcript resolved for seat {seat!r} "
                  f"gen {gen} ({source}); pass --transcript PATH",
                  file=sys.stderr)
        return 2, [], {}, {}
    if not log_path.is_file():
        print(f"ERR: predecessor transcript not found: {log_path} "
              f"({source})", file=sys.stderr)
        return 2, [], {}, {}

    start_idx, start_ts = _last_real_input(log_path, not_after_ts=until_ts)
    calls: list[dict] = []
    counts = {"a": 0, "b": 0, "c": 0, "d": 0, "s": 0}
    for tool, inp in _tool_uses_after(log_path, start_idx, until_ts=until_ts):
        cat, label, cmd = classify_tool_use(
            tool, inp, seat, entries, facts_list, hand_paths)
        calls.append({"tool": tool, "cmd": cmd, "cat": cat,
                      "summary": _summarize_tool_input(inp), "label": label})
        counts[cat] += 1
    window = {"gen": gen, "start_line": start_idx, "start_ts": start_ts,
              "recorded_at": recorded_at, "source": source,
              "log_path": str(log_path),
              "window_reason": "predecessor window, bounded by record (rotate-out; "
                              "d is the decision, not a cut)"}
    return 0, calls, counts, window


def cmd_rotate_out_audit(root: Path, args) -> int:
    code, calls, counts, window = rotate_out_audit(
        root, args.seat, args.gen,
        Path(args.transcript) if args.transcript else None,
        registry_dir=args.registry_dir)
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
    p.add_argument("--seat", "--post", required=True)
    p.add_argument("--gen", type=int, default=None,
                   help="rotation-record generation to audit (default: the "
                        "seat's LATEST rotation record; the transcript comes "
                        "from that record's own session_log)")
    p.add_argument("--transcript", default=None,
                   help="explicit transcript path (overrides the seat's "
                        "rotation record; env/newest-.jsonl are never used)")
    p.add_argument("--redact", action=argparse.BooleanOptionalAction,
                   default=True,
                   help="mask keys/emails/message bodies in the printed "
                        "report (default ON; --no-redact for a local raw view)")

    p = sub.add_parser("rotate-out-audit",
                        help="classify the outgoing predecessor's rotate-out calls")
    p.add_argument("--seat", "--post", required=True)
    p.add_argument("--gen", type=int, default=None,
                   help="generation that ROTATED OUT (default: the latest "
                        "record's b_generation.before)")
    p.add_argument("--transcript", default=None,
                   help="explicit predecessor transcript path (else resolved "
                        "from the rotation records)")
    p.add_argument("--registry-dir", default=None,
                   help="registry dir to fall back through (default: "
                        "rotate.REGISTRY_DEFAULT_DIR)")

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