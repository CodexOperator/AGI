"""Child probe for the AGI_REAL_JUDGE opt-in (hypothesis:l4-the-suite-never-
reaches-openrouter-one-autouse-stub-on-openrouter-get-unless-the-real-judge-
flag-is-set). This is the nerve that proves `_no_openrouter` truly stands the
suite down. It is only ever run as a NESTED pytest child by test_rotate.py's
test_real_judge_optin_stands_the_stub_down -- once with AGI_REAL_JUDGE=1 plus
a junk key, once with the flag unset. Each child run lives in ONE real env, so
the autouse fixture (`_no_openrouter`) has already decided by the time THIS
body runs and the assertions pin that decision with no monkeypatch of our own
-- a plain in-process test would set the env after the strip and could not
distinguish "the escape works" from "the test re-set it"."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate
import rotate as rotate_alias  # noqa: E402 -- the 2-alias object under test


def test_optin_stands_the_stub_down():
    # _REAL_JUDGE_ON is THIS child conftest's import-time snapshot of the
    # flag; it is True exactly when the operator launched AGI_REAL_JUDGE=1
    # for this child (and the session strip can no longer touch it).
    from tests.conftest import _REAL_JUDGE_ON

    key_present = bool(os.environ.get("OPENROUTER_API_KEY"))
    real_func = rotate._openrouter_get.__name__ != "<lambda>"
    alias_real = rotate_alias._openrouter_get.__name__ != "<lambda>"
    assert real_func == alias_real, "both rotate aliases must see one choice"
    if _REAL_JUDGE_ON:
        assert real_func, "opt-in must leave the REAL _openrouter_get in place"
        assert key_present, "opt-in must keep OPENROUTER_API_KEY in the env"
    else:
        assert not real_func, "default-off must stub _openrouter_get"
        assert not key_present, "default-off must drop the key env"