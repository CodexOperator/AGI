"""L4.110 prime ruling A — rotation template resolution from a FIXTURE root.

rotate-self resolves its rotation template (brief file + step list + telemetry
set) from `.agi/nodes/.geometry/rotations.md` — a type-config node the PRIME
owns. RESOLUTION ORDER, testable: `--template <name>` > role default > refuse
loudly NAMING THE NODE. No hardcoded brief path lives in rotate.py; the brief
file always comes from the node.

The resolution/refusal tests build a throwaway .agi with its OWN rotations.md
(written by the test) and drive `rotate.main(['rotate-self', '--dry-run', ...])`
against it — they never touch the live node or seats.md. The startup-parse tests
(hypothesis:l4-rotations-startup-commands-must-parse) are the one exception:
they READ templates.*.startup.first_turn from the checked-in live
.agi/nodes/.geometry/rotations.md (both roles) so a dead command in the shipped
node fails the suite; they never write it.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import rotate  # noqa: E402

ROTATIONS_BODY = """---
id: config:rotations
mint_id: deadbeef00000000000000000000000001
type: config
templates:
  director:
    brief_file: extensions/agi/briefs/director-successor.md
    steps: [handoff, spawn, join, authority, release]
    telemetry: [seed, model, effort]
  prime_director:
    brief_file: extensions/agi/briefs/prime-director-successor.md
    steps: [handoff, spawn, join, authority, release, button-down]
    telemetry: [seed, model, effort, ack]
  helper:
    brief_file: extensions/agi/briefs/helper-successor.md
    steps: [handoff, spawn]
    telemetry: [seed]
---
# config:rotations
fixture
"""

SEATS_BODY = """---
id: config:seats
mint_id: 3e88873e3c204c5088f6ab81322a26de
type: config
seats:
  - {"name": "sanctuary-director", "role": "director"}
  - {"name": "belam", "role": "prime_director"}
