#!/usr/bin/env bash
# town:sanctuary seed — Prime-run (schema written_by [prime_director, owner]; town and vision are prime/owner minted, goal:g12).
# Order matters: the charter vision FIRST (towns._resolve_visions refuses a dangling vision id by name), then the town — whose `council` cell names the council-sanctuary row in config:posts (that row is a prime-run posts write, not a node mint).
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
W=extensions/agi/bin/write.py
python3 $W create vision sanctuary --parent moral:faith --parent moral:love --parent moral:beauty \
  --set 'title=The sanctuary town — the original town: the seat protocol, the formations, and the constitutions that hold every other town, overseen by the Sanctuary Master and the Master Sensei (owner 2026-09-14 01:06Z, verbatim in doc:l4-owner-decisions L773-775)' \
  --set 'tags=["sanctuary","town","charter"]' --set town=sanctuary --set season=1 --set core=false \
  --set 'proposes_goals=["goal:g15.25","goal:g15"]' --set status=open --actor belam --role prime_director
python3 $W vision:sanctuary 'note CHARTER, vision 1 of 3 for town:sanctuary (owner ruling 2026-09-14 01:06Z; minted by the Prime — the schema admits only owner/prime). Owner text is the source, never paraphrased into a claim: doc:l4-owner-decisions 01:06Z (sanctuary needs its own town, it is the original town; Core is just graph-function code and most config; Sanctuary town is overseen by Sanctuary Master and Master Sensei) with the formations saved under goal:g15. Visions 2 and 3 follow on the owner or Prime word.' --actor belam --role prime_director
python3 $W create town sanctuary --parent ladder:ladder --set 'visions=["vision:sanctuary"]' --set council=council-sanctuary --set season=1 --actor belam --role prime_director
python3 - <<'PY'
import sys; sys.path.insert(0,'extensions/agi/bin'); import towns
from pathlib import Path
print([(t.slug, sorted(t.visions), t.council, t.season) for t in towns.load_towns(Path('.'))])
PY
git add .agi/nodes/vision/sanctuary.md .agi/nodes/town/sanctuary.md
