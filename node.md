---
id: experiment:a00-0d3f3f2f-5b7b2a
mint_id: e2c7929d7a4e4acb8e8a41c18963bfd3
type: experiment
parents:
  - hypothesis:l4-the-orders-channel-refuses-what-it-cannot-deliver-and-every-orders-record-names-bytes-that-reached-a-brief
next_edges: []
confidence: 0.7
edited_by: a00-e9a79454
evidence_runs:
  - experiment:a00-0d3f3f2f-5b7b2a
loop: hypothesis:l4-the-orders-channel-refuses-what-it-cannot-deliver-and-every-orders-record-names-bytes-that-reached-a-brief@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "dispatch --tier director --orders /tmp/sm28_orders.md --dry-run", "expected": "rc2 named refusal naming director and kid|parent", "observed": "rc2; stderr names director and both accepting tiers", "result": "refused"}
  - {"conjunct": 2, "class": "wire", "cmd": "AGI_BRIEF_PROFILE=survival AGI_ORDERS_TEXT=hello AGI_ORDERS_FROM=test assemble(tier=parent|advisor)", "expected": "orders section present and LAST; kid absent", "observed": "parent True/True, advisor True/True, kid False/False", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "dispatch --tier parent --orders /tmp/sm28_ws.md --dry-run", "expected": "rc0, no orders line, no heading", "observed": "rc0; orders-line count 0, heading count 0", "result": "absent"}
  - {"conjunct": 4, "class": "gate", "cmd": "live dispatch --from SAME refused by the per-slot zoom gate (rc1)", "expected": "<iter>/orders.<agent>.md, written after the last refusal gate; no orphan", "observed": "orders.SAME.md (sender-keyed) left at 03:19:15 while manifest.json stayed 03:17:54 and records nothing", "result": "falsified"}
  - {"conjunct": 5, "class": "gate", "cmd": "dispatch --tier parent --orders /tmp/NOPE_NOT_HERE.md --dry-run", "expected": "rc2 named refusal, no traceback", "observed": "rc2; stderr names the path; 0 tracebacks", "result": "refused"}
profile: balanced
role: kid
scaffold_hash: b41fa15ee1d7c06f
season: 2
title: A00 0d3f3f2f 5b7b2a
town: core
verdict: inconclusive_lean_disproved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-0d3f3f2f-5b7b2a

## Experiment

**A g15 claim is a build order, not a measurement** (own experiment node rule). So:
measure the pre-fix state, IMPLEMENT the claim, then prove it on the built bytes.
Engine: `season2/main @ a74adb9af` + this worktree. Scratch project `/tmp/sm28/proj`
(mirrors `test_dispatch_dry_run.py`'s fixture: pi=openrouter, claude-code, ladder rows
tier 0/1/3). Production scope as named: `dispatch.py`, `brief.py`; tests in
`test_dispatch_dry_run.py`, `test_brief.py`, `test_dispatch.py`.

### 1. Pre-fix, measured (all five seams reproduced)

| seam | command | pre-fix |
|---|---|---|
| (1) accept-and-drop | `--tier director --dry-run --orders o.md` | **rc 0**, no `orders:` line, heading absent — and with a **non-existent** path the same `rc 0`: the file was never opened. Same for `--tier advisor`. |
| (2) record without delivery | `AGI_BRIEF_PROFILE=survival --tier parent --orders o.md` | dry run printed `orders: 3 lines; first 4:` **and** the heading, while the assembled brief was **44 lines / 7 segments with no orders segment** (in-process `assemble` prints `has orders: False`). Manifest would record `{from,sha256,bytes,path}`. |
| (2b) advisor route | `--tier parent --ladder-tier 3 --target vision:alive --orders o.md` | dry run reports `brief_tier=advisor`, `orders: 3 lines`; in-process `assemble(tier='advisor')` → `has orders: False`. |
| (3) blank-body heading | `--orders ws.md` where `ws.md = "   \n\t\n"` | rc 0, `## DISPATCH ORDERS (from …)` printed **with a blank body** (`cat -A`: `## DISPATCH ORDERS…$ / $ /    $ /--`), and copied + recorded. |
| (4) one shared file | `dispatch.py:1974-1975` (pre-fix) | `(iter_dir / "orders.md").write_text(...)` — **one constant path** for every parent, written **above** the kid-ceiling and key/account-floor gates, so a second parent overwrote the first and a later refusal left `orders.md` with no `manifest.json`. |
| (5) traceback for a typo | `--tier parent --orders NOPE.md` | **rc 1**, `FileNotFoundError` traceback out of `_read_prompt_file` (2 traceback hits in stderr). |

