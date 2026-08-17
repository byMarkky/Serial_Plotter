import serial
import serial.tools.list_ports
import time
import queue
import threading
import re
import csv
import datetime as dt
import os

def list_ports():
    """
    List all the ports of the computer
    :return: list
    """
    return serial.tools.list_ports.comports()

def read_port(puerto, baud_rate=115200):
    """
    Open the serial port and read the data line by line.

    :param puerto: ie. 'COM3' in Windows, '/dev/ttyUSB0' or '/dev/ttyACM0' in Linux/Mac
    :param baud_rate: baud rate of the serial port
    :return: None
    """
    try:
        ser = serial.Serial(puerto, baud_rate, timeout=1)
        print(f"Conectado a {puerto} a {baud_rate} baudios.")
        time.sleep(2)  # da tiempo a que el ESP32 reinicie tras abrir el puerto

        while True:
            if ser.in_waiting > 0:
                linea = ser.readline().decode('utf-8', errors='ignore').strip()
                if linea:
                    print(f"Recibido: {linea}")

    except serial.SerialException as e:
        print(f"Error al abrir el puerto: {e}")
    except KeyboardInterrupt:
        print("\nLectura interrumpida por el usuario.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Puerto cerrado.")

class SerialReader:
    def __init__(self, config):
        self.config = config
        self.puerto = config.get_port()
        self.baud_rate = config.get_baud_rate()
        self.data_queue = queue.Queue()
        self._stop_event = threading.Event()
        self.ser = None
        self.thread = None
        self.csv_path = None

        if self.csv_path is None:
            timestamp = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
            self.csv_path = f"datos_{timestamp}.csv"
        self.csv_file = None
        self.csv_writer = None

    def start(self):
        self.ser = serial.Serial(self.puerto, self.baud_rate, timeout=1)

        self.csv_file = open(self.csv_path, 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['timestamp', 'Celda', 'Temperatura'])

        self.thread = threading.Thread(target=self._leer, daemon=True)
        self.thread.start()

    def get_temperatures(self, linea):
        patron = self.config.get_regex()
        coincidencias = re.findall(patron, linea)
        return {int(num): float(temp) for num, temp in coincidencias}

    def _save_csv(self, temperaturas):
        timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        for celda, temp in temperaturas.items():
            self.csv_writer.writerow([timestamp, f"Celda {celda}", temp])
        self.csv_file.flush()   # Fuerza la escritura en el disco

    def _leer(self):
        while not self._stop_event.is_set():
            try:
                if self.ser.in_waiting > 0:
                    linea = self.ser.readline().decode('utf-8', errors='ignore').strip()
                    if linea:
                        temperaturas = self.get_temperatures(linea)
                        self.data_queue.put(temperaturas)
                        self._save_csv(temperaturas)
                        print(temperaturas)
            except serial.SerialException as e:
                print(f"Error al abrir el puerto: {e}")
                break

    def stop(self):
        print("Serial stop() llamado")
        self._stop_event.set()
        print(f"_stop_event.is_set(): {self._stop_event.is_set()}")
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)
            print("Puerto serial cerrado (thread)")
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Puerto serial cerrado (ser)")
        if self.csv_file:
            self.csv_file.close()
            print(f"CSV Guardado en: {os.path.abspath(self.csv_path)}")