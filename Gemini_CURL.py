import os
import requests

headers = {
    'Content-Type': 'application/json',
}

params = {
    'key': os.getenv('AIzaSyBbW-oad2I-g5k4pAI9K0PSjZhqqHB6QYU', ''),
}

data = '{"contents": [{"role":"user","parts":[{"text": "Hello"}]},{"role": "model","parts":[{"text": "Great to meet you. What would you like to know?"}]},{"role":"user","parts":[{"text": "I have two dogs in my house. How many paws are in my house?"}]},]}'


response = requests.post(
    'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyBbW-oad2I-g5k4pAI9K0PSjZhqqHB6QYU',
    params=params,
    headers=headers,
    data=data,
)

print(response)
