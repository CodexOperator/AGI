---
id: config:formations
mint_id: 97a8741002184f63be6a0b05856aab85
type: config
parents:
  - goal:g7.16
next_edges: []
active: doc:council-loop
locations: {}
scaffold_hash: 71df4e5fd8e3ff79
templates:
  doc:council-loop: g7.16.1
  doc:l4-formation-2-texas-two-step: g7.16.2
  doc:formation-local-town: ""
  doc:l4-formation-1-prime-only: ""
  doc:l4-formation-3-hybrid-gradual-expansion: ""
  doc:l4-formation-4-full-activation: ""
---
# config:formations

The run-mode switch (goal:g7.16). `active` = ONE formation template; `templates` = template -> the goal it serves.
Switch: write.py config:formations 'set active doc:<id>'. Read-back: verification.py `formation` check (rotation, full).
