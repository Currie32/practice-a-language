from typing import Dict, List, Tuple

import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import callback_context, clientside_callback, dcc, html, Input, Output,State, callback, register_page, no_update
from dash_selectable import DashSelectable
from deep_translator import GoogleTranslator
from gtts import gTTS, lang
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

from assets.audio import get_audio_file
from callbacks.conversation_settings import start_conversation_button_disabled, update_conversation_setting_values
from callbacks.display_components import display_conversation_helpers, display_user_input, loading_visible
from callbacks.placeholder_text import user_input_placeholder
from callbacks.tooltips import tooltip_translate_language_known_text
from callbacks.translate import translate_highlighted_text
from pages.chat_request import get_assistant_message, system_content


register_page(__name__, path="")
MESSAGES = []
MESSAGES_COUNT = 0
LANGUAGES_DICT = {name: abbreviation for abbreviation, name in lang.tts_langs().items()}
LANGUAGES = sorted(LANGUAGES_DICT)  # Get just the names of the languages


layout = html.Div(children=[
    html.Div(id='header', children=[
        html.H1(id='title', children='Practice a Language'),
    ]),
    html.Div(id='content', children=[
        html.Div(className='languages', children=[
            html.Div(id='language-menu-known', children=[
                dcc.Dropdown(
                    LANGUAGES,
                    placeholder='I speak',
                    id='language-known',
                    clearable=False,
                ),
            ]),
            html.Div(id='language-menu-learn', children=[
                dcc.Dropdown(
                    LANGUAGES,
                    placeholder='I want to learn',
                    id='language-learn',
                    clearable=False,
                ),
            ]),
        ]),
        html.Div(className='conversation-setting-wrapper', children=[
            html.Div(className='conversation-setting-menu', children=[
                dcc.Dropdown(
                    [
                        'asking for directions',
                        'booking a hotel',
                        'buying a bus ticket',
                        'buying groceries',
                        'cooking a meal',
                        'going to a show',
                        'hobbies',
                        'making a dinner reservation',
                        'meeting someone for the first time',
                        'music',
                        'ordering at a cafe',
                        'ordering at a restaurant',
                        'pets',
                        'recent movies',
                        'renting a car',
                        'shopping in a store',
                        'weekend plans',
                        'other',
                    ],
                    placeholder='Choose a setting',
                    id='conversation-setting',
                ),
            ]),
            html.Div(className='conversation-setting-custom-input', children=[
                dbc.Input(id="conversation-setting-custom", placeholder="Or type a custom setting for a conversation", type="text"),
            ])
        ]),
        html.P(id='toggle-play-audio-wrapper', children=[
            html.P('Play audio of new message', id='toggle-play-audio-text'),
            daq.ToggleSwitch(id='toggle-play-audio', value=True, color='#322CA1'),
        ]),
        dbc.Button('Start a new conversation', id='button-start-conversation', n_clicks=0, disabled=True),
        html.Div(id='conversation-div', children=[
            html.P('Highlight text to see the translation.', id='help-highlight-for-translation', style={'display': 'none'}),
            DashSelectable(id="conversation"),
            html.Div(id="translation"),
            html.I(className='bi bi-question-circle', id='help-translate-language-known', style={'display': 'none'}),
            html.Div(id='loading', children=[
                dbc.Spinner(color="#85b5ff", type="grow", size='sm', spinner_class_name='loading-icon'),
                dbc.Spinner(color="#85b5ff", type="grow", size='sm', spinner_class_name='loading-icon'),
                dbc.Spinner(color="#85b5ff", type="grow", size='sm', spinner_class_name='loading-icon'),
            ]),
            dbc.Tooltip(id='tooltip-translate-language-known', target="help-translate-language-known"),
            dbc.Input(id="user-response", type="text", style={"display": "none"}),
        ]),
    ]),
])


