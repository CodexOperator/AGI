#!/usr/bin/env python3
"""scrub.py -- the one span-based redactor for every datasets/ landing.

Patterns: dotted/hex/decimal-encoded IPs, sk-or- keys, OPENROUTER_*KEY
mentions, hex>=40 (ed25519-style keys), emails.

Why span-based, not token-then-global-replace: a naive approach (find a set
of sensitive substrings, then `text.replace(token, "[REDACTED]")` for each)
can corrupt UNRELATED content. Confirmed case (ABC.01 landing, 2026-09-20):
an 8-char truncated-sha256 hash fragment in a node body happened to decode
as IP-shaped and got flagged as a candidate; replacing it globally also
clobbered the first 8 characters of a DIFFERENT, unrelated 16-char truncated
hash elsewhere in the same file that coincidentally started with the same 8
characters, leaving a corrupted residue exposed. The content in that
instance was benign (a content hash of public test data), but the mechanism
was wrong and would not stay benign in general.

Fix: collect match SPANS directly from the source text (never a derived
token list), resolve any overlaps by keeping the longest span at each
position, then rebuild the text by walking spans left-to-right and
substituting only the exact matched region. A short flagged span can then
never reach outside its own boundaries to corrupt a coincidentally similar
but unrelated longer run elsewhere.

Usage:
    from scrub import scrub_file, redact_text
    scrubbed_text, redaction_counts = scrub_file("/path/to/file")
    # or on an in-memory string:
    scrubbed_text, redaction_counts = redact_text(raw_text)

CLI: python3 scrub.py <in> <out>  -- scrub one file, print redaction counts.
"""
import re
import sys

IP_DOTTED = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")
IP_DEC = re.compile(r"\b(?:[1-9]\d{7,11})\b")
HEX_RUN = re.compile(r"\b[0-9a-fA-F]{8,}\b")
SK_OR = re.compile(r"(?i)sk-or-[A-Za-z0-9_\-]+")
OPENROUTER_KEY = re.compile(r"(?i)OPENROUTER_[A-Z_]*KEY[A-Za-z0-9_=]*")
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")


def hex_to_ip(h):
    try:
        u = int(h, 16)
        if u > 0xFFFFFFFF:
            return None
        return ".".join(str((u >> (8 * i)) & 0xFF) for i in (3, 2, 1, 0))
    except Exception:
        return None


def decimal_to_ip(s):
    try:
        u = int(s)
        if u > 0xFFFFFFFF or u < 0x10000000:
            return None
        return ".".join(str((u >> (8 * i)) & 0xFF) for i in (3, 2, 1, 0))
    except Exception:
        return None


def collect_spans(text):
    """Return list of (start, end, kind) for every sensitive span, computed
    directly from the ORIGINAL text so every span's coordinates are exact
    and safe to resolve for overlaps without corrupting unrelated content."""
    spans = []
    for m in IP_DOTTED.finditer(text):
        spans.append((m.start(), m.end(), "ip_dotted"))
    for m in SK_OR.finditer(text):
        spans.append((m.start(), m.end(), "sk_key"))
    for m in OPENROUTER_KEY.finditer(text):
        spans.append((m.start(), m.end(), "openrouter_key"))
    for m in EMAIL.finditer(text):
        spans.append((m.start(), m.end(), "email"))
    for m in HEX_RUN.finditer(text):
        h = m.group(0)
        if len(h) >= 40:
            spans.append((m.start(), m.end(), "hex40_key"))
        elif hex_to_ip(h):
            spans.append((m.start(), m.end(), "ip_hex"))
    for m in IP_DEC.finditer(text):
        if decimal_to_ip(m.group(0)):
            spans.append((m.start(), m.end(), "ip_decimal"))
    return spans


def resolve_overlaps(spans):
    """Sort by start; when spans overlap, keep the one that extends
    furthest, extending the kept span rather than dropping coverage."""
    spans = sorted(spans, key=lambda s: (s[0], -(s[1] - s[0])))
    kept = []
    last_end = -1
    for start, end, kind in spans:
        if start >= last_end:
            kept.append((start, end, kind))
            last_end = end
        elif end > last_end:
            ps, pe, pk = kept[-1]
            if end > pe:
                kept[-1] = (ps, end, pk)
                last_end = end
    return kept


def redact_text(text):
    """Scrub an in-memory string. Returns (scrubbed_text, kind_counts)."""
    spans = resolve_overlaps(collect_spans(text))
    if not spans:
        return text, {}
    out = []
    pos = 0
    kinds = {}
    for start, end, kind in spans:
        out.append(text[pos:start])
        out.append("[REDACTED]")
        kinds[kind] = kinds.get(kind, 0) + 1
        pos = end
    out.append(text[pos:])
    return "".join(out), kinds


def scrub_file(path):
    """Scrub a file's contents. Returns (scrubbed_text, kind_counts)."""
    raw = open(path, errors="replace").read()
    return redact_text(raw)


def recheck(text):
    """Post-scrub sanity check: return any remaining candidate spans (should
    be empty on scrubbed output, modulo intentionally-public strings like an
    agent's own id). Always run this on the OUTPUT before committing it."""
    return collect_spans(text)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: scrub.py <in-file> <out-file>", file=sys.stderr)
        sys.exit(2)
    scrubbed, kinds = scrub_file(sys.argv[1])
    with open(sys.argv[2], "w") as f:
        f.write(scrubbed)
    remaining = recheck(scrubbed)
    print(f"redactions: {kinds}")
    print(f"remaining candidates in output (should be ~0): {len(remaining)}")
