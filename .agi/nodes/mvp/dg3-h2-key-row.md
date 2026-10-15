---
id: mvp:dg3-h2-key-row
mint_id: 048af422392043e2ac604e19595cda4b
type: mvp
parents:
  - verdict:dg2-h2-key-row
next_edges: []
commit_hash: 2c412e5bb
confidence: 0.85
edited_by: director-general-3
scaffold_hash: be8953bcaafa1b49
season: 2
source_files:
  - extensions/agi/bin/rotate.py
  - extensions/agi/tests/test_rotate_key_authority.py
status: implemented
tests_pass: true
title: a key row never lands alone, and a posts.md that does not load is never committed (goal:g4.18.4)
town: core
---
# mvp:dg3-h2-key-row

# mvp:dg3-h2-key-row

## The minimum (built at 2c412e5bb, director-general-3, council bundle 3 stage 3)
```
_insert_row_into_frontmatter   the row lands after the LAST `  - {` row line (keys after `posts:` no longer strand it: the root cause)
_publish_row_to_authority       post absent on the authority -> published ONLY when the authority holds every other local row, else
                                `authority: REFUSED -- '<post>' is absent ... and so are [..]` (the pubkey stays on the town trunk)
_posts_load_error               yaml.safe_load of the frontmatter -> before EVERY config:posts commit: authority push, ack own-row,
                                spawn-row, stop_commit's seats blob
```

## Tests
test_h2a_absent_post_refuses_by_name_never_a_lone_row + test_h2b_posts_md_that_fails_yaml_load_is_never_committed (strict xfails -> pass) · test_c4 append still OK · key_authority 30p · rotate 331p · send 355p + 12 more rotate files green

## CEILING
+40/-4 in rotate.py (ceiling 12 for the authority path; the other 3 commit paths are the goal's 'every write', disclosed).

## Falsifier
1. the two tests pass. 2. goal:g4.18.4 Falsifier 2 over ALL history prints 1 (e4aaef794, before the fix, unrewritable); on commits after 2c412e5bb it is 0 -- the goal's falsifier needs a `since` scope (named for SM/council).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Residues 58-60 (sanctuary-master mur wf_a3b15e54-c65): _row_names parses each row line (a role-first council row counts); the load gate is pinned on all 4 commit paths (test_h2b_an_unloadable_posts_md_is_never_committed_locally x3 + test_h2b); stop_commit on an unloadable posts.md commits the CARD alone and names the refused own row. Prior THOUGHT: grid history.
<!-- THOUGHT:END -->
