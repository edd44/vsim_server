#!/usr/bin/python2.7
import curses
import socket
import struct
import time
import math
from vsim_server import *


def main(stdscr):
    s = setup_socket()
    curses.initscr()

    while 1:
        data = s.recv(256)
        outsim_pack = struct.unpack('I12f3i', data)
        #print(str(outsim_pack[7]) + " " + str(outsim_pack[8]) +" "+ str(outsim_pack[9]))
        accel = [outsim_pack[7], outsim_pack[8], outsim_pack[9]]
        pos = [outsim_pack[13], outsim_pack[14], outsim_pack[15]]
        header = outsim_pack[4]#/3.14
        pitch = outsim_pack[5]#/3.14
        roll = outsim_pack[6]#/3.14

        # accel = [9.2342342344, -24.323, 0.2341]
        # pos = [435,23,0.1233]
        # header = 2
        # pitch = 3.123
        # roll = 13.2

        stdscr.addstr(0, 0, "accel", 0)
        stdscr.addstr(1, 3,  "x: %10.2f" % accel[0], 0)
        stdscr.addstr(2, 3,  "y: %10.2f" % accel[1], 0)
        stdscr.addstr(3, 3,  "z: %10.2f" % accel[2], 0)

        stdscr.addstr(0+5, 0, "position", 0)
        stdscr.addstr(1+5, 3,  "x: %10.2f" % pos[0], 0)
        stdscr.addstr(2+5, 3,  "y: %10.2f" % pos[1], 0)
        stdscr.addstr(3+5, 3,  "z: %10.2f" % pos[2], 0)

        stdscr.addstr(0+10, 0, "local?", 0)
        stdscr.addstr(1+10, 3,  "head:  %10.2f" % header, 0)
        stdscr.addstr(2+10, 3,  "pitch: %10.2f" % pitch, 0)
        stdscr.addstr(3+10, 3,  "roll:  %10.2f" % roll, 0)

        local_accel = [1,1,1]
        local_accel[0] = math.cos(header)*accel[0] + math.sin(header)*accel[1]
        local_accel[1] = -math.sin(header)*accel[0] + math.cos(header)*accel[1]
        local_accel[2] = 1

        stdscr.addstr(0+15, 0, "local accel", 0)
        stdscr.addstr(1+15, 3,  "x:  %10.2f" % local_accel[0], 0)
        stdscr.addstr(2+15, 3,  "y: %10.2f" % local_accel[1], 0)
        stdscr.addstr(3+15, 3,  "z:  %10.2f" % local_accel[2], 0)

        #time.sleep(1)
        stdscr.refresh()
    curses.endwin()

if __name__ == "__main__":
    curses.wrapper(main)
