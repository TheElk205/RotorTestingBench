#!/usr/bin/python3
import numpy as np

from python.guiQt.SerialReader import SerialReader
from python.guiQt.ValueMapper import ValueMapper


class MeasurementValuesProcessor:
    path = '/dev/ttyACM0'
    arduino = None
    valueMapper = None

    # Will contain all values read from serial mapped accordingly
    valuesPressure = [[] for y in range(5)]

    def __init__(self, path):
        self.path = path
        self.arduino = SerialReader(path)
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
        self.valuesPressure = [self.valueMapper.get_mapped_value(sensor) for sensor in self.arduino.values]
        # print("Arduino Values: {}".format(self.arduino.values))
        # print("Mapped Values: {}".format(self.valuesPressure))
        return [sensor[-numberOfvalues:] for sensor in self.valuesPressure]

    def stop_serial(self):
        self.arduino.terminate = True

