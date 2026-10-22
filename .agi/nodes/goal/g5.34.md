---
id: goal:g5.34
mint_id: da91a7b9370d4107a6c2fe3983d10d72
type: goal
parents:
  - goal:g5
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G5.34
goal_kind: subgoal
origin: goal
role: prime
season: 3
seeds: []
status: complete
tags: []
title: "G5.34: the owner's abliterated open-weight models sit on this box's /data, checksum-verified: DeepSeek-V4-Flash abliterated Q2_K + Qwen3.8-27B abliterated (full weights + one Q4 GGUF), with the 20% disk floor kept"
town: local-maxxing
---
# goal:g5.34

## Why this exists
goal:g5 (Local-maxxing): the owner asked (00:5xZ 10-22, verbatim below) for a director-general to download the abliterated models the town could use, quantized at least. The Prime measured this box at 00:4xZ 10-22: /data 352G, 273G free (so ~200G usable above the 20% floor), / 22G free, 7 GB RAM, 4 cores, no GPU — a STORAGE target here, not a serving one. The upstream sizes (Hugging Face file listings as reported by search, 00:5xZ 10-22, ESTIMATE until the director reads the API): DeepSeek-V4.1-Flash abliterated smallest llama.cpp build Q2_K ~271 GB, full ~510 GB (both over the budget); DeepSeek-V4-Flash abliterated (huihui-ai) Q2_K ~99.7 GB, Q4_K ~165 GB; Qwen3.8-27B abliterated (huihui-ai) full ~55 GB (estimate), Q4 GGUF ~17 GB (estimate); Qwen3.8-Max (2.4T) multi-TB; Qwen 4 previewed 09-22, no weights. Everything feasible together (~240 GB) exceeds the budget; the owner picked the set (AskUserQuestion 00:5xZ 10-22): "DeepSeek + Qwen 27B (Recommended)" = ~172 GB.

## OWNER 2026-10-22 00:5xZ, verbatim
"Can we have one of the director generals download all the abliterated models we could find useful at least quantized. Like we have qwen I think but I also wanna download a deepseek v4.1 flash quantized abliterated model and maybe a full size abliterated deepseek model. Definitely a full size abliterated qwen 3.8 and 4.0 when that comes out. Just let me know which ones are feasible which are not. Use pirate face to download them using torrents if needed while it’s still legal"
"It’s not and I’m guessing there’s no flash version abliterated that’s smaller? On deepseek"
Pick: "DeepSeek + Qwen 27B (Recommended)" — DeepSeek V4-Flash abliterated Q2_K (~100 GB) + Qwen3.8-27B abliterated full weights (~55 GB) + its Q4 GGUF (~17 GB).

## Target end-state
- /data/work/models/ (on the /data mount, never /) holds, each with a SHA256SUMS line that matches the Hugging Face LFS oid:
  1. DeepSeek-V4-Flash abliterated, Q2_K GGUF (huihui-ai: Huihui-DeepSeek-V4-Flash-abliterated-ds4-GGUF, or its newer 0731 sibling if that has a llama.cpp Q2 <= 105 GB), with the repo's README + license;
  2. Qwen3.8-27B abliterated, full safetensors (huihui-ai/Huihui-Qwen3.8-27B-abliterated) + config/tokenizer + license;
  3. one Q4_K_M (or nearest Q4) GGUF of that same abliterated 27B (huihui-ai's own GGUF if it exists, else the best-documented community quant, named in the leaf's THOUGHT).
- A one-page doc node (doc:abliterated-models-local) lists each file: repo, revision sha, bytes, sha256, license, and the runtime it needs (ds4 / llama.cpp build).
- Qwen 4: when open weights AND an abliterated build exist, the director reports the size; it downloads only if the 20% floor still holds after it, else it banks the pick to the owner.

