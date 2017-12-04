eseries
=======

The E-series is a system of preferred numbers used with electronic
components such as resistors and capacitors. For example, the E6
series contains six values (10, 15, 22, 33, 47, 68) which cover a
one-order of magnitude range of values (one decade) from 10 to 99.
These base values repeat again to cover the next decade from 100
to 999, as 100, 220, 330, 470, and 680.

This ``eseries`` library is useful for selecting values from the
standard E3, E6, E12, E24, E48, E96 and E192 decades.

For example, to find the nearest E24 value to 319 use::

  >>> from eseries import find_nearest, E24
  >>> find_nearest(E24, 319)
  330

To find the next value greater-than or equal-to 184 in the E96 series
use:

  >>> from eseries import find_greater_than_or_equal, E96
  >>> find_greater_than_or_equal(E96, 184)
  187

To find a few values around the specified value, use:

  >>> from eseries import find_nearest_few, E24
  >>> find_nearest_few(E24, 5000)
  (4700, 5100, 5600)

