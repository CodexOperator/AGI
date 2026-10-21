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
        title = V.caption(plan["title"], 30, V.INK, width=52).next_to(head, DOWN, aligned_edge=LEFT, buff=0.12)
        machine = V.Machine([-0.6, 0.5, 0], "reads the bytes")
        graph = V.Graph([3.9, 2.3])
        tick = V.Tick([6.2, -3.2, 0], len(plan["beats"]))
        self.add(head, title, machine.group, tick.group)
        self.last = None
        for b in plan["beats"]:
            self.beat(b, plan, repo, machine, graph, tick)
        self.hold(plan["duration"] + 0.2)

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
        say = V.caption(b["spoken"], 26, V.SOFT, width=70).to_edge(DOWN, buff=0.6)
        parts = [0.4, 0.5, 0.3]
        want, rest = mv.schedule(b["t0"], t1, parts)
        self.run([FadeIn(say, shift=UP * 0.15)] + [tick.advance()], want[0])
        pulse = [Indicate(graph.nodes[-1], scale_factor=1.5, color=V.WARM)] if graph.nodes else []
        self.run(pulse or [FadeIn(say)], want[1])
        self.hold(b["t0"] + (sum(want) + rest - want[2]) / FPS)
        self.run([FadeOut(say)], want[2])

    def feed(self, b, plan, repo, t1, machine, graph, tick):
        pairs = b["pairs"][:2]
        strands = [V.Strand(repo, p["sha"], p["path"], p["lo"], p["hi"], p["needle"], b["i"]).mobject() for p in pairs]
        cites = [V.Cite(p["sha"], p["path"], p["lo"], p["hi"], b["i"]) for p in pairs]
        stack = VGroup(*strands).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-4.6, 0.5, 0])
        if stack.width > 6.2:
            stack.scale_to_fit_width(6.2)
        claim = V.caption(pairs[0]["claim"], 24, V.INK, width=78).to_edge(DOWN, buff=0.55)
        node, edge, grow = graph.add()
        parts = [0.5, 0.7, 0.4, 0.7, 0.3]
        want, rest = mv.schedule(b["t0"], t1, parts)
        self.run([FadeIn(stack, shift=RIGHT * 0.3), FadeIn(claim, shift=UP * 0.15)] + machine.relabel(cites[0]) + [tick.advance()], want[0])
        self.run([stack.animate.scale(0.45).next_to(machine.inp, LEFT, buff=0.1)], want[1])
        self.run([Indicate(machine.box, scale_factor=1.04, color=V.ACCENT)], want[2])
        self.run(grow, want[3])
        self.hold(b["t0"] + (sum(want) + rest - want[4]) / FPS)
        self.run([FadeOut(stack), FadeOut(claim)], want[4])
