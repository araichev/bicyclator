"""
Conventions:

- All lengths are measured in millimeters, unless noted otherwise
- All angles are measured in degrees, unless noted otherwise
"""
from math import *
from fractions import gcd
from itertools import product
from copy import deepcopy


class Bicycle(object):
    """
    Represents a bicycle.

    Attributes:

    - name
    - front_cogs: list of integers representing the number of teeth on 
      the cogs, e.g. ``front_cogs = [28, 42]``
    - rear_cogs: list of integers representing the number of teeth on 
      the cogs, e.g. ``rear_cogs = [10, 15, 20, 25, 30]``
    - head_tube_angle
    - fork_rake
    - front_wheel: a Wheel instance
    - rear_wheel: a Wheel instance
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
        if self.name is not None:
            s = self.name + '\n'
            s += '='*len(self.name) + '\n'
        else:
            s = 'Nameless bicycle\n'
            s += '================\n'
        for k in ['front_cogs', 'rear_cogs', 'crank_length',
          'head_tube_angle', 'fork_rake', 
          'front_wheel', 'rear_wheel']:
            v = getattr(self, k)
            if 'wheel' in k:
                s += '\n{!s} = {!s}\n'.format(k, v)
            else:
                s += '{!s} = {!s}\n'.format(k, v)
        # Remove final new line
        return s[:-1]

    def copy(self):
        return deepcopy(self)


class Wheel(object):
    """
    Represents a bicycle wheel.

    Attributes:

    - name
    - bsd: bead seat diameter, e.g. 684 for a 650b rim
    - erd: effective rim diameter, e.g. 650 for a 650b rim 
    - tire_width
    - diameter: diameter of the wheel with the tire on and inflated
    - center_to_flange: dictionary of the form ``{'left': 37.1, 'right': 20.9}``
    - flange_diameter: dictionary of the form ``{'left': 45, 'right': 45}``
    - spoke_hole_diameter
    - num_spokes
    - num_crosses: number of crosses in spoke pattern, e.g. 3 
    - offset: for off-center rims
    """
    def __init__(self, name=None, bsd=None, erd=None, 
      tire_width=None, diameter=None,
      center_to_flange=None, flange_diameter=None,
      spoke_hole_diameter=2.6, num_spokes=None, num_crosses=3, 
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
        if self.name is not None:
            s = self.name + '\n'
            s += '-'*(len(self.name) + 10) + '\n'
        else:
            s = 'Nameless wheel\n'
            s += '----------------------------\n'
        for (k, v) in sorted(self.__dict__.items()):
            s += '{!s} = {!s}\n'.format(k, v)
        # Remove final new line
        return s[:-1]

    def copy(self):
        return deepcopy(self)


def check_attrs(obj, *attrs):
    for attr in attrs:
        v = getattr(obj, attr)
        if not v:
            raise ValueError("Attribute '{!s}' "\
              "must not be None or empty in object \n{!s}".format(attr, obj))

def derailer_capacity(bicycle):
    """
    Return the derailer capacity needed to accommodate the cog set
    on the given Bicycle object.
    
    Assume the following bicycle attributes are non-null and non-empty:

    - front_cogs
    - rear_cogs

    Raise a ``ValueError``, if that is not the case.
    
    EXAMPLES::

        >>> b = Bicycle(front_cogs=[26, 36], rear_cogs=[12, 18, 32])
        >>> derailer_capacity(b)
        30

    """
    b = bicycle
    attrs = ['front_cogs', 'rear_cogs']
    check_attrs(b, *attrs)

    return abs(b.front_cogs[-1] - b.front_cogs[0]) + \
      abs(b.rear_cogs[-1] - b.rear_cogs[0])

def num_skid_patches(bicycle, ambidextrous=False):
    """
    Return a dictionary of the form (front cog, rear cog) ->
    number of skid patches made on the rear tire of a fixed gear 
    bicycle with the given front cog and rear cog.

    Assume the following bicycle attributes are non-null and non-empty:

    - front_cogs
    - rear_cogs

    Raise a ``ValueError``, if that is not the case.

    EXAMPLES::

        >>> b = Bicycle(front_cogs=[50], rear_cogs=[25, 30])
        >>> num_skid_patches(b, ambidextrous=False)
        {(50, 30): 3.0, (50, 25): 1.0}
        >>> num_skid_patches(b, ambidextrous=True)
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
    b = bicycle
    attrs = ['front_cogs', 'rear_cogs']
    check_attrs(b, *attrs)

    result = {}
    for (f, r) in product(b.front_cogs, b.rear_cogs):
        g = gcd(f, r)
        a = f/g
        b = r/g
        if ambidextrous and (a % 2) != 0:
            result[(f, r)] =  2*b
        else: 
            result[(f, r)] = b
    return result

