import google.generativeai as genai
import sys
import os

for folder in os.listdir('./Functions'):
    sys.path.append(os.path.abspath('./Functions/'+folder))

# Tất cả hàm phải nằm trong một folder nằm trong folder Functions
from music import ( # type: ignore
    find_music,
    download_music,
    play_music
)
from read_braille import ( # type: ignore
    read_braille
)

"""
import time
sys.path.append(os.path.abspath('.'))
import config
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
            read_braille
        ]

        model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                                    tools=functions,
                                    system_instruction=instruction)
        chat = model.start_chat(enable_automatic_function_calling = True, history=[])
        
        start_message = chat.send_message('This is a system message, do not reply to this, start by introducing yourself to the user')
        print(f"Yanshee: {start_message.text}")
        """
        YanAPI.start_voice_tts(str(start_message.text),True)
        time.sleep(2)
        # """
        
        while True:
            # listen_res = YanAPI.sync_do_voice_asr_value() | add thêm if check người dùng có nói ko
            prompt = input("User: ")
            # prompt = listen_res["question"]
            if (prompt == "exit"):
                break
            response = chat.send_message(prompt)
            print(f"Yanshee: {response.text}")
            # YanAPI.start_voice_tts(str(response.text),True)

if __name__ == "__main__":
    gemini()