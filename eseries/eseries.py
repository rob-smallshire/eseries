from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from builtins import int
# from builtins import round
from builtins import range
from builtins import map
from builtins import zip
from builtins import str
from future import standard_library
standard_library.install_aliases()
from bisect import bisect_right, bisect_left
from collections import OrderedDict
from enum import IntEnum

import math
from math import log10, floor


_MINIMUM_E_VALUE = 1e-200


class ESeries(IntEnum):
    """An enumeration of possible E-Series identifiers.
    """
    E3 = 3
    E6 = 6
    E12 = 12
    E24 = 24
    E48 = 48
    E96 = 96
    E192 = 192


E3 = ESeries.E3
E6 = ESeries.E6
E12 = ESeries.E12
E24 = ESeries.E24
E48 = ESeries.E48
E96 = ESeries.E96
E192 = ESeries.E192


_E = OrderedDict((
    (E3, (10, 22, 47)),
    (E6, (10, 15, 22, 33, 47, 68)),
    (E12, (10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82)),
    (E24, (10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91)),
    (E48, (100, 105, 110, 115, 121, 127, 133, 140, 147, 154, 162, 169, 178, 187, 196, 205, 215, 226, 237, 249, 261, 274,
        287, 301, 316, 332, 348, 365, 383, 402, 422, 442, 464, 487, 511, 536, 562, 590, 619, 649, 681, 715, 750, 787,
        825, 866, 909, 953)),
    (E96, (100, 102, 105, 107, 110, 113, 115, 118, 121, 124, 127, 130, 133, 137, 140, 143, 147, 150, 154, 158, 162, 165,
        169, 174, 178, 182, 187, 191, 196, 200, 205, 210, 215, 221, 226, 232, 237, 243, 249, 255, 261, 267, 274, 280,
        287, 294, 301, 309, 316, 324, 332, 340, 348, 357, 365, 374, 383, 392, 402, 412, 422, 432, 442, 453, 464, 475,
        487, 499, 511, 523, 536, 549, 562, 576, 590, 604, 619, 634, 649, 665, 681, 698, 715, 732, 750, 768, 787, 806,
        825, 845, 866, 887, 909, 931, 953, 976)),
    (E192, (100, 101, 102, 104, 105, 106, 107, 109, 110, 111, 113, 114, 115, 117, 118, 120, 121, 123, 124, 126, 127, 129,
          130, 132, 133, 135, 137, 138, 140, 142, 143, 145, 147, 149, 150, 152, 154, 156, 158, 160, 162, 164, 165, 167,
          169, 172, 174, 176, 178, 180, 182, 184, 187, 189, 191, 193, 196, 198, 200, 203, 205, 208, 210, 213, 215, 218,
          221, 223, 226, 229, 232, 234, 237, 240, 243, 246, 249, 252, 255, 258, 261, 264, 267, 271, 274, 277, 280, 284,
          287, 291, 294, 298, 301, 305, 309, 312, 316, 320, 324, 328, 332, 336, 340, 344, 348, 352, 357, 361, 365, 370,
          374, 379, 383, 388, 392, 397, 402, 407, 412, 417, 422, 427, 432, 437, 442, 448, 453, 459, 464, 470, 475, 481,
          487, 493, 499, 505, 511, 517, 523, 530, 536, 542, 549, 556, 562, 569, 576, 583, 590, 597, 604, 612, 619, 626,
          634, 642, 649, 657, 665, 673, 681, 690, 698, 706, 715, 723, 732, 741, 750, 759, 768, 777, 787, 796, 806, 816,
          825, 835, 845, 856, 866, 876, 887, 898, 909, 920, 931, 942, 953, 965, 976, 988))
))


def series(series_key):
    """The base values for the given E-series.

    Args:
        series_key: An E-Series key such as E24.

    Returns:
        A tuple of base value for the series. For example, for
        E3 the tuple (10, 22, 47) will be returned.

    Raises:
        ValueError: If not such series exists.
    """
    try:
        return _E[series_key]
    except KeyError:
        raise ValueError("E-series {} not found. Available E-series keys are {}"
                         .format(series_key,
                                 ', '.join(str(key.name) for key in series_keys())))


def series_keys():
    """The available series keys.

    Note:
        The series keys returned will be members of the ESeries enumeration.
        These are useful for programmatic use. For constant values consider
        using the module aliases E3, E6, E12, etc.

    Returns:
        A set-like object containing the series-keys.
    """
    return _E.keys()


def series_key_from_name(name):
    """Get an ESeries from its name.

    Args:
        name: The series name as a string, for example 'E24'

    Returns:
        An ESeries object which can be uses as a series_key.

    Raises:
        ValueError: If not such series exists.
    """
    try:
        return ESeries[name]
    except KeyError:
        raise ValueError("E-series with name {!r} not found. Available E-series keys are {}"
                         .format(name,
                                 ', '.join(str(key.name) for key in series_keys())))