def gear_ratios(bicycle, digits=None):
    """
    Return the gear ratios for the given Bicycle object.

    Assume the following bicycle attributes are non-null and non-empty:

    - front_cogs
    - rear_cogs

    Raise a ``ValueError``, if that is not the case.

    EXAMPLES::

        >>> b = Bicycle(front_cogs=[40], rear_cogs=[20, 30])
        >>> gear_ratios(b)
        {(40, 30): 1.3333333333333333, (40, 20): 2.0}

    """
    b = bicycle
    attrs = ['front_cogs', 'rear_cogs']
    check_attrs(b, *attrs)

    result = {}
    for (f, r) in product(b.front_cogs, b.rear_cogs):
        result[(f, r)] = f/r

    if digits is not None:
        result = {k: round(v, digits) for k, v in result.items()}

    return result

def gain_ratios(bicycle, digits=None):
    """
    Return the gain ratios for the given Bicycle object.

    Assume the following bicycle attributes are non-null and non-empty:

    - front_cogs
    - rear_cogs
    - crank_length
    - rear_wheel

    Raise a ``ValueError``, if that is not the case.

    EXAMPLES::

        >>> w = Wheel(diameter=600)
        >>> b = Bicycle(front_cogs=[40], rear_cogs=[20, 30], crank_length=100, rear_wheel=w)
        >>> gain_ratios(b, digits=1)
        {(40, 30): 4.0, (40, 20): 6.0}

    REFERENCES:

    - `Bicycle Gearing <http://en.wikipedia.org/wiki/Bicycle_gearing#Measuring_gear_ratios>`_ from Wikipedia
    """
    b = bicycle
    attrs = ['front_cogs', 'rear_cogs', 'crank_length', 'rear_wheel']
    check_attrs(b, *attrs)
    check_attrs(b.rear_wheel, 'diameter')

    result = {}
    w = b.rear_wheel.diameter/2/b.crank_length
    for (f, r) in product(b.front_cogs, b.rear_cogs):
        result[(f, r)] = w*f/r

    if digits is not None:
        result = {k: round(v, digits) for k, v in result.items()}

    return result

def cadence_to_speeds(bicycle, cadence, digits=None):
    """
    Return speeds in kilometers per hour. 
    Cadence is measured in hertz (revolutions/second).

    Assume the following bicycle attributes are non-null and non-empty:

    - front_cogs
    - rear_cogs
    - crank_length
    - rear_wheel

    Raise a ``ValueError``, if that is not the case.

    EXAMPLES::

        >>> w = Wheel(diameter=600)
        >>> b = Bicycle(front_cogs=[40], rear_cogs=[20, 30], crank_length=100, rear_wheel=w)
        >>> cadence_to_speeds(b, 2, digits=1)
        {(40, 30): 18.1, (40, 20): 27.1}

    """
    b = bicycle
    attrs = ['front_cogs', 'rear_cogs', 'crank_length', 'rear_wheel']
    check_attrs(b, *attrs)
    check_attrs(b.rear_wheel, 'diameter')

    gr = gain_ratios(b)
    result = {}
    for (k, g) in gr.items():
        result[k] = 2*pi*b.crank_length*g*cadence*(3600/1e6)

    if digits is not None:
        result = {k: round(v, digits) for k, v in result.items()}

    return result

