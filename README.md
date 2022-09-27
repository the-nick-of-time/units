# Units

When doing calculations using physical measurements, it's all too easy to forget to account for
units. This can result in problems when you find you've been adding kilograms to newtons and
your calculation is off by a factor of ten.

This library uses the standard library `decimal.Decimal` for all calculations to avoid most
floating-point calculation pitfalls. Values given are automatically converted so you can enter
any value that constructor can take. Functionally, this means that float notation should be
given as strings rather than float literals.

Q. How many meters does light travel in a millisecond?

```pycon
>>> from units.time import seconds
>>> from units.constants import c
>>> 
>>> (c * seconds("1e-3")).sig_figs(5)
2.9979E+5 m

```

Q. What is that in feet?

```pycon
>>> from units.time import seconds
>>> from units.constants import c
>>> 
>>> (c * seconds("1e-3")).to_feet().sig_figs(5)
9.8357E+5 ft

```

Q. How fast is someone on the equator moving around the center of the earth?

```pycon
>>> from units.time import days
>>> from units.constants import earth_radius
>>> from math import pi
>>> 
>>> circumference = 2 * pi * earth_radius
>>> (circumference / days(1)).to_meters_per_second().sig_figs(3)
464 m s^-1

```

Q. What's the mass of air in one of your car tires, if the inner radius is 6 inches, the outer
radius is 12.5 inches, the width is 8 inches, and it's filled to 42 psi?

```pycon
>>> from units.length import inches
>>> from units.pressure import psi
>>> from units.constants import R, air_molar_mass
>>> from units.temperature import celsius, celsius_to_kelvin_absolute
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
as you can see, that task is easy.

