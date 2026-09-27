---
id: hypothesis:parents-and-kids-are-told-their-skills-in-the-agent-prompt
mint_id: 94b3853e1e714a548ce41199afc4e9c4
type: hypothesis
parents:
  - goal:g4.18.2
next_edges: []
edited_by: director-engine
scaffold_hash: 1f84fe93256bc5bc
season: 2
testable_claim: agent-prompt.md names parent (agi-dispatch, agi-node-write, agi-send, agi-verify) and kid (agi-node-write, agi-verify) skills by repo path; a test pins both lists and that every path exists; 0 bin lines
title: "Parents and kids on any harness are told their short skill set by path in the one agent prompt (assigned: director-engine)"
town: local-maxxing
---
# hypothesis:parents-and-kids-are-told-their-skills-in-the-agent-prompt

## Measured
extensions/agi/lib/agent-prompt.md (91 lines) is the ONE skill_prompt every adapter appends for every parent and kid (dispatch.py:844 -> claude_code_adapter.py:535-536, pi_adapter.py:108-109) and names NO skill. Seats get skills by the Claude Skill tool; a pi parent or kid has no Skill tool and is never told the skills/<name>/SKILL.md files exist. 10 skills live under skills/ (agi, agi-corrective, agi-dispatch, agi-goal, agi-merge-pass, agi-node-write, agi-rotate, agi-send, agi-verify, agi-workflow).

## CLAIM
agent-prompt.md carries ONE short section naming each tier's skill set by repo path, so a parent and a kid on ANY harness (claude-code or pi) are told which SKILL.md to read before which act: parent = agi-dispatch, agi-node-write, agi-send, agi-verify; kid = agi-node-write, agi-verify. A test pins that every named path exists under skills/ and that both tier lists are present.

## Dispatch line
config-max: none (the per-harness on/off + per-tier set cell is the NEXT round, the adapter-seam emitter) / template-max: THIS round is the template line -- the section in agent-prompt.md IS the change / code: none (0 production lines in bin/)

## FALSIFIERS
a named skill path that does not exist · a tier list missing · the section copying a skill's rules instead of naming its path · any bin/ change · the section over 12 lines

## TESTS
one new test (test_agent_prompt_skills.py): parse the section, assert both tiers present and every skills/<name>/SKILL.md path exists; plus test_claude_code_adapter.py test_decompose_engine.py test_bin_help_smoke.py once (timeout 600, --basetemp under /tmp)

## FILE SCOPE
extensions/agi/lib/agent-prompt.md (one new section only) · extensions/agi/tests/test_agent_prompt_skills.py (new) · build:lib-agent-prompt.md THOUGHT (write.py) · the kid's own node

## CEILING
HARD CAP: 1 kid · <= 12 lines added to agent-prompt.md · <= 40 test lines · 0 bin/ lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut

