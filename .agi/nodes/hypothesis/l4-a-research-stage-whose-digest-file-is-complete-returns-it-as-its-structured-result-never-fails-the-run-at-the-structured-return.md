---
id: hypothesis:l4-a-research-stage-whose-digest-file-is-complete-returns-it-as-its-structured-result-never-fails-the-run-at-the-structured-return
mint_id: be9e4290f0354ce9a41d36b4b1477f1f
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 4a5954dca18c902b
season: 2
testable_claim: "In the trove-survey workflow (extensions/agi/workflows/agi-trove-survey.js + workflow.py stage return handling ~898-946), a read/critique stage whose per-page digest file is complete on disk returns that file as its structured result: when the model stdout carries no valid structured block (unstructured=N) or the kid exits at the wall, the stage resolves from the digest file (schema-validated from the file, marked resolved-from-digest in the run status) and the run continues to critique / panel / judge; a stage fails only when neither a structured block nor a complete digest exists. Measured: 4 of 4 runs on 2026-09-18 (kv-compression 05:1xZ, round0 05:2xZ, paper-2609 06:2xZ, staged 06:4xZ) ended the read stage rc=2 with unstructured=N failed=1 although every digest was complete (<= 100 lines per page), so critique / panel / judge never ran and every survey was judged by hand. Falsifier: a complete digest with an unstructured stdout still fails the stage; an incomplete digest is accepted as a result; a valid structured block is ignored in favour of the file; the resolved-from-digest mark is missing from the status."
title: "SM.111 (owner 06:5xZ via thought-master, added to the finish set): a research stage whose digest file is complete returns it as its structured result -- the run never fails at the structured return when the work is on disk"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-research-stage-whose-digest-file-is-complete-returns-it-as-its-structured-result-never-fails-the-run-at-the-structured-return

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.111 BRIEF (sanctuary-master 09-18 06:5xZ; owner order verbatim via thought-master: "Also send a message to sanctuary master to fix the research workflow issue on structured outputs."). Kid measures first on the four red logs in the thought town worktree (.agi/sessions/trove-{kv2,r0,p2609,staged}-*.log): WHAT the read stage returned (stdout tail), WHY the structured parse refused (workflow.py ~898 validate + the unstructured path ~939), and where agi-trove-survey.js writes the digest. SHAPE (template-first): the stage manifest declares result_file: <digest path pattern> (a manifest key, so any research stage can opt in); workflow.py, on an unstructured or wall-cut return, reads result_file, validates it against the stage schema, marks the stage resolved-from-digest, and proceeds; a valid structured block still wins; neither -> failed as today. Never a parser hack per model. CEILING 20 production lines (resolver 12, status mark 3, manifest 5). TESTS (one file, test_workflow_result_file.py, stub stages): (1) unstructured stdout + complete digest -> resolved-from-digest, downstream stages run; (2) wall-cut stage + complete digest -> same; (3) unstructured + INCOMPLETE digest (schema fails) -> failed, downstream skipped by name; (4) valid structured block + digest -> the block wins; (5) no result_file key -> today's behaviour byte-for-byte; (6) the run status names resolved-from-digest stages. FILE SCOPE: workflow.py, the trove-survey manifest + agi-trove-survey.js only if the digest path is not already deterministic, one test file. Queue: alongside SM.110 (share 3, no overlap in workflow.py hunks = the kid rebases on SM.110's landing if both touch the stage runner). Inside the finish set (owner-added). Delivery: batch + your mur review in one line; parent blocks in the foreground on its kid.
