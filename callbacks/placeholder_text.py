from dash import callback, Input, Output


@callback(
    Output('user-response', 'placeholder'),
    Input('language-known', 'value'),
    Input('language-learn', 'value'),
)
def user_input_placeholder(language_known: str, language_learn: str) -> str:
    """
    Set the placeholder text for the user response Input field.

    Params:
        language_known: The language that the user speaks.
        language_learn: The language that the user wants to learn.

    Returns:
        Placeholder text for the user reponse Input field.
    """

    if language_known and language_learn:
        return f'Type your response in {language_learn} or {language_known}'
    else:
        return 'Type your response'