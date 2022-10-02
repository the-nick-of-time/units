Base Dimensions and Units
=========================
.. include:: macros.rst

.. csv-table:: SI prefixes
	:file: prefixes.csv
	:widths: 40, 20, 40
	:header-rows: 1

Each of the SI base units also have versions with these prefixes applied.
Here, those are
:class:`meters <pyunitx.length.meters>` for length,
:class:`seconds <pyunitx.time.seconds>` for time,
:class:`grams <pyunitx.mass.grams>` for mass (:class:`kilograms <pyunitx.mass.kilograms>` are the consistent base unit but the prefixes are applied to grams),
:class:`kelvin <pyunitx.temperature.kelvin>` for temperature,
:class:`moles <pyunitx.mole.moles>` for quantity, and
:class:`amperes <pyunitx.current.amperes>` for current.

Length
------

The full suite of functions on a unit is shown for :class:`meters <pyunitx.length.meters>` here as an example.
All units have exactly the same interface so the copies are omitted for brevity.

.. _unit-example:
.. autoclass:: pyunitx.length.meters
	:members:
	:special-members: __new__, __add__, __sub__, __abs__, __pos__, __neg__, __mul__, __truediv__, __pow__, __getattr__, __eq__, __lt__, __le__

.. automodule:: pyunitx.length
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to, to_latex, to_natural_si, meters

Time
----

.. automodule:: pyunitx.time
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to, to_latex, to_natural_si

Mass
----

.. automodule:: pyunitx.mass
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to, to_latex, to_natural_si

Temperature
-----------

.. automodule:: pyunitx.temperature
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to, to_latex, to_natural_si


Angle
-----

.. automodule:: pyunitx.angle
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to, to_latex, to_natural_si


Moles
-----

.. automodule:: pyunitx.mole
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to, to_latex, to_natural_si


Current
-------

.. automodule:: pyunitx.current
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to, to_latex, to_natural_si


Data
----

.. automodule:: pyunitx.data
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to, to_latex, to_natural_si