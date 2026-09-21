"""T-005 tests: identity scheme (graph-core/R3).

Plus goal:g2.5's fixed-width hierarchical addresses, added alongside the
original ``<type>:<slug>`` scheme without touching it — see the tests below
``# --- goal:g2.5 ---``.
"""

import json
import shutil
import subprocess
import warnings

import pytest

from graph_core.identity import (
    ALPHABET,
    IdRegistry,
    derive_slug,
    is_valid_address,
    is_valid_mint_id,
    mint_address,
    mint_id,
    mint_permanent_id,
    plan_reid,
    supernode,
)


def test_slug_kebab_case_lowercase() -> None:
    """R3.1: slug is kebab-case, lowercase, punctuation stripped."""
    s = derive_slug("Capillary DAG Memory!")
    assert s == "capillary-dag-memory"


def test_slug_caps_at_max_tokens() -> None:
    """R3.1: slug capped at 5 tokens by default."""
    s = derive_slug("one two three four five six seven")
    assert s == "one-two-three-four-five"


def test_mint_id_format() -> None:
    """R3.1: id format is <prefix>:<slug>."""
    out = mint_id("hyp", "LRU saturates warm load")
    assert out == "hyp:lru-saturates-warm-load"


def test_collision_yields_suffix() -> None:
    """R3.2: second mint of identical source in same registry yields :2."""
    reg = IdRegistry()
    a = reg.mint("hyp", "LRU saturates warm load")
    b = reg.mint("hyp", "LRU saturates warm load")
    c = reg.mint("hyp", "LRU saturates warm load")
    assert a == "hyp:lru-saturates-warm-load"
    assert b == "hyp:lru-saturates-warm-load:2"
    assert c == "hyp:lru-saturates-warm-load:3"


def test_long_id_emits_user_warning() -> None:
    """R3.3: ids over 40 chars warn but are still returned."""
    # Use long-word tokens so the 5-token-capped slug still exceeds 40 chars.
    long_text = "extraordinarily verbose hypothesization regarding complications"
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        out = mint_id("hyp", long_text)
        assert any(issubclass(item.category, UserWarning) for item in w)
        assert len(out) > 40


def test_stability_across_registries() -> None:
    """R3.4: same source text yields the same id when registries don't collide."""
    reg1 = IdRegistry()
    reg2 = IdRegistry()
    sources = ["alpha beta", "gamma delta", "epsilon zeta"]
    seq1 = [reg1.mint("idea", s) for s in sorted(sources)]
    seq2 = [reg2.mint("idea", s) for s in sorted(sources)]
    assert seq1 == seq2


def test_empty_source_yields_untitled() -> None:
    """Edge case: empty/whitespace source yields a stable fallback."""
    assert derive_slug("") == "untitled"
    assert derive_slug("   ") == "untitled"


# --- goal:g2.5 — fixed-width hierarchical addresses ---


def test_alphabet_is_36_lowercase_alphanumeric() -> None:
    """ALPHABET is 0-9a-z, 36 distinct chars, no uppercase (case-insensitive filesystems)."""
    assert ALPHABET == "0123456789abcdefghijklmnopqrstuvwxyz"
    assert len(ALPHABET) == 36
    assert len(set(ALPHABET)) == 36
    assert ALPHABET == ALPHABET.lower()


def test_mint_address_known_seed_is_a_constant() -> None:
    """Determinism across processes: a fixed seed always maps to this exact address.

    If this ever fails after a legitimate code change, it means the hash
    function (or its parameters) changed — which is precisely the kind of
    change that would silently reassign every address in a live corpus, so
    this test exists to force that change to be noticed and deliberate.
    """
    assert mint_address("graph-core-known-seed", set()) == "bgdefrb"


def test_mint_address_is_width_and_alphabet_bound() -> None:
    addr = mint_address("any-seed", set())
    assert len(addr) == 7
    assert all(c in ALPHABET for c in addr)


