from typing import Dict, List, Tuple

import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import (
    Input,
    Output,
    State,
    callback,
    callback_context,
    clientside_callback,
    dcc,
    html,
    no_update,
    register_page,
)
from dash_selectable import DashSelectable
from deep_translator import GoogleTranslator
from gtts import lang
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

from assets.audio import get_audio_file
from assets.chat_request import (
    convert_audio_recording_to_text,
    get_assistant_message,
    system_content,
)
from assets.message_correction import get_corrected_message
from callbacks.conversation_settings import (
    start_conversation_button_disabled,
    update_conversation_setting_values,
)
from callbacks.display_components import (
    display_conversation_helpers,
    display_user_input,
    is_user_recording_audio,
    loading_visible,
)
from callbacks.placeholder_text import user_input_placeholder
from callbacks.tooltips import tooltip_translate_language_known_text
from callbacks.translate import translate_highlighted_text


register_page(__name__, path="")
MESSAGES = []
LANGUAGES_DICT = {name: abbreviation for abbreviation, name in lang.tts_langs().items()}
LANGUAGES = sorted(LANGUAGES_DICT)  # Get just the names of the languages


layout = html.Div(
    children=[
        # Content section
        html.Div(
            id="content",
            children=[
                html.Div(
                    id="intro",
                    children=[
                        html.P(
                            children="Practice a language by having conversations about the topic of your choice."
                        ),
                    ],
                ),
                # Language selection section
                html.Div(
                    className="languages",
                    children=[
                        # Known language dropdown
                        html.Div(
                            id="language-menu-known",
                            children=[
                                dcc.Dropdown(
                                    LANGUAGES,
                                    placeholder="I speak",
                                    id="language-known",
                                    clearable=False,
                                ),
                            ],
                        ),
                        # Learn language dropdown
                        html.Div(
                            id="language-menu-learn",
                            children=[
                                dcc.Dropdown(
                                    LANGUAGES,
                                    placeholder="I want to learn",
                                    id="language-learn",
                                    clearable=False,
                                ),
                            ],
                        ),
                    ],
                ),
                # Conversation setting section
                html.Div(
                    className="conversation-setting-wrapper",
                    children=[
                        # Conversation setting dropdown
                        html.Div(
                            className="conversation-setting-menu",
                            children=[
                                dcc.Dropdown(
                                    [
                                        "a book you read",
                                        "a movie you watched",
                                        "a recent holiday",
                                        "a restaurant you went to",
                                        "asking for directions",
                                        "booking a hotel",
                                        "buying a bus ticket",
                                        "buying groceries",
                                        "cooking a meal",
                                        "favourite foods",
                                        "going to a concert",
                                        "going to a movie",
                                        "going to a restaurant",
                                        "going to a show",
                                        "hobbies",
                                        "making a dinner reservation",
                                        "meeting someone for the first time",
                                        "music",
                                        "ordering at a cafe",
                                        "ordering at a restaurant",
                                        "pets",
                                        "planning a trip",
                                        "renting a car",
                                        "shopping in a store",
                                        "weekend plans",
                                        "other",
                                    ],
                                    placeholder="Choose a topic",
                                    id="conversation-setting",
                                ),
                            ],
                        ),
                        # Custom conversation setting input
                        html.Div(
                            className="conversation-setting-custom-input",
                            children=[
                                dbc.Input(
                                    id="conversation-setting-custom",
                                    placeholder="Or type a custom topic for a conversation",
                                    type="text",
                                ),
                            ],
                        ),
                    ],
                ),
                # Toggle to play audio of new messages
                html.Div(
                    id="audio-settings",
                    children=[
                        html.Div(
                            id="toggle-play-audio-div",
                            children=[
                                html.P(
                                    "Play audio of new message",
                                    id="audio-settings-text",
                                ),
                                daq.ToggleSwitch(
                                    id="toggle-play-audio", value=True, color="#322CA1"
                                ),
                            ],
                        ),
                        html.Div(
                            id="slider-audio-speed-div",
                            children=[
                                html.P("Audio speed", id="audio-settings-text"),
                                daq.Slider(
                                    id="audio-speed",
                                    min=1,
                                    max=21,
                                    value=11,
                                    step=10,
                                    size=100,
                                    color="#322CA1",
                                ),
                            ],
                        ),
                    ],
                ),
                # Button to start a conversation
                dbc.Button(
                    "Start a new conversation",
                    id="button-start-conversation",
                    n_clicks=0,
                    disabled=True,
                ),
                # Conversation section
                html.Div(
                    id="conversation-div",
                    children=[
                        # Helper text to highlight for translation
                        html.P(
                            "Highlight text to see the translation.",
                            id="help-highlight-for-translation",
                            style={"display": "none"},
                        ),
                        # Show translated text that is highlighted
                        DashSelectable(id="conversation"),
                        html.Div(id="translation"),
                        # Icons to show when loading a new message
                        html.Div(
                            id="loading",
                            children=[
                                dbc.Spinner(
                                    color="#85b5ff",
                                    type="grow",
                                    size="sm",
                                    spinner_class_name="loading-icon",
                                ),
                                dbc.Spinner(
                                    color="#85b5ff",
                                    type="grow",
                                    size="sm",
                                    spinner_class_name="loading-icon",
                                ),
                                dbc.Spinner(
                                    color="#85b5ff",
                                    type="grow",
                                    size="sm",
                                    spinner_class_name="loading-icon",
                                ),
                            ],
                        ),
                        # Helper icons and tooltip about writing and recording user response
                        html.Div(
                            id="user-response-helper-icons",
                            children=[
                                html.Div(
                                    children=[
                                        html.I(
                                            className="bi bi-question-circle",
                                            id="help-translate-language-known",
                                        ),
                                        dbc.Tooltip(
                                            id="tooltip-translate-language-known",
                                            target="help-translate-language-known",
                                        ),
                                    ]
                                ),
                                html.Div(
                                    children=[
                                        html.I(
                                            className="bi bi-question-circle",
                                            id="help-change-microphone-setting",
                                        ),
                                        dbc.Tooltip(
                                            id="tooltip-change-microphone-setting",
                                            target="help-change-microphone-setting",
                                            children="If you are unable to record audio, you might need to change your device's microphone settings.",
                                        ),
                                    ]
                                ),
                            ],
                        ),
                        # User response section
                        html.Div(
                            id="user-response",
                            children=[
                                dbc.Textarea(id="user-response-text"),
                                html.Div(
                                    id="user-response-buttons",
                                    children=[
                                        dbc.Button(
                                            html.I(className="bi bi-mic-fill"),
                                            id="button-record-audio",
                                            n_clicks=0,
                                        ),
                                        dbc.Button(
                                            html.I(className="bi bi-arrow-return-left"),
                                            id="button-submit-response-text",
                                            n_clicks=0,
                                        ),
                                    ],
                                ),
                            ],
                            style={"display": "none"},
                        ),
                        # Boolean for when to look for the user's audio recording
                        dcc.Store(id="check-for-audio-file", data=False),
                        # Store for messages
                        dcc.Store(id="messages-store", data=[]),
                    ],
                ),
            ],
        ),
    ]
)


