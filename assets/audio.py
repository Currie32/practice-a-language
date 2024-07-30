import base64

from gtts import gTTS
from pydub import AudioSegment


def get_audio_file(text: str, language: str, playback_speed: float) -> str:
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
    audio_path = "temp_audio.mp3"
    tts.save(audio_path)

    # Create a new audio segment with adjusted speed
    audio = AudioSegment.from_file(audio_path)
    playback_speed = 1 + (playback_speed / 100)
    adjusted_audio = audio.speedup(playback_speed=playback_speed)

    # Save the adjusted audio to a new file
    adjusted_audio_file = f"adjusted_audio.mp3"
    adjusted_audio.export(adjusted_audio_file, format="mp3")

    with open(adjusted_audio_file, "rb") as audio_file:
        audio_data = audio_file.read()
        audio_base64 = base64.b64encode(audio_data).decode("utf-8")
        audio_src = f"data:audio/mpeg;base64,{audio_base64}"

        return audio_src
