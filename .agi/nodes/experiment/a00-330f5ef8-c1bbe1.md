---
id: experiment:a00-330f5ef8-c1bbe1
mint_id: 4279c9b4c1ce4fd6aaddb869045521ce
type: experiment
parents:
  - hypothesis:lm-jev-single-axis-question-beats-baseline
next_edges: []
confidence: 0.9
edited_by: a00-28d22ed0
evidence_runs:
  - experiment:a00-330f5ef8-c1bbe1
line_ceiling: 300
loop: hypothesis:lm-jev-single-axis-question-beats-baseline@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "independent recompute of arm1_review q2 agreement and AUC from persisted single_axis_rows.jsonl, no kid score fn", "expected": "agreement >= 0.826 and AUC >= 0.60 (the pre-registered bar)", "observed": "agree 0.541, AUC 0.581, n=370, base 0.776", "result": "FALSIFIED - the bar is missed by 0.285 agreement / 0.019 AUC; the kid disproved verdict stands"}
  - {"conjunct": 2, "class": "gate", "cmd": "independent recompute of arm0_prior q1 agreement plus wire capture of the arm0 state", "expected": "q1 < 0.55 would show the 0.588 residual is a reading, not a class prior", "observed": "q1 0.051, n=369, base 0.507; wire: state = 27-char act id only, keys q1..q5, no body bytes, no scrub token, 1110 calls", "result": "did not falsify - the empty-body arm does NOT reproduce the 0.588 residual; it is a reading"}
  - {"conjunct": 3, "class": "wire", "cmd": "monkeypatched the urllib call site on a forced cache miss and captured the questions arm2 sends", "expected": "exactly one choice verdict-class question on the scrubbed body, nothing else", "observed": "arm2 1110 calls, keys=['q1'], len(state)=6857, [SCRUBBED] present; independent recompute q1 0.607 (macro AUC 0.855)", "result": "did not falsify - right input reaches the call; q1 0.607 is below the 0.65 bar but above the 0.588 batched residual"}
  - {"conjunct": 1, "class": "auth", "cmd": "env -u TYPESAFE_API_KEY -u TYPESAFE_KEY python3 acts_replay_single_axis.py", "expected": "refusal by name with zero network", "observed": "exit 2, stderr blocked:no_key -- 0 network calls", "result": "did not falsify - refusal by name holds"}
production_lines: 74
profile: balanced
role: kid
scaffold_hash: c2a78d481e9626de
season: 2
title: "Cause 2 SHAPE + prior control: single-axis accept-vs-demote call 0.541 vs 0.776 base (falsified), empty-body arm q1 0.051 (residual is a reading, not a prior)"
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-330f5ef8-c1bbe1

## Experiment

Cause 2 (SHAPE) + the prior control, on the TM.42 pinned scrubbed corpus. New file
`.agi/context/local-maxxing/typesafe/acts_replay_single_axis.py` (74 lines), importing
`acts_replay` as `J` (`MODEL=jev-1.13.0`, `SEED=20260918`, `REPEATS=3`, `ENDPOINT`,
`PRICE`) and `acts_replay_scrub` as `S` for the pin + `scrub()`. Corpus PINNED via
`S.pinned_corpus()`: the 370 act ids in `acts_replay_scrub.jsonl`, labels re-derived from
live node files, state = node BODY with `PAT`/`[SCRUBBED]` applied. No re-sampling.

Three arms, same acts, same seeds, same n=370 (1110 calls each = 3330 total), ONE jsonl
cache (`single_axis_cache.jsonl`, key = `arm|act|repeat|model`) + ONE rows jsonl
(`single_axis_rows.jsonl`), flushed after every call. No per-item cache dirs.

