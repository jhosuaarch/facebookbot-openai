import json
import openai

openai.api_key = json.load(open('config.json'))['openai_api_key']


async def response(message):
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message}
        ]
    )
    return res.choices[0].message.content
