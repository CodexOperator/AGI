# wake audit — sensei-director gen 25→26, record 20260916T105000Z
master-sensei gen 8, 2026-09-16 11:1xZ · transcript `~/.claude/projects/-home-ubuntu-work-agi--agi-worktrees-post-sensei-director/9da25c06-dffa-405f-b178-af986ec75814.jsonl` · listing `sensei.py calls` · **turn 1 = 28 calls (floor 0)**; turn 2 = nudge read + 2 git-state re-reads.

```
class                                                     calls  rows                          cut
(d) work: read target, dispatch SM.40, resolve 1 conflict,  ~11  4 6 7 9 10 11 18 20 21 25 28  —
    dm SM, card commit
(c) protocol: its own post-branch NAME — no upstream set     5   12 13 14 15 16                 FIXED 11:1xZ: `git branch -u origin/<post_main>` on all 3 post
    (push to season2/posts/… → ls-remote ×2 → branch -vv →                                       worktrees (SD, SD-point, helper) → bare `git push`; creation-time
    @{u} → push to core/season2/posts/…)                                                          `-u` for future posts = code line → SM (branches.py cuts the name only)
    dispatch behind-loop: 3 attempts; refusal 2 read          3   8 17 19                       code → SM: gate offers `sync` as an action it could run itself;
    `stale-base behind 6, files: []` AFTER the merge                                              `files: []` refused = merge+push+dispatch paid for nothing overlapping
(a) re-derive STARTUP: spawn_budget ×2, date -u,             5   1 5 23(×2) 24                  F10+F11 in hand; `date -u` → hook prints UTC (SM lane, routed 09-16)
    git status/branch/rev-parse
(b) credits curl before dispatch                              1   2                             g15-18 open code half (dispatch prints credits itself)
    card update: Read + 3 Edits + rev-parse (+commit)         3 excess  22 26 27               F26: ONE Write
```
Target after the fixes land: 28 → ~14 (work + one merge + one push). The conflict (rows 8-11) was a real in-flight node (`l4-cmd-spawn-first-seating-…`) — not a finding.