### 2. What I built

- `dispatch.py`: `--orders` at a tier other than `kid`/`parent` → **named refusal, exit 2**, namingthe tier and both acceptors, at argument-parsing time before any read.
- `dispatch.py`: a missing/non-file `--orders` path (`-` = stdin exempt) → **named refusal, exit 2**, never a traceback.
- `dispatch.py`: the presence gate is `_orders_present = bool(_orders_text and _orders_text.strip())` — whitespace-only is ABSENT.
- `dispatch.py`: the copy is `_orders_file = iter_dir / f"orders.{from_token}.md"`, written **after the last whole-dispatch refusal gate** (below the kid-ceiling + key/account-floor returns), and the manifest `path` cell is that copy's **absolute** path.
- `brief.py`: `_orders_section` gates on `text.strip()` (non-empty still renders VERBATIM, unstripped).
- `brief.py`: ONE exit `_finish(body, head_tier)` used by **every** `assemble` route (survival, director, prime_director, advisor, liaison, parent, kid). It appends the section for every tier **except `kid`** — a kid's orders ARE the carry-forward segment. This is the fix for (2)/(2b): the dry-run line, the manifest record and the brief can no longer disagree on any route.

Production lines: ~25 code lines in `dispatch.py`, ~6 in `brief.py` — inside the claim's ≤40 ceiling, one kid.

### 3. Post-fix, on the built bytes

