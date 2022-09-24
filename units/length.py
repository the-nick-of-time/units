from decimal import Decimal

from units.base import make_unit, make_dimension

__all__ = [
    "Length",
    "meters",
    "kilometers",
    "feet",
    "miles",
    "yards",
    "inches",
    "astronomical_unit",
]

Length = make_dimension("Length")

meters = make_unit("meters", Length, 1)

kilometers = make_unit("kilometers", Length, 1000)
feet = make_unit("feet", Length, Decimal("0.3048"))
miles = make_unit("miles", Length, "1609.344")
yards = make_unit("yards", Length, "0.9144")
inches = make_unit("inches", Length, "0.0254")
astronomical_unit = au = make_unit("au", Length, 149_597_870_700)
