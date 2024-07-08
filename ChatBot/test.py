import google.generativeai as genai
from func import (
    add,
    subtract,
    multiply,
    divide
)

genai.configure(api_key='AIzaSyBbW-oad2I-g5k4pAI9K0PSjZhqqHB6QYU')


model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", tools=[add, subtract, multiply, divide]
)

chat = model.start_chat(enable_automatic_function_calling=True)


response = chat.send_message(
    "I have 57 cats, each owns 100 mittens, how many mittens is that in total?"
)

print(response)
     