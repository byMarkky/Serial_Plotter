# TODO: Implement a class to plot all data read from serial port to matplotlib
from Config import Config


class Plotter:
    def __init__(self):
        self.config = Config()

    def set_config(self, config):
        self.config = config