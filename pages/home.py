import re

import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output,State, callback, register_page, no_update
import dash.dependencies as dd
from dash_selectable import DashSelectable
from gtts import gTTS
from playsound import playsound
import dash_daq as daq

from deep_translator import GoogleTranslator
from langdetect import detect

from pages.chat_request import chat_completion_request, system_content


register_page(__name__, path="")
MESSAGES = []


layout = html.Div(children=[
    html.Div(id='header', children=[
        html.H1(id='title', children='Practice a Language'),
    ]),
    html.Div(id='content', children=[
        html.Div(className='languages', children=[
            html.Div(id='language-menu-known', children=[
                dcc.Dropdown(
                    ['English', 'French', 'German', 'Spanish'],
                    placeholder='I speak',
                    id='language-known',
                    clearable=False,
                ),
            ]),
            html.Div(id='language-menu-learn', children=[
                dcc.Dropdown(
                    ['English', 'French', 'German', 'Spanish'],
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
                        'buying a bus ticket',
                        'ordering at a cafe',
                        'ordering at a restaurant',
                        'other',
                    ],
                    placeholder='Choose a setting',
                    id='conversation-setting',
                ),
            ]),
            html.Div(className='setting-text', children=[
                dbc.Input(id="setting-text", placeholder="Type a custom setting for a conversation", type="text"),
            ])
        ]),
        html.P(id='toggle-play-audio-wrapper', children=[
            html.P('Play audio of new message', id='toggle-play-audio-text'),
            daq.ToggleSwitch(id='toggle-play-audio', value=True, color='rgb(10, 108, 255)'),
        ]),
        dbc.Button('Start a new conversation', id='button-start-conversation', n_clicks=0, disabled=True),
        html.Div(id='conversation-div', children=[
            html.I(className='bi bi-exclamation-circle', id='help-highlight-for-translation', style={'display': 'none'}),
            dbc.Tooltip("Highlight text to see the translation.", target="help-highlight-for-translation"),
            DashSelectable(id="conversation"),
            html.Div(id="translation"),
            html.I(className='bi bi-exclamation-circle', id='help-translate-language-known', style={'display': 'none'}),
            dbc.Tooltip(id='tooltip-translate-language-known', target="help-translate-language-known"),
            dbc.Input(id="user-input", type="text", style={"display": "none"}),
            html.Div(id='dummy')
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
                'margin': '30px 0px 0px',
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

    # return not (has_two_languages & has_different_languages & has_setting)
    return False


@callback(
    Output('conversation-setting', 'value'),
    Output('setting-text', 'value'),
    Input('conversation-setting', 'value'),
    Input('setting-text', 'value'),
)
def conversation_settings(setting_choice, custom_setting_text):

    # Determine which input triggered the callback
    triggered_input_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    if triggered_input_id == 'conversation-setting':
        if setting_choice != 'other':
            custom_setting_text = ''

    elif triggered_input_id == 'setting-text':
        if custom_setting_text:
            setting_choice = 'other'

    return setting_choice, custom_setting_text


@callback(
    Output('conversation', 'children', allow_duplicate=True),
    [Input('button-start-conversation', 'n_clicks')],
    [
        State('language-known', 'value'),
        State('language-learn', 'value'),
        State('conversation-setting', 'value'),
    ],
    prevent_initial_call='initial_duplicate',
)
def start_conversation(n_clicks, language_known, language_learn, conversation_setting):

    # Use the global variable inside the callback
    global MESSAGES

    if n_clicks:

        MESSAGES = []
        MESSAGES.append({
            "role": "system",
            "content": system_content(language_known, language_learn, conversation_setting)
        })
        
        # chat_response = chat_completion_request(messages)
        # content = chat_response.json()["choices"][0]["message"]['content']

        message_assistant = 'Guten Morgen! Wie kann ich Ihnen helfen?'
        MESSAGES.append({'role': 'assistant', 'content': message_assistant})

        conversation = [html.Div(className="message-ai-wrapper", children=[
            html.Div(className='message-ai', id='message-1', children=[message_assistant]),
            html.Div(
                html.I(className='bi bi-play-circle', id='button-play-audio'),
                id=f'button-message-1',
                className='button-play-audio-wrapper',
            )
        ])]

        return conversation
        

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
    Input("user-input", "n_submit"),
    State("user-input", "value"),
    State("conversation", "children"),
    prevent_initial_call=True,
)
def add_to_conversation_user(n_submit, message_user, conversation):

    # Use the global variable inside the callback
    global MESSAGES

    if n_submit is not None:

        MESSAGES.append({'role': 'user', 'content': message_user})

        language_detected = detect(message_user)
        if language_detected == 'en':
            translator = GoogleTranslator(source='en', target='de')
            message_user = translator.translate(message_user)

        conversation = conversation + [html.Div(className="message-user-wrapper", children=[
            html.Div(className='message-user', id=f'message-{len(MESSAGES)-1}', children=[message_user]),
            html.Div(
                html.I(className='bi bi-play-circle', id='button-play-audio'),
                id=f'button-message-{len(MESSAGES)-1}',
                className='button-play-audio-wrapper',
            ),
        ])]

        # chat_response = chat_completion_request(messages)
        # content = chat_response.json()["choices"][0]["message"]['content']
        message_assistant = 'Natürlich! Wissen Sie, mit welcher Busgesellschaft Sie reisen möchten?'
        MESSAGES.append({'role': 'assistant', 'content': message_assistant})

        conversation = conversation + [html.Div(className="message-ai-wrapper", children=[
            html.Div(className='message-ai', id=f'message-{len(MESSAGES)-1}', children=[message_assistant]),
            html.Div(
                html.I(className='bi bi-play-circle', id='button-play-audio'),
                id=f'button-message-{len(MESSAGES)-1}',
                className='button-play-audio-wrapper',
            )
        ])]
        # print(MESSAGES)

        # user_message = 'Hallo, ich möchte ein Ticket nach Berlin kaufen.'
        # conversation = conversation + [html.Div(className='message-user', children=[user_message])]
        # conversation = conversation + [html.Div(className='message-ai', children=['Natürlich! Wissen Sie, mit welcher Busgesellschaft Sie reisen möchten?'])]
        # MESSAGES.append({'role': 'user', 'content': user_message})
        # print(MESSAGES)
        return conversation, ''


@callback(
    Output('translation', 'children'),
    Input('conversation', 'selectedValue'),
)
def find_clicked_word(text_to_translate):

    translation = ""
    if text_to_translate:
        # text_to_translate = re.sub(r'[^A-Za-z ]', '', text_to_translate)
        translator = GoogleTranslator(source='de', target='en')
        translation = translator.translate(text_to_translate)
        translation = f'Translation: {translation}'

    return translation


for i in range(2):
    @callback(
        Output(f'button-message-{i+1}', 'value'),
        Input(f'button-message-{i+1}', "n_clicks"),
        State(f'message-{i+1}', 'children'),
    )
    def convert_text_to_speech(n_clicks, text):
        if n_clicks:
            text = text[0]
            play_audio(text, 'de')

        return None


def play_audio(text, language):
    # Perform text-to-speech conversion using gTTS
    tts = gTTS(text=text, lang=language)  # Replace 'en' with the desired language code
    speech_file = 'output.mp3'
    tts.save(speech_file)
    playsound(speech_file)


@callback(
    Output('dummy', 'children', allow_duplicate=True),
    Input('conversation', 'children'),
    State('toggle-play-audio', 'value'),
    prevent_initial_call='initial_duplicate',
)
def play_newest_message(text, toggle_audio):

    if text and toggle_audio:
        play_audio(text[-1]['props']['children'][0]['props']['children'][0], 'de')
        # print("text", text)
        # print(123, text[-1]['props']['children'])

    return None
