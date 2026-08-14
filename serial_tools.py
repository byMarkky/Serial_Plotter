import serial
import serial.tools.list_ports
import time
import queue
import threading
import re

def list_ports():
    """
    List all the ports of the computer
    :return: list
    """
    return serial.tools.list_ports.comports()

# TODO: Change the method to return the data as an object
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
    def __init__(self, puerto, baud_rate=115200):
        self.puerto = puerto
        self.baud_rate = baud_rate
        self.data_queue = queue.Queue()
        self._stop_event = threading.Event()
        self.ser = None
        self.thread = None

    def start(self):
        self.ser = serial.Serial(self.puerto, self.baud_rate, timeout=1)
        self.thread = threading.Thread(target=self._leer, daemon=True)
        self.thread.start()

    def get_temperatures(self, linea):
        patron = r'Celda\s+(\d+):\s*(-?\d+\.?\d*)'
        coincidencias = re.findall(patron, linea)
        return {int(num): float(temp) for num, temp in coincidencias}

    def _leer(self):
        while not self._stop_event.is_set():
            try:
                if self.ser.is_open:
                    linea = self.ser.readline().decode('utf-8', errors='ignore').strip()
                    if linea:
                        temperaturas = self.get_temperatures(linea)
                        self.data_queue.put(temperaturas)
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