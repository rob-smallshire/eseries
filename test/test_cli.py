import os

from eseries.cli import main


def test_nearest(capfd):
    code = main("nearest E12 21".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "22\n"


def test_nearest_with_symbol(capfd):
    code = main("nearest E12 21000 -s".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "22 k\n"


def test_nearby(capfd):
    code = main("nearby E24 21".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "18\n20\n22\n"


def test_gt(capfd):
    code = main("gt E24 21".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "22\n"


def test_lt(capfd):
    code = main("lt E24 21".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "20\n"


def test_ge(capfd):
    code = main("ge E24 22".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "22\n"


def test_le(capfd):
    code = main("le E24 22".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "22\n"


def test_tolerance(capfd):
    code = main("tolerance E12".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "0.1\n"


def test_tolerance_e12_percent(capfd):
    code = main("tolerance E12 --symbol".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "10%\n"


def test_tolerance_e192_percent(capfd):
    code = main("tolerance E192 --symbol".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "0.5%\n"


def test_series_e3(capfd):
    code = main("series E3".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "10\n22\n47\n"


def test_range_e12(capfd):
    code = main("range E12 1700 3400".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "1.8e3\n2.2e3\n2.7e3\n3.3e3\n"


def test_range_e12_symbol(capfd):
    code = main("range E12 1700 3400 -s".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "1.8 k\n2.2 k\n2.7 k\n3.3 k\n"


def test_lower_tolerance(capfd):
    code = main("lower-tolerance-limit E48 316".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "310\n"


def test_lower_tolerance_zero(capfd):
    code = main("lower-tolerance-limit E48 0".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "0\n"


def test_upper_tolerance(capfd):
    code = main("upper-tolerance-limit E48 316".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "322\n"


def test_tolerance_limits(capfd):
    code = main("tolerance-limits E48 316".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "310\n322\n"


def test_bogus_e_series_gives_exit_code_ex_dataerr():
    code = main("tolerance-limits E13 316".split())
    assert code == os.EX_DATAERR


def test_bogus_value_gives_exit_code_ex_dataerr():
    code = main("tolerance-limits E12 FOO".split())
    assert code == os.EX_DATAERR


def test_malformed_command_gives_code_ex_usage():
    code = main("foo E13 316".split())
    assert code == os.EX_USAGE