"""Small closed-vocabulary loader for model-facing prose templates."""
from pathlib import Path
from string import Formatter

_TEMPLATE_ROOT = Path(__file__).resolve().parents[1] / "templates"


class TemplateFieldError(ValueError):
    """A required template field was not supplied by the call site."""


def render(family: str, name: str, **fields) -> str:
    """Render one plain-text template, refusing undeclared/missing fields."""
    path = _TEMPLATE_ROOT / family / f"{name}.md"
    text = path.read_text(encoding="utf-8").rstrip("\n")
    required = {field for _, field, _, _ in Formatter().parse(text) if field}
    missing = sorted(required - fields.keys())
    if missing:
        raise TemplateFieldError(
            f"{family}/{name} missing required field(s): {', '.join(missing)}"
        )
    return text.format(**fields)