_TOLERANCE = {
    E3: 0.4,
    E6: 0.2,
    E12: 0.1,
    E24: 0.05,
    E48: 0.02,
    E96: 0.01,
    E192: 0.005
}


def tolerance(series_key):
    """The nominal tolerance of an E Series.

    Args:
        series_key: An E-Series key such as E24.

    Returns:
        A float between zero and one. For example 0.1 indicates a 10% tolerance.

    Raises:
        ValueError: For an unknown E-Series.
    """
    try:
        return _TOLERANCE[series_key]
    except KeyError:
        raise ValueError("E-series {} not found. Available E-series keys are {}"
                         .format(series_key,
                                 ', '.join(str(key.name) for key in series_keys())))



LOG10_MANTISSA_E = {num: list(map(lambda x: log10(x) % 1, series)) for num, series in _E.items()}

GEOMETRIC_SCALE_E = {num: max(b/a for a, b in zip(series, series[1:])) for num, series in _E.items()}


def find_greater_than_or_equal(series_key, value):
    """Find the smallest value greater-than or equal-to the given value.

    Args:
        series_key: An E-Series key such as E24.
        value: The query value.

    Returns:
        The smallest value from the specified series which is greater-than
        or equal-to the query value.

    Raises:
        ValueError: If series_key is not known.
        ValueError: If value is not finite.
        ValueError: If value is out of range.
    """
    candidates = find_nearest_few(series_key, value, num=3)
    for candidate in candidates:
        if candidate >= value:
            return candidate


def find_greater_than(series_key, value):
    """Find the smallest value greater-than or equal-to the given value.

    Args:
        series_key: An E-Series key such as E24.
        value: The query value.

    Returns:
        The smallest value from the specified series which is greater-than
        the query value.

    Raises:
        ValueError: If series_key is not known.
        ValueError: If value is not finite.
        ValueError: If value is out of range.
    """
    candidates = find_nearest_few(series_key, value, num=3)
    for candidate in candidates:
        if candidate > value:
            return candidate


def find_less_than_or_equal(series_key, value):
    """Find the largest value less-than or equal-to the given value.

    Args:
        series_key: An E-Series key such as E24.
        value: The query value.

    Returns:
        The largest value from the specified series which is less-than
        or equal-to the query value.

    Raises:
        ValueError: If series_key is not known.
        ValueError: If value is not finite.
        ValueError: If value is out of range.
    """
    candidates = find_nearest_few(series_key, value, num=3)
    for candidate in reversed(candidates):
        if candidate <= value:
            return candidate


def find_less_than(series_key, value):
    """Find the largest value less-than or equal-to the given value.

    Args:
        series_key: An E-Series key such as E24.
        value: The query value.

    Returns:
        The largest value from the specified series which is less-than
        the query value.

    Raises:
        ValueError: If series_key is not known.
        ValueError: If value is not finite.
        ValueError: If value is out of range.
    """
    candidates = find_nearest_few(series_key, value, num=3)
    for candidate in reversed(candidates):
        if candidate < value:
            return candidate


def find_nearest(series_key, value):
    """Find the nearest value.

    Args:
        series_key: The ESeries to use.
        value: The value for which the nearest value is to be found.

    Returns:
        The value in the specified E-series closest to value.

    Raises:
        ValueError: If series_key is not known.
        ValueError: If value is not finite.
        ValueError: If value is out of range.
    """
    return find_nearest_few(series_key, value, num=1)[0]


def find_nearest_few(series_key, value, num=3):
    """Find the nearest values.

    Args:
        series_key: The ESeries to use.
        value: The value for which the nearest values are to be found.
        num: The number of nearby values to find: 1, 2 or 3.

    Returns:
        A tuple containing num values. With num == 3 it is guaranteed
        that  at least one item less than value, and one item greater
        than value.

    Raises:
        ValueError: If series_key is not known.
        ValueError: If num is not 1, 2 or 3.
        ValueError: If value is not finite.
        ValueError: If value is out of range.
    """
    if num not in {1, 2, 3}:
        raise ValueError("num {} is not 1, 2 or 3".format(num))
    start = value / pow(GEOMETRIC_SCALE_E[series_key], 1.5)
    stop = value * pow(GEOMETRIC_SCALE_E[series_key], 1.5)
    candidates = tuple(erange(series_key, start, stop))
    nearest = _nearest_n(candidates, value, num)
    return nearest


def erange(series_key, start, stop):
    """Generate  E values in a range inclusive of the start and stop values.

    Args:
        series_key: The ESeries to use.
        start: The beginning of the range. The yielded values may include this value.
        stop: The end of the range. The yielded values may include this value.

    Yields:
        Values from the specified range which lie between the start and stop
        values inclusively, and in order from lowest to highest.

    Raises:
        ValueError: If series_key is not known.
        ValueError: If start is not less-than or equal-to stop.
        ValueError: If start or stop are not both finite.
        ValueError: If start or stop are out of range.
    """
    if math.isinf(start):
        raise ValueError("Start value {} is not finite".format(start))
    if math.isinf(stop):
        raise ValueError("Stop value {} is not finite".format(stop))
    if start < _MINIMUM_E_VALUE:
        raise ValueError("{} is too small. The start value must greater than or equal to {}".format(stop, _MINIMUM_E_VALUE))
    if stop < _MINIMUM_E_VALUE:
        raise ValueError("{} is too small. The stop value must greater than or equal to {}".format(stop, _MINIMUM_E_VALUE))
    if not start <= stop:
        raise ValueError("Start value {} must be less than stop value {}".format(start, stop))

    return _erange(series_key, start, stop)


