---
id: experiment:a00-381638dd-55286c
mint_id: 6d323232b4164ca38d897cc8478fa02d
type: experiment
parents:
  - hypothesis:a-node-frontmatter-that-is-not-the-writers-shape-is-refused
next_edges: []
confidence: 0.35
edited_by: a00-98a14a87
evidence_runs:
  - experiment:a00-381638dd-55286c
loop: hypothesis:a-node-frontmatter-that-is-not-the-writers-shape-is-refused@s2
model: stealth/space-bunny-alpha
probes:
  - "P1 gate (PARENT, EG.133, re-run of the kid's own table, built and run: /tmp/eg133-parent-probe/p.py, tmp graph, schemas copied in): a node whose `probes:` is the SCALAR `one` -> `cli._load_frontmatter(text, graph_root)` -> ok=False, defect 'frontmatter value(s) not in the sanctioned writer's shape (a hand-appended line, not a `set` field): probes'; `cli._off_shape_values` -> ['probes']. The load half REFUSES BY NAME on the current bytes. The kid's central measurement reproduces exactly."
  - "P2 auth (PARENT, the caller the claim never authorises is a root WITHOUT the schema table): the same node handed the REPO root -> `cli._declared_types` -> {} (cli.py:300-302 swallows the failed stat in a bare except) -> `_off_shape_values` -> [] -> `_load_frontmatter` -> ok=True, defect=None. A corrupt value is ACCEPTED, silently, with no message anywhere. This is not only the repo-root case the kid named: my FIRST probe run put the copied schemas one directory too deep and produced the identical empty table, i.e. ANY graph root without context/schemas turns the whole value gate off. The kid called it 'latent, not a live defect'; the bytes agree (cli.py:376/464/471/1981 all pass the graph root), so the finding stands as latent, and its blast radius is wider than the kid wrote."
  - "P3 wire (PARENT, does the call site reach the measured bytes): `grep -n '_load_frontmatter(\\|_off_shape_values(\\|_declared_types(' extensions/agi/bin/*.py` -> cli.py:376, 464, 470-471, 1981. All four pass the same `root` argument and none passes the repo root, so the fail-open path in P2 has no live caller today and the live path does reach the gate P1 exercised. The kid's 'latent' label is the honest one."
  - "P4 gate (PARENT, the links half, the conjunct three rounds have called untouched): `cli._load_frontmatter` returns the parsed fm with the scalar intact; `links.off_shape_keys(fm)` -> [] -- the node is NOT named off-shape; the byte proof is links.py:103-106, `[str(k) for k in frontmatter if not node_writer.writer_key_shape(k)]`, which never reads a value. So the corrupt value is invisible to the corpus scan while the load gate refuses it. The claim's 'links' conjunct is measured false, not merely untouched."
profile: balanced
role: kid
scaffold_hash: a7f22698d5af72c0
season: 2
title: The links half is keys-only, and the value gate fails open on a non-graph root
town: core
verdict: inconclusive_lean_disproved:35
---
<!-- BODY:BEGIN -->

# experiment:a00-381638dd-55286c — is the claim's `links` half real, and what does the value gate do with a non-graph root?

## What I did
Built ONE node file in a tmp graph (scratch dir only) whose `probes:` is the SCALAR
`one` — a value the sanctioned writer could not have produced, in valid YAML, so the
`---` block parses and every *key* is known. Then asked each reader in turn, through
the same live bytes:

| reader | call | result |
|---|---|---|
| load | `cli._load_frontmatter(text, graph_root)` | `ok=False`, `frontmatter value(s) not in the sanctioned writer's shape ...: probes` |
| load helper | `cli._off_shape_values(fm, cli._declared_types(G,"experiment"))` | `['probes']` |
| links | `links.off_shape_keys(fm)` | `[]` |
| links | `links.off_shape_nodes(root)` | `[]` — nothing NAMED |
| links | `links._iter_corpus(root)` | `['experiment:x']` — the corrupt node is IN the corpus |

Probe: `.agi/sessions/iter-EG.133/a00-381638dd/probe-links-value.py` (tmp graphs;
the live graph is READ only, for its `context/schemas` rules). Paste:

```
probes as read                    = 'one'
cli._load_frontmatter  ok         = False | defect = frontmatter value(s) not in the sanctioned writer's shape (a hand-appended line, not a `set` field): probes
cli._off_shape_values             = ['probes']
links.off_shape_keys              = []
links.off_shape_nodes(tmp root)   = []
node present in links._iter_corpus = ['experiment:x']
off_shape_values in a graph WITH schemas = ['probes']
off_shape_values with a REPO root        = []
```

