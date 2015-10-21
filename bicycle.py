import functools
from math import *
from fractions import gcd
from itertools import product

"""
All lengths are measured in mm unless noted otherwise.

TODO:

- Add more detail to docstrings
- Make a UI. For inspiration see http://www.bikecalc.com/ and http://en.wikipedia.org/wiki/Bicycle_gearing#Gear_ratio_calculators.

"""

def derailer_capacity(front_cogs, rear_cogs):
    """
    Return the derailer capacity needed to accommodate the given cog set.
    """
    return abs(front_cogs[-1] - front_cogs[0]) + \
      abs(rear_cogs[-1] - rear_cogs[0])

def gear_ratios(front_cogs, rear_cogs, digits=None):
    """
    Return the gear ratios for the given cogs.
    """
    result = {}
    for (f, r) in product(front_cogs, rear_cogs):
        result[(f, r)] = f/r

    if digits is not None:
        result = {k: round(v, digits) for k, v in result.items()}

    return result

def gain_ratios(crank_length, front_cogs, rear_cogs, wheel_diameter, 
  digits=None):
    """
    Return the gain ratios for the given parameters.
    For an explanation and calculator, respectively, see
    http://en.wikipedia.org/wiki/Bicycle_gearing#Measuring_gear_ratios
    http://sheldonbrown.com/gain.html.
    The wheel diameter is the diameter of the wheel with the tire on and
    inflated.
    """
    result = {}
    w = wheel_diameter/2/crank_length
    for (f, r) in product(front_cogs, rear_cogs):
        result[(f, r)] = w*f/r

    if digits is not None:
        result = {k: round(v, digits) for k, v in result.items()}

    return result

def speed_to_cadences(speed, crank_length, front_cogs, rear_cogs,
  wheel_diameter, digits=None):
    """
    Return cadences in revolutions/second. 
    Speed is measured in km/hour.
    """
    gr = gain_ratios(crank_length, front_cogs, rear_cogs, wheel_diameter)
    cl = crank_length
    result = {}
    for (k, g) in gr.items():
        result[k] = speed/(g*2*pi*cl)*(1e6/3600)

    if digits is not None:
        result = {k: round(v, digits) for k, v in result.items()}

    return result

def cadence_to_speeds(cadence, crank_length, front_cogs, rear_cogs,
   wheel_diameter, digits=None):
    """
    Return speeds in km/hour. 
    Cadence is measured in revolutions/second.
    """
    gr = gain_ratios(crank_length, front_cogs, rear_cogs, wheel_diameter)
    result = {}
    for (k, g) in gr.items():
        result[k] = g*2*pi*crank_length*cadence*(3600/1e6)

    if digits is not None:
        result = {k: round(v, digits) for k, v in result.items()}

    return result

def trail(head_tube_angle, fork_rake, wheel_diameter, digits=None): 
    """
    Return [trail, mechanical trail, wheel flop] for a bicycle
    with the given parameters.
    For an explanation and calculator, respectively, see
    http://en.wikipedia.org/wiki/Bicycle_and_motorcycle_geometry#Trail
    http://yojimg.net/bike/web_tools/trailcalc.php.
    """
    a = radians(head_tube_angle)
    wheel_radius = wheel_diameter/2
    trail = (wheel_radius*cos(a) - fork_rake)/sin(a)
    mechanical_trail = trail*sin(a)
    wheel_flop = trail*sin(a)*cos(a)
    result = [trail, mechanical_trail, wheel_flop]

    if digits is not None:
        result = [round(v, digits) for v in result]

    return result

def skid_patches(front_cogs, rear_cogs, ambidextrous=False):
    """
    For each pair of front and rear cog combinations (f, r), 
    compute the number of skid patches made on the 
    rear tire of a fixed gear bike with front cog f and 
    rear cog r.
    Let a and b denote the numerator and denominator of the fraction
    f/r in lowest terms.
    Then the number of skid patches is b with one proviso.
    If the skidder is ambidextrous (can skid with either foot forward),
    and a is odd, then the number of skid patches is 2*b.
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
    """
    return bsd + 2*tire_width


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

    def derailer_capacity(self):
        return derailer_capacity(
          front_cogs=self.front_cogs,
          rear_cogs=self.rear_cogs,
          )

    def gear_ratios(self, digits=None):
        return gear_ratios(
          front_cogs=self.front_cogs,
          rear_cogs=self.rear_cogs, 
          digits=digits,
          )

    def gain_ratios(self, digits=None):
        return gain_ratios(
          crank_length=self.crank_length, 
          front_cogs=self.front_cogs,
          rear_cogs=self.rear_cogs, 
          wheel_diameter=self.rear_wheel.diameter, 
          digits=digits,
          )

    def speed_to_cadences(self, speed, digits=None):
        return speed_to_cadences(
          speed, 
          crank_length=self.crank_length, 
          front_cogs=self.front_cogs,
          rear_cogs=self.rear_cogs, 
          wheel_diameter=self.rear_wheel.diameter, 
          digits=digits,
          )

    def cadence_to_speeds(self, cadence, digits=None):
        return cadence_to_speeds(
          cadence, 
          crank_length=self.crank_length, 
          front_cogs=self.front_cogs,
          rear_cogs=self.rear_cogs, 
          wheel_diameter=self.rear_wheel.diameter, 
          digits=digits,
          )
        
    def skid_patches(self, ambidextrous=False):
        return skid_patches(
          front_cogs=self.front_cogs, 
          rear_cogs=self.rear_cogs,
          ambidextrous=ambidextrous,
          )

    def trail(self, digits=None): 
        return trail(
          head_tube_angle=self.head_tube_angle, 
          fork_rake=self.fork_rake,
          wheel_diameter=self.front_wheel.diameter,
          )


class Wheel(object):
    """
    Represents a bicycle wheel
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

    def spoke_length(self, digits=None):
        return spoke_length(
          center_to_flange=self.center_to_flange, 
          flange_diameter=self.flange_diameter, 
          spoke_hole_diameter=self.spoke_hole_diameter, 
          erd=self.erd, 
          offset=self.offset, 
          num_spokes=self.num_spokes,
          num_crosses=self.num_crosses, 
          digits=digits
          )

    def approx_diameter(self):
        """
        Return the approximate wheel radius.
        The rim diameter is the bead seat diameter and not the effective
        rim diameter (ERD).
        """
        return approx_wheel_diameter(
          bsd=self.bsd, 
          tire_width=self.tire_width
          )
