---
id: hypothesis:s28-manifest-merge
mint_id: 663d6a55377a4d31ba4ec21bed8cf4b3
type: hypothesis
parents:
  - goal:s28
confidence: 0.9
evidence_runs: 0
title: S28 manifest merge
verdict: pending
---
# hypothesis:s28-manifest-merge

## Hypothesis

**Claim:** `dispatch.py` can union its agents into an existing
`manifest.json` keyed by agent id, atomically, and that restores `post_wire`'s
parent-admission path without changing single-dispatch behaviour.

Grounding, measured 2026-09-02: `dispatch.py:329` does
`(iter_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))` — a
wholesale write built when one dispatch owned an iteration. A parent shelling
out to `dispatch.py --tier kid` is a *second* dispatch into the same iteration
directory, so the second write clobbers the first. After one parent + one kid
the manifest read `['a00-f0fd9669/kid']`; the parent was gone.

**What would prove it:** (1) a parent plus two kids leaves three agents in the
manifest with the parent's `tier: parent` entry intact; (2) `post_wire`'s
`owns_all_complete` branch actually executes and admits the parent — today it
cannot, since `post_wire` iterates `manifest["agents"]`; (3) a single dispatch
into a fresh iteration produces a byte-identical manifest to the current
behaviour; (4) re-dispatching the same agent id updates its entry rather than
appending a duplicate.

**What would disprove it:** if merging cannot be made safe against two
dispatches racing — a parent spawning kids while another write is in flight —
then a merge is not sufficient and the manifest needs a different ownership
model (per-agent files, or a lock). Temp-file-plus-rename is the intended
mechanism; losing an entry under concurrency falsifies it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by the director rather than by a kid, because `goal:s28` already states
the claim and the fix, and spending a kid round to restate them would be motion
without work. The kid's job is the experiment: implement the merge and measure
the four predictions, one of which — that the `owns_all_complete` branch runs at
all — is currently unobservable and is the whole point.

Confidence 0.9 rather than higher because prediction 4 and the concurrency
disproof clause are genuinely open. The merge itself is close to certain; that a
temp-file rename is sufficient against two dispatches racing is not, and that is
`goal:g4.1` arriving one tier up.
<!-- THOUGHT:END -->