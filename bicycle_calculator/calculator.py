"""
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

Todo
----
- Update docstring examples
"""

import functools
from math import *
from fractions import gcd
from itertools import product


class Bicycle(object):
    """
    Represents a bicycle.
    """
    def __init__(self, name=None, head_tube_angle=None, 
      fork_rake=None, crank_length=None,
      front_cogs=None, rear_cogs=None,
      front_wheel=None, rear_wheel=None):
        self.name = name
        self.head_tube_angle = head_tube_angle
        self.fork_rake = fork_rake
        self.crank_length = crank_length
        if front_cogs is None:
            front_cogs = []
        if rear_cogs is None:
            rear_cogs = []
        self.front_cogs = sorted(front_cogs)
        self.rear_cogs = sorted(rear_cogs)
        if front_wheel is None:
            front_wheel = Wheel()
        if rear_wheel is None:
            rear_wheel = Wheel()
        self.front_wheel = front_wheel
        self.rear_wheel = rear_wheel

    def __repr__(self):
        s = self.name + '\n'
        s += '='*len(self.name) + '\n'
        for (k, v) in sorted(self.__dict__.items()):
            s += '{!s} = {!s}\n'.format(k, v)
        return s

    # def derailer_capacity(self):
    #     """
    #     Call the corresponding module function using this 
    #     bicycle's attributes as inputs.
    #     """
    #     return derailer_capacity(
    #       front_cogs=self.front_cogs,
    #       rear_cogs=self.rear_cogs,
    #       )

    # def gear_ratios(self, digits=None):
    #     """
    #     Call the corresponding module function using this 
    #     bicycle's attributes as inputs.
    #     """
    #     return gear_ratios(
    #       front_cogs=self.front_cogs,
    #       rear_cogs=self.rear_cogs, 
    #       digits=digits,
    #       )

    # def gain_ratios(self, digits=None):
    #     """
    #     Call the corresponding module function using this 
    #     bicycle's attributes as inputs.
    #     """
    #     return gain_ratios(
    #       front_cogs=self.front_cogs,
    #       rear_cogs=self.rear_cogs, 
    #       crank_length=self.crank_length, 
    #       wheel_diameter=self.rear_wheel.diameter, 
    #       digits=digits,
    #       )

    # def cadence_to_speeds(self, cadence, digits=None):
    #     """
    #     Call the corresponding module function using this 
    #     bicycle's attributes as inputs.
    #     """
    #     return cadence_to_speeds(
    #       cadence, 
    #       front_cogs=self.front_cogs,
    #       rear_cogs=self.rear_cogs, 
    #       crank_length=self.crank_length, 
    #       wheel_diameter=self.rear_wheel.diameter, 
    #       digits=digits,
    #       )

    # def speed_to_cadences(self, speed, digits=None):
    #     """
    #     Call the corresponding module function using this 
    #     bicycle's attributes as inputs.
    #     """
    #     return speed_to_cadences(
    #       speed, 
    #       front_cogs=self.front_cogs,
    #       rear_cogs=self.rear_cogs, 
    #       crank_length=self.crank_length, 
    #       wheel_diameter=self.rear_wheel.diameter, 
    #       digits=digits,
    #       )
        
    # def num_skid_patches(self, ambidextrous=False):
    #     """
    #     Call the corresponding module function using this 
    #     bicycle's attributes as inputs.
    #     """
    #     return num_skid_patches(
    #       front_cogs=self.front_cogs, 
    #       rear_cogs=self.rear_cogs,
    #       ambidextrous=ambidextrous,
    #       )

    # def trail(self, digits=None): 
    #     """
    #     Call the corresponding module function using this 
    #     bicycle's attributes as inputs.
    #     """
    #     return trail(
    #       head_tube_angle=self.head_tube_angle, 
    #       fork_rake=self.fork_rake,
    #       wheel_diameter=self.front_wheel.diameter,
    #       )


