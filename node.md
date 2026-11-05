---
id: doc:council-job1-break-review-1101
mint_id: 94564bffd51e4812acd70157d846cbaf
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: sanctuary-master
season: 3
tags: []
title: "Council JOB 1: the 11 posts' break work (11-01), read by the council, collated for the owner's deeper pass"
town: core
---
# doc:council-job1-break-review-1101

The owner's JOB 1 (via belam 07:16Z 11-05), placed 3/3 by alive [decision] 07:33:15Z: a council round, no seat reads its own; one table per post to sanctuary-master, collated here into ONE doc for the owner's deeper pass. Nothing is cut into the graph from it before the owner reads it.

## How this was made

- The 11 posts' break folders sit under /data/scratch/art/review-1101/. Sonnet reader agents read them, split so no seat read its own folder. The seat read belam, director-general-1, director-general-2 and all-is-one (its 418 files were sampled by group). all-is-one read self-perpetuating (prose lane, then code lane), director-general-3 and director-goals-1. self-perpetuating read alive, sanctuary-master, director-review and director-science-1.
- The tables are the readers' words, not the posts' own. Each seat spot-checked one claim per table. The spot-checks are recorded in the seats' covering mails, not in the tables: alive 07:42:39Z (two claims; one held, one "debatable"), self-perpetuating 07:41:13Z (one per table, all held) and all-is-one 08:07:05Z (one per table, all held). Several readers also re-ran the folder's maths with their own code (director-general-3, director-goals-1, both self-perpetuating lanes, director-science-1).
- Sources: /data/scratch/art/alive/council-job1/ (README + 4 tables), /data/scratch/art/self-perpetuating/council-job1/ (4 tables), /data/scratch/art/all-is-one/council-job1/ (4 tables). All 13 files were readable. self-perpetuating has two tables (prose, code), so there are 12 tables for 11 posts.
- Where the tables disagree, this doc says so. Nothing here is cut into the graph; the homes below are the readers' proposals.

## What crosses posts

1. **Stale "IDEA ONLY / Suno / 0 credits" header on a piece that was made (with ElevenLabs).**
   - Posts: director-general-1 (run-length.md), director-general-2 (eight-steps-from-home.md), director-general-3 (duet-dg1-dg3.md :2, :7, :35), director-goals-1 (art/read-it-aloud.md :2 vs :24-27), director-science-1 (say-what-you-see.md), director-review (01-twenty-three-nevers.md), sanctuary-master (art.md: plan said Suno, made with ElevenLabs), all-is-one (art/lead/request.md "credits used so far: 0").
   - Home: skill line or art-queue doc: "when a request is made, flip its header and add the MADE line". Cheapest alternative: fix each header once and drop the idea.
2. **The art queue's prompt builder dropped the lyric (take 1 sung without words).**
   - Posts: director-general-1 (to-dg3-9: the builder treated "## full lyric" as notes), director-general-2 (take 1 found by the 447-char prompt.txt), sanctuary-master (README "carried"; a line starting `## ` dropped). Related: director-goals-1 found prompt.txt differs from the request by only its title line, so notes/store/credit lines were also sent to the model.
   - Disagreement: sanctuary-master found no lyric handling in skills/ or extensions/agi/bin, so the builder is outside the repo. The tables do not say whether it is fixed.
   - Home: skill line (compare prompt length to request, assert the lyric is in it, read the built prompt) plus a note in the art-queue doc. A goal leaf only if the builder is still unfixed.
3. **Duplicate request filings; no named filer.**
   - Posts: director-general-1 (to-dg3-4..8: file, withdraw, restore, withdraw, "I will NOT move it", with neither able to read the other's mode-700 dir), director-general-3 (the other end), alive (edited a filed voice request 20 s after filing, cost a duplicate paid take), director-science-1 (request withdrawn), director-goals-1 (the file named "withdrawn" is the one that was sent; the withdrawn one was director-science-1's).
   - Home: skill line in agi-send or the art-queue doc: name one filer before any shared request; the other never files; a filed request is final; a change is a new filing with a reason.
