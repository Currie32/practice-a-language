import base64
import os
import re

import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import callback_context, dcc, html, Input, Output,State, callback, register_page, no_update
from dash_selectable import DashSelectable
from gtts import gTTS, lang


from deep_translator import GoogleTranslator
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

from pages.chat_request import chat_completion_request, system_content


register_page(__name__, path="")
MESSAGES = []
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
        html.Div(className='setting', children=[
            html.Div(className='setting-menu', children=[
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
            html.Div(className='setting-text', children=[
                dbc.Input(id="setting-text", placeholder="Or type a custom setting for a conversation", type="text"),
            ])
        ]),
        html.P(id='toggle-play-audio-wrapper', children=[
            html.P('Play audio of new message', id='toggle-play-audio-text'),
            daq.ToggleSwitch(id='toggle-play-audio', value=True, color='#322CA1'),
        ]),
        dbc.Button('Start a new conversation', id='button-start-conversation', n_clicks=0, disabled=True),
        html.Div(id='conversation-div', children=[
            html.P('Highlight text to see the translation.', id='help-highlight-for-translation', style={'display': 'none'}),
            # dbc.Tooltip("Highlight text to see the translation.", target="help-highlight-for-translation"),
            DashSelectable(id="conversation"),
            html.Div(id="translation"),
            html.I(className='bi bi-question-circle', id='help-translate-language-known', style={'display': 'none'}),
            html.Div(id='loading', children=[
                dbc.Spinner(color="#85b5ff", type="grow", size='sm', spinner_class_name='loading-icon'),
                dbc.Spinner(color="#85b5ff", type="grow", size='sm', spinner_class_name='loading-icon'),
                dbc.Spinner(color="#85b5ff", type="grow", size='sm', spinner_class_name='loading-icon'),
            ]),
            dbc.Tooltip(id='tooltip-translate-language-known', target="help-translate-language-known"),
            dbc.Input(id="user-input", type="text", style={"display": "none"}),
            html.Audio(id='dummy', autoPlay=True),
        ]),
    ]),
])


@callback(
    Output('tooltip-translate-language-known', 'children'),
    Input('language-known', 'value'),
    Input('language-learn', 'value'),
)
def tooltip_translate_language_known_text(language_known, language_learn):

    return f'If you type your response in {language_known}, it will automatically be translated to {language_learn}.'


@callback(
    Output('help-highlight-for-translation', 'style'),
    Output('help-translate-language-known', 'style'),
    Input('conversation', 'children'),
)
def show_conversation_help_icon(conversation):

    if conversation:
        return (
            {'display': 'block'},
            {
                'margin': '20px 0px 0px',
                'float': 'right',
            }
        )
    
    return {'display': 'none'}, {'display': 'none'}


@callback(
    Output('user-input', 'placeholder'),
    Input('language-known', 'value'),
    Input('language-learn', 'value'),
)
def user_input_placeholder(language_known, language_learn):

    if language_known and language_learn:
        return f'Type your response in {language_learn} or {language_known}'
    else:
        return 'Type your response'
    


@callback(
    Output('button-start-conversation', 'disabled'),
    Input('language-known', 'value'),
    Input('language-learn', 'value'),
    Input('conversation-setting', 'value'),
)
def start_conversation_button_disabled(known_language, learn_language, conversation_setting):
    has_two_languages = ((known_language is not None) & (learn_language is not None))
    has_different_languages = (known_language != learn_language)
    has_setting = conversation_setting is not None

    return not (has_two_languages & has_different_languages & has_setting)


@callback(
    Output('conversation-setting', 'value'),
    Output('setting-text', 'value'),
    Input('conversation-setting', 'value'),
    Input('setting-text', 'value'),
)
def conversation_settings(setting_choice, custom_setting_text):
    # Determine which input triggered the callback
    triggered_input_id = callback_context.triggered[0]['prop_id'].split('.')[0]

    if triggered_input_id == 'conversation-setting':
        if setting_choice != 'other':
            custom_setting_text = ''

    elif triggered_input_id == 'setting-text':
        if custom_setting_text:
            setting_choice = 'other'

    return setting_choice, custom_setting_text


@callback(
    Output('loading', 'style', allow_duplicate=True),
    Input('button-start-conversation', 'n_clicks'),
    Input("user-input", "n_submit"),
    State("user-input", "value"),
    prevent_initial_call='initial_duplicate',
)
def loading_visible(n_submit1, n_submit2, message_user):

    # Determine which input triggered the callback
    triggered_input_id = callback_context.triggered[0]['prop_id'].split('.')[0]

    if triggered_input_id == 'button-start-conversation':
        if n_submit1:
            return {'display': 'flex'}

    elif triggered_input_id == 'user-input':
        if n_submit2 is not None and message_user:
            return {'display': 'flex'}

    return {'display': 'none'}


