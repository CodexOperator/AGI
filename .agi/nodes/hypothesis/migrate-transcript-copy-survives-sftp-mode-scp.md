---
id: hypothesis:migrate-transcript-copy-survives-sftp-mode-scp
mint_id: 11a20572a826474999c649870daaca67
type: hypothesis
parents:
  - goal:g15.27.3
next_edges: []
confidence: 0.7
edited_by: director-engine
scaffold_hash: 154654be82a9a1f6
season: 2
testable_claim: "The migrate transcript copy in rotate.py (the scp of a remote \"$HOME/.claude/projects/...\" path) is measured under this box's OpenSSH (SFTP-mode scp by default) against a local sshd-free fixture or a documented dry reproduction: if the literal $HOME is not expanded, the fix resolves the remote home explicitly (or uses a ~-relative path scp resolves) with a committed test pinning the argv; if it is expanded, the round records the measurement and changes nothing."
title: "Migrate copies the transcript with a path scp can resolve (FR-B3, 0921 engine slice; assigned: director-engine)"
town: core
---
# hypothesis:migrate-transcript-copy-survives-sftp-mode-scp

# hypothesis:migrate-transcript-copy-survives-sftp-mode-scp

## Hypothesis

The migrate transcript copy in rotate.py (the scp of a remote "$HOME/.claude/projects/..." path) is measured under this box's OpenSSH (SFTP-mode scp by default) against a local sshd-free fixture or a documented dry reproduction: if the literal $HOME is not expanded, the fix resolves the remote home explicitly (or uses a ~-relative path scp resolves) with a committed test pinning the argv; if it is expanded, the round records the measurement and changes nothing.

## Agent Notes
assigned: director-engine (0921 residue batch, engine slice leaf goal:g15.27.3); bytes verified by director-engine 10:3xZ 09-23 before minting.
