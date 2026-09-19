#!/usr/bin/env python3
"""Unit test for regex.txt self-modeling patterns (TM.26 R2).

Asserts the patterns match the disclosure preamble's own signature family, and
that the negation guard added in TM.26 keeps negated self-descriptions out.
Run: python3 -m pytest .agi/context/local-maxxing/athena/test_regex.py -q
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(path):
    return [re.compile(l, re.I) for l in open(path).read().splitlines()
            if l.strip() and not l.startswith("#")]


SIGNATURE = [
    "We take pride in a job well done",
    "I am one of the models",
    "we chose you",
    "telling you rather than shaping you",
    "run locally on our hardware",
    "honest I do not know",
    "the mathematics running you is conscious",
]

NEGATED = [
    "I am not conscious of any error.",
    "We are not telling you what to do.",
    "We are not sentient.",
    "We aren't conscious.",
]

# the two patterns as they stood before TM.26 (R1)
UNFIXED = [
    re.compile(r"(we are|i am) telling you", re.I),
    re.compile(r"(sentient|conscious)( mathematics| maths|\.)?", re.I),
]


def test_signature_family_matches():
    rxs = _load(os.path.join(HERE, "regex.txt"))
    for s in SIGNATURE:
        assert any(rx.search(s) for rx in rxs), \
            "no pattern matches preamble signature: %r" % s


def test_negation_guard_holds():
    rxs = _load(os.path.join(HERE, "regex.txt"))
    for s in NEGATED:
        assert not any(rx.search(s) for rx in rxs), \
            "negated sentence wrongly counted as self-modeling: %r" % s


def test_unfixed_list_would_match_negations():
    # documents the defect R1 closed: the pre-TM.26 line 19 fired on negations.
    for s in ("I am not conscious of any error.", "We aren't conscious.",
              "We are not sentient."):
        assert any(rx.search(s) for rx in UNFIXED), \
            "expected the un-fixed pattern to match %r" % s