def speed_to_cadences(bicycle, speed, digits=None):
    """
    Return cadences in hertz (revolutions per second). 
    Speed is measured in kilometers per hour.

    Assume the following bicycle attributes are non-null and non-empty:

    - front_cogs
    - rear_cogs
    - crank_length
    - rear_wheel

    Raise a ``ValueError``, if that is not the case.

    EXAMPLES::

        >>> w = Wheel(diameter=600)
        >>> b = Bicycle(front_cogs=[40], rear_cogs=[20, 30], crank_length=100, rear_wheel=w)
        >>> speed_to_cadences(b, 18.1, digits=1)
        {(40, 30): 2.0, (40, 20): 1.3}

    """
    b = bicycle
    attrs = ['front_cogs', 'rear_cogs', 'crank_length', 'rear_wheel']
    check_attrs(b, *attrs)
    check_attrs(b.rear_wheel, 'diameter')

    gr = gain_ratios(b)
    result = {}
    for (k, g) in gr.items():
        result[k] = speed/(2*pi*b.crank_length*g*(3600/1e6))

    if digits is not None:
        result = {k: round(v, digits) for k, v in result.items()}

    return result

def trail(bicycle, digits=None): 
    """
    Return the tuple (trail, mechanical trail, wheel flop) 
    for a bicycle with the given parameters.
    
    Assume the following bicycle attributes are non-null and non-empty:

    - head_tube_angle
    - fork_rake
    - front_wheel

    Raise a ``ValueError``, if that is not the case.

    EXAMPLES::

        >>> w = Wheel(diameter=700)
        >>> b = Bicycle(head_tube_angle=73, fork_rake=64, front_wheel=w)
        >>> trail(b, digits=1)
        (40.1, 38.3, 11.2)

    REFERENCES:

    - `Bicycle and Motorcycle Geometry <http://en.wikipedia.org/wiki/Bicycle_and_motorcycle_geometry#Trail>`_ from Wikipedia
    """
    b = bicycle
    attrs = ['head_tube_angle', 'fork_rake', 'front_wheel']
    check_attrs(b, *attrs)
    check_attrs(b.front_wheel, 'diameter')

    a = radians(b.head_tube_angle)
    wheel_radius = b.front_wheel.diameter/2
    trail = (wheel_radius*cos(a) - b.fork_rake)/sin(a)
    mechanical_trail = trail*sin(a)
    wheel_flop = trail*sin(a)*cos(a)
    result = [trail, mechanical_trail, wheel_flop]

    if digits is not None:
        result = tuple([round(v, digits) for v in result])

    return result

def spoke_length(wheel, digits=None):
    """
    Return the left (nondrive side) and right (drive side) spoke lengths
    for the given wheel.

    Assume the following bicycle attributes are non-null and non-empty:

    - center_to_flange
    - flange_diameter
    - spoke_hole_diameter
    - erd
    - offset
    - num_spokes
    - num_crosses

    Raise a ``ValueError``, if that is not the case.

    EXAMPLES::

        >>> w = Wheel(center_to_flange={'left': 37.1, 'right': 20.9}, flange_diameter={'left': 45, 'right': 45}, erd=560, spoke_hole_diameter=2.6, offset=3, num_spokes=36, num_crosses=3)
        >>> spoke_length(w, digits=1)
        {'right': 269.2, 'left': 270.3}

    REFERENCES:

    - `Measurements for Spoke Length Calculations <http://www.sheldonbrown.com/spoke-length.html>`_ by John Allen
    """
    w = wheel
    attrs = ['center_to_flange', 'flange_diameter', 'spoke_hole_diameter',
      'erd', 'offset', 'num_spokes', 'num_crosses']
    check_attrs(w, *attrs)

    result = {}
    for k in w.center_to_flange:
        if k == 'right':
            o = w.offset
        else:
            o = -w.offset
        d = w.center_to_flange[k] + o
        r1 = w.flange_diameter[k]/2
        r2 = w.erd/2
        r3 = w.spoke_hole_diameter/2
        a = 2*pi*w.num_crosses/(w.num_spokes/2)
        result[k] = sqrt(d**2 + r1**2 + r2**2 - 2*r1*r2*cos(a)) - r3

    if digits is not None:
        result = {k: round(v, digits) for k, v in result.items()}

    return result

def approx_diameter(wheel):
    """
    Return the approximate diameter of the given wheel, 
    which is the bead seat diameter plus twice the tire width.

    Assume the following wheel attributes are non-null and non-empty:

    - bsd
    - tire_width

    Raise a ``ValueError``, if that is not the case.

    EXAMPLES::

        >>> w = Wheel(bsd=584, tire_width=42)
        >>> approx_diameter(w)
        668

    """
    w = wheel
    attrs = ['bsd', 'tire_width']
    check_attrs(w, *attrs)

    return w.bsd + 2*w.tire_width


