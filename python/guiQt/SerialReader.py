#!/usr/bin/python3
from time import sleep

import serial
import threading
import datetime
import numpy as np
import re
import json

class SerialReader (threading.Thread):
    values = [[] for y in range(5)]
    terminate = False
    arduino = serial.Serial('/dev/ttyACM0', 9600)
    print(arduino.name)
    # Toggle DTR to reset Arduino
    arduino.setDTR(False)
    sleep(1)
    # toss any data already received, see
    # http://pyserial.sourceforge.net/pyserial_api.html#serial.Serial.flushInput
    arduino.flushInput()
    arduino.setDTR(True)


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
            except serial.SerialException as serEx:
                print("Serial exception: {0}".format(serEx))
                self.terminate = True

    def read_from_serial(self):
        line = self.arduino.readline().decode("utf-8")
        print("line: " + line)
        if line.startswith("{"):
            j = json.loads(line)
            valuepair = np.array([j['time'], j['value']])
            self.values[j['pin']].append(valuepair)

    def exit(self):
        self.terminate = True

    def get_values(self):
        return self.values