import unittest
from vsim_server import *

class MyTest(unittest.TestCase):
    def test_checksum_calculation(self):
        self.assertEqual(calc_checksum(1, 100), 2)
        self.assertEqual(calc_checksum(3, 222), 9)
        self.assertEqual(calc_checksum(0, 99), 8)
        self.assertEqual(calc_checksum(9, 199), 8)

    def test_packet_formatter(self):
        self.assertEqual(format_packet(1,100), "/11002\\")
        self.assertEqual(format_packet(0,222), "/02226\\")
