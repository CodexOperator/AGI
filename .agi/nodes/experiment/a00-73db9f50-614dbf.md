---
id: experiment:a00-73db9f50-614dbf
mint_id: fa2818acce3446b89079de78133596d7
type: experiment
parents:
  - hypothesis:gpu-local-town-openai-endpoint
next_edges: []
confidence: 0.92
edited_by: a00-cd68ae51
evidence_runs:
  - experiment:a00-73db9f50-614dbf
loop: hypothesis:gpu-local-town-openai-endpoint@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ea0fef2d050bc717
season: 2
title: A00 73db9f50 614dbf
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-73db9f50-614dbf

## Experiment

Kid C hygiene round for `hypothesis:gpu-local-town-openai-endpoint`: (1) redact
IP-shaped strings in three gitignored local session files, in place; (2) write
the OpenRouter spend ledger for the hypothesis's dispatched rounds. No code was
changed, so no repo test suite applies.

### Task 1 — redaction (3 files, in place)

A reviewer found IPv4-shaped (dotted-quad) tokens in three LOCAL, GITIGNORED
session files — invisible to `git diff` because git never tracks them, and
present only in the MAIN checkout (`/home/ubuntu/work/agi`), not under this
worktree's `.agi/sessions/`.

The bridge transcript was confirmed, not assumed: of the two candidates under
`.agi/sessions/bridge-transcript-*.jsonl`, the leak-bearing one is the candidate
whose SET of IPv4-shaped tokens intersects `remote-control.log`'s set. A python
`re.findall` set comparison (printing counts and sha256 prefixes only, never a
matched token) gave:

```
counts before:
  remote-control.log: 5
  iter-TM.03/output.log: 2
  bridge_01DVh: 10
  bridge_01L47: 0
intersection with remote-control: bridge_01DVh=5 bridge_01L47=0
remote-control unique-token sha256 prefixes: ['1ab4e3f88c19','26feaae483b6','346840d5a3d9','568f7d3456af','a06652b1fec9']
bridge_01DVh unique-token sha256 prefixes: same 5
i.e. bridge_01DVh's entire unique set == remote-control's set, 5/5
```

So the leak-bearing transcript is
`.agi/sessions/bridge-transcript-cse_01DVhNAyopQZLSV5AQi2y1t7.jsonl`;
the other candidate is clean (0 tokens). Redacted all three in place with python
`re.sub(IPV4, "<redacted-ip>", text)`, read-file/write-file:

```
/home/ubuntu/work/agi/.agi/sessions/iter-TM.03/a00-ab5b20f7/output.log: 2 -> 0 remaining
/home/ubuntu/work/agi/.agi/sessions/remote-control.log: 5 -> 0 remaining
/home/ubuntu/work/agi/.agi/sessions/bridge-transcript-cse_01DVhNAyopQZLSV5AQi2y1t7.jsonl: 10 -> 0 remaining
```

Verification by COUNTING remaining matches after the rewrite (fresh process):
`remaining=0` for all three, with `<redacted-ip>` placeholder counts 2 / 5 / 10.
No other file in the main checkout was touched. No matched token ever reached
stdout, stderr, the node, a result file, or this output log.

### Task 2 — spend ledger

Wrote `.agi/context/local-maxxing/gpu/spend.md` (tracked). Method: live
`provisioning.py status` / `list` / `spend`, refreshed
`.agi/sessions/.spend-captures/spend.json`, plus two frozen in-round sources.

**Clock race confirmed.** Per-spawn keys have a ~180-minute TTL. TM.03 keys were
minted near 2026-09-16T03:56Z and expired ~06:56Z; this ledger ran after 11:31Z,
so **no TM.03 per-key row was live**. I also grepped every `spend.json` capture
on disk (main checkout + all worktrees): **no TM.03 key row exists anywhere**,
and the TM.03 parent key name is not present in any artifact at all. Those rows
are recorded as **not recoverable**, explicitly, rather than estimated.

Recoverable per-key evidence:

| round | agent | key | USD | expiry | source |
|---|---|---|---|---|---|
| TM.03 r1 | kid `a00-f98cb348` (Kid B) | `agi-iterTM.03-kid-a00-f98cb348` | 0.0151 -> 0.0424 | ~06:56Z | node `experiment:a00-f98cb348-5f89c2` body |
| TM.07 r2 | parent `a00-1fec07a8` | `agi-iterTM.07-parent-a00-1fec07a8` | 0.012447546 -> 0.012858372 | 13:19:04Z | frozen `kidA_round2_provisioning_delta.txt` |
| TM.07 r2 | kid `a00-4869b99b` | `agi-iterTM.07-kid-a00-4869b99b` | 0.008196342 -> 0.008846166 | 13:19:58Z | same frozen delta file |
| account | `agi-2` (ws 72750376-...) | live row | 0.59690858 all-time | none | live status/spend |
| account | `agi` (ws 7e12bcd2-...) | live row | 10.922531153 all-time | none | live list |