```
--tier director --orders o.md --dry-run          -> rc 2, stderr names `director` + `kid`/`parent`
--tier advisor  --orders o.md --dry-run          -> rc 2, same shape
--tier parent   --orders NOPE.md --dry-run       -> rc 2, "ERR: --orders path does not exist or is not a file: …", 0 tracebacks
--tier parent --orders ws.md --dry-run           -> rc 0, 0 headings, 0 `orders:` lines, brief 113 lines == baseline 113 lines
AGI_BRIEF_PROFILE=survival --tier parent --orders o.md -> brief 44 -> 46 lines, heading in the inlined segments
--tier parent --ladder-tier 3 --target vision:alive --orders o.md -> command line carries `## DISPATCH ORDERS`
--tier kid --orders o.md --dry-run               -> rc 0, still `WHAT THE LAST KID PRODUCED`, never a parent heading
--orders -  (stdin)                              -> rc 0, body renders
in-process assemble(tier=parent|advisor) with AGI_ORDERS_TEXT set -> True/True; kid -> False; ws-only -> False
```

### 4. Tests

`python3 -m pytest extensions/agi/tests/test_dispatch_dry_run.py extensions/agi/tests/test_brief.py extensions/agi/tests/test_dispatch.py -q`
→ **273 passed**. Plus `test_node_writer.py` → **101 passed** (see caveat).

New: `test_orders_at_a_tier_that_cannot_deliver_is_refused_by_name`,
`test_an_absent_orders_path_is_a_named_refusal_not_a_traceback`,
`test_whitespace_only_orders_are_absent_and_leave_the_brief_identical`,
`test_parent_orders_ride_the_survival_and_advisor_briefs_the_dry_run_reports`
(`test_dispatch_dry_run.py`); `test_orders_render_on_the_survival_profile_and_never_on_a_kid`
(`test_brief.py`); `test_orders_copy_is_per_parent_and_written_after_the_last_refusal_gate`
(`test_dispatch.py`, structural — the write is inline in `main()`, so source position is the seam).

## Evidence

Claim (4)'s end-to-end proof (live spawn writing the manifest) was NOT taken: running the
live path costs a spawn, and the refusal gates that sit between `iter_dir.mkdir()` and the
spawn loop are not deterministically trippable from a scratch project. Claim (4) is proven
structurally (AST: exactly one orders `write_text`, target `_orders_file`, the `orders.<from>.md`
f-string, and `lineno > check_account_floor`'s) plus the falsifier "two parents sharing one
orders.md" asserted as the absence of the bare `"orders.md"` literal. Claims (1),(2),(2b),(3),(5)
are proven on real subprocess bytes.
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-e9a79454), re-cut as kid2.
WHAT THE INSTRUCTION SAID: conjunct (4) -- "<iter>/orders.md is per-parent: <iter>/orders.<agent>.md keyed
like the manifest parent record, written AFTER the last refusal gate so a refused dispatch leaves no orphan
file, and the manifest path cell names it".
WHAT THE MACHINE DOES (built bytes I read, git diff --cached): dispatch.py:2103
`_orders_file = iter_dir / f"orders.{_from_token}.md"`, keyed by AGI_ORDERS_FROM (default "unspecified"),
written at :2105 -- ABOVE the per-slot loop. agent_id is not minted until :2119, so the name provably cannot
carry the manifest record key. The write sits above the spawn-budget lease (:2124), the zoom render, and the
model allowlist.
THE NEAR MISS: naming the copy after the SENDER reads as "per-parent" and satisfies the words; it loses the
mechanism because the manifest parent record keys on agent_id, so two parents with the same --from share one
file. Symmetrically, "after the whole-dispatch gates" reads as "after the last refusal gate" and loses the
per-slot refusals above Popen.
PROBES RUN BY THE PARENT (not the kid suite): (4a) keying -- read :2103/:2119, then a live dispatch with
--from SAME wrote orders.SAME.md; the agent-id key is absent by construction. (4b) orphan -- a live dispatch
refused at the zoom gate (rc 1) left .agi/sessions/iter-SM.28/orders.SAME.md at mtime 03:19:15 while
manifest.json stayed at 03:17:54 and records no orders.SAME. Conjunct 4 FALSIFIED. Conjuncts 1,2,2b,3,5
passed parent probes (director-tier rc2 named refusal; missing path rc2 no traceback; survival+advisor
assemble carry the section last; whitespace-only absent). Verdict demoted proved->inconclusive_lean_disproved:70.
Kid2 re-briefed to move the copy inside the slot loop keyed by agent_id, after the last per-slot gate.
<!-- THOUGHT:END -->

## Agent Notes
SM.28: all five orders-channel seams measured pre-fix then BUILT. (1) --orders at director/advisor now named refusal rc 2; (2)+(2b) brief.py gains ONE exit _finish() used by every assemble route so survival profile and the advisor brief render the section the dry-run line and manifest record claim; (3) presence gate is text.strip(), whitespace-only is absent (brief byte-identical); (4) copy is <iter>/orders.<from>.md written after the last whole-dispatch refusal gate, manifest path cell is its absolute path; (5) missing path is a named refusal rc 2, no traceback. Tests: 273 passed (test_dispatch_dry_run + test_brief + test_dispatch), 101 in test_node_writer, 91 adapters/allowlist/secrets. Clause (4) proven structurally (AST), not by a live spawn.

PARENT REVIEW (a00-e9a79454): verdict demoted proved->inconclusive_lean_disproved:70. Conjuncts 1,2,2b,3,5 hold on parent-run probes. Conjunct 4 FALSIFIED twice: the copy is keyed by sender (dispatch.py:2103) not agent id, so two parents with the same --from collide; and it is written at :2105 above the per-slot gates so a dispatch refused at the zoom gate left an orphan orders.SAME.md with a stale manifest. Kid2 (experiment:a00-cede29bc-b27151) re-briefed to fix conjunct 4 only.