@callback(
    Output("conversation", "children", allow_duplicate=True),
    Output("loading", "style", allow_duplicate=True),
    Output("messages-store", "data", allow_duplicate=True),
    Input("button-start-conversation", "n_clicks"),
    State("language-known", "value"),
    State("language-learn", "value"),
    State("conversation-setting", "value"),
    State("conversation-setting-custom", "value"),
    prevent_initial_call=True,
)
def start_conversation(
    button_start_conversation_n_clicks: int,
    language_known: str,
    language_learn: str,
    conversation_setting: str,
    conversation_setting_custom: str,
) -> Tuple[List[html.Div], Dict[str, str]]:
    """
    Start the practice conversation by providing information about
    the language the user wants to practice and the setting for the conversation.

    Params:
        button_start_conversation_clicks: Number of time the start conversation button was clicked
        language_known: The language that the user speaks.
        language_learn: The language that the user wants to learn.
        conversation_setting: A conversation setting provided from the dropdown menu.
        conversation_setting_custom: A custom conversation setting provided by the user.

    Returns:
        A history of the conversation.
        The display value for the loading icons.
    """

    # Replace conversation_setting with conversation_setting_custom if it has a value
    if conversation_setting_custom:
        conversation_setting = conversation_setting_custom

    if button_start_conversation_n_clicks:
        messages = []
        messages.append(
            {
                "role": "system",
                # Provide content about the conversation for the system (OpenAI's GPT)
                "content": system_content(
                    conversation_setting,
                    language_learn,
                    language_known,
                ),
            }
        )

        # Get the first message in the conversation from OpenAI's GPT
        message_assistant = get_assistant_message(messages)
        # message_assistant = 'Guten morgen, wie kann ich ihnen helfen!' #  <- Testing message

        messages.append({"role": "assistant", "content": message_assistant})

        # Create a list to store the conversation history
        conversation = [
            html.Div(
                className="message-ai-wrapper",
                children=[
                    html.Div(
                        className="message-ai",
                        id="message-1",
                        children=[message_assistant],
                    ),
                    html.Div(
                        html.I(className="bi bi-play-circle", id="button-play-audio"),
                        id="button-message-1",
                        className="button-play-audio-wrapper",
                    ),
                    # For initial audio play
                    html.Audio(id="audio-player-0", autoPlay=True),
                    # Need two audio elements to always provide playback after conversation has been created
                    html.Audio(id=f"audio-player-1", autoPlay=True),
                    html.Audio(id=f"audio-player-2", autoPlay=True),
                ],
            )
        ]

        return conversation, {"display": "none"}, messages


