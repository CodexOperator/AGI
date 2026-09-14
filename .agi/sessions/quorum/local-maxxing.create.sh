#!/usr/bin/env bash
# town:local-maxxing seed — Prime-run (schema written_by [prime_director, owner]; the SM's mint was refused BY NAME, goal:g12, 00:5xZ).
# Order matters: the charter vision FIRST (towns._resolve_visions refuses a dangling vision id by name), then the town.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
W=extensions/agi/bin/write.py
python3 $W create vision local-maxxing --parent moral:faith --parent moral:antifragility --parent moral:beauty \
  --set 'title=The local-maxxing town — the smallest, fastest, most open model that can do each job, everywhere it can be done, with the graph itself deciding which model that is (owner 2026-09-04, verbatim in goal:g14); a very slow, gentle research loop on the recurrent looped transformer + the g14 treasury, run by the thought master (owner 23:32Z, doc:l4-owner-decisions)' \
  --set 'tags=["local-maxxing","town","charter"]' --set town=local-maxxing --set season=1 --set core=false \
  --set 'proposes_goals=["goal:g14.2","goal:g14.3"]' --set status=open --actor belam --role prime_director
python3 $W vision:local-maxxing 'note CHARTER, vision 1 of 3 for town:local-maxxing (Prime XX seating order 00:48Z; drafted by the Sanctuary Master, minted by the Prime — the schema admits only owner/prime). Owner text is the source, never paraphrased into a claim: goal:g14 body line 29 (2026-09-04, local-maxxing, verbatim) and doc:l4-owner-decisions tail (2026-09-13 23:32Z: slow gentle research loop, recurrent looped transformer, [region] secrets hub, encryption town later). Visions 2 and 3 follow under goal:g14.2 on the owner or Prime word. The thought master (goal:g14.3) reads the paper itself — nobody summarizes it from memory.' --actor belam --role prime_director
python3 $W create town local-maxxing --parent ladder:ladder --set 'visions=["vision:local-maxxing"]' --set council=council-local-maxxing --set season=1 --actor belam --role prime_director
python3 - <<'PY'
import sys; sys.path.insert(0,'extensions/agi/bin'); import towns
from pathlib import Path
print([(t.slug, sorted(t.visions), t.council, t.season) for t in towns.load_towns(Path('.'))])
PY
git add .agi/nodes/vision/local-maxxing.md .agi/nodes/town/local-maxxing.md
