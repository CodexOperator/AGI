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