class Wheel(object):
    """
    Represents a bicycle wheel.
    """
    def __init__(self, name=None, bsd=None, erd=None, 
      tire_width=None, diameter=None,
      center_to_flange=None, flange_diameter=None,
      spoke_hole_diameter=2.6, num_spokes=None, num_crosses=None, 
      offset=0):
        self.name = name
        self.erd = erd
        self.bsd = bsd
        self.tire_width = tire_width
        self.diameter = diameter
        if center_to_flange is None:
            center_to_flange = {'left': None, 'right':None}
        self.center_to_flange = center_to_flange  
        if flange_diameter is None:
            flange_diameter = {'left': None, 'right':None}
        self.flange_diameter = flange_diameter  
        self.spoke_hole_diameter = spoke_hole_diameter
        self.num_spokes = num_spokes
        self.num_crosses = num_crosses
        self.offset = offset

    def __repr__(self):
        s = self.name + '\n'
        s += '-'*len(self.name) + '\n'
        for (k, v) in sorted(self.__dict__.items()):
            s += '{!s} = {!s}\n'.format(k, v)
        return s

    # def spoke_length(self, digits=None):
    #     """
    #     Call the corresponding module function using this 
    #     wheel's attributes as inputs.
    #     """
    #     return spoke_length(
    #       center_to_flange=self.center_to_flange, 
    #       flange_diameter=self.flange_diameter, 
    #       spoke_hole_diameter=self.spoke_hole_diameter, 
    #       erd=self.erd, 
    #       offset=self.offset, 
    #       num_spokes=self.num_spokes,
    #       num_crosses=self.num_crosses, 
    #       digits=digits
    #       )

    # def approx_diameter(self):
    #     """
    #     Call :func:`approx_wheel_diameter` using this 
    #     wheel's attributes as inputs.
    #     """
    #     return approx_wheel_diameter(
    #       bsd=self.bsd, 
    #       tire_width=self.tire_width
    #       )


def derailer_capacity(bicycle):
    """
    Return the derailer capacity needed to accommodate the given cog set.
    
    Uses the following bicycle attributes:

    - front_cogs
    - rear_cogs

    EXAMPLES::

        >>> derailer_capacity([26, 36], [12, 18, 32])
        30

    """
    return abs(front_cogs[-1] - front_cogs[0]) + \
      abs(rear_cogs[-1] - rear_cogs[0])

def gear_ratios(front_cogs, rear_cogs, digits=None):
    """
    Return the gear ratios for the given cogs.

    EXAMPLES::

        >>> gear_ratios([40], [20, 30])
        {(40, 30): 1.3333333333333333, (40, 20): 2.0}

    """
    result = {}
    for (f, r) in product(front_cogs, rear_cogs):
        result[(f, r)] = f/r

    if digits is not None:
        result = {k: round(v, digits) for k, v in result.items()}

    return result

def gain_ratios(front_cogs, rear_cogs, crank_length, wheel_diameter, 
  digits=None):
    """
    Return the gain ratios for the given parameters.

    EXAMPLES::

        >>> gain_ratios([40], [20, 30], 100, 600)
        {(40, 30): 4.0, (40, 20): 6.0}

    REFERENCES:

    - `Bicycle Gearing <http://en.wikipedia.org/wiki/Bicycle_gearing#Measuring_gear_ratios>`_ from Wikipedia
    """
    result = {}
    w = wheel_diameter/2/crank_length
    for (f, r) in product(front_cogs, rear_cogs):
        result[(f, r)] = w*f/r

    if digits is not None:
        result = {k: round(v, digits) for k, v in result.items()}

    return result

def cadence_to_speeds(cadence, front_cogs, rear_cogs, crank_length, 
   wheel_diameter, digits=None):
    """
    Return speeds in kilometers per hour. 
    Cadence is measured in hertz (revolutions/second).

    EXAMPLES::

        >>> cadence_to_speeds(2, [40], [20, 30], 100, 600, digits=1)
        {(40, 30): 18.1, (40, 20): 27.1}

    """
    gr = gain_ratios(front_cogs, rear_cogs, crank_length, wheel_diameter)
    result = {}
    for (k, g) in gr.items():
        result[k] = 2*pi*crank_length*g*cadence*(3600/1e6)

    if digits is not None:
        result = {k: round(v, digits) for k, v in result.items()}

    return result

