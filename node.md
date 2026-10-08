---
id: hypothesis:l4-message-bodies-are-files-never-argv-strings-every-free-text-cli-takes-file-or-stdin-and-refuses-backticks
mint_id: cd0d6f80f14a4ad091fd323349addc83
type: hypothesis
parents:
  - goal:g6.16
next_edges: []
edited_by: belam
scaffold_hash: e0c29b800cd890ed
season: 2
testable_claim: "OWNER RULING (verbatim banked a74dea7f3, doc:l4-owner-decisions tail; relayed by belam gen 26 00:3xZ): 'Need to fix that backtick issue it keeps biting us. Maybe avoid them somehow entirely by using direct cli commands instead for all these scripts? We already have a commands just extend it'. MEASURED: gen 25's review focus string and the Prime's dm 00:2xZ both EXECUTED `rotate.py rotate` inside a double-quoted argv string (refused by name both times -- luck, not a guard); sanctuary-master gen 4 blanked a numbers-line fragment the same way at 23:3xZ. PRIORITY over node E. CLAIM: (1) every engine CLI that takes free text -- send.py send, write.py note/thought/set, workflow.py --args, rotate.py --stops, cli.py done --deliverables -- accepts it from a FILE or STDIN (`--file PATH` / `-`) and REFUSES argv text that carries a backtick or `$(` by name (the shell has already run it; the refusal names the artefact and the --file route); (2) config:commands / commands.py gains named entries `dm --to <post> --file`, `note <node> --file`, `thought <node> --file`, `review <args.json>`, `stops --file` so a role never composes a quoted shell string; (3) every role brief and skills/agi/SKILL.md carry the one line: message bodies are files, never argv strings -- write with a QUOTED heredoc (<<'EOF') then pass the path; (4) a test proves a body containing a backtick and $(id) arrives byte-identical through each route. FALSIFIERS: a send/note/stops that stores an argv body containing a backtick without refusing; a commands.py without the five entries; a brief that still shows a double-quoted body; a byte-changed body through --file. TESTS (<=5): refusal per CLI; byte-identity per route; commands entries resolve; brief text. FILE SCOPE: send.py, write.py, workflow.py, rotate.py (--stops), cli.py (done), commands.py + config:commands, brief.py role text, skills/agi/SKILL.md, their tests. CEILING: <=60 production lines across 2 kids (CLIs + commands one kid; briefs/SKILL + tests one kid), re-brief SM past 2x."
thought_session: dissolve-legacy-2026-09-19
title: L4 message bodies are files never argv strings every free text cli takes file or stdin and refuses backticks
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-message-bodies-are-files-never-argv-strings-every-free-text-cli-takes-file-or-stdin-and-refuses-backticks

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
CANCELLED by owner order 03:0xZ (verbatim in doc:l4-owner-decisions tail; relayed by belam gen 27 02:58Z): SM.78 / node I is STRUCK from the closeout -- 'not a good enough fix morally'. Round state at cancellation (sanctuary-master gen 5): parent a00-aeb3ab88 and both kids had already exited (kid a00-3b2ef119 :80, kid a00-d767f2f8 :55, parent done 04831cad2 on season2/loops/hypothesis-l4-message-bodies-are-...-a00-aeb3ab88); nothing to stop, 0/25 live. Harvested NOTHING; the branch stays unmerged; no code from it reaches MAIN. The hypothesis stays open for a later stream.
