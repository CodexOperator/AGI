"""T-073 tests: similarity query (embeddings/R5)."""

import warnings

from embeddings.similarity import cosine, similar_to


def _vecs() -> dict[str, list[float]]:
    return {
        "a": [1.0, 0.0, 0.0],
        "b": [0.99, 0.01, 0.0],  # very close to a
        "c": [0.0, 1.0, 0.0],   # orthogonal to a
        "d": [-1.0, 0.0, 0.0],  # opposite of a
        "e": [0.5, 0.5, 0.0],   # 45deg from a
    }


def test_top_k_descending_score() -> None:
    """R5.1: results ordered by descending score, max k items."""
    res = similar_to("a", k=3, vectors=_vecs())
    ids = [r[0] for r in res]
    scores = [r[1] for r in res]
    assert len(res) == 3
    # Descending
    assert all(scores[i] >= scores[i + 1] for i in range(len(scores) - 1))
    # b should be first (closest to a)
    assert ids[0] == "b"
    # d (opposite) should be last (lowest score)
    assert ids[-1] in {"d", "c"}  # d is -1.0, c is 0.0


def test_query_excludes_self() -> None:
    """The query node itself is not in the result list."""
    res = similar_to("a", k=10, vectors=_vecs())
    assert "a" not in [r[0] for r in res]


def test_missing_embedding_returns_empty_with_warning() -> None:
    """R5.2: no embedding for queried node → empty list + warning, NOT raise."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        res = similar_to("ghost", k=5, vectors=_vecs())
    assert res == []
    user_warnings = [item for item in w if issubclass(item.category, UserWarning)]
    assert len(user_warnings) >= 1
    assert "ghost" in str(user_warnings[0].message)


def test_scores_in_range() -> None:
    """R5.3: all scores in [-1.0, 1.0]."""
    res = similar_to("a", k=10, vectors=_vecs())
    for _, s in res:
        assert -1.0 <= s <= 1.0


def test_determinism() -> None:
    """R5.4: same args + state → identical results."""
    v = _vecs()
    a = similar_to("a", k=3, vectors=v)
    b = similar_to("a", k=3, vectors=v)
    assert a == b


def test_k_zero_returns_empty() -> None:
    res = similar_to("a", k=0, vectors=_vecs())
    assert res == []


def test_k_larger_than_available_returns_all_others() -> None:
    res = similar_to("a", k=100, vectors=_vecs())
    assert len(res) == 4  # five vectors minus self


def test_cosine_basic() -> None:
    assert cosine([1, 0], [1, 0]) == 1.0
    assert cosine([1, 0], [0, 1]) == 0.0
    assert cosine([1, 0], [-1, 0]) == -1.0


def test_cosine_zero_vector_returns_zero() -> None:
    assert cosine([0, 0], [1, 1]) == 0.0
