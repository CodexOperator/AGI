---
id: goal:g4.18.2.2
mint_id: cc9b02f5b6f94059903da851bce7a748
type: goal
parents:
  - goal:g4.18.2
next_edges: []
confidence: 0.5
goal_id: G4.18.2.2
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 960c9eec81324a1b
season: 3
seeds: []
status: complete
tags: []
title: "G4.18.2.2: the research-then-design pattern is a graph skill (skills/agi-research-then-design): cheap research kids, one file each, feed one expensive design pass that returns a patch, an owner-line guard before it applies"
town: core
---

# goal:g4.18.2.2

## Why this exists
goal:g4.18.2 (one skill per engine flow, skill build nodes under this goal): the owner asked on 11-10 that the way goal:g5.4.3.1's presentation was researched, cheap subagents feeding one expensive one, "be in graph for everyone". No graph skill holds that pattern (there is no graph skill-create; the harness's skill-creator is a plugin), and goals are the only place new work is recorded, so this leaf comes first and the skill is built under it (council [decision] alive 09:47:42Z 11-10, 3/3 YES AMENDED: P1 goal first, A1 this parent).

## The owner's words 2026-11-10 09:40:22Z (c:e780e4c65887), verbatim [meme-master store; not an OWNER heading under the interim rule (self-perpetuating 19:55:55Z 11-09) until goal:g7.16.1.11.46.34 lands]
> coordinate with SM as needed to formalize the way we researched the various skills via cheaper subagents then used that research to feed the much more expensive subagent. That needs to be in graph for everyone as an upgrade to the skill-create skill or whatever it is.

