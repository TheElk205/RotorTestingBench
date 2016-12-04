#!/usr/bin/python3
import numpy as np

from python.guiQt.SerialCommunicator import SerialCommunicator
from python.guiQt.ValueMapper import ValueMapper


class MeasurementValuesProcessor:
    path = '/dev/ttyACM0'
    arduino = None
    valueMapper = None

    # Will contain all values read from serial mapped accordingly
    valuesPressure = [[] for y in range(5)]

    def __init__(self, serialCommunicator):
        self.arduino = serialCommunicator
        self.arduino.start()
        self.valueMapper = ValueMapper()

    def __del__(self):
        print("Ending Serial Reader Thread")
        if self.arduino is not None:
            self.arduino.join()

    def get_last_n_values(self, numberOfvalues):
        """
        Returns the last 'numberOfValues' values or less if less are available
        :param numberOfvalues:
        :return:
        """
        self.valuesPressure = [self.valueMapper.get_mapped_value(sensor[-numberOfvalues:]) for sensor in self.arduino.values]
        # self.valuesPressure = self.arduino.values
        # print("Arduino Values: {}".format(self.arduino.values))
        # print("Mapped Values: {}".format(self.valuesPressure))
        return [sensor for sensor in self.valuesPressure]

    def stop_serial(self):
        self.arduino.terminate = True

