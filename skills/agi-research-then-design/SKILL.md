---
name: agi-research-then-design
description: >
  Feed one expensive design pass with many cheap research kids: declare the scale, fan out one research kid per
  question (the harness Agent tool, alias sonnet), each writing ONE cited file; check every file exists and is
  non-empty; then ONE design pass (the most capable alias the post is allowed) reads them all by path and returns a PATCH, never an edit; the
  coordinator guards the target's owner-marked lines byte for byte before applying. Use when a target (a deck, a
  doc, a skill, a brief) needs a researched rewrite worth an expensive pass.
---

# agi-research-then-design — cheap research feeds one expensive design pass (goal:g4.18.2.2)

The owner, 11-10 09:40:22Z (c:e780e4c65887) [meme-master store; not an OWNER heading under the interim rule until goal:g7.16.1.11.46.34 lands]:
> coordinate with SM as needed to formalize the way we researched the various skills via cheaper subagents then used that research to feed the much more expensive subagent. That needs to be in graph for everyone as an upgrade to the skill-create skill or whatever it is.

Route: the harness Agent tool, as skill agi-workflow's SUPERSEDED line names it (agi-workflow :12). Fan-out reviews stay skill agi-review.

```
DECLARE ─▶ RESEARCH (N kids, alias sonnet, parallel) ─▶ GAP CHECK ─▶ DESIGN (M passes, top allowed alias) ─▶ GUARD ─▶ APPLY ─▶ REPORT
 counts      one question -> ONE file each               every file     reads ALL files by path,         owner lines     the coordinator   token counts
 in the      table first, a URL per claim                exists,        returns a unified PATCH,         byte-identical  only              per call
 brief       VERIFIED / SECONDARY / UNVERIFIED           non-empty      never edits the live file        or REFUSED
```

## 1 · Declare the scale (before the first launch)
The coordinator's brief (its card or the target's node) names: the research-kid count, the design-pass count, each
stage's ROLE and harness ALIAS, the OUT dir, and the target's owner-line marker (§5). Research: alias sonnet.
Design: the most capable alias the RUNNING post is allowed: fable where an owner word or the post's row allows it
(meme-master's post, on belam's [owner] relay 07:0xZ 11-10); otherwise sonnet. The director brief's SUBAGENTS
rule is the owner's own subagent rule: under it a director's run is sonnet-only until the owner rules on this
pattern's design stage (put to the owner through belam, council 11-10); this skill does not widen it.
Name models by alias only; the versions a run resolved to go in that run's own report, never in this skill.
A design pass is the expensive stage: one pass, or a declared few, each with its own question. Never a fan-out of them.

## 2 · Research (cheap, parallel)
One Agent call per QUESTION, all in ONE message, alias sonnet, in the background. Each prompt carries:
- the context files to read, by path, and "read nothing else" (private dirs named, never their contents copied in);
- ONE question, with its numbered sub-points;
- ONE output file: `OUT/research-<letter>-<topic>.md`, a table first, then the detail; a URL per claim; each claim
  tagged VERIFIED / SECONDARY / UNVERIFIED; never an invented number; no edit to any repo;
- a reply of one line: the file it wrote and its line count.

## 3 · Gap check (no spend over a gap)
Before any design pass, every file the design prompt will cite must exist and be non-empty:
```bash
for f in OUT/research-*.md OUT/<ledger>.md; do [ -s "$f" ] || { echo "GAP: $f missing or empty: re-run its kid"; exit 1; }; done
```
A gap stops the run: re-run that ONE kid, then check again. A kid's reply that names its file is not this check.

## 4 · Design (expensive, fed)
One Agent call per declared pass, on the design alias §1 named. The prompt names every research file BY PATH (never a summary pasted
in), the target, and the owner-line ledger if the target has one, and asks for ONE unified patch in
`OUT/design-<n>.patch` against a named base of the target. The pass never edits the live file. A file added later
reaches a running pass by a follow-up message that names its path, and the coordinator's report says so.

