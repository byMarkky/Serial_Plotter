import serial
import serial.tools.list_ports
import time

def list_ports():
    """Lista los puertos seriales disponibles para ayudarte a identificar el correcto."""
    return serial.tools.list_ports.comports()


def read_port(puerto, baudrate=115200):
    """
    Abre el puerto serial y lee datos línea por línea del ESP32.

    puerto: ej. 'COM3' en Windows, '/dev/ttyUSB0' o '/dev/ttyACM0' en Linux/Mac
    baudrate: debe coincidir con el Serial.begin() del código del ESP32
    """
    try:
        ser = serial.Serial(puerto, baudrate, timeout=1)
        print(f"Conectado a {puerto} a {baudrate} baudios.")
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

