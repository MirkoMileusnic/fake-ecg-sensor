import serial

def potiRead(COM, baudrate, timeout, MAX):
    serial = serial.Serial(port=COM, baudrate=baudrate, timeout=timeout)    # bei Linux port=´/dev/ttyACM0´

    while True:
        if serial.in_waiting > 0:
            poti_value = serial.readline().decode('utf-8').strip()
            factor = int(poti_value)/MAX
            return factor
