from YansheeRobot import YanAPI
import time

ip_addr = "10.10.63.13"  # Đổi IP
YanAPI.yan_api_init(ip_addr)

def set_servo_angles(angles):
    return YanAPI.set_servos_angles_layers(angles)

def balance_with_arms():
    angles = {
        "RightShoulderRoll": {"angle": 180, "isNeedBessel": 0, "runtime": 2000},
        "LeftShoulderRoll": {"angle": 0, "isNeedBessel": 0, "runtime": 2000},
        "RightElbowFlex": {"angle": 90, "isNeedBessel": 0, "runtime": 2000},
        "LeftElbowFlex": {"angle": 90, "isNeedBessel": 0, "runtime": 2000} 
    }
    result = set_servo_angles(angles)
    time.sleep(2)
    return result

def lift_right_leg():
    angles = {
        "RightHipFB": {"angle": 90, "isNeedBessel": 0, "runtime": 2000},
        "RightKneeFlex": {"angle": 70, "isNeedBessel": 0, "runtime": 2000}
    }
    result = set_servo_angles(angles)
    time.sleep(2)
    return result

def step_right_leg_over():
    angles = {
        "RightHipFB": {"angle": 180, "isNeedBessel": 0, "runtime": 3000},
        "RightKneeFlex": {"angle": 60, "isNeedBessel": 0, "runtime": 3000}
    }
    result = set_servo_angles(angles)
    time.sleep(3)
    return result

def lower_right_leg():
    angles = {
        "RightHipFB": {"angle": 120, "isNeedBessel": 0, "runtime": 2000},
        "RightKneeFlex": {"angle": 40, "isNeedBessel": 0, "runtime": 2000}
    }
    result = set_servo_angles(angles)
    time.sleep(2)
    return result

def lift_left_leg():
    angles = {
        "LeftHipFB": {"angle": 90, "isNeedBessel": 0, "runtime": 2000},
        "LeftKneeFlex": {"angle": 70, "isNeedBessel": 0, "runtime": 2000}
    }
    result = set_servo_angles(angles)
    time.sleep(2)
    return result

def step_left_leg_over():
    angles = {
        "LeftHipFB": {"angle": 180, "isNeedBessel": 0, "runtime": 3000},
        "LeftKneeFlex": {"angle": 60, "isNeedBessel": 0, "runtime": 3000}
    }
    result = set_servo_angles(angles)
    time.sleep(3)
    return result

def lower_left_leg():
    angles = {
        "LeftHipFB": {"angle": 120, "isNeedBessel": 0, "runtime": 2000},
        "LeftKneeFlex": {"angle": 40, "isNeedBessel": 0, "runtime": 2000}
    }
    result = set_servo_angles(angles)
    time.sleep(2)
    return result

def return_to_standing():
    angles = {
        "RightShoulderRoll": {"angle": 90, "isNeedBessel": 0, "runtime": 2000},
        "LeftShoulderRoll": {"angle": 90, "isNeedBessel": 0, "runtime": 2000},
        "RightElbowFlex": {"angle": 90, "isNeedBessel": 0, "runtime": 2000}, 
        "LeftElbowFlex": {"angle": 90, "isNeedBessel": 0, "runtime": 2000},
        "RightHipFB": {"angle": 120, "isNeedBessel": 0, "runtime": 2000},
        "RightKneeFlex": {"angle": 0, "isNeedBessel": 0, "runtime": 2000},
        "LeftHipFB": {"angle": 120, "isNeedBessel": 0, "runtime": 2000},
        "LeftKneeFlex": {"angle": 0, "isNeedBessel": 0, "runtime": 2000}
    }
    result = set_servo_angles(angles)
    time.sleep(2)
    return result

def step_over_obstacle():
    result = {}
    
    result['balance_with_arms'] = balance_with_arms()
    
    result['lift_right_leg'] = lift_right_leg()
    
    result['step_right_leg_over'] = step_right_leg_over()
    
    result['lower_right_leg'] = lower_right_leg()

    result['lift_left_leg'] = lift_left_leg()

    result['step_left_leg_over'] = step_left_leg_over()

    result['lower_left_leg'] = lower_left_leg()

    result['return_to_standing'] = return_to_standing()
    
    return result

result = step_over_obstacle()