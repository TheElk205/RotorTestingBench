#!/usr/bin/python3
import serial
import threading
import datetime
import numpy as np
import re

class SerialReader (threading.Thread):
    values = [[] for y in range(4)]
    terminate = False
    ser = serial.Serial('/dev/ttyACM0', 9600)
    print(ser.name)

    def __init__(self, threadid, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadid
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        # Get lock to synchronize threads
        while not self.terminate:
            try:
                self.read_from_serial()
                self.counter += 1
            except serial.SerialException:
                print("Serial exception")

    def read_from_serial(self):
        line = self.ser.readline().decode("utf-8")
        sensor, value = self.get_value_from_serial_string(line)
        currenttime = datetime.datetime.now().timestamp()
        valuepair = np.array([currenttime, value])
        self.values[sensor].append(valuepair)

    def get_value_from_serial_string(self, serialstring):
        pattern = re.compile("^[0-9]:[0-9]+(\r\n|\r|\n)")
        if not pattern.match(serialstring):
            return 0, 0
        read = serialstring.split(':')
        return int(read[0]), int(read[1])

    def exit(self):
        self.terminate = True

    def get_values(self):
        return self.values