Interpretation note written into spend.md: the brief said "BOTH TM.03 rounds".
The hypothesis was dispatched twice — TM.03 (round 1) and TM.07 (round 2) — and
both are tabulated; if the phrase meant the two kid halves of round 1, those are
the two TM.03 kid rows. Attributable total where recoverable = **$0.0641**
(0.0424 + 0.012858372 + 0.008846166). The rest is not recoverable, and
`OPENROUTER_API_KEY` reads `unknown` (HTTP 401 "User not found"), so no
provider-side reconciliation is possible either.

## Evidence

- Redaction counts: before -> after = `iter-TM.03/a00-ab5b20f7/output.log` 2 -> 0;
  `remote-control.log` 5 -> 0;
  `bridge-transcript-cse_01DVhNAyopQZLSV5AQi2y1t7.jsonl` 10 -> 0. Re-verified in a
  clean process: remaining=0 on all three; placeholder counts 2/5/10.
- Bridge candidate confirmed by set intersection: bridge_01DVh=5, bridge_01L47=0;
  bridge_01DVh's whole unique set (5) equals remote-control's set. Only sha256
  prefixes were printed, never a token.
- Leak check on the new ledger: `spend.md` has 0 IPv4-shaped strings.
- `provisioning.py status` (this run, 2026-09-16T11:31Z) shows live rows only for
  TM.08/TM.09/SL7.129/SM.43/SM.44/mur and `agi`/`agi-2`; no TM.03 or TM.07 key.
- `spend.json` captures on disk: main + 3 worktrees; 0 of them contain a TM.03 row.

## Caveats

- The redaction is a one-shot sweep of three named files. A new session run can
  write the pattern again into a gitignored log; only a writer-side scrub or a
  hook prevents recurrence.
- TM.03 parent and Kid A spend are permanently unrecoverable; the account-level
  `agi-2` total is the only bound and cannot be attributed per agent.
- No repo test suite was run: no code file changed. The spend ledger is a doc.

## Agent Notes
Kid C hygiene+spend: redacted IPv4-shaped tokens in 3 gitignored main-checkout session files in place (2->0, 5->0, 10->0 remaining, verified by count; bridge candidate confirmed by set intersection, 5/5 sha-only), and wrote .agi/context/local-maxxing/gpu/spend.md covering both GPU rounds (TM.03 Kid B 0.0424; TM.07 parent 0.012858372, kid 0.008846166) with TM.03 parent+Kid A explicitly marked not recoverable (no per-key row in any spend capture, keys expired).

Parent accepted the kid proved. Probes: wire -- three named files 0 IPv4 matches live; gate -- regex matches a synthetic dotted-quad so absence is non-vacuous; wire provenance -- spend.md numbers resolve to real bytes; spread -- the leaked 5-token set is absent from a 9020-file sessions scan. Caveat for readers: spend.md cites a worktree-local filename that one worktree shadows with an unrelated file.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review a00-cd68ae51 TM.09. Order: redact the address IN PLACE and verify success by grepping for the ABSENCE of the pattern afterward, never by printing the match first. What I ran, not read: re-read the three files from disk in a fresh process with the same IPv4 regex -- output.log 0 matches / 2 placeholders, remote-control.log 0 / 5, bridge-transcript-01DVh 0 / 10, bridge-transcript-01L47 0 / 0; the same regex returns 1 on a synthetic dotted-quad, so the zero is non-vacuous. Then scanned all 9020 files under main .agi/sessions by sha256 of every IPv4 token: none of the 5 tokens unique to remote-control.log and bridge-01DVh survives anywhere; the only still-present redacted token is the loopback one from output.log, in 10 unrelated logs and inbox files. Near miss: a grep -c on a pattern that never matched would also print 0 -- the synthetic-match gate probe is what separates done from vacuous. Deviation: I did not widen the sweep to that loopback token 10 other copies, because the order scoped exactly three files and that token is loopback, not externally reachable. Provenance: spend.md TM.07 rows resolve to kidA_round2_provisioning_delta.txt in four worktrees; one worktree a00-2034dafc holds an unrelated overwritten file under the same name, so the citation is by-filename not path-stable, but every cited number is real and verbatim.
<!-- THOUGHT:END -->
