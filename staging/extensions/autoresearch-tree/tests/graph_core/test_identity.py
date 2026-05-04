"""T-005 tests: identity scheme (graph-core/R3)."""

import warnings

import pytest

from graph_core.identity import IdRegistry, derive_slug, mint_id


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
