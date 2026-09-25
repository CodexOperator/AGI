"""Falsifier for the transport-registry boundary hypothesis.

This is deliberately a test fixture, not a production refactor: it records the
current boundary and proves the smallest proposed seam can host a fake
adapter without editing a router core.
"""
from __future__ import annotations

import ast
from pathlib import Path
import importlib.util
import sys

SEND = Path(__file__).resolve().parents[1] / "bin" / "send.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _tree() -> ast.AST:
    return ast.parse(SEND.read_text(), filename=str(SEND))


def test_pre_fix_boundary_is_measurable() -> None:
    """The current router still has both forbidden couplings, explicitly."""
    tree = _tree()
    rotate_imports = [
        n.lineno for n in ast.walk(tree)
        if isinstance(n, (ast.Import, ast.ImportFrom))
        and any(a.name == "rotate" for a in n.names)
    ]
    assert rotate_imports, "fixture drift: live rotate import disappeared"
    assert any(isinstance(n, ast.If) and "harness" in ast.unparse(n)
               for n in ast.walk(tree)), "fixture drift: harness policy branch disappeared"


def test_fixture_protocol_and_registry_accept_fake_transport(tmp_path: Path) -> None:
    """A protocol-shaped adapter is registered and reached by generic lookup."""
    fixture = FIXTURES / "transport_registry_fixture.py"
    spec = importlib.util.spec_from_file_location("transport_registry_fixture", fixture)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    try:
        fake = tmp_path / "fake_transport.py"
        fake.write_text(
            "def send(request):\n"
            "    return {'transport': 'fake', 'accepted': True, 'text': request['text']}\n"
        )
        module.register("fake", fake)
        result = module.route("fake", {"text": "hello"})
        assert result == {"transport": "fake", "accepted": True, "text": "hello"}
        assert "fake" in module.TRANSPORTS
        assert not hasattr(module, "route_fake"), "router must not branch by transport name"
    finally:
        del sys.modules[spec.name]


def test_fixture_preserves_a_compatibility_shape() -> None:
    """The generic result is sufficient for a compatibility facade."""
    fixture = FIXTURES / "transport_registry_fixture.py"
    spec = importlib.util.spec_from_file_location("transport_registry_fixture_shape", fixture)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    try:
        result = module.route("memory", {"text": "read-only"})
        assert set(result) == {"transport", "accepted", "text"}
        assert result["accepted"] is True
    finally:
        del sys.modules[spec.name]
