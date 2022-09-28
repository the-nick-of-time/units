# Units

[![Coverage Status](https://coveralls.io/repos/github/the-nick-of-time/units/badge.svg?branch=main)](https://coveralls.io/github/the-nick-of-time/units?branch=main)
[![Documentation Status](https://readthedocs.org/projects/pyunitx/badge/?version=latest)](https://pyunitx.readthedocs.io/en/latest/?badge=latest)

When doing calculations using physical measurements, it's all too easy to forget to account for
units. This can result in problems when you find you've been adding kilograms to newtons and
your calculation is off by a factor of ten.

This library uses the standard library `decimal.Decimal` for all calculations to avoid most
floating-point calculation pitfalls. Values given are automatically converted so you can enter
any value that constructor can take. Functionally, this means that float notation should be
given as strings rather than float literals.

Q. How many meters does light travel in a millisecond?

```pycon
>>> from pyunitx.time import seconds
>>> from pyunitx.constants import c
>>> 
>>> (c * seconds("1e-3")).sig_figs(5)
2.9979E+5 m

```

Q. What is that in feet?

```pycon
>>> from pyunitx.time import seconds
>>> from pyunitx.constants import c
>>> 
>>> (c * seconds("1e-3")).to_feet().sig_figs(5)
9.8357E+5 ft

```

Q. How fast is someone on the equator moving around the center of the earth?

```pycon
>>> from pyunitx.time import days
>>> from pyunitx.constants import earth_radius
>>> from math import pi
>>> 
>>> circumference = 2 * pi * earth_radius
>>> (circumference / days(1)).to_meters_per_second().sig_figs(3)
464 m s^-1

```

Q. What's the mass of air in one of your car tires, if the inner radius is 6 inches, the outer
radius is 12.5 inches, the width is 8 inches, and it's filled to 42 psi?[^1]

[^1]: No, I don't write homework problems.

```pycon
>>> from pyunitx.length import inches
>>> from pyunitx.pressure import psi
>>> from pyunitx.constants import R, air_molar_mass
>>> from pyunitx.temperature import celsius, celsius_to_kelvin_absolute
>>> from math import pi
>>> 
>>> volume = (pi * inches(8) * (inches("12.5") ** 2 - inches(6) ** 2)).to_meters_cubed()
>>> pressure = psi(42).to_pascals()
>>> temperature = celsius_to_kelvin_absolute(celsius(25))
>>> mols = pressure * volume / (R * temperature)
>>> mass = mols * air_molar_mass
>>> mass.to_avoirdupois_pounds_mass().sig_figs(3)
0.369 lbm_A

```

All constants like `R` are defined in SI base units so you will need to convert your units, but
as you can see, that task is easy. It's just a matter of calling `.to_<other unit>()`. You can
convert from any unit to another that measures the same dimension this way. If you're going to a
composite unit that hasn't been explicitly declared with a name, this is still possible, and the
library will create a converter for you - you just need to get the name right. The name format
is as intuitive as possible, as you can see with the above examples.

A name is made of the names of the base units, suffixed with `_squared`, `_cubed`, etc. to
relate the size of the exponent and prefixed by `per_` if the exponent is negative. Units with
negative exponents are made singular[^2] to follow how you would say it.

[^2]: Naively; it's done by just stripping off a trailing 's' if there is one.

Some examples of the most complicated possible situations will be illustrative.

```pycon
>>> from pyunitx.constants import gas_constant, stefan_boltzmann
>>> print(gas_constant.to_feet_pounds_per_mole_per_rankine().sig_figs(4))
3.407 ft^2 slug mol^-1 °R^-1 s^-2

>>> print(stefan_boltzmann.to_horsepower_per_feet_squared_per_rankine_to_the_fourth().sig_figs(5))
3.7013E-10 slug s^-3 °R^-4

```

You will notice that the output will have all units broken down to their bases. It is guaranteed
to be equivalent.

