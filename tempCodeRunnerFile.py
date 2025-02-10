import serial

serial = serial.Serial(port='COM3', baudrate=9600, timeout=1)    # bei Linux port=´/dev/ttyACM0´

while True:
    if serial.in_waiting > 0:
        poti_value = serial.readline().decode('utf-8').strip()
        print(poti_value) 