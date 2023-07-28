import re

import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output,State, callback, register_page
import dash.dependencies as dd
from dash_selectable import DashSelectable


from deep_translator import GoogleTranslator
translator = GoogleTranslator(source='de', target='en')

from pages.chat_request import chat_completion_request, system_content


register_page(__name__, path="")
MESSAGES = []


layout = html.Div(className='content', children=[
    html.H1(
        className='title',
        children='Practice a Language'
    ),
    html.Div(className='languages', children=[
        html.Div(className='language-menu', children=[
            dcc.Dropdown(
                ['English', 'French', 'German', 'Spanish'],
                placeholder='I speak',
                id='language-known',
                clearable=False,
            ),
        ]),
        html.Div(className='language-menu', children=[
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
            dbc.Input(id="input", placeholder="Type something...", type="text"),
        ])
    ]),
    dbc.Button('Start a new conversation', id='start-conversation-button', n_clicks=0, disabled=True),
    html.Div(id='conversation-div', children=[
        DashSelectable(id="conversation"),
        html.Div(id="translation"),
        dbc.Input(id="user-input", placeholder="Type something...", type="text", style={"display": "none"}),
        
        ],
    ),

    
    
    
    
])


@callback(
    Output('start-conversation-button', 'disabled'),
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
    Output('conversation', 'children', allow_duplicate=True),
    [Input('start-conversation-button', 'n_clicks')],
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

        content = 'English: Good morning! How can I help you?\nGerman: Guten Morgen! Wie kann ich Ihnen helfen?\nmapping: morning: Morgen, help: helfen'
        MESSAGES.append({'role': 'assistant', 'content': content})

        match = re.search(r'German:\s*(.*?)\n', content)
        assistant_message = match.group(1).strip()

        conversation = [html.Div(className='message-ai', children=[assistant_message])]
        conversation = conversation + [html.Div(className='message-user', children=['adsf we  sadfdfg wss'])]
        conversation = conversation + [html.Div(className='message-ai', children=['Natürlich! Wissen Sie, mit welcher Busgesellschaft Sie reisen möchten?'])]

        print(MESSAGES)

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
    Input("user-input", "n_submit"),
    State("user-input", "value"),
    State("conversation", "children"),
)
def add_to_conversation_user(n_submit, input_value, conversation):

    # Use the global variable inside the callback
    global MESSAGES

    if n_submit is not None:
        user_message = 'Hallo, ich möchte ein Ticket nach Berlin kaufen.'
        conversation = conversation + [html.Div(className='message-user', children=[user_message])]
        conversation = conversation + [html.Div(className='message-ai', children=['Natürlich! Wissen Sie, mit welcher Busgesellschaft Sie reisen möchten?'])]
        MESSAGES.append({'role': 'user', 'content': user_message})
        print(MESSAGES)
        return conversation


@callback(
    Output('translation', 'children'),
    Input('conversation', 'selectedValue'),
)
def find_clicked_word(text_to_translate):

    translation = ""
    if text_to_translate:
        text_to_translate = re.sub(r'[^A-Za-z ]', '', text_to_translate)
        translation = translator.translate(text_to_translate)
        translation = f'Translation: {translation}'

    return translation
