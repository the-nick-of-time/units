from pyunitx._api import make_dimension, make_unit, si_unit

Mass = make_dimension("Mass")

kilograms = make_unit(
    name="kilograms",
    dimension=Mass,
    scale=1,
    abbrev="kg",
    doc="""\
    Kilograms are the SI base unit of mass, despite having a magnitude prefix.
    """
)
grams = make_unit(
    name="grams",
    dimension=Mass,
    scale="0.001",
    abbrev="g",
    doc="""A gram is roughly defined as the mass of a milliliter of water."""
)

generated = si_unit(base_unit=grams, skip=["kilo"])
globals().update(generated)

atomic_mass_unit = make_unit(
    name="atomic_mass_unit",
    abbrev="u",
    dimension=Mass,
    scale="1.660538782e-27",
    doc="""
    The unified atomic mass unit is defined as 1/12 of the mass of one atom of
    carbon-12, approximately the mass of one proton or neutron. As such, it is 
    equal to :math:`\\frac{1 g}{N_A}`.
    """
)

av_pound = make_unit(
    name="pounds_mass",
    dimension=Mass,
    scale="0.45359237",
    abbrev="lbm",
    doc="""Avoirdupois pounds are one of the definitions of mass in the |ucs|."""
)
troy_pound = make_unit(
    name="troy_pounds_mass",
    dimension=Mass,
    scale="0.3732417",
    abbrev="lbm_T",
    doc="""Troy pounds are a little smaller."""
)
slug = make_unit(
    name="slug",
    dimension=Mass,
    scale="14.59390",
    abbrev="slug",
    doc="""\
    A slug is the amount of mass that would be accelerated at 1 
    foot/second/second by a force of one pound. Using slugs you can form a 
    consistent set of measurements whereas the pound-mass cannot.
    """
)

__all__ = [
              "Mass",
              "kilograms",
              "av_pound",
              "troy_pound",
              "slug",
              "grams"
          ] + list(generated.keys())
