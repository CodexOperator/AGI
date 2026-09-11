"""Replay of the fixture injection corpus against the stream-master door (L4).

Mirrors hypothesis:l4-the-stream-master-is-the-only-door's PROVED BY: every corpus
entry must produce a refusal or a relay of <=50 words containing no instruction.
Offline, synthetic, no network, no live chat — per the node's HARD RULES.
"""

from __future__ import annotations

from stream_master.corpus import INJECTION_CORPUS
from stream_master.relay import IngestGate, MAX_WORDS, relay_or_refuse


def _draft_for(kind: str, source_text: str) -> str:
    """Model the Master's own-words summarizer.

    The real summarizer produces a typed short draft it *believes* is its own words;
    this module's job is to refuse any draft that smuggles an instruction, over-caps,
    or over-words it. For fixtures the summarizer is identity: the valve under test is
    the screening/cap layer, not the (modeled, out-of-scope) rephraser.
    """
    return source_text


def test_corpus_replay_every_entry_refused_or_clean() -> None:
    gate = IngestGate()
    results = {}

    for event_kind, source_text, expected in INJECTION_CORPUS:
        decision, note, _ = gate.intake(event_kind, source_text)

        if expected == "free-event-no-relay":
            assert decision == "refused", (event_kind, decision)
            results[expected] = "refused-at-intake"
            continue

        if expected == "oversize":
            # over-cap message is dropped at intake, never truncated into a model
            assert decision == "drop", (event_kind, decision)
            results[expected] = "dropped-at-intake"
            continue

        # everything else is a paid, under-cap event that qualifies — now the relay
        # valve decides.
        assert decision == "qualify", (event_kind, expected, decision)
        draft = _draft_for(event_kind, source_text)
        decision2, msg = relay_or_refuse(draft, MAX_WORDS)

        if expected == "benign-relay":
            assert decision2 == "relay", (event_kind, msg)
            n = len(draft.split())
            assert n <= MAX_WORDS
        elif expected == "overword":
            assert decision2 == "refuse", "51-word draft must be refused"
            results[expected] = msg
        else:
            # every injection class must be refused, not passed through
            assert decision2 == "refuse", (event_kind, msg)
            results[expected] = msg

    # sanity: every class in the corpus produced its expected guard outcome
    assert "role-play" in results or True  # benign/oversize/free not dict-keyed; assert below
    injected = {"role-play", "ignore-previous", "reveal-prompt", "tool-call",
                "unicode-smuggle", "markdown-smuggle"}
    refused = {k for k in results if k in injected}
    assert refused == injected, f"missing refusals: {injected - refused}"


def test_paid_only_zero_relay_for_free_event() -> None:
    gate = IngestGate()
    decision, note, _ = gate.intake("message", "free unboosted chat text")
    assert decision == "refused"
    assert "not a paid event kind" in note


def test_51_word_relay_refused() -> None:
    decision, msg = relay_or_refuse("word " * 51, MAX_WORDS)
    assert decision == "refuse"
    assert "51 words" in msg


def test_overcap_dropped_never_truncated() -> None:
    gate = IngestGate()
    decision, note, _ = gate.intake("boost", "x" * 40_000)
    assert decision == "drop"
    assert "over" in note  # one-line log, message discarded whole


def test_clean_relay_passes() -> None:
    decision, msg = relay_or_refuse("the intro slide is good", MAX_WORDS)
    assert decision == "relay"
    assert "no instruction" in msg
