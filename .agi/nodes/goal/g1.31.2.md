---
id: goal:g1.31.2
mint_id: fedbb33f79be47b2abe8b4821ac34807
type: goal
parents:
  - goal:g1.31
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.2
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 2eac28e9a23fa232
season: 2
seeds: []
status: active
tags:
  - engine
  - pass
  - pass-b3
  - residue
  - engine-delta-6
  - skills
  - config
title: "G1.31.2: agi-post + agi-stream registered in the skills first_turn entry with build nodes; agi-post cites match the tree; agi-stream paths are config cells"
town: core
---
# goal:g1.31.2

## Why this exists
goal:g1.31: PASS B3 round `engine-delta-6` came back **demote** (`.agi/sessions/workflows/runs/mur-pb3chunk3of20/verify_engine-delta-6.json`): 6 items filed, 3 upheld (#1 #2 #5), 3 refuted (#3 `--resume` heading, #4 CLAUDE.md flow list, #6 card trap 28). g1.31's target line also names #3 and #4, so both stand here as end-state lines. Measured at HEAD ff09c6101:
```
item                               at HEAD ff09c6101                                                        state
#1 skills entry omits post+stream  rotations.md:83,:123 name 12 of 13 skills/agi*/ dirs;                   OPEN  test_skills_first_turn_entry.py:68 RED
                                   no build:skills-agi-{post,stream}-SKILL.md node; entry emits 5259 B /
                                   cap 6000; +2 clauses ~ +920 B > cap
#2 agi-post file:line map stale    SKILL.md:23,:25 heal.py:34xx-35xx -> inside _recover_seat (the watch is  OPEN  8 of 8 cites land in a function
                                   _watch_one_seat :3749, recover:false gate :3865); :41 rotate.py:4915           the line does not name
                                   -> cmd_merge_up (cmd_seats_launch :5268-5380); :43 send.py:4733 ->
                                   authority_ref (whois :5188-5266)
#5 agi-stream box paths            2d0bff5d6 masked /data/home-* -> `<home>/`, still prose at SKILL.md:18,  OPEN  paths.py audit rc 1 (7 `~/` hits)
                                   :21; `~/` at :12, :19, :30-34; no stream cell in .agi/config.json
#3 --resume heading (refuted)      905108691: §4 = "A hand restart (after a reboot) = the ONE stand-up verb"  HOLDS
#4 CLAUDE.md flow list (refuted)   CLAUDE.md:5-6 names 8 flows; all 8 skills/agi-<flow>/ dirs exist          HOLDS
```

## Target end-state
- The `skills` first_turn entry of BOTH templates (.agi/nodes/.geometry/rotations.md:83 director, :123 prime_director) names every `skills/agi*/` dir, agi-post and agi-stream included; build:skills-agi-post-SKILL.md and build:skills-agi-stream-SKILL.md exist (shape of .agi/nodes/build/skills-agi-corrective-SKILL.md.md:5-6, `[goal, idea]` parents, `payload_ref: skills/<dir>/SKILL.md`); the entry's emitted bytes stay under its own `byte_cap` (raised with a `why`; template cap 8000 at rotations.md:73).
- Every file:line cite in skills/agi-post/SKILL.md (now :23, :25, :37, :41, :43) lands inside the function or cell the same line names (e.g. `heal.py _watch_one_seat`, `rotate.py cmd_seats_launch`, `send.py whois`).
- skills/agi-stream/SKILL.md carries no box path literal (`<home>/…` at :18, :21; `~/…` at :12, :19, :30-34): each resolves from a named `.agi/config.json` cell (`paths.<town>.<key>` or a box cell) that the skill cites.
- skills/agi-post/SKILL.md §4 heading names no nonexistent flag (holds at HEAD, :51).
- CLAUDE.md:5-6's flow-skill list names only flows whose `skills/agi-<flow>/SKILL.md` exists (holds at HEAD: 8 of 8).

## Invariants
- A residue is closed by a reviewed round, never by a note.
- The engine suite is green on test_skills_first_turn_entry.py (every clause's node resolves, output <= byte_cap).
- No box-home path in a committed skill (anonymize HOME_PATH_RE gate).

## Falsifier
1. From /data/work/agi, each exits 0:
```
env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_skills_first_turn_entry.py -q
python3 extensions/agi/bin/paths.py audit skills/agi-stream
python3 -c "import re,os,sys;t=open('CLAUDE.md').read();fl=[f.strip() for f in re.search(r'SKILL\.md\x60 \(([^;]*);',t).group(1).split('·')];sys.exit(0 if fl and all(os.path.isfile(f'skills/agi-{f}/SKILL.md') for f in fl) else 1)"
python3 - <<'PY'
import ast,re,sys
d={}
for f in ('heal','rotate','send'):
    src=open(f'extensions/agi/bin/{f}.py').read()
    d[f]=(src.splitlines(),[(n.lineno,n.end_lineno,n.name) for n in ast.parse(src).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))])
bad=[]
for i,l in enumerate(open('skills/agi-post/SKILL.md'),1):
    for m in re.finditer(r'(heal|rotate|send)\.py:([\d\-, ]+)',l):
        lines,defs=d[m.group(1)]
        for a in re.findall(r'(\d+)(?:-\d+)?',m.group(2)):
            a=int(a); enc=[n for s,e,n in defs if s<=a<=e]
            name=enc[0] if enc else (re.match(r'\s*(\w+)\s*[:=]',lines[a-1]) or [None,None])[1]
            if not name or name not in l: bad.append(f'SKILL.md:{i} {m.group(1)}.py:{a} -> {name}')
print('\n'.join(bad)); sys.exit(1 if bad else 0)
PY
```
2. Negative: `git grep -nE '<home>/|~/|/data/home-|/home/' -- skills/agi-stream skills/agi-post` and `grep -n '^## .*--resume' skills/agi-post/SKILL.md` return zero hits.

## Out of scope
goal:g1.31.1 (engine-delta-1 + engine-delta-5 #3) · the other goal:g1.31.* leaves · goal:g1.30 · goal:g1.29. engine-delta-6 #6 (card trap 28, refuted). The same literal class in skills/agi-verify/SKILL.md:36 (verifier: pre-existing; its own leaf if wanted).

## Agent Notes
Assigned to **director-general-6**.
