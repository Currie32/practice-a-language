from typing import Dict, List, Tuple

from dash import Input, Output, State, callback, callback_context, html


@callback(
    Output("help-highlight-for-translation", "style"),
    Output("user-response-helper-icons", "style"),
    Input("conversation", "children"),
)
def display_conversation_helpers(
    conversation: List,
) -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Show helper text and icons if there is a conversation, otherwise keep them hidden.

    Params:
        conversation: The conversation between the user and OpenAI's GPT.

    Returns:
        The style value for the highlight-to-translate text
        The style value for the user-response-helper-icons div.
    """

    if conversation:
        return (
            {"display": "block"},
            {
                "display": "flex",
                "margin": "20px 0px 0px",
                "justify-content": "space-between",
            },
        )

    return {"display": "none"}, {"display": "none"}


@callback(Output("user-response", "style"), Input("conversation", "children"))
def display_user_input(conversation: List) -> Dict[str, str]:
    """
    Display the user response Input field if there is a conversation, otherwise hide it.

    params:
        conversation: The conversation between the user and OpenAI's GPT.

    returns:
        The display value for the user response Input field.
    """

    if conversation:
        return {"display": "flex"}

    return {"display": "none"}


@callback(
    Output("button-record-audio", "children"),
    Output("check-for-audio-file", "data", allow_duplicate=True),
    Input("button-record-audio", "n_clicks"),
    prevent_initial_call=True,
)
def is_user_recording_audio(button_record_audio_n_clicks: int) -> Tuple[html.I, bool]:
    """
    Change the icon for the audio recording button based on if
    a recording is taking place or not. Also, check for the audio
    recording after it has been completed.

    Params:
        button_record_audio_n_clicks: Number of times the button to record the user's audio has been clicked.

    Returns:
        The icon of the button.
        Whether to check for a file of the user's audio recording.
    """

    # Recording taking place
    if button_record_audio_n_clicks % 2 == 1:
        return html.I(className="bi bi-headphones"), False

    # Not recording right now
    else:
        return html.I(className="bi bi-mic-fill"), True


@callback(
    Output("loading", "style", allow_duplicate=True),
    Input("button-start-conversation", "n_clicks"),
    Input("button-submit-response-text", "n_clicks"),
    Input("user-response-text", "n_submit"),
    Input("button-record-audio", "n_clicks"),
    State("user-response-text", "value"),
    prevent_initial_call="initial_duplicate",
)
def loading_visible(
    button_start_conversation_n_clicks: int,
    button_submit_text_n_clicks: int,
    user_response_text_n_submits: int,
    user_response_audio_n_clicks: int,
    user_response_text: str,
) -> Dict[str, str]:
    """
    Whether to make the loading icons visible.

    Params:
        button_start_conversation_n_clicks: Number of time the start conversation button was clicked.
        button_submit_text_n_clicks: Number of times the button to submit the user's text reponse was clicked.
        user_response_text_n_submits: Number of times the user's text response was submitted (by clicking enter/return).
        user_response_audio_n_clicks: Number of times the button to record the user's audio was clicked.
        user_response_text: The text of the user_response field when it was submitted.

    Returns:
        The display status for the loading icons.
    """

    # Determine which input triggered the callback
    triggered_input_id = callback_context.triggered[0]["prop_id"].split(".")[0]

    if triggered_input_id == "button-start-conversation":
        if button_start_conversation_n_clicks:
            return {"display": "flex"}

    if triggered_input_id == "button-submit-response-text":
        if button_submit_text_n_clicks:
            return {"display": "flex"}

    elif triggered_input_id == "user-response-text":
        if user_response_text_n_submits is not None and user_response_text:
            return {"display": "flex"}

    elif triggered_input_id == "button-record-audio":
        if user_response_audio_n_clicks:
            return {"display": "flex"}

    return {"display": "none"}
