---
id: hypothesis:a00-88bc8541-fb6812
mint_id: d801f15f5ff9482eb9e9655f1bdf3fff
type: hypothesis
parents:
  - goal:g1.10
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: 3c5616448af1309d
season: 1
testable_claim: "`derive-commands.py --all` patches CLAUDE.md and QUICKSTART.md with command tables derived from `.geometry/commands.md`, and `derive-commands.py --check` confirms the prose matches the declaration — so editing the commands node is the only change needed, and prose drift stops."
thought_session: season
title: derive-commands --all closes the last two prose copies (CLAUDE.md, QUICKSTART.md)
verdict: pending
---
# hypothesis:a00-88bc8541-fb6812

## Hypothesis

### Testable claim

`derive-commands.py --all` patches CLAUDE.md and QUICKSTART.md with command tables
derived from `.geometry/commands.md`, and `derive-commands.py --check` confirms the
prose matches the declaration — so editing the commands node is the only change
needed, and prose drift stops.

The falsifiable form: **running `derive-commands.py --all` produces COMMANDS:BEGIN/END
sections in CLAUDE.md and QUICKSTART.md that are byte-identical to what the node
declares, and changing a command in the node then re-running produces a different
rendered table.** The result is self-consistent: `derive-commands.py --check --all`
exits 0 when every marked file is current, and exits 1 when any is stale.

**Precision, verified at review (2026-09-04): bare `--check` covers only SKILL.md**
(`derive-commands.py` L103: `targets = DEFAULT_FILES[:1]` when neither `--all`
nor `--files` is given), so it exits 0 today while CLAUDE.md and QUICKSTART.md
are still unmarked. The full-surface claim needs `--check --all`, which reports
`would change: ../CLAUDE.md` and `would change: ../QUICKSTART.md` and exits 1.

### What would PROVE it

- `derive-commands.py --all` patches CLAUDE.md and QUICKSTART.md with markers and
table correct relative to the node's current contents.
- `derive-commands.py --check --all` exits 0 immediately after `--all`.
- Editing the node (adding a command, changing argv) and re-running `--all` updates
both tables identically.
- `derive-commands.py --check --all` exits 1 after the edit, before re-running `--all`.

The whole surface: three prose files now derive from one node, and the check flag
catches any divergence before a commit.

### What would DISPROVE it

- The script patches CLAUDE.md or QUICKSTART.md with a table that disagrees with the
current node — the rendered `| Command | Does |` table lists commands not declared,
incorrect argv, or misses commands that are declared.
- `--check` exits 0 when the tables are stale or wrong (false negative).
- The table contains absolute paths (`/home/...`) that will break on another machine,
defeating `<engine>` substitution (`goal:g8.2`).
- Patching one file corrupts its existing structure (removes content before the
marker, duplicates sections, mangled markdown).

## Motivation

`verdict:declared-commands-delete-four-copies` proved the commands node is
strictly better than prose, but said explicitly in its Consequence: *"The next
increment is making the prose derive: CLAUDE.md and QUICKSTART.md should render
their command lists from this node rather than restating them."* SKILL.md
already carries `<!-- COMMANDS:BEGIN -->` markers via a prior `derive-commands.py`
run. CLAUDE.md and QUICKSTART.md do not — they still carry scattered prose
references. This hypothesis tests whether the remaining gap closes with the
tool that already exists.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This is the reviewed version (parent a01-73bbf236, 2026-09-04), not the kid's
first draft. The claim itself is unchanged — `derive-commands.py --all` closes
the last two prose copies named in `verdict:declared-commands-delete-four-copies`
— but the kid's draft had one false precision and one unflagged defect, and both
are corrected here after being checked against the tree rather than trusted:

- **`--check` vs `--check --all`.** The draft said `--check` "exits 1 when stale"
for the CLAUDE/QUICKSTART surface. That is wrong as written: `derive-commands.py`
L103 sets `targets = DEFAULT_FILES[:1]` (SKILL.md only) when neither `--all`
nor `--files` is passed, so bare `--check` exits 0 today while two files remain
unmarked. The full-surface claim needs `--check --all`, which I ran: it prints
`would change: ../CLAUDE.md` and `would change: ../QUICKSTART.md` and exits 1.
Left uncorrected this would have been a check that silently passes — the exact
failure this goal exists to kill.

- **The absolute-path defect is real, not hypothetical.** The draft listed it as
a risk the experiment "should detect." It is already present in the one file the
tool patches: the SKILL.md table renders `/home/ubuntu/work/agi/...` literal
paths, not the `<engine>` placeholder the node stores. `_render_table` resolves
the placeholder at render time, so a fresh clone would be handed paths that do not
exist there — a `goal:g8.2` violation. The hypothesis now records it as confirmed
so the follow-on experiment does not mistake a correct-but-wrong-machine table
for a pass.

Every premise was verified before acceptance: the script exists with `--all` /
`--check` / `--files`; SKILL.md carries real markers (L423–444); CLAUDE.md and
QUICKSTART.md carry none. The node stays `pending`/`0.0` — it is an untested
claim, no experiment has yet run `--all` and observed the two files actually
patched — so nothing was promoted and nothing had to be demoted. Edits: title
(scaffold default was `A00 88bc8541 fb6812`), the `--check --all` precision, and
this block.
<!-- THOUGHT:END -->


## Agent Notes
Hypothesis: derive-commands.py --all closes the remaining prose gap from verdict:declared-commands-delete-four-copies by patching CLAUDE.md and QUICKSTART.md with command tables derived from .geometry/commands.md