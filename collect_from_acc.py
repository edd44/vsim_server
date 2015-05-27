#!/usr/bin/python2.7

import csv
import time
import serial
from parse import *

with open('../pomiary/acc.csv', 'w') as csvfile:
    fieldnames = ['time', 'x', 'y']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #writer.writeheader()
    s = serial.Serial("/dev/ttyUSB0", 115200)
    s.readline()
    now = time.time()
    print("Started successfully\n")

    # for i in range(4):
    #     writer.writerow({'time': time.time(), 'x':i, 'y':-i*3})

    try:
        while(1):
            line = s.readline()
            x, y = parse("X{} Y{}",str(line))
            writer.writerow({'time': (time.time()-now), 'x':x, 'y':y})
    except KeyboardInterrupt:
        s.close()
