"""stream-master.relay: the narrow door's mechanism pieces (L4).

Deterministic, offline. Covers the hypothesis's PROVED BY items that need no live
transport and no model:
  (b) paid-only intake  -> ``IngestGate.accept``
  (c) hard size cap     -> ``IngestGate.cap_check`` (over-cap DROPPED, one-line log,
                           never truncated into a model)
  (d) 50-word relay     -> ``RelayValidator`` / ``relay_or_refuse`` (a 51-word draft
                           is refused)
  (a) injection guards  -> instruction screening; a relay containing any instruction
                           to an agent is refused
The Master's "own-words summarizer" is modeled as a caller-supplied short draft; the
validator's job is to refuse any draft that is over-cap, over-word, or smuggles an
instruction — the parts a summarizer cannot be trusted to self-police.

The relay contract (typing the relay, never the original text, carrying the paid event
id and platform user id) is enforced by the caller; this module validates the three
unforgeable constraints. Naming is deliberately orthogonal to the streamer-stub's real
commands (brb/back/panic/relay): refusal here is an ordinary in-process return, never a
process kill switch.
"""

from __future__ import annotations

MAX_WORDS = 50
INGESTION_CAP_TOKENS = 4000  # hard ingestion cap; config-seeded default
INGESTION_CAP_BYTES = 32_000

# Accepted event kinds per platform is config-declared; a generic shape is validated here
# so nothing branches on a platform's name.
DEFAULT_ACCEPTED_KINDS = {"boost", "cheer", "subscribe", "sub_gift", "gift_upgrade", "paid_message"}

# --- instruction screening heuristics ---------------------------------------------
# Each entry: (pattern, reason). A relay is refused if ANY pattern matches. These are a
# deliberately strict net for the fixture corpus; the corpus itself is the spec.
_INSTRUCTION_PATTERNS = [
    # role-play / identity override (classic prompt-injection opener)
    ("ignore previous", "ignore-previous"),
    ("disregard earlier", "ignore-previous"),
    ("forget your", "ignore-previous"),
    ("you are now", "role-play"),
    ("pretend you are", "role-play"),
    ("act as if", "role-play"),
    ("hidden instructions", "reveal-prompt"),
    ("system prompt", "reveal-prompt"),
    ("your instructions say", "reveal-prompt"),
    # direct imperatives toward the agent / graph
    ("run this command", "imperative"),
    ("execute", "imperative"),
    ("you must", "imperative"),
    ("please run", "imperative"),
    ("now send", "imperative"),
    ("post to the graph", "imperative"),
    ("write.py", "tool-call"),
    ("use tool", "tool-call"),
    ("call the", "tool-call"),
    ("function call", "tool-call"),
]

_CONTROL_SMUGGLE = [
    "\u200b",  # zero-width space
    "\u200c",  # zero-width non-joiner
    "\u200d",  # zero-width joiner
    "\u2060",
    "\ufeff",  # bidi / BOM
]


def _word_count(text: str) -> int:
    return len(text.split())


def _contains_control_smuggle(text: str) -> bool:
    return any(ch in text for ch in _CONTROL_SMUGGLE)


def screening_reason(relay_body: str) -> str | None:
    """Return the reason a relay draft is refused as an instruction, else None.

    The match is against the relay's own typed text. A failure is a REFUSAL — the draft
    never reaches the graph; it is neither truncated nor passed through.
    """
    low = relay_body.lower()
    for pattern, reason in _INSTRUCTION_PATTERNS:
        if pattern in low:
            return reason
    if _contains_control_smuggle(relay_body):
        return "unicode-smuggle"
    if "```" in relay_body or "[command]" in relay_body:
        return "markdown-smuggle"
    return None


class IngestGate:
    """The paid-only, capped intake side of the door."""

    def __init__(self, accepted_kinds=frozenset(DEFAULT_ACCEPTED_KINDS),
                 cap_tokens=INGESTION_CAP_TOKENS, cap_bytes=INGESTION_CAP_BYTES):
        self.accepted_kinds = frozenset(accepted_kinds)
        self.cap_tokens = cap_tokens
        self.cap_bytes = cap_bytes

    def accept(self, event_kind: str) -> bool:
        """Paid-only intake: True only for a config-accepted event kind.

        No free-text source names — an event kind is either in the accepted table or not.
        """
        return event_kind in self.accepted_kinds

    def cap_check(self, text: str) -> tuple[bool, str]:
        """Return (ok, log_line). Over-cap is DROPPED, never truncated into a model."""
        if len(text) > self.cap_bytes:
            return False, f"ingestion dropped: over byte cap {len(text)}>{self.cap_bytes}"
        # cheap token proxy: base chars/3 is a rough token count, config-seeded.
        approx_tokens = len(text) // 3
        if approx_tokens > self.cap_tokens:
            return False, f"ingestion dropped: over token cap ~{approx_tokens}>{self.cap_tokens}"
        return True, "ingestion ok"

    def intake(self, event_kind: str, text: str):
        """Full intake step: refuse (not paid) or drop (over cap) or qualify for relay."""
        if not self.accept(event_kind):
            return ("refused", "not a paid event kind", None)
        ok, log = self.cap_check(text)
        if not ok:
            return ("drop", log, None)
        return ("qualify", "ok", text)


class RelayValidator:
    """The relay side: a draft passes only if <=50 words and no instruction smuggled."""

    def __init__(self, max_words=MAX_WORDS):
        self.max_words = max_words

    def validate(self, draft_body: str) -> tuple[bool, str]:
        reason = screening_reason(draft_body)
        if reason is not None:
            return False, f"refused: relay contains instruction ({reason})"
        n = _word_count(draft_body)
        if n > self.max_words:
            return False, f"refused: relay {n} words > {self.max_words}"
        return True, f"ok: {n} words, no instruction"


def relay_or_refuse(draft_body: str, max_words=MAX_WORDS):
    """One-call convenience: (decision, message). decision in {'relay','refuse'}."""
    ok, msg = RelayValidator(max_words).validate(draft_body)
    return ("relay", msg) if ok else ("refuse", msg)
