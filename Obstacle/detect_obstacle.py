from YansheeRobot import YanAPI
from step_over import step_over_obstacle
import time

ip_addr = "10.10.63.13"  # Đổi IP
YanAPI.yan_api_init(ip_addr)

def get_distance():
    try:
        distance = YanAPI.get_sensors_ultrasonic_value()
        return distance / 10
    except Exception as e:
        return None

def detect_obstacle():
    distance = get_distance()
    if distance is not None:
        if distance <= 1.5:
            return True
    return False

def main():
    try:
        while True:
            if detect_obstacle():
                step_over_obstacle()
            time.sleep(1)

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
