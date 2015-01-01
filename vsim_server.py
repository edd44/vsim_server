import serial
import sys
import pygame
import time

s = serial.Serial("/dev/ttyUSB0", 19200)

pygame.joystick.init()
j = pygame.joystick.Joystick(0)

j.init()
pygame.init()
size = width, height = 320, 240
screen = pygame.display.set_mode(size)

middle_position = 130
multiplier = -50
position = middle_position

while 1:
	time.sleep(.001)
	position = int(j.get_axis(0)*multiplier+middle_position)
	print position
	s.write(chr(position))

	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: sys.exit()