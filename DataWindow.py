import tkinter as tk
from Plotter import Plotter

class DataWindow:
    def __init__(self, master, serial_reader):
        self.top = tk.Toplevel(master)
        self.top.title("Real Time Data")
        self.top.geometry("600x400")

        self.master = master
        self.serial_reader = serial_reader

        print("SHOW DATA WINDOWS")
        self.plotter = Plotter(self.top, self.serial_reader)
        self.plotter.plot()

        self.top.protocol("WM_DELETE_WINDOW", lambda: self._on_close())

    def _on_close(self):
        print("1 _on_close() ejecutado")
        self.plotter.stop()
        print("2 plotter.stop() ejecutado")
        self.serial_reader.stop()
        print("3 serial_reader.stop() ejecutado")
        self.top.destroy()
        print("4 top.destroy ejecutado")
        self.master.destroy()
        print("5 master.destroy ejecutado")
