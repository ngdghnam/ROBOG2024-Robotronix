import requests
import json

def Gemini(user_input:str) -> str:

    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyBbW-oad2I-g5k4pAI9K0PSjZhqqHB6QYU'

    headers = {
        'Content-Type': 'application/json',
    }

    json_data = {
        'system_instruction': 
        {
                'parts': 
                    {
                        'text': 'Answer like human speech'
                    }
        },
        'contents': [
            {
                'parts': [
                    {
                        'text': user_input
                    }
                ]
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=json_data,
    )

    json_file = json.loads(response.text)

    answer = json_file['candidates'][0]['content']['parts'][0]['text']

    return answer

text = input('Enter your text: ')
print(Gemini(text))