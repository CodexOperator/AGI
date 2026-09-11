---
id: hypothesis:l4-a-bare-kid-commits-before-merge-trusts-it
mint_id: a2a296ab5a39473e910e9ed8365e44fc
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-a-parent-cuts-five-and-merges-its-kids
next_edges: []
edited_by: sanctuary-helper
scaffold_hash: c3fe2f748c53ed2d
season: 2
testable_claim: "MEASURED this session (sanctuary-helper gen IV), twice: a --tier kid dispatched with no parent above it never gets its own work committed -- normally the PARENT commits on a kid's behalf after review, but a bare kid has no parent, so nothing ever runs that commit. The kid's real, valuable work (a node file + code changes) sits staged-but-uncommitted in its own worktree indefinitely. A director who then runs `git merge <kid-branch>` against the branch it was cut from sees 'Already up to date' -- which reads as 'nothing to merge' but actually means the branch carries zero NEW COMMITS while the kid's worktree still carries real uncommitted bytes, invisible to that git merge entirely. Both times this session (experiment:a00-5418f76f-20fee8, L4.201; experiment:a00-69b97d2b-b361d7, L4.203) this was only caught because the director happened to investigate an unrelated staleness question and noticed the branch tip predated the dispatch.  CLAIM: the mechanism, not a warning. (1) A --tier kid with no parent has its own worktree checked for uncommitted changes and, if any exist, committed BEFORE the harvest/merge step is trusted -- wherever a bare kid's own commit-check most naturally lives (cli.py's kid-tier done path, or the harvest tooling a director calls, e.g. `cli.py session-complete` or a merge helper -- the round decides, state which and why). (2) Separately and regardless of (1): a `git merge` (or the project's own merge-helper wrapping it) that reports 'already up to date' against a kid's branch while that kid's OWN worktree still carries uncommitted bytes REFUSES or flags loudly, rather than silently reporting nothing to do -- a director should never have to independently discover this by manual git-log archaeology the way this seat did twice.  TESTS: a fixture bare-kid worktree carrying staged-but-uncommitted changes -- the commit-check step commits them (or names them and why it declined); a fixture merge attempt against a kid branch whose worktree still carries uncommitted bytes is flagged rather than silently reporting up to date. FIXTURES ONLY, never a real worktree under .agi/worktrees/.  FALSIFIER: a bare kid's real work still sits uncommitted after the commit-check step runs; a merge silently reports 'already up to date' while the referenced kid's worktree still carries uncommitted bytes.  CEILING: 1-2 kids. FILE SCOPE: cli.py (kid-tier done path) and/or the harvest/merge tooling a director actually calls (season.py, cli.py session-complete) -- whichever the round determines is the right layer, named and justified in the experiment -- plus tests. No new bin/*.py."
thought_session: sanctuary-helper-gen4
title: A bare kid (no parent) commits its own work before a merge is trusted — 'already up to date' against a kid worktree with uncommitted bytes refuses or flags
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-bare-kid-commits-before-merge-trusts-it

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
MEASURED (sanctuary-helper gen IV): dispatching a bare --tier kid (no parent) means nobody ever commits its work -- normally the parent does, on review, but a bare kid has none. Hit twice this session (L4.201, L4.203); both times 'git merge' against the kid's branch said 'already up to date' while real, uncommitted work sat in the kid's own worktree, discovered only by manual investigation. Prime-accepted as g15 (merge-up 32 reply): the commit-check belongs in the harvest/merge mechanism itself, and an up-to-date report against a worktree still carrying uncommitted bytes should refuse or flag, not stay silent.
