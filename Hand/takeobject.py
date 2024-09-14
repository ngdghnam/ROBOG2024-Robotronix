import YanAPI 

ip = "192.168.0.160"
YanAPI.yan_api_init(ip)
# Reset tu the 
def reset_body():
    YanAPI.sync_play_motion('reset')

dist  = 27 

# Cam do vat
# YanAPI.sync_play_motion('stretch', 'both')
YanAPI.set_servos_angles(
    {
        # Tay phai 
        "RightShoulderRoll" : 0, 
        "RightShoulderFlex" : 180,
        "RightElbowFlex" : 120,

        # Angles from each hand are opposite to each other

        # Tay Trai
        "LeftShoulderRoll" : 180, 
        "LeftShoulderFlex" : 0,
        "LeftElbowFlex" : 60,         
    },
    200
)
