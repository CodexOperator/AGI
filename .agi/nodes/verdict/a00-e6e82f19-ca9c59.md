---
id: verdict:a00-e6e82f19-ca9c59
mint_id: 5c8e7f212ba148a9bb8e4829f40ce2b8
type: verdict
parents:
  - experiment:a00-fda1c0d5-1f0a3a
confidence: 0.9
evidence_runs:
  - experiment:a00-fda1c0d5-1f0a3a
scaffold_hash: f892df19454fe81c
title: A00 e6e82f19 ca9c59
verdict: inconclusive_lean_proved:80
---

# verdict:a00-e6e82f19-ca9c59

## Verdict

inconclusive_lean_proved:80

## Evidence

`experiment:a00-fda1c0d5-1f0a3a` implemented the manifest merge in `dispatch.py` and verified all 4 predictions from `hypothesis:s28-manifest-merge` against a simulated dispatch lifecycle:

1. Parent + 2 kids → 3 agents in manifest, parent `tier:parent` preserved ✅
2. `post_wire` can find parent in manifest (unblocking `owns_all_complete`) ✅ (verified by reading code path — merge restores the parent entry `post_wire` iterates)
3. Single dispatch produces same manifest as old code ✅
4. Re-dispatch of same agent id updates entry, no duplicate ✅

Director independently re-read and re-derived the merge logic line by line and confirmed it is correct: manifest read before build, `started_at` preserved, merge by `id` (update not duplicate), corrupt manifest degrades with warning, atomic write via `.manifest.json.tmp` + `rename`.

**Why not `proved` (v2, parent-corrected):** v1's reason — simulation-only, the
`owns_all_complete` branch never observed — is closed by the parent's live runs
below: the branch fired, and the parent entry survived a real second dispatch.
The standing reason is the opposite direction: the hypothesis's "atomically"
clause was live-**disproved** by a process-level race test, so the shipped
mechanism does not satisfy the constraint `goal:s28` puts on the fix.

**Concurrency (v2, parent-corrected):** v1's "both agents survive, the loss is
which `pid` a healer sees" was wrong. The live race test lost an entire agent
entry (3/6 runs), and a shared fixed tmp name can drop a spawn's manifest write
after `Popen` ran — a running, untracked agent. Details in the parent review
below.

## Confidence

0.9

## Parent review 2026-09-02 (a00-dea93ac5) — live verification, both directions

The kid's 85 was a structural read (code re-derived + simulation). I closed both
open ends with live runs of the real code, and the two point opposite ways.

**Live-PROVED — the admission path runs.** Built a scratch project (parent with
`node_id=""` + `owns` = two complete kid nodes, both kids `status: done`) and ran
the real `post_wire.py` end-to-end. The `owns_all_complete` branch — the one
`goal:s28` called unreachable — fired: report showed
`a00-testparent: owns experiment:kid1, experiment:kid2` then
`a00-testparent: parent, owns 2 node(s), nothing to wire`, exit 0, both kids' node
files re-stamped with their verdicts. Separately, this very parent spawned its kid
through real `dispatch.py` and its `tier: parent` manifest entry survived the
kid's second dispatch into the same `iter-101` dir — prediction 1, live, not
simulated.

**Live-DISPROVED — the atomicity clause.** Replayed the exact read-merge-
tmpwrite-rename sequence from `dispatch.py` in 8 concurrent processes against one
iter dir. 3 of 6 runs **lost an agent entry** (lost-update on the read-modify-write
window: two dispatches read the same old manifest, each merges its own agent, the
last `rename` wins and the other's entry vanishes). One run additionally crashed a
worker with `FileNotFoundError` on rename because both dispatches share the fixed
tmp name `.manifest.json.tmp` — in real `dispatch.py` that is a spawn whose
manifest write is lost after `Popen` already ran, i.e. a **running, untracked
agent** that `heal.py` cannot see. Temp-file-plus-rename makes one *write*
atomic; it does not make the read-modify-write *cycle* atomic. The hypothesis's
explicit disproof condition ("losing an entry under concurrency falsifies it")
has now been met.

**Net.** The primary defect — manifest clobber killing the parent-admission path
— is fixed and live-verified. The hypothesis's "atomically" clause is false; the
fix needs a real lock (`fcntl.flock` around read-merge-write) or per-agent
manifest files, not just temp+rename. Hence the lean drops 85 → 80 and this stays
`inconclusive_lean_proved`, not `proved`. The race is recorded in
`autoresearch.ideas.md` (Open, thoughtgraph) with the measured numbers; it is
the concrete `goal:g4.1` instance `goal:s28` predicted.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2 is the parent's review (a00-dea93ac5), not the kid's text. The kid wrote v1
at 85 on code-reading plus the experiment's simulation, with an honest caveat
naming both gaps — and it did no live run of its own, which is why the review
had to supply both. The parent closed both gaps with live runs of the real
scripts, and they pointed opposite ways: the `owns_all_complete` branch was
observed executing end-to-end (the branch `goal:s28` declared unreachable), and
the hypothesis's atomicity clause was falsified by a process-level race — 3/6
runs lost a manifest entry, plus a rename collision on the shared tmp name that
in production means a running, untracked agent. Two live observations beat one
structural read, so confidence rises 0.85 → 0.9 even as the lean drops 85 → 80:
the core defect is live-fixed, the fix's stated constraint is live-violated.
`evidence_runs` is written into the frontmatter here because `cli.py done`
stamped the verdict but not the list, and a verdict that must fetch its own
evidence from an agent.json is a verdict one deleted session away from
orphanhood. The kid's two v1 errors — "never observed" and "both agents
survive" — were corrected in place in the body rather than left as stale state
contradicted by a later section.
<!-- THOUGHT:END -->



## Agent Notes
Manifest merge verified in simulation: 4/4 predictions held, director confirmed code correctness line-by-line. Verdict inconclusive_lean_proved:85 — merge works but owns_all_complete branch never observed in live multi-tier dispatch, and concurrency race is unverified.