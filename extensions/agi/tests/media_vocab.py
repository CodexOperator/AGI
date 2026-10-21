#!/usr/bin/env python3
"""goal:g5.4.2 M4: the visual vocabulary of the animated explainer, and the ONLY file that may draw text (media_video.lint reds a raw Text/Code/MarkupText anywhere else).
  Strand   a window of REAL engine bytes (the cited line around the needle): it reads `git show SHA:PATH` itself, the needle is drawn warm, and every span it hands to the
           renderer is recorded in DRAWN; media_video.check_drawn later re-reads the engine and requires each recorded string to be a substring of it (council C1).
  Cite     "file, line N": the file and the lines must exist at the sha; recorded.
  Machine  a block with an in-port and an out-port that reads strands and emits a tool chip (the ribosome of the first chapters, any reader of bytes later).
  Graph    nodes and edges that grow, one node per cited piece; Tick = the commit clock, one step per beat.
  Caption  words that are NOT engine text (the chapter title, the claim of a pair, the narrator's sentence): drawn, never checked against the engine.
manim is imported inside the functions that draw, so the bookkeeping (and its tests) runs without it.
"""
import html
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import media_video as mv  # noqa: E402

BG, INK, SOFT, ACCENT, WARM, EDGE, PANEL = "#0e1513", "#e9efec", "#9fb0a8", "#8db8ff", "#ffb86b", "#44564f", "#16201d"
MONO, SANS = "DejaVu Sans Mono", "DejaVu Sans"
DRAWN = []


def dump(path):
    """The record of everything drawn from the engine, for media_video.check_drawn."""
    json.dump(DRAWN, open(path, "w"), indent=1)


def _markup(spans, size, font, color=INK):
    """MarkupText for a list of (text, hot) spans. Records nothing itself: the Strand does."""
    from manim import MarkupText
    body = "".join(f'<span foreground="{WARM if hot else color}"{" weight=\'bold\'" if hot else ""}>{html.escape(t, quote=False)}</span>' for t, hot in spans)
    return MarkupText(body, font=font, font_size=size)


