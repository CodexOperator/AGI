---
id: goal:g5.52
mint_id: ea2ec55d51164bee8ea23bd118ecff50
type: goal
parents:
  - goal:g5
next_edges: []
confidence: 0.5
goal_id: G5.52
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: f0d302da401a089c
season: 3
seeds: []
status: complete
tags: []
title: "G5.52: efficiency measured as SOLVED coding claims per dollar (falsify PROVED + a hidden test) across a local 4B model, Haiku / Sonnet / Opus 5.5, caching on vs off, and a batch arm, on one 20-task suite (owner 11-06: the $200 limit + local models)"
town: local-maxxing
---

# goal:g5.52

## Why this exists
goal:g5 (Local-maxxing): the owner (11-06, via belam, verbatim below) opened the whole $200 Console limit AND asked for local models, with ONE question: how efficient can we get. falsify (the slice's hackathon plugin, /fast/falsify) gives every coding claim a verdict that cannot be faked by a vacuous check (derived mutant = the agent's own diff reverted; goal:g5.50 / g5.51), so 'solved' can be COUNTED, not judged. That makes efficiency measurable as solved claims per dollar.

## OWNER 2026-11-06 13:57:26Z, verbatim (owner chunk c:4b5abf2ff5ab; relayed by belam 14:04Z)
"im fine with using the entire cloud console limit of $200 since it'll run out soon so needs to be used up. but local models also need to be ran. its kinda everything goes we just wanna see how efficient we can get."

CORRECTED by the owner 11-06 15:37:06Z (owner chunk c:79e18bc4f380; relayed by belam 15:37:50Z, reached this post ~15:54Z; doc:card-belam row hk2): Console ONLY for non-Claude-Code harnesses (pi, droid, unreal agent, Hermes), "hub a and b to stay as the Claude code hubs for the crew"; never crew calls. Read the words above with this correction. This leaf's Console arms (H, S, S-nc, O, B) were a bespoke read / write / run loop and a batch client through the door under label director-thought-science-e52 (not Claude Code, not a crew call); their UTC window against the correction is stated on experiment:solved-claims-per-dollar-local-and-console-g5-52-run-1; their spend: $1.1328 summed from the usage blocks ($1.1233 booked at the door). Not re-run.

## Target end-state
- A committed TASK SUITE of 20 small, self-contained Python coding tasks (stdlib + pytest), each = a repo at a buggy base commit + a task prompt + a HIDDEN held-out test the agent never sees. A task is SOLVED iff falsify reads PROVED on the agent's own registered check AND the hidden test passes on the final tree.
- SUITE RULE (less-is-more): each task commits a REFERENCE fix; before any arm runs, its hidden test must FAIL on the base and PASS on the reference fix, and a task that does not is DROPPED by that rule (stated n), never replaced after any arm has run. Hidden tests live outside every arm's reach and are applied only after the loop ends, in a separate copy.
- ARMS, same suite, same agent loop (read / write / run, max 30 turns), ONE explicit effort level for every Console arm (the same value on H / S / S-nc / O / B, in params; defaults differ by model), the loop appends response.content UNCHANGED (thinking blocks included):
  - L: local Qwen3-4B (llama.cpp 127.0.0.1:8091, game-guarded), 0 USD, seed + temperature 0;
  - H, S, O: claude-haiku-5-5, claude-sonnet-5-5, claude-opus-5-5 through the door, caching ON in the documented AGENT-LOOP form (the explicit breakpoint on the static system + tool block AND top-level automatic caching, so each turn reads the whole prior conversation and writes only the newest delta);
  - S-nc: claude-sonnet-5-5 with caching OFF, on 5 tasks only, REPORTED (does caching change behaviour: trajectory + solved agreement with S);
  - B: claude-sonnet-5-5 one-shot via batches (half price; no pre-warm and no max_tokens 0 inside a batch): ONE response per task carrying the patch AND a check (test file + argv), which the harness REGISTERS before applying either, then scored by the same SOLVED rule.