@callback(
    Output('conversation', 'children', allow_duplicate=True),
    Output('loading', 'style', allow_duplicate=True),
    Input('button-start-conversation', 'n_clicks'),
    State('language-learn', 'value'),
    State('conversation-setting', 'value'),
    State('conversation-setting-custom', 'value'),
    prevent_initial_call=True,
)
def start_conversation(
    button_start_conversation_n_clicks: int,
    language_learn: str,
    conversation_setting: str,
    conversation_setting_custom: str,
) -> Tuple[List[html.Div], Dict[str, str]]:
    """
    Start the practice conversation by providing information about
    the language the user wants to practice and the setting for the conversation.

    Params:
        button_start_conversation_clicks: Number of time the start conversation button was clicked
        language_learn: The language that the user wants to learn.
        conversation_setting: A conversation setting provided from the dropdown menu.
        conversation_setting_custom: A custom conversation setting provided by the user.
    
    Returns:
        A history of the conversation.
        The display value for the loading icons.
    """

    # Use the global variables inside the callback
    global MESSAGES
    global MESSAGES_COUNT

    # Replace conversation_setting with conversation_setting_custom if it has a value
    if conversation_setting_custom:
        conversation_setting = conversation_setting_custom

    if button_start_conversation_n_clicks:

        MESSAGES = []
        MESSAGES.append({
            "role": "system",
            # Provide content about the conversation for the system (OpenAI's GPT)
            "content": system_content(language_learn, conversation_setting)
        })

        # Get the first message in the conversation from OpenAI's GPT
        message_assistant = get_assistant_message(MESSAGES)
        # message_assistant = 'Guten morgen!' #  <- Testing message
        
        MESSAGES.append({'role': 'assistant', 'content': message_assistant})
        MESSAGES_COUNT += 1

        # Create a list to store the conversation history

        conversation = [html.Div(className="message-ai-wrapper", children=[
            html.Div(className='message-ai', id='message-1', children=[message_assistant]),
            html.Div(
                html.I(className='bi bi-play-circle', id='button-play-audio'),
                id='button-message-1',
                className='button-play-audio-wrapper',
            ),
            # For initial audio play
            html.Audio(id="audio-player-0", autoPlay=True),
            # Need two audio elements to always provide playback after conversation has been created
            html.Audio(id=f"audio-player-1-1", autoPlay=True),
            html.Audio(id=f"audio-player-1-2", autoPlay=True),
        ])]

        return conversation, {'display': 'none'}


@callback(
    Output("conversation", "children"),
    Output('user-response', 'value'),
    Output('loading', 'style'),
    Input("user-response", "n_submit"),
    State("user-response", "value"),
    State("conversation", "children"),
    State("language-known", "value"),
    State("language-learn", "value"),
)
def continue_conversation(
    user_response_n_submits: int,
    message_user: str,
    conversation: List,
    language_known: str,
    language_learn: str,
) -> Tuple[List, str, Dict[str, str]]:
    """
    Continue the conversation by adding the user's response, then calling OpenAI
    for its response.

    Params:
        user_response_n_submits: Number of times the user response was submitted.
        message_user: The text of the user_response field when it was submitted.
        conversation: The conversation between the user and OpenAI's GPT.
        language_known: The language that the user speaks.
        language_learn: The language that the user wants to learn.

    Returns:
        The conversation with the new messages from the user and OpenAI's GPT.
        An empty string for the user response Input field.
        The new display value to hide the loading icons.
    """

    # Use the global variable inside the callback
    global MESSAGES
    global MESSAGES_COUNT

    if user_response_n_submits is not None and message_user:

        try:
            language_detected = detect(message_user)
            if language_detected == LANGUAGES_DICT[language_known]:
                translator = GoogleTranslator(source=LANGUAGES_DICT[language_known], target=LANGUAGES_DICT[language_learn])
                message_user = translator.translate(message_user)
        except LangDetectException:
            pass

        MESSAGES.append({'role': 'user', 'content': message_user})
        MESSAGES_COUNT += 1
        message_new = format_new_message("user", len(MESSAGES), message_user)
        conversation = conversation + message_new

        message_assistant = get_assistant_message(MESSAGES)
        # message_assistant = 'Natürlich!'  # <- testing message
        MESSAGES.append({'role': 'assistant', 'content': message_assistant})
        MESSAGES_COUNT += 1
        message_new = format_new_message("ai", len(MESSAGES), message_assistant)
        conversation = conversation + message_new

        return conversation, '', {'display': 'none'}

    return no_update


