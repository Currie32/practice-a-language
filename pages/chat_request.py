import os
import re
import requests

import openai
from tenacity import retry, wait_random_exponential, stop_after_attempt

openai.api_key = os.environ.get('OPENAI_KEY')


def get_assistant_message(messages):

    chat_response = chat_completion_request(messages)
    message_assistant = chat_response.json()["choices"][0]["message"]['content']

    # Remove space before "!" or "?"
    message_assistant = re.sub(r'\s+([!?])', r'\1', message_assistant)

    return message_assistant


@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, model="gpt-3.5-turbo-0613"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    json_data = {"model": model, "messages": messages, "temperature": 1.5}
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


def system_content(language_learn, setting, point_in_conversation="Start"):

    content = f"{point_in_conversation} a conversation about {setting} in {language_learn}. \
        Provide one statement in {language_learn}, then wait for my response. \
        Always finish your response with a question. \
        Example response: Bonjour, qu'est-ce que je peux vous servir aujourd'hui?"

    content = re.sub(r"\s+", " ", content)
    
    return content
