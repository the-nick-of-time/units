# Units

When doing calculations using physical measurements, it's all too easy to forget to account for
units. This can result in problems when you find you've been adding kilograms to newtons and
your calculation is off by a factor of ten.

This library uses the standard library `decimal.Decimal` for all calculations to avoid most
floating-point calculation pitfalls. Values given are automatically converted so you can enter
any value that constructor can take. Functionally, this means that float notation should be
given as strings rather than float literals.

Q. How many meters does light travel in a millisecond?

```python
from units.time import seconds
from units.constants import c

print(c * seconds("1e-3"))
```

Q. What is that in feet?

```python
from units.time import seconds
from units.constants import c

print((c * seconds("1e-3")).to_feet())
```

Q. How fast is someone on the equator moving around the center of the earth?

```python
from units.time import days
from units.constants import earth_radius
from math import pi

circumference = 2 * pi * earth_radius
speed = (circumference / days(1)).to_meters_per_second()
```

Q. What's the mass of air in one of your car tires, if the inner radius is 6 inches, the outer
radius is 12.5 inches, the thickness is 8 inches, and it's filled to 42 psi?

```python
from units.length import inches
from units.pressure import psi
from units.constants import R, air_molar_mass
from units.temperature import celsius, celsius_to_kelvin_absolute
from units.volume import cubic_meter
from math import pi

volume = (pi * inches(8) * (inches("12.5") ** 2 - inches(6) ** 2)).to_meters_cubed()
pressure = psi(42).to_pascals()
temperature = celsius_to_kelvin_absolute(celsius(25))
mols = pressure * volume / (R * temperature)
mass = mols * air_molar_mass
print(mass.to_avoirdupois_pounds_mass())
```

All constants like `R` are defined in SI base units so you will need to convert your units, but
as you can see, that task is easy.

