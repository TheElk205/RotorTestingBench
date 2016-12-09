#!/usr/bin/python3
from time import sleep

import serial
import threading
import numpy as np
import json

from struct import unpack, calcsize

from serial import Serial


class SerialCommunicator (threading.Thread):
    values = [[] for y in range(6)]
    terminate = False
    path = '/dev/ttyACM0'
    arduino = None

    def __init__(self, path):
        threading.Thread.__init__(self)
        self.name = 'SerialReaderThread'

        self.path = path
        self.init_arduino()

    def run(self):
        print("Starting " + self.name)
        # Get lock to synchronize threads
        while not self.terminate:
            try:
                self.read_bytes_from_serial()
            except serial.SerialException as serEx:
                print("Serial exception: {0}".format(serEx))
                self.terminate = True

    def send_bytes_to_serial(self, data):
        self.arduino.write(bytearray([data]))

    def read_bytes_from_serial(self):
        isMessage = False
        if not isMessage:
            zerosCount = 0
            while zerosCount < 6:
                bytes = self.arduino.read(1)
                if unpack('B', bytes)[0] == 0:
                    zerosCount = zerosCount +1
                else:
                    zerosCount = 0

        # print("Message Started: ")
        pin = unpack('B', self.arduino.read(1))[0]
        # print("Pin: {0}".format(pin))
        value = unpack('H', self.arduino.read(2))[0]
        # print("value: {0}".format(value))
        time = unpack('I', self.arduino.read(4))[0]
        # print("time: {0}".format(time))

        valuepair = np.array([time, value])
        if(pin == 5):
            print(value)
        self.values[pin].append(valuepair)

    def exit(self):
        self.terminate = True

    def get_values(self):
        return self.values

    def init_arduino(self):
        self.arduino = Serial(self.path, 9600)
        print(self.arduino.name)
        # Toggle DTR to reset Arduino
        self.arduino.setDTR(False)
        sleep(1)
        # toss any data already received, see
        # http://pyserial.sourceforge.net/pyserial_api.html#serial.Serial.flushInput
        self.arduino.flushInput()
        self.arduino.setDTR(True)