@callback(
    Output("conversation", "children", allow_duplicate=True),
    Output("user-response-text", "value", allow_duplicate=True),
    Output("loading", "style", allow_duplicate=True),
    Output("messages-store", "data", allow_duplicate=True),
    Input("user-response-text", "n_submit"),
    Input("button-submit-response-text", "n_clicks"),
    State("user-response-text", "value"),
    State("conversation", "children"),
    State("language-known", "value"),
    State("language-learn", "value"),
    State("messages-store", "data"),
    prevent_initial_call="initial_duplicate",
)
def continue_conversation_text(
    user_response_n_submits: int,
    button_submit_n_clicks: int,
    message_user: str,
    conversation: List,
    language_known: str,
    language_learn: str,
    messages_store: List[Dict[str, str]],
) -> Tuple[List, str, Dict[str, str]]:
    """
    Continue the conversation by adding the user's response, then calling OpenAI
    for its response.

    Params:
        user_response_n_submits: Number of times the user response was submitted.
        button_submit_n_clicks: Number of times the button to submit the user's response was clicked.
        message_user: The text of the user_response field when it was submitted.
        conversation: The conversation between the user and OpenAI's GPT.
        language_known: The language that the user speaks.
        language_learn: The language that the user wants to learn.
        messages_store: Store of messages.

    Returns:
        The conversation with the new messages from the user and OpenAI's GPT.
        An empty string for the user response Input field.
        The new display value to hide the loading icons.
    """

    if (
        user_response_n_submits is not None or button_submit_n_clicks is not None
    ) and message_user:
        try:
            language_detected = detect(message_user)
            if language_detected == LANGUAGES_DICT[language_known]:
                translator = GoogleTranslator(
                    source=LANGUAGES_DICT[language_known],
                    target=LANGUAGES_DICT[language_learn],
                )
                message_user = translator.translate(message_user)
            else:
                message_user = get_corrected_message(message_user, language_learn)
        except LangDetectException:
            pass

        messages = messages_store.copy()
        messages.append({"role": "user", "content": message_user})
        message_new = format_new_message("user", len(messages), message_user)
        conversation = conversation + message_new

        messages_to_send = [messages[0]] + messages[1:][-5:]

        message_assistant = get_assistant_message(messages_to_send)
        # message_assistant = 'Natürlich!'  # <- testing message
        messages.append({"role": "assistant", "content": message_assistant})
        message_new = format_new_message("ai", len(messages), message_assistant)
        conversation = conversation + message_new

        return conversation, "", {"display": "none"}, messages

    return no_update


def format_new_message(
    who: str, messages_count: int, message: str, message_corrected: str = ""
) -> List[html.Div]:
    """
    Format a new message so that it is ready to be added to the conversation.

    Params:
        who: Whether the message was from the ai or user. Only valid values are "ai" and "user".
        messages_count: The number of messages in the conversation.
        message: The new message to be added to the conversation.

    Returns:
        The new message that has been formatted so that it can be viewed on the website.
    """

    return [
        html.Div(
            className=f"message-{who}-wrapper",
            children=[
                html.Div(
                    className=f"message-{who}",
                    id=f"message-{messages_count - 1}",
                    children=[message],
                ),
                html.Div(
                    className=f"message-{who}-corrected",
                    id=f"message-{messages_count - 1}-corrected",
                    children=[message_corrected],
                ),
                html.Div(
                    html.I(className="bi bi-play-circle", id="button-play-audio"),
                    id=f"button-message-{messages_count - 1}",
                    className="button-play-audio-wrapper",
                ),
                # Need two audio elements to always provide playback
                html.Audio(id=f"audio-player-1", autoPlay=True),
                html.Audio(id=f"audio-player-2", autoPlay=True),
            ],
        )
    ]


