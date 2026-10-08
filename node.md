---
id: mvp:cli-invocation-r1
mint_id: c65596bd84814916b29e0fcb2019b4cd
type: mvp
parents:
  - verdict:cli-invocation-r1
next_edges:
  - outcome:cli-invocation-r1
edited_by: season.py
season: 1
status: implemented
tags:
  - cli
  - shell
  - detection
thought_session: season
title: "MVP: CLI Shell Detection"
---
detect_shell() -> (shell_type, confidence). Covers bash/zsh/fish/cmd.
Implementation: environment_indexers/cli.py