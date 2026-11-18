---
name: report
derived_from: goal:g5.4.3.3 (owner 11-18 15:2xZ via meme-master; placed by sanctuary-master 15:3xZ); shaped by the council 11-18 (remix 15:46:03Z, plasma 15:46Z, less-is-more's reconciling word 15:48:28Z)
fields:
  title: {type: str}
  kind: {type: str}             # research-presentation | research-paper | algo-optimized-video | seo-optimized-blog-post
  stage: {type: str}            # draft | final | published
  artifact_sha256: {type: str}  # sha256 (64 hex) of the CURRENT private bytes; never the bytes
  artifact_where: {type: str}   # OPTIONAL, by role only: box-local | owner-drive | public; never a folder or a file name
  url: {type: str}              # OPTIONAL, at stage published only
  parents: {type: list}         # the one goal the report answers
  next_edges: {type: list}
  tags: {type: list}
  season: {type: int}
  status: {type: str}           # absent = live; `deprecated` = retired in place
validation:
  required: [id, type, mint_id, title, tags, parents, kind, stage, artifact_sha256]
  types:
    title: str
    kind: str
    stage: str
    artifact_sha256: str
    parents: list
    tags: list
  regex:
    kind: '^(research-presentation|research-paper|algo-optimized-video|seo-optimized-blog-post)$'
    stage: '^(draft|final|published)$'
    artifact_sha256: '^[0-9a-f]{64}$'
    artifact_where: '^(box-local|owner-drive|public)$'
spawn:
  allowed_parents: [goal]
  min_parents: 1
  max_parents: 1
---

# report

A POINTER to one private artifact the owner puts out: its sha256, never its text. ID prefix: `report:<short-slug>`.

A NEW type, not doc + a subtype: `links.py schema` binds required fields per directory type, so a doc subtype could
not require `kind`, `stage` and `artifact_sha256` without requiring them of every doc; and a doc may carry text, a
report never does.

## The four kinds
| kind | the owner's phrase (11-18, verbatim) | judged by | schema.org type |
|---|---|---|---|
| research-presentation | research presentation | its live audience: the class rubric | PresentationDigitalDocument |
| research-paper | research paper | graders, plus proof readers (L608-style) | ScholarlyArticle |
| algo-optimized-video | algo-optimized video | the platform's recommender: retention, CTR | VideoObject |
| seo-optimized-blog-post | SEO-optimized blog post | the search engine: rank, impressions | BlogPosting |

## Stage
- `draft`: agents' bytes, marked DRAFT (goal:g5.4.3).
- `final`: the owner's own wording; the owner writes every final word (goal:g5.4.3). Rewriting is a step inside
  final, tracked by the shepherd loop, not by the node.
- `published`: it left the box on the owner's yes (L629). `url` only here.

## Body
1. Never artifact text: no excerpt, no quote. A sibling form (a PDF beside its tex) is named by sha256 only.
2. New bytes = a new version of THIS node (a grid version, its THOUGHT says why), never a second report node and
   never a version field: the sha pins the bytes.
3. `artifact_where` names a ROLE, never a folder or a file name (L629: the graph reaches the public origin).

## Spawn rule
`allowed_parents: [goal]`, `min_parents: 1`, `max_parents: 1`: a report answers one goal.
