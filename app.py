from typing import Dict, List, Tuple

import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, no_update, page_container
from dash.dependencies import Input, Output, State
from flask import send_from_directory


app = Dash(
    __name__,
    use_pages=True,
    pages_folder="pages",
    external_stylesheets=[dbc.icons.BOOTSTRAP, dbc.themes.BOOTSTRAP],
)
app.config.suppress_callback_exceptions = True
server = app.server

@server.route('/robots.txt')
def serve_robots():
    return send_from_directory('.', 'robots.txt', mimetype='text/plain')


@server.route('/sitemap.xml')
def serve_sitemap():
    return send_from_directory('.', 'sitemap.xml', mimetype='application/xml')


app.layout = html.Div([
    html.Div(className='container', children=[
        page_container,
        html.Div(id='footer', children=[
            html.P("Practice a Language. All rights reserved."),
            html.P(className="footer-pipe", children=["|"]),
            html.A("We're open source!", target="_blank", href="https://github.com/Currie32/statistical_stories")
        ]),
    ])
])


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
