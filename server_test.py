import unittest
from vsim_server import *

class MyTest(unittest.TestCase):
    def test_checksum_calculation(self):
        self.assertEqual(calc_checksum(1, 100), 2)
        self.assertEqual(calc_checksum(3, 222), 9)
        self.assertEqual(calc_checksum(0, 99), 8)
        self.assertEqual(calc_checksum(9, 199), (9+1+9+9)%10)

    def test_packet_formatter(self):
        self.assertEqual(format_packet(1,100), "/11002\\")
        self.assertEqual(format_packet(0,222), "/02226\\")

    def test_position_calc(self):
        Config.middle_position = 150
        Config.drive_multiplier = 25
        self.assertEqual(calc_left_drive(0.,0.), 150)
        self.assertEqual(calc_left_drive(-1.,0.), 175)
        self.assertEqual(calc_left_drive(0.,-1.), 125)
        self.assertEqual(calc_left_drive(-1.,-1.), 150)
        self.assertEqual(calc_left_drive(1.,1.), 150)
        self.assertEqual(calc_right_drive(0.,0.), 150)
        self.assertEqual(calc_right_drive(-1.,0.), 125)
        self.assertEqual(calc_right_drive(0.,-1.), 125)
        self.assertEqual(calc_right_drive(-1.,-1.), 100)
        self.assertEqual(calc_right_drive(1.,1.), 200)
