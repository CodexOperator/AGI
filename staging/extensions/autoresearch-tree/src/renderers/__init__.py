"""renderers: multi-format renderers over a shared internal representation (R1+)."""

from .ascii import render_ascii
from .git_diff import MismatchedRunsError, render_git_diff
from .mermaid import render_mermaid
from .representation import RenderToken, Representation, build_representation

__all__ = [
    "RenderToken",
    "Representation",
    "build_representation",
    "render_ascii",
    "render_mermaid",
    "render_git_diff",
    "MismatchedRunsError",
]
