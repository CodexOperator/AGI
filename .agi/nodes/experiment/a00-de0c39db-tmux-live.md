---
id: experiment:a00-de0c39db-tmux-live
mint_id: 43c4538ac51a4b84a08b8c24385212fd
type: experiment
parents:
  - hypothesis:a00-de0c39db-59b16e
---

# Real tmux path and environment probe

Implemented the log path handoff and ran `python3 -m pytest extensions/agi/tests/test_tmux_hold.py -q`: 6 passed. The installed tmux test executed initial and replacement pane children, observed HARNESS_MARKER values, and cleaned its private server.
