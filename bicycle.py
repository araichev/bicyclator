import functools
from math import *
from fractions import gcd
from itertools import product

"""
All lengths are measured in mm unless noted otherwise.

Eventually make it so that user inputs more common measurements,
such as rim diameter and tire width.

See http://en.wikipedia.org/wiki/Bicycle_gearing#Gear_ratio_calculators
for good UI features for calculators.
Good UI at http://www.bikecalc.com/.
"""

def gain_ratios(crank_length, cogs, wheel_diameter, digits=1):
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
    for (f, r) in product(cogs['front'], cogs['rear']):
        temp = w*f/r
        result[(f, r)] = round(temp, digits)
    return result

def speed_to_cadences(speed, crank_length, cogs, wheel_diameter, digits=1):
    """
    Return cadences in revolutions/minute. 
    Speed is measured in km/hour.
    """
    gr = gain_ratios(crank_length, cogs, wheel_diameter)
    cl = crank_length
    result = {}
    for (k, g) in gr.items():
        temp = speed/(g*2*pi*cl)*(1000000/60)
        result[k] = round(temp, digits)
    return result

def cadence_to_speeds(cadence, crank_length, cogs, wheel_diameter, digits=1):
    """
    Return speeds in km/hour. 
    Cadence is measured in revolutions/minute.
    """
    gr = gain_ratios(crank_length, cogs, wheel_diameter)
    cl = crank_length
    result = {}
    for (k, g) in gr.items():
        temp = g*2*pi*cl*cadence*(60/1000000)
        result[k] = round(temp, digits)
    return result

def derailer_capacity(cogs):
    """
    Return the derailer capacity needed to accommodate the given cog set.
    """
    return abs(cogs['front'][-1] - cogs['front'][0]) + \
      abs(cogs['rear'][-1] - cogs['rear'][0])


class Bicycle(object):
    """
    Represents a bicycle.
    """
    def __init__(self, name=None, head_tube_angle=None, 
      fork_rake=None, crank_length=None,
      cogs=None, wheels=None):
        self.name = name
        self.head_tube_angle = head_tube_angle
        self.fork_rake = fork_rake
        self.crank_length = crank_length
        if cogs is None:
            cogs = {'front': [], 'rear': []}
        self.cogs = {
          'front': sorted(cogs['front']), 
          'rear': sorted(cogs['rear']),
          }
        if wheels is None:
            wheels = {'front': Wheel(), 'rear': Wheel()}
        self.wheels = wheels
    
    def __repr__(self):
        s = self.name + '\n'
        s += '='*len(self.name) + '\n'
        for (k, v) in sorted(self.__dict__.items()):
            s += '{!s} = {!s}\n'.format(k, v)
        return s

    def derailer_capacity(self):
        return derailer_capacity(self.cogs)

    def gain_ratios(self, digits=1):
        return gain_ratios(self.crank_length, self.cogs, 
          self.wheels['rear'].diameter, digits=digits)

    def speed_to_cadences(self, speed, digits=1):
        return speed_to_cadences(speed, self.crank_length, self.cogs,
          self.wheels['rear'].diameter, digits=digits)

    def cadence_to_speeds(self, cadence, digits=1):
        return derailer_capacity(self.cogs, digits=digits)


    # def gain_ratios(self, digits=1):
    #     """
    #     Return the gain ratios.
    #     For an explanation and calculator, respectively, see
    #     http://en.wikipedia.org/wiki/Bicycle_gearing#Measuring_gear_ratios
    #     http://sheldonbrown.com/gain.html.
    #     The wheel radius is the distance from the center of the hub to the
    #     rolling surface of the tire.
    #     """
    #     result = {}
    #     wheel_radius = self.wheels['front'].diameter/2
    #     w = wheel_radius/self.crank_length
    #     for (f, r) in product(self.cogs['front'], self.cogs['rear']):
    #         temp = w*f/r
    #         result[(f, r)] = round(temp, digits)
    #     return result
        
    def skid_patches(self, ambidextrous=False):
        """
        For each pair of front and rear sprocket combinations (f, r) of in
        this bike's cogset, compute the number of skid patches made on the 
        rear tire of a fixed gear bike with front sprocket f and 
        rear sprocket r.
        Let a and b denote the numerator and denominator of the fraction
        f/r in lowest terms.
        Then the number of skid patches is b with one proviso.
        If the skidder is ambidextrous (can skid with either foot forward),
        and a is odd, then the number of skid patches is 2*b.
        """
        result = {}
        for (f, r) in product(self.cogs['front'], self.cogs['rear']):
            g = gcd(f, r)
            a = f/g
            b = r/g
            if ambidextrous and (a % 2) != 0:
                result[(f, r)] =  2*b
            else: 
                result[(f, r)] = b
        return result

        
    def trail(self, digits=1): 
        """
        Return this bike's trail, mechanical trail, and wheel flop.
        For an explanation and calculator, respectively, see
        http://en.wikipedia.org/wiki/Bicycle_and_motorcycle_geometry#Trail
        http://yojimg.net/bike/web_tools/trailcalc.php.
        The wheel radius is the distance from the center of the hub to the
        rolling surface of the tire.
        """
        a = radians(self.head_tube_angle)
        wheel_radius = self.wheels['front'].diameter/2
        trail = (wheel_radius*cos(a) - self.fork_rake)/sin(a)
        mechanical_trail = trail*sin(a)
        wheel_flop = trail*sin(a)*cos(a)
        result = (trail, mechanical_trail, wheel_flop)
        return [round(x, digits) for x in result]


class Wheel(object):
    """
    Represents a bicycle wheel
    """
    def __init__(self, name=None, rim_diameter=None, 
      erd=None, tire_width=None, diameter=None,
      center_to_flange=None, flange_diameter=None,
      spoke_hole_diameter=2.6, num_spokes=None, num_crosses=None, offset=0):
        self.name = name
        self.erd = erd
        self.tire_width = tire_width
        self.rim_diameter = rim_diameter
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

    def spoke_length(self, digits=1):
        """
        Return the left (nondrive side) and right (drive side) spoke lengths
        for this bike's wheel.
        """
        result = {}
        for k in self.center_to_flange:
            if k == 'right':
                o = self.offset
            else:
                o = -self.offset
            d = self.center_to_flange[k] + o
            r1 = self.flange_diameter[k]/2
            r2 = self.erd/2
            r3 = self.spoke_hole_diameter/2
            a = 2*pi*self.num_crosses/(self.num_spokes/2)
            temp = sqrt(d**2 + r1**2 + r2**2 - 2*r1*r2*cos(a)) - r3
            result[k] = round(temp, digits)
        return result

    def approx_diameter(self):
        """
        Return the approximate wheel radius.
        The rim diameter is the bead seat diameter and not the effective
        rim diameter (ERD).
        """
        return int(self.rim_diameter + 2*self.tire_width)
