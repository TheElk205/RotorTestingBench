#!/usr/bin/python3
from time import sleep

import serial
import threading
import datetime
import numpy as np
import re
import json

from struct import unpack, calcsize

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
                self.read_bytes_from_serial()
                self.counter += 1
            except serial.SerialException as serEx:
                print("Serial exception: {0}".format(serEx))
                self.terminate = True
    def read_bytes_from_serial(self):
        isMessage = False
        if not isMessage:
            print("Waiting for message: ")
            zerosCount = 0
            while zerosCount < 5:
                bytes = self.arduino.read(1)
                if unpack('B', bytes)[0] == 0:
                    zerosCount = zerosCount +1
                else:
                    zerosCount = 0
        print("Message Started: ")
        pin = unpack('B', self.arduino.read(1))[0]
        print("Pin: {0}".format(pin))
        value = unpack('B', self.arduino.read(1))[0]
        print("value: {0}".format(value))
        time = unpack('I', self.arduino.read(4))[0]
        print("time: {0}".format(time))

        valuepair = np.array([time, value])
        self.values[pin].append(valuepair)

    def read_json_from_serial(self):
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