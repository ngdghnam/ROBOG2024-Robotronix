# Xử lý cầm đồ vật 
import YanAPI as yapi 
import time 

# Reset tu the 
yapi.start_play_motion("reset")


# Cam do vat 
yapi.sync_do_tts("Starting pick up object", True)
time.sleep(0.5)

yapi.set_servos_angle({
    "RightShoulderRoll" : 90, 
    "RightShoulderLeft": 0,
    "+"    
}, 200)