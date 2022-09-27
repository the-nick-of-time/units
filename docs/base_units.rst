Base Dimensions and Units
=========================
.. include:: macros.rst


Length
------

The full suite of functions on a unit is shown for :class:`units.length.meters` here as an example.
All units have exactly the same interface so the copies are omitted for brevity.

.. _unit-example:
.. autoclass:: pyunitx.length.meters
	:members:
	:special-members: __new__, __add__, __sub__, __eq__, __mul__, __truediv__, __getattr__, __pow__

.. automodule:: pyunitx.length
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to, meters

Time
----

.. automodule:: pyunitx.time
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to

Mass
----

.. automodule:: pyunitx.mass
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to

Temperature
-----------

.. automodule:: pyunitx.temperature
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to


Angle
-----

.. automodule:: pyunitx.angle
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to


Moles
-----

.. automodule:: pyunitx.mole
	:members:
	:exclude-members: sig_figs, is_dimension, equivalent_to