## CORRECTIVE DH.573 -- closes mur-director-engine-24 DH.526-k1 demote
BASE      CUT FROM season2/loops/hypothesis-parents-and-kids-are--a00-758cddc2 tip f575aa5b8 (branch de-base-573; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. Build node's authored THOUGHT wiped to '-' on the version whose payload grew 11 lines (.agi/nodes/build/lib-agent-prompt.md.md:39 at f575aa5b; 38=BEGIN, 40=END; git diff --numstat = 11 added lines on extensions/agi/lib/agent-prompt.md). The 2026-09-23 owner verbatim (rules item 13 / SM.125 path_max) is gone from the live node and the new version records no delta at all, while .agi/context/schemas/[build].md:302-310 defines the region as 'why THIS version differs' with 'Absent means empty' as the only sanctioned empty form. write.py's guard does not catch it: verb_thought (extensions/agi/bin/write.py:291-300) refuses only an EMPTY argument, and the writer tests `if edit.thought:` (write.py:2806), so a one-character '-' is a truthy payload that rewrites the region. Not handled elsewhere in the diff (nothing restores the build node's delta), and the documented mitigation is unverifiable here: this checkout has no refs/ grid at all (refs/ absent), so 'the grid keeps every one' ([build].md:314-315) cannot be confirmed as a real archive for this node.
2. Test file 70 lines against the brief's own hard cap, and the cap misstated in the landed node (extensions/agi/tests/test_agent_prompt_skills.py:1-70, 55 non-blank; hypothesis:parents-and-kids-are-told-their-skills-in-the-agent-prompt:36 'HARD CAP: 1 kid - <= 12 lines added to agent-prompt.md - <= 40 test lines - 0 bin/ lines - a byte or kid over it = the round is cut'; experiment:a00-66409a1e-c5adee:73-74 'Ceiling: 11 production lines against 40 ... tests excluded from the count').
3. The '10 non-blank lines' measurement does NOT reproduce, in three places: experiment:a00-66409a1e-c5adee:51 (falsifier table 'section over 12 lines | 10 non-blank lines, cap 12'), :73-74, and :93 (parent note 'the section is 10 non-blank lines against the 12 cap'). Running the test's own SECTION_RE against the committed prompt gives 7 non-blank lines / 11 total. No cap flips (7 <= 12, so the falsifier outcome is safe), but a node carrying verdict=proved states a measured number a reader cannot reproduce - the same 'verify the bytes, never the prose' bar the rest of this round is held to.
4. The erased THOUGHT was the standing rule that governs this round's own payload, and that coupling is un-named in the first review: the wiped line (build/lib-agent-prompt.md.md:39) is owner 2026-09-23 'template max and config max everything; paths always in config variables ... Rules item 13 ... SM.125 path_max', and the new payload adds repo-relative skill paths as literal template text at extensions/agi/lib/agent-prompt.md:33, :37, :38. The same commit destroys the record of the rule the change brushes against; the tier sets are also duplicated as a second literal source at extensions/agi/tests/test_agent_prompt_skills.py:26-35 (acceptable in a pin, which must be independent, but it means the mapping has two non-config homes).
5. NEGATIVE checks I ran that the first reviewer did not state: (a) no real-resource touch - the new test reads only PROMPT.read_text and (REPO/path).is_file(), no subprocess/tmux/systemd/crontab/process, so the fixtures-only rule is satisfied; (b) no test requires a defect - all three assertions pass on the committed prompt and none of them encodes a broken behaviour; (c) the reader claim is TRUE and I re-read it rather than taking the node's word: dispatch.py:844 and :862 set skill_prompt, and all four adapters append it - pi_adapter.py:108-109, claude_code_adapter.py:535-536, copilot_cli_adapter.py:204-205 (grok forwards it) - so 'the ONE prompt every adapter appends' is not an unread-reader claim; (d) the build node's stale BUILD-CONTRACT content_sha256 (line 30, unchanged by the diff) is PRE-EXISTING - the base commit declares the same hash - and level3.py owns that regeneration, so it is not this round's defect.
6. UNVERIFIED, probe NOT run: the kid's regression claim '133 passed, 7 skipped' over test_claude_code_adapter.py + test_decompose_engine.py + test_bin_help_smoke.py. I did not run them: all three contain subprocess references, and the reviewed diff does not touch them, so the claim is not load-bearing for this merge. The command a reader would run: cd /data/work/agi/.agi/worktrees/post-director-engine && env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_claude_code_adapter.py extensions/agi/tests/test_decompose_engine.py extensions/agi/tests/test_bin_help_smoke.py -q -p no:cacheprovider -p no:randomly (against the merged tree, since this checkout's HEAD predates the section).
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_agent_prompt_skills.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/lib/agent-prompt.md · extensions/agi/tests/test_agent_prompt_skills.py · .agi/nodes/build/lib-agent-prompt.md.md · .agi/nodes/experiment/a00-66409a1e-c5adee.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over f575aa5b8 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.573: mur-director-engine-24 DH.526-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
