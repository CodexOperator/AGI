---
name: agi-send
description: >
  Send, read, and list mail across agi posts with box (graph SoT): signed commits on
  refs/box/<from>/<to>, consume vs list, adjacency (matrix), and what may be sent upward.
  Use whenever a post messages another post, reads its inbox, or checks unread mail.
  Retired inbox-file send path lives under extensions/agi/deprecated/bin/ (never git rm).
---

# agi-send — box mail (consume vs list)

Source of truth: `/var/lib/agi/<post>/bin/box` (same binary projected per seat). Identity is `AGI_POST=<me>` — never shell as another uid to "fix" refuse.

## 1 · The acts
```bash
# send (stdin body → signed tip on refs/box/<me>/<to>; adjacent seats only)
printf '%s\n' "$BODY" | box send <to>

# list unread only (does NOT consume)
box n

# consume unread (prints bodies; advances refs/held/<me>/<from>)
box read
```
- `box read` **CONSUMES** (moves held). `box n` only lists. Never invent a peek that skips held.
- Read runs as the post uid. Foreign uid (e.g. belam reading sanctuary-master) → `[refused]`.
- Off-matrix → `[off-matrix] … nothing sent` (levels differ by >1 or missing harness).
- Body via printf/pipe — never `b=$(cat)` in caller scripts; never embed backticks/`$(` in the shell string for the body.

## 2 · Panes (not tmux)
ET seats: systemd `agi-post@<post>.service` + fifo `/run/agi-<post>/i` + out `/var/lib/agi/<post>/o`. Raw-shell has no auto mail-wake (pi/claude harnesses poll `box n`); SM drives DG raw-shell by writing the fifo.

## 3 · To the Prime — tagged or REFUSED
`printf '%s\n' "[tag] <one line>" | box send belam`, tag ∈ `merge-up` · `decision` · `rotation` · `red` · `rule` · `complete` · `owner`.
```
director ─▶ Prime : ONLY merge-up · a decision only the Prime makes · rotation · red · rule-changing finding
                    NEVER progress · status · acks · harvests — nodes + the commit log carry those
Prime ─▶ master   : ONE report per COMPLETED pass
```
Speak up ONE tier only. Owner words stay verbatim, in NODES.

## 4 · Skills SoT
Graph `skills/*/SKILL.md` is SoT. Seat `~/.grok/skills/<name>` → symlink via `agi-sync` (post-doc-sync). Never hand-edit box copies.
