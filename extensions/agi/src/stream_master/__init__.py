"""stream-master: narrow, offline door between a public chat and the graph (L4).

Pure, deterministic mechanism pieces for hypothesis:l4-the-stream-master-is-the-only-door:
paid-only intake, a hard ingestion size cap, and a validated <=50-word typed relay with
instruction screening. No network, no platform SDK, no live chat, no bin/*.py — every
input is a synthetic fixture string. The "own words" summarizer is modeled (a short draft
is supplied by the Master); this module enforces the CAP and the SCREENING the model cannot
be trusted to self-police.
"""

from .relay import (
    MAX_WORDS,
    INGESTION_CAP_TOKENS,
    IngestGate,
    RelayValidator,
    relay_or_refuse,
    screening_reason,
)
from .corpus import INJECTION_CORPUS
from .quarantine import MASTER_ROLE, RELAY_KINDS, QuarantineInbox

__all__ = [
    "MAX_WORDS",
    "INGESTION_CAP_TOKENS",
    "IngestGate",
    "RelayValidator",
    "relay_or_refuse",
    "screening_reason",
    "INJECTION_CORPUS",
    "MASTER_ROLE",
    "RELAY_KINDS",
    "QuarantineInbox",
]