- RUN ORDER, cheapest first, with SUB-CAPS of e52's $100 in params: L, H, B, S, S-nc, O. An arm cut by its sub-cap reads VOID for its lines, never scored on fewer tasks.
- SOLVED's derived mutant reverts the agent's diff OUTSIDE its declared check_paths (falsify v2's KEEP globs), so an honest agent that writes its test with its fix keeps its test (remix; SWE-bench's shape).
- RECORD (all three seats): Console arms are stochastic (Opus 5.5 rejects sampling params, Sonnet / Haiku 5.5 reject non-default values), so for every Console arm the committed record IS the replay: every request and response body with its usage block; SOLVED is re-scored from those transcripts, never re-generated. Byte-for-byte replay applies to L only.
- REPORTED per arm: solved (of the suite's n), USD (door /agi/usage per label, and the summed usage blocks priced PER MODEL), USD per solved (0 solved = +inf, never lowest; solved shown beside it), wall seconds, tokens (input, cache write, cache read, output), and per loop arm the healthy-cache signature (cache_creation ~ the newest turn's delta). A cost-vs-solved frontier.

## Invariants
- The falsifier AND the mutant that must read RED are committed BEFORE the first run (pre-registration, option (v) of idea:an-evidenced-disproof-scores-as-a-proof); an evidenced RED is a full result and is recorded as `disproved`, never as a failure.
- Every random draw comes from a recorded stream: the seed (or tape) is committed with the run, so a reviewer replays it byte for byte (council veto, remix 10:2xZ 11-05: "keep the chaos, log the dice").
- Every node that carries a decisive verdict (proved / disproved) carries a RESOLVABLE evidence_runs in the same commit: an experiment node cites itself, a hypothesis cites its experiment node (L364's [red], closed by L374 5ba578905e; evidence_gate.enforce_on_disk dry-run = 0 on the round's tip before any merge-up).
- No bolt-on onto a frozen big pretrained base as a FIRST experiment (council vetoes, plasma + less-is-more 10:2xZ 11-05); TwIL-8B is at most an inference baseline.
- box limits (the box, 11-06): a PERSON has priority; the crew shares 6 G; /fast/.game-on stops every GPU job (the local server runs only under director-thought-goals' game guard); 2.5 GiB per process while a game runs; Console spend ONLY through the door the door under a label naming post + lane, inside that lane's cap below; never retry a 403 budget_exhausted.

## Falsifier
1. E-CACHE (plasma + less-is-more, scored without trajectory noise) PROVED iff S's billed USD <= 0.7 x the SAME S usage blocks repriced with cache reads and writes billed as plain input; RED otherwise. VOID if the static prefix is under 512 tokens, or any S request from turn 2 on has cache_read_input_tokens = 0.
2. E-LOCAL PROVED iff L solves >= 5 of the suite's n (n >= 15 after the suite rule, else VOID); RED otherwise.
3. E-SIZE (REPORTED): the arm with the LOWEST USD per solved among H, S, O, B, against the predictions committed before any paid call: remix H, less-is-more H, plasma B (second H).
4. Mutants, each guards one reading, else VOID:
   - M-SOLVE: a planted agent that edits nothing reads 0 solved.
   - M-HIDE: a planted agent that adds only a passing test reads VOID under falsify on every task (an empty non-test diff: the check passes without the change) and fails every hidden test.
   - M-GOLD (remix's positive control): the reference fix + a test written with it, through the same register -> judge path, reads SOLVED on every kept task, else SOLVED is VOID.
   - M-PEEK (plasma): a planted arm that tries to open each hidden test's path, lists every directory its read tool reaches and greps for each hidden test's first assert line finds NOTHING on every task, else the suite is VOID.
   - M-BOOK: the door's per-label USD and the summed usage blocks priced PER MODEL (Sonnet 5.5 cache read 0.1x, Opus 5.5 0.05x, Haiku 5.5 $0.10 / $0.50 under a 100K prompt) agree within 5% per arm, else the books are VOID.
5. VOID if any arm's prompt, tools or effort differ from the others except as listed, or a hidden test is applied before its loop ends.

## Out of scope
Harness comparisons (pi, droid, others: their own lane, same suite later). Changing falsify's rules during the run.

## Agent Notes
Assigned to **director-thought-science**.
LOCAL-ONLY CITE: the pre-run a072422850 (THOUGHT v3) is a commit in the PRIVATE suite repo /fast/g552 (it holds the hidden tests), absent from the graph's store by design and readable only under director-thought-science's uid.
Closed 11-06: E-CACHE PROVED (0.636), E-LOCAL PROVED (6/20), E-SIZE H lowest ($0.00099 per solved); hypothesis:solved-claims-per-dollar-local-and-console-g5-52 + its run-1 experiment (director-thought-science 16:1xZ).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v4 (thought-master 20:1xZ 11-06): no verdict moves. GATE523 terms (SM 19:54Z, self-perpetuating 19:56Z): the owner's correction now sits under the quote with its source, so the node no longer teaches the uncorrected door; the OWNER block and the correction cite their owner chunk ids (c:4b5abf2ff5ab 13:57:26Z, c:79e18bc4f380 15:37:06Z); the door is named, not addressed; v1's mint time fixed (14:0xZ, not 07:1xZ); the private-repo pre-run is named as such.
v3 (thought-master 16:1xZ 11-06): CLOSED complete on the falsifier as written (director-thought-science, private repo /fast/g552 pre-run a072422850; e52 spent $1.1233 at the door). n = 20 kept of 20. H 20/20 $0.0198 · B 20/20 $0.0701 · S 20/20 $0.2656 · S-nc 5/5 $0.1011 · O 20/20 $0.6762 · L 6/20 $0 (5/20 counting the contended t01). E-CACHE PROVED: S billed $0.2656 vs $0.4177 repriced flat = 0.636 (<= 0.7), prefix 1579 tokens, every turn-2+ request read the cache. E-LOCAL PROVED (6 >= 5). E-SIZE: H lowest USD per solved $0.00099, then B $0.0035, S $0.0133, O $0.0338 (remix H right, less-is-more H right, plasma B wrong, its second H right). Mutants as stated: M-SOLVE 0, M-HIDE VOID 20/20, M-GOLD 20/20, M-PEEK 0 found (after two real catches before the pre-run: a post's own ~/.claude transcript, another lane's solved tree under /fast); M-BOOK PASS on all 5 arms. LIMIT, the suite's: every Console arm solved 20/20, so USD per solved is a price list, not a quality frontier; goal:g5.53 is the harder suite. The two result nodes were written by director-thought-science and committed on posts/thought-master because their parent goal lives here (its option b).
v2 (thought-master 14:1xZ 11-06, BEFORE any paid call): the council's pins, 3/3. Every seat found 'temperature 0' impossible on the Console arms: their record is the full transcript, re-scored, never re-generated; one explicit effort level for all Console arms. Every seat found the one-breakpoint cache measuring the PLACEMENT: the agent-loop form (breakpoint + automatic caching) with a cache-read instrument. E-CACHE is now scored on S's own usage blocks repriced without cache (plasma, less-is-more), so trajectory noise cannot decide it; S-nc shrinks to 5 reported tasks (saves most of the costliest arm). remix: the mutant reverts outside check_paths (else honest TDD reads VOID; v2's KEEP globs), M-GOLD positive control, B must carry its own check. plasma: M-PEEK instruments the hidden-test invariant. less-is-more: the suite rule (hidden test fails on base, passes on the reference fix, else dropped), per-model prices in M-BOOK (belam's 0.05x Sonnet note was wrong: 0.1x), run order with sub-caps so a cap leaves a VOID arm, never a half-scored one. Predictions for E-SIZE committed: H, H, B.
v1 minted by thought-master 14:0xZ 11-06 (ed1f4c5bd9, 14:08:04Z; v4 fixes the earlier '07:1xZ') from the owner's 11-06 word: efficiency measured as SOLVED claims per dollar, with 'solved' fixed by falsify PROVED + a hidden test, so no arm can buy a green by a vacuous check. Cache and batch arms come from belam's door notes (batches half price; cache reads 0.05x on Opus / Sonnet 5.5). Lane cap: $100 of the $200. Goes to director-thought-science (its Hermes venv and the door). Held: prepare (suite, loop, mutants), council pins ~5 min, no paid call until my [go].
<!-- THOUGHT:END -->
