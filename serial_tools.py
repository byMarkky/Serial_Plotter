import serial
import serial.tools.list_ports
import time

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
