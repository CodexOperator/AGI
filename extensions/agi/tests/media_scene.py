#!/usr/bin/env python3
"""goal:g5.4.2 M4: ONE scene class for all 18 chapters, driven by a plan (media_video.py plan C2 plan.json). Run by manim, inside the venv:
  M4_PLAN=plan.json M4_DRAWN=drawn.json M4_REPO=/path/to/repo manim -r 1280,720 --fps 25 --media_dir MEDIA -v WARNING media_scene.py Chapter
The scene draws nothing but media_vocab objects (media_video.lint keeps it so). Beat i runs from t0 to t1 of the plan: a FEED beat brings the cited bytes in, through the Machine,
out as a node of the Graph, with the pair's claim under it; a CALM beat (a sentence that claims nothing about the engine) breathes the graph and shows the sentence. Run times are whole
frames (media_video.schedule), so the chapter's picture is as long as its mp3. The picture is silent: the narration is muxed afterwards (media_video publish)."""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manim import Scene, FadeIn, FadeOut, Indicate, UP, DOWN, LEFT, RIGHT, VGroup  # noqa: E402

import media_video as mv  # noqa: E402
import media_vocab as V  # noqa: E402

FPS = mv.FPS


class Chapter(Scene):
    def construct(self):
        plan = json.load(open(os.environ["M4_PLAN"]))
        repo = os.environ.get("M4_REPO", mv.REPO)
        self.camera.background_color = V.BG
        self.frames = 0
        head = V.caption(f"Chapter {plan['n']}", 22, V.SOFT).to_corner(UP + LEFT, buff=0.5)
        title = V.caption(plan["title"], 28, V.INK).next_to(head, DOWN, aligned_edge=LEFT, buff=0.12)
        if title.width > 10.6:
            title.scale_to_fit_width(10.6).next_to(head, DOWN, aligned_edge=LEFT, buff=0.12)      # scaling moves the title about its centre: put its left edge back under the chapter label
        assert abs(title.get_left()[0] - head.get_left()[0]) < 0.01, "the title is not left-aligned under the chapter label"
        machine = V.Machine([1.7, 0.5, 0], "reads the bytes")
        graph = V.Graph([4.3, 2.1])
        tick = V.Tick([6.3, 3.35, 0], len(plan["beats"]))
        self.add(head, title, machine.group, tick.group)
        self.last = None
        for b in plan["beats"]:
            self.beat(b, plan, repo, machine, graph, tick)
        self.hold(plan["duration"] + 0.2)

    def tear_down(self):
        super().tear_down()
        V.dump(os.environ["M4_DRAWN"])         # what was drawn from the engine, for media_video.check_drawn; written on every run, cached partials or not

    # -- time: every wait and play is a whole number of frames, and the beat ends on its plan time
    def run(self, anims, frames):
        self.play(*anims, run_time=frames / FPS)
        self.frames += frames

    def hold(self, until):
        n = round(until * FPS) - self.frames
        if n > 0:
            self.wait(n / FPS)
            self.frames += n

    def beat(self, b, plan, repo, machine, graph, tick):
        t0, t1 = b["t0"], b["t1"]
        self.hold(t0)
        if b["kind"] == "calm":
            self.calm(b, t1, graph, tick)
        else:
            self.feed(b, plan, repo, t1, machine, graph, tick)
        self.hold(t1)

    def calm(self, b, t1, graph, tick):
        say = V.caption(b["spoken"], 28, V.SOFT, width=58)
        if say.height > 1.45:
            say.scale_to_fit_height(1.45)
        say.to_edge(DOWN, buff=0.5).align_to([-6.6, 0, 0], LEFT)
        parts = [0.4, 0.5, 0.3]
        want, rest = mv.schedule(b["t0"], t1, parts)
        self.run([FadeIn(say, shift=UP * 0.15)] + [tick.advance()], want[0])
        pulse = [Indicate(graph.nodes[-1], scale_factor=1.5, color=V.WARM)] if graph.nodes else []
        self.run(pulse or [FadeIn(say)], want[1])
        self.hold(b["t0"] + (sum(want) + rest - want[2]) / FPS)
        self.run([FadeOut(say)], want[2])

    def feed(self, b, plan, repo, t1, machine, graph, tick):
        """The beat's pairs in chunks of two, one chunk after the other across the beat; the sentence stays under all of them."""
        chunks = mv.pair_chunks(b["pairs"])
        claim = V.caption(b["spoken"], 26, V.INK, width=66)
        if claim.height > 1.45:                              # more than four lines (C13's longest sentence has five): scaled to the height of four so it never reaches the strand or the file name
            claim.scale_to_fit_height(1.45)
        claim.to_edge(DOWN, buff=0.45).align_to([-6.6, 0, 0], LEFT)
        for k, ((c0, c1), pairs) in enumerate(zip(mv.chunk_times(b["t0"], t1, len(chunks)), chunks)):
            self.feed_chunk(b, pairs, c0, c1, machine, graph, tick, claim, first=k == 0, last=k == len(chunks) - 1)

    def feed_chunk(self, b, pairs, t0, t1, machine, graph, tick, claim, first, last):
        from manim import RoundedRectangle
        strand_objs = [V.Strand(repo=os.environ.get("M4_REPO", mv.REPO), sha=p["sha"], path=p["path"], lo=p["lo"], hi=p["hi"], needle=p["needle"], beat=b["i"]) for p in pairs]
        strands = [so.mobject() for so in strand_objs]
        cites = [V.Cite(p["sha"], p["path"], p["lo"], p["hi"], b["i"]) for p in pairs]
        stack = VGroup(*strands).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        if stack.height > 3.7:
            stack.scale_to_fit_height(3.7)
        stack.to_edge(LEFT, buff=0.6).set_y(0.15)
        floor = claim.get_top()[1] + 0.3                     # a long sentence under two strands must not touch them: shrink the stack into the room that is left (recorded, RED below MIN_SCALE)
        if stack.get_bottom()[1] < floor:
            before = stack.height
            stack.scale_to_fit_height(2.3 - floor).to_edge(LEFT, buff=0.6).set_y((2.3 + floor) / 2)
            V.note_layout(b["i"], stack.height / before)
        needle = strand_objs[0].needle_mobject().move_to(stack.get_center())
        node, edge, grow = graph.add()
        chip_label = cites[0].mobject(16, V.INK)
        chip = VGroup(RoundedRectangle(corner_radius=0.12, width=chip_label.width + 0.3, height=0.42, stroke_color=V.WARM, stroke_width=2, fill_color=V.PANEL, fill_opacity=1), chip_label)
        chip_label.move_to(chip[0])
        chip.next_to(machine.out, RIGHT, buff=0.12)
        # appear -> (the sentence is spoken while the bytes are on screen) -> the needle goes in -> the machine reads -> the chip comes out and becomes a node -> fade
        parts = [0.5, 1.0, 0.35, 0.9, 0.3]
        want, rest = mv.schedule(t0, t1, parts)
        self.run([FadeIn(stack, shift=RIGHT * 0.3)] + ([FadeIn(claim, shift=UP * 0.15)] if first else []) + machine.relabel(cites[0]) + ([tick.advance()] if first else []), want[0])
        self.hold(t0 + (want[0] + rest) / FPS)
        self.add(needle)
        self.run([needle.animate.scale(0.5).move_to(machine.inp.get_center() + LEFT * 0.7), stack.animate.set_opacity(0.3)], want[1])
        self.run([machine.flash(), machine.scan(), FadeOut(needle, scale=0.3)], want[2])
        self.add(chip)
        self.run([chip.animate.scale(0.2).move_to(node.get_center())] + grow, want[3])
        self.run([FadeOut(stack), FadeOut(chip)] + ([FadeOut(claim)] if last else []), want[4])
