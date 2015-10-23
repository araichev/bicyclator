import unittest

from bicycle_calculator.bicycle import *


class TestBicycle(unittest.TestCase):
    def setUp(self):
        self.front_cogs = [30, 40]
        self.rear_cogs = [10]
        self.crank_length = 100
        self.wheel_diameter = 400

    def test_derailer_capacity(self):
        get = derailer_capacity(self.front_cogs, self.rear_cogs)
        expect = 10
        self.assertEqual(get, expect)

    def test_gear_ratios(self):
        get = gear_ratios(self.front_cogs, self.rear_cogs)
        expect = {(30, 10): 3, (40, 10): 4}
        self.assertEqual(get, expect)
        
    def test_gain_ratios(self):
        get = gain_ratios(self.front_cogs, self.rear_cogs, 
          self.crank_length, self.wheel_diameter)
        expect = {(30, 10): 6, (40, 10): 8}
        self.assertEqual(get, expect)

    def test_speed_to_cadences(self):
        pass

    def test_cadence_to_speeds(self):
        pass

    def test_trail(self):
        pass

    def test_skid_patches(self):
        pass

    def test_spoke_length(self):
        pass

    def test_approximate_wheel_diameter(self):
        pass

    def test_bicycle_init(self):
        pass

    def test_wheel_init(self):
        pass


if __name__ == '__main__':
    unittest.main()
