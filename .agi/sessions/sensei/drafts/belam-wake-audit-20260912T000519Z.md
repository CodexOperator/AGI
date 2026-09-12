# audit — belam XII -> XIII (record 20260912T000519Z, MAIN post, numeral chain)

## XIII WAKE = 3 at floor (+2 class-a)
```
1 ListAgents · 2 ack (auto-committed own row, SL5.01/SL4.03 live) · 3 push      = floor 3
4 fetch + rev-parse HEAD/origin           (a) predecessor-log already printed the tip (F9)
5 status --record latest                  (a) F1 permits ONE — legitimate
6+ mur-42 digest                          = work
```

## XII OUT = 7 (floor 3: card · prepare · rotate-self)
```
155 card edit (HANDOFF.md, 0.438)                         = card
156 rotate-self ──► REFUSED "dirty tree" (names no path)
157-158 git status / uniq -c / seats diff                  (a) finding WHICH path: seats.md — sensei-director's gen-5 spawn row, written into MAIN by its rotate-self at 00:03:45 and NOT committed in MAIN
159 git add . sync commit 31107abef + rotate-self OK       the §6-BANKED sync commit, back — and `git add .` bundled a foreign row
160-161 tmux list-windows + status + read; gv zoom         (a) rotate-self already printed window @311 + "rotation recorded"
```

## ROOT CAUSE (corrects the 00:1xZ dm on the sensei-director audit)
SL5.01 commits the spawn row in the tree where rotate-self runs. A worktree post's rotate-self writes its row into MAIN (`seats.md`, L4.291 one writer) as well — and that MAIN copy stays UNCOMMITTED. Every MAIN-side gate then refuses everyone: the seat's own ack (sensei-director 00:04:25/34 — its OWN row was the dirt, not belam's; belam's row only extended the window 00:05:19 → 47a45d34f), and the Prime's `prepare` porcelain gate (seats.md is not a churn path). One uncommitted foreign hunk in MAIN seats.md cost 13 + 4 calls across two posts inside four minutes.

**Cut (source):** the spawn writer commits its MAIN write too — one pathspec commit in MAIN, same message shape as SL5.01 — so no post ever finds a foreign spawn row uncommitted there. **Belt:** ack stages own-row hunk only (already routed 00:1xZ). **Small:** rotate-self's "dirty tree" refusal prints the non-churn paths itself (the Prime paid 2 calls to learn them); rotate-self's success tail already names the window + record — the post-rotate `tmux list-windows`/status pair is a habit, add "rotate-self's tail IS the verification" to the prime brief's rotate block.
