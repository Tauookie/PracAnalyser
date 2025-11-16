import matplotlib.pyplot as plt
import numpy as np
from random import randint

class Analyzer:
    def __init__(self, xData, yData, debug):
        self.x = xData
        self.y = yData
        self.D1 = None
        self.D2 = None
        self.debug = debug


    def get_derivatives(self):
        self.D1 = np.gradient(self.y, self.x)
        self.D2 = np.gradient(self.D1, self.x)

        self.debug_plot(self.x, self.D1)
        self.debug_plot(self.x, self.D2)


    def is_there_diode(self):
        averageD2 = np.mean(self.D2)
        deviations = (self.D2 - averageD2)**2
        avDev = np.std(self.D2)**2
        maxDeviation = deviations.max()

        return (maxDeviation - avDev) * 100


    def debug_plot(self, x, y):
        if self.debug:
            plt.figure(randint(1, 10 ** 6))
            plt.plot(x, y, marker='o')

if __name__ == '__main__':
    pass
