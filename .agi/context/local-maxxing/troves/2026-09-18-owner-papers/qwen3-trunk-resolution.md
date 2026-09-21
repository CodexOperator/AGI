# qwen3-trunk-resolution — resolving the owner's "qwen3.8 50b" candidate
READER: research-reader (read-only). TROVE APPEND-ONLY. Read 2026-09-18 UTC.

## PAGE 1 — Qwen3 model family (qwenlm.github.io/blog/qwen3/, HF Qwen/Qwen3-8B) 2026-09-18
- MEASURED: Released Qwen3 open weights = DENSE: Qwen3-32B, 14B, 8B, 4B, 1.7B, 0.6B;
  MoE: Qwen3-30B-A3B (30B total / 3B active), Qwen3-235B-A22B; plus Qwen3-Next-80B-A3B.
- MEASURED: Qwen3-8B = 8.2B params, 6.95B non-embedding, 36 layers, GQA 32 Q / 8 KV,
  32,768 native context (131,072 w/ YaRN), Apache-2.0.
- RESOLUTION: There is NO "Qwen3 50B" in the released family. "qwen3.8 50b" is most likely
  a garbled "Qwen3-8B" (8 -> "3.8"?) OR "Qwen3-30B-A3B". STATUS: UNRESOLVED — cannot confirm
  a 50B Qwen3 exists. Nearest small Qwen trunks usable on an 8 GB GPU: Qwen3-0.6B/1.7B/4B
  (Q4) or Qwen3-8B (Q4, ~5 GB). EAGLE-3 draft heads exist for Qwen2.5-7B/14B/32B (HF).
- ACTION for the town: assume trunk = Qwen3-8B (or smaller) until the owner supplies the
  exact id; do not plan against a non-existent 50B checkpoint.
