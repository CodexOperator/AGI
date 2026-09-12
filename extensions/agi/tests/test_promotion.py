"""RUNG 4 SLICE 4 -- seatsig.countersign: tier EARNED by countersigned verdicts.

hypothesis:l4-an-untrusted-lane-earns-tier-by-signed-verdicts, SLICE 4
(conjunct 3, the last unbuilt piece). Proves on FIXTURE graphs only (never
the live tree, never a real key, never a real ladder cell / row write outside
the tmp root): the promotion threshold is DECLARED on the ladder node and read
through the engine reader (never hardcoded); a trusted reviewer's
countersignature of the counted post's verdict record is what is counted, and
only when it verifies against the reviewer's row pubkey AND the reviewer's
tier is not 'untrusted' AND the reviewer is not the counted post; the row is
promoted off 'untrusted' only when the count crosses the threshold AND the
acting post is neither the promoted post nor itself untrusted; every refusal
names the count and the number needed.
"""

from __future__ import annotations

import json

import geometry_config
import seatsig
from seatsig import countersign

CH = "ed25519"


def _posts_md(rows, key="posts"):
    body = "\n".join(f"  - {r!r}" for r in rows)
    return (
        f"---\nid: config:{key}\nmint_id: 3e88873e3c204c5088f6ab81322a26de\n"
        f"type: config\nparents:\n  - goal:g17\n{key}:\n{body}\n"
        "---\n\n# config\n\nfixture body\n"
    )


def _ladder_md(threshold):
    return (
        f"---\nid: ladder:ladder\nmint_id: 5f6bbbfff8634f36ba0ba67defa52a66\n"
        f"type: ladder\nparents:\n  - goal:g12.3\n"
        f"{countersign.PROMOTION_THRESHOLD_CELL}: {threshold}\n---\n\n"
        "fixture ladder body\n"
    )


def _keypair():
    scheme = seatsig.get(CH)
    priv, pub = scheme.keygen()
    return priv, pub.hex()


def _project(tmp_path, threshold=1, bobby_untrusted=True):
    """A fixture project: a prime (belam) that performs the config write, a
    trusted reviewer (alice), a second reviewer (bobby -- UNTRUSTED when
    asked, the negative control), and the untrusted post to promote
    (newcomer). The ladder node declares the promotion threshold."""
    _belam_priv, belam_pub = _keypair()
    _alice_priv, alice_pub = _keypair()
    _bobby_priv, bobby_pub = _keypair()
    _new_priv, new_pub = _keypair()
    root = tmp_path / "proj"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(
        json.dumps({"metric_primary": "outcome_coverage"}))
    d = root / ".agi" / "nodes" / ".geometry"
    d.mkdir(parents=True, exist_ok=True)
    rows = [
        {"name": "belam", "role": "prime_director", "tier": 3,
         "pubkey": belam_pub},
        {"name": "alice", "role": "director", "tier": 1, "pubkey": alice_pub},
        {"name": "bobby", "role": "director", "tier": 1, "pubkey": bobby_pub},
        {"name": "newcomer", "role": "kid", "tier": "untrusted",
         "pubkey": new_pub},
    ]
    if bobby_untrusted:
        rows[2]["tier"] = "untrusted"
    (d / "posts.md").write_text(_posts_md(rows))
    (d / "ladder.md").write_text(_ladder_md(threshold))
    return root, {
        "belam": _belam_priv, "alice": _alice_priv,
        "bobby": _bobby_priv, "newcomer": _new_priv,
        "pub": {"belam": belam_pub, "alice": alice_pub,
                "bobby": bobby_pub, "newcomer": new_pub},
    }


def _sig(reviewer, priv, node, verdict, owner):
    """A reviewer's OWN countersignature over one verdict record's canonical
    bytes -- produced disjointly with the reviewer's key, never the writer's."""
    scheme = seatsig.get(CH)
    canon = bytes.fromhex(
        countersign.verdict_canonical_hex(node, verdict, owner))
    return f"{reviewer}:{CH}:{scheme.sign(priv, canon).hex()}"


def _load(root):
    return geometry_config.load_rows(countersign.graph_root(root))


def test_promotion_threshold_met(tmp_path):
    """Threshold-met promotes: one trusted reviewer's countersignature of the
    newcomer's verdict record clears a declared threshold of 1 and the row's
    tier leaves 'untrusted'. The actor (belam) is a different, seated post."""
    root, keys = _project(tmp_path, threshold=1)
    node = "experiment:fixture-1"
    cell = countersign.verdict_cell(
        node, "proved", "newcomer",
        [_sig("alice", keys["alice"], node, "proved", "newcomer")])
    row = countersign.promote(root, "newcomer", [cell], actor="belam")
    assert row is not None, "threshold met with a trusted reviewer -> promotes"
    assert str(row["tier"]) != "untrusted"
    assert row["promoted_by"] == "belam"
    got = next(r for r in _load(root) if r["name"] == "newcomer")
    assert str(got["tier"]) != "untrusted"


