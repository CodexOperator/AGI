---
id: "mvp:cli-invocation-r1"
mint_id: c65596bd84814916b29e0fcb2019b4cd
next_edges:
  - outcome:cli-invocation-r1
parents:
  - verdict:cli-invocation-r1
status: implemented
tags:
  - cli
  - shell
  - detection
title: "MVP: CLI Shell Detection"
type: mvp
---

detect_shell() -> (shell_type, confidence). Covers bash/zsh/fish/cmd.
Implementation: environment_indexers/cli.py
