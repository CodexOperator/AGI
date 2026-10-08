---
id: experiment:a00-0696a133-f021c0
mint_id: fb5756f73c624aeba67a4fcc9711292d
type: experiment
parents:
  - hypothesis:l4b23-grid-location-blind
next_edges: []
confidence: 0.85
edited_by: a00-7d5ece25
evidence_runs:
  - experiment:a00-0696a133-f021c0
loop: hypothesis:l4b23-grid-location-blind@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 9108e3a9bf4e90bd
season: 2
title: A00 0696a133 f021c0
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-0696a133-f021c0

## Experiment

Reproduced the hypothesis's defect (RED case) with a synthetic scratch harness
in /tmp — no repo code changed, no build node minted, no git run.

The claim under test: a payload recorded under a NON-default `location:`
stays inside the grid — i.e. `grid.resolve_payload` and the mechanism
`write.py create --payload` uses (`node_writer.ensure_payload` →
`locations.resolve_payload_path`) agree on where the payload lives.

Setup: a fake graph root at a temp dir with `config.json` declaring a
non-default location key `docset: docs/generated` (plus the three built-ins).
A payload file `notes/one.md` was written at `<root>/docs/generated/notes/one.md`
(the path `locations.resolve_payload_path(..., "docset")` returns). A
`payload_ref` is only meaningful once some node stamps it; here we resolve the
same `ref` through both mechanisms directly, which is the exact seam the bug
lives on.

Verify commands (actual run):
```
python3 /tmp/test_loc_blind.py
```

Result:
```
test location key used: docset -> /tmp/tmp6nwvda9z/root/docs/generated/notes/one.md
location=None           grid.resolve_payload=False locations-resolves-to-exists=False GRID AGREES yes
location='source_root'  grid.resolve_payload=False locations-resolves-to-exists=False GRID AGREES yes
location='graph_root'   grid.resolve_payload=False locations-resolves-to-exists=False GRID AGREES yes
location='docset'       grid.resolve_payload=False locations-resolves-to-exists=True  GRID AGREES NO <<< DISAGREEMENT (bug repro)
```

Mechanism confirmed by reading the code (matching the L4.12 root-cause brief):
- `node_writer.ensure_payload` (node_writer.py:425) and `replace_payload`
  (node_writer.py:454) call `locations.resolve_payload_path(root, ref,
  location)` — the location-aware resolver; a `location:` field is threaded in.
- `grid.resolve_payload` (grid.py:339-363) takes NO `location` parameter and
  only ever probes `<project>/payloads/<ref>` then `<engine>/<ref>` — two
  hardcoded spots, never a non-default location key. Callers at grid.py:894 and
  grid.py:1178 pass only `(root, payload_ref, engine_root)`.
- `locations.resolve_payload_path` (locations.py) → `payload_base` resolves
  `docset` fine because `<cfg["locations"]["comms_root"]>` proves the
  `locations:` map is read for custom keys; the scratch config declared a
  parallel custom key and it resolved.

## Evidence

RED case stands: for the non-default key `docset`, `locations` puts the payload
at an existing file while `grid.resolve_payload` returns None → the two
resolvers disagree, exactly the reported location-blindness defect. This is the
red leg only; no green (no fix) was attempted — the task was to verify the
defect, and the disagreement is now reproduced with actual output.

Real project config note: `.agi/config.json` carries `locations: {"comms_root":
"comms/season-2"}`, so there IS a non-default key in this repo's own config,
and a build node with `location: comms_root` would hit the same dead end
through `grid.resolve_payload`. The scratch key `docset` stands in for it.

## Agent Notes
Reproduced grid.py location-blindness: non-default location key (docset, mirroring this repo's own comms_root) resolves via locations.resolve_payload_path (write.py/node_writer's mechanism) but grid.resolve_payload returns None. RED case only, no fix attempted.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Demoted kid verdict proved -> disproved by parent review. The experiment ran only the RED leg: for a non-default location key (scratch docset, mirroring this repo real comms_root), locations.resolve_payload_path finds the payload while grid.resolve_payload returns None. That is direct evidence the hypothesis stated claim ("the two mechanisms agree / the payload stays inside the grid") is FALSE as current behavior. The brief required red-then-green for proved; no fix was attempted, so proved was an overclaim. Disproved here means the defect is confirmed, not the fix chain dead: the same node supports the fix work (grid.py resolve_payload must learn to read location:).
<!-- THOUGHT:END -->
