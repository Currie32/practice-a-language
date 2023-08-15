import base64
import os

from gtts import gTTS


def get_audio_file(text: str, language: str) -> str:
    """
    Create and return an mp3 file that contains the audio
    for a message to be played in the desired language's accent.

    Params:
        text: The text for the audio
        language: The language for the accent of the audio

    Returns:
        A path to the mp3 file
    """

    # Perform text-to-speech conversion
    tts = gTTS(text, lang=language)
    audio_path = 'temp_audio.mp3'
    tts.save(audio_path)
    
    # Read and encode the audio file
    with open(audio_path, 'rb') as audio_file:
        audio_data = audio_file.read()
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        audio_src = f"data:audio/mpeg;base64,{audio_base64}"
    
    # Delete the temporary audio file
    os.remove(audio_path)
    
    return audio_src