## 5 · Guard (the coordinator, never an agent)
Lines the target marks as the owner's must be byte-identical before and after the patch, else the patch is REFUSED.

| target | owner-line marker | one line? |
|---|---|---|
| `.tex` (a deck) | `% OWNER c:<12 hex>` (or `c:pending-tap`) on the same physical line; a spoken line in `\note` opens `OWNER (c:...)` | yes: an owner sentence stays on one physical line |
| a graph node (`.md`) | the `## OWNER` block, and the `[... store; not an OWNER heading ...]` interim quote block | no: the guard's BLOCK mode (marker `## OWNER`) compares the block whole, from its heading to the next `## ` |
| anything else | the brief names its marker before the first launch, or says the target holds no owner lines (the guard's explicit `none`) | the brief says |

'The owner writes every final line' is goal:g5.4.3's own rule for the class paper, not every target's: a target's
brief says whether it has owner lines at all.
A target with more than one marker (a deck: the on-screen `% OWNER c:` and the spoken `OWNER (c:`) is guarded once
per marker, or once by their common word (`OWNER`); every run must PASS. A guard on one marker alone passes a patch
that edits the other's lines (§7 runs that mutant).
```bash
# guard TARGET PATCH MARKER [none]: applies PATCH to a COPY; PASS only when every MARKER line is byte-identical.
# A MARKER opening '## ' (a node's '## OWNER') is BLOCK mode: the block from that heading line to the next '## ' is compared whole.
# Closed by default: 0 MARKER lines in TARGET is READ NOTHING (rc 2) unless the 4th argument is 'none' (the brief says
# TARGET holds no owner lines). An empty or missing PATCH, or an empty MARKER, is READ NOTHING (rc 2).
guard() { t=$1 p=$2 m=$3 e=${4-}
  [ -n "$m" ] || { echo "GUARD: READ NOTHING (no marker named)"; return 2; }
  [ -s "$p" ] || { echo "GUARD: READ NOTHING (patch $p missing or empty: a pass that wrote nothing)"; return 2; }
  sel() { case $m in '## '*) awk -v h="$m" '$0==h{f=1;print;next} f&&/^## /{f=0} f' "$1";; *) grep -F -- "$m" "$1";; esac; }
  w=$(mktemp -d) || return 2
  cp -- "$t" "$w/pre" && cp -- "$t" "$w/post" || { echo "GUARD: READ NOTHING (cannot copy $t)"; return 2; }
  b=$(sel "$w/pre" | wc -l); [ "$b" = 0 ] && [ "$e" != none ] && { echo "GUARD: READ NOTHING (0 '$m' lines in $t; pass 'none' only when the brief says it holds no owner lines)"; return 2; }
  patch -s --dry-run "$w/post" < "$p" >/dev/null 2>&1 || { echo "GUARD: REFUSED (the patch does not apply)"; return 1; }
  patch -s "$w/post" < "$p" >/dev/null 2>&1
  if diff <(sel "$w/pre") <(sel "$w/post") >/dev/null; then
    echo "GUARD: PASS ($b marked line(s) byte-identical); apply: cp $w/post $t"; else
    echo "GUARD: REFUSED (a marked line changed):"; diff <(sel "$w/pre") <(sel "$w/post") | sed 's/^/  /'; return 1; fi; }
```
- The line mode matches every line holding the marker, an agent line that QUOTES it too: the compared set is a superset,
  which can only over-refuse. The block mode compares every block under that exact heading line, blank lines included.
- FLOORS (alive, named): the guard compares the marked SET, not places: a marked line moved whole, with an edited
  unmarked copy left where it stood, reads PASS. The interim `[... store; not an OWNER heading ...]` quote block has no
  mode yet: compare it by hand. Every run leaves its `mktemp -d` dir (the PASS line names it); the coordinator clears its own.
- A patch that adds or drops a marked line is refused as well (the set changed): the owner writes those lines.

## 6 · Apply and report
Apply only a PASS. The coordinator's message reports: the declared counts against the run's actual calls, the
harness token count of each call (research and design sums apart), the versions each alias resolved to (from the
agents' own replies), every file that arrived late, and each guard verdict with its before-count.

## 7 · Worked example (meme-master, goal:g5.4.3.1, the class presentation deck, 11-10)
Declared and run: 8 research kids (alias sonnet) + 4 design passes (alias fable) + 1 one-line version probe = 13 Agent
calls. Tokens: research 65,458 to 111,243 each, 697,817 in all; design 108,669 to 289,299 each, 845,293 in all;
the probe 40,464. Wall time: research about 80 to 220 s each, design 330 to 1,350 s each. Two inputs reached a running
design pass by follow-up message (one research file, the owner's decisions twice). Guard: 4 of 4 patches PASS, the
marked-line set growing 16 -> 31 -> 66 -> 70 as the owner wrote lines between passes. Gap check: not run mechanically
that night (each kid's reply named its file): §3 is new practice. The prompts, owner lines and private paths elided:
`skills/agi-research-then-design/example-2026-11-10.md`.

The guard's mutants, RUN (a scratch dir; a deck with one on-screen and one spoken owner line; one-line patches):
```bash
d=$(mktemp -d); cd "$d"
printf '%s\n' '\begin{frame}{Why}' 'The graph keeps every thought. % OWNER c:000000000000' 'Agents add one node a turn.' \
  '\note{OWNER (c:000000000000) We started with one file.}' '\end{frame}' > deck.tex
cp deck.tex a.tex; sed -i 's/one node a turn/one node per turn/' a.tex; diff -u deck.tex a.tex > ok.patch
cp deck.tex b.tex; sed -i 's/every thought/each thought/' b.tex; diff -u deck.tex b.tex > mutant.patch
cp deck.tex c.tex; sed -i 's/one file/a single file/' c.tex; diff -u deck.tex c.tex > note.patch
printf 'no marker here\n' > empty.tex; : > nothing.patch
printf '%s\n' '## OWNER' '> keep every thought.' '' '## Body' 'agent text' > node.md
cp node.md n.md; sed -i 's/every thought/each thought/' n.md; diff -u node.md n.md > block.patch
cp empty.tex e.tex; sed -i 's/here/at all/' e.tex; diff -u empty.tex e.tex > none.patch
guard deck.tex ok.patch OWNER                  # GUARD: PASS (2 marked line(s) byte-identical) ...        rc 0
guard deck.tex mutant.patch OWNER              # GUARD: REFUSED (a marked line changed): ...               rc 1
guard deck.tex note.patch OWNER                # GUARD: REFUSED (a marked line changed): the spoken line rc 1
guard deck.tex note.patch '% OWNER c:'         # GUARD: PASS: the one-marker hole; never guard a deck so   rc 0
guard deck.tex note.patch 'OWNER (c:'          # GUARD: REFUSED: once per marker, every run must PASS      rc 1
guard empty.tex ok.patch OWNER                 # GUARD: READ NOTHING (0 'OWNER' lines ...): closed default rc 2
guard empty.tex none.patch OWNER none          # GUARD: PASS (0 marked line(s) ...): the brief said none   rc 0
guard deck.tex nothing.patch OWNER             # GUARD: READ NOTHING (patch ... missing or empty ...)      rc 2
guard deck.tex absent.patch OWNER              # GUARD: READ NOTHING (patch ... missing or empty ...)      rc 2
guard node.md block.patch '## OWNER'           # BLOCK mode: REFUSED (the block body changed)              rc 1
```

## 8 · Never
- a design pass launched over a gap (§3), or with research pasted into its prompt instead of named by path;
- a design pass editing the live target; an applied patch without a PASS;
- a model named by version in a brief or this skill (alias only); a fan-out of design passes;
- a guard run by an agent on itself: the coordinator runs it on its own copy.