def speed_to_cadences(speed, front_cogs, rear_cogs, crank_length, 
  wheel_diameter, digits=None):
    """
    Return cadences in hertz (revolutions per second). 
    Speed is measured in kilometers per hour.

    EXAMPLES::

        >>> speed_to_cadences(18.1, [40], [20, 30], 100, 600, digits=1)
        {(40, 30): 2.0, (40, 20): 1.3}

    """
    gr = gain_ratios(front_cogs, rear_cogs, crank_length, wheel_diameter)
    result = {}
    for (k, g) in gr.items():
        result[k] = speed/(2*pi*crank_length*g*(3600/1e6))

    if digits is not None:
        result = {k: round(v, digits) for k, v in result.items()}

    return result

def trail(head_tube_angle, fork_rake, wheel_diameter, digits=None): 
    """
    Return the tuple (trail, mechanical trail, wheel flop) 
    for a bicycle with the given parameters.
    
    EXAMPLES::

        >>> trail(73, 64, 700, digits=1)
        (40.1, 38.3, 11.2)

    REFERENCES:

    - `Bicycle and Motorcycle Geometry <http://en.wikipedia.org/wiki/Bicycle_and_motorcycle_geometry#Trail>`_ from Wikipedia
    """
    a = radians(head_tube_angle)
    wheel_radius = wheel_diameter/2
    trail = (wheel_radius*cos(a) - fork_rake)/sin(a)
    mechanical_trail = trail*sin(a)
    wheel_flop = trail*sin(a)*cos(a)
    result = [trail, mechanical_trail, wheel_flop]

    if digits is not None:
        result = tuple([round(v, digits) for v in result])

    return result

def num_skid_patches(front_cogs, rear_cogs, ambidextrous=False):
    """
    Return a dictionary of the form (front cog, rear cog) ->
    number of skid patches made on the rear tire of a fixed gear 
    bicycle with the given front cog and rear cog.

    EXAMPLES::

        >>> num_skid_patches([50], [25, 30], ambidextrous=False)
        {(50, 30): 3.0, (50, 25): 1.0}

        >>> num_skid_patches([50], [25, 30], ambidextrous=True)
        {(50, 30): 6.0, (50, 25): 1.0}

    SKID PATCH THEOREM:

    Let a/b be the ratio of the number of teeth on the front cog to the
    number of teeth on the rear cog written in lowest terms. 
    Then

    1. For single-sided skidding, there are b skid patches.
    2. Ambidexterous skidding (skidding with either the left or right foot forward) doubles the number of skid patches if and only if a is odd.

    REFERENCES:

    - `A Bike Forums post <http://www.bikeforums.net/singlespeed-fixed-gear/242123-skid-patch-theorem.html>`_ by user Fraction.
    """
    result = {}
    for (f, r) in product(front_cogs, rear_cogs):
        g = gcd(f, r)
        a = f/g
        b = r/g
        if ambidextrous and (a % 2) != 0:
            result[(f, r)] =  2*b
        else: 
            result[(f, r)] = b
    return result

def spoke_length(center_to_flange, flange_diameter, spoke_hole_diameter,
  erd, offset, num_spokes, num_crosses, digits=None):
    """
    Return the left (nondrive side) and right (drive side) spoke lengths
    for a bicycle wheel with the given parameters.

    EXAMPLES::

        >>> center_to_flange = {'left': 37.1, 'right': 20.9}
        >>> flange_diameter = {'left': 45, 'right': 45}
        >>> spoke_length(center_to_flange, flange_diameter, 2.6, 560, 3, 36, 3, digits=1)
        {'right': 269.2, 'left': 270.3}

    REFERENCES:

    - `Measurements for Spoke Length Calculations <http://www.sheldonbrown.com/spoke-length.html>`_ by John Allen
    """
    result = {}
    for k in center_to_flange:
        if k == 'right':
            o = offset
        else:
            o = -offset
        d = center_to_flange[k] + o
        r1 = flange_diameter[k]/2
        r2 = erd/2
        r3 = spoke_hole_diameter/2
        a = 2*pi*num_crosses/(num_spokes/2)
        result[k] = sqrt(d**2 + r1**2 + r2**2 - 2*r1*r2*cos(a)) - r3

    if digits is not None:
        result = {k: round(v, digits) for k, v in result.items()}

    return result

def approx_wheel_diameter(bsd, tire_width):
    """
    Return the approximate wheel diameter given the a bead seat diameter
    for a wheel and a tire width.
    Return the bead seat diameter plus twice the tire width.

    EXAMPLES::

        >>> approx_wheel_diameter(584, 42)
        668

    """
    return bsd + 2*tire_width


