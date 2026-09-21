# single axis -- hypothesis:lm-jev-single-axis-question-beats-baseline

MODEL=jev-1.13.0 SEED=20260918 REPEATS=3; n_acts=370; spend $0.161497 of cap $1.00.

| arm | q | label | n | agree | base | AUC | ECE | confusion |
|---|---|---|---|---|---|---|---|---|
| arm0_prior | q1 | q1 | 369 | 0.051 | 0.507 | 0.558 | 0.776 | inconclusive_lean_proved>pending:162 proved>pending:129 inconclusive_lean_disproved>pending:31 inconclusive_lean_proved>proved:24 proved>proved:12 pending>pending:6 |
| arm0_prior | q2 | q2 | 370 | 0.257 | 0.776 | 0.314 | 0.240 | accept>demote:214 accept>accept:73 demote>accept:49 demote>demote:34 |
| arm1_review | q2 | q2 | 370 | 0.541 | 0.776 | 0.581 | 0.172 | accept>accept:147 accept>demote:140 demote>demote:52 demote>accept:31 |
| arm2_verdict | q1 | q1 | 369 | 0.610 | 0.507 | 0.855 | 0.161 | proved>proved:116 inconclusive_lean_proved>inconclusive_lean_proved:84 inconclusive_lean_proved>proved:47 inconclusive_lean_proved>pending:43 proved>inconclusive_lean_proved:23 inconclusive_lean_disproved>inconclusive_lean_disproved:14 |
