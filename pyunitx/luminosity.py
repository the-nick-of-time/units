from pyunitx._api import make_dimension, make_unit, si_unit

LuminousIntensity = make_dimension("Luminous Intensity")

candela = make_unit(
    name="candela",
    abbrev="cd",
    scale=1,
    dimension=LuminousIntensity,
    doc="""\
    The candela is the SI base unit of luminous intensity, a quantity calculated
    to approximate the amount of light that is visible to humans for a given 
    source.
    """
)

generated = si_unit(base_unit=candela)
globals().update(generated)

__all__ = [
              "LuminousIntensity",
          ] + list(generated.keys())