## Invariants
- /data stays >= 20% free after every file (read `df` BEFORE each file, against the file's API size); / is never written.
- Weights never enter the git repo or the graph: no file under .agi/ or the worktrees, no LFS, no grid payload.
- One download at a time, rate-limited, under skill agi-memory-guard (a 100 GB stream is an io and page-cache load on a shared box); never during a post move (goal:g7.16.1.11.45 G7) — start after G7 closes.
- Source = Hugging Face direct, public repos, no token. A torrent only if Hugging Face fails for a file AND that file's license (MIT for DeepSeek, Apache-2.0 for Qwen3.8-27B) permits redistribution; the torrent's payload must match the same sha256.
- No serving here: nothing is loaded into RAM on this box (7 GB).

## Falsifier
1. `cd /data/work/models && sha256sum -c SHA256SUMS` exits 0 with exactly the 3 artifacts' weight files listed, AND `df --output=pcent /data | tail -1` <= 80%.
2. negative: `git -C /data/work/agi ls-files | grep -ciE '\.(gguf|safetensors)$'` = 0, and `find / -xdev -name '*.gguf' 2>/dev/null` (root fs only) = 0 hits.

## Out of scope
DeepSeek-V4.1-Flash abliterated (smallest general build ~271 GB) and any full-size DeepSeek (~510 GB+): over this box's budget, banked to the owner. Qwen3.8-Max 2.4T: multi-TB. Qwen3.8-Flash-Next abliterated: not in the owner's pick. Serving any of these (goal:g5's serving leaves).

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
CLOSED complete 2026-10-22 by its owner, director-general-1, on the falsifiers as written (re-run after the last file, 08:3xZ-09:xxZ):
1. `cd /data/work/models && sha256sum -c SHA256SUMS`: 36 lines, 36 OK, 0 not-OK, rc 0 (the 3 artifacts' weight files: DeepSeek-V4-Flash-Q2_K-0731.gguf, the 18 Qwen3.8-27B safetensors, Huihui-Qwen3.8-27B-abliterated-Q4_K.gguf; every LFS line = the Hugging Face oid); `df --output=pcent /data` = 66% (<= 80).
2. `git -C /data/work/agi ls-files | grep -ciE '\.(gguf|safetensors)$'` = 0 (MAIN at c35aff54a5). The root-fs find was run as `find / -xdev -path /var/lib/agi -prune -o ( -name '*.gguf' -o -name '*.safetensors' ) -print` = 0 hits: the falsifier's bare `find / -xdev` is AMENDED only by pruning /var/lib/agi (the homes' parent), because a walk there is the dentry-slab trap in skill agi-memory-guard; the other root-fs trees were walked in full, and /data is a different mount.
Doc node: doc:abliterated-models-local on the trunk as c35aff54a5 (G belam, blob cae9d52cb3). Picks: DeepSeek 0731 Q2_K (97.59 GB, smaller than the ds4 repo's 99.71 GB), Qwen3.8-27B full (55.59 GB, 31 files), huihui-ai's plain Q4_K (16.81 GB). Pace 40 MB/s, then 20 MB/s from belam's 06:05Z memory WARN; no stop. Banked out of scope (unchanged): V4.1-Flash abliterated ~271 GB, full DeepSeek ~510 GB+, Qwen3.8-Max, Qwen 4 (not out).
FOLLOW-UP 2026-10-22 (council [word] 09:1xZ, relayed by SM 09:24Z; the blob 61aabca57a had already landed): the own-home read the pruned find skipped, run by director-general-1 as itself, exactly as written:
`du -sh ~/.cache/huggingface ~/.cache/hf 2>/dev/null` -> "No such file or directory" for both (no Hugging Face cache exists; every file came by curl straight into /data/work/models, never through huggingface_hub). `find ~ -xdev -path ~/t -prune -o ( -name '*.gguf' -o -name '*.safetensors' -o -name '*.incomplete' ) -size +100M -print` -> empty, 0 hits (the pattern now includes safetensors and *.incomplete); ~/t itself, which that find prunes, read 0 hits with the same pattern. / has 19G free (68% used), unchanged. Nothing removed, nothing to name: the falsifier holds, so the status stays complete.
<!-- THOUGHT:END -->
