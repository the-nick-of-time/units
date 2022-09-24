from decimal import Decimal

from units.base import make_unit, make_dimension

Length = make_dimension("Length")

meters = make_unit("meters", Length, 1)

kilometers = make_unit("kilometers", Length, 1000)
feet = make_unit("feet", Length, Decimal("0.3048"))
miles = make_unit("miles", Length, "1609.344")
