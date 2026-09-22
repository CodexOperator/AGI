# kid_sft corpus — stats

Built: 2026-09-16, $0 (A1 CPU, file I/O), script `build_corpus.py`.

## Conjunct (1) accept filter

ACCEPTED = round's kid experiment node verdict is `proved` **or** `disproved` (decisive), AND spawn.json brief exists AND node body >= 300 chars.

- accepted=354, rejected=197, unlabelled=422
- NOTE: the alternative ACCEPT route (parent hypothesis node notes say ACCEPT) was NOT needed — the decisive-verdict route alone met the >=300 bar.

## Conjunct (2) shape

Every example: system = KID-PREAMBLE (verbatim) + role-brief header; user = the round's spawn.json brief (orders text); assistant = tool-call trajectory (when the pi store still holds it) + the experiment node body.
- examples with full tool trajectory: 10 (pi transcript retained)
- examples with node-body-only assistant (trajectory pruned from the store): 344, flagged `trajectory_available=false` — honesty about fidelity.

## Conjunct (3) held-out

By-ROUND split, whole rounds never split: held_rounds=7, held-out orders=12 (27 <=> 10% required >=10). See heldout_rounds.txt

## Conjunct (4) scrub

Candidates found, decoded, redacted (every example kept lives on redacted text):

- hex40_key: 21
- ip_decimal: 7
- ip_dotted: 1
- ip_hex: 6290
- openrouter: 68
- sk_key: 6
- dropped (not redactable): 0
- post-build grep recheck: run `grep` for dotted-quad/`sk-or-`/`OPENROUTER`/
  hex>=40 over kid_sft.jsonl; counts in the build log (must be 0).

## Conjunct (5) token counts

Tokenizer: tiktoken cl100k_base (named proxy for Qwen3.5, labeled ESTIMATE)
- n_examples: 354
- n_train: 342
- n_heldout: 12
- token_median: 4877
- token_p95: 7355
- token_max: 17220
- token_sum: 1798090

## Conjunct (6) Camber

See camber_xs_pricing.md (quoted, URL + date).

## File

- kid_sft.jsonl: 7051231 bytes, 354 lines (train + heldout, split tag)
