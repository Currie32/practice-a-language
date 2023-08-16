from dash import Input, Output, State, callback
from deep_translator import GoogleTranslator
from gtts import lang

LANGUAGES_DICT = {name: abbreviation for abbreviation, name in lang.tts_langs().items()}


@callback(
    Output("translation", "children"),
    Input("conversation", "selectedValue"),
    State("language-known", "value"),
    State("language-learn", "value"),
)
def translate_highlighted_text(
    text_to_translate: str, language_known: str, language_learn: str
) -> str:
    """
    Translate any highlighted text from the language the user wants to learn
    to the language the user knows.

    Params:
        text_to_translate: the highlighted text that will be translated.
        language_known: The language that the user speaks.
        language_learn: The language that the user wants to learn.

    Returns:
        A translation of the highlighted text.
    """

    translation = ""
    if text_to_translate:
        language_learn_abbreviation = LANGUAGES_DICT[language_learn]
        language_known_abbreviation = LANGUAGES_DICT[language_known]
        translator = GoogleTranslator(
            source=language_learn_abbreviation, target=language_known_abbreviation
        )
        translation = translator.translate(text_to_translate)
        translation = f"Translation: {translation}"

    return translation
