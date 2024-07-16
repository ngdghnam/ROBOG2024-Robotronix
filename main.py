import sys
import os
sys.path.append(os.path.abspath('./Functions/CheckInternet'))
sys.path.append(os.path.abspath('./Functions/ChatBot'))
from gemini import gemini # type: ignore
from CheckInternet import internet_on # type: ignore
import config
# """
import YanAPI
ip_addr = config.YanIP
YanAPI.yan_api_init(ip_addr)
# """
    
if __name__ == "__main__":
    if internet_on():
        # YanAPI.start_voice_tts('Starting ChatBot mode'),True)
        YanAPI.start_voice_tts("Starting Gemini mode", False)
        gemini()
    else:
        # Chế độ offline -> offline.py
        pass