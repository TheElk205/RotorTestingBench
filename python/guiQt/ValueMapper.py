import numpy as np


class ValueMapper:

    def __init__(self):
        # For 100K predefined resistors
        self.perBit = 5 / 1024
        # Some basic value pairs [voltage, gram]
        self.mapping = np.array([[2.5, 10],
                            [3.55, 12],
                            [4, 50],
                            [4.2, 100],
                            [4.45, 200],
                            [4.5, 310],
                            [4.6, 450],
                            [4.65, 580],
                            [4.75, 710],
                            [4.8, 900],
                            [4.85, 1000]])

    def get_mapped_value(self, value):
        toMap = [row[1] for row in value]
        # print("Coming in: {0}".format(toMap))
        toMap = [value * 0.01 for value in toMap]
        # print("Going Out: {0}".format(toMap))
        return np.transpose(np.array([[row[0] for row in value], toMap]))

    def map_value(self, value):
        for i in range(len(self.mapping)):
            valueInvoltage = value*self.perBit
            if valueInvoltage >= self.mapping[i][0]:
                x1 = self.mapping[i][0]
                x2 = self.mapping[i+1][0]
                y1 = self.mapping[i][1]
                y2 = self.mapping[i+1][1]
                return y1 + ((valueInvoltage - x1)*(y2 - y1))/(x2-x1)
        return value
