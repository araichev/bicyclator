# All lengths are measured in mm unless noted otherwise.
#
# Eventually make it so that user inputs more common measurements,
# such as rim diameter and tire width.
#
# See http://en.wikipedia.org/wiki/Bicycle_gearing#Gear_ratio_calculators
# for good UI features for calculators.
# Good UI at http://www.bikecalc.com/.
from math import *
from fractions import gcd
from itertools import product

class Bicycle(object):
    """
    Represents a bicycle.
    """
    def __init__(self, head_tube_angle=None, 
      fork_rake=None, crank_length=None,
      front_sprockets=[], rear_sprockets=[], rim_diameter=None, erd=None,
      tire_width=None, wheel_radius=None,
      center_to_flange={'left':None,'right':None},
      flange_diameter={'left':None,'right':None},
      spoke_hole_diameter=2.6, spokes=None, crosses=None, offset=0):
        self.head_tube_angle = head_tube_angle
        self.fork_rake = fork_rake
        self.crank_length = crank_length
        self.front_sprockets = front_sprockets  # e.g. [46,36]
        self.rear_sprockets = rear_sprockets    # e.g. [12,14,16,18,20]
        self.rim_diameter = rim_diameter
        self.erd = erd
        self.tire_width = tire_width
        self.wheel_radius = wheel_radius
        self.center_to_flange = center_to_flange    # e.g. {'left':45,'right:20}
        self.flange_diameter = flange_diameter  # e.g. {'left':45,'right:45}
        self.spoke_hole_diameter = spoke_hole_diameter
        self.spokes = spokes
        self.crosses = crosses
        self.offset = offset
    
    def __str__(self):
        s = "specs\n"
        s += "-----\n"
        for (k, v) in sorted(self.__dict__.items()):
            s += "%s = %s\n" % (k, v)
        return s
        
    def cadence(self, speed, digits=1):
        """
        Return cadences in revolutions/minute. 
        Speed is measured in km/hour.
        """
        gr = self.gain_ratio()
        cl = self.crank_length
        result = {}
        for (k, g) in gr.items():
            temp = speed/(g*2*pi*cl)*(1000000/60.0)
            result[k] = round(temp, digits)
        return result

    def derailer_capacity(self):
        """
        Return the derailer capacity needed for this bike's sprocketset.
        """
        return abs(self.front_sprockets[0] - self.front_sprockets[-1]) + \
        abs(self.rear_sprockets[0] - self.rear_sprockets[0])

    def gain_ratio(self, digits=1):
        """
        Return the gain ratios.
        For an explanation and calculator, respectively, see
        http://en.wikipedia.org/wiki/Bicycle_gearing#Measuring_gear_ratios
        http://sheldonbrown.com/gain.html.
        The wheel radius is the distance from the center of the hub to the
        rolling surface of the tire.
        """
        result = {}
        w = self.wheel_radius/self.crank_length
        for (f, r) in product(self.front_sprockets, self.rear_sprockets):
            temp = w*f/r
            result[(f, r)] = round(temp, digits)
        return result
    
    def mechanical_advantage(self):
        """
        Return the mechanical advantage of this bike's cantilever brake.
        See
        http://www.circleacycles.com/cantilevers/
        """
        pass    
    
    def skid_patches(self, ambidextrous=False):
        """
        For each pair of front and rear sprocket combinations (f, r) of in
        this bike's sprocketset, compute the number of skid patches made on the 
        rear tire of a fixed gear bike with front sprocket f and rear sprocket r.
        Let a and b denote the numerator and denominator of the fraction
        f/r in lowest terms.
        Then the number of skid patches is b with one proviso.
        If the skidder is ambidextrous (can skid with either foot forward),
        and a is odd, then the number of skid patches is 2*b.
        """
        result = {}
        for (f, r) in product(self.front_sprockets, self.rear_sprockets):
            g = gcd(f, r)
            a = f/g
            b = r/g
            if ambidextrous and a % 2 != 0:
                result[(f, r)] =  2*b
            else: 
                result[(f, r)] = b
        return result

    def speed(self, cadence, digits=1):
        """
        Return speeds in km/hour. Cadence is measured in revolutions/minute.
        """
        gr = self.gain_ratio()
        cl = self.crank_length
        result = {}
        for (k, g) in gr.items():
            temp = g*2*pi*cl*cadence*(60.0/1000000)
            result[k] = round(temp, digits)
        return result
    
    def spoke_length(self, digits=1):
        """
        Return the left (nondrive side) and right (drive side) spoke lengths
        for this bike's wheel.
        """
        result = {}
        for k in self.center_to_flange.keys():
            if k == 'right':
                o = self.offset
            else:
                o = -self.offset
            d = self.center_to_flange[k] + o
            r1 = self.flange_diameter[k]/2
            r2 = self.erd/2
            r3 = self.spoke_hole_diameter/2
            a = 2*pi*self.crosses/(self.spokes/2)
            temp = sqrt(d**2 + r1**2 + r2**2 - 2*r1*r2*cos(a)) - r3
            result[k] = round(temp, digits)
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
        trail =  (self.wheel_radius*cos(a) - self.fork_rake)/sin(a)
        mechanical_trail = trail*sin(a)
        wheel_flop = trail*sin(a)*cos(a)
        result = (trail, mechanical_trail, wheel_flop)
        return [round(x, digits) for x in result]

    def wheel_radius_approx(self):
        """
        Return the approximate wheel radius.
        The rim diameter is the bead seat diameter and not the effective
        rim diameter (ERD).
        """
        return int(self.rim_diameter/2 + self.tire_width)
