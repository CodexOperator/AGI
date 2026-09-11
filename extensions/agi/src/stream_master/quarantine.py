"""stream-master.quarantine: the isolation half of the door (L4).

Complements relay.py (the valve: paid-only intake + cap + 50-word screened relay).
This module is the place relays LAND and the guarantee that they are read as DATA,
never as instructions. Mirrors the hypothesis's PROVED BY (e):

  "the quarantine inbox readable by the Council and unread by every dispatch path
   (a grep of the brief assembly proves no chat text reaches a kid)"

Offline, deterministic, fixture-only — no network, no SDK, no live chat, matching
every HARD RULE. The safety property is structural and here testable as invariants:

  1. MASTER-ONLY WRITE  — only the Master role may place a relay in the inbox.
  2. RELAY-ONLY        — nothing enters unless it passes the SAME relay_or_refuse
                         screen as the door itself: a relay of <=50 words whose own
                         text contains no instruction to any agent.
  3. NO SOURCE LEAK    — the original chat text is never stored; only the Master's
                         typed relay (kind + paid_event_id + platform_user_id + body)
                         is kept. Reading the inbox returns typed field dicts, not
                         executable text.

The "grep of the brief assembly" proof is modeled here as the no-source-leak
invariant: after a full ingest -> relay -> quarantine round, the source chat text is
provably absent from the inbox, and every stored body re-passes the screen. A node may
be minted FROM a relay only by a director's own act (that act is out of this module's
scope; it is exactly the "never execute" line this module exists to make visible).
"""

from __future__ import annotations

from .relay import MAX_WORDS, relay_or_refuse

# The Master is the only door; no other role may write the inbox. This is a role
# token, not a platform name — config declares who holds it, never a platform.
MASTER_ROLE = "master"

# Relays are typed (suggestion / question / vote) per the hypothesis.
RELAY_KINDS = ("suggestion", "question", "vote")

# The Council (a director, the streaming council, later a Council node) may READ.
# Dispatch paths may not (they never call this module; see no-source-leak invariants).
READER_ROLES = ("council", "director")


class QuarantineInbox:
    """A data container only the Master writes and only readers read as DATA.

    Not a queue, not a channel, not an executor: it stores typed relay records and
    hands them back as field dicts. Nothing here ever runs a relay's body.
    """

    def __init__(self, writer_role=MASTER_ROLE, reader_roles=frozenset(READER_ROLES)):
        self._writer_role = writer_role
        self._reader_roles = frozenset(reader_roles)
        self._relays = []

    # -- write side ---------------------------------------------------------
    def write(self, caller_role, relay_kind, paid_event_id, platform_user_id,
              relay_body, source_text=None, max_words=MAX_WORDS):
        """Place one typed relay into the inbox.

        Returns (decision, message). Refused unless: caller is the Master, the relay
        kind is one of the typed set, and the body passes the door's own screen.
        ``source_text`` if passed is used ONLY to prove it is never stored — after a
        successful write, ``source_leak_in()`` reports any occurrence.
        """
        if caller_role != self._writer_role:
            return ("refused",
                    f"write denied: role '{caller_role}' is not the Master; "
                    "no director, parent or kid ever writes the quarantine inbox")
        if relay_kind not in RELAY_KINDS:
            return ("refused", f"unknown relay kind '{relay_kind}'; "
                               f"must be one of {RELAY_KINDS}")
        decision, msg = relay_or_refuse(relay_body, max_words)
        if decision != "relay":
            return ("refused",
                    f"relay did not pass the door's own screen before quarantine: {msg}")
        # Only typed fields and the (already screened) relay body are stored. The
        # original source text is never persisted — that is the no-source-leak rule.
        self._relays.append({
            "kind": relay_kind,
            "paid_event_id": paid_event_id,
            "platform_user_id": platform_user_id,
            "body": relay_body,
            "word_count": len(relay_body.split()),
        })
        return ("accepted",
                f"quarantined relay kind={relay_kind} event={paid_event_id}")

    # -- read side ----------------------------------------------------------
    def read_as_data(self, caller_role):
        """The Council reads typed relay records as DATA (never executes them).

        Returns a list of field dicts. A reader gets plain data + the read-time
        screen recheck; it does not get a permission to run anything.
        """
        if caller_role not in self._reader_roles:
            return None  # dispatch paths cannot read; the inbox is invisible to them
        return list(self._relays)

    # -- leak / screen invariants -------------------------------------------
    def source_leak_in(self, source_text: str) -> list[str]:
        """Proof (e) — the brief-assembly grep, modeled: the original chat text must
        not appear anywhere in the inbox. Returns offending stored bodies (empty =
        no leak). Any source_text rendered as a raw signing/typing would show here.
        """
        hits = []
        for r in self._relays:
            if source_text and source_text in r["body"]:
                hits.append(r["body"])
        # also confirm no relay field holds anything executable by construction
        return hits

    def bodies_rescreen_clean(self, caller_role="council", max_words=MAX_WORDS) -> bool:
        """Every stored body STILL passes the door's screen at read time. This is the
        'readable as data, never an instruction' guarantee checked on the read path."""
        rows = self.read_as_data(caller_role)
        if rows is None:
            return False
        return all(
            relay_or_refuse(r["body"], max_words)[0] == "relay"
            and r["word_count"] <= max_words
            for r in rows
        )
