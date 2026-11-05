"""goal:g5.4.2: the ONE place that names the media data dir (council 18:02Z 10-21: it was typed in five files and named a post, and the shuffle reuses post names).
BASE = $MEDIA_BASE, else /data/work/media/season3: a dir named for the WORK, not a post. Every other media file imports it; test_media_paths greps the rest for a typed data dir.
QUEUE_DIR holds the two queue files SM's gates read (RENDERING, HOLD-GATES): $MEDIA_QUEUE_DIR, else BASE's parent."""
import os

BASE = os.environ.get("MEDIA_BASE") or "/data/work/media/season3"
QUEUE_DIR = os.environ.get("MEDIA_QUEUE_DIR") or os.path.dirname(BASE)
LANE = os.environ.get("MEDIA_LANE") == "1"      # the media lane (SM's media gate) sets it: a test that needs the data dir FAILS when it is missing; in any other suite it SKIPS (a clone without the data dir is not RED)


def need(path, what="the media data dir"):
    """For tests that read the data dir: FAIL in the media lane (R-gross: a missing narration mp3 is a FAIL), SKIP everywhere else."""
    import pytest
    if not os.path.exists(path):
        (pytest.fail if LANE else pytest.skip)(f"{what} missing: {path}")
    return path
