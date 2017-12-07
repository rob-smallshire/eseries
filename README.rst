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

Status
------

.. image:: https://travis-ci.org/rob-smallshire/eseries.svg?branch=master
    :target: https://travis-ci.org/rob-smallshire/eseries
    
.. image:: https://coveralls.io/repos/github/rob-smallshire/eseries/badge.svg?branch=master
    :target: https://coveralls.io/github/rob-smallshire/eseries?branch=master

Installation
------------

The ``eseries`` package is available on the Python Package Index (PyPI):

.. image:: https://badge.fury.io/py/eseries.svg
    :target: https://badge.fury.io/py/eseries

The package support Python 3 only. To install::

  $ pip install eseries

Python Interface
----------------

For full help::

  >>> import eseries
  >>> help(eseries)

In the meantime, here are some highlights.

To find the nearest E24 value to 319 use::

  >>> from eseries import find_nearest, E24
  >>> find_nearest(E24, 319)
  330

To find the next value greater-than or equal-to 184 in the E96 series
use::

  >>> from eseries import find_greater_than_or_equal, E96
  >>> find_greater_than_or_equal(E96, 184)
  187

To find a few values around the specified value, use::

  >>> from eseries import find_nearest_few, E24
  >>> find_nearest_few(E24, 5000)
  (4700, 5100, 5600)


Command-Line Interface
----------------------

There's also a handy command-line interface. Run ``eseries --help``
to see a list of commands::

  $ eseries --help
  eseries

  Usage: eseries [options] <command> [<args> ...]

  Options:
    -h --help     Show this screen.
    -v --verbose  Use verbose logging

 Available commands:
    ge
    gt
    help
    le
    lower-tolerance-limit
    lt
    nearby
    nearest
    range
    series
    tolerance
    tolerance-limits
    upper-tolerance-limit

  See 'eseries help <command>' for help on specific commands.

To find a nearby value, use::

  $ eseries nearest E24 37726
  39e3

If you prefer an SI exponent symbol, supply ``--symbol`` or ``-s``::

  $ eseries nearest E24 37726 -s
  39 k

To show values around the given value, use the ``nearby`` command::

  $ eseries nearby E48 52e6 -s
  48.7 M
  51.1 M
  53.6 M

To show the smallest value greater than or equal to the given value, use the ``ge`` command::

  $ eseries ge E48 52e3 -s
  53.6 k

 To show the upper and lower tolerance limits of a nominal value, use the ``tolerance-limits`` command::

  $ eseries tolerance-limits E48 35
  34.3
  35.7

 To show all values in an inclusive range, use the ``range`` command::

  $ eseries range E6 74e-9 34e-6 --symbol
  100 n
  150 n
  220 n
  330 n
  470 n
  680 n
  1 µ
  1.5 µ
  2.2 µ
  3.3 µ
  4.7 µ
  6.8 µ
  10 µ
  15 µ
  22 µ
  33 µ
