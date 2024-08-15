import sys
import os
sys.path.append(os.path.abspath('./Functions/CheckInternet'))
sys.path.append(os.path.abspath('./Functions/ChatBot'))
from gemini import gemini # type: ignore
from CheckInternet import internet_on # type: ignore
import config
import time

import YanAPI
ip_addr = config.YanIP
YanAPI.yan_api_init(ip_addr)
    
if __name__ == "__main__":
    YanAPI.sync_play_motion(name="raise",direction="right",speed="fast",repeat=3)
    time.sleep(1)
    YanAPI.start_play_motion(name="reset")
    
    if internet_on():
        YanAPI.start_voice_tts("Internet connection detected, starting Chatbot mode", False)
        gemini()
    else:
        # Chế độ offline
        YanAPI.start_voice_tts("No Internet Connection", False)