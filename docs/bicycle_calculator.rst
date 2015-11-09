bicycle_calculator package
****************************

bicycle_calculator.bicycle module
==================================

Conventions
------------
- All lengths are measured in millimeters unless noted otherwise.
- Front cogs and rear cogs are each encoded as a list of integers
  representing the number of teeth on the cogs, 
  e.g. ``front_cogs = [28, 42]``.
- Wheel diameter is the diameter of the wheel with the tire on and inflated.
- Center to flange measurements are encoded by a dictionary with 
  center-to-left-flange and center-to-right-flange measurements listed
  under ``'left'`` and ``'right'`` keys, respectively.
  Similarly with flange diameter measurements.
  For example ``center_to_flange = {'left': 37.1, 'right': 20.9}`` and
  ``flange_diameter = {'left': 45, 'right': 45}``


.. automodule:: bicycle_calculator.bicycle
    :members:
    :undoc-members:
    :show-inheritance:

