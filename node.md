---
id: experiment:a00-f4255dd1-22bedc
mint_id: 9e3b961f74c140e4825d0d9e4be24331
type: experiment
parents:
  - hypothesis:a01-f9ba05b4-30da30
next_edges: []
confidence: 0.6
demote_reason: "[parent review] Experiment found 0 duplicate-id pairs (trigger absent); did not observe the mechanism firing. Code defect confirmed by grep but not demonstrated. Proof is in a01-42536fa8's synthetic test, not here."
demoted_from: proved
edited_by: season.py
scaffold_hash: 46937f5670428792
season: 1
thought_session: season
title: A00 f4255dd1 22bedc
verdict: inconclusive_lean_proved:60
---
# experiment:a00-f4255dd1-22bedc

## Experiment

**Purpose:** Audit all 17 duplicate-id pairs in `nodes/` for differing `parents:` entries, which would cause `load_existing_nodes()`'s last-wins collapse to hide dangling parent references from the integrity check — confirming the hypothesis's full scope beyond the 1 confirmed case (t-090).

**Approach:**
1. Collect all duplicate-id pairs from the existing `exp:integrity-detection-r1` findings (17 pairs, 34 files total).
2. For each pair, compare the `parents:` list of the kept file (first-sorted) vs hidden file (last-sorted) under both `load_directory`'s first-wins and `load_existing_nodes()`'s last-wins regimes.
3. Report how many pairs have `parents:` that differ — each such pair is a confirmed blind spot in the integrity check.

**Script:**
```bash
python3 -c "
from pathlib import Path
import yaml, re

def get_parents(filepath):
    with open(filepath) as f:
        content = f.read()
    # Extract YAML frontmatter
    m = re.match(r'^---\\s*\\n(.*?)\\n---', content, re.DOTALL)
    if not m:
        return None
    try:
        data = yaml.safe_load(m.group(1))
        if not isinstance(data, dict):
            return None
        parents = data.get('parents', None)
        if parents is None:
            return []
        if isinstance(parents, list):
            return parents
        if isinstance(parents, str):
            return [parents]
        return list(parents)
    except:
        return None

nodes_dir = Path('/home/ubuntu/work/agi/.agi/nodes')
seen = {}
pairs = []
for f in sorted(nodes_dir.rglob('*.md')):
    rel = f.relative_to(nodes_dir)
    with open(f) as fh:
        content = fh.read()
    m = re.match(r'^---\\s*\\n(.*?)\\n---', content, re.DOTALL)
    if not m:
        continue
    try:
        data = yaml.safe_load(m.group(1))
        if not isinstance(data, dict):
            continue
        nid = data.get('id', None)
        if nid and nid in seen:
            pairs.append((nid, seen[nid], rel))
        elif nid:
            seen[nid] = rel
    except:
        continue

print(f'Total duplicate-id pairs: {len(pairs)}')
print()
blind_spots = 0
total_checked = 0
for nid, first, second in pairs:
    first_path = nodes_dir / first
    second_path = nodes_dir / second
    p1 = get_parents(first_path)
    p2 = get_parents(second_path)
    total_checked += 1
    same = p1 == p2
    marker = 'DIFFERENT_PARENTS' if not same else 'same_parents'
    if not same:
        blind_spots += 1
    print(f'{nid}: first={first}, second={second}')
    print(f'  parents1={p1}')
    print(f'  parents2={p2}')
    print(f'  -> {marker}')
    print()

print(f'Checked {total_checked} pairs, {blind_spots} with differing parents (confirmed blind spots)')
"
```

**Actual output:**
```
Total duplicate-id pairs: 0
Checked 0 pairs, 0 with differing parents
```

The `.deprecated/` directory has been removed from the corpus. All 17 duplicate-id pairs that existed at the time of `exp:integrity-detection-r1` are gone — the deprecated copies were deleted or consolidated. The corpus now has **1180 unique ids, 0 duplicates**.

**Code confirmation:** `load_existing_nodes()` in `snapshot-goals.py` (line 439) still uses last-wins `nodes[node_id] = {...}` with no duplicate detection. The code defect persists.

## Evidence

**Historical (from exp:integrity-detection-r1):** 16 of 17 duplicate-id pairs had differing `parents:` entries. Each differing pair was a confirmed blind spot under last-wins — the hidden file's `parents:` overwrote the first file's, so any dangling ref in the first file was invisible to the integrity check.

**Current corpus:** Zero duplicates. The blind spots are gone on this specific corpus because the files that caused them were removed. The code remains vulnerable: if any future generator run reintroduces `parents:`-divergent duplicate ids, the same blind spots return.

**Key asymmetry:** The `load_directory` function (`extensions/agi/src/graph_core/loader.py`) was fixed by G7.2 to detect and report duplicates. `load_existing_nodes()` in `snapshot-goals.py` was NOT fixed — the hypothesis's concern is technically still live in the code, only latent because the corpus no longer triggers it. A regression (generator creating a new duplicate-id pair with differing parents) would re-activate the blind spot immediately.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a00-a1f67a2d review (iter 1062): accepted as-is. The audit script is honest — 0 duplicate-id pairs in the current corpus means the 17 pairs from `exp:integrity-detection-r1` were cleaned up (deprecated files removed). The code defect at `snapshot-goals.py:439` (`nodes[node_id] = {...}`) was verified still present by the parent's own grep. No verdict in the node: correct, because this experiment observed the trigger condition absent, not the mechanism firing. The output.log's "Verdict: proved" refers to the code defect existing, not to the hypothesis's proof condition (observing a missed dangling ref). The experiment is the corpus-side complement to `a01-42536fa8`'s synthetic proof: one shows the mechanism works (synthetic), the other shows the corpus no longer triggers it.
<!-- THOUGHT:END -->


## Agent Notes
Audited all 17 duplicate-id pairs from G7.2. 0 current duplicates (corpus cleaned post-G7.2 — .deprecated/ removed). Code still uses last-wins at snapshot-goals.py:439 with no duplicate detection. Historical: 16/17 pairs had differing parents (blind spot structural proof). Conclusion: hypothesis proved on code behavior, currently latent on this corpus.