# M2 re-cut 2: the council's small return of 06:23Z 10-16, against 81cb084d6b (goal:g5.4.2)

Reading guide: only the sentences the return named are changed. NEW lines are tagged (a pair id of their own chapter, or image); OLD lines are what they replace. NEW PAIRS are added to C7 (C7.13) and C17 (C17.17, C17.18). The FM1 change makes `--chapters=N` required. The SIBLING GREP table at the end lists, for every claim the council returned, the grep run over the narration and html sentences and every sentence it hit, each `fixed` or `kept` with a reason; `python3 extensions/agi/tests/media_sibling.py .agi/context/media/season3-explainer-script.md .agi/context/media/season3-explainer-recut2-diff.md 81cb084d6b .` checks it (a hit with no row, a `fixed` row whose old sentence is still there, or a `kept` row with no reason is RED).

## Sentences

- F1 C3: OLD "The field called next edges sits just above it ..." -> NEW "... sits just below it ..." [C3.4,C3.3] (parents is :5-:6, next_edges :7).
- F2 C4: OLD "Nobody has to remember to start it or stop it by hand." [image] -> NEW "If it ends, the unit starts it again." [C4.3] (Restart=always).
- C1 nit: OLD "And yet this tiny tool does a great deal of the engine's work." [image] -> NEW "And yet a small thing is a fine place to begin." [image] (plainly a picture; no engine claim).
- R1 C8: OLD "... re-attached to the branch tip." [C8.3] -> NEW "... set again at the branch tip, detached." [C8.3] (:146 is `checkout -q --detach $b`).
- R2 C7: OLD "... nothing is going on at all." [image] -> NEW "... nothing is committed at all." [C7.8].
- R3 C11: OLD "the guards that make the safe road the only road." [image] -> NEW "the guards that keep the safe road the easy road, and make a wrong turn loud." [image].
- R4 C7: OLD "But the engine has been set up so that the room is never forgotten." [image] -> NEW "But the engine keeps a pair of small notes about the dish." [C7.10,C7.11].
- C7 nit: OLD "The dish sits in memory, and ..." [C7.6] -> NEW "The dish sits in memory, under the runtime directory's wt directory, and ..." [C7.6,C7.13]; the power-loss sentence is now [C7.6,C7.13]; NEW PAIR C7.13 (RUNTIME_DIRECTORY/wt, engine-post.md:L183-L184).
- C6 nit: OLD "... called the working directory ..." -> NEW "... called wt ..." [C6.8,C6.9].
- H1 C17: OLD "Nothing happens, nothing at all, and that is the point." [image] -> NEW "Nothing is committed, and no reference moves, and that is the point." [C17.17,C17.18]; NEW PAIRS C17.17 (copy of C7.8: commit-tree) and C17.18 (copy of C7.9: update-ref).
- H2 C13: "The tool is the engine's design for the climb." [image] -> [C13.14]; "The skill is the hand that does it now." [image] -> [C13.16] (the master gate skill's pair).
- H3 C16: "It is a built tool waiting for its trigger." [image] -> [C16.6].
- Sibling-driven (found by the grep below, not named by the council): C12 "when the tool re-attaches the view to the branch tip" -> "sets the view again at the branch tip, detached" [C12.9]; C17 "The read view is re-attached to the branch tip." -> "set again at the branch tip, detached" [C17.11]; C17 "no post can move a neighbor's branch, and no stray commit can be made where it would be stranded" -> "the reference guard refuses a post that tries to move a neighbor's branch, and the commit guard stops a stray commit where it would be stranded" [C17.12,C17.13] (the guard fails open and the no-verify flag passes: C12.4, C12.9).

## FM1 (mutant D)

`media_fm1.py` now REQUIRES `--chapters=N`: a run without it prints one line to stderr, checks nothing and exits 2. The count cannot be taken from the file (a renamed heading lowers both sides, which is how mutant D ran green with chapters=17). The run doc's check command names `--chapters=18`. Test: `test_mutant_d_cli_without_chapters_flag_checks_nothing` (the `## C7` heading renamed `## Chapter 7`, C7's fn: dropped: no flag -> exit 2 and no output; `--chapters=18` -> red, "chapters=17, the outline has 18"; the real outline with the flag -> exit 0).

## SIBLING GREP

grep F1: next edges.*(above|below)|(above|below) it\b
grep F2: by hand|nobody has to|remember to start
grep C1: great deal of the engine|does a great deal|every other tool
grep R1: re-?attach|attached
grep R2H1: nothing (at all|happens|is going)|going on at all
grep R3U2: only road|only way|no post can|no stray commit can|impossible|cannot move
grep R4: never forgotten|never lost|nothing is lost|is never forgot
grep C7N: vanish|working area|sits in memory
grep C6N: working directory|working area
grep H23: waiting for its trigger|design for the climb|hand that does it now|\bbuilt tool\b

