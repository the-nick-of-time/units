from decimal import Decimal

from units._api import make_dimension, make_unit

__all__ = [
    "Length",
    "meters",
    "kilometers",
    "feet",
    "miles",
    "yards",
    "inches",
    "astronomical_unit",
    "au",
]

Length = make_dimension("Length")

meters = make_unit(name="meters", dimension=Length, scale=1)

kilometers = make_unit(name="kilometers", dimension=Length, scale=1000)
feet = make_unit(name="feet", dimension=Length, scale=Decimal("0.3048"))
miles = make_unit(name="miles", dimension=Length, scale="1609.344")
yards = make_unit(name="yards", dimension=Length, scale="0.9144")
inches = make_unit(name="inches", dimension=Length, scale="0.0254")
astronomical_unit = au = make_unit(name="au", dimension=Length, scale=149_597_870_700)
