"""PRIME RULING 2026-09-11 — the master-sensei templates carve-out in write.py.

A g15 build order (hypothesis:write-guard-carve-out-for-master-sensei-templates):
the master-sensei seat may write config:rotations `templates` (startup +
telemetry, and the `## facts` body section) for every role EXCEPT
prime_director, directly instead of dm-and-wait, WITHOUT the written-]++;
```
write written_by gate refusing it. The rule is DATA (the schema's
`master_sensei_row` declaration), the enforcement generic in write.py
`_enforce_written_by` — the self_row pattern. A second half is load-bearing:
every resolved first_turn/after_join cmd in the written value must pass
rotate's startup producing judge, so a Sensei cannot land an entry the
executor would refuse.

Acceptance / refusal (tests a-c of the ruling):
(a) master-sensei writes director.startup.first_turn   -> accepted, written
(b) master-sensei writes prime_director anything, or brief_file/steps of any
    template, or config:seats, or any other config node -> refused BY NAME
(c) an entry judged non-None by the producing judge    -> refused NAMING the entry

Tested on a fixture root; never touches the live rotations/seats nodes.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import write  # noqa: E402
import node_writer  # noqa: E402

LIVE_SCHEMA = (Path(__file__).resolve().parents[3] / ".agi" /
                "context" / "schemas" / "[config].md")

TEMPLATES = {
    "director": {
        "brief_file": ".agi/sessions/quorum/{seat}.md",
        "steps": ["handoff", "spawn", "join", "authority", "release"],
        "telemetry": ["seed", "model"],
        "startup": {
            "first_turn": [
                {"label": "rotation-record", "cmd": "python3 extensions/agi/bin/rotate.py status --seat {seat} --record latest", "why": "x"},
            ],
            "after_join": [
                {"label": "ack", "cmd": "python3 extensions/agi/bin/rotate.py ack --seat {seat} --gen {gen} --ref {succ_ref} continue", "why": "y"},
            ],
        },
    },
    "prime_director": {
        "brief_file": "extensions/agi/briefs/prime-director-successor.md",
        "steps": ["handoff", "reap", "belam-cap"],
        "telemetry": ["seed", "model"],
        "startup": {
            "first_turn": [
                {"label": "verify", "cmd": "python3 extensions/agi/bin/commands.py run verify", "why": "z"},
            ],
            "after_join": [],
        },
    },
}


def _clone():
    import copy
    return copy.deepcopy(TEMPLATES)


def _write_rotations_node(root):
    import json
    d = root / "nodes" / ".geometry"
    d.mkdir(parents=True, exist_ok=True)
    # a node body with a ## facts section between non-facts sections
    body = (
        "# config:rotations\n\npreamble\n\n"
        "## templates\n\nkeep me\n\n"
        "## facts\n\n- F1 probe one\n- F2 probe two\n\n"
        "## steps\n\nkeep me too\n"
    )
    tpl = json.dumps(_clone())
    (d / "rotations.md").write_text(
        "---\nid: config:rotations\nmint_id: 4d469eed090b47a8bb039eb40d96f861\n"
        "type: config\nparents:\n  - hypothesis:x\n"
        "templates: " + tpl + "\n---\n\n" + body + "\n")


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    root = tmp_path
    agi = root / ".agi"
    agi.mkdir(parents=True, exist_ok=True)
    (agi / "config.json").write_text("{}")
    sd = agi / "context" / "schemas"
    sd.mkdir(parents=True)
    if LIVE_SCHEMA.exists():
        (sd / "[config].md").write_text(LIVE_SCHEMA.read_text(encoding="utf-8"))
    else:
        (sd / "[config].md").write_text(
            "---\nname: config\n"
            "written_by: [owner, prime_director]\n"
            "master_sensei_row: {actor: master-sensei, list_key: templates, "
            "fields: [startup, telemetry], deny_roles: [prime_director]}\n---\n")
    _write_rotations_node(agi)
    # a config:seats node so _resolve_seats_role resolves the actor through
    # the seat-registry path (mirrors the live graph).
    (agi / "nodes/.geometry/seats.md").write_text(
        "---\nid: config:seats\nmint_id: 3e88873e3c204c5088f6ab81322a26de\n"
        "type: config\nseats:\n"
        "  - {name: master-sensei, role: director}\n"
        # A longer-prefix collision seat: an actor string starting with
        # `master-sensei-` that resolves (longest-prefix) to THIS seat, not the
        # real master-sensei — the impostor the seat-keyed identity must refuse.
        "  - {name: master-sensei-impostor, role: director}\n"
        "---\n# seats\n\nfixture\n")
    return agi  # the graph root (.agi), which is what find_project_root returns


def _templates_edit(new_templates):
    """A whole-`templates` set, the write shape (self_row pattern)."""
    import json
    e = write.Edit("config:rotations")
    write.verb_set(e, "templates", json.dumps(new_templates))
    return e


def test_master_sensei_writes_director_startup_accepted(project):
    """ACCEPTANCE (a): master-sensei changes director.startup.first_turn to a
    judge-clean entry -> admitted, written."""
    new = _clone()
    new["director"]["startup"]["first_turn"].append(
        {"label": "inbox", "cmd": "python3 extensions/agi/bin/send.py read {seat}", "why": "n"})
    res = write.submit(project, _templates_edit(new), actor="master-sensei-7a")
    assert res.status == node_writer.UPDATED
    text = (project / "nodes/.geometry/rotations.md").read_text()
    assert "inbox" in text


def test_master_sensei_writes_director_telemetry_accepted(project):
    new = _clone()
    new["director"]["telemetry"] = ["seed", "model", "ack"]
    res = write.submit(project, _templates_edit(new), actor="master-sensei-7a")
    assert res.status == node_writer.UPDATED


def test_master_sensei_refused_touching_prime_director(project):
    """REFUSAL (b): master-sensei touches the prime_director template at all
    -> refused BY NAME (prime/owner-only)."""
    new = _clone()
    new["prime_director"]["telemetry"].append("window")
    with pytest.raises(write.EditError) as ei:
        write.submit(project, _templates_edit(new), actor="master-sensei-7a")
    msg = str(ei.value)
    assert "prime_director" in msg
    assert "prime/owner-only" in msg


def test_master_sensei_refused_touching_brief_file(project):
    """REFUSAL (b): master-sensei changes brief_file of ANY template (here on
    its own role's template) -> refused BY NAME."""
    new = _clone()
    new["director"]["brief_file"] = "hacked.md"
    with pytest.raises(write.EditError) as ei:
        write.submit(project, _templates_edit(new), actor="master-sensei-7a")
    msg = str(ei.value)
    assert "brief_file" in msg
    assert "prime/owner-only" in msg


def test_master_sensei_refused_touching_steps(project):
    """REFUSAL (b): master-sensei changes steps of any template -> refused."""
    new = _clone()
    new["director"]["steps"] = ["evil"]
    with pytest.raises(write.EditError) as ei:
        write.submit(project, _templates_edit(new), actor="master-sensei-7a")
    assert "steps" in str(ei.value)


def test_master_sensei_refused_other_config_node(project):
    """REFUSAL (b): master-sensei writing config:seats is NOT granted by the
    templates carve-out — a prime-only field there refuses by the self_row
    gate (config:seats stays own-row-fields-only for every seated role)."""
    import json
    e = write.Edit("config:seats")
    write.verb_set(e, "seats", json.dumps(
        [{"name": "master-sensei", "role": "director"},
         {"name": "other", "role": "director", "session_ref": "X"}]))
    with pytest.raises(write.EditError) as ei:
        write.submit(project, e, actor="master-sensei-7a")
    msg = str(ei.value)
    assert "seats" in msg or "row" in msg


def test_master_sensei_refused_judge_dirty_entry(project):
    """REFUSAL (c): a startup entry the producing judge refuses -> refused
    NAMING the entry."""
    new = _clone()
    new["director"]["startup"]["after_join"].append(
        {"label": "rogue", "cmd": "echo X", "why": "oops"})
    with pytest.raises(write.EditError) as ei:
        write.submit(project, _templates_edit(new), actor="master-sensei-7a")
    msg = str(ei.value)
    assert "rogue" in msg        # names the entry
    assert "judge" in msg        # names the judge


def test_owner_still_writes_whole_templates(project):
    """The carve-out must not shrink OWNER/PRIME: they write anything."""
    new = _clone()
    new["prime_director"]["brief_file"] = "prime-only.md"
    new["director"]["steps"] = ["anything"]
    res = write.submit(project, _templates_edit(new), actor="owner")
    assert res.status == node_writer.UPDATED


def test_non_sensei_seated_director_still_refused(project):
    """A different seated role (e.g. a helper) cannot write templates -> the
    written_by gate still refuses; the carve-out is master-sensei ONLY."""
    new = _clone()
    new["director"]["telemetry"].append("extra")
    with pytest.raises(write.EditError):
        write.submit(project, _templates_edit(new), actor="sanctuary-helper-2c")


BODY_TEMPLATE = (
    "# config:rotations\n\n"
    "preamble\n\n"
    "## templates\n\nkeep me\n\n"
    "## facts\n\n- F1 probe one\n- F2 probe two\n\n"
    "## steps\n\nkeep me too\n"
)


def test_master_sensei_facts_body_edit_accepted(project):
    """The facts body section is the third writable region: a master-sensei
    body edit confined to `## facts` is accepted."""
    new_body = BODY_TEMPLATE.replace("- F1 probe one\n- F2 probe two",
                                     "- F1 probe one\n- F2 probe two\n- F3 probe three")
    src = project / "facts.md"
    src.write_text(new_body)
    e = write.Edit("config:rotations")
    write.verb_replace(e, "body", "1:", str(src))
    res = write.submit(project, e, actor="master-sensei-7a")
    assert res.status == node_writer.UPDATED
    assert "F3 probe three" in (project / "nodes/.geometry/rotations.md").read_text()


def test_master_sensei_body_edit_outside_facts_refused(project):
    """Changing a non-facts body section (here `## steps`) is refused."""
    new_body = BODY_TEMPLATE.replace("## steps\n\nkeep me too",
                                     "## steps\n\ntampered")
    src = project / "steps.md"
    src.write_text(new_body)
    e = write.Edit("config:rotations")
    write.verb_replace(e, "body", "1:", str(src))
    with pytest.raises(write.EditError) as ei:
        write.submit(project, e, actor="master-sensei-7a")
    msg = str(ei.value)
    assert "facts" in msg


def test_master_sensei_refused_non_dict_template_value(project):
    """CLAIM (1): a non-dict new template value (here director = 'garbage', a
    str) is REFUSED BY NAME — it must not silently drop brief_file + steps
    (hypothesis:l4-the-carve-out-refuses-a-non-dict-template-and-keys-on-the-
    resolved-seat, falsifier: 4 probes)."""
    new = _clone()
    new["director"] = "garbage"  # a str, not a dict — the silent-drop shape
    with pytest.raises(write.EditError) as ei:
        write.submit(project, _templates_edit(new), actor="master-sensei-7a")
    msg = str(ei.value)
    assert "director" in msg        # names the role
    assert "must be a dict" in msg  # names the shape
    assert "str" in msg             # names what it actually got
    # the drop must not land: nothing was written
    assert "garbage" not in (project / "nodes/.geometry/rotations.md").read_text()


def test_master_sensei_refused_non_dict_template_list_value(project):
    """CLAIM (1), list shape: templates.director = [] is refused by name."""
    new = _clone()
    new["director"] = []
    with pytest.raises(write.EditError) as ei:
        write.submit(project, _templates_edit(new), actor="master-sensei-7a")
    msg = str(ei.value)
    assert "director" in msg
    assert "must be a dict" in msg
    assert "list" in msg


def test_master_sensei_refused_config_seats_body_edit(project):
    """CLAIM (2): the facts-body gate applies only to the node that carries the
    declaration's list_key (`templates`). A body-only master-sensei edit to a
    config:seats node — even confined to a `## facts` section — is REFUSED,
    not granted by the templates carve-out. Under the pre-fix code this probe
    was ADMITTED (defect (2)); the repaired gate falls it through to the
    written_by/self_row refusal."""
    new_body = (
        "# seats\n\ncameo\n\n## facts\n\n- F probe one\n"
    )
    src = project / "fakts.md"
    src.write_text(new_body)
    e = write.Edit("config:seats")
    write.verb_replace(e, "body", "1:", str(src))
    with pytest.raises(write.EditError) as ei:
        write.submit(project, e, actor="master-sensei-7a")
    msg = str(ei.value)
    assert "seats" in msg or "templates" in msg or "facts" in msg


def test_master_sensei_impostor_resolves_to_other_seat_refused(project):
    """CLAIM (3): the master-sensei identity is the RESOLVED SEAT name only
    (`_resolve_seat(root, actor) == the declared actor`), never the free-text
    `--actor` string. `master-sensei-impostor-9f` resolves (longest-prefix) to
    the `master-sensei-impostor` seat, NOT the master-sensei seat, so a
    templates write by it is REFUSED. Under the pre-fix code its string
    `startswith('master-sensei-')` admitted it to the carve-out (defect (3))."""
    new = _clone()
    new["director"]["telemetry"].append("impostor")
    with pytest.raises(write.EditError) as ei:
        write.submit(project, _templates_edit(new),
                     actor="master-sensei-impostor-9f")
    msg = str(ei.value)
    # refused on SOME ground — the impostor is never the master-sensei
    assert "seats" in msg or "templates" in msg or "written_by" in msg


def test_verb_examples_parse_as_their_arity(project):
    """CLAIM (4): every VERB_EXAMPLES entry PARSES as its verb's arity via the
    shared `parse_script` — so the grammar the -h epilog teaches is real, not
    just hand-checked. The repaired `set` example is `set key value` (arity 2);
    the pre-fix `set k=v` parsed as one token and would be refused."""
    for name, example in write.VERB_EXAMPLES.items():
        # parse_script takes the verb line exactly as the CLI's `--script`
        # positional does (the node-id is a separate argument), which is the
        # same form the epilog examples are written in.
        parsed = write.parse_script(example)
        assert len(parsed) == 1, f"{name}: {example} did not parse to one verb"
        got_name, got_args = parsed[0]
        assert got_name == name, f"example for {name!r} parsed as {got_name!r}"
        assert len(got_args) == write.ARITY[name], (
            f"{name}: example {example!r} parses to {len(got_args)} args, "
            f"arity is {write.ARITY[name]}")


def test_set_epilog_example_is_two_arg(project):
    """CLAIM (4), the named regression: the epilog `set` example is `set key
    value` (TWO arguments), never `set k=v` (one token, refused)."""
    assert write.VERB_EXAMPLES["set"] == "set key value"
    # and it genuinely parses to two args (the grammar the epilog teaches)
    parsed = write.parse_script("set key value")
    assert len(parsed[0][1]) == 2
