import google.generativeai as genai
import sys
import os
import fnmatch

for folder in os.listdir('./Functions'):
    sys.path.append(os.path.abspath('./Functions/'+folder))

# Tất cả hàm phải nằm trong một folder nằm trong folder Functions
from music import ( # type: ignore
    find_music,
    download_music,
    play_music,
    check_available_song
)
from weather import ( # type: ignore
    weather
)
"""
# Không có sensor
from TempDectect import ( # type: ignore
    temperature_sensor,
    humidity_sensor
)
"""
from face_reg import ( # type: ignore
    face_registration,
    face_recognition,
    add_face_data
)
from object_detection import ( # type: ignore
    detect_obj
)

#"""
import time
sys.path.append(os.path.abspath('.'))
import config
import YanAPI
ip_addr = config.YanIP
YanAPI.yan_api_init(ip_addr)
# """

def gemini():
    with open('./Functions/ChatBot/personality.txt', 'r') as instruction:

        genai.configure(api_key='AIzaSyBbW-oad2I-g5k4pAI9K0PSjZhqqHB6QYU')
        
        functions=[
            find_music,
            download_music,
            play_music,
            weather,
            check_available_song,
            face_registration,
            face_recognition,
            add_face_data,
            detect_obj
        ]

        model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                                    tools=functions,
                                    system_instruction=instruction)
        chat = model.start_chat(enable_automatic_function_calling = True, history=[])
        
        start_message = chat.send_message('This is a system message, do not reply to this, start by a quick introduction')
        print(f"Yanshee: {start_message.text}")
        # """
        YanAPI.start_voice_tts(str(start_message.text),False)
        YanAPI.sync_play_motion('bow', speed='slow')
        YanAPI.start_play_motion('Reset', speed='slow')
        time.sleep(3)
        # """
        
        while True:
            listen_res = YanAPI.sync_do_voice_asr_value()
            prompt = listen_res["question"]
            print(f'user: {prompt}')
            match prompt:
                case prompt if fnmatch.fnmatch(prompt, "*Shut down"):
                    break # Thêm code tắt robot cũm được
                case prompt if len(prompt) == 0:
                    print('Yanshee: I cannot hear you, please repeat')
                    YanAPI.sync_do_tts("I cannot hear you, please repeat",False)
                case _:
                    response = chat.send_message(prompt)
                    print(f"Yanshee: {response.text}")            
                    YanAPI.sync_do_tts(str(response.text),False)
            

if __name__ == "__main__":
    gemini()