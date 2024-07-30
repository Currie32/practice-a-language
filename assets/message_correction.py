import os

from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential

client = OpenAI(api_key=os.environ.get("OPENAI_KEY"))


def get_corrected_message(message: str, language_learn: str) -> str:
    """
    Get and process the assistant's (OpenAI's model) message to continue the conversation.

    Params:
        message: The message from the assistant.
        language_learn: The language that the user wants to learn.

    Returns:
        The corrected message from the assistant.
    """

    message_corrected = _chat_completion_request(message, language_learn)
    if message_corrected != message:
        return message_corrected


@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def _chat_completion_request(message: str, language_learn: str) -> str:
    """
    Request a response to the user's statement from one of OpenAI's chat models.

    Params:
        messages: The conversation history between the user and the chat model.
        language_learn: The language that the user wants to learn.

    Returns:
        The corrected message from OpenAI's model.
    """

    try:
        content = f"You are an excellent {language_learn} teacher. Correct this sentence for any mistakes:\n{message}"
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=[{"role": "system", "content": content}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return e