def test_mint_address_stable_under_insertion() -> None:
    """Minting N addresses then N+1 leaves the first N unchanged (goal:g2.5).

    This is the property that rules out anything derived from sort position
    or corpus size: an address depends only on its own seed, so appending a
    new seed cannot perturb any address already minted.
    """
    seeds = [f"node-{i}" for i in range(200)]
    taken: set[str] = set()
    first_n: dict[str, str] = {}
    for seed in seeds:
        addr = mint_address(seed, taken)
        taken.add(addr)
        first_n[seed] = addr
    assert len(set(first_n.values())) == len(seeds)  # sanity: no collisions at this scale

    # Mint one more (N+1) and recheck every earlier seed against the grown `taken`.
    extra_addr = mint_address("node-200", taken)
    taken.add(extra_addr)
    for seed, addr in first_n.items():
        assert mint_address(seed, taken - {addr}) == addr


def test_mint_address_collision_probe_is_deterministic() -> None:
    """Same (seed, taken) always yields the same probed address."""
    taken = {"aaaaaaa"}
    a = mint_address("seed-that-would-collide", taken)
    b = mint_address("seed-that-would-collide", set(taken))
    assert a == b


def test_plan_reid_collision_resolution_is_order_independent(tmp_path) -> None:
    """Force real base-hash collisions (width=2, 1296 slots) and vary input order.

    200 fixed seeds at width=2 are known (checked directly against the private
    hashing helpers before writing this test) to produce 20 base-hash
    collision groups — real probing, not a hypothetical. width=2 keeps the
    slot space (1296) far above the seed count (200) so probing can never run
    out of room; a width=1 corpus this size would exhaust all 36 slots and
    ``mint_address`` would loop forever, which is a real hazard of this
    design worth flagging rather than triggering.

    plan_reid imposes its own canonical (sorted) processing order internally,
    so the resulting {old_id: new_id} mapping must be identical regardless of
    what order the caller happened to hand nodes in — this is the batch-level
    guarantee mint_address's own docstring says a single-seed call cannot make
    on its own.
    """
    seeds = [f"collide-{i}" for i in range(200)]
    forward = [{"id": s} for s in seeds]
    shuffled = [{"id": s} for s in reversed(seeds)]

    res_forward = plan_reid(forward, width=2, out_path=tmp_path / "forward.json")
    res_shuffled = plan_reid(shuffled, width=2, out_path=tmp_path / "shuffled.json")

    assert res_forward["mapping"] == res_shuffled["mapping"]
    # Confirm this actually exercised collision probing, not just the common case.
    assert len(set(res_forward["mapping"].values())) == len(seeds)


def test_mint_address_alphabet_only_and_git_ref_safe() -> None:
    """Every minted address is alphabet-only and a valid one-level git ref component."""
    taken: set[str] = set()
    addrs = []
    for i in range(25):
        a = mint_address(f"ref-safety-{i}", taken)
        taken.add(a)
        addrs.append(a)
        assert is_valid_address(a)

    if shutil.which("git") is None:
        pytest.skip("git not available")
    for a in addrs:
        proc = subprocess.run(
            ["git", "check-ref-format", "--allow-onelevel", f"refs/grid/node/{a}"],
            capture_output=True,
        )
        assert proc.returncode == 0, f"address {a!r} is not a valid git ref component"


def test_is_valid_address_rejects_wrong_width_and_bad_chars() -> None:
    assert is_valid_address("abc1234")
    assert not is_valid_address("abc123")  # too short
    assert not is_valid_address("abc12345")  # too long
    assert not is_valid_address("ABC1234")  # uppercase not in ALPHABET
    assert not is_valid_address("abc-234")  # punctuation


def test_supernode_truncation_round_trips() -> None:
    addr = mint_address("supernode-roundtrip-seed", set())
    assert supernode(addr, 7) == addr
    assert supernode(addr, 6) == addr[:6]
    assert supernode(addr, 5) == addr[:5]
    # Truncating the 6-char supernode to 5 matches truncating the address directly.
    assert supernode(supernode(addr, 6), 5) == supernode(addr, 5)