---
body
"""


def _fixture_root(tmp_path, rotations: str | None,
                  seats: str | None = SEATS_BODY) -> Path:
    root = tmp_path
    agi = root / ".agi"
    agi.mkdir(parents=True, exist_ok=True)
    (agi / "config.json").write_text("{}")
    g = agi / "nodes" / ".geometry"
    g.mkdir(parents=True)
    if seats is not None:
        (g / "seats.md").write_text(seats)
    if rotations is not None:
        (g / "rotations.md").write_text(rotations)
    return agi  # the graph root (.agi), which is what find_project_root returns


def _rot_root(tmp_path, monkeypatch, rotations, seats=SEATS_BODY):
    r = _fixture_root(tmp_path, rotations, seats)

    def fake_root():
        return r
    monkeypatch.setattr(rotate, "find_project_root", fake_root)
    return r


def test_e_role_default_resolves_director(tmp_path, monkeypatch, capsys):
    """PROOF (e): on each seated role's dry run, rotate-self prints the
    template it resolved and from which level (role default)."""
    r = _rot_root(tmp_path, monkeypatch, ROTATIONS_BODY)
    rc = rotate.main(["rotate-self", "--name", "sanctuary-director",
                      "--dry-run", "--role", "director"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "(0) template" in out
    assert "director" in out
    assert "role default" in out
    assert "director-successor.md" in out
    assert "steps" in out


def test_f_explicit_template_from_another_role(tmp_path, monkeypatch, capsys):
    """PROOF (f): `--template <other-role>` resolves that role's brief/steps
    with no code change (using one role's template on another is legal)."""
    r = _rot_root(tmp_path, monkeypatch, ROTATIONS_BODY)
    rc = rotate.main(["rotate-self", "--name", "sanctuary-director",
                      "--template", "helper", "--dry-run", "--role", "director"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "--template flag" in out
    assert "helper-successor.md" in out


def test_g_removed_default_refuses_naming_node(tmp_path, monkeypatch, capsys):
    """PROOF (g): removing a role's default from the node makes its dry run
    refuse, NAMING THE NODE."""
    import re
    # drop the `director:` entry from the templates block
    body = re.sub(r"(?ms)^  director:.*?^  prime_director:",
                  "  prime_director:", ROTATIONS_BODY)
    _rot_root(tmp_path, monkeypatch, body)
    rc = rotate.main(["rotate-self", "--name", "sanctuary-director",
                      "--dry-run", "--role", "director"])
    err = capsys.readouterr().err
    assert rc == 1
    assert "rotations.md" in err
    assert "director" in err


def test_absent_node_refuses_loudly(tmp_path, monkeypatch, capsys):
    """The LIVE state until the prime lands rotations.md: the node is absent,
    and rotate-self refuses loudly naming it."""
    _rot_root(tmp_path, monkeypatch, None)
    rc = rotate.main(["rotate-self", "--name", "sanctuary-director",
                      "--dry-run", "--role", "director"])
    err = capsys.readouterr().err
    assert rc == 1
    assert "rotations.md" in err

# --- hypothesis:l4-rotations-startup-commands-must-parse -------------------
# A first_turn command that names a verb the producing tool does not have, or
# uses a placeholder EMPTY by construction at spawn time, wakes a successor
# into a usage dump (exit 2) on its very first turn (measured reproduction:
# `rotate.py whois` is not a verb; `send.py whois {succ_ref}` with {succ_ref}
# empty-by-construction). A template test must RENDER every first_turn cmd of
# every template with fixture values, assert each producing python verb parses
# with `-h` (exit 0), and assert no placeholder renders empty.

import json  # noqa: E402
import shlex  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402
import yaml as _yaml  # noqa: E402

# First_turn VALUES mirroring the LIVE canon (test_rotate_startup.VALUES), with
# every placeholder the fixed director/prime first_turn lists still uses.
STARTUP_VALUES = {
    "seat": "sanctuary-director",
    "succ_ref": "abc123",
    "succ_name": "sd-next",
    "succ_transcript": "/tmp/sd-next.jsonl",
    "pin_ref": "/tmp/sanctuary-director.meter",
    "gen": "11",
    "prime_ref": "7cff1a",
    "worktree": "/wt",
    "repo": "/repo",
    "tmux_session": "agi-rc",
    "pred_pids": "123 456",
}

# The startup-parse tests read templates.*.startup.first_turn straight from
# the checked-in .agi/nodes/.geometry/rotations.md (BOTH roles: director and
# prime_director), instead of a mirrored fixture that could mask a dead command
# in the live node. Reading the live node is all the tests do — rotations.md is
# never written here. The dead _FIXED_TEMPLATES_BODY / FIXED_FIRST_TURN fixture
# this replaced only MIRRORED the node, so a live node that regressed to
# `rotate.py whois` would keep them green; reading the bytes the suite ships is
# the only claim that holds the templates to what rotates the seats.
def _live_first_turn(path: "str | Path | None" = None) -> dict:
    """Templates.<role>.startup.first_turn for EVERY role, read from the
    checked-in .agi/nodes/.geometry/rotations.md by default (not a fixture
    copy) — or from an explicit `path=` copy, so a drift test can point the
    SHARED reader at a /tmp copy and show the live-config judgement go red
    without touching the live node (hypothesis:l4-the-drifted-node-test-is-
    in-the-suite). The rotations node is `type: config`, owned by the
    owner/prime — a kid reads it (and the fixed templates it already carries
    under hypothesis:l4-rotations-startup-commands-must-parse) and never
    writes it.
    """
    from graph_core.persistence import frontmatter as _fm  # noqa: E402
    if path is None:
        path = (Path(__file__).resolve().parents[3]
                / ".agi" / "nodes" / ".geometry" / "rotations.md")
    rot = Path(path)
    assert rot.exists(), f"rotations.md missing: {rot}"
    nf = _fm.load_node_file(rot)
    templates = nf.frontmatter.get("templates") or {}
    out = {}
    for name, ent in templates.items():
        if not isinstance(ent, dict):
            continue
        startup = ent.get("startup") or {}
        ft = startup.get("first_turn") or []
        entries = [e for e in ft if isinstance(e, dict)]
        if entries:
            out[str(name)] = entries
    return out


# --- hypothesis:l4-no-role-template-documents-a-hand-setup-... vocabulary --
# The templates' `why` lines record the hand calls each entry was created to
# REPLACE (e.g. "gen X call 1-2: the record ... read by hand") — MEASURED
# provenance, not instruction. A guard that greps EVERY template field for the
# vocabulary would RED on the shipped tree and force the deletion of the wake
# that justified each entry. So this guard discriminates INSTRUCTION (the
# fields a post ACTS ON: a first_turn/after_join entry's `cmd`/`label`, and
# the `delivery` prose the executor emits into STARTUP OUTPUT) from PROVENANCE
# (`why`, which never is).

HAND_STEP_VOCAB = ("setup call", "by hand", "run once", "pin the meter",
                   "ListAgents once")


def _live_templates(path: "str | Path | None" = None) -> dict:
    """FULL templates dict (both roles: director + prime_director) straight
    from the checked-in .agi/nodes/.geometry/rotations.md — the same
    live-reader discipline as _live_first_turn, widened to after_join and
    delivery so the vocabulary guard sees every field a post reads at wake.
    Never a mirror: a live node that regresses to "_run this setup call by
    hand" as a cmd must trip here on the shipped bytes.
    """
    if path is None:
        path = (Path(__file__).resolve().parents[3]
                / ".agi" / "nodes" / ".geometry" / "rotations.md")
    rot = Path(path)
    assert rot.exists(), f"rotations.md missing: {rot}"
    text = rot.read_text(encoding="utf-8")
    frontmatter = text.split("---", 2)[1]
    loaded = _yaml.safe_load(frontmatter) or {}
    return loaded.get("templates") or {}


def _guard_hits(templates: dict) -> list[str]:
    """Every hand-step vocabulary hit in an INSTRUCTION field, as
    '{role}:{section}.{field}: "{vocab}"'. Instruction fields are a
    first_turn/after_join entry's `cmd` and `label`, plus the template's
    `delivery` prose. `why` is provenance and is NOT scanned — it records the
    hand calls the entry REPLACES and its deletion would destroy the wake that
    paid for the entry."""
    hits = []
    for name, ent in templates.items():
        if not isinstance(ent, dict):
            continue
        startup = ent.get("startup") or {}
        for section in ("first_turn", "after_join"):
            for i, entry in enumerate(startup.get(section) or []):
                if not isinstance(entry, dict):
                    continue
                for field in ("cmd", "label"):
                    txt = entry.get(field)
                    if not isinstance(txt, str):
                        continue
                    low = txt.lower()
                    for v in HAND_STEP_VOCAB:
                        if v in low:
                            hits.append(f"{name}:{section}[{i}].{field}: {v!r}")
        delivery = ent.get("delivery")
        if isinstance(delivery, str):
            low = delivery.lower()
            for v in HAND_STEP_VOCAB:
                if v in low:
                    hits.append(f"{name}:delivery: {v!r}")
    return hits


def test_guard_live_no_instruction_field_matches_hand_vocab():
    """(i) LIVE node, both roles read from the checked-in rotations.md: no
    INSTRUCTION field (cmd/label/delivery) matches the hand-step vocabulary.
    All shipped hits live in `why` provenance lines — which a post never acts
    on — so the guard must stay GREEN here while still tripping on an
    instruction field (assertions ii/iii below)."""
    templates = _live_templates()
    assert set(templates) >= {"director", "prime_director"}
    hits = _guard_hits(templates)
    assert not hits, f"live instruction field matches hand-step vocab: {hits}"


def test_guard_fixture_cmd_hand_vocab_fails():
    """(ii) FALSIFIER (cmd): a fixture whose first_turn `cmd` says "run the
    setup call by hand" must FAIL the guard — a guard that passes on a
    template that says "by hand" is a broken guard."""
    t = _yaml.safe_load(ROTATIONS_BODY.split("---", 2)[1])["templates"]
    t["director"]["startup"] = t["director"].get("startup") or {}
    t["director"]["startup"]["first_turn"] = [
        {"label": "setup", "cmd": "echo run the setup call by hand",
         "why": "provenance-only hits stay green in assertion (iii)"}]
    hits = _guard_hits(t)
    assert hits, "cmd instruction field with hand vocab must FAIL the guard"


def test_guard_fixture_delivery_hand_vocab_fails():
    """(ii) FALSIFIER (delivery): a fixture whose `delivery` prose tells a
    post to run a step "by hand" must FAIL the guard — delivery is startup
    prose the executor emits into STARTUP OUTPUT, an instruction field."""
    t = _yaml.safe_load(ROTATIONS_BODY.split("---", 2)[1])["templates"]
    t["director"]["delivery"] = (
        "you must pin the meter by hand on your first turn")
    hits = _guard_hits(t)
    assert hits, "delivery instruction field with hand vocab must FAIL the guard"


def test_guard_fixture_why_only_hit_passes():
    """(iii) NEAR-MISS (the one that satisfies the words and fails the
    mechanism): a fixture whose ONLY vocabulary hit is an instruction-free
    `why` provenance line must PASS the guard — deleting that `why` would
    destroy the wake that paid for the entry, so the guard must not force it."""
    t = _yaml.safe_load(ROTATIONS_BODY.split("---", 2)[1])["templates"]
    t["director"]["startup"] = t["director"].get("startup") or {}
    t["director"]["startup"]["first_turn"] = [
        {"label": "rotation-record", "cmd": "true",
         "why": "gen X call 1-2: the record + sequence read by hand"}]
    assert not _guard_hits(t), "a why-only provenance hit must PASS the guard"


# --- hypothesis:l4-no-role-template-... (PARENT CORRECTION #2): the wake-
# READ body region, not the frontmatter fields. Kid 1 scanned cmd/label/
# delivery and LOST the mechanism: the field a post actually ACTS ON at wake
# is the region the `facts` first_turn entry PRINTS — `write.py
# config:rotations 'read body N:M'` emits the SAME node's body lines into
# STARTUP OUTPUT every rotation. F13 lives there and kid 1 (frontmatter-only)
# could not see it. In that region the guard must classify each vocabulary
# hit as INSTRUCTION (`by hand, one command:` — introduces a hand-run
# command, the F13 form) vs PROHIBITION (`never ... by hand`, F8/F9/F14) vs
# CITATION (`ran ... by hand before rotating` past-tense provenance, F16) —
# and FAIL only on an instruction that is not the ONE declared open sentence.

import re  # noqa: E402

# The range is never hardcoded: it is resolved from the live templates' OWN
# `facts` cmd. The range has already drifted once — F18 records 'facts range
# 37:60 (F15-F17 had fallen off the printed range)' — so a guard that bakes
# 37:61 in goes stale the moment the Sensei bumps the printed span.
# DEFECT B (parent correction): the discriminator is NOT a single literal
# phrase. `_INSTR_SIG` recognized the F13 form ('one command'/'one-call') but
# let the in-class F16 instruction escape — 'run it ONCE and emit the tokens
# it prints' (rotate-out pre-flight) hits neither. The vocab matcher below
# (`_HAND_STEP_PATTERNS`) and this signature both accept the canon's flexible
# case-insensitive phrasing (`run once`, `run it ONCE`), so F16 is SEEN and
# the classifier must decide it on its merits. The stated discriminator:
#   INSTRUCTION = the hit introduces a hand-run SETUP/PERFORM step the waked
#     post must execute (the F13 form: 'Spend by hand, one command: `…`').
#   F16's 'run it ONCE and emit the tokens it prints' is addressed to the
#     OUTGOING post at rotate-out — relay the automated `--prepare` pre-flight
#     output, the opposite of a waked hand-setup step — and is pulled back to
#     CITATION by `_EMIT_SIG`.
_INSTR_SIG = re.compile(r"one command|one-call|run\s+(?:it\s+)?once", re.I)
_NEG_SIG = re.compile(r"\b(never|no|not|nothing|none)\b", re.I)
# 'run it once and EMIT THE TOKENS it prints' — relay-the-tool guidance
# (rotate-out pre-flight), not a hand-setup step (DEFECT B discriminator).
_EMIT_SIG = re.compile(r"emit the tokens", re.I)

# The region vocabulary as (canon-label, case-insensitive regex). `run once`
# allows the single intervening word the canon actually uses ('run it ONCE'),
# so the F16 near-miss is a seen hit instead of a silent substring miss.
_HAND_STEP_PATTERNS = [
    ("setup call", re.compile(re.escape("setup call"), re.I)),
    ("by hand", re.compile(re.escape("by hand"), re.I)),
    ("run once", re.compile(r"run\s+(?:it\s+)?once", re.I)),
    ("pin the meter", re.compile(re.escape("pin the meter"), re.I)),
    ("ListAgents once", re.compile(re.escape("ListAgents once"), re.I)),
]


def _facts_body_range(templates: dict) -> tuple[int, int]:
    """The wake-read facts body region (N, M), 1-based inclusive, resolved
    from the templates' OWN `facts` first_turn cmd — `write.py
    config:rotations 'read body N:M'`. Every template carrying a facts entry
    must agree; a facts cmd that stops naming a body range fails loudly."""
    ranges = set()
    for name, ent in templates.items():
        if not isinstance(ent, dict):
            continue
        startup = ent.get("startup") or {}
        for e in startup.get("first_turn") or []:
            if not isinstance(e, dict):
                continue
            if e.get("label") != "facts":
                continue
            m = re.search(r"read body (\d+):(\d+)", e.get("cmd", ""))
            assert m, (f"{name} facts cmd does not name a body range: {e!r}")
            ranges.add((int(m.group(1)), int(m.group(2))))
    assert ranges, "no template declares a `facts` read body N:M first_turn"
    assert len(ranges) == 1, (f"facts body ranges disagree across templates: "
                              f"{ranges}")
    return ranges.pop()


def _canonical_body_lines(source: "str | Path") -> list[str]:
    """The node body split into 1-based-addressable lines through the SAME
    canonical frontmatter reader `write.py ... read body N:M` uses (BODY:BEGIN
    stripped), so the guard scans exactly the bytes the post reads at wake."""
    from graph_core.persistence import frontmatter as _fm  # noqa: E402
    nf = _fm.load_node_file(Path(source))
    return nf.body.split("\n")


def _classify_hand_hit(line: str, pos: int) -> str:
    """INSTRUCTION | PROHIBITION | CITATION for ONE vocabulary occurrence.
    PROHIBITION: a negation word ('never/no/not/...') inside the ~32 chars
      before the hit — 'never `ps`/`tmux` by hand', 'NEVER merge by hand',
      'there is no fetch+rev-parse to run by hand'.
    INSTRUCTION: the hit introduces an inline hand-run command — 'by hand,
      one command: `K=$(...)`' — the F13 form.
    CITATION: anything else — past-tense provenance ('ran ... by hand before
      rotating', F16) or a described consequence ('re-derives every fact by
      hand'), where the hit is never an order to the reading post."""
    before = line[max(0, pos - 32):pos]
    after = line[pos:pos + 80]
    if _NEG_SIG.search(before):
        return "PROHIBITION"
    if _INSTR_SIG.search(after):
        # The F16 form, 'run it ONCE and emit the tokens it prints', carries an
        # instruction signature AND the relaying marker. It is the OUTGOING
        # post's rotate-out pre-flight (`rotate-self --prepare`): run the
        # automated verb once and emit its printed tokens — never explore by
        # hand. That is the anti-hand guidance for the seat leaving, NOT a
        # hand-setup step the waked successor performs, so it stays CITATION
        # (DEFECT B: F16 is decided on its merits, not silently skipped).
        if _EMIT_SIG.search(after):
            return "CITATION"
        return "INSTRUCTION"
    return "CITATION"


def _region_hand_hits(source: "str | Path") -> list[tuple[int, int, str, str]]:
    """(line_no, pos, vocab, kind) for every hand-step vocabulary occurrence
    inside the wake-read facts body region, resolved from the templates' own
    `facts` cmd of `source`. The one reader both the live node and the
    falsifier fixtures route through."""
    templates = _live_templates(source)
    n, m = _facts_body_range(templates)
    lines = _canonical_body_lines(source)
    hits = []
    for i in range(n, m + 1):
        line = lines[i - 1]
        for label, rx in _HAND_STEP_PATTERNS:
            for mo in rx.finditer(line):
                hits.append((i, mo.start(), label, _classify_hand_hit(line, mo.start())))
    return hits


def _rotations_fixture_with_region(tmp_path: Path, body_lines: list[str],
                                   region: tuple[int, int]) -> Path:
    """A self-contained fixture rotations.md whose canonical body is exactly
    `'\n'.join(body_lines)` (the reader numbers `<!-- BODY:BEGIN -->` as
    body line 1) and whose director facts cmd reads `region_start:region_end`
    of it — so a falsifier places an injected instruction/prohibition/
    citation line in the region, at a known line, and exercises the widened
    guard hermetically. Written under tmp_path; the live node is never
    touched."""
    body = "\n".join(body_lines) + "\n"
    n, m = region
    cmd_val = (f"python3 extensions/agi/bin/write.py config:rotations "
               f"'read body {n}:{m}'")
    text = (f"---\nid: config:rotations\n"
            f"mint_id: deadbeef00000000000000000000000009\n"
            f"type: config\ntemplates:\n  director:\n"
            f"    brief_file: x\n    steps: []\n    telemetry: []\n"
            f"    startup:\n      first_turn:\n"
            f"        - {{label: facts, cmd: \"{cmd_val}\", why: fixture}}\n"
            f"---\n<!-- BODY:BEGIN -->\n{body}<!-- BODY:END -->\n")
    p = tmp_path / "rotations.md"
    p.write_text(text, encoding="utf-8")
    return p


def _region_instructions(source: "str | Path") -> list[tuple[int, int, str, str]]:
    return [h for h in _region_hand_hits(source) if h[3] == "INSTRUCTION"]


def _region_refusal(source: "str | Path") -> "str | None":
    """DEFECT A fix: the ONE decision the region guard makes, instead of a
    bare count. Both the live node and every falsifier fixture call this same
    helper and assert on the REFUSAL IT RETURNS, so a fixture cannot pass on a
    state the live assertion would refuse (and vice versa). The acceptable
    region state is: exactly ONE hand-setup instruction is declared, and it
    carries the g15-18 open code half (F13). Returns None when approved;
    returns a named REFUSAL STRING otherwise (blanket exemption — a second
    declared instruction; or an un-declared instruction — no g15-18 key).
    The old fixture test asserted `len(instructions) == 2` — a count with no
    code path anywhere that refuses a second declaration; the anti-blanket
    property lived only in the live assertion. This helper unifies them."""
    instructions = _region_instructions(source)
    if len(instructions) > 1:
        return (f"region declares {len(instructions)} hand-setup instructions; "
                f"only the ONE g15-18 open code half may be declared (blanket "
                f"exemption refused): "
                f"{[_line(source, h[0])[:45] for h in instructions]}")
    if not instructions:
        return None  # nothing declared; approved (the live region declares F13)
    line = instructions[0][0]
    if "g15-18" not in _line(source, line):
        return (f"the sole instruction must carry the g15-18 open code half "
                f"to be declared: {_line(source, line)[:60]}")
    return None


def _line(source: "str | Path", lineno: int) -> str:
    return _canonical_body_lines(source)[lineno - 1]


def test_region_live_only_f13_is_the_one_declared_instruction():
    """Widened guard on the LIVE node: resolve the region from the live
    templates' own <code>facts</code> cmd and classify every vocabulary hit in
    the bytes the wake actually prints. PROHIBITION/CITATION hits (F1 'never
    ... by hand', F8 'the record by hand', F9, F14 'NEVER merge by hand',
    F16 'ran ... by hand before rotating') must NOT trip. The ONE live
    INSTRUCTION is F13, declared by the g15-18 open code half it names.
    Blanket exemption is forbidden, so the declared set is exactly one
    sentence, and it must carry that key."""
    src = Path(__file__).resolve().parents[3] \
        / ".agi" / "nodes" / ".geometry" / "rotations.md"
    hits = _region_hand_hits(src)
    assert hits, "wake-read facts region has no hand-vocab hits at all"
    # DEFECT A: the load-bearing decision — exactly ONE declared instruction,
    # bearing the g15-18 key — is the guard's refusal verdict, shared with the
    # fixtures. Not a bare count.
    refusal = _region_refusal(src)
    assert refusal is None, refusal
    line_no = _region_instructions(src)[0][0]
    txt = _line(src, line_no)
    # declared by name: the open code half, g15-18, is written into F13
    assert "g15-18" in txt, ("the one live instruction must carry the g15-18 "
                             f"open code half to be declared, got: {txt[:90]}")
    # prohibitions and citations exist and none of them trips the guard
    kinds = {h[3] for h in hits}
    assert kinds <= {"INSTRUCTION", "PROHIBITION", "CITATION"}, kinds
    assert "PROHIBITION" in kinds and "CITATION" in kinds, (
        f"live region expected both prohibitions (F8/F9/F14) and a citation "
        f"(F16): {kinds}")


def test_region_fixture_declared_instruction_plus_forbidden_and_prose_passes(
        tmp_path):
    """FALSIFIER (the honest green, widened): a fixture whose wake-read
    region holds the F13-declared instruction ('by hand, one command' + the
    g15-18 key) ALONGSIDE a prohibition ('NEVER merge by hand') and a
    citation ('ran ... by hand before rotating') must PASS — the guard trips
    only on an un-declared instruction, never on F8/F14-style prohibition or
    F16-style citation. (Body-line layout: 1 BODY:BEGIN, 2 # config, 3 blank,
    4 ## facts, 5 blank, 6 F13, 7 F8, 8 F16 — region 6:8.)"""
    body = [
        "# config:rotations", "", "## facts", "",
        "- F13 (g15-18 is the open code half). Spend by hand, one command: "
        "`K=$(grep -m1 '^K=' .env | cut -d= -f2-) && curl -s -m 20 "
        "https://example.invalid/credits`",
        "- F8 prohibition. NEVER merge by hand ahead of it.",
        "- F16 citation. every seat ran `rotate-self -h` by hand before "
        "rotating.",
    ]
    p = _rotations_fixture_with_region(tmp_path, body, (6, 8))
    hits = _region_hand_hits(p)
    refusal = _region_refusal(p)
    assert refusal is None, refusal
    assert "g15-18" in _line(p, _region_instructions(p)[0][0])
    kinds = {h[3] for h in hits}
    assert kinds == {"INSTRUCTION", "PROHIBITION", "CITATION"}, kinds


def test_region_fixture_undeclared_instruction_fails(tmp_path):
    """FALSIFIER (widened, the load-bearing guard): a wake-read region whose
    ONLY vocabulary hit is a NEW instruction — 'grep the ledger by hand, one
    command', WITHOUT the F13 g15-18 key — must FAIL the widened guard. A
    blanket exemption set is not acceptable: only F13's sentence is declared,
    and this is not it."""
    body = [
        "# config:rotations", "", "## facts", "",
        "- F99 (new). Grep the ledger by hand, one command: `grep -n 'KEY' "
        "secrets.txt` (unkeyed — not the declared open sentence).",
        "- F8 prohibition. NEVER touch the record by hand.",
    ]
    p = _rotations_fixture_with_region(tmp_path, body, (6, 7))
    refusal = _region_refusal(p)
    assert refusal is not None, ("an instruction lacking the g15-18 key must "
                                 "be REFUSED, not just counted")
    assert "g15-18" in refusal  # the refusal names the missing declaration
    # and a guard over the frontmatter fields alone still MISSES it (the
    # near-miss kid 1's scan could not see): the cmd/label/delivery guard is
    # green even though the wake prints this hand instruction.
    t = _live_templates(p)
    assert not _guard_hits(t), "frontmatter-field guard is the weaker half"


def test_region_fixture_blanket_exemption_refused(tmp_path):
    """FALSIFIER (anti-blanket-exemption, DEFECT A fixed): two
    g15-18-stamped instructions in the region must be REFUSED — the declared
    set is keyed to the ONE open sentence, not to a marker anyone can copy.
    The fixture drives `_region_refusal` — the SAME decision the live
    assertion calls — and asserts it returns a refusal string, not that a
    bare `len == 2` happens to hold (the old count had no code path that
    refused anything). Only F13 may be declared."""
    body = [
        "# config:rotations", "", "## facts", "",
        "- F13 (g15-18). Spend by hand, one command: `curl ...`",
        "- F99 (g15-18 too). Grep by hand, one command: `grep ...`",
    ]
    p = _rotations_fixture_with_region(tmp_path, body, (6, 7))
    assert len(_region_instructions(p)) == 2  # the fixture really holds two
    refusal = _region_refusal(p)
    assert refusal is not None, ("two declared instructions must be REFUSED "
                                 "(blanket exemption), not silently allowed")
    assert "blanket" in refusal and "ONE" in refusal


def test_region_live_f16_run_once_seen_but_not_a_waked_hand_step():
    """DEFECT B pin on the LIVE node: the widened vocabulary must SEE and
    class the canon's flexible `run it ONCE` (F16) — not miss it as a
    substring gap ('run once' vs 'run it once'). Once seen, F16's instruction
    must NOT count as a waked hand-setup step: its 'run it once and emit the
    tokens it prints' is addressed to the OUTGOING post's rotate-out
    pre-flight (`rotate-self --prepare`) — relay the automated tool's output,
    the anti-hand guidance for the seat leaving — so F13 remains the region's
    ONE declared INSTRUCTION and the widened guard stays green."""
    src = Path(__file__).resolve().parents[3] \
        / ".agi" / "nodes" / ".geometry" / "rotations.md"
    lines = _canonical_body_lines(src)
    n, m = _facts_body_range(_live_templates(src))
    run_once_lines = [i for i in range(n, m + 1)
                      if re.search(r"run\s+it\s+once", lines[i - 1], re.I)]
    assert len(run_once_lines) == 1, (
        f"expected exactly F16's run-it-once line in the region, got "
        f"{run_once_lines}")
    i = run_once_lines[0]
    hits = [h for h in _region_hand_hits(src)
            if h[0] == i and "run once" in h[2]]
    assert hits, "F16's 'run it ONCE' must be a SEEN vocabulary hit"
    assert {h[3] for h in hits} <= {"CITATION"}, (
        f"F16's pre-flight is addressed to the outgoing post at rotate-out, "
        f"not a waked hand-setup step: {[(h[1], h[3]) for h in hits]}")
    # the seen-and-decided F16 still leaves exactly the ONE F13 instruction
    refusal = _region_refusal(src)
    assert refusal is None, refusal


def _producing_python_verb(cmd: str) -> tuple[Path, str] | None:
    """For an engine-python producing stage (`python3 <abs|rel>.py <verb> ...`),
    return (abs_script, verb); None for a non-python producer (git/tmux/ps) or
    a help-only stage (script already invoked with `-h`)."""
    try:
        toks = shlex.split(cmd)
    except ValueError:
        return None
    if not toks or toks[0] not in ("python3", sys.executable):
        return None
    if len(toks) < 3:
        return None
    script = toks[1]
    if not script.endswith(".py") or "extensions/" not in script:
        return None
    verb = toks[2]
    if verb.startswith("-"):
        return None  # help-only stage, parses by construction
    p = Path(script)
    if not p.is_absolute():
        p = Path(__file__).resolve().parents[3] / script  # repo-root-relative
    return p, verb


def test_uniquely_director_first_turn_is_the_shipped_outer_shape():
    # Outer-shape guard on the LIVE node, not a mirror: the checked-in
    # rotations.md director first_turn must carry the shipped `rotation-record`
    # fix and must NOT carry the dead `seat-row` (it read {succ_ref}, empty by
    # construction at spawn — the row is only produced by the successor's own
    # ack). If the live node drifts, the guard trips here AND the parse/
    # empty-assertions below guard the templates that actually ship.
    first_turn = _live_first_turn()
    assert "director" in first_turn, "live rotations.md has no director template"
    assert "prime_director" in first_turn, (
        "live rotations.md has no prime_director template")
    cmds = [e["label"] for e in first_turn["director"]]
    assert "rotation-record" in cmds
    assert "seat-row" not in cmds  # the fix: seat-row cannot succeed at spawn


def test_every_first_turn_producing_verb_parses_and_no_placeholder_empty():
    # hypothesis:l4-rotations-startup-commands-must-parse, fix-proof on the
    # LIVE node: render every first_turn cmd of EVERY template read from the
    # checked-in .agi/nodes/.geometry/rotations.md (director + prime_director),
    # assert each producing python verb parses (`<argv0> <verb> -h` exit 0) and
    # that no placeholder was left EMPTY (`{p}` resolving to "") — the state
    # that made `send.py whois {succ_ref}` dump usage (empty session_ref).
    # A live node that regresses to `rotate.py whois` fails here (whois is not
    # a rotate.py verb — the falsifier below proves it), which is exactly the
    # drift the FIXED_FIRST_TURN fixture used to mask.
    import re as _re
    first_turn = _live_first_turn()
    assert set(first_turn) >= {"director", "prime_director"}, (
        "expected BOTH templates' first_turn in the live rotations.md")
    checked_verb = 0
    for tmpl_name, entries in first_turn.items():
        for entry in entries:
            cmd = entry["cmd"]
            # every placeholder the cmd uses must have a NON-EMPTY value —
            # the state whose absence made `send.py whois {succ_ref}` dump
            # usage (empty session_ref) at spawn.
            used = _re.findall(r"\{([A-Za-z_][A-Za-z0-9_]*)\}", cmd)
            for key in used:
                assert STARTUP_VALUES.get(key), (
                    f"{tmpl_name}/{entry['label']} uses {{{key}}} which is "
                    f"EMPTY at spawn: {cmd!r}")
            rendered = rotate._resolve_startup_placeholders(cmd, STARTUP_VALUES)
            assert "{" not in rendered, (tmpl_name, entry["label"], rendered)
            # check every stage of a `;` sequence and the FIRST stage of each
            # `|` pipeline (the producing stage; post-`|` filters are sed/head)
            for stage in rendered.split(";"):
                producing = stage.split("|")[0].strip()
                if not producing:
                    continue
                pv = _producing_python_verb(producing)
                if pv is None:
                    continue
                script, verb = pv
                r = subprocess.run(
                    [sys.executable, str(script), verb, "-h"],
                    capture_output=True, text=True)
                assert r.returncode == 0, (
                    f"{tmpl_name}/{entry['label']} verb {verb!r} does not "
                    f"parse: {r.stderr.strip() or r.stdout.strip()}")
                checked_verb += 1
    assert checked_verb >= 2, "each of the two live templates must check a verb"


def test_falsifier_old_rotate_whois_does_not_parse():
    # The falsifier, made load-bearing: the OLD shipped command
    # `rotate.py whois` is NOT a verb — `-h` exits 2 (usage). The fix proof is
    # that the assertion above passes for `rotate.py status ... --record
    # latest` while this one proves whois is genuinely the defect.
    r = subprocess.run([sys.executable, str(BIN / "rotate.py"), "whois", "-h"],
                       capture_output=True, text=True)
    assert r.returncode != 0, "rotate.py whois must not parse (it has no such verb)"
    assert "invalid choice: 'whois'" in r.stderr


def test_status_record_reads_latest_surfaces_capsys(tmp_path, monkeypatch, capsys):
    root = tmp_path / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / "nodes" / ".geometry" / "seats.md").write_text(SEATS_BODY)
    rot = root / "sessions" / "rotations"
    rot.mkdir(parents=True)
    import datetime
    stamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
    (rot / f"sanctuary-director.{stamp}.json").write_text(
        json.dumps({"rotation": "rotate-self", "seat": "sanctuary-director",
                    "result": "success", "recorded_at": "2026-09-11T00:00:00Z"}))

    def fake_root():
        return root
    monkeypatch.setattr(rotate, "find_project_root", fake_root)
    rc = rotate.main(["status", "--seat", "sanctuary-director",
                      "--record", "latest"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "latest rotation record" in out
    assert "result" in out and "success" in out
    assert "sequence=" in out
    assert "row:" in out and "sanctuary-director" in out


def test_wait_returns_zero_when_record_already_terminal(
        tmp_path, monkeypatch, capsys):
    """hypothesis:rotate-status-record-latest-gains-wait FALSIFIER (a): a
    `--wait` call must return 0 immediately (never sleep) when the record is
    already terminal — s12_self_reap present — on its first read."""
    import datetime
    root = tmp_path / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / "nodes" / ".geometry" / "seats.md").write_text(SEATS_BODY)
    rot = root / "sessions" / "rotations"
    rot.mkdir(parents=True)
    stamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
    (rot / f"sanctuary-director.{stamp}.json").write_text(json.dumps({
        "rotation": "rotate-self", "seat": "sanctuary-director",
        "result": "success", "s12_self_reap": {"pane_pid": 123}}))

    def fake_root():
        return root
    monkeypatch.setattr(rotate, "find_project_root", fake_root)

    def boom(*a, **k):
        raise AssertionError("--wait slept past an already-terminal record")
    monkeypatch.setattr(rotate.time, "sleep", boom)

    rc = rotate.main(["status", "--seat", "sanctuary-director",
                      "--record", "latest", "--wait", "30"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "s12_self_reap" in out and "123" in out
    assert "sequence=" in out


def test_wait_times_out_when_record_never_terminal(
        tmp_path, monkeypatch, capsys):
    """hypothesis:rotate-status-record-latest-gains-wait FALSIFIER (b): a
    `--wait N` whose record never becomes terminal must time out, print the
    last-seen record plus ERR, and exit 2 — never return 0."""
    import datetime
    root = tmp_path / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / "nodes" / ".geometry" / "seats.md").write_text(SEATS_BODY)
    rot = root / "sessions" / "rotations"
    rot.mkdir(parents=True)
    stamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
    (rot / f"sanctuary-director.{stamp}.json").write_text(json.dumps({
        "rotation": "rotate-self", "seat": "sanctuary-director",
        "result": "success"}))

    def fake_root():
        return root
    monkeypatch.setattr(rotate, "find_project_root", fake_root)

    # drive the poll entirely on a fake clock + advancing sleep so the
    # suite spends no wall time (hypothesis:l4-status-wait-waits-for-the-
    # record-to-appear).
    clock = {"now": 1000.0}
    monkeypatch.setattr(rotate.time, "monotonic", lambda: clock["now"])
    monkeypatch.setattr(rotate.time, "sleep",
                        lambda s: clock.update(now=clock["now"] + s))

    rc = rotate.main(["status", "--seat", "sanctuary-director",
                      "--record", "latest", "--wait", "3"])
    cap = capsys.readouterr()
    assert rc == 2
    assert "ERR: still not terminal after 3s" in cap.err
    assert "latest rotation record" in cap.out
    assert "success" in cap.out


def test_wait_waits_for_record_to_appear_then_terminal(
        tmp_path, monkeypatch, capsys):
    """hypothesis:l4-status-wait-waits-for-the-record-to-appear happy path:
    with NO record yet, `--wait N` must wait for the record to APPEAR and
    then for its s12_self_reap, within one deadline — exiting 0 with the
    terminal record printed. Previously the no-record path returned 0 at
    once with `(no rotation record for <seat>)`, never waiting at all."""
    import datetime
    root = tmp_path / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / "nodes" / ".geometry" / "seats.md").write_text(SEATS_BODY)
    rot = root / "sessions" / "rotations"
    rot.mkdir(parents=True)

    clock = {"now": 1000.0}
    created = {"done": False}

    def fake_root():
        return root
    monkeypatch.setattr(rotate, "find_project_root", fake_root)
    monkeypatch.setattr(rotate.time, "monotonic", lambda: clock["now"])

    def fake_sleep(secs):
        # the record lands partway through the wait, inside the deadline
        if not created["done"]:
            created["done"] = True
            stamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
            (rot / f"sanctuary-director.{stamp}.json").write_text(json.dumps({
                "rotation": "rotate-self",
                "seat": "sanctuary-director",
                "result": "success",
                "s12_self_reap": {"pane_pid": 555}}))
        clock["now"] += secs
    monkeypatch.setattr(rotate.time, "sleep", fake_sleep)

    rc = rotate.main(["status", "--seat", "sanctuary-director",
                      "--record", "latest", "--wait", "30"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "(no rotation record" not in out
    assert "s12_self_reap" in out and "555" in out
    assert "sequence=" in out


def test_wait_for_missing_record_times_out(tmp_path, monkeypatch, capsys):
    """hypothesis:l4-status-wait-waits-for-the-record-to-appear FALSIFIER:
    a `--wait N` whose record never APPEARS must time out in one deadline
    and exit 2 with `ERR: no rotation record for <seat> after Ns` — not the
    old silent `(no rotation record for <seat>)` return 0. Wall-time-free."""
    root = tmp_path / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / "nodes" / ".geometry" / "seats.md").write_text(SEATS_BODY)
    rot = root / "sessions" / "rotations"
    rot.mkdir(parents=True)

    clock = {"now": 1000.0}
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate.time, "monotonic", lambda: clock["now"])
    monkeypatch.setattr(rotate.time, "sleep",
                        lambda s: clock.update(now=clock["now"] + s))

    rc = rotate.main(["status", "--seat", "sanctuary-director",
                      "--record", "latest", "--wait", "3"])
    cap = capsys.readouterr()
    assert rc == 2
    assert "ERR: no rotation record for sanctuary-director after 3s" in cap.err
    assert "(no rotation record" not in cap.out


def test_wait_returns_zero_when_record_becomes_terminal_mid_wait(
        tmp_path, monkeypatch, capsys):
    """hypothesis:rotate-status-record-latest-gains-wait happy path: a
    `--wait N` call must hold until s12_self_reap lands mid-wait, then return
    0 with the now-terminal record printed."""
    import datetime
    import threading
    root = tmp_path / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / "nodes" / ".geometry" / "seats.md").write_text(SEATS_BODY)
    rot = root / "sessions" / "rotations"
    rot.mkdir(parents=True)
    stamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
    rec = rot / f"sanctuary-director.{stamp}.json"
    rec.write_text(json.dumps({"rotation": "rotate-self",
                               "seat": "sanctuary-director",
                               "result": "success"}))

    real_sleep = rotate.time.sleep

    def become_terminal():
        real_sleep(0.2)
        doc = json.loads(rec.read_text())
        doc["s12_self_reap"] = {"pane_pid": 999}
        rec.write_text(json.dumps(doc))
    threading.Thread(target=become_terminal, daemon=True).start()

    def fake_root():
        return root
    monkeypatch.setattr(rotate, "find_project_root", fake_root)
    monkeypatch.setattr(rotate.time, "sleep",
                        lambda *a, **k: real_sleep(0.05))

    rc = rotate.main(["status", "--seat", "sanctuary-director",
                      "--record", "latest", "--wait", "10"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "s12_self_reap" in out and "999" in out

# --- hypothesis:l4-a-rotation-costs-... mechanism 3: geometry freshness ------
# A rotating WORKTREE's OWN copy of `.agi/nodes/.geometry/` (config:rotations +
# config:seats) can be BEHIND the shared geometry branch (`origin/season/s2`).
# Spawning a successor there would bake a STALE rotation config into it
# SILENTLY. So rotate-self resolves WHICH tree the geometry comes from, once,
# up front: the integration tree (`locations.git_common_root`) when the
# worktree's own is behind and that tree's is current, else REFUSE BY NAME with
# the behind-count and the sync command. Falsifier: a rotate-self that spawns
# on a stale .geometry/ silently.
import subprocess as _sp  # noqa: E402


def _mgit(root, *args):
    out = _sp.run(["git", "-C", str(root), *args],
                  capture_output=True, text=True)
    assert out.returncode == 0, f"git {' '.join(args)}: {out.stderr.strip()}"
    return out.stdout.strip()


def _geometry_commit(root, rotations_body, message) -> str:
    """Write .agi/nodes/.geometry/ + config.json into `root`, commit, return the
    full commit sha. The commit only touches the geometry subtree, so a later
    `rev-list --count HEAD..ref -- .agi/nodes/.geometry/` sees exactly 1."""
    agi = root / ".agi"
    agi.mkdir(parents=True, exist_ok=True)
    (agi / "config.json").write_text("{}")
    g = agi / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    (g / "rotations.md").write_text(rotations_body)
    (g / "seats.md").write_text(SEATS_BODY)
    _mgit(root, "add", "-A")
    _mgit(root, "commit", "-q", "-m", message)
    return _mgit(root, "rev-parse", "HEAD")


def _mgit_repo(root):
    root.mkdir(parents=True, exist_ok=True)
    _mgit(root, "init", "-q")
    _mgit(root, "config", "user.email", "test@example.com")
    _mgit(root, "config", "user.name", "test")


def test_m3_stale_worktree_refuses_by_name_and_sync_cmd(
        tmp_path, monkeypatch, capsys):
    """Mechanism 3 (REFUSE): a worktree whose own .geometry/ is behind
    origin/season/s2 must refuse rotate-self BY NAME with the behind-count and
    the sync command — never spawn on the stale config silently."""
    repo = tmp_path / "repo"
    _mgit_repo(repo)
    base = _geometry_commit(repo, ROTATIONS_BODY, "geometry v1")
    tip = _geometry_commit(repo, ROTATIONS_BODY + "# v2\n", "geometry v2")
    # Simulate the shared geometry branch having moved: origin/season/s2 points
    # at the newer geometry while this worktree stays at v1 (behind by 1).
    _mgit(repo, "update-ref", "refs/remotes/origin/season/s2", tip)
    _mgit(repo, "checkout", "-q", "-b", "loop/stale", base)
    root = repo / ".agi"

    def fake_root():
        return root
    monkeypatch.setattr(rotate, "find_project_root", fake_root)
    monkeypatch.chdir(repo)
    rc = rotate.main(["rotate-self", "--name", "sanctuary-director",
                      "--dry-run", "--role", "director"])
    err = capsys.readouterr().err
    assert rc == 1
    assert "refused" in err
    assert "behind" in err
    assert "1 commit" in err
    assert "origin/season/s2" in err
    assert "git merge --no-edit origin/season/s2" in err   # merge, never rebase


def test_m3_stale_worktree_serves_integration_tree_geometry(
        tmp_path, monkeypatch, capsys):
    """Mechanism 3 (serve from {repo}): a WORKTREE behind on .geometry/ whose
    integration tree (locations.git_common_root) carries CURRENT geometry
    resolves config:rotations + config:seats FROM that tree — the resolver
    names it. The live rotate-self still never spawns on it: `_prepare_checks`
    (goal:g15.14 STEP 2, landed after this mechanism was cut) refuses ANY
    behind count first — rc 3, the merge line — so a behind seat SYNCS its
    tree rather than being served around it (director fix-up at the SL1.06
    harvest; the serve path stays as the guard on the fixture seam, where the
    checklist does not run)."""
    main = tmp_path / "main"
    _mgit_repo(main)
    base = _geometry_commit(main, ROTATIONS_BODY, "geometry v1")
    _mgit(main, "checkout", "-q", "-b", "season/s2")
    # A linked worktree forked at v1: its own geometry is behind.
    wt = tmp_path / "wt"
    _mgit(main, "worktree", "add", "-q", "-b", "loop/stale", str(wt), base)
    # Advance the INTEGRATION tree (season/s2) with newer geometry; the worktree
    # (still at v1) is now behind origin/season/s2 by exactly 1 geometry commit.
    tip = _geometry_commit(main, ROTATIONS_BODY + "# v3\n", "geometry v3")
    _mgit(main, "update-ref", "refs/remotes/origin/season/s2", tip)
    root = wt / ".agi"

    # the resolver alone: the integration tree's geometry is served, by name
    cfg_root, note = rotate._geometry_resolution_root(root)
    assert cfg_root == main / ".agi"
    assert "integration tree" in note
    assert str(main) in note
    assert "by 1 commit" in note

    # the live command: the captive checklist wins — refused by name, rc 3,
    # with the ONE clear command (merge, never rebase)
    def fake_root():
        return root
    monkeypatch.setattr(rotate, "find_project_root", fake_root)
    monkeypatch.chdir(wt)
    rc = rotate.main(["rotate-self", "--name", "sanctuary-director",
                      "--dry-run", "--role", "director"])
    cap = capsys.readouterr()
    assert rc == 3, cap.out + cap.err
    assert "behind origin/season/s2 (1)" in cap.err
    assert "git merge --no-edit origin/season/s2" in cap.err
    assert "rebase" not in cap.err


def test_m3_template_source_recorded(tmp_path):
    """Mechanism 3: the rotate-self rotation record NAMES which tree the
    template came from (`template_source`)."""
    import json as _json  # noqa: E402
    rec = tmp_path / "seat.20260101T000000Z.json"
    rotate._write_rotate_self_started(
        rec, seat="sanctuary-director", steps=["handoff"],
        gen_before=10, gen_after=11,
        template_source="integration tree /repo (worktree geometry behind "
                        "origin/season/s2 by 2 commit(s))")
    doc = _json.loads(rec.read_text(encoding="utf-8"))
    assert doc["template_source"].startswith("integration tree /repo")
    assert "by 2 commit(s)" in doc["template_source"]
    assert doc["result"] == "started"
    assert doc["steps_reached"] == ["handoff"]
