#!/usr/bin/python2.7
import serial
import sys
import pygame
import time

def calc_checksum(servo_nr, value):
	s = str(int(value)).zfill(3)
	return (int(s[0])+int(s[1])+int(s[2])+servo_nr)%10

def format_packet(servo_nr, value):
	checksum = calc_checksum(servo_nr, value)
	packet="/"+str(servo_nr)+str(int(value)).zfill(3)+str(checksum)+"\\"
	return packet

def set_servo(servo_nr, value):
	s = serial.Serial("/dev/ttyUSB0", 19200)
	packet=format_packet(servo_nr, value)
	print packet
	s.write(packet)
	time.sleep(.02)

def main():
	pygame.joystick.init()
	j = pygame.joystick.Joystick(0)

	j.init()
	pygame.init()
	size = width, height = 320, 240
	screen = pygame.display.set_mode(size)

	middle_position = 150
	multiplier = -50
	position = middle_position

	while 1:
		time.sleep(.01)
		#ISO convention {X-roll, Y-Pitch, Z-yaw}
		pitch =-(j.get_axis(1))
		roll =-(j.get_axis(0))
		print str(pitch)+" "+str(roll)
		set_servo(1, (pitch+roll)*multiplier/2+middle_position)
		set_servo(0, (-pitch+roll)*multiplier/2+middle_position)

		for event in pygame.event.get(): # User did something
			if event.type == pygame.QUIT: sys.exit()

if __name__ == "__main__":
    main()
