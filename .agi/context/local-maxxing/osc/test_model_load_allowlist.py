"""The basetemp ALLOW-LIST: a declared dir may be read back, an undeclared one
may not. Stand-ins only -- no library, no weights file, no network.

The motivating case is osc_lowpeak_test.py:46-51, which builds a tiny config-built
Qwen2 in its own tmp dir and reads it back with from_pretrained. The guard must let
that through on a python where transformers EXISTS, and must still refuse a
from_pretrained on a dir under tmp_path that the test never declared -- otherwise
"under tmp_path" is not a guard, it is a shape.
"""

import sys
import types

import pytest


def _standin_transformers():
    """The REAL shape, module + submodule: the loader class is a classmethod held
    on `transformers.models.llama`, and the conftest's meta_path hook patches it
    at exec time even when the import happens inside the body."""
    calls = []

    class AutoModelForCausalLM:
        @classmethod
        def from_pretrained(cls, name, **kw):
            calls.append((name, kw))
            return "RECORDED"

    sub = types.ModuleType("transformers.models.llama")
    sub.AutoModelForCausalLM = AutoModelForCausalLM
    root = types.ModuleType("transformers")
    return root, sub, calls


@pytest.fixture
def tf_standin(tmp_path, monkeypatch):
    root, sub, _calls = _standin_transformers()
    (tmp_path / "transformers").mkdir()
    (tmp_path / "transformers" / "models").mkdir()
    (tmp_path / "transformers" / "__init__.py").write_text("")
    (tmp_path / "transformers" / "models" / "__init__.py").write_text("")
    (tmp_path / "transformers" / "models" / "llama.py").write_text(
        "class AutoModelForCausalLM:\n"
        "    CALLS = []\n"
        "    @classmethod\n"
        "    def from_pretrained(cls, name, **kw):\n"
        "        cls.CALLS.append(name)\n"
        "        return 'RECORDED'\n")
    monkeypatch.syspath_prepend(str(tmp_path))
    for name in ("transformers", "transformers.models", "transformers.models.llama"):
        monkeypatch.delitem(sys.modules, name, raising=False)
    import transformers.models.llama as m  # noqa: PLC0415 -- the in-body import IS the shape
    yield m
    for name in ("transformers", "transformers.models", "transformers.models.llama"):
        sys.modules.pop(name, None)


def test_under_tmp_path_but_undeclared_is_still_refused(tmp_path, tf_standin,
                                                         model_load_refusal):
    """THE GATE: a dir under pytest's basetemp is NOT a licence. Undeclared, a
    from_pretrained on it raises, and the real loader is never reached."""
    m = tf_standin
    ckpt = tmp_path / "Qwen3-8B"          # looks exactly like a downloaded snapshot
    ckpt.mkdir()
    with pytest.raises(model_load_refusal):
        m.AutoModelForCausalLM.from_pretrained(str(ckpt))
    assert m.AutoModelForCausalLM.CALLS == []


def test_a_declared_dir_the_test_built_is_read_back(tmp_path, tf_standin,
                                                   allow_model_load):
    """The allow-list earns its keep: a tiny config-built checkpoint the test wrote
    into its own tmp dir is read by the REAL loader, not refused."""
    m = tf_standin
    ckpt = tmp_path / "tiny-qwen2"
    ckpt.mkdir()
    (ckpt / "config.json").write_text("{}")
    (ckpt / "model.safetensors").write_bytes(b"\x00" * 16)   # a few MB in reality
    allow_model_load(ckpt)
    assert m.AutoModelForCausalLM.from_pretrained(str(ckpt)) == "RECORDED"
    assert m.AutoModelForCausalLM.CALLS == [str(ckpt)]


def test_a_declaration_does_not_cover_a_sibling_dir(tmp_path, tf_standin,
                                                   allow_model_load, model_load_refusal):
    """The declaration is a PATH, not a subtree: the dir next to it is still refused."""
    m = tf_standin
    allow_model_load(tmp_path / "tiny")
    with pytest.raises(model_load_refusal):
        m.AutoModelForCausalLM.from_pretrained(str(tmp_path / "tiny-8b"))


def test_a_hub_id_is_refused_even_though_it_is_a_string(tmp_path, tf_standin,
                                                        model_load_refusal):
    """A hub id resolves to no local realpath, so nothing can be declared for it."""
    m = tf_standin
    with pytest.raises(model_load_refusal):
        m.AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-8B")
    assert m.AutoModelForCausalLM.CALLS == []