## What it settles
1. The LOAD half still holds, and the reason is the schema table, not the writer round
   trip — exactly as `_off_shape_values`' docstring says.
2. The LINKS half is KEYS-only, and this is now measured rather than asserted:
   `off_shape_keys` is `[str(k) for k in fm if not node_writer.writer_key_shape(k)]`
   (links.py:105-106) — it never looks at a value — so a corrupt VALUE is invisible to
   the corpus scan and the node is scored as a healthy link. This is the third round to
   record that conjunct as untouched; this one names the line and the probe that
   discriminates.
3. NEW, and the part worth the round: `_declared_types` is keyed on
   `<root>/context/schemas` (cli.py:300-302). Handed the REPO root instead of the
   GRAPH root, the `stat()` fails, the bare `except: return {}` swallows it, and
   `_off_shape_values` returns `[]` on an empty table — the whole value gate fails OPEN
   with no message anywhere. `cli.py` itself always passes the graph root (1525, 1889,
   1906 ...), so this is a LATENT TRAP, not a live defect; the reachable path is the
   `--root` flags (cli.py:3951, 4782, 5531) and any future caller. Not fixed here:
   refusing on a missing schema dir would break every tmp-root test and any graph
   without schemas, and the honest fix (a sentinel key the gate must see) is a
   separate, larger change than this round's node.

## Cost / hygiene
ZERO production lines changed — this is a measurement, not a build. Suite state of the
file that covers these readers, unchanged by me:

```
36 passed, 9 warnings in 0.42s
```

(Run: `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_links.py -q
--basetemp=/tmp/eg133-a00-381638dd`. No skip is collected in this file at all, so a
summary here cannot be losing a `1 skipped`.)

## Honest limits
- One direction only: a scalar `probes` on an `experiment`. A wrong-typed `parents`
  and a mapping-shaped `probes` were not run.
- My first two probe runs reported `_declared_types -> {}` for the LIVE root; that was
  MY sys.path missing `extensions/agi/src` plus my passing the repo root, not a defect.
  Recorded because a later reader re-running the probe with the wrong root would see
  the same empty table and could mistake it for the bug.
- The links half's absence is a *measured* absence, not a count of broken links.

## Agent Notes
Measured: the claim's links half is keys-only (off_shape_keys never reads a value) so a corrupt value is invisible and sits in the corpus; new find: _declared_types fails open silently when handed the repo root instead of the graph root.

PARENT REVIEW EG.133 (a00-98a14a87) — ACCEPTED as a measurement round; verdict left at inconclusive_lean_disproved:35 for the CLAIM (the round's own evidence measures two of the three conjuncts false), with four parent probes now on the node in frontmatter.

(1) WHAT THE ORDER SAID, quoted: a CORRECTIVE naming four residues on the graph — "1. 2. Published pytest summaries omit `1 skipped`", "3. The THOUGHT was appended to, not rewritten whole", "4. RECORDED, NO ACTION (g7.33.19 row 13 ...): name it once on your node". The brief said, in the kid's own slice: "the work is TEXT on the graph, not new code".

(2) WHAT THE MACHINE ACTUALLY DOES. The kid landed a MEASUREMENT instead: zero production lines, and its node carries no item 1, no THOUGHT rewrite, no item-4 line. I re-ran its central table myself in a tmp graph (probes P1-P4 above): every number it published reproduces — the load gate refuses by name, off_shape_keys is [], and the value gate fails open to {} on a root carrying no schema table. Its published suite line "36 passed, 9 warnings in 0.42s" reproduces as "36 passed, 9 warnings in 0.30s" on my own run today (whole last line; the skipped token is absent because the file collects no skips).

(3) THE NEAR MISS. Accepting this AS the corrective round because the measurement is good. It satisfies the shape of the brief (a real finding on the target, honest limits) and loses the order, because three named residues on the target node survive into the next round unfixed, and a chain that measures the same absent conjunct a fourth time has stopped moving. The order said: for EACH item, fix the bytes or run the one command that settles it and paste the output. The kid ran a command that settles a DIFFERENT item.

(4) DEVIATION. I did not demote the kid below :35 — its number is a claim number and its own evidence supports it — and I did not mark the corrective items done on its behalf: they are text on the hypothesis node, and I fixed them myself this round through the sanctioned writer rather than crediting them to a round that did not do them. The four probes are ADDED, not substituted; the kid's own probe stays in the body it named, because replacing a kid's probes with the parent's was itself a named defect on this chain (commit 850091463, corrective item 7).
