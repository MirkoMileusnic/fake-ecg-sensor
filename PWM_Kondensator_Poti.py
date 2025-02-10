import RPi.GPIO as GPIO  #ChatGPT code, hier wird die Zeit abgemessen, wie lange es dauert bis ein Kondensator lädt und die Zeit wird durch den Poti-Widerstand geregelt
import time

# GPIO Pin Configurations
POTI_PIN = 18  # GPIO where potentiometer is connected

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(POTI_PIN, GPIO.IN)

def read_potentiometer():
    """ Measure the time taken for the capacitor to discharge """
    
    # Charge the capacitor
    GPIO.setup(POTI_PIN, GPIO.OUT)
    GPIO.output(POTI_PIN, True)
    time.sleep(0.1)  # Increase charge time for larger capacitors

    # Set pin to INPUT and start measuring discharge time
    GPIO.setup(POTI_PIN, GPIO.IN)
    
    start_time = time.time()
    while GPIO.input(POTI_PIN) == GPIO.HIGH:
        pass  # Wait for capacitor to discharge

    elapsed_time = time.time() - start_time  # Get discharge time
    return elapsed_time

def potiRead():
    """ Scale the potentiometer value between 0 and 1 """
    max_time = 0.5  # Adjust for larger capacitors (0.5s max)
    raw_value = read_potentiometer()
    
    # Normalize to 0-1 range
    factor = min(raw_value / max_time, 1)
    
    return factor

try:
    while True:
        poti_value = potiRead()
        print(f"Potentiometer Value: {poti_value:.5f}")
        time.sleep(0.2)  # Small delay for next reading

except KeyboardInterrupt:
    print("\nExiting...")
    GPIO.cleanup()