def test_a_declared_dir_over_the_byte_cap_is_still_refused(tmp_path, tf_standin,
                                                           allow_model_load,
                                                           model_load_refusal,
                                                           monkeypatch):
    """Falsifier 3 survives the allow-list: a declared dir is still capped, so it
    cannot become the > ~200 MiB hole. The cap is read from the config cell
    `values.core.model_load_allowed_max_bytes`; the test lowers it to 0 rather
    than writing 64 MiB on a memory-guarded box."""
    conftest = sys.modules[_no_model_load_owner()]
    m = tf_standin
    ckpt = tmp_path / "tiny"
    ckpt.mkdir()
    (ckpt / "model.safetensors").write_bytes(b"\x00" * 32)
    allow_model_load(ckpt)
    monkeypatch.setattr(conftest, "MAX_ALLOWED_LOAD_BYTES", 0)
    with pytest.raises(model_load_refusal):
        m.AutoModelForCausalLM.from_pretrained(str(ckpt))
    assert m.AutoModelForCausalLM.CALLS == []


def test_a_declaration_never_outlives_its_test(tmp_path, tf_standin, allow_model_load):
    """The first half of the leak falsifier: the declaration IS live inside the
    test that made it. Read the other half in test_zz_below, which runs after."""
    (tmp_path / "tiny").mkdir()
    allow_model_load(tmp_path / "tiny")
    assert _declared_now(tmp_path / "tiny")


def test_zz_a_later_test_sees_no_declaration(tmp_path, tf_standin, model_load_refusal):
    """The second half: the autouse fixture clears the set at teardown, so this
    later test inherits no hole -- the set is empty and the call is refused."""
    assert not _declared_now(tmp_path / "tiny")
    with pytest.raises(model_load_refusal):
        tf_standin.AutoModelForCausalLM.from_pretrained(str(tmp_path / "tiny"))


def _declared_now(path):
    conftest = sys.modules[_no_model_load_owner()]
    import os
    return os.path.realpath(path) in conftest._ALLOWED


def _no_model_load_owner():
    for name, m in list(sys.modules.items()):
        d = m.__dict__ if isinstance(m, types.ModuleType) else {}
        if "ModelLoadRefused" in d and "_patch_one" in d:
            return name
    pytest.skip("the .agi/context conftest is not loaded in this run")


def test_an_inherited_classmethod_loader_keeps_the_subclass_and_reads_files_under_the_dir(
        tmp_path, monkeypatch, allow_model_load, model_load_refusal):
    """The REAL transformers shape the stand-in above does not have: from_pretrained
    is a classmethod DEFINED on a base (`_BaseAutoModelClass`) and CALLED on a
    subclass, and the loader then opens `<dir>/model.safetensors` -- a FILE under
    the declared dir. DH.413 harvest (director-engine): the stub read a[0] -- the
    CLASS -- as the path, so osc_lowpeak_test.py's declared tmp checkpoint was
    refused; delegating would also have re-bound the base. Both halves pinned."""
    pkg = tmp_path / "shim"
    (pkg / "transformers").mkdir(parents=True)
    (pkg / "transformers" / "__init__.py").write_text(
        "class _Base:\n"
        "    SEEN = []\n"
        "    @classmethod\n"
        "    def from_pretrained(cls, name, **kw):\n"
        "        cls.SEEN.append((cls.__name__, str(name)))\n"
        "        return cls\n"
        "class AutoModelForCausalLM(_Base):\n"
        "    pass\n")
    monkeypatch.syspath_prepend(str(pkg))
    monkeypatch.delitem(sys.modules, "transformers", raising=False)
    try:
        import transformers as t  # noqa: PLC0415 -- the in-body import IS the shape
        ckpt = tmp_path / "tiny"
        ckpt.mkdir()
        (ckpt / "model.safetensors").write_bytes(b"\x00" * 16)
        allow_model_load(ckpt)
        assert t.AutoModelForCausalLM.from_pretrained(ckpt) is t.AutoModelForCausalLM
        assert t.AutoModelForCausalLM.from_pretrained(ckpt / "model.safetensors") \
            is t.AutoModelForCausalLM
        assert t._Base.SEEN == [("AutoModelForCausalLM", str(ckpt)),
                                ("AutoModelForCausalLM", str(ckpt / "model.safetensors"))]
        with pytest.raises(model_load_refusal):
            t.AutoModelForCausalLM.from_pretrained(tmp_path / "tiny-8b" / "model.safetensors")
    finally:
        sys.modules.pop("transformers", None)
