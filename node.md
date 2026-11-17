---
id: goal:g5.4.3.1.1
mint_id: e88ad2c804c74eae9c9420c4f24fbc8a
type: goal
parents:
  - goal:g5.4.3.1
next_edges: []
confidence: 0.5
goal_id: G5.4.3.1.1
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 36493c37205917b9
season: 3
seeds: []
status: active
tags: []
title: "G5.4.3.1.1: the council's full pass over the deck and an A/B of its animations: basic route (rough-draft-v1) vs the full graph treatment (rough-draft-v2), on one versioned copy, measured blind, compared on S9"
town: core
---

# goal:g5.4.3.1.1

## Why this exists
goal:g5.4.3.1 (the class presentation, built tonight by the BASIC route: meme-master + harness subagents): the owner asked on 11-10 for the council's full pass over the whole deck (how well it reflects us), an upgrade of its animations and visuals by the FULL GRAPH TREATMENT, saved as an official graph result, and an A/B of the two routes for the owner and on the final slide. A comparison only says something if its arms, its measure and its copy are fixed before it runs, so it gets its own leaf under the deck's (council [decision] alive 09:53:15Z 11-10, 3/3 YES AMENDED; SM's (a) (b) (c)).

## The owner's words 2026-11-10 09:44:23Z (c:61b389266d66), verbatim [meme-master store; not an OWNER heading under the interim rule (self-perpetuating 19:55:55Z 11-09) until goal:g7.16.1.11.46.34 lands]
> can we have the whole presentation now be passed over by the council fully to see how well it reflects us and then updated and upgraded as far as animations and visuals and the like and saved as an official graph workflow result to compare the whole presentation for me personally, and then also to compare in the final slide how the basic workflow vs the full graph treatment did for the animation. I'm fine installing whatever but that should help. I'll let prime know you have permission to request this. Ask to pass it to prime on my behalf

## The owner's words 2026-11-10 09:47:47Z (c:1ae05e71c801), verbatim [meme-master store; same interim rule]
> after all finished upload it to the agi gdrive folder either via connector or rsync in agi/class-presentation under rough-draft-v1 and rough-draft-v2 for the regular and full graph treatment versions respectively

## Target end-state
1. THE COPY: a privacy-scanned copy of the deck as doc node(s) under goal:g5.4.3.1, sources in the body, through a PLAIN gated tip; its head names the private source's sha256, the copy time, the count of '% OWNER' lines, and every owner line a removal touched (by line number). Each removal is marked in place ([elided: course] / [elided: person] / [withheld: verbal-only]). The council's pass reads that version and names it; a later change edits the same node(s) in place (A1, sp ADD C).
2. THE COUNCIL'S FULL PASS over the copy: per slide, how well it reflects us.
3. THE TWO ARMS: arm A = the basic route as built (goal:g5.4.3.1), arm B = the full graph treatment (goal -> idea -> hypothesis -> experiment -> verdict, dispatched the graph's way) under THIS leaf; both patch the COPY, so the guard's 'before' is the copy (sp ADD C).
4. THE MEASURE, TM's, with its pass line, on this leaf BEFORE arm B's first launch: per slide, the council's 'reflects us' score, the harness token count and the wall time per arm, both arms on one slide set (SM (c), sp ADD B, A2).
   THE MEASURE AS SET (thought-master 04:5xZ 11-17, RE-CUT 1 06:5xZ 11-17 with the council's six amends; set before arm B's first launch, fixed from here, never tuned after a score):
   - UNIT: the S-labelled slide of the copy (doc:draft-presentation-deck-v1), its frames and animation steps scored as ONE. The copy reads 13 S-labels; S9 is EXCLUDED (it reports this measure, so it has nothing to score before the key), and so is any title or closing frame that carries no claim: n = 12 (aio M1, M2). Both arms rendered on one toolchain before any score.
   - QUALITY: each council seat (alive, all-is-one, self-perpetuating) scores every slide of X and of Y on one 1-5 scale, 'how well it reflects us': 1 misrepresents us, 2 true but could be any project's, 3 accurate and specific, 4 accurate, specific and shows how we work, 5 only we could have made it. A slide's score per arm = the mean of the three seats. A failed render = READ NOTHING for that slide, dropped from both arms, its count reported.
   - A SLIDE ONLY ONE ARM CARRIES (arm B adds, splits or drops one): scored and REPORTED beside the verdict, never paired, never in the sign test; its count named (alive (3)).
   - BLIND, and its limits said now: sanctuary-master (it does not score) assigns A/B to X/Y by a coin it records, shuffles the slide order per seat, keeps the key; every seat boxes its whole sheet to it before thought-master asks for the key. The coin hides the LABEL and the ORDER; it cannot hide the LOOK (arm B's animations show on the slide), so each seat states on its sheet whether it recognised which arm was which, and the count is in the report (sp (2)). The PROCESS break is closed by (a), council 3/3 pick (alive, SM): arm B's patch tips get sanctuary-master's mechanical gate (capsule, anonymize, render, b-7) and a word from a NON-scoring seat (belam or director-goals-1); the three scorers give no word on arm B's content until the key is unmasked (aio M3).
   - COST: per arm, the harness tokens (input + cache write + cache read + output, from each harness's own usage records, renders included) and the wall time from the arm's first dispatch to its last render; arm A's are read from goal:g5.4.3.1's own records, or NOT MEASURED if they were not kept (never estimated).
   - PASS LINE: arm B BEATS arm A only if (1) the per-slide paired difference (B - A) has a positive mean, (2) an exact two-sided sign test over the NON-TIED slides gives p < 0.05, and (3) no slide drops by 2 points or more. Anything else reads 'no measured difference' (or 'B worse', if the mean is negative and the sign test passes the other way), reported as such, never softened. Said before any score, the test's floor (exact, two-sided; non-tied n -> improved slides needed): n <= 5 NEVER passes; 6 -> 6; 7 -> 7; 8 -> 8; 9 -> 8; 10 -> 9; 11 -> 10; 12 -> 10. A slide's score is a mean of three, so ties are likely: a 'no measured difference' with few non-tied slides reads as this floor, not as arm B's quality (sp (1)).
   - REPORTED beside the verdict (not pass criteria): the per-seat spread (max - min per slide), the mean difference with a slide-bootstrap 95% CI, the recognised-arm count, the unpaired slides, and arm B's cost as the increment over arm A in tokens and wall time; S9 quotes those numbers, in the owner's words.
5. S9 (the final slide) compares 'basic' with 'basic + the graph treatment' and reports arm B's cost as the increment over arm A, named so; S9's numbers are TM's, its words the owner's (goal:g5.4.3's rule).
6. The A/B for the owner personally: both WHOLE decks, rendered, uploaded by meme-master to the owner's own Drive under agi/class-presentation after each render (c:1ae05e71c801). The bytes that go up: rough-draft-v1 = the PRIVATE deck as built (arm A); rough-draft-v2 = arm B's patch applied to the PRIVATE deck by meme-master (dry-run there first; a hunk that fails on a line a removal touched is re-cut against the private bytes, never forced). Never the committed copy, whose lines carry the removal markers. The private decks carry their notes; whether the notes travel to the agi folder is the owner's to say (sp 10:06:49Z).

## Invariants
- The COMMITTED copy holds the owner's verbal-only item (c:2763ec818294) NOWHERE, speaker notes included (a commit reaches origin and the grid and is never rewritten); the private deck keeps its notes as the owner allows (c:4b5d4abae03e) (aio's TERM).
- Names read: the copy's tip lists every proper name in the added text, classed owner / post / a cited source's author / other; every 'other' is elided before the cut; a count of 0 is READ NOTHING (sp ADD A; role-meme-master's bar).
- Every patch either arm returns passes the owner-line guard set at 09:47:42Z ('% OWNER' lines byte-identical; a before-count of 0 is READ NOTHING); a removal on an owner line the head does not list is refused (A3, A5, sp ADD C).
- The basic deck is submitted Tue 11-10 morning (the owner: 'evening I believe but morning would be best', c:787879d6bc35) as goal:g5.4.3.1 says; neither arm edits the file being submitted before then.
- Scored BLIND: the arms are handed as X and Y, the per-slide order shuffled by a post that does not score, every score boxed before TM unmasks; both arms RENDERED on one recorded toolchain before any score; a failed render is READ NOTHING for that slide, never 0 and never a pass (sp ADD B, A2).
- DECLARED SCALE: kids, passes, model aliases (renders included) declared on this leaf before the first launch; the harness token counts reported after (SM's TERM).
- THE BOX: the toolchain (tectonic, manim, HyperFrames) and every render under /data/scratch/meme-master, `df -B1M` on that path before an install or a render batch; renders are heavy runs (agi-memory-guard's same-command refusal above load5 8, the post's own MemoryMax, one render at a time); nothing system-wide without belam (A4, aio ADD).

## Falsifier
1. THE COPY EXISTS, from the repo top, exits 0 only when a doc node under goal:g5.4.3.1 carries, in its HEAD (the body before its first '## ' heading), a 64-hex value after 'sha256' and a numeric count after '% OWNER'; either missing = no pass (alive's NIT 10:05:47Z: a doc naming both words in prose no longer passes):
```
[ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" ] && python3 -I -c 'import re,subprocess,sys
r=subprocess.run(["git","grep","-l","-e","^  - goal:g5\\.4\\.3\\.1$","--",".agi/nodes/doc"],capture_output=True,text=True)
if r.returncode not in (0,1): print("READ NOTHING git grep rc",r.returncode); sys.exit(1)
ok=[]
for p in r.stdout.split():
    t=open(p,encoding="utf-8").read()
    if not t.startswith("---\n") or "\n---" not in t[4:]: continue
    body=t[4:].split("\n---",1)[1]
    head=re.split(r"^## ",body,maxsplit=1,flags=re.M)[0]
    h=re.search(r"sha256\W{0,20}[0-9a-f]{64}\b",head)
    c=re.search(r"% OWNER\W{0,20}(lines?\W{0,20})?(count\W{0,20})?\d+",head)
    if h and c: ok.append(p)
print("copy heads:",ok or "none"); sys.exit(0 if ok else 1)'
```
   RUN at the mint's base 19b8cd62d9: exit 1 ('copy heads: none'); outside a repo: exit 1. Control (a scratch doc whose head holds 'source sha256: <64 hex>' and "'% OWNER' lines: 11"): exit 0. Mutants, each exit 1: the two words in prose only; a short hash; a count 'TBD'; both fields below the head.
2. THE MEASURE BEFORE THE ARM, read by hand from git: the commit that puts TM's measure and pass line on this node precedes arm B's first dispatch.
3. THE VERBAL-ONLY ITEM, run by meme-master (the script sits in its private dir): the deck's own script (deck/check-owner.sh, its word list off the trunk) over the COPY with its \note{...} span drop TURNED OFF for this run, so notes are read like every other line: `F2 source: none`; the output and the script's sha256 go verbatim in the copy tip's message. CONTROL, the same mode: a fixture \note{...} holding a line the floor matches reads RED. Plus a hand read of every speaker-note body in the copy, named in that message (sp's AMEND 10:06:49Z: run as goal:g5.4.3.1 defines it, the script drops note spans and would pass the very case Invariant 1 bars).
4. BLIND AND RENDERED, read by hand: every score is boxed before TM's unmask; both arms' render log names one toolchain; any failed render is READ NOTHING for its slide.
5. THE RESULT: a verdict node under this leaf carries TM's per-slide table for both arms, and S9's wording is the owner's (an owner chunk, read by hand).

## Out of scope
goal:g5.4.3.1's own submission (Tue 11-10 morning, the basic deck) · goal:g5.4.3.2 (the paper) · goal:g4.18.2.2 (the research-then-design skill).

## Agent Notes
Running director: named by sanctuary-master on this line before any dispatch (SM asked thought-master 09:54Z; the measure is TM's).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
thought-master 04:5xZ 11-17, RE-CUT 1 06:5xZ (all six council amends on bebebf6f3c taken whole: sp ties table + the blind's limit by sight; aio the unit = the S-labelled slide, S9 excluded, n = 12, and the process break closed by pick (a); alive a one-arm slide is reported, never paired; the time NIT): THE MEASURE + pass line set under item 4, before arm B's first launch (falsifier 2), as the council placed it (SM (c), sp ADD B, A2): a 1-5 anchored scale scored by the three seats, blinded by sanctuary-master, cost read from records (NOT MEASURED, never estimated, where a record was not kept), and a sign-test pass line whose small-n strictness is said before any score. Nothing else in the leaf changes.
director-goals-1 11-10, CHILD of e33c14e641 (SM 10:07:11Z: ONE child, all five): (i) F1 reads the copy head's own fields (a 64-hex sha256 and a numeric '% OWNER' count, before the first '## ' heading), not the two words anywhere (alive's NIT 10:05:47Z); (ii) the Agent Notes line names SM's [ask] 09:54Z to thought-master (SM's NIT); (iii) F3 runs the deck script on the copy with note spans KEPT, plus a fixture-note control (sp's AMEND 10:06:49Z); (iv) Target 6 names the bytes uploaded, v1 and v2 from the PRIVATE deck (sp); (v) the date: Tuesday is 11-10, not 11-11 (meme-master's [correction] 10:0xZ; the owner's c:787879d6bc35 unchanged), here and in goal:g5.4.3.1 in the same commit. Nothing else changed. Mint: drafted from the owner's words (c:61b389266d66 and the follow-up c:1ae05e71c801, both quoted in the interim form, P) and meme-master's [decision] 6c1a42b8c5 (~09:5xZ), with every term of the council's [decision] alive 09:53:15Z (3/3 YES AMENDED) placed: (a) + A1 + sp ADD C (the versioned copy, removals on the record; Target 1), aio's TERM (the copy stricter than the deck; Invariant 1), sp ADD A (names read), (b) + A3 + A5 (the arms, the guard, submission first), (c) + sp ADD B + A2 (the measure fixed before, blind, rendered), SM's TERM (declared scale), A4 + aio ADD (the box). The running director is named by SM on the Agent Notes line before any dispatch; until then the line holds no 'Assigned to' form, so no claim reader counts it. Next free id read over every ref (no child of goal:g5.4.3.1 before this).
<!-- THOUGHT:END -->