def format_new_message(who: str, messages_count: int, message: str) -> List[html.Div]:
    """
    Format a new message so that it is ready to be added to the conversation.

    Params:
        who: Whether the message was from the ai or user. Only valid values are "ai" and "user".
        messages_count: The number of messages in the conversation.
        message: The new message to be added to the conversation.

    Returns:
        The new message that has been formatted so that it can be viewed on the website.
    """

    return [html.Div(className=f"message-{who}-wrapper", children=[
        html.Div(className=f'message-{who}', id=f'message-{messages_count - 1}', children=[message]),
        html.Div(
            html.I(className='bi bi-play-circle', id='button-play-audio'),
            id=f'button-message-{messages_count - 1}',
            className='button-play-audio-wrapper',
        ),
        # Need two audio elements to always provide playback
        html.Audio(id=f"audio-player-{messages_count - 1}-1", autoPlay=True),
        html.Audio(id=f"audio-player-{messages_count - 1}-2", autoPlay=True),
    ])]


@callback(
    Output('audio-player-0', 'src'),
    Input('conversation', 'children'),
    State('toggle-play-audio', 'value'),
    State("language-learn", "value"),
)
def play_newest_message(conversation: List, toggle_audio: bool, language_learn: str) -> str:
    """
    Play the newest message in the conversation.

    Params:
        conversation: Contains all of the data about the conversation
        toggle_audio: Whether to play the audio of the newest message
        language_learn: The language that the user wants to learn.

    Returns:
        A path to the mp3 file for the newest message.
    """

    if conversation and toggle_audio:

        newest_message = conversation[-1]['props']['children'][0]['props']['children'][0]
        language_learn_abbreviation = LANGUAGES_DICT[language_learn]

        return get_audio_file(newest_message, language_learn_abbreviation)

    return no_update


# Loop through the messages to determine which one should have its audio played
for i in range(100):
    @callback(
        Output(f'audio-player-{i+1}-1', 'src'),
        Output(f'audio-player-{i+1}-2', 'src'),
        Input(f'button-message-{i+1}', "n_clicks"),
        State(f'conversation', 'children'),
        State("language-learn", "value"),
    )
    def play_audio_of_clicked_message(
        button_message_n_clicks: int,
        conversation: List,
        language_learn: str,
    ) -> str:
        """
        Play the audio of the message that had its play-audio button clicked.

        Params:
            button_message_n_clicks: The number of times the play-audio button was clicked.
            conversation: The conversation between the user and OpenAI's GPT.
            language_learn: The language that the user wants to learn.

        Returns:
            A path to the message's audio that is to be played
        """

        if button_message_n_clicks:

            triggered_input_id = callback_context.triggered[0]['prop_id'].split('.')[0]
            message_number_clicked = triggered_input_id.split('-')[-1]

            if message_number_clicked:
                message_number_clicked = int(message_number_clicked)
                message_clicked = conversation[message_number_clicked - 1]['props']['children'][0]['props']['children'][0]
                language_learn_abbreviation = LANGUAGES_DICT[language_learn]

                # Rotate between audio elements so that the audio is always played
                if button_message_n_clicks % 2 == 0:
                    return get_audio_file(message_clicked, language_learn_abbreviation), ""
                else:
                    return "", get_audio_file(message_clicked, language_learn_abbreviation)

        return "", "",
