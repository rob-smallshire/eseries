from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from builtins import int
from future import standard_library
standard_library.install_aliases()
from math import floor, log10

from eseries.eseries import _round_sig

PREFIXES = 'yzafpnum kMGTPEZY'


def eng_string(x, sig_figs=3, prefix=True):
    """
    Returns float/int value <x> formatted in a simplified engineering format -
    using an exponent that is a multiple of 3.

    Args:
        sig_figs: number of significant figures

    prefix: Use SI suffix for exponent, e.g. k instead of e3, n instead of
    e-9 etc.
    """
    x = float(x)
    sign = ''
    if x < 0:
        x = -x
        sign = '-'

    if x == 0:
        exp3 = 0
        x3 = 0
    else:
        exp = int(floor(log10(x)))
        exp3 = exp - (exp % 3)
        x3 = x / (10 ** exp3)
        x3 = _round_sig(x3, 3)  # None of the E-series values have more than 3 s.f.
        if x3 == int(x3):  # prevent from displaying .0
            x3 = int(x3)

    if prefix and (-24 <= exp3 <= 24) and (exp3 != 0):
        exp3_text = ' ' + PREFIXES[exp3 // 3 + 8]
    elif exp3 == 0:
        exp3_text = ''
    else:
        exp3_text = 'e' + str(exp3)

    t3 = str(x3)

    return ''.join((sign, t3, exp3_text))