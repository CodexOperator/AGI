---
id: verdict:dg2-r2
mint_id: ff76220b45054e00814eabfb8f7f4f6b
type: verdict
parents:
  - experiment:dg2-r2-harvest
  - hypothesis:trunk-red-boxkit-fake-denylist-derives-from-classes
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-r2-harvest
scaffold_hash: f576e72169516475
season: 2
title: "DG2.R2 proved 0.9: fake denylist derived from anonymize.CLASSES; planted-kit row green with the kit's own bytes clean once email_allow allowed user@UID.service (d572f65d6b)"
town: core
verdict: proved
---
# verdict:dg2-r2

## Verdict: proved (0.9)
The fake denylist is derived from anonymize.CLASSES (one synthetic `boxkit-fake-<class>-token` per class; a new class needs no test edit), the planted-kit row is green and the kit's own bytes stay clean, with no assert removed or loosened. No falsifier fired: red on the base, green on the tip (F1); bin/ and kit bytes 0 (F2); no hand class list (F3); no real-looking value (F4). The row needed a second, config-max fix outside the brief's scope -- the email_allow entry widened by the Prime on SM's pick (A), recorded here as part of the landed state, not as test code.
