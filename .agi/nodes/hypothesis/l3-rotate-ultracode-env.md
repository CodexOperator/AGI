---
id: hypothesis:l3-rotate-ultracode-env
mint_id: 7baf7724778f49d6804fb5f047c21d3a
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: ubuntu
scaffold_hash: 62f33aadd09270e3
season: 1
testable_claim: "A successor or advisor spawned for a role whose ladder settings carry ultracode gets CLAUDE_CODE_WORKFLOWS=1 in its environment and the keyword ultracode in its prompt, and reports ultracode: yes from its own system-reminder; without the env var it reports no"
title: L3 rotate ultracode env gate
---
# hypothesis:l3-rotate-ultracode-env

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
MEASURED LIVE 2026-09-06 by the prime (belam), three throwaway successors through the fixed rotate.py on claude 2.1.263: (1) --settings '{ultracode: true}' alone, prompt without the keyword: session shows effort max, ultracode NOT enabled (owner saw it in the status line). (2) keyword ultracode as the first line of the prompt body plus the same settings: the successor answers ultracode: no. (3) the same plus CLAUDE_CODE_WORKFLOWS=1 exported in the tmux window before the claude command: the successor answers ultracode: yes. The binary's own text: dynamic workflows are not enabled for this session (org policy, launch gate, or the Dynamic workflows setting in /config); ultracode is not available for this session (dynamic workflows are off, or the model / your organization does not allow xhigh effort); the ultracode keyword trigger is on by default and opts the turn in. The prime's own session (belam-S1-L3) was launched without the env var, so it runs without ultracode; the bridge's apply_flag_settings request at its start returned error. FILES: extensions/agi/bin/rotate.py (spawn and loop: when the resolved role settings contain ultracode true, prefix the tmux command with export CLAUDE_CODE_WORKFLOWS=1 and make the keyword ultracode the first line of the assembled prompt, after the head is fine, but it must be in the user turn), extensions/agi/bin/adapters/claude_code_adapter.py (same env and keyword for tier-3 advisors and any ultracode row), tests. Also decide whether --settings ultracode is still needed once the env var and keyword are present (measure with a fourth throwaway: env var plus keyword, no settings) and keep only what is load-bearing, say which. VERIFY: red-first test that the built command carries the env export and the keyword for an ultracode role and neither for a plain role; a dry spawn prints it; one live throwaway via rotate.py spawn --name belam-test4 --prompt-file with the two-line reply protocol (line 1 ultracode: yes or no, line 2 continue) answers yes; kill the window after. REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list (pass --evidence-runs), every verify command with its actual output in the body. Do not commit, push, or run grid.py commit.

ADDENDUM 2026-09-06 (owner): the remote-control GUI (desktop Claude app, Mac) still renders ultracode as off for a session that reported yes; the owner reads that as the GUI's own value, which would override the session setting only when a message is submitted from that GUI window. Kid: confirm whether CLAUDE_CODE_WORKFLOWS=1 also makes the bridge's apply_flag_settings request succeed (it returned error on the prime's own session, launched without the env var), and document for the owner: flip the GUI toggle on before sending from the GUI, or send from the terminal.
