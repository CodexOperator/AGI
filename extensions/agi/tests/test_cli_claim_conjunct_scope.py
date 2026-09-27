"""hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only -- a
hypothesis node's numbered CLAIM conjuncts come from its `testable_claim`
FIELD alone when that field carries a numbered item.

A review in a hypothesis BODY cites its own orders as (1)..(n); unioned into
the conjunct set, review prose manufactures a phantom conjunct and the parent
probe gate then demands a negative probe for a number no claim ever carried
(mur-10 DH.465 measured [1,2,3,4] for a 3-conjunct claim).
"""


def _load_cli():
    import importlib.util
    from pathlib import Path
    bin_dir = Path(__file__).resolve().parents[1] / "bin"
    spec = importlib.util.spec_from_file_location("agi_cli", bin_dir / "cli.py")
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    return cli


FIELD_NODE = (
    "---\nid: hypothesis:target\ntype: hypothesis\ntitle: Target\n"
    'testable_claim: "three real legs (1) first; (2) second; (3) third"\n'
    "---\n\n# hypothesis:target\n\n"
    "PARENT REVIEW -- the orders said: (1) cut the docstring; "
    "(2) add the clause; (3) red-first; (4) re-apply it. A 4-item to-do list, "
    "not four claim legs.\n"
)

BODY_ONLY_NODE = (
    "---\nid: hypothesis:target\ntype: hypothesis\ntitle: Target\n"
    "---\n\n# hypothesis:target\n\n## CLAIM\n\n(1) first; (2) second.\n"
)


def test_body_review_prose_does_not_manufacture_a_conjunct(tmp_path):
    """Falsifier 1: the field's own numbers win -- a review citing (1)..(4)
    adds no 4th conjunct."""
    cli = _load_cli()
    nf = tmp_path / "target.md"
    nf.write_text(FIELD_NODE)
    assert cli._claim_conjunct_numbers(nf) == [1, 2, 3]


def test_a_node_with_no_claim_field_still_reads_its_body(tmp_path):
    """Falsifier 2 (must stay green): no numbered field = no regression, the
    body remains the fallback, so an old node with only a body claim keeps its
    conjuncts."""
    cli = _load_cli()
    nf = tmp_path / "target.md"
    nf.write_text(BODY_ONLY_NODE)
    assert cli._claim_conjunct_numbers(nf) == [1, 2]


def test_a_node_with_an_unnumbered_field_falls_back_to_the_body(tmp_path):
    """Falsifier 3 (gate unchanged on every other shape): a prose field with no
    numbered item is not a claim surface, so the body still decides."""
    cli = _load_cli()
    nf = tmp_path / "target.md"
    nf.write_text(
        "---\nid: hypothesis:target\ntype: hypothesis\ntitle: Target\n"
        'testable_claim: "the gate never counts a review as a conjunct"\n'
        "---\n\n# hypothesis:target\n\n## CLAIM\n\n(1) first; (2) second.\n"
    )
    assert cli._claim_conjunct_numbers(nf) == [1, 2]


def _gate(tmp_path, n_probes):
    """Call the REAL gate (cli._parent_probe_gate) the way `done` does at
    cli.py:1554, on a temp graph whose target hypothesis is FIELD_NODE, with
    a six-field probe for each of conjuncts 1..n_probes."""
    import json
    from types import SimpleNamespace
    cli = _load_cli()
    root = tmp_path / "graph"
    (root / "nodes" / "hypothesis").mkdir(parents=True)
    (root / "nodes" / "hypothesis" / "target.md").write_text(FIELD_NODE)
    probes = [{"conjunct": n, "class": "gate", "cmd": "true", "expected": "refuse",
               "observed": "refuse", "result": "pass"} for n in range(1, n_probes + 1)]
    args = SimpleNamespace(parent="hypothesis:target",
                           node_id="experiment:kid", probes=json.dumps(probes))
    return cli._parent_probe_gate(root, {"tier": "parent"}, args, "proved")


def test_gate_through_the_wire_ignores_the_phantom_conjunct(tmp_path):
    """The WIRE test: a field-only 3-conjunct claim whose body review cites
    (1)..(4) is PASSED by the real gate on probes for 1..3 -- nobody demands
    a negative probe for the review's 4th to-do item."""
    err, active, covered = _gate(tmp_path, 3)
    assert (err, active, covered) == (None, True, [1, 2, 3])


def test_gate_still_bites_on_a_conjunct_with_no_probe(tmp_path):
    """Negative control (unchanged shape, claim 3): drop the conjunct-3 probe
    and the same gate must REFUSE by name. A pass alone would be vacuous."""
    err, active, covered = _gate(tmp_path, 2)
    assert active and "conjunct(s): 3" in err and covered == [1, 2]


def test_a_node_with_no_numbers_anywhere_yields_no_conjuncts(tmp_path):
    """Unchanged shape: the gate stays inactive (empty set) rather than
    inventing numbers."""
    cli = _load_cli()
    nf = tmp_path / "target.md"
    nf.write_text(
        "---\nid: hypothesis:target\ntype: hypothesis\ntitle: Target\n"
        'testable_claim: "no numbering here"\n---\n\n# hypothesis:target\n\nprose\n'
    )
    assert cli._claim_conjunct_numbers(nf) == []


def _done_project(tmp_path, n_probes):
    import argparse, json
    g = tmp_path / ".agi"
    for d in ("hypothesis", "experiment"):
        (g / "nodes" / d).mkdir(parents=True)
    (g / "config.json").write_text("{}")
    (g / "nodes" / "hypothesis" / "target.md").write_text(FIELD_NODE)
    (g / "nodes" / "experiment" / "backer.md").write_text(
        "---\nid: experiment:backer\ntype: experiment\ntitle: Backer\n"
        "mint_id: backermint\nparents:\n- hypothesis:target\n---\n\nbody\n")
    (g / "sessions" / "iter-001" / "a00-p").mkdir(parents=True)
    rec = g / "sessions" / "iter-001" / "a00-p" / "agent.json"
    rec.write_text(json.dumps({"id": "a00-p", "tier": "parent", "status": "running"}))
    (g / "sessions" / "iter-001" / "manifest.json").write_text(
        json.dumps({"agents": [{"id": "a00-p", "status": "running"}]}))
    probes = [{"conjunct": n, "class": "gate", "cmd": "true", "expected": "refuse",
               "observed": "refuse", "result": "pass"} for n in range(1, n_probes + 1)]
    return rec, argparse.Namespace(
        iter_n=1, agent_id="a00-p", verdict="proved", confidence=0.9,
        node_id="experiment:backer", parent="hypothesis:target", notes="",
        next_edge=None, evidence_runs=["experiment:backer"],
        no_evidence_gate=False, owns=None, no_spawn_gate=False,
        probes=json.dumps(probes))


def test_done_call_site_ignores_the_body_review_conjunct(tmp_path, monkeypatch,
                                                        capsys):
    """cmd_done CALL SITE: field (1)(2)(3) + body review citing (1)..(4)."""
    cli = _load_cli()
    rec, args = _done_project(tmp_path, 3)
    rec2, args2 = _done_project(tmp_path / "second", 2)
    monkeypatch.setattr(cli, "_find_root", lambda: rec.parents[3])
    assert cli.cmd_done(args) == 0 and '"status": "done"' in rec.read_text()
    monkeypatch.setattr(cli, "_find_root", lambda: rec2.parents[3])
    assert cli.cmd_done(args2) == 2 and "conjunct(s): 3" in capsys.readouterr().err
    assert '"status": "running"' in rec2.read_text()  # refusal wrote nothing
