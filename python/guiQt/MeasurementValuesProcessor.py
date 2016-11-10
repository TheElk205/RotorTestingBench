#!/usr/bin/python3
from python.guiQt.SerialReader import SerialReader
from python.guiQt.ValueMapper import ValueMapper


class MeasurementValuesProcessor:
    path = '/dev/ttyACM0'
    arduino = None
    valueMapper = None

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
        return self.valueMapper.get_mapped_value(self.arduino.values[-numberOfvalues:])

