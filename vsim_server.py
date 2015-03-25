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

    screen_height = 240
    screen_width = 320

def calc_checksum(servo_nr, value):
    s = str(int(value)).zfill(3)
    return (int(s[0])+int(s[1])+int(s[2])+servo_nr)%10

def format_packet(servo_nr, value):
    checksum = calc_checksum(servo_nr, value)
    packet="/"+str(servo_nr)+str(int(value)).zfill(3)+str(checksum)+"\\"
    return packet

def set_servo(servo_nr, value):
    s = serial.Serial("/dev/ttyUSB0", 19200)
    s.write(format_packet(servo_nr, value))
    time.sleep(.02)

def calc_left_drive(pitch, roll):
    return (-pitch+roll)*Config.drive_multiplier+Config.drive_middle_position

def calc_right_drive(pitch, roll):
    return (pitch+roll)*Config.drive_multiplier+Config.drive_middle_position

def main():
    pygame.joystick.init()
    j = pygame.joystick.Joystick(0)

    j.init()
    pygame.init()
    size = width, height = Config.screen_width, Config.screen_height
    screen = pygame.display.set_mode(size)
    font = pygame.font.SysFont("calibri",30)

    #middle_position = 150
    #multiplier = -50
    #position = middle_position

    pitch_label_pos = (Config.screen_width / 2, 10)
    roll_label_pos = (10, Config.screen_height / 2)
    lservo_label_pos = (10, Config.screen_height-30)
    rservo_label_pos = (Config.screen_width-70, Config.screen_height-30)

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
            screen.fill((0,0,0))

            screen.blit(font.render(str(int(pitch*100)), True,(255,255,255)),pitch_label_pos)
            screen.blit(font.render(str(int(roll*100)), True,(255,255,255)),roll_label_pos)

            screen.blit(font.render(str(lservo), True,(255,255,255)),lservo_label_pos)
            screen.blit(font.render(str(rservo), True,(255,255,255)),rservo_label_pos)

            center = [Config.screen_width/2, Config.screen_height/2]
            pygame.draw.line(screen, (255,0,0), center, [Config.screen_width/2, Config.screen_height/2+int(pitch*100)], 10)
            pygame.draw.line(screen, (0,255,0), center, [Config.screen_width/2+int(roll*100), Config.screen_height/2], 10)


            pygame.display.flip()
            if event.type == pygame.QUIT: sys.exit()

if __name__ == "__main__":
    main()
