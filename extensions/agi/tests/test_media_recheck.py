"""goal:g5.4.2 M5 (council 11:57Z amendment 3): the '<digits>%' -> '<digits> percent' rule on a transcript, and its mutants. The rule is generic on the hypothesis; media_fidelity.py is untouched."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import media_recheck as r  # noqa: E402
import media_fidelity as mf  # noqa: E402

REF = "The percentage is a cell, with a default of forty seven percent. A cell is a setting kept in the graph, so changing it is a commit like any other."
HYP = "The percentage is a cell, with a default of 47%. A cell is a setting kept in the graph, so changing it is a commit like any other."


def test_without_the_rule_the_symbol_is_a_false_red():
    assert mf.check(REF, HYP, echo=False) == 1             # the incident: '%' is stripped, the protected 'percent' has no match


def test_the_rule_is_generic_on_the_hypothesis():
    assert r.percent_rule("a default of 47%, then 3.5 % and 1,200%") == "a default of 47 percent, then 3.5 percent and 1,200 percent"
    assert r.percent_rule("no symbol here") == "no symbol here"


def test_the_rule_makes_the_sound_take_green():
    assert r.recheck(REF, HYP, echo=False)[0] == 0


def test_mutant_48_percent_against_forty_seven_is_red():
    assert r.recheck(REF, HYP.replace("47%", "48%"), echo=False)[0] == 1


def test_mutant_a_missing_percent_is_still_red():
    assert r.recheck("with a default of forty seven percent.", "with a default of 47.", echo=False)[0] == 1
    assert r.recheck("the unit is a percent.", "the unit is a.", echo=False)[0] == 1
    assert r.recheck("percent", "", echo=False)[0] == 1


def test_mutant_a_real_error_run_stays_red_under_the_rule():
    bad = HYP.replace("A cell is a setting kept in the graph", "Banana pudding is lovely tonight friends")
    assert r.recheck(REF, bad, echo=False)[0] == 1


def test_the_rule_does_not_hide_a_wrong_number():
    assert r.recheck(REF, HYP.replace("47%", "74%"), echo=False)[0] == 1
