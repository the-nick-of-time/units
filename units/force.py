from units import make_compound_dimension, make_compound_unit
from units.length import Length, meters, feet
from units.mass import Mass, kilograms, slug
from units.time import Time, seconds

__all__ = ["Force", "newtons", "pounds", "kgf", "kilograms_force"]

Force = make_compound_dimension(((Mass, 1), (Length, 1), (Time, -2)))

newtons = make_compound_unit(scale=1, exponents={kilograms: 1, meters: 1, seconds: -2},
                             name="newtons")
kgf = kilograms_force = make_compound_unit(scale="9.80665", exponents={kilograms: 1,
                                                                       meters: 1,
                                                                       seconds: -2})
pounds = make_compound_unit(scale="4.4482216152605", exponents={slug: 1, feet: 1, seconds: -2},
                            name="pounds")
