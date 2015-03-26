#!/usr/bin/python2.7
import serial
import sys
import pygame
import time

'''
Pseduo-PWM servo interface description

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

'''

class Config:
    drive_middle_position = 150
    drive_multiplier = 25


def calc_checksum(servo_nr, value):
    s = str(int(value)).zfill(3)
    return (int(s[0])+int(s[1])+int(s[2])+servo_nr)%10


def format_packet(servo_nr, value):
    checksum = calc_checksum(servo_nr, value)
    packet="/"+str(servo_nr)+str(int(value)).zfill(3)+str(checksum)+"\\"
    return packet


def set_servo(servo_nr, value):
    #s = serial.Serial("/dev/ttyUSB0", 19200)
    #s.write(format_packet(servo_nr, value))
    time.sleep(.02)


def calc_left_drive(pitch, roll):
    return (-pitch+roll)*Config.drive_multiplier+Config.drive_middle_position


def calc_right_drive(pitch, roll):
    return (pitch+roll)*Config.drive_multiplier+Config.drive_middle_position


class Window():
    def __init__(self):
        self.width = 320
        self.height = 240
        self.center = [int(self.width/2), int(self.height)/2]
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)
        self.font = pygame.font.SysFont("calibri", 30)
        self.pitch_label_pos = (self.width / 2, 10)
        self.roll_label_pos = (10, self.height / 2)
        self.lservo_label_pos = (10, self.height-30)
        self.rservo_label_pos = (self.width-70, self.height-30)

    def set_pitch_value(self, value):
        self.screen.blit(self.font.render(str(int(value*100)), True, (255, 255, 255)), self.pitch_label_pos)
        pygame.draw.line(self.screen, (255,0,0), self.center, [self.width/2, self.height/2+int(value*100)], 10)

    def set_roll_value(self, value):
        self.screen.blit(self.font.render(str(int(value*100)), True, (255, 255, 255)), self.roll_label_pos)
        pygame.draw.line(self.screen, (255,0,0), self.center, [self.width/2+int(value*100), self.height/2], 10)

    def set_rservo_value(self, value):
        self.screen.blit(self.font.render(str(value), True, (255, 255, 255)), self.rservo_label_pos)

    def set_lservo_value(self, value):
        self.screen.blit(self.font.render(str(value), True, (255, 255, 255)), self.lservo_label_pos)


def main():
    pygame.joystick.init()
    j = pygame.joystick.Joystick(0)

    j.init()
    pygame.init()

    window = Window()

    while 1:
        time.sleep(.01)
        #ISO convention {X-roll, Y-Pitch, Z-yaw}
        pitch =(j.get_axis(1))
        roll =(j.get_axis(0))
        #print str(pitch)+" "+str(roll)
        lservo = int(calc_left_drive(pitch, roll))
        rservo = int(calc_right_drive(pitch, roll))
        set_servo(0, lservo)
        set_servo(1, rservo)

        for event in pygame.event.get(): # User did something
            window.screen.fill((0,0,0))
            window.set_pitch_value(pitch)
            window.set_roll_value(roll)
            window.set_lservo_value(lservo)
            window.set_rservo_value(rservo)
            pygame.display.flip()
            if event.type == pygame.QUIT: sys.exit()

if __name__ == "__main__":
    main()
