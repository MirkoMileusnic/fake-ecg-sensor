import os
import socket
import time
import serial

# Load environment variables from .env
try:
    with open(".env", "r") as env_file:
        for line in env_file:
            key, value = line.strip().split("=", 1)
            os.environ[key] = value
except OSError as e:
    print("Error loading .env file:", e)

# Configuration
FILE_PATH = "2-sample-signal-100hz.txt"
UDP_ADDR = os.getenv("UDP_ADDR", "192.168.1.50")
UDP_PORT = int(os.getenv("UDP_PORT", 3000))
FREQUENCY_HZ = int(os.getenv("FREQUENCY_HZ", 100))
INTERVAL = 1.0 / FREQUENCY_HZ


# Convert float to bytes (MicroPython doesn't have struct module by default)
def float_to_bytes(value):
    return bytearray(str(value), "utf-8")

serial = serial.Serial(COM="COM3", baudrate=9600, timeout=1)    # bei Linux COM=´/dev/ttyACM0´ 

def potiRead(MAX):  
    if serial is None:  
        print("⚠️ No serial connection available!")
        return 1  
    try:
        poti_value = serial.readline().decode('utf-8').strip()
        factor = int(poti_value)/MAX
        return factor
    except Exception as e:
        print("Error: ", e)
        return 1


# Initialize UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    with open(FILE_PATH, "r") as file:
        for line in file:
            try:
                value = float(line.strip()) * potiRead(MAX=682)   # bei mir war 682 maximaler Wert vom Poti
                data = float_to_bytes(value)
                packet = bytearray([0]) + data  # Prepend data type byte
                sock.sendto(packet, (UDP_ADDR, UDP_PORT))
                print("Sent EKG sensor data:", value)
            except ValueError:
                print("Invalid line, skipping:", line.strip())

            time.sleep(INTERVAL)

    # Send termination packet
    sock.sendto(bytearray([3, 9]), (UDP_ADDR, UDP_PORT))
    print("Sent termination signal")
except OSError as e:
    print("Error accessing file:", e)
finally:
    sock.close()