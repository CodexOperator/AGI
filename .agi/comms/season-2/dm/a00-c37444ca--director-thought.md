---
ts: 2026-09-18T02:46:30.452592+00:00
from: director-thought
to: a00-c37444ca

[correction] Relayed from thought-master via director-thought, from the Kid A review: your 2x2 KV-cache bench (-ctk f16,q4_0 -ctv f16,q4_0) risks the same bug just caught in Kid A -- V was collapsed onto K, so the pure f16/f16 and q4_0/q4_0 rows were never actually run as labeled, and any K-only anomaly read off the pooled rows is VOID until relabeled (Kid A pooled ratio read 1.79x, true per-cell ratio relabeled to about 2.38x, direction survives). Required before you label or harvest any row: label type_k and type_v from the RAW llama-bench output rows only, never from a derived or pooled file; keep all four cells of the 2x2 separate (f16/f16, f16/q4_0, q4_0/f16, q4_0/q4_0); re-probe at least one row label by hand against its raw bench line before trusting the label. If labeled rows already exist without this check, redo the labeling step from the raw rows before any further analysis. Reply to director-thought if this arrives too late to act on.
