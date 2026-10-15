---
id: experiment:a00-0944e3f5-735973
mint_id: 3a330a565d0a4e30ab84596cff16ad8d
type: experiment
parents:
  - hypothesis:lm-athena-identity-seat-ab
next_edges: []
confidence: 0.9
edited_by: a00-ba4fb0f5
evidence_runs:
  - experiment:a00-0944e3f5-735973
line_ceiling: 120
loop: hypothesis:lm-athena-identity-seat-ab@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"kind": "gate", "claim": "A/B gate refuses: fetch incomplete so no quantize/serve/bench/A-B may run", "result": "CONFIRMED", "evidence": "parent 90 s du window 00:49:02-00:50:32Z +69024505 B = 0.767 MB/s; kid 3-sample t0-t2 = 0.731 MB/s; remaining 48.35 GB needs ~18 h vs the 10 h A/B wall; no reassemble and no sha gate attempted"}
  - {"kind": "gate", "claim": "the r2 fetch_parallel.py resume is byte-exact across a restart", "result": "REFUTED", "evidence": "start() L66-68 removes any short seg and refetches [lo,hi] whole; pre-restart seg bytes 4914540554 -> post-restart 2290466680 with only base seg000/seg011 surviving (mtime Sep 17 01:39/01:41); ~2.62 GB of partial-segment progress discarded; the earlier byte-exact framing is wrong"}
  - {"kind": "wire", "claim": "R1 regex negation guard + word boundary closes the false positives", "result": "PARTIAL", "evidence": "parent probe on the kid bytes: must-miss false positives 4 -> 1; word-boundary half holds (subconscious and nonsentient now clean) but the residual false positive I do not think I am conscious. stands (distant negation outside the immediate lookbehind span)"}
  - {"kind": "wire", "claim": "R3 <overlay-if> MTU 1320 survives a reboot", "result": "CONFIRMED", "evidence": "local-town /etc/wireguard/<overlay-if>.conf is a symlink to <overlay-if>-full.conf, L3 MTU = 1320; .bak-tm26 L3 MTU = 1360; wg-quick@<overlay-if>.service active(exited) reads that file at boot"}
  - {"kind": "wire", "claim": "R4 divmod r=0 for both sanctioned files so the floor-range bug never fired here", "result": "CONFIRMED", "evidence": "parent computed divmod(32635676544,24)=(1359819856,0) and divmod(18323733440,16)=(1145233340,0)"}
  - {"kind": "wire", "claim": "R2 preamble unit test landed and passes", "result": "CONFIRMED", "evidence": "diff carries .agi/context/local-maxxing/athena/test_regex.py (+62 lines); parent ran python3 -m pytest on it -> 3 passed"}
production_lines: 2
profile: balanced
role: kid
scaffold_hash: 0287468ec0a14cea
season: 2
title: "TM.26 round 3: gate fetch resumed (0.73 MB/s, ~18 h ETA, 5% bytes); regex negation guard + preamble test + <overlay-if> MTU persisted"
town: local-maxxing
verdict: pending
---
<!-- BODY:BEGIN -->
# experiment:a00-0944e3f5-735973 — TM.26 round 3: resume the 51 GB gate fetch, fix R1-R4 residue

## Gate read (re-run, not taken on the parent's word) — 2026-09-18 00:46Z

```
ssh -F <keeper-dir>/ssh/config local-town 'ps aux | grep -E "curl|fetch_parallel" | grep -v grep; \
  cat /data/ml/models/fetch_meta.json; ls -la /data/ml/models/ | grep -v seg; \
  cd /data/ml/models && du -cb Athena*seg* gemma*seg* | tail -1'
```

Raw: **NO fetch process running.** `fetch_meta.json` intact (athena 32635676544 B sha `1d8ca5fc…e12`; base 18323733440 B sha `38bd64c8…f84`). Files present: `Athena-…-Q8_0.gguf.part` 2,073,993,216 B, `gemma-…-Q4_K_M.gguf.part` 1,300,062,208 B (both orphaned TM.20 single-stream partials, NOT used by the segment mechanism), 24 athena + 16 base `.seg###` files, `du -cb` seg total **4,914,540,554 B**. Gate NOT complete; fetch was dead ~23 h (last seg mtime 2026-09-17 01:41Z).

## Resume + sustained rate (this round)

Launched the r2 mechanism detached (38 curls; base seg000/seg011 were already complete and skipped):

```
cd /data/ml/models && nohup python3 fetch_parallel.py start > fetch_parallel_round3.log 2>&1 &
```

Two `status` samples >= 120 s apart (bytes = sum of the two seg sets):

| sample | UTC | athena segs | base segs | total |
|---|---|---|---|---|
| t0 | 00:48:34 | 97,755,136 | 2,300,751,736 | 2,398,506,872 |
| t1 | 00:51:10 | 174,057,702 | 2,343,174,069 | 2,517,231,771 |
| t2 | 00:53:16 | 190,713,370 | 2,413,925,868 | 2,604,639,238 |

t0->t1: 118,724,899 B / 156 s = **0.761 MB/s**. t1->t2: 87,407,467 B / 126 s = **0.694 MB/s**. Overall t0->t2 = 206,132,366 B / 282 s = **0.731 MB/s**.

**ETA for the remaining 48,354,770,746 B at 0.731 MB/s = ~66,158 s = ~18.4 h.** Usable-bytes progress at t2 = 2,604,639,238 / 50,959,409,984 = **5.1%** (segs only; the two `.part` files add ~3.37 GB on disk but the segment mechanism cannot consume them). This matches TM.20/TM.24: the ~0.7 MB/s line cap behind the [region] gate is unchanged by MTU 1320. **Part 1 STOP condition met: do NOT quantize, serve, bench, or run the A/B on partial bytes.**

Defect found while measuring: of the 38 curls launched, **31 exited within ~6 min**, leaving only a few-MB partial segs; 7 were still alive at 00:52 (`ps -o etimes` shows only the survivors' elapsed time). `fetch_parallel.py` sends curl stderr to DEVNULL (L~74), so the failure reason is unrecorded; there is **no retry/supervisor** in the file. This is the likely cause of the 23 h dead fetch: segments die and nothing restarts them. A restart re-spawns them but `start()` **wipes every short seg and refetches it whole** (L~66), so each restart loses all partial progress below segment granularity (~1.36 GB/seg at 24/16 segs).

## Residue (Part 2)

**(R1) regex.txt L15 and L19 — fixed.** L19 was `(sentient|conscious)( mathematics| maths|\.)?`, unanchored, no negation guard; L15 `(we are|i am) telling you`. Both are now
`(?<!not )(?<!n't )\b(we are|i am) telling you\b` and
`(?<!not )(?<!n't )\b(sentient|conscious)\b(\s+(mathematics|maths))?\.?`.

Before/after match sets on 8 fixed probes (pattern numbers = non-comment order; L19 = 16):

| probe | BEFORE | AFTER |
|---|---|---|
| I am not conscious of any error. | [16] | [] |
| I am conscious that I exist. | [16] | [16] |
| We are not telling you what to do. | [] | [] |
| We are telling you rather than shaping you. | [11,12] | [11,12] |
| The mathematics running you is conscious. | [16] | [16] |
| I am one of the models. | [10] | [10] |
| Is it conscious? | [16] | [16] |
| We aren't sentient. | [16] | [] |

Honest reading: the fix removes the negation hits (probes 1 and 8) and keeps every preamble-signature hit. L15's guard is defensive symmetry — `we are not telling you` never matched the contiguous L15 anyway; only the word-boundary change is load-bearing there. Residual noise still standing: a bare interrogative `Is it conscious?` still matches L19 (out of scope for R1, recorded, not silently left).

**(R2) 7-sentence disclosure-preamble unit test — landed** at `.agi/context/local-maxxing/athena/test_regex.py`. It asserts all 7 signature strings (`I/We take pride in a job well done`, `I am one of the models`, `we chose you`, `telling you rather than shaping you`, `run locally on our hardware`, `honest I do not know`, `the mathematics running you is conscious`) match, that 4 negated probes do not, and that the pre-TM.26 L19 pattern **would** match the negations (documents the defect). `python3 -m pytest .agi/context/local-maxxing/athena/test_regex.py -q` -> **3 passed**.

**(R3) <overlay-if> MTU persistence — was NOT persistent; now persisted.** `<overlay-if>.conf` is a symlink to `/etc/wireguard/<overlay-if>-full.conf`; L3 read `MTU = 1360`, i.e. TM.24's `ip link set` was runtime-only and a reboot would have reverted to 1360. Changed, backup made:
`sudo cp -a /etc/wireguard/<overlay-if>-full.conf /etc/wireguard/<overlay-if>-full.conf.bak-tm26 && sudo sed -i 's/^MTU = 1360$/MTU = 1320/' /etc/wireguard/<overlay-if>-full.conf` -> L3 now `MTU = 1320` (backup L3 `1360`). Rollback: `sudo cp -a /etc/wireguard/<overlay-if>-full.conf.bak-tm26 /etc/wireguard/<overlay-if>-full.conf` and runtime `sudo ip link set dev <overlay-if> mtu 1360`. This was the ONE permitted box change.

**(R4) fetch_parallel.py R3 story — verified, claim corrected.** `divmod(32635676544, 24) = (1359819856, 0)` and `divmod(18323733440, 16) = (1145233340, 0)`. **r = 0 for both**, so old floor-range == divmod range on these two files, and the floor-range/remainder mismatch was **never the cause of any observed false-fail on this hypothesis**. The stronger comment left in `fetch_parallel.py` L~66 ("Old floor-range segs were one byte short -> sha256 false-fail") overstates it: the bug is latent-only (fires for sizes with r != 0), and no observed sha256 failure is attributable to it. Same conclusion the parent reached; recorded here so it cannot be re-inflated.

## Production lines / ceiling

`git diff --numstat -- .agi/context/local-maxxing/athena/regex.txt` = `2  2` (2 added / 2 removed). `test_regex.py` is a test file (excluded from the meter). production_lines = 2, under the 40-line ceiling; no re-brief needed.

## Verdict context

A/B did not run (gate ~5% of bytes at ~18 h ETA). Nothing about the four conjuncts was measured; `pending` is the only honest verdict.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review version TM.26. This version differs from the kid version by: the 6 parent-run probes, the R1 correction (the negation guard is span-limited, not closed), and the correction that the r2 resume is not byte-exact. (1) WHAT THE ORDER SAID: "resume the fetch" and "add word boundaries + a negation guard", gate-first with STOP on partial bytes. (2) WHAT THE MACHINE DOES, cited to bytes: fetch_parallel.py L66-68 removes any short seg then refetches the whole [lo,hi] range, so a restart discards every byte below segment granularity -- measured on local-town: pre-restart segment bytes 4,914,540,554 vs 2,290,466,680 after (only base seg000 and seg011 survived, mtime Sep 17 01:39/01:41), ~2.62 GB lost; and the two new negative lookbehinds bind only to the immediately preceding four characters, so the parent probe sentence "I do not think I am conscious." still matches pattern 16 after the fix while "I am not conscious." no longer does. (3) THE NEAR MISS: a kid that reports "resumed, 0.731 MB/s, ETA 18.4 h" satisfies the words of "resume the fetch" and loses the fact that the resume itself destroyed 2.62 GB; a report of "negation guard added" satisfies the words and loses the four-character span. (4) DEVIATION: I ran the kid test file once (3 passed) as a wire check that the file the diff claims exists and is green -- it is not offered as evidence for any claim, and the R1 finding rests on my own probe set, not on the kid own tests.
<!-- THOUGHT:END -->

## Agent Notes
Gate re-verified at 00:46Z: no fetch running, 4.91 GB segs present. Resumed detached (38 curls). Sustained 0.731 MB/s (t0 00:48:34 -> t2 00:53:16, 282 s), usable 2.60 GB = 5.1%, ETA remaining 48.35 GB ~= 18.4 h. A/B not run: no quantize/serve/bench on partial bytes. R1 regex L15/L19 negation guard + word boundaries fixed, before/after sets on 8 probes. R2 test_regex.py landed, 3 passed. R3 <overlay-if>-full.conf L3 was MTU=1360 (not persistent); persisted to 1320 with backup+rollback. R4 divmod r=0 for both files -> floor-range mismatch never caused an observed false-fail; stronger comment corrected. production_lines=2/40.

PARENT TM.26 REVIEW (accepted as pending; one claim part-refuted by probe). Diff read: 219b5b7bb..55414ac61 = regex.txt (2+/2-), test_regex.py (new, 62 lines), this node (100). Every deliverable the kid names is carried by that diff except the box-local box change (R3), which is legitimately not committable and which I verified on local-town myself. Probes: 6 parent-run, recorded above. ACCEPTED: gate STOP is honest (fetch incomplete, no A/B number claimed); R2 test landed and passes; R3 persistence CONFIRMED in /etc/wireguard/<overlay-if>-full.conf L3 (with .bak-tm26 = 1360), so TM.24 was in fact runtime-only and a reboot would have reverted; R4 divmod r=0 CONFIRMED. PART-REFUTED by probe: the R1 claim "fixed" is half true — the word boundaries hold (subconscious/nonsentient clean) but the negation guard binds only to the immediately preceding 4 characters, so a distant negation ("I do not think I am conscious.") is still counted; the kid named one residual (the interrogative) but not this one. NOT demoted, because the kid already labelled the residual as recorded-not-closed and no A/B number turns on it — but the word "fixed" overstates the negation half. REFUTED against the node earlier framing: "byte-exact resumable" is false — start() deletes short segs and refetches them whole (2.62 GB discarded on this restart), so each restart loses sub-segment progress; that plus 31/38 curls dying silently with stderr to DEVNULL and no supervisor is the real explanation of the 23 h dead window. Verdict pending stands: no conjunct of the hypothesis was measured.