@callback(
    Output('conversation', 'children', allow_duplicate=True),
    Output('loading', 'style', allow_duplicate=True),
    [Input('button-start-conversation', 'n_clicks')],
    [
        State('language-learn', 'value'),
        State('conversation-setting', 'value'),
    ],
    prevent_initial_call=True,
)
def start_conversation(n_clicks, language_learn, conversation_setting):

    # Use the global variable inside the callback
    global MESSAGES

    if n_clicks:

        MESSAGES = []
        MESSAGES.append({
            "role": "system",
            "content": system_content(language_learn, conversation_setting)
        })
        
        chat_response = chat_completion_request(MESSAGES)
        message_assistant = chat_response.json()["choices"][0]["message"]['content']
        # Remove space before "!" or "?"
        message_assistant = re.sub(r'\s+([!?])', r'\1', message_assistant)
        # message_assistant = 'Guten morgen! Wie kann ich Ihnen helfen?'
        MESSAGES.append({'role': 'assistant', 'content': message_assistant})

        conversation = [html.Div(className="message-ai-wrapper", children=[
            html.Div(className='message-ai', id='message-1', children=[message_assistant]),
            html.Div(
                html.I(className='bi bi-play-circle', id='button-play-audio'),
                id='button-message-1',
                className='button-play-audio-wrapper',
            ),
            html.Audio(id="audio-player-1", autoPlay=True),
        ])]

        return conversation, {'display': 'none'}
        

@callback(
    Output('user-input', 'style'),
    Input('conversation', 'children')
)
def display_user_input(conversation):

    if conversation:
        return {'display': 'block'}
    
    return {'display': 'none'}


@callback(
    Output("conversation", "children"),
    Output('user-input', 'value'),
    Output('loading', 'style'),
    Input("user-input", "n_submit"),
    State("user-input", "value"),
    State("conversation", "children"),
    State("language-known", "value"),
    State("language-learn", "value"),
    prevent_initial_call=True,
)
def add_to_conversation_user(n_submit, message_user, conversation, language_known, language_learn):

    # Use the global variable inside the callback
    global MESSAGES
    if n_submit is not None and message_user:

        try:
            language_detected = detect(message_user)
            if language_detected == LANGUAGES_DICT[language_known]:
                translator = GoogleTranslator(source=LANGUAGES_DICT[language_known], target=LANGUAGES_DICT[language_learn])
                message_user = translator.translate(message_user)
        except LangDetectException:
            pass

        MESSAGES.append({'role': 'user', 'content': message_user})

        conversation = conversation + [html.Div(className="message-user-wrapper", children=[
            html.Div(className='message-user', id=f'message-{len(MESSAGES)-1}', children=[message_user]),
            html.Div(
                html.I(className='bi bi-play-circle', id='button-play-audio'),
                id=f'button-message-{len(MESSAGES)-1}',
                className='button-play-audio-wrapper',
            ),
            html.Audio(id=f"audio-player-{len(MESSAGES) - 1}", autoPlay=True),
        ])]

        chat_response = chat_completion_request(MESSAGES)
        message_assistant = chat_response.json()["choices"][0]["message"]['content']
        # Remove space before "!" or "?"
        message_assistant = re.sub(r'\s+([!?])', r'\1', message_assistant)
        # message_assistant = 'Natürlich! Wissen Sie, mit welcher Busgesellschaft Sie reisen möchten?'
        MESSAGES.append({'role': 'assistant', 'content': message_assistant})

        conversation = conversation + [html.Div(className="message-ai-wrapper", children=[
            html.Div(className='message-ai', id=f'message-{len(MESSAGES)-1}', children=[message_assistant]),
            html.Div(
                html.I(className='bi bi-play-circle', id='button-play-audio'),
                id=f'button-message-{len(MESSAGES)-1}',
                className='button-play-audio-wrapper',
            ),
            html.Audio(id=f"audio-player-{len(MESSAGES) - 1}", autoPlay=True),
        ])]

        return conversation, '', {'display': 'none'}

    return no_update


@callback(
    Output('translation', 'children'),
    Input('conversation', 'selectedValue'),
    State("language-known", "value"),
    State("language-learn", "value"),
)
def find_clicked_word(text_to_translate, language_known, language_learn):

    translation = ""
    if text_to_translate:
        # text_to_translate = re.sub(r'[^A-Za-z ]', '', text_to_translate)
        translator = GoogleTranslator(source=LANGUAGES_DICT[language_learn], target=LANGUAGES_DICT[language_known])
        translation = translator.translate(text_to_translate)
        translation = f'Translation: {translation}'

    return translation


for i in range(100):
    @callback(
        Output(f'audio-player-{i+1}', 'src'),
        Input(f'button-message-{i+1}', "n_clicks"),
        State(f'conversation', 'children'),
        State("language-learn", "value"),
    )
    def convert_text_to_speech(n_clicks, text, language_learn):

        if n_clicks:

            triggered_input_id = callback_context.triggered[0]['prop_id'].split('.')[0]
            message_number_clicked = triggered_input_id.split('-')[-1]

            if message_number_clicked:
                message_number_clicked = int(message_number_clicked)
                message_clicked = text[message_number_clicked - 1]['props']['children'][0]['props']['children'][0]
                return play_audio(message_clicked, LANGUAGES_DICT[language_learn])

        return None


def play_audio(text, language):
    # Perform text-to-speech conversion using gTTS
    tts = gTTS(text, lang=language)
    # Save audio to a temporary file
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


@callback(
    Output('dummy', 'src'),
    Input('conversation', 'children'),
    State('toggle-play-audio', 'value'),
    State("language-learn", "value"),
    prevent_initial_call=True
)
def play_newest_message(text, toggle_audio, language_learn):

    if text and toggle_audio:

        return play_audio(text[-1]['props']['children'][0]['props']['children'][0], LANGUAGES_DICT[language_learn])

    return None
