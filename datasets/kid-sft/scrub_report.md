# kid_sft — scrub report (conjunct 4)

Built 2026-09-16, $0 (A1 CPU). Script: `build_corpus.py`.

## Method

Every `system` / `user` / `assistant` string in every example was scanned for address- and
key-shaped tokens, each candidate DECODED, then REDACTED in place (`[REDACTED]`). Redaction is
longest-token-first so a 64-hex sha is removed whole before an 8-hex sub-window can fire.
An example is only DROPPED when a candidate cannot be removed without destroying the example
(no such case arose). Post-build `grep` recheck (below) re-proves the jsonl is clean.

## Candidates found, decoded, redacted (all redacted; dropped = 0)

| kind | decoded as | count |
|---|---|---|
| ip_dotted   | literal dotted-quad IPs      | 1 |
| ip_hex      | hex tokens decoding to a 32-bit IP (8-hex windows) | 6290 |
| ip_decimal  | decimal integers decoding to a 32-bit IP | 7 |
| sk_key      | `sk-or-...` secret keys        | 6 |
| openrouter  | the literal provider name      | 68 |
| hex40_key   | ed25519-style hex >= 40 chars  | 21 |
| **dropped** | (not redactable)               | **0** |

(ip_hex count is high because every 8-hex token in node frontmatter — agent-id segments,
short commit hashes — decodes to a 32-bit integer and is conservatively redacted. This
over-redaction is accepted collateral: conjunct (4) requires ZERO leaves, and over-redaction
only blurs non-secret identifiers, never leaks.) — over-redaction note.

## Post-build grep recheck over `kid_sft.jsonl` (must be 0)

| pattern | count |
|---|---|
| dotted-quad `\b\d{1,3}(\.\d{1,3}){3}\b` | 0 |
| `sk-or-[A-Za-z0-9_\-]+` | 0 |
| `OPENROUTER` (case-insens) | 0 |
| hex >= 40 `\b[0-9a-fA-F]{40,}\b` | 0 |

All named subnet/loopback forms (127.x, 10.x, 192.168.x, 172.16-31.x) that existed as
dotted-quad were redacted by the ip_dotted rule; hex and decimal integer encodings of any IP
included both byte orders (normal and byte-reversed) are removed by ip_hex / ip_decimal.

## Struggle / caveat

- The residual-56-hex bug: an 8-hex sub-window inside a 64-hex sha was redacted before the
  longer token, corrupting it and leaking 56 hex chars into the jsonl. Fixed by ordering
  redaction longest-token-first; final grep confirms 0 remains. This is the kind of
  overlap a fixed regex order silently misses.