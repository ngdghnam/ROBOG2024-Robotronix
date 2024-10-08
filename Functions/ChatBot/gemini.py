import google.generativeai as genai
import sys
import os
import fnmatch

for folder in os.listdir('./Functions'):
    sys.path.append(os.path.abspath('./Functions/'+folder))

# Import tất cả hàm chức năng
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
from face_reg import ( # type: ignore
    face_registration,
    face_recognition,
    add_face_data
)
from object_detection import ( # type: ignore
    detect_obj
)

import time
sys.path.append(os.path.abspath('.'))
import config
import YanAPI
ip_addr = config.YanIP
YanAPI.yan_api_init(ip_addr)

def gemini():
    with open('./Functions/ChatBot/personality.txt', 'r') as instruction: # cài đặt tính cách cho Gemini

        genai.configure(api_key=config.Gemini_API_KEY)
        
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
         
        # set up

        model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                                    tools=functions,
                                    system_instruction=instruction)
        chat = model.start_chat(enable_automatic_function_calling = True, history=[])
        
        # init Gemini và cho Gemini bắt đầu conversation trước
        start_message = chat.send_message('This is a system message, do not reply to this, start by a quick introduction')
        print(f"Yanshee: {start_message.text}")
        YanAPI.start_voice_tts(str(start_message.text),False)
        YanAPI.sync_play_motion('bow', speed='slow')
        YanAPI.start_play_motion('Reset', speed='slow')
        time.sleep(3)
        
        # Program loop
        while True:
            listen_res = YanAPI.sync_do_voice_asr_value()
            prompt = listen_res["question"]
            print(f'user: {prompt}')
            match prompt: # Nếu user nói goodbye -> end program
                case prompt if fnmatch.fnmatch(prompt, "*Good Bye"):
                    print('Yanshee: Goodbye, see you later')
                    YanAPI.sync_do_tts("Goodbye, see you later",False)
                    break
                case prompt if len(prompt) == 0: # Không nghe user
                    print('Yanshee: I cannot hear you, please repeat')
                    YanAPI.sync_do_tts("I cannot hear you, please repeat",False)
                case _:
                    response = chat.send_message(prompt)
                    print(f"Yanshee: {response.text}")            
                    YanAPI.sync_do_tts(str(response.text),False)

if __name__ == "__main__":
    gemini()