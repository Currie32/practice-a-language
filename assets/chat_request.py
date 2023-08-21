import os
import re
import requests
import time

import openai
from dash import callback, Input, no_update, Output
from tenacity import retry, stop_after_attempt, wait_random_exponential

openai.api_key = os.environ.get("OPENAI_KEY")


def get_assistant_message(messages):

    chat_response = chat_completion_request(messages)
    message_assistant = chat_response.json()["choices"][0]["message"]["content"]

    # Remove space before "!" or "?"
    message_assistant = re.sub(r"\s+([!?])", r"\1", message_assistant)

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
        return e


def system_content(
    language_learn, language_known, setting, point_in_conversation="Start"
):

    content = f"{point_in_conversation} a conversation about {setting} in {language_learn}. \
        Provide one statement in {language_learn}, then wait for my response. \
        Do not write in {language_known}. \
        Always finish your response with a question. \
        Example response: Bonjour, qu'est-ce que je peux vous servir aujourd'hui?"

    content = re.sub(r"\s+", " ", content)

    return content



@callback(
    Output("user-response-text", "value", allow_duplicate=True),
    Output("loading", "style", allow_duplicate=True),
    Output("check-for-audio-file", "data", allow_duplicate=True),
    Input("check-for-audio-file", "data"),
    prevent_initial_call=True,
)
def translate_recording(check_for_audio_file) -> str:
    """
    Continue the conversation by adding the user's response, then calling OpenAI
    for its response.

    Params:
        user_response_n_submits: Number of times the user response was submitted.
        message_user: The text of the user_response field when it was submitted.
        conversation: The conversation between the user and OpenAI's GPT.
        language_known: The language that the user speaks.
        language_learn: The language that the user wants to learn.

    Returns:
        The conversation with the new messages from the user and OpenAI's GPT.
        An empty string for the user response Input field.
        The new display value to hide the loading icons.
    """
    audio_recording = "recorded_audio.wav"
    while check_for_audio_file:
        if os.path.exists(audio_recording):

            # r = sr.Recognizer()
            # with sr.Microphone() as source:
            #     audio = r.listen(source)

            # print("data2", data, type(data))
            # convert_file = data.export(format="wav")
            # print("convert_file", convert_file)

            # file_name = "audio_recording.wav"
            # with open(file_name, "wb") as f:
            #     f.write(data)

            # response = requests.get(data)
            # if response.status_code == 200:
            #     with open(file_name, 'wb') as f:
            #         f.write(response.content)

            audio_file= open(audio_recording, "rb")
            os.remove(audio_recording)
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            message_user = transcript.to_dict()['text']

            # print("response", response.content)

            # message_user = r.recognize_google(response) # <- for testing since it's free
            # print("message_user", message_user)

            return message_user, {"display": "none"}, False

        time.sleep(0.1)

    return no_update