def test_plan_reid_is_idempotent(tmp_path) -> None:
    nodes = [{"id": f"idem-{i}"} for i in range(30)]
    res1 = plan_reid(nodes, out_path=tmp_path / "run1.json")
    res2 = plan_reid(nodes, out_path=tmp_path / "run2.json")
    assert res1["mapping"] == res2["mapping"]
    assert res1["supernode_groups"] == res2["supernode_groups"]
    assert res1["max_group_size"] == res2["max_group_size"]


def test_plan_reid_writes_no_input_and_reports_references(tmp_path) -> None:
    """plan_reid is a planner: it writes only its own output file, never a node."""
    nodes = [
        {"id": "a"},
        {"id": "b", "parents": ["a"]},
        {"id": "c", "supersedes": "a", "evidence_runs": ["b", "does-not-exist"]},
    ]
    out = tmp_path / "plan.json"
    res = plan_reid(nodes, out_path=out)

    assert set(res["mapping"].keys()) == {"a", "b", "c"}
    assert len(set(res["mapping"].values())) == 3  # all distinct
    assert res["references"] == {"parents": 1, "supersedes": 1, "evidence_runs": 1, "total": 3}
    assert out.exists()
    written = json.loads(out.read_text())
    assert written["mapping"] == res["mapping"]


def test_plan_reid_supernode_stats_match_manual_grouping(tmp_path) -> None:
    nodes = [{"id": f"group-check-{i}"} for i in range(80)]
    res = plan_reid(nodes, out_path=tmp_path / "plan.json")

    groups: dict[str, int] = {}
    for new_id in res["mapping"].values():
        groups[new_id[:6]] = groups.get(new_id[:6], 0) + 1
    assert res["supernode_groups"] == len(groups)
    assert res["max_group_size"] == max(groups.values())
    assert res["groups_over_capacity"] == sum(1 for v in groups.values() if v > 36)


def test_plan_reid_rejects_duplicate_ids() -> None:
    with pytest.raises(ValueError):
        plan_reid([{"id": "dup"}, {"id": "dup"}])


# --- goal:g2.5 "Tension resolved 2026-08-25" — mint_permanent_id -----------


def test_mint_permanent_id_format() -> None:
    """32 lowercase hex chars — the format grid.py's sanitize() needs to be
    the identity function on (no colon, nothing outside [0-9a-f])."""
    mid = mint_permanent_id()
    assert len(mid) == 32
    assert mid == mid.lower()
    assert all(c in "0123456789abcdef" for c in mid)
    assert is_valid_mint_id(mid)


def test_mint_permanent_id_is_fresh_every_call_not_derived() -> None:
    """Never derived from content/id — two independent calls must not
    collide by construction, and repeated calls must not repeat a value
    over a reasonably large sample (would indicate accidental determinism)."""
    ids = {mint_permanent_id() for _ in range(500)}
    assert len(ids) == 500


def test_mint_permanent_id_takes_no_seed_and_is_non_deterministic() -> None:
    """Unlike mint_address, this is a pure function of NOTHING — calling it
    twice must not yield the same id, which is exactly what rules out
    deriving it from a node's content or existing id."""
    assert mint_permanent_id() != mint_permanent_id()


def test_is_valid_mint_id_rejects_wrong_shape() -> None:
    assert is_valid_mint_id(mint_permanent_id())
    assert not is_valid_mint_id("too-short")
    assert not is_valid_mint_id("A" * 32)  # uppercase not allowed
    assert not is_valid_mint_id("g" * 32)  # 'g' outside hex alphabet
    assert not is_valid_mint_id("0" * 31)  # one char short
    assert not is_valid_mint_id("0" * 33)  # one char long
    assert not is_valid_mint_id("level3:bin-grid")  # a node id, not a mint id


def test_mint_permanent_id_is_a_valid_git_ref_component() -> None:
    """The property the whole format choice rests on: sanitize() must be the
    identity function on this output, so grid.py needs no escaping layer."""
    if shutil.which("git") is None:
        pytest.skip("git not available")
    for _ in range(10):
        mid = mint_permanent_id()
        proc = subprocess.run(
            ["git", "check-ref-format", "--allow-onelevel", f"refs/grid/node/{mid}"],
            capture_output=True,
        )
        assert proc.returncode == 0, f"mint id {mid!r} is not a valid git ref component"