class Strand:
    """A window of engine bytes. Built from WHERE the bytes are (repo, sha, path, lines, needle): the scene never hands it text."""
    def __init__(self, repo, sha, path, lo, hi, needle, beat, width=26):
        self.sha, self.path, self.lo, self.hi, self.beat, self.needle = sha, path, lo, hi, beat, needle
        self.window, i0, i1 = mv.strand_window(repo, sha, path, lo, hi, needle)
        self.lines = mv.wrap(self.window, i0, i1, width)
        if mv.rejoin(self.lines) != self.window:
            raise ValueError("wrap lost bytes")

    def mobject(self, size=32, maxw=5.9):
        from manim import VGroup, LEFT, DOWN
        rows = VGroup(*[_markup([sp for sp in ln if sp[0] != "\n"] or [(" ", False)], size, MONO) for ln in self.lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        w0, scale = rows.width, 1.0
        if rows.width > maxw:
            rows.scale_to_fit_width(maxw)
            scale = maxw / w0
        DRAWN.append({"kind": "strand", "beat": self.beat, "sha": self.sha, "path": self.path, "lo": self.lo, "hi": self.hi, "text": mv.rejoin(self.lines),
                      "rows": ["".join(t for t, _ in ln if t != "\n") for ln in self.lines], "scale": round(scale, 3)})
        return rows

    def needle_mobject(self, size=30, maxw=2.6):
        """The needle alone, warm: the piece of the bytes that the sentence is about, small enough to travel. Recorded like the window (it is a substring of it)."""
        m = _markup([(self.needle, True)], size, MONO)
        if m.width > maxw:
            m.scale_to_fit_width(maxw)
        DRAWN.append({"kind": "strand", "beat": self.beat, "sha": self.sha, "path": self.path, "lo": self.lo, "hi": self.hi, "text": self.needle})
        return m


class Cite:
    """"engine-root.md, line 41": a pointer to the bytes."""
    def __init__(self, sha, path, lo, hi, beat):
        self.sha, self.path, self.lo, self.hi, self.beat = sha, path, lo, hi, beat
        self.label = f"{os.path.basename(path)}, line {lo}" + (f"-{hi}" if hi != lo else "")

    def mobject(self, size=20, color=ACCENT):
        DRAWN.append({"kind": "cite", "beat": self.beat, "sha": self.sha, "path": self.path, "lo": self.lo, "hi": self.hi})
        return caption(self.label, size, color, font=MONO)


def caption(text, size=26, color=INK, width=None, font=SANS):
    """Words that are not engine bytes. Wrapped at `width` characters if given."""
    import textwrap
    from manim import VGroup, LEFT, DOWN
    lines = textwrap.wrap(text, width) if width else [text]
    g = VGroup(*[_markup([(ln, False)], size, font, color) for ln in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    return g


class Machine:
    """The reader: a rounded block, an in-port on its left, an out-port on its right; the file it is reading is named UNDER it."""
    def __init__(self, center, label):
        from manim import RoundedRectangle, Circle, VGroup, Line, DOWN
        self.box = RoundedRectangle(corner_radius=0.22, width=2.3, height=2.6, stroke_color=ACCENT, stroke_width=3, fill_color=PANEL, fill_opacity=1).move_to(center)
        self.inp = Circle(radius=0.13, stroke_color=ACCENT, fill_color=ACCENT, fill_opacity=1).move_to(self.box.get_left())
        self.out = Circle(radius=0.13, stroke_color=WARM, fill_color=WARM, fill_opacity=1).move_to(self.box.get_right())
        self.label = caption(label, 20, SOFT, font=MONO).next_to(self.box, DOWN, buff=0.3)
        self.lines = VGroup(*[Line(self.box.get_center() + [-0.7, 0.8 - 0.33 * k, 0], self.box.get_center() + [-0.7 + w, 0.8 - 0.33 * k, 0], color=EDGE, stroke_width=5) for k, w in enumerate((1.3, 0.9, 1.4, 0.7, 1.1, 0.5))])
        self.group = VGroup(self.box, self.lines, self.inp, self.out, self.label)

    def flash(self):
        """A warm light runs once round the block's own outline (rounded like it)."""
        from manim import ShowPassingFlash
        ring = self.box.copy().set_fill(opacity=0).set_stroke(color=WARM, width=8)
        return ShowPassingFlash(ring, time_width=0.8)

    def scan(self):
        """The reading: the lines inside the block light up one after the other."""
        from manim import LaggedStart, Indicate
        return LaggedStart(*[Indicate(l, scale_factor=1.0, color=ACCENT) for l in self.lines], lag_ratio=0.25)

    def relabel(self, cite):
        from manim import FadeIn, FadeOut, DOWN
        new = cite.mobject(20, SOFT).next_to(self.box, DOWN, buff=0.3)
        old, self.label = self.label, new
        return [FadeOut(old), FadeIn(new)]


class Graph:
    """Nodes and edges that grow. One node per cited piece, laid on a fixed lattice at the right of the frame, each linked to the one before it."""
    COLS = 4

    def __init__(self, origin):
        self.origin, self.nodes, self.edges = origin, [], []

    def slot(self, k):
        import numpy as np
        r, c = divmod(k, self.COLS)
        c = c if r % 2 == 0 else self.COLS - 1 - c          # a snake, so each node touches the one before it
        return np.array([self.origin[0] + 0.66 * c, self.origin[1] - 0.66 * r, 0.0])

    def add(self):
        """-> (node, edge or None, [animations]) for the next node."""
        from manim import Dot, Line, GrowFromCenter, Create
        k = len(self.nodes)
        n = Dot(self.slot(k), radius=0.15, color=ACCENT)
        e = Line(self.nodes[-1].get_center(), n.get_center(), color=EDGE, stroke_width=4) if self.nodes else None
        self.nodes.append(n)
        if e is not None:
            self.edges.append(e)
        return n, e, ([Create(e)] if e is not None else []) + [GrowFromCenter(n)]


class Tick:
    """The commit clock: a ring and one hand that steps by 1/steps of a turn per beat."""
    def __init__(self, center, steps):
        import numpy as np
        from manim import Circle, Line, VGroup
        center = np.array(center, dtype=float)
        self.center, self.step = center, 6.283185307 / max(steps, 1)
        self.ring = Circle(radius=0.32, stroke_color=SOFT, stroke_width=3).move_to(center)
        self.hand = Line(center, center + np.array([0, 0.26, 0]), color=WARM, stroke_width=4)
        self.group = VGroup(self.ring, self.hand)

    def advance(self):
        from manim import Rotate
        return Rotate(self.hand, angle=-self.step, about_point=self.center, rate_func=lambda t: t)
