import os
import requests

import openai
from tenacity import retry, wait_random_exponential, stop_after_attempt

openai.api_key = os.environ.get('OPENAI_KEY')


@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, functions=None, function_call=None, model="gpt-3.5-turbo-0613"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    json_data = {"model": model, "messages": messages}
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


def system_content(language_known, language_learn, setting, point_in_conversation="Start"):
    
    return f"""You are a {language_learn} language teacher. {point_in_conversation} a role-playing exercise about {setting}. Provide one response, then wait for my response. Always finish your response with a question. Respond in the following format:
    {language_known}: <response-in-{language_known}>
    {language_learn}: <response-in-{language_learn}>
    """