@callback(
    Output("audio-player-1", "src"),
    Input("conversation", "children"),
    State("toggle-play-audio", "value"),
    State("audio-speed", "value"),
    State("language-learn", "value"),
)
def play_newest_message(
    conversation: List, toggle_audio: bool, audio_speed: int, language_learn: str
) -> str:
    """
    Play the newest message in the conversation.

    Params:
        conversation: Contains all of the data about the conversation
        toggle_audio: Whether to play the audio of the newest message
        audio_speed: The speed of the audio
        language_learn: The language that the user wants to learn.

    Returns:
        A path to the mp3 file for the newest message.
    """

    if conversation and toggle_audio:
        newest_message = conversation[-1]["props"]["children"][0]["props"]["children"][
            0
        ]
        language_learn_abbreviation = LANGUAGES_DICT[language_learn]

        return get_audio_file(newest_message, language_learn_abbreviation, audio_speed)

    return no_update


# Loop through the messages to determine which one should have its audio played
# Use 100 as a safe upper limit. Using len(MESSAGES) didn't work
for i in range(100):

    @callback(
        Output(f"audio-player-1", "src", allow_duplicate=True),
        Output(f"audio-player-2", "src", allow_duplicate=True),
        Input(f"button-message-{i+1}", "n_clicks"),
        State(f"conversation", "children"),
        State("toggle-play-audio", "value"),
        State("audio-speed", "value"),
        State("language-learn", "value"),
        prevent_initial_call="initial_duplicate",
    )
    def play_audio_of_clicked_message(
        button_message_n_clicks: int,
        conversation: List,
        toggle_audio: bool,
        audio_speed: int,
        language_learn: str,
    ) -> str:
        """
        Play the audio of the message that had its play-audio button clicked.

        Params:
            button_message_n_clicks: The number of times the play-audio button was clicked.
            conversation: The conversation between the user and OpenAI's GPT.
            toggle_audio: Whether to play the audio of the new message
            audio_speed: The speed of the audio
            language_learn: The language that the user wants to learn.

        Returns:
            A path to the message's audio that is to be played
        """

        if button_message_n_clicks and toggle_audio:
            triggered_input_id = callback_context.triggered[0]["prop_id"].split(".")[0]
            message_number_clicked = triggered_input_id.split("-")[-1]

            if message_number_clicked:
                message_number_clicked = int(message_number_clicked)
                message_clicked = conversation[message_number_clicked - 1]["props"][
                    "children"
                ][0]["props"]["children"][0]
                language_learn_abbreviation = LANGUAGES_DICT[language_learn]

                # Rotate between audio elements so that the audio is always played
                if button_message_n_clicks % 2 == 0:
                    return (
                        get_audio_file(
                            message_clicked, language_learn_abbreviation, audio_speed
                        ),
                        "",
                    )
                else:
                    return "", get_audio_file(
                        message_clicked, language_learn_abbreviation, audio_speed
                    )

        return ("", "")


# A clientside callback to start recording the user's audio when they click on
# "button-record-audio". Need to be a clientside callback to access the user's
# microphone as dash code runs on the server side and cannot access the
# microphone after the app has been deployed to Google Cloud Run.
clientside_callback(
    """
    function (n_clicks) {
        if (n_clicks % 2 === 1) {
            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                navigator.mediaDevices.getUserMedia({ audio: true }).then(function(stream) {
                    var audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    window.mediaRecorder = new MediaRecorder(stream);
                    window.audioChunks = [];

                    window.mediaRecorder.ondataavailable = function(e) {
                        if (e.data.size > 0) {
                            window.audioChunks.push(e.data);
                        }
                    };
                    window.mediaRecorder.start();
                })
            }
        }
        return ""
    }
    """,
    Output("user-response-text", "value", allow_duplicate=True),
    Input("button-record-audio", "n_clicks"),
    prevent_initial_call=True,
)


# A clientside callback to stop the recording of the user's audio when they click on
# "button-record-audio".
clientside_callback(
    """
    function (n_clicks) {
        if (n_clicks % 2 === 0) {
            window.mediaRecorder.onstop = function() {
                var audioBlob = new Blob(window.audioChunks, { type: 'audio/wav' });
                var reader = new FileReader();
                reader.onload = function(event){
                    var base64data = event.target.result.split(',')[1];
                    fetch('/save_audio_recording', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ audio_data: base64data }),
                    });
                };
                reader.readAsDataURL(audioBlob);
            };
            window.mediaRecorder.stop();
        }
    }
    """,
    Output("user-response-text", "children"),
    Input("button-record-audio", "n_clicks"),
    prevent_initial_call=True,
)
