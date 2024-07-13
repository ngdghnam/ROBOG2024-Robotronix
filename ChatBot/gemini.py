import google.generativeai as genai
import sys
import os
sys.path.append(os.path.abspath('./VoiceToMusic'))
from online_music import ( # type: ignore
    find_music,
    download_music,
    play_music
)
sys.path.append(os.path.abspath('./Read_Braille'))
from read_braille import ( # type: ignore
    read_braille
)


with open('./ChatBot/personality.txt', 'r') as instruction:

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
    
    while True:
        prompt = input("User: ")
        if (prompt == "exit"):
            break
        response = chat.send_message(prompt)
        print(f"Yanshee: {response.text}")