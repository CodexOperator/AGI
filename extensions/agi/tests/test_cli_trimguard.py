"""hypothesis:l4-trimguard-never-reads-a-closing-quote-as-an-open-span

The open-ended-quote regex must never match the CLOSING quote of a closed
span. Pre-fix, cmd_trimguard ran two independent regexes; the open-ended one
`[""“]([^""“”\\n]{25,})$` (re.M) matched the closing quote of a closed span
whenever that quote was the last on its line with 25+ non-quote chars after
it — minting a phantom open span that wrongly ABORTed the trim on the live
HANDOFF §6 item 106 line.

These tests drive the span-extraction decision directly (the pure helper
`_collect_owner_spans`), which is what cmd_trimguard now calls, so the
acceptance cases are hermetic rather than tied to the live HANDOFF bytes.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_cli():
    bin_dir = Path(__file__).resolve().parents[1] / "bin"
    spec = importlib.util.spec_from_file_location("agi_cli", bin_dir / "cli.py")
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    return cli


cli = _load_cli()
collect = cli._collect_owner_spans
ITEM106 = (
    "- **106.** ACCOUNT RUNWAY — CLOSED 2026-09-11 11:5xZ by the owner's top-up "
    "(\"keep using pi rounds till done\", verbatim in `doc:l4-owner-decisions`): "
    "$26.52 of $132.00 at 11:52Z; pi rounds continue to the end of the queue"
)


def test_closed_span_then_25plus_trailing_chars_reports_no_phantom():
    """The exact §6 item-106 shape: a closed span followed by 25+ non-quote
    chars to end of line. Only the real closed span may be reported — the
    trailing run after the CLOSING quote must NOT become an open span."""
    spans = collect(ITEM106)
    assert "keep using pi rounds till done" in spans
    # no phantom open span: nothing reported that starts at the closing quote
    assert not any(s.startswith(", verbatim") for s in spans)
    assert len(spans) == 1


def test_unclosed_quote_line_still_aborts():
    """A real unclosed quote of 25+ chars running to end of line is STILL
    reported as an open span (the guard must keep catching a true truncation)."""
    line = (
        "- **200.** Some item: \"this is a genuinely long owner quote that was "
        "truncated by the line collapse and has no closing quote on this line"
    )
    spans = collect(line)
    assert len(spans) == 1
    assert any("genuinely long owner quote" in s for s in spans)


def test_line_with_two_closed_spans_reports_both():
    line = (
        "- **300.** first \"owner quote alpha bravo charlie delta echo foxtrot "
        "golf hotel\" and second \"india juliet kilo lima mike november oscar "
        "papa quebec\""
    )
    spans = collect(line)
    assert "owner quote alpha bravo charlie delta echo foxtrot golf hotel" in spans
    assert "india juliet kilo lima mike november oscar papa quebec" in spans
    assert len(spans) == 2


def test_stray_closing_curly_quote_is_skipped_not_an_opener():
    """A stray `”` BEFORE a real straight-quoted span is skipped, never an
    opener — so only the one real span is reported (hypothesis:l4-trimguard-
    never-reads-a-closing-quote-as-an-open-span)."""
    line = 'foo” bar "this is a real owner quote of twenty-five plus"'
    spans = collect(line)
    assert "this is a real owner quote of twenty-five plus" in spans
    assert len(spans) == 1


def test_real_handoff_section_has_no_open_spans(tmp_path):
    """A FIXTURE copy of the item-106 §6 shape (never the live HANDOFF.md)
    contains exactly one closed span and no open span — the trim guard must
    PASS against it (no phantom). Written under tmp_path so the hermetic
    suite does not depend on the live HANDOFF bytes."""
    fixture = tmp_path / "HANDOFF.md"
    fixture.write_text(
        "# SESSION HANDOFF — fixture\n"
        "\n"
        "## §6 Owner decisions\n"
        f"{ITEM106}\n"
        "Some trailing non-quoted line with more than enough words to fill "
        "past the twenty-five character floor and prove no phantom opens.\n"
    )
    body = fixture.read_text()
    start = body.index("## §6 Owner decisions")
    spans = collect(body[start:])
    assert len(spans) == 1
    assert "keep using pi rounds till done" in spans
    assert not any(s.startswith(", verbatim") for s in spans)
