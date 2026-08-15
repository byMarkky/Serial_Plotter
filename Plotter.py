from Config import Config
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import datetime as dt
import matplotlib.cm as cm
import queue
import re

class Plotter:
    def __init__(self, master_frame, serial_reader):
        self.config = Config()
        self.data_limit = 20
        self.serial_reader = serial_reader

        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(1, 1, 1)

        self.canvas = FigureCanvasTkAgg(self.fig, master=master_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

        self.xs = []
        self.ys = {}
        self.colores = {}
        self._paletas = cm.tab10.colors
        self.ani = None

    def _color_celda(self, nombre_celda):
        if nombre_celda not in self.colores:
            index = len(self.colores) % len(self._paletas)
            self.colores[nombre_celda] = self._paletas[index]
        return self.colores[nombre_celda]

    def _parsear_celdas(self, linea):
        patron = r'Celda\s+(\d+):\s*(-?\d+\.?\d*)'
        coincidencias = re.findall(patron, linea)
        return {f"Celda {num}": float(temp) for num, temp in coincidencias}

    def animate(self, i, xs, ys):
        nuevos_datos = False
        while not self.serial_reader.data_queue.empty():
            try:
                linea = self.serial_reader.data_queue.get_nowait()
            except (ValueError, queue.Empty):
                break

            celdas = linea
            if not celdas:
                continue

            timestamp = dt.datetime.now().strftime('%H:%M:%S')
            xs.append(timestamp)
            nuevos_datos = True

            for nombre_celda, temp in celdas.items():
                if nombre_celda not in ys:
                    ys[nombre_celda] = []
                ys[nombre_celda].append(temp)

            if not nuevos_datos:
                return

        del xs[:-self.data_limit]
        for nombre_celda in ys:
            del ys[nombre_celda][:-self.data_limit]

        self.ax.clear()
        for nombre_celda, valores in ys.items():
            puntos_x = xs[-len(valores):]   # Usamos los ultimos N valores de xs
            self.ax.plot(puntos_x, valores, label=nombre_celda)
        self.ax.legend(loc='upper left')

        self.ax.tick_params(axis='x', rotation=45)
        self.fig.subplots_adjust(bottom=0.30)
        self.ax.set_title('Temperatura')
        self.ax.set_ylabel('Temperatura (ºC)')
        pass

    def plot(self):
        self.ani = animation.FuncAnimation(
            self.fig, self.animate,
            fargs=(self.xs, self.ys), interval=1000,
            cache_frame_data=False
        )
        self.canvas.draw()

    def set_config(self, config):
        self.config = config


    def stop(self):
        if self.ani:
            self.ani.event_source.stop()