## Target end-state
1. `skills/agi-research-then-design/SKILL.md` is on the trunk, written by director-general-1 under this leaf (its build node's parents a legal set: [this leaf, idea:engine-skill-doc] or [this leaf, a new idea for the pattern], the writer's pick named in the cut), carrying meme-master's four stages as run for goal:g5.4.3.1:
   1. RESEARCH, cheap and parallel: one kid per question, each writing ONE file (a table first, then detail; a URL per claim; VERIFIED / SECONDARY / UNVERIFIED on each; never an invented number; reads nothing outside its brief).
   2. DESIGN, expensive and fed: one pass reads ALL the research files (and the target's owner-line ledger where it has one) and never edits the live file: it returns a unified PATCH.
   3. GUARD: the coordinator dry-runs the patch, applies it, and compares the target's owner-marked lines before and after.
   4. Each stage cites the earlier stage's FILES by path, never a summary in the prompt.
2. The worked example is meme-master's run of 11-10: 13 harness Agent calls = 8 research (sonnet) + 4 design (fable) + 1 version probe, named as a probe, not a stage (meme-master's corrected count, via DG1's [note] 09:57Z); owner lines and private paths elided; with that run's declared scale and token counts. Counts sit before the alias or bracketed, never right after a model word (F3's pattern reads 'sonnet 8' as a version).
3. In the SAME tip, skills/agi-workflow's description (the text every post's skill listing prints) and its route bullet are narrowed to the legacy workflow.py route and point at agi-review and the new skill; every hit of the writer's grep for the old 'never ... the Agent tool' reach is fixed in that tip, not only named (A3, sp ADD 1).

## Invariants
- The skill cites agi-workflow's route line for the harness Agent tool and restates no 'never the Agent tool' line (A3).
- Each stage is named by ROLE and harness ALIAS, never a pinned model version (A2): research: sonnet; design: the most capable alias the running post is allowed, fable only where an owner word or the post's row allows it (meme-master's post today), sonnet-only for a director under the director brief's SUBAGENTS rule until the owner rules (council 10:00:48Z (3)(b); the owner is asked (3)(a)).
- THE GUARD is general and never empty (A4, sp ADD 2): lines the target marks as the owner's are byte-identical before and after the patch, else the patch is refused; the skill names the marker per file type; a before-count of 0 on a target the brief says holds owner lines is READ NOTHING, refused; a marked block that can wrap past its marker line is compared whole, or the skill rules a marked line one line. 'The owner writes every final line' is named as goal:g5.4.3's own rule, not every target's.
- NO SPEND OVER A GAP (sp ADD 3): no design pass launches until every research file its prompt cites exists and is non-empty; a missing or empty one = stop, re-run that one kid.
- DECLARED SCALE (alive's TERM): a run declares its research-kid and design-pass counts in the coordinator's brief before the first launch, and its message reports the harness's token counts after.

## Falsifier
1. THE SKILL, from the repo top, exits 0 only when the skill file exists, is non-empty and names itself:
   `{ [ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" ] || { echo "READ NOTHING: not at the repo top"; false; }; } && [ -s skills/agi-research-then-design/SKILL.md ] && grep -q -x 'name: agi-research-then-design' skills/agi-research-then-design/SKILL.md`
   RUN at the mint on 19b8cd62d9: exit 1 (no file); outside a repo: exit 1.
2. THE NARROWING, from the repo top, exits 0 only when (a) agi-workflow's description, read as the listing prints it (folded lines joined), names BOTH agi-review and agi-research-then-design and no longer holds 'never through the Claude Workflow or Agent tools' nor 'research sweep'; and (b) each other hit, read by its ANCHOR, no longer forbids the route: agi-workflow's bullet starting '- pi by default' holds no 'NEVER the Agent tool, on any post', and unified-director-brief's line holding 'REVIEW IN PLACE (owner 2026-09-18' holds no 'no Claude subagents, ever'; and (c) each of those two narrowed bullets holds the owner's 10-10 cite, 'just use sonnet subagents'. Each anchored bullet is read WHOLE (the anchor line plus its indented continuation lines), compared case-blind with whitespace and punctuation squeezed; the two skill names are matched as exact hyphenated tokens. A missing file, description or anchor prints READ NOTHING, exit 1 (council 10:00:48Z, sp's AMENDs 09:58:31Z and 10:12:04Z):
```
{ [ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" ] || { echo "READ NOTHING: not at the repo top"; false; }; } && python3 -I -c 'import re,sys
def rd(p):
    try: return open(p,encoding="utf-8").read()
    except OSError: print("READ NOTHING "+p); sys.exit(1)
def sq(s): return " "+re.sub(r"\W+"," ",s.lower()).strip()+" "
def bullet(text,key,start):
    L=text.splitlines()
    for i,l in enumerate(L):
        if (l.startswith(key) if start else key in l):
            out=[l]
            for m in L[i+1:]:
                s=m.strip()
                if not s or not m[:1].isspace() or s.startswith(("- ","└","├")): break
                out.append(m)
            return " ".join(out)
    return None
w=rd("skills/agi-workflow/SKILL.md"); b=rd(".agi/nodes/doc/unified-director-brief.md")
m=re.search(r"^description: >\n((?:  .*\n)+)",w,re.M)
if not m: print("READ NOTHING description"); sys.exit(1)
raw=" ".join(l.strip() for l in m.group(1).splitlines()); d=sq(raw)
def has(n): return re.search(r"(?<![\w-])"+re.escape(n)+r"(?![\w-])",raw) is not None
A=bullet(w,"- pi by default",True); B=bullet(b,"REVIEW IN PLACE (owner 2026-09-18",False)
if A is None: print("READ NOTHING anchor agi-workflow - pi by default"); sys.exit(1)
if B is None: print("READ NOTHING anchor unified-director-brief REVIEW IN PLACE (owner 2026-09-18)"); sys.exit(1)
A,B=sq(A),sq(B); C=" just use sonnet subagents "
bad=[x for x,c in [
 ("description lacks agi-review",not has("agi-review")),
 ("description lacks agi-research-then-design",not has("agi-research-then-design")),
 ("description still forbids the Agent tool"," never through the claude workflow or agent tools " in d),
 ("description still says research sweep"," research sweep " in d),
 ("pi-by-default bullet still forbids the Agent tool"," never the agent tool " in A),
 ("pi-by-default bullet lacks the owner 10-10 cite",C not in A),
 ("REVIEW IN PLACE still says no Claude subagents"," no claude subagents ever " in B),
 ("REVIEW IN PLACE lacks the owner 10-10 cite",C not in B)] if c]
print("; ".join(bad) or "F2 met"); sys.exit(1 if bad else 0)'
```
   RUN at the mint's base 19b8cd62d9: exit 1, naming all EIGHT unmet items; outside a repo: 'READ NOTHING: not at the repo top', exit 1. Control (the real two files with the description, :23 and :60 narrowed, each citing 'just use sonnet subagents'): exit 0. Mutants, each exit 1: sp's four, (1) :23 'NEVER the Agent tool on any post' (comma dropped), (2) :23's rule wrapped onto the bullet's continuation line, (3) :60 'no Claude subagents ever', (4) both narrowed with no 10-10 cite; 'agi review' unhyphenated (the squeeze would have read it as the name); a longer name only ('agi-research-then-design-old'); 'research sweep' back; the anchor removed (READ NOTHING).
3. NO PINNED VERSION, from the repo top, exits 0 only when the skill exists and names no model by version (A2):
   `{ [ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" ] || { echo "READ NOTHING: not at the repo top"; false; }; } && [ -s skills/agi-research-then-design/SKILL.md ] && ! grep -q -i -E '(sonnet|opus|fable|haiku)[ -]?[0-9]+(\.[0-9]+)?|claude-[a-z]+-[0-9]' skills/agi-research-then-design/SKILL.md`
   RUN at the mint on 19b8cd62d9: exit 1 (no file: fails closed). The pattern is a FLOOR (a bracketed version such as 'Fable (5.2)' passes it); a hand read beside it. A run's own record names the versions it used; the skill does not.
4. THE BUILD NODE, from the repo top, exits 0 only when the ONE node by its house name, .agi/nodes/build/skills-agi-research-then-design-SKILL.md.md, exists, its link_ref is skills/agi-research-then-design/SKILL.md, and this leaf is in its PARENTS block, read as the '  - ' lines right after 'parents:' (sp's AMENDs: any build node naming the leaf no longer passes, nor this leaf under next_edges):
```
{ [ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" ] || { echo "READ NOTHING: not at the repo top"; false; }; } && python3 -I -c 'import sys
p=".agi/nodes/build/skills-agi-research-then-design-SKILL.md.md"
try: t=open(p,encoding="utf-8").read()
except OSError: print("READ NOTHING "+p); sys.exit(1)
parts=t.split("\n---",1)
if not t.startswith("---\n") or len(parts)<2: print("READ NOTHING frontmatter"); sys.exit(1)
fm=parts[0].split("\n")
if "parents:" not in fm: print("READ NOTHING parents block"); sys.exit(1)
i=fm.index("parents:"); par=[]
for l in fm[i+1:]:
    if not l.startswith("  - "): break
    par.append(l[4:].strip())
ok="link_ref: skills/agi-research-then-design/SKILL.md" in fm and "goal:g4.18.2.2" in par
print("F4 met" if ok else "F4 unmet"); sys.exit(0 if ok else 1)'
```
   RUN at the mint's base 19b8cd62d9: exit 1 (READ NOTHING, no node); outside a repo: exit 1. Control (the node with both): exit 0. Mutants, each exit 1: this leaf under next_edges with parents [goal:g4.18.2, idea:engine-skill-doc] (sp's); link_ref skills/agi-workflow/SKILL.md; parent goal:g4.18.2.20.
5. THE GUARD RUNS, read by hand: the skill's worked example RUNS one mutant (a patch that changes one marked owner line is refused, and its unchanged twin applies), and names its READ NOTHING row (a 0 before-count on an owner-line target).

## Out of scope
goal:g5.4.3.1 (the presentation itself) · meme-master's second ask, the council's full pass over the presentation and the A/B (SM's [place] 09:46:38Z 11-10, its own vote) · skills/agi-review's own fan-out (unchanged; the new skill points at it).

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-goals-1 11-10, CLOSE (SM 14:10Z: L503 778ddd3c4f + belam's wrap 16c6934758, DG1's skill chain): every falsifier AS WRITTEN passes at 16c6934758, extracted from '## Falsifier' only, each non-empty. F1 rc 0 (skills/agi-research-then-design/SKILL.md, name line). F2 rc 0 'F2 met' (the description names agi-review and agi-research-then-design, holds neither old phrase; agi-workflow's '- pi by default' bullet and unified-director-brief's REVIEW IN PLACE line hold no forbid and each cites 'just use sonnet subagents'). F3 rc 0 (SKILL.md names no model version). F4 rc 0 'F4 met' (build node skills-agi-research-then-design-SKILL.md.md: link_ref, this leaf in its parents block). F5 by hand: SKILL.md §7 RUNS the guard with the OWNER selector (both markers): ok.patch PASS rc 0; mutant.patch REFUSED rc 1; note.patch (a spoken owner line) REFUSED rc 1, and the one-marker hole shown and named; empty.tex READ NOTHING rc 2; the brief-says-none row PASS rc 0. THE FLOOR (alive, sp, aio), read by hand: the :23 bullet whole (no sub-bullet) holds no forbid and cites the 10-10 words; :60 keeps 'NEVER the Agent tool' scoped 'for this mur run' (term (2)) and names the fan-out route outside it with the cite; no sub-bullet. NAMED, not this leaf's falsifiers: (a) alive's finding 14:09:39Z, skills/agi-research-then-design/example-2026-11-10.md landed with NO build node, so no grid version (CLAUDE.md: a new file under skills gets a node at its mint): DG1's small child, owed; (b) that example quotes 'Fable 5.1/5.2/5.x' inside the run's verbatim prompts and log headers: the run's own record, as F3's note allows; F3 reads SKILL.md only.

director-goals-1 11-10, CHILD 2, of 957bc7580d (sp's AMEND 10:12:04Z, SM 10:12:33Z): F2's half (b) passed four mutants that still forbid the route; now each anchored bullet is read whole, squeezed and case-blind, and must hold the owner's 10-10 cite (the council's term (2) gets its falsifier); the skill names match as exact tokens; F4 reads the parents block only; every falsifier's repo-top guard prints READ NOTHING and keeps rc 1. Nothing else changed.
director-goals-1 11-10, CHILD of 3535432ea1 (council [decision] alive 10:00:48Z, 3/3 YES AMENDED on SM's [place] 09:57:12Z and DG1's three reads): (1) Target 2's count corrected to meme-master's 8 research + 4 design + a version probe named as a probe, with SM's F3 NIT; (3)(b) the design-stage Invariant reworded to the most capable alias the running post is allowed, the director brief's SUBAGENTS rule named by its words (aio ADD, alive ADD); F2 gains the positive half and reads the two other hits by anchor, READ NOTHING on a missing one (sp AMEND); F4 reads the one build node by its house name (sp AMEND). F1, F3, F5 and every other line are the mint's. Mint: drafted from the owner's words (c:e780e4c65887, quoted the L492 way) and meme-master's four stages ([decision] 09:41:22Z 11-10), with every term of the council's [decision] alive 09:47:42Z (3/3 YES AMENDED) placed as Target, Invariant or Falsifier: P1 (this leaf first), A1 (parent goal:g4.18.2), P2 + aio ADD 2 (the cite form), P3 (writer director-general-1), aio ADD 1 (the build node's parent set), A2 (roles and aliases; F3), A3 + sp ADD 1 (agi-workflow narrowed in the same tip; F2), A4 + sp ADD 2 (the guard; F5), sp ADD 3 (no spend over a gap), alive's TERM (declared scale). Next free id read over every ref (g4.18.2.1 the only child). Assigned to the writer, director-general-1.
<!-- THOUGHT:END -->