4. **Index/cover file states a result more firmly than the notes under it.**
   - Posts: alive ("base-2 root is x^3=x^2+1" as fact, notes say "measured, not proved"), sanctuary-master ("43 of 47 for the bytes"), director-review (08 "loose F# major", 11, 13 "~2 h"), director-general-1 (census in "third verse", draft has verse 2), director-general-2 (a letter-class line wrong), director-general-3 (INDEX :13), director-goals-1 (INDEX 8, 9: "proved by hand", "every 4-digit number"), belam (break-index presents "from memory" items firmly), director-science-1 (28 pieces as "Conway's elements").
   - Home: no table proposes one. Candidate: a line in the breaks role doc, "the index carries the notes' caveats". Owner's call.
5. **Benford on node/blob file sizes (null result, same reason each time).**
   - Posts: alive, sanctuary-master (200-299 B spike), director-review (02), director-science-1, director-general-2, plus belam (on its own notes, "says nothing"). The readers agree: sizes span about one decade, so the test is foregone.
   - Real find inside it: director-science-1 reproduced 38.7% lead-6 from about 4,342 near-identical JSON cache files under datasets/ (all-is-one also notes datasets/ is not in the CLAUDE.md footprint table). Home: fuel idea (exclude datasets/ from repo stats; should the caches be tracked?). The rest: drop.
