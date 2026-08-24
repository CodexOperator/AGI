---
confidence: 0.6
id: "level3:skills-agi-SKILL.md@v2"
origin: build-version
version: 2
supersedes: "level3:skills-agi-SKILL.md"
parents:
  - goal:g8.1
  - goal:g8.2
payload_ref: skills/agi/SKILL.md
tags:
  - level3
  - build-version
  - g8.1
  - g8.2
title: "Level-3 v2: skills/agi/SKILL.md — global skill install and the <project>/agi/<project>-tree layout"
type: level3
---

`skills/agi/SKILL.md` updated to describe the distribution shape the parent
committed to this iteration, replacing the v1 description (`agi/` = gitignored
drop-in clone with `nodes/`, `GOALS.md`, `agi-tree.config.json` at the project
root).

**The shape, in one paragraph.** Global reach comes from two symlinks
(`~/.claude/skills/agi` → `<engine>/skills/agi`, `~/.local/bin/agi` →
`<engine>/extensions/agi/driver.sh`) plus a `SessionStart` hook registered
once in `~/.claude/settings.json`. Per project, the engine still clones in —
unchanged — but the graph now lives one level deeper as its **own nested git
repo**, `<project>/agi/<project>-tree/`, instead of at the project root. This
is a **refinement of shape 1** (drop-in clone) from G8.1's three candidates,
not shape 2 or 3, and not a closed decision — no experiment has run to falsify
or confirm it. I documented the layout as the committed convention per the
brief's instruction; I did not mark goal:g8.1 decided.

**The symlink exception.** `agi-tree/agi` → the engine checkout and
`agi/agi-tree` → the tree are symlinks, not clones, because here the graph
literally builds the engine the loop runs on, so a stale clone would make
engine edits invisible to what's actually shipped. This does not violate
G8.2's invariant because it stays a **naming/filesystem convenience for one
specific local pair** — the engine still contains no `if project ==
"agi-tree"` branch, and `find-root.sh`'s discovery logic (walk up, then
descend into `<start>/agi/*-tree/`) treats a symlinked tree and a cloned tree
identically; it never checks which one it found.

**Verified on disk (`ls -la`), all under `/home/ubuntu`):**
- `.claude/skills/agi` → `work/agi/skills/agi` (symlink, confirmed)
- `.local/bin/agi` → `work/agi/extensions/agi/driver.sh` (symlink, confirmed)
- `~/.claude/settings.json` has a `SessionStart` hook block (confirmed present;
  did not diff its full command list beyond seeing the section header)
- `work/agi-tree/agi` → `work/agi` (symlink, confirmed)
- `work/agi/agi-tree` → `work/agi-tree` (symlink, confirmed)
- `work/agi/.gitignore` contains a bare `agi-tree` line with the comment
  explaining the trailing-slash-doesn't-match-symlink reasoning (confirmed;
  this is an **uncommitted** working-tree change — `git status` in the engine
  repo shows `.gitignore` and `extensions/agi/lib/find-root.sh` both modified,
  not yet committed)
- `extensions/agi/lib/find-root.sh` already implements the two-phase
  walk-up/descend-into-`agi/*-tree` discovery described in the brief
  (confirmed by reading the file; also uncommitted — this is kid-a's parallel
  work, not mine, and I did not touch it)
- `extensions/agi/bin/level3.py` does stamp `origin: level3-scan` and prune
  every such node it doesn't re-derive (confirmed by grep), which is why this
  node uses `origin: build-version` instead

**Taken from the brief, not independently verified:**
- `work/fantasia/agi/fantasia-tree/` — **does not exist yet.** `ls -la` on
  `fantasia/agi` shows no `fantasia-tree` subdirectory; `fantasia/` today still
  has the *old* layout (`GOALS.md`, `agi-tree.config.json`, `nodes/` at its own
  root, with a plain non-symlinked `agi/` clone beside them). So the SKILL.md
  worked example describes the target convention, not fantasia's current
  state. I flagged this as a deviation in the doc edit rather than escalating,
  since the brief explicitly asked me to "describe the layout as the committed
  convention" even though nothing instantiates it for fantasia yet.

**Open items left deliberately undone** (documented as such in SKILL.md, not
implemented by me or claimed done):
- Engine-commit pinning in `agi-tree.config.json`, G8.1's other explicit ask —
  not implemented anywhere in the engine.
- No `init` command or any other mechanism creates `<project>/agi/<project>-tree/`
  automatically; today it's manual (clone the engine, `git init` the tree
  inside it). I did not find an `init` subcommand for this and did not invent
  one in the doc.
- G8.1's falsifier — clone to an empty machine and check `git fetch` /
  `crontab -l` — belongs to G1.5, separately unrun.
- G8.2's falsifier — a third project (neither fantasia nor agi-tree) reaching
  a rendered map and a first chain with **no engine change at all** — has
  **not** been run this iteration. Nothing here constitutes that evidence;
  this node documents a decision, not an experiment result.

**Parent review, same version.** The doc asserted "the tree is never committed
into the engine" while the engine's `.gitignore` carried only a literal
`agi-tree` line — verified with `git check-ignore --no-index`: `agi-tree`
matched, `fantasia-tree` and `some-tree` did not. So the sentence was true for
exactly one pair and false for every project the layout is *for*: a fantasia
clone of the engine would have had `fantasia-tree/` untracked-but-committable
inside it, which is the vendoring failure H0/H0b already cost this project
twice. Fixed in the same version: the engine `.gitignore` pattern is now the
root-anchored, name-agnostic `/*-tree` (re-verified — `agi-tree`,
`fantasia-tree`, `some-tree` all ignored; a nested
`extensions/agi/nested-tree` correctly still tracked), and the SKILL.md
gitignore block now shows **both** required entries — `agi/` in the project
repo, `/*-tree` in the engine repo — with the anchoring and
trailing-slash-vs-symlink reasoning stated. Recorded here rather than as a v3
because it is the same payload edit still under review.

Deviation from the brief worth naming: I placed the new "Install" section
immediately before "Auto-injection" (rather than appending at the end) because
Auto-injection already explains the hook's runtime behavior in detail — Install
covering *how it got registered* reads better directly upstream of that,
and it kept the edit inside the existing section order per the "prefer
editing over appending" constraint.
