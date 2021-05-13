"""The command-line for eseries"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from builtins import int
from future import standard_library
standard_library.install_aliases()
import os
import sys

import docopt
import docopt_subcommands as dsc

from eseries.eng import eng_string
from eseries.version import __version__
from eseries.eseries import series_key_from_name, find_nearest, find_nearest_few, find_greater_than_or_equal, \
    find_greater_than, find_less_than, find_less_than_or_equal, tolerance, series, erange, lower_tolerance_limit, \
    tolerance_limits, upper_tolerance_limit

DOC_TEMPLATE = """{program}

Usage: {program} [options] <command> [<args> ...]

Options:
  -h --help     Show this screen.
  -v --verbose  Use verbose logging

Available commands:
  {available_commands}

See '{program} help <command>' for help on specific commands.
"""


@dsc.command()
def handle_nearest(precommand, args):
    """usage: {program} nearest <e-series> <value> [--symbol]

    The nearest value in an E-Series.

    Options:
      -s --symbol  Use the SI magnitude prefix symbol.
    """
    series_key = extract_series_key(args)
    value = extract_value(args)
    nearest = find_nearest(series_key, value)
    nearest_text = present_value(args, nearest)
    print(nearest_text)
    return os.EX_OK


@dsc.command()
def handle_nearby(precommand, args):
    """usage: {program} nearby <e-series> <value> [--symbol]

    At least three nearby values in an E-Series, and least one of
    which will be less-than the given value, and at least one
    greater-than the given value.

    Options:
      -s --symbol  Use the SI magnitude prefix symbol.
    """
    series_key = extract_series_key(args)
    value = extract_value(args)
    nearby_few = find_nearest_few(series_key, value)
    for item in nearby_few:
        item_text = present_value(args, item)
        print(item_text)
    return os.EX_OK


@dsc.command()
def handle_gt(precommand, args):
    """usage: {program} gt <e-series> <value> [--symbol]

    The largest value greater-than the given value.

    Options:
      -s --symbol  Use the SI magnitude prefix symbol.
    """
    series_key = extract_series_key(args)
    value = extract_value(args)
    nearest = find_greater_than(series_key, value)
    nearest_text = present_value(args, nearest)
    print(nearest_text)
    return os.EX_OK


@dsc.command()
def handle_ge(precommand, args):
    """usage: {program} ge <e-series> <value> [--symbol]

    The largest value greater-than or equal-to the given value.

    Options:
      -s --symbol  Use the SI magnitude prefix symbol.
    """
    series_key = extract_series_key(args)
    value = extract_value(args)
    nearest = find_greater_than_or_equal(series_key, value)
    nearest_text = present_value(args, nearest)
    print(nearest_text)
    return os.EX_OK


@dsc.command()
def handle_lt(precommand, args):
    """usage: {program} lt <e-series> <value> [--symbol]

    The largest value less-than the given value.

    Options:
      -s --symbol  Use the SI magnitude prefix symbol.
    """
    series_key = extract_series_key(args)
    value = extract_value(args)
    nearest = find_less_than(series_key, value)
    nearest_text = present_value(args, nearest)
    print(nearest_text)
    return os.EX_OK


@dsc.command()
def handle_le(precommand, args):
    """usage: {program} le <e-series> <value> [--symbol]

    The largest value less-than or equal-to the given value.

    Options:
      -s --symbol  Use the SI magnitude prefix symbol.
    """
    series_key = extract_series_key(args)
    value = extract_value(args)
    nearest = find_less_than_or_equal(series_key, value)
    nearest_text = present_value(args, nearest)
    print(nearest_text)
    return os.EX_OK


@dsc.command()
def handle_tolerance(precommand, args):
    """usage: {program} tolerance <e-series> [--symbol]

    The tolerance of the given E-Series.

    Options:
     -s --symbol  Display as a percentage.
    """
    series_key = extract_series_key(args)
    tol = tolerance(series_key)
    if args['--symbol']:
        percent = float(tol * 100)
        if percent.is_integer():
            percent = int(percent)
        print("{}%".format(percent))
    else:
        print(tol)
    return os.EX_OK

@dsc.command()
def handle_series(precommand, args):
    """usage: {program} series <e-series>

    The base values for the given E-Series.
    """
    series_key = extract_series_key(args)
    for item in series(series_key):
        print(item)
    return os.EX_OK


@dsc.command()
def handle_range(precommand, args):
    """usage: {program} range <e-series> <start-value> <stop-value> [--symbol]

    All values in the given E-series from start-value to stop-value inclusive.

    Options:
      -s --symbol  Use the SI magnitude prefix symbol.
    """
    series_key = extract_series_key(args)
    start_value = extract_value(args, '<start-value>')
    stop_value = extract_value(args, '<stop-value>')
    items = erange(series_key, start_value, stop_value)
    for item in items:
        item_text = present_value(args, item)
        print(item_text)
    return os.EX_OK


@dsc.command()
def handle_lower_tolerance_limit(precommand, args):
    """usage: {program} lower-tolerance-limit <e-series> <value> [--symbol]

    The lower tolerance limit of a nominal value given the tolerance
    of the specified E-Series.

    Options:
      -s --symbol  Use the SI magnitude prefix symbol.
    """
    series_key = extract_series_key(args)
    value = extract_value(args)
    lower = lower_tolerance_limit(series_key, value)
    lower_text = present_value(args, lower)
    print(lower_text)
    return os.EX_OK


@dsc.command()
def handle_upper_tolerance_limit(precommand, args):
    """usage: {program} upper-tolerance-limit <e-series> <value> [--symbol]

    The upper tolerance limit of a nominal value given the tolerance
    of the specified E-Series.

    Options:
      -s --symbol  Use the SI magnitude prefix symbol.
    """
    series_key = extract_series_key(args)
    value = extract_value(args)
    upper = upper_tolerance_limit(series_key, value)
    upper_text = present_value(args, upper)
    print(upper_text)
    return os.EX_OK


@dsc.command()
def handle_tolerance_limits(precommand, args):
    """usage: {program} tolerance-limits <e-series> <value> [--symbol]

    The upper and lower tolerance limits of a nominal value given the
    tolerance of the specified E-Series.

    Options:
      -s --symbol  Use the SI magnitude prefix symbol.
    """
    series_key = extract_series_key(args)
    value = extract_value(args)
    lower, upper = tolerance_limits(series_key, value)
    lower_text = present_value(args, lower)
    upper_text = present_value(args, upper)
    print(lower_text)
    print(upper_text)
    return os.EX_OK


def present_value(args, nearest):
    return eng_string(nearest, prefix=args['--symbol'])


def extract_series_key(args):
    e_series_name = args['<e-series>'].upper()
    series_key = series_key_from_name(e_series_name)
    return series_key


def extract_value(args, name='<value>'):
    text_value = args[name]
    try:
        value = float(text_value)
    except ValueError:
        raise ValueError("{!r} could not be interpreted as an E-Series {}".format(
            text_value, name[1:-1]))
    return value


def main(argv=None):
    try:
        return dsc.main(
            program='eseries',
            argv=argv,
            doc_template=DOC_TEMPLATE,
            exit_at_end=False)
    except (docopt.DocoptExit, SystemExit) as exc:
        print(exc, file=sys.stderr)
        return os.EX_USAGE
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return os.EX_DATAERR


if __name__ == '__main__':
    sys.exit(main())