def test_one_short_refuses_by_name_with_both_numbers(tmp_path, capsys):
    """One short of the threshold refuses BY NAME with the count and the
    number needed. Same single valid verdict, threshold 2."""
    root, keys = _project(tmp_path, threshold=2)
    node = "experiment:fixture-2"
    cell = countersign.verdict_cell(
        node, "proved", "newcomer",
        [_sig("alice", keys["alice"], node, "proved", "newcomer")])
    assert countersign.promote(root, "newcomer", [cell], actor="belam") is None
    err = capsys.readouterr().err
    assert "needs 2" in err and "got 1" in err, err


def test_self_promotion_refused(tmp_path, capsys):
    """A post cannot promote its own row (never a self-edit), even with a
    valid countersigned verdict -- the actor IS the promoted post."""
    root, keys = _project(tmp_path, threshold=1)
    node = "experiment:fixture-3"
    cell = countersign.verdict_cell(
        node, "proved", "newcomer",
        [_sig("alice", keys["alice"], node, "proved", "newcomer")])
    assert countersign.promote(root, "newcomer", [cell],
                               actor="newcomer") is None
    err = capsys.readouterr().err
    assert "cannot promote its own row" in err, err


def test_untrusted_countersigner_not_counted(tmp_path, capsys):
    """An untrusted reviewer's countersignature does NOT count: threshold 1
    with only bobby (untrusted) signing yields count 0 and a refusal that
    names the count."""
    root, keys = _project(tmp_path, threshold=1)
    node = "experiment:fixture-4"
    cell = countersign.verdict_cell(
        node, "proved", "newcomer",
        [_sig("bobby", keys["bobby"], node, "proved", "newcomer")])
    assert countersign.promote(root, "newcomer", [cell], actor="belam") is None
    err = capsys.readouterr().err
    assert "got 0" in err, err


def test_reviewer_double_signature_counts_once(tmp_path, capsys):
    """A counter-signer counted twice does not count twice: ONE verdict record
    carrying TWO identical signatures from the same trusted reviewer is still
    ONE counted verdict, so threshold 2 refuses with got 1."""
    root, keys = _project(tmp_path, threshold=2)
    node = "experiment:fixture-5"
    one = _sig("alice", keys["alice"], node, "proved", "newcomer")
    cell = countersign.verdict_cell(
        node, "proved", "newcomer", [one, one])
    assert countersign.promote(root, "newcomer", [cell], actor="belam") is None
    err = capsys.readouterr().err
    assert "got 1" in err, err


def test_duplicate_verdict_record_counts_once(tmp_path, capsys):
    """The same verdict cell handed twice counts once (the record is the
    unit, not the occurrence). Threshold 2 refuses with got 1."""
    root, keys = _project(tmp_path, threshold=2)
    node = "experiment:fixture-6"
    cell = countersign.verdict_cell(
        node, "proved", "newcomer",
        [_sig("alice", keys["alice"], node, "proved", "newcomer")])
    assert countersign.promote(root, "newcomer", [cell, cell],
                               actor="belam") is None
    err = capsys.readouterr().err
    assert "got 1" in err, err


def test_owner_cannot_countersign_own_verdict(tmp_path, capsys):
    """The reviewer cannot countersign its own work: a verdict of newcomer
    'countersigned' by newcomer itself does not count (the counted verdict is
    never the post's own). Threshold 1 refuses with got 0."""
    root, keys = _project(tmp_path, threshold=1)
    node = "experiment:fixture-8"
    cell = countersign.verdict_cell(
        node, "proved", "newcomer",
        [_sig("newcomer", keys["newcomer"], node, "proved", "newcomer")])
    assert countersign.promote(root, "newcomer", [cell], actor="belam") is None
    err = capsys.readouterr().err
    assert "got 0" in err, err


def test_different_canonical_bytes_does_not_verify(tmp_path, capsys):
    """A countersignature over DIFFERENT canonical bytes does not verify: the
    reviewer signs a bare different message, so re-deriving the canonical from
    the cell's OWN fields makes the signature read FORGED and nothing counts."""
    root, keys = _project(tmp_path, threshold=1)
    scheme = seatsig.get(CH)
    forged = scheme.sign(keys["alice"], b"a different verdict entirely").hex()
    node = "experiment:fixture-7"
    cell = countersign.verdict_cell(
        node, "proved", "newcomer", [f"alice:{CH}:{forged}"])
    assert countersign.promote(root, "newcomer", [cell], actor="belam") is None
    err = capsys.readouterr().err
    assert "got 0" in err, err