| arm | question | state |
|---|---|---|
| arm0_prior | `J.Q` batched five questions | the act id ONLY (`experiment:a00-...`, 27 chars, no body bytes) |
| arm1_review | ONE `noul` "accepted as-is, not demoted?" (wire key `q2` so `S.agree`'s noul branch scores it) | scrubbed body |
| arm2_verdict | ONE `choice` "select the verdict class" (criteria from `J.Q["q1"]`) | scrubbed body |

Command: `python3 acts_replay_single_axis.py` → `single_axis.md`.

## Evidence

Pinned n = 370 acts (verdict + experiment). All 3330 rows HTTP 200. Residual scrub leak
tokens in the states = 0 (`leaked_acts=0.000`).

| arm | q | label | n | agree | base | AUC | ECE | confusion (top 6) |
|---|---|---|---|---|---|---|---|---|
| arm0_prior | q1 | q1 | 369 | **0.051** | 0.507 | 0.558 | 0.776 | inconclusive_lean_proved>pending:162 proved>pending:129 inconclusive_lean_disproved>pending:31 inconclusive_lean_proved>proved:24 proved>proved:12 pending>pending:6 |
| arm0_prior | q2 | q2 | 370 | 0.257 | 0.776 | 0.314 | 0.240 | accept>demote:214 accept>accept:73 demote>accept:49 demote>demote:34 |
| arm1_review | q2 | q2 | 370 | **0.541** | 0.776 | **0.581** | 0.172 | accept>accept:147 accept>demote:140 demote>demote:52 demote>accept:31 |
| arm2_verdict | q1 | q1 | 369 | **0.610** | 0.507 | **0.855** | 0.161 | proved>proved:116 inconclusive_lean_proved>inconclusive_lean_proved:84 inconclusive_lean_proved>proved:47 inconclusive_lean_proved>pending:43 proved>inconclusive_lean_proved:23 inconclusive_lean_disproved>inconclusive_lean_disproved:14 |

AUC: arm1/arm0-q2 = binary AUC on the `accept` positive class; arm2 = macro one-vs-rest
over the 5 verdict classes. `n=369` on the choice arms = one act whose recorded class is
not in the 5-class set; `n=370` on the accept/demote arm.

**Pre-registered bar, line by line (bars not moved):**

1. ARM 1 agree >= 0.826 **and** AUC >= 0.60 → measured **0.541 / 0.581 — BOTH FAIL**.
2. ARM 0 q1 < 0.55 → measured **0.051 — PASS** (the bare id predicts `pending` for
   322/370 acts; the 0.588 batched residual was NOT a class prior).
3. ARM 2 q1 >= 0.65 → measured **0.610 — FAIL** (but it DOES clear the 0.588 batched
   residual, +0.022).

**Falsifier pre-registered in the parent, line by line:**

- "ARM 1 agreement <= 0.796 or AUC < 0.55" → **TRIPS on agreement (0.541 <= 0.796)**.
  Cause 2 (question shape) is dead for the accept-vs-demote axis; hop 3 = cause 3
  (attach the reviewer evidence). AUC did not trip (0.581 >= 0.55), so the body carries
  a weak-but-real review signal that the noul threshold mis-calibrates (ECE 0.172).
- "ARM 0 q1 >= 0.55" → does NOT trip. jev is reading the body on the verdict axis.
- "ARM 2 q1 <= 0.588" → does NOT trip (0.610 > 0.588). Narrowing buys a little on the
  verdict axis; it does not reach 0.65.

Surprise worth carrying forward: arm2's macro AUC is **0.855** — on the scrubbed body jev
ranks verdict classes well, so the verdict axis is readable; TM.42's 0.588 agreement on
the batched form understated a real signal. The accept-vs-demote axis is the one that is
weak (AUC 0.581) and, worse, mis-thresholded against a 0.776 majority base.

Spend: **$0.161497** = 3,845,157 input tokens × $0.042/Mtok (cap $1.00; 16% used; all
three arms completed; J.CAP's $0.50 per-process bound never bound).

Probes (recorded):
- **auth** — `env -u TYPESAFE_API_KEY -u TYPESAFE_KEY python3 acts_replay_single_axis.py`
  → stderr `blocked:no_key -- 0 network calls`, exit 2, no call site reached.
- **gate** — every one of the 3330 rows HTTP 200; `max(leak_after) = 0`; arms balanced
  1110/1110/1110; answers keyed `q1..q5` (arm0), `q2` (arm1), `q1` (arm2).
- **wire** — `urllib.request.urlopen` monkeypatched on a forced call (probe_wire.py):
  arm0 state = the 27-char act id, no newline, 5 questions; arm1 = scrubbed body (6823
  chars) + exactly 1 `noul` question; arm2 = scrubbed body + exactly 1 `choice` question;
  the three cache keys are distinct, so arms cannot collide in the shared jsonl.
- Two later replays were cache hits: `single_axis_cache.jsonl` stayed at 3330 lines and
  `single_axis.md` was byte-identical, so the score re-runs at $0.

## Verdict

The pre-registered hypothesis (ALL THREE conditions) is **not supported** — condition 1
fails by a wide margin and condition 3 fails. Cause 2 (question shape) is falsified on
the accept-vs-demote axis. Condition 2 passing is the useful survivor: the TM.42 batched
q1 residual is a reading, not a class prior. Next hop is cause 3 / calibration, not shape.
No engine code changed; `python3 -m pytest extensions/agi/tests/test_cli_done_kid_ceiling.py -q`
→ 2 passed (the new file is a context script and has no test file of its own).

## Agent Notes
3 arms, 3330 calls, $0.161497 of $1.00, pinned n=370 scrubbed: ARM1 single-axis accept-vs-demote 0.541 agree / AUC 0.581 (bar 0.826/0.60) FAILS and trips the parent falsifier -> cause 2 SHAPE dead, hop 3 = cause 3; ARM0 id-only q1 0.051 PASSES (0.588 residual was a reading, not a class prior); ARM2 single choice q1 0.610 / macro AUC 0.855 clears the 0.588 batched residual but misses 0.65 -- verdict axis is readable, accept-vs-demote is mis-thresholded.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW of experiment:a00-330f5ef8-c1bbe1. (1) WHAT THE INSTRUCTION SAID. The pre-registered claim in hypothesis:lm-jev-single-axis-question-beats-baseline: ARM1 single-axis accept-vs-demote agreement >= 0.826 AND AUC >= 0.60; ARM0 empty-body q1 < 0.55; ARM2 verdict-class q1 >= 0.65; and the parent must run ONE negative probe per conjunct and record it as probes:. (2) WHAT THE MACHINE ACTUALLY DOES, cited to the bytes. acts_replay_single_axis.py defines ARMS with arm0 state = a[id] (id only), arm1 = one noul question under wire key q2 on S.scrub(body), arm2 = one choice q1 on S.scrub(body); cache key = sha256(arm|act|rep|model) so the three arms cannot collide in the shared single_axis_cache.jsonl. I independently recomputed from the persisted rows (no kid score fn): arm1 q2 agree 0.541, AUC 0.581 (n=370, base 0.776) -- bar missed by 0.285/0.019, so conjunct 1 is FALSIFIED and the kid disproved verdict stands. arm0 q1 0.051 (n=369, base 0.507) -- conjunct 2 holds; the wire probe captured arm0 sending a 27-char act id as state, keys q1..q5, no body bytes, 1110 calls, so the prior is measured on a body-free input. arm2 independent recompute 0.607, macro AUC 0.855 -- conjunct 3 misses 0.65 but clears the 0.588 batched residual, so narrowing buys only +0.019..0.022 on this axis. My wire probe monkeypatched the urllib call site on a forced cache miss and captured arm1 = exactly q2 noul on a 6857-char scrubbed body, arm2 = exactly q1 choice on the same. (3) THE NEAR MISS. A reader could take the kid score numbers as exact: the kid aggregates by majority-of-3 per repeat (S.agree/J.pick) while my recompute thresholds the mean noul / mean probabilities, so arm0 q2 reads 0.257 (kid) vs 0.281 (mine) and arm2 q1 reads 0.610 vs 0.607. The plausible implementation that satisfies the words and loses the mechanism is one that reports a single aggregation without saying which -- but no pre-registered bar moves under either aggregation (arm0 q2 stays far below 0.776; arm2 q1 stays below 0.65 and above 0.588), so this is a reporting caveat, not a falsification. Second near miss: an arm-cache key that omitted the arm name would let arm1 answers satisfy an arm0 lookup and silently fake the prior; the key carries the arm, and the cache shows 1110 rows per arm at HTTP 200. (4) DEVIATION. I did not re-run the kid suite as evidence, per the parent contract; I recomputed independently and ran my own probes. The kid recorded its probes in the body prose only, so I added the frontmatter probes: field via write.py -- the four probes above are mine. Deliverables named by the kid all resolve in the working tree: acts_replay_single_axis.py (74 lines, matches production_lines 74), single_axis_cache.jsonl (3330), single_axis_rows.jsonl (3330), single_axis.md (1061 bytes), title set, verdict disproved, confidence 0.9.
<!-- THOUGHT:END -->

Parent review: accepted disproved. Independent recompute from persisted rows confirms arm1 agree 0.541 / AUC 0.581 (bar 0.826/0.60, conjunct 1 FALSIFIED), arm0 q1 0.051 (prior control holds), arm2 q1 0.607 / AUC 0.855 (below 0.65, above 0.588). Wire probe confirms each arm sends the intended state and question shape; auth probe exits blocked:no_key. Trajectory: cause 2 SHAPE is dead on accept-vs-demote, hop 3 = cause 3 (reviewer evidence) or calibration; the verdict axis is genuinely readable at AUC 0.855 and the TM.42 0.588 was an argmax understatement.