hit C1 | fixed | And yet this tiny tool does a great deal of the engine's work. => And yet a small thing is a fine place to begin.
hit F1 | fixed | The field called next edges sits just above it, present and empty, and the map's own picture counts the parents as the edges. => The field called next edges sits just below it, present and empty, and the map's own picture counts the parents as the edges.
hit F1 | kept:the corrected sentence: parents is :5-:6 and next_edges is :7 of the example node, pair C3.4 | The field called next edges sits just below it, present and empty, and the map's own picture counts the parents as the edges.
hit F2 | fixed | Nobody has to remember to start it or stop it by hand. => If it ends, the unit starts it again.
hit F2 | kept:a post merging an archived dish by hand is what C11 states; the sentence claims no automation either way | The post can recover and merge by hand.
hit R1 | fixed | The real index moves only later, when the read view is re-attached to the branch tip. => The real index moves only later, when the read view is set again at the branch tip, detached.
hit R1 | fixed | The next turn, when the tool re-attaches the view to the branch tip, that stray commit would be stranded, nearly invisible, hanging by a thread. => The next turn, when the tool sets the view again at the branch tip, detached, that stray commit would be stranded, nearly invisible, hanging by a thread.
hit R1 | fixed | The read view is re-attached to the branch tip. => The read view is set again at the branch tip, detached.
hit R1 | kept:an attached head is the git term for a head on a branch, which is what the hook leaves alone, pair C12.9 | Any other worktree, any attached head, and any commit with the no verify flag, are left alone.
hit R2H1 | fixed | I want to be careful, because this is the moment where it would be easy to imagine a great deal going on, and in truth, nothing is going on at all. => I want to be careful, because this is the moment where it would be easy to imagine a great deal going on, and in truth, nothing is committed at all.
hit R2H1 | fixed | Nothing happens, nothing at all, and that is the point. => Nothing is committed, and no reference moves, and that is the point.
hit R2H1 | kept:a return value of nothing from a reader function, not a claim about the engine being idle, pair C3.6 | It takes the text of a node and gives back a dictionary, or nothing at all if the text has no readable front matter.
hit R2H1 | kept:names the empty tree of the mail commit, pair C14.3, not the engine being idle | The tool takes the message from standard input, and it calls commit tree with the signing flag, with a tree that is the empty tree, the tree of nothing at all.
hit R3U2 | fixed | But the care is the point, and now we turn to the guards that make the safe road the only road. => But the care is the point, and now we turn to the guards that keep the safe road the easy road, and make a wrong turn loud.
hit R3U2 | fixed | The guards stood by all the while: no post can move a neighbor's branch, and no stray commit can be made where it would be stranded. => The guards stood by all the while: the reference guard refuses a post that tries to move a neighbor's branch, and the commit guard stops a stray commit where it would be stranded.
hit R4 | fixed | But the engine has been set up so that the room is never forgotten. => But the engine keeps a pair of small notes about the dish.
hit R4 | kept:the sentence follows the archive reference that holds the moved dish's commit, pair C11.8 | Nothing is lost.
hit C7N | fixed | The dish sits in memory, and a few bytes in it differ from the receipt. => The dish sits in memory, under the runtime directory's wt directory, and a few bytes in it differ from the receipt.
hit C7N | kept:now tagged C7.13, the pair on RUNTIME_DIRECTORY/wt | The dish sits in memory, under the runtime directory's wt directory, and a few bytes in it differ from the receipt.
hit C7N | kept:now tagged C7.13 as well as C7.6, the pair that names the directory | If the machine were to lose power this instant, the edit would vanish, and the history would show that nothing had ever happened.
hit C7N | kept:tagged C4.1 and C4.9, and C4.9 is the RUNTIME_DIRECTORY/wt pair | This is a directory in memory, and it is where the post's tiny working trees will live, each of them vanishing when the machine reboots unless it has been committed.
hit C7N | kept:the working area is the wt directory under the runtime directory, pair C7.2 and C7.13 | A directory in the working area is only treated as a tree if it has a tag in it.
hit C7N | kept:the memory working area is the wt directory, pair C8.6 and C7.13 | The tool looks at every directory in the memory working area.
hit C7N | kept:the working area is the wt directory, pair C13.3 and C7.13 | Then for every directory that is still lying in the working area, it calls the turn tool's purge.
hit C6N | fixed | The tool first makes sure it knows who the post is, and it works out where the dishes live: a directory in memory, called the working directory, which the unit gave the post. => The tool first makes sure it knows who the post is, and it works out where the dishes live: a directory in memory, called wt, which the unit gave the post.
hit C6N | kept:the working area names the wt directory, which C6.9 and C7.13 cite | A directory in the working area is only treated as a tree if it has a tag in it.
hit C6N | kept:the working area names the wt directory, which C6.9 and C7.13 cite | The tool looks at every directory in the memory working area.
hit C6N | kept:the working area names the wt directory, which C6.9 and C7.13 cite | Then for every directory that is still lying in the working area, it calls the turn tool's purge.
hit H23 | kept:the html summary was already tagged C16.6 | At this revision nothing schedules or calls tick.sh: it is built and waiting for its trigger.
hit H23 | kept:now tagged C16.6 | It is a built tool waiting for its trigger.
hit H23 | kept:now tagged C13.16 | The skill is the hand that does it now.
hit H23 | kept:now tagged C13.14 | The tool is the engine's design for the climb.
hit R3U2 | fixed | The guards: a mistake cannot move a peer's ref => The guards: a post's mistake is refused when it tries to move a peer's ref
