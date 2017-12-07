from hypothesis import given
from hypothesis.strategies import integers, floats

from eseries.eng import eng_string


def test_eng_string_zero():
    assert eng_string(0) == "0"


@given(x=integers(max_value=-1))
def test_eng_string_negative_sign(x):
    assert eng_string(x).startswith('-')


@given(x=integers(min_value=0))
def test_eng_string_non_negative_sign(x):
    assert not eng_string(x).startswith('-')


@given(x=integers(min_value=-999, max_value=999))
def test_eng_string_less_than_one_thousand(x):
    assert eng_string(x) == str(x)


@given(x=floats(min_value=1000, max_value=999999))
def test_eng_string_less_e3(x):
    assert eng_string(x, prefix=False).endswith('e3')


@given(x=floats(min_value=1000, max_value=999999))
def test_eng_string_kilo(x):
    assert eng_string(x, prefix=True).endswith(' k')


@given(x=floats(min_value=1000000, max_value=999999999))
def test_eng_string_mega(x):
    assert eng_string(x, prefix=True).endswith(' M')