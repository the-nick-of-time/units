Derived Dimensions and Units
============================
.. include:: macros.rst

.. csv-table:: SI prefixes
	:file: prefixes.csv
	:widths: 40, 20, 40
	:header-rows: 1

Each of the SI named derived units have versions with these prefixes applied.
Here, those are
:class:`coulombs <pyunitx.charge.coulombs>` for charge,
:class:`joules <pyunitx.energy.joules>` for energy,
:class:`newtons <pyunitx.force.newtons>` for force,
:class:`hertz <pyunitx.frequency.hertz>` for frequency,
:class:`watts <pyunitx.power.watts>` for power,
:class:`pascals <pyunitx.pressure.pascals>` for pressure,
:class:`ohms <pyunitx.pressure.ohms>` for resistance, and
:class:`volts <pyunitx.voltage.volts>` for voltage.

Volume is a curious case in that :class:`liters <pyunitx.volume.liters>` often has the milli- prefix applied :class:`milliliters <pyunitx.volume.milliliters>`
but almost no other SI prefix is used with them. In general calculations, cubic meters are preferred.
Nonetheless the full suite of prefixes is available for liters.


Area
----

.. automodule:: pyunitx.area
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to, to_latex, to_natural_si


Charge
------

.. automodule:: pyunitx.charge
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to, to_latex, to_natural_si


Energy
------

.. automodule:: pyunitx.energy
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to, to_latex, to_natural_si


Force
-----

.. automodule:: pyunitx.force
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to, to_latex, to_natural_si


Frequency
---------

.. automodule:: pyunitx.frequency
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to, to_latex, to_natural_si


Power
-----

.. automodule:: pyunitx.power
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to, to_latex, to_natural_si


Pressure
--------

.. automodule:: pyunitx.pressure
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to, to_latex, to_natural_si


Resistance
----------

.. csv-table:: Resistor Color Codes
	:file: colors.csv
	:header-rows: 1

.. automodule:: pyunitx.resistance
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to, to_latex, to_natural_si


Voltage
-------

.. automodule:: pyunitx.voltage
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to, to_latex, to_natural_si


Volume
------

.. automodule:: pyunitx.volume
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to, to_latex, to_natural_si


Non-consistent Derived Units
----------------------------

.. automodule:: pyunitx.derived
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to, to_latex, to_natural_si