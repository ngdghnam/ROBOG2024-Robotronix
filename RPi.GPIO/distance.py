import RPi.GPIO as GPIO
import time

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define GPIO pins for the ultrasonic sensor
TRIG = 23
ECHO = 24

# Set up the GPIO pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    # Send ultrasonic signal
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Wait for the signal to return
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Calculate the distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Formula to calculate distance
    distance = round(distance, 2)

    return distance

def detect_obstacle():
    distance = get_distance()

    # Condition to detect obstacles lower than 15mm
    if distance <= 5 cm:
        return True  # Obstacle detected
    else:
        return False  # No obstacle

# Main function for the robot to call
def main():
    try:
        while True:
            obstacle_detected = detect_obstacle()

            # Here you can handle robot logic if an obstacle is detected
            if obstacle_detected:
                # Take action when an obstacle is detected
                pass
            else:
                # Take action when no obstacle is detected
                pass

            time.sleep(1)

    except KeyboardInterrupt:
        GPIO.cleanup()

# Call the main function
if __name__ == "__main__":
    main()