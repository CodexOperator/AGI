---
id: hypothesis:l3-scaffold-stamps-spawner-env
mint_id: 8ed238fecddf433d99a84070e52d49ba
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l3w0-ladder-roles-table
next_edges: []
edited_by: a00-4ad19971
loop: goal:g15@s2
model: claude-fable-5-1
profile: balanced
role: director
scaffold_hash: 83c0d2af3d79df8c
season: 2
testable_claim: "node_writer.py reads loop/model/profile/role from os.environ at scaffold time (AGI_LOOP, AGI_MODEL, AGI_PROFILE, AGI_ROLE), while dispatch.py computes the correct values only into the child spawn_env. So a node scaffolded by a dispatching agent carries that agent identity: the g15 director scaffold hypothesis:a00-4ad19971-1d668e was born role=parent model=claude-opus-5 loop=vision:alive@s2 (the advisor), and every kid a parent spawns is born role=parent model=glm. Proved by a test that scaffolds under a foreign AGI_ROLE and asserts the row values on the node; disproved if the stamps already come from the resolved row."
thought_session: iter-L3.14
title: A scaffolded node is stamped with the SPAWNER role, model and loop, not the spawned agent row
---
# hypothesis:l3-scaffold-stamps-spawner-env

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
Second live witness, one tier down, 2026-09-07 05:02 UTC: outcome:a00-a4a9db7e-ec4e27 was written by DeepSeek kid a00-a4a9db7e and is stamped role=parent model=~z-ai/glm-flash-latest loop=mvp:the-corpus-becomes-schema-valid@s2 — the GLM parent that ran dispatch.py. Sibling defect, same family (identity at write time): the parent review on that node is stamped edited_by=ubuntu because dispatch.py exports no AGI_AGENT_ID and write.py defaults --actor to the OS user; the all-is-one advisor found the missing export independently (idea:declared-differentiation, finding C). One fix could cover both: dispatch exports AGI_AGENT_ID, node_writer stamps from the resolved row it is handed rather than from os.environ, write.py defaults --actor to AGI_AGENT_ID.
