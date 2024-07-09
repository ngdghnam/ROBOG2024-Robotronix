import google.generativeai as genai
from Find_music_test import find_music
from download_music import download_music

genai.configure(api_key='AIzaSyBbW-oad2I-g5k4pAI9K0PSjZhqqHB6QYU')

model = genai.GenerativeModel(model_name='gemini-1.5-flash', tools=[find_music, download_music])

chat = model.start_chat(enable_automatic_function_calling=True)

response = chat.send_message(
    "I want to find a song called IT BOY, can you provide the artist and download that song"
)

print(response)