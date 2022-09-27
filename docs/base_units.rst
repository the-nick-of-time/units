Base Dimensions and Units
=========================
.. include:: macros.rst


Length
------

The full suite of functions on a unit is shown for :class:`units.length.meters` here as an example.
All units have exactly the same interface so the copies are omitted for brevity.

.. _unit-example:
.. autoclass:: units.length.meters
	:members:
	:special-members: __new__, __add__, __sub__, __eq__, __mul__, __truediv__, __getattr__, __pow__

.. automodule:: units.length
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to, meters

Time
----

.. automodule:: units.time
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to

Mass
----

.. automodule:: units.mass
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to

Temperature
-----------

.. automodule:: units.temperature
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to


Angle
-----

.. automodule:: units.angle
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to


Moles
-----

.. automodule:: units.mole
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to
