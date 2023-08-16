from typing import Dict, List, Tuple

from dash import Input, Output, State, callback, callback_context


@callback(
    Output("help-highlight-for-translation", "style"),
    Output("help-translate-language-known", "style"),
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
        The style value for the translate-language-known icon.
    """

    if conversation:
        return (
            {"display": "block"},
            {
                "margin": "20px 0px 0px",
                "float": "right",
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
        return {"display": "block"}

    return {"display": "none"}


@callback(
    Output("loading", "style", allow_duplicate=True),
    Input("button-start-conversation", "n_clicks"),
    Input("user-response", "n_submit"),
    State("user-response", "value"),
    prevent_initial_call="initial_duplicate",
)
def loading_visible(
    button_start_conversation_n_clicks: int,
    user_response_n_submits: int,
    user_response_text: str,
) -> Dict[str, str]:
    """
    Whether to make the loading icons visible.

    Params:
        button_start_conversation_clicks: Number of time the start conversation button was clicked
        user_response_n_submits: Number of times the user response was submitted.
        user_response_text: The text of the user_response field when it was submitted.

    Returns:
        The display status for the loading icons.
    """

    # Determine which input triggered the callback
    triggered_input_id = callback_context.triggered[0]["prop_id"].split(".")[0]

    if triggered_input_id == "button-start-conversation":
        if button_start_conversation_n_clicks:
            return {"display": "flex"}

    elif triggered_input_id == "user-response":
        if user_response_n_submits is not None and user_response_text:
            return {"display": "flex"}

    return {"display": "none"}
