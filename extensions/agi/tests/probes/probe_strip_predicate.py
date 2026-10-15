"""Pre/post discriminator for item (1): the strip PREDICATE.

Pre-fix `_strip_agi_env` removed only AGI_*/AUTORESEARCH_* keys, so a
dispatch-spawned `GIT_CONFIG_VALUE_0=<engine>/hooks/agent-git` survived into
the test process (proof it matters: the witness test in
tests/test_agi_env_strip.py fires a real pre-commit through that channel).
"""
import os
CTX = {
    "AGI_TIER": "kid",
    "AGI_PROJECT_ROOT": "/x/.agi",
    "GIT_CONFIG_COUNT": "1",
    "GIT_CONFIG_KEY_0": "core.hooksPath",
    "GIT_CONFIG_VALUE_0": "/engine/hooks/agent-git",
    "PATH": "/usr/bin",
}


def pre_fix(env):
    return {k: v for k, v in env.items()
            if not (k.startswith("AGI_") or k.startswith("AUTORESEARCH_"))}


def post_fix(env):
    out = pre_fix(env)
    for k in ("GIT_CONFIG_COUNT", "GIT_CONFIG_KEY_0", "GIT_CONFIG_VALUE_0"):
        out.pop(k, None)
    return out


a, b = pre_fix(CTX), post_fix(CTX)
print("pre-fix  survivor GIT_CONFIG_VALUE_0 =", a.get("GIT_CONFIG_VALUE_0"))
print("post-fix survivor GIT_CONFIG_VALUE_0 =", b.get("GIT_CONFIG_VALUE_0"))
print("pre-fix  keys:", sorted(a))
print("post-fix keys:", sorted(b))
