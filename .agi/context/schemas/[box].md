---
name: box
structural: true
derived_from: SM.125 slice 3 (hypothesis:l4-config-max-and-template-max-are-required-verdict-fields-of-every-merge-up-review-and-a-named-line-of-every-dispatch-order) -- the four cell names were hardcoded in boxes.py and re-hardcoded in paths.py with nothing declaring the object; this schema is the one declaration
fields:
  root: {type: str}          # the project root this box's graph describes; placeholder {root}
  logs_dir: {type: str}      # the directory this box's logs live in; placeholder {logs}
  tmux_session: {type: str}  # the tmux session seats are spawned into; placeholder {tmux}
  user: {type: str}          # the account this box runs as; placeholder {user}
placeholders:
  root: root                # {root} renders the `root` cell
  logs: logs_dir            # {logs} renders the `logs_dir` cell
  tmux: tmux_session        # {tmux} renders the `tmux_session` cell
  user: user                # {user} renders the `user` cell
  repo_root: repo_root      # {repo_root} renders the `repo_root` cell (crons)
  box: box                  # {box} renders the `box` cell (crons' own box)
validation:
  required: [root, logs_dir, tmux_session, user]
  types:
    root: str
    logs_dir: str
    tmux_session: str
    user: str
---

# box

**The `box` cell group on `.agi/config.json` — the four facts that differ
between two boxes running the same graph.** `extensions/agi/bin/boxes.py`
reads this declaration as its one source of the cell names AND of the
placeholder map (falling back only to the fields it can read when the schema
is absent); `extensions/agi/bin/paths.py audit`
uses those names to classify a box-specific literal as `logs`, `tmux` or
`user`. A third reader must read this schema, not write a fourth list.

## Why the object needs a schema at all

The cells exist so a `paths.py audit` failure can name the *cell* a literal
should have moved to, and so `boxes.resolve_placeholders` can render
`{root} {logs} {tmux} {user}` on a box with no absolute path copied from
another. Before this file the names lived in code only, which is exactly the
`config_max` residue the SM.125 review named: a fact about the graph's own
shape with no declaration in the graph.

## Not a node type

No node of type `box` is minted and `validation.required` above applies to a
node frontmatter block, never to the embedded `config.json` object — the
required list is declared here so the shape is stated once, and the real
guard for a missing cell is `paths.py audit`'s exit 2 (it refuses to report a
class clean when its cell is unset). Absent cell, loudly: never silent.

Absent cell, loudly: never silent.

## Box-local override (`config.local.json`)

Authority for the four cells on THIS machine is the untracked sibling
`config.local.json` (gitignored), read by `boxes._box` after the committed
`config.json` and winning per key. Shared `config.json` may keep a foreign
reference box (e.g. a retired path used as a negative fixture / unify
forbidden-set seed on other machines). **Never write this box's real
`root`/`logs_dir`/`user` into the shared file** — that hands
`unify._real_repos` nonsense paths on every other box
(hypothesis:a00-d089cf46-707110 / goal:g7.33.14). Worktree graphs resolve the
main checkout's `config.local.json` via git common-dir when their own copy is
absent (same shape as envfile → main `.env`).
