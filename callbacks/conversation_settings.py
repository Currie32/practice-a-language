from typing import Tuple

from dash import Input, Output, State, callback, callback_context


@callback(
    Output("button-start-conversation", "disabled"),
    Input("language-known", "value"),
    Input("language-learn", "value"),
    Input("conversation-setting", "value"),
    State("conversation-setting-custom", "value"),
)
def start_conversation_button_disabled(
    language_known: str,
    language_learn: str,
    conversation_setting: str,
    conversation_setting_custom: str,
) -> bool:
    """
    Whether to disable the start conversation button based on the values in the required fields.

    Params:
        language_known: The language that the user speaks.
        language_learn: The language that the user wants to learn.
        conversation_setting: A conversation setting provided from the dropdown menu.
        conversation_setting_custom: A custom conversation setting provided by the user.

    Returns:
        True if the conversation button should be disabled, otherwise False.
    """
    has_two_languages = (language_known is not None) & (language_learn is not None)
    has_different_languages = language_known != language_learn

    has_setting = (
        (conversation_setting == "other") & (conversation_setting_custom is not None)
    ) | ((conversation_setting != "other") & (conversation_setting is not None))

    return not (has_two_languages & has_different_languages & has_setting)


@callback(
    Output("conversation-setting", "value"),
    Output("conversation-setting-custom", "value"),
    Input("conversation-setting", "value"),
    Input("conversation-setting-custom", "value"),
)
def update_conversation_setting_values(
    conversation_setting: str,
    conversation_setting_custom: str,
) -> Tuple[str, str]:
    """
    Update the value of a conversation setting based on the new value
    for the other setting.

    Params:
        conversation_setting: A conversation setting provided from the dropdown menu.
        conversation_setting_custom: A custom conversation setting provided by the user.

    Returns:
        The updated values for conversation_setting and conversation_setting_custom.
    """

    # Determine which input triggered the callback
    triggered_input_id = callback_context.triggered[0]["prop_id"].split(".")[0]

    # Reset conversation_setting_custom when conversation_setting changes to something other than 'other'
    if triggered_input_id == "conversation-setting":
        if conversation_setting != "other":
            conversation_setting_custom = ""

    # If a value is provided for conversation_setting_custom, change conversation_setting to 'other'
    elif triggered_input_id == "conversation-setting-custom":
        if conversation_setting_custom:
            conversation_setting = "other"

    return conversation_setting, conversation_setting_custom
