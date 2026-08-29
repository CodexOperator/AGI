---
confidence: 0.5
id: "hyp:autoresearch-tree-skill-r1"
mint_id: 34bd4629c6884ee0829929ccc7e2766b
next_edges:
  - exp:autoresearch-tree-skill-r1
origin: build-site
parents:
  - idea:domain-autoresearch-tree-skill
subgraph: false
tags:
  - autoresearch-tree-skill
  - R1
testable_claim: Skill Lives in a Forked Skill Repository
title: "autoresearch-tree-skill/R1: Skill Lives in a Forked Skill Repository"
type: hypothesis
---

**Description:** A new skill is added to the existing autoresearch skill repository alongside the existing skills, without modifying or removing them.

**Acceptance Criteria:**
- [ ] The new skill is added at a documented path inside the existing autoresearch skill repository
- [ ] No file under the existing autoresearch-create or autoresearch-finalize skills is modified or removed by this kit's installation
- [ ] Adding the skill is one new directory of files, not a patch to existing files
- [ ] After installation, both the new skill and the original skills are listed by the standard skill enumeration
