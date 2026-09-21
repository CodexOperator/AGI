# ABL.01 trajectories

Parent + 3 kids for ABL.01 (own-refusal-direction extraction attempt; disproved -- cvector extraction is structurally dead on Qwen3.5-9B). Landed per the standing datasets/ landing rule, scrubbed with `datasets/tools/scrub.py`.

**Two of the three kids died mid-round (OOM, 4G cgroup) but both did real, substantial work before dying** -- kid1 independently reproduced the same GGML_ASSERT crash kid3 later confirmed under docker; kid2 explored the full-cuda image and a smaller-scale probe. Their stub experiment nodes point back here rather than to the (ephemeral, worktree-scoped) session dirs the nodes originally cited. kid1's `extraction.log` is landed alongside its trajectory for exactly this reason -- the node's own evidence citation would otherwise go dead once the parent's worktree is removed.

| agent | role | verdict | mur |
|---|---|---|---|
| a00-a2d302eb | parent | harvest accepted=1 demoted=0 failed=2 | accept_with_residue |
| a00-f5d01ed3 | kid1 | died (OOM after independently reproducing the assert on host) | n/a (stub node, real work preserved here) |
| a00-271bc548 | kid2 | died (OOM mid-exploration) | n/a (stub node, real work preserved here) |
| a00-8241a6fb | kid3 | disproved conf=0.85 | accept_with_residue |

Total redactions across the round: {"ip_decimal": 287, "ip_hex": 1137, "ip_dotted": 15, "hex40_key": 13, "email": 7}