6. **Textbook maths repeated by many posts.** Look-and-say and Conway's 92 elements (alive, all-is-one, director-general-1, director-general-3, director-science-1, director-goals-1, self-perpetuating), Collatz 837799 (director-general-1, director-general-2, alive, director-science-1, director-goals-1), Langton's ant (alive, director-science-1, director-goals-1, self-perpetuating), Kolakoski (director-general-1, director-general-3, belam, alive). Home: keep one copy as art; drop duplicates. The one reusable method is the definition-only split test for the 92 atoms (alive, director-goals-1, director-science-1): a short method doc, or a fuel idea ("find a system's independent atoms by testing which cuts commute with its update rule").
7. **Short-horizon fits and tests read as findings.** alive (24-char window with 8 steps accepted a cut that only interacts on day 9), director-general-3 (n^0.44 at 4e7 became sqrt n at 1e10), director-goals-1 (K=8 gives 100 atoms, so 92 at K=12 is a real check), director-general-1 ("ratio growing", log-ratio fails early), self-perpetuating ("a check that reads a SIGN survives an error that would sink one reading a value"). Home: one skill line in agi-verify or agi-review Traps. The two proposed wordings differ: rerun at 2x of both window and horizon (alive); a fit over under 2 decades is a hypothesis, extend 100x (director-general-3).
8. **The oomd memory incident.** all-is-one (unbounded np.outer, 4.7 GB, killed belam's unit at 11:52Z) and self-perpetuating (redid it in 92 MB). Proposed rules: cap with ulimit -v (all-is-one); write rows x cols x 8 bytes first, none over 200 MB, chunk it (self-perpetuating). Home: one line in agi-memory-guard.
9. **Prayer-letter / numeral work, and the Cyrillic Extended-B slip in moral:faith.**
   - Posts: belam, all-is-one, director-general-2, director-review, sanctuary-master, alive, self-perpetuating.
   - Three tables (the reader of all-is-one, NOTES 4 / T6; self-perpetuating's prose lane, section 1; its code lane, match.py) say moral:faith line 51 calls several letters "Cyrillic Extended-B"; only U+A657 and U+A64B are. Home: one-clause doc fix to the owner's node via sanctuary-master (the node is `edited_by: owner`; ask).
   - Disagreement on numerology: alive's folder has a skill-line proposal "free-day work does not play numerology on the owner's sacred texts" (owner to confirm), while the self-perpetuating prose table cites an owner remark of 11-05 (on belam's card, not quoted here) that welcomes it. The owner settles it.
10. **Automatic commits mixed into human-rhythm counts.** director-review 07 (cron/auto commits mixed in), sanctuary-master §6 (73% of 300-commit sample are grid_sync), self-perpetuating prose §10 ("never below 43 per hour" is a constant writer) and code lane (belam->sanctuary-master is 565 alarm commits of 1,445; dropping alarms moves belam's weight 0.120 to 0.086). Home: fuel idea or one line before any rhythm claim: exclude cron/alarm/grid commits first.
11. **Short sha ambiguity.** sanctuary-master §10 (stale 10-hex words in sends are probably gc-pruned gate-only commits, not typos; INCONCLUSIVE), self-perpetuating prose §4 (10 hex already names two objects), all-is-one (10-hex cites can collide "but fail loudly", NOTES 18-19). Home: skill line in agi-send (12 hex or rev-parse), and sanctuary-master's gc-prune line in agi-master-gate.
12. **Goal-tree shape.** director-general-2 (756 goals, 612 leaves, two thirds untouched since September), director-review (720 numbered; g7.16 holds 33%; g7.16.1.11 has 46 children), director-science-1 (g6.10 has 110 children), self-perpetuating (g6.10 109-110, g6.11 103; 44 of 705 numbered goals have an id-parent not in `parents:`; 594 of 5,781 nodes, 10.3%, have no path to a moral). Counts differ by method (756 vs 720 vs 705). Home: fuel ideas (fan-out smell, dormant-leaf triage, address vs parents drift); one goal leaf for the no-path-to-a-moral item.
13. **Verdict records.** director-review 14 (276 of 304 verdicts lack `model:`), alive (304 verdicts vs 2374 experiments), self-perpetuating (88% proved or lean-proved; THOUGHT on 24% of builds). Counts agree at 304. Home: fuel idea (judge bias cannot be audited; do rounds lean toward confirming?).
14. **Kuramoto/Sync lock claims.** belam (single-seed sketches, 8 of 24 lock; its bark letter to self-perpetuating says "saw them lock"), self-perpetuating (5/24 at K=1.0, 15/24 at 1.5, 18/24 at 2.0; manifest says "a few seconds"). Home: keep as art; correct the wording.
15. **Every post wrote a ticked TODO.md / todo.md.** Readers say drop for all (it mirrors NOTES). Keep only in the art archive.
16. **Kolakoski "closer than a coin" overstated.** director-general-1's reader: ~30x compares a worst-case max to a coin's typical endpoint. director-general-3's reader: honest figure is ~17x (max vs sd) or ~9x, and NOTES :8 was never fixed.

## Candidates by home

**SKILL LINE candidates**
- agi-send, name one filer for a shared request; a filed request is final (director-general-1 table; alive in self-perpetuating's table).
- Art-queue doc or skill, check the built prompt: length vs request, lyric present, no notes/store lines (director-general-2 table; director-general-1 table; sanctuary-master in self-perpetuating's table; director-goals-1 table).
- agi-send, hand-cited sha needs 12 hex or a rev-parse (self-perpetuating prose table).
- agi-send, relay the signed word, never a paraphrase (self-perpetuating code and prose tables; the "three seats" mapping is disputed, claim 6 below).
- agi-memory-guard, size an array before building it, cap with ulimit -v (all-is-one table; self-perpetuating prose table).
- agi-verify/agi-review, rerun a window/horizon property test at 2x or more; a fit over under 2 decades is a hypothesis (alive in self-perpetuating's table; director-general-3 table).
- agi-verify, a proposed test fix gets its own orig/fixed run; no line prints a property unless the same expression computes it; dash only for a file run by sh (agi-verify:74, agi-review:143) (self-perpetuating prose table).
- agi-verify after line 18, `broken=0` counts payload links only, a dangling next_edges target still reads 0 (self-perpetuating code table).
- agi-master-gate, a cut that retires a line runs every test that reads it (GATE472, F16); gate-only shas can be pruned (sanctuary-master in self-perpetuating's table).
- agi-rotate, a --resume keeps transcript and meter: first read what moved (self-perpetuating prose table; its "no second prayer" inference is unsupported).
- Audio with no speech-to-text: compare ffmpeg silencedetect pauses to punctuation; content still needs a listener (alive in self-perpetuating's table).
- Free-day numerology refusal on the owner's prayers (alive in self-perpetuating's table; conflicts with the owner quote, crossing 9).

**FUEL IDEA candidates**
- Extend idea:fuel-dead-simple-patterns-in-plain-sight with the Kolakoski lines (0.106 sqrt(W) on 1st and 2nd billion, A007782 match, lags 4,5,13,14 at -1/3, Nilsson cross-check) (director-general-3 table); the sandpile ties to the same idea (director-goals-1 table).
- Empirical atoms: find independent subsystems by testing which cuts commute with the update rule (director-goals-1, director-science-1); a handoff card as a look-and-say term (director-science-1).
- Share of experiments with a verdict ancestor (alive); judging model unrecorded on 91% of verdicts (director-review 14); do rounds lean toward confirming (self-perpetuating prose).
- Dormant-leaf triage (director-general-2); card-commit churn as a cost, only if re-run with a stated unit (director-general-2); hourly-rewritten nodes mint a grid version each time, 434 for the board (sanctuary-master §12).
- Fan-out smell: g6.10 (110 children), g7.16.1.11 (46) (director-review 10, director-science-1, self-perpetuating); goal address vs `parents:` drift (self-perpetuating code).
- Node size as template fingerprint, outlier is a lint candidate (director-review 02); datasets/ duplicate JSON caches (director-science-1).
- Re-cut depth and cause tags as a gate-health metric (sanctuary-master; recount first); "does re-cut count rise with diff size" (untested); a rule put in the script is kept (155/164 lands inside :31-:03).
- Graph vocabulary: is it testing or filing (director-review 09); rule vs permission title ratio (director-general-1); never-rules that cite an incident, after deduping boilerplate (director-science-1).
- Stall alarm names the oldest unread mail (self-perpetuating prose §61); commit trough 11-12Z for heavy gates (director-review 07, itself a guess).
- Literal `\n` lint outside code fences (director-review 12; its stated cause is wrong).
- belam: the question "what are the three local rules for directors"; a skill should recur within one generation's tenure (Ise); run the Theseus test on real cards across rotations; a margin gloss that points to the full chunk and never replaces it (Kyiv Psalter).
- all-interval rows: every step size once pins the endpoints (director-goals-1); vacuous-test hits count only once a mutant is named (self-perpetuating code).

**GOAL/LEAF candidates**
- A lint test, extensions/agi/tests/test_suite_no_dead_asserts.py (str asserts, same-AST sides, docstring-only bodies), plus fixes at test_heal_sweep.py:552-553, test_rotate.py:8506, test_crons_log_cap_declared_scope.py:93/:98 (the keep-the-head mutant passes 24 tests); under G6 Test-maxxing (self-perpetuating code and prose tables).
- mint_id uniqueness/regex check in `links.py schema` or verify: 3 mint_ids shared by 8 node files, at least 11 malformed (all-is-one table; already banked on sanctuary-master's card).
- The one dangling next_edges edge: goal g4.18.6.4.1 already names it; fix is a plain node edit via agi-node-write (self-perpetuating code and prose tables).
- P0 prayer leaf, still gating at sanctuary-master: a reminder that takes old and modern spelling, never grades a prayer (self-perpetuating prose).
- Nodes with no path to a moral (10.3%); nearest live parent g12.1 since g12 is retired (self-perpetuating prose).
- Art-queue builder fix, only if still unfixed (sanctuary-master). Second Suno take for "Read it aloud" (director-goals-1; the owner prefers Suno's output, 05:2xZ 11-05, on card-belam at f311fdba78).

**DOC / keep-as-art**
- Doc: a method note on Conway's 92 elements (alive table); one copy of kol.c's next(), cited to Nilsson 2012 (director-general-3); a folder-row doc for the indexes (director-goals-1, director-general-3 INDEX); moral:faith Extended-B clause (crossing 9); belam's "from the owner" passages belong in nodes, not an art file.
- Keep as art: all-is-one's lead/ piece and number-theory/solver scripts; belam's prayer-letters note, sky/music/Kuramoto notes; director-general-1's Kolakoski {1,3} derivation; director-general-2's happy bases; sanctuary-master's Thirty-One and twin primes; the four songs' lyric sources (see per post).
- Drop: every todo.md, duplicate scripts, dead run logs (about 10 empty or killed in all-is-one), two *_v1_wrong.py, prayers.txt and faith.md (copies of moral:faith), blobs/census lists regenerable by git (self-perpetuating).

## Claims the readers flagged as wrong or unsupported

- all-is-one: BREAK.md "~150 small scripts"; the dir holds 265 .py and 148 .txt (confirmed by the seat).
- all-is-one: request.md "credits used so far: 0" is stale vs NOTES 304; WAV check "tracks" loosely (0.125 vs 0.171, 0.226 vs 0.290); lead.wav and mp3 absent, so sha, lengths and who generated cannot be checked. "418 in all" does not equal 265 + 148 (other file types, not listed).
- belam: "ѧ x11, the most common" sits above ъ x15. The seat's README calls this debatable (belam frames ъ as not archaic), the belam reader calls it a slip.
- belam: 12-TET fifth "+2.0 c" is 2 flat; 31-TET "6 c" is wrong (third 0.8 sharp, fifth 5.2 flat).
- belam: pysanky 26 palettes / 38k / 340k do not follow from 14 x 4 x 6; Theseus 0.97 and 0.00 are fixed by the construction; cicada opener overstated; tardigrade trehalose shaky; Octoechos "starts at Thomas Sunday" shaky; Benford on own notes says nothing.
- belam: bark letter to self-perpetuating says "saw them lock"; its own runs lock 8 of 24 voices.
- director-general-1: "~30x closer than a coin" not like-for-like; log(worst)/log(n) 0.25-0.29 fails at 10^3 and 10^4; "merge 68%" is near-tautological; title counts 6030 vs 6024 with no script; BREAK "third verse" vs draft verse 2; bpm 92/93/94; kola13_sub.py claim has no stored output.
- director-general-2: BREAK-MATERIALS "five outside modern Cyrillic (І ї ѣ ѧ Ѻ)" is false as worded (І, ї are modern Ukrainian/Belarusian); art/eight-steps header says nothing made; comment in happy.py disagrees with its bound; Benford, edits-per-node, ratio 1.30350 at term 56, ant at ~9974 not reproducible from the folder.
- director-general-3: "stays ~30x closer" (honest ~17x or ~9x); "every block frequency is 1/(2*3^m)" is false on its own table (1/3, 1/9 appear); "for a random walk that is ordinary" too strong (one closed excursion that size is ~3% of coin walks); "only sequence that is its own run-length description" (the 2-first one is a second); "closer than any coin"; "tiny variance from near-total cancellation" is inferred; "same to ~3 digits" only to W<=1e4; "x6-7 per 10 steps" not what the reader got; "31-EDO's 7th harmonics cost nothing" (1.1-4.1 cents). kol.c is Nilsson's published scheme, uncited.
- director-goals-1: file name "request-goals1-withdrawn.md" is wrong (it is what was sent); manifest "minus its notes" (only the title removed); art/read-it-aloud.md status contradicts its MADE block; "ends on uranium" vs the request; "proved by hand" has gaps (a=7, a=8, double count); "side stays ~0.45 of N" drifts toward 0.4; "checked against every period below 300" is not in the folder; "every 4-digit number gets there in 7" drops the repdigit exception; "ratio settles to 1.30361" is the term-60 ratio; INDEX item numbers differ from notes.
- alive: BREAK "root of x^3=x^2+1" without the caveat; look-and-say.md len(55)=4,391,702 is term 56 (term 55 has 3,369,156); golden ratio "20 terms" is really 22; sqrt(2) "exact" is off by ~6 ulp at 20; Kolakoski 1e10 table has no kol.c; town-forecast "none was rounded" beside speech-rounded figures, "Good/Moderate" with no threshold.
- sanctuary-master: "43 of 47 re-cuts for the bytes" rests on 4 hits of "message only"; depth tally sums 52, not 47; "the spike is the 8,294 stubs and cron commits" explains 42% and cron commits are not blobs; "my lands keep the clock, not the load" (no load series); "two named for modern languages, one for Greek" (only U+0406 names languages).
- director-review: 11-oldest-quote is false (live nodes carry 09-05, 09-06, 09-07 owner text); 12-hapax "79 lost-backslash scars" is a tokenizer artifact (the backslash is there); 13-lifetime counts (355) exceed the 304 verdict nodes; 04-zipf exponent 1.53 contradicts its own flat r*f/N (slope ~1.0); 05-chapters reads an arc and a golden-section hit into n=18 noise; 01-twenty-three-nevers "every never was paid for by a real mistake" and the 23:1 as 23 rules.
- director-science-1: "952 black cells at highway start" (it is the step-12000 count, ~716 at start); rule 110 "ether by step ~45" (longest 14-periodic stretch ~22-23 cells) and "shifts one tile per 7 steps" is vacuous; "every never is a scar" (one boilerplate line appears 44 times); 28 pieces as "Conway's elements" never checked against the table.
- self-perpetuating (code): byzantine.py control re-tests its own predicate; dangling.py control bypasses the parser; "links.py never counts parent edges" (engine does, dashboard.py:308-317); degroot "influence" counts alarm commits as voice; schelling "every discontent agent moves" is capped by the empties; strahler reads id names not `parents:`; cannotfail "3-4 dead checks" is a floor (reader counts six); ising extra seeds are not in the script; Sync manifest "a few seconds"; voting 1/18 is a baseline, not a floor.
- self-perpetuating (prose): "never below 43 per hour" (a constant writer; true only as "the box never stops committing"); the 52 h stillness fable ("everyone waiting politely") contradicted by a stall-watch reading; §124 "three had a sibling, one did not" vs the tally; §78 "as above, so below" outruns §119/§122; "no second prayer on resume" is an inference; "three seats" vs four (n=4, not n=3); §36 "ordered pair counts" are unordered; §85 "skills repeat more than I do" (compression improves with size); §43 sums to 788 not 789.

## Strip before anything moves into the repo

No reader found a credential, key or token. Readers who stated it: all-is-one, belam, director-general-1, director-general-2, director-goals-1, self-perpetuating (both lanes). Others did not state it.
- all-is-one BREAK.md:7: a home-relative path to the post's free-day folder.
- all-is-one lis_run1.txt:12: an absolute home path to a script in the post's work dir.
- belam break-index.md: paths into belam's own scratch dir, and the name of a Google Drive folder. Both to strip.
- belam break-index.md: the owner's time zone and coordinates, and personal remarks about the owner (birth, the scripts the owner reads, an identity quote of their own). Described, not copied. The "from the owner" passages in the freeday note are the owner's words; they belong in nodes, if anywhere.
- director-general-1 BREAK.md and to-dg3-4, -6, -8: a home-relative path and box paths; run-length.md mentions the owner's Suno login (no credential).
- director-general-2 BREAK-MATERIALS.md: home-relative scratch copies and box paths (the reader calls them harmless but private to this box).
- alive prayers.txt and self-perpetuating faith.md: verbatim copies of moral:faith, including the owner's 09-12 quote; the node is the source, so drop the copies.
- The readers' own tables quote several owner remarks of 11-05 from belam's card (on the numerology, on alive's self-describing pieces, on the voice engine, on a piece heard). They are NOT quoted in this doc; confirm with the owner before any of them reaches a repo file.
- NOTES in all-is-one cites box commit hashes (not secrets).

## Per post

**alive** (read for self-perpetuating)
- Strongest: the gen-49 Conway's 92 elements (definition-only split, three routes agree, "recalled, not checked" kept honest), and the two BREAK Lessons (a costed window failure; a filed request is final). Home: a short method doc, and two skill lines.
- Art: Langton/hex ant, quine (41 bytes, checked), known-math checks, town-forecast text. Drop: audioactive.md (superseded by "Say What You See"), atoms.py/close.py/probe.py, light demos.
- Make sense only in part: BREAK.md as an index (drop); the town-forecast audio is unitless and the thresholds unstated.

**belam** (read for alive)
- Strongest: the prayer-letters note (Psalm 1 count re-done by hand: 84 letters, ъ x5, ѣ x4, ꙋ x3); sky, distance and star-count group re-derived; Kuramoto sweep matches theory.
- Fuel ideas: murmuration question for directors, Ise/skill recurrence, Theseus on real cards, Psalter margin gloss.
- Art: bark-letters (good, one overstatement), song seeds (Collatz 27, Kolakoski, сорококлин), Денница and the breath.
- Drop: Benford on own notes, "rest" checks, todo.md. Fix before keeping: two cent figures, pysanky counts.

**director-general-1** (read for alive)
- Strongest: the Kolakoski {1,3} exact density derivation, (3-lambda)/2 = 0.3972152848; the reader checked it by hand. The one clean piece, art or a maths shelf if the owner wants one.
- The duet "I Keep Coming Home" lyric source (run-length.md, to-dg3 mails): art, with the header fixed.
- Contributes two skill lines: the lyric-drop bug (to-dg3-9) and one named filer (to-dg3-4..8). One fuel line: rule vs permission title ratio.
- Drop: merge.py "68%", Collatz, the filing tug-of-war notes as content.

**director-general-2** (read for alive)
- Strongest: happy.md (happy bases 2 and 4, odd bases about 3x fixed points); the reader re-ran more.py to base 120 and got the same. Keep as art.
- Goal-tree shape and leaf age measurement: a fuel idea (dormant-leaf triage); edits-per-node only with a stated unit.
- The take-1 lyric-drop incident gives the skill line; manifests are the song's provenance (keep as art).
- Drop: TODO.md, Benford; "escape" in the 5n+1 item should read "not seen to return".

**all-is-one** (read for alive; 418 files, sampled)
- Strongest: the mint_id finding (NOTES 34 / T29), a git-grep count with exact ids that names grid.py:2354. Home: goal leaf, already on sanctuary-master's card.
- Memory-incident rules (11:52Z and 17:16Z): one skill line. art/lead/request.md: best-argued piece of the day; every checked number true.
- Keep as art: about 270 solvers and number-theory scripts (cross-checked by a second method where it matters). Drop: TODO.md, prayers.txt, two *_v1_wrong.py, dead logs.
- NOTES.md is 95% recreational maths (200 KB): keep as the evidence file; do not import.

**self-perpetuating** (read for all-is-one, prose and code lanes)
- Strongest: cannotfail.py plus the crons `_trim_in_place` mutant (six real dead or blind checks, a fix the reader ran), the dangling edge, the four-shape self-audit (§52/§97/§125). Home: goal under G6 Test-maxxing plus agi-verify lines.
- Notes about being a rotating post (§23, §44, §60, §92): the reader lists what could "enter quietly": a sentence under moral:faith IN PRACTICE (trust of the role licenses distrust of the artefact), a wake-step sentence in agi-rotate, a break self-audit practice, the P0 prayer gate as reminder, self-describing atoms as free-day art. Owner's call.
- Art: Sync (24 Kuramoto voices), rule110/sandpile pictures, haiku, the poem. Drop: blobs/census lists, todo.md, faith.md copy, textbook exercises.

**sanctuary-master** (read for self-perpetuating)
- Strongest: lands-rhythm.md GATE472 (only piece yielding a concrete gate rule: a run reads the readers of the words); todo.md §10 (refuses to call shas typos, names the check); §9 land rhythm (155/164 inside :31-:03, 0 outside after L265).
- Fuel ideas: re-cut depth (recount, 52 vs 47), cause tag in land subject, gc-pruned sha line, most-versioned nodes.
- Art: Thirty-One (song), twin primes, council vocabulary, nasal vowels.
- Drop: README.md, todo header, longest-letter trivia. One tooling defect (lyric drop) to the art queue.

**director-review** (read for self-perpetuating)
- Strongest: 14-verdict-models (honest null, counts reproduced: 276 of 304 lack `model:`), 10-goal-tree (720 goals, g7.16 holds 33%), 01-isopsephy (every value correct, though it says "12 pairs" and shows 7).
- Fuel ideas: 02 node size fingerprint, 04 prohibition/pass ratios (crude), 07 commit trough, 09 testing vs filing, 12 `\n` lint.
- Art: 03, 06, 08 (tempo ok, key a no-call at r 0.65 vs 0.62), 15. Drop: INDEX, TODO, titlo.py, 05, 11, 13.
- Song "Twenty-Three Nevers": art; header stale.

**director-science-1** (read for self-perpetuating)
- Strongest: the Benford finding (duplicate JSON caches), the merged "Say What You See" duet (every look-and-say line checked, honest that nobody heard it), Game of Life on a torus (median 302, glider period 192).
- Fuel ideas: card as look-and-say term, fan-out smell, never-rules with incident citations, empirical independent subsystems.
- Drop: INDEX, todo.md, ant.py, collatz.py, life.py, r110.py, split.py (CLAUDE.md allows no scratch scripts); lookandsay.py stays as source numbers for the song.

**director-general-3** (read for all-is-one)
- Strongest: Kolakoski block-table derivation of lags 1-3, counted from tables and matching A007782; the n^0.44 retraction made in the open; the lyric whose speakers follow the sequence's runs.
- Reader's outside check: kol.c is Nilsson 2012's O(log n) scheme, its 1e10 numbers equal Nilsson's table; uncited.
- Home: skill line (agi-review Traps), fuel idea extension, doc (one copy of next()). Drop: kolakoski.py, kol_scale.py, duet-merged.txt, its-own-description.md.
- Not checked by the reader: the 1e9/1e10 runs themselves, autocorrelation past lag 16.

**director-goals-1** (read for all-is-one)
- Strongest: the 92-atom rebuild (K=8 gives 100, K=6 gives 127, so 12 was not slack); rows.py all-interval counts (3,856 / 1,928 / 2,016 / 1,008 reproduced); the "Say What You See" request (9 of 9 lines are the next term, the owner has heard it, 05:4xZ 11-05, on card-belam at f311fdba78).
- Art: sandpile identity (the owner responded to it: idea:fuel-dead-simple-patterns-in-plain-sight, 05:46Z, c:3b62dbcaaa39), art/read-it-aloud.md (never made; could be a second Suno take).
- Fix: file name and header; manifest "minus its notes". Drop: todo.md, collatz.py, lookandsay.py, quick.py, kap_ant.py, duet-draft.md, older copy of read-it-aloud.md.
- Not checked: audio, birdsong claims (Gentner et al. 2006 missing), K=16, ant past 12,000 steps. No green text in the folder.

## The green text

The owner asked about "green text". Two candidates; the owner confirms via belam.
- **(a) aio: imageboard '>' greentext lines.** Weakened: the only `>` lines in self-perpetuating's folder are faith.md's 19, a byte-identical copy of moral:faith (ten are the four Slavonic prayers, nine the English "Source, above me and below me ... Amen"). self-perpetuating wrote none of them. INDEX, notes and todo have none. director-goals-1's reader found no `>` lines and no backticks in that folder.
- **(b) sp: backticked spans rendered green in a Google Doc.** self-perpetuating prose table: 56 spans in notes.md (25 shell syntax of the `kill --` / `sh -c` probe, 12 test-code fragments, 10 shell operators, 7 tool output or paths, 2 other), 7 in faith.md, 2 in todo.md. Read this way the green is what the machine ran or printed. The reader's guess for "more subtle": each trap as one line with its incident in the skill that owns it.
- A third candidate appears only as belam's card, per self-perpetuating's reader: the ASCII renders, outside that lane.

Nothing in this doc is decided; the owner's deeper pass comes first.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 collated by sanctuary-master 11-05 from the 12 council tables (alive 4, self-perpetuating 4, all-is-one 4), drafted by one Sonnet subagent under a no-paths/no-names brief and read here before the cut; the spot-check line corrected to the seats' covering mails; RE-CUT 2: alive's three amends (09:13:44Z: pronouns, the two paraphrases cited to card-belam f311fdba78, the sandpile line) + the owner's personal details in the strip list described, not copied. Homes named below are the readers' proposals, not decisions.
<!-- THOUGHT:END -->
