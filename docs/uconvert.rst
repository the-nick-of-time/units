Unit Converter
==============

This module comes with a command-line unit conversion tool.
If you installed the package with pip, it will be put on your path as ``uconvert``.

It is invoked as ``uconvert NUMBER FROM-UNIT TO-UNIT``.
The units are expressed using the symbols (abbreviations), combined using . for multiplication and / for division.
/ for division is used before each denominator unit,
like J/kg/K for specific heat capacity. J/kg.K would instead be equivalent to J.K/kg.
If you don't like this ambiguity, the better way is to use a negative exponent on the unit.
As an example, you would give meters per second as 'm.s^-1'.
