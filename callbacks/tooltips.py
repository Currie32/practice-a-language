from dash import Input, Output, callback


@callback(
    Output("tooltip-translate-language-known", "children"),
    Input("language-known", "value"),
    Input("language-learn", "value"),
)
def tooltip_translate_language_known_text(
    language_known: str, language_learn: str
) -> str:
    """
    The tooltip text for the translate-language-known icon.

    Params:
        language_known: The language that the user speaks.
        language_learn: The language that the user wants to learn.

    Returns:
        The text for the tooltip.
    """

    return f"If you type your response in {language_known}, it will automatically be translated to {language_learn}."