def _erange(series_key, start, stop):
    series_values = series(series_key)
    series_log = LOG10_MANTISSA_E[series_key]
    epsilon = (series_log[-1] - series_log[-2]) / 2
    start_log = log10(start) - epsilon
    start_decade, start_mantissa = _decade_mantissa(start_log)
    start_index = bisect_left(series_log, start_mantissa)
    if start_index == len(series_log):
        # Wrap to next decade
        start_decade += 1
        start_index = 0
    stop_log = log10(stop) + epsilon
    stop_decade, stop_mantissa = _decade_mantissa(stop_log)
    stop_index = bisect_right(series_log, stop_mantissa)
    assert stop_index != 0
    series_decade = int(log10(series_values[0]))
    for decade in range(start_decade, stop_decade + 1):
        index_begin = start_index if decade == start_decade else 0
        index_end = stop_index if decade == stop_decade else len(series_log)
        for index in range(index_begin, index_end):
            found = series_values[index]
            scale_exponent = decade - series_decade
            result = found * math.pow(10, scale_exponent)
            rounded_result = _round_sig(result, figures=series_decade + 1)
            if start <= rounded_result <= stop:
                yield rounded_result


def open_erange(series_key, start, stop):
    """Generate E values in a half-open range inclusive of start, but exclusive of stop.

    Args:
        series_key: The ESeries to use.
        start: The beginning of the range. The yielded values may include this value.
        stop: The end of the range. The yielded values will not include this value.

    Yields:
        Values from the specified range which lie in the half-open range defined by
        the start and stop values, from lowest to highest.

    Raises:
        ValueError: If series_key is not known.
        ValueError: If start is not less-than or equal-to stop.
        ValueError: If start or stop are not both finite.
        ValueError: If start or stop are out of range.
    """
    if math.isinf(start):
        raise ValueError("Start value {} is not finite".format(start))
    if math.isinf(stop):
        raise ValueError("Stop value {} is not finite".format(stop))
    if start < _MINIMUM_E_VALUE:
        raise ValueError("{} is too small. The start value must greater than or equal to {}".format(stop, _MINIMUM_E_VALUE))
    if stop < _MINIMUM_E_VALUE:
        raise ValueError("{} is too small. The stop value must greater than or equal to {}".format(stop, _MINIMUM_E_VALUE))
    if not start <= stop:
        raise ValueError("Start value {} must be less than stop value {}".format(start, stop))
    return (item for item in erange(series_key, start, stop) if item != stop)


def lower_tolerance_limit(series_key, value):
    """The lower limit for a nominal value of a series.

    Args:
        series_key: The ESeries to use.
        value: A nominal value. This value need not be an member of
            the specified E-series.

    Returns:
        The lower tolerance limit for the nominal value based on the
        E-series tolerance.

    Raises:
        ValueError: If series_key is not known.
    """
    return value - value * tolerance(series_key)


def upper_tolerance_limit(series_key, value):
    """The upper limit for a nominal value of a series.

    Args:
        series_key: The ESeries to use.
        value: A nominal value. This value need not be an member of
            the specified E-series.

    Returns:
        The upper tolerance limit for the nominal value based on the
        E-series tolerance.

    Raises:
        ValueError: If series_key is not known.
    """
    return value + value * tolerance(series_key)


def tolerance_limits(series_key, value):
    """The lower and upper tolerance limits for a nominal value of a series.

    Args:
        series_key: The ESeries to use.
        value: A nominal value. This value need not be an member of
            the specified E-series.

    Returns:
        A 2-tuple containing the lower and upper tolerance limits for the
        nominal value based on the E-series tolerance.

    Raises:
        ValueError: If series_key is not known.
    """
    return (lower_tolerance_limit(series_key, value),
            upper_tolerance_limit(series_key, value))


def _nearest_n(candidates, value, n):
    abs_deltas = tuple(abs(c - value) for c in candidates)
    indexes = [index for index, _ in sorted(enumerate(abs_deltas), key=lambda x: x[1])]
    nearest_three = tuple(sorted(candidates[i] for i in indexes[:n]))
    return nearest_three


def _round_sig(x, figures=6):
    return 0 if x == 0 else round(x, int(figures - floor(log10(abs(x))) - 1))


def _decade_mantissa(value):
    f_decade, mantissa = divmod(value, 1)
    return int(f_decade), mantissa



