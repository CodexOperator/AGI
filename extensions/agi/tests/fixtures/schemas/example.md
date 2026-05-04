---
fields:
  evidence_runs:
    type: list
  verdict:
    type: string
    enum:
    - proved
    - disproved
    - inconclusive_lean_proved
    - inconclusive_lean_disproved
    - pending
name: experiment
---

The experiment schema defines what fields experiment nodes carry.
