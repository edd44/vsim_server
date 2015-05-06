#!/usr/bin/python2.7
import serial
import sys
import pygame
import time
from window import Window

'''
Pseudo-PWM servo interface description

      150

180         120
       #
    __ # __
    |  #  |
    |  #  |
    |     |
    |     |
    | TOP |
    |_____|

    #0 - left servo
    #1 - right servo

ISO convention {X-roll, Y-Pitch, Z-yaw}
'''


class Config:
    drive_middle_position = 150
    drive_multiplier = 25


def calc_checksum(servo_nr, value):
    s = str(int(value)).zfill(3)
    return (int(s[0])+int(s[1])+int(s[2])+servo_nr)%10


def format_packet(servo_nr, value):
    checksum = calc_checksum(servo_nr, value)
    packet = "/"+str(servo_nr)+str(int(value)).zfill(3)+str(checksum)+"\\"
    return packet


def set_servo(servo_nr, value):
    try:
        s = serial.Serial("/dev/ttyUSB0", 19200)
        s.write(format_packet(servo_nr, value))
    except serial.serialutil.SerialException:
        print "Unable to open USB serial"
    time.sleep(.02)


def calc_left_drive(pitch, roll):
    return (-pitch+roll)*Config.drive_multiplier+Config.drive_middle_position


def calc_right_drive(pitch, roll):
    return (pitch+roll)*Config.drive_multiplier+Config.drive_middle_position

def dump_results(results):
    f = open('result_file','w')
    f.write('time\tpitch\troll\n')
    for entry in results:
        f.write(str(entry['time']) + "\t" + "{:.3f}".format(entry['pitch'])+ "\t" + "{:.3f}".format(entry['roll']) + "\n")
    f.write("\n")
    f.close()

def main():
    pygame.joystick.init()
    j = pygame.joystick.Joystick(0)
    j.init()
    pygame.init()
    window = Window()
    results = [];

    while 1:
        time.sleep(.01)
        pitch =(j.get_axis(1))
        roll =(j.get_axis(0))
        lservo = int(calc_left_drive(pitch, roll))
        rservo = int(calc_right_drive(pitch, roll))
        results.append({'time': time.time(), 'pitch': pitch, 'roll': roll})
        set_servo(0, lservo)
        set_servo(1, rservo)

        for event in pygame.event.get():
            window.screen.fill((0, 0, 0))
            window.set_pitch_value(pitch)
            window.set_roll_value(roll)
            window.set_lservo_value(lservo)
            window.set_rservo_value(rservo)
            pygame.display.flip()
            if event.type == pygame.QUIT:
                dump_results(results)
                sys.exit()

if __name__ == "__main__":
    main()
