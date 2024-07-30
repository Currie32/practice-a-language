import base64
import io

import dash_bootstrap_components as dbc
from dash import Dash, html, page_container
from flask import Flask, request, send_from_directory

from footer import footer

server = Flask(__name__)
app = Dash(
    __name__,
    use_pages=True,
    pages_folder="pages",
    external_stylesheets=[dbc.icons.BOOTSTRAP, dbc.themes.BOOTSTRAP],
    server=server,
)
app.config.suppress_callback_exceptions = True


@server.route("/robots.txt")
def serve_robots():
    return send_from_directory(".", "robots.txt", mimetype="text/plain")


@server.route("/sitemap.xml")
def serve_sitemap():
    return send_from_directory(".", "sitemap.xml", mimetype="application/xml")


app.index_string = """<!DOCTYPE html>
<html lang="en">
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-THNE3MSS49"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());

            gtag('config', 'G-THNE3MSS49');
        </script>
        <meta charset="UTF-8">
        <meta name="description" content="Practice a language by having conversations about the topic of your choice.">
        <meta property="og:title" content="Practice a Language">
        <meta property="og:description" content="Practice a language by having conversations about the topic of your choice.">
        <meta property="og:image" content="https://practicealanguage.xyz/assets/favicon.ico">
        <meta property="og:url" content="https://practicealanguage.xyz">
        <meta name="twitter:card" content="https://practicealanguage.xyz/assets/favicon.ico">
        <meta name="twitter:title" content="Practice a Language">
        <meta name="twitter:description" content="Practice speaking and writing in a foreign language.">
        <meta name="twitter:image" content="https://practicealanguage.xyz/assets/favicon.ico">
        <meta name="google-adsense-account" content="ca-pub-4657073290295216">
        <link rel="canonical" href="https://practicealanguage.xyz">
        <meta name="robots" content="index, follow">
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""

app.layout = html.Div(
    [
        html.Div(
            className="container",
            children=[
                html.Div(
                    id="header",
                    children=[
                        html.H1(id="title", children="Practice a Language"),
                    ],
                ),
                page_container,
                footer,
            ],
        )
    ],
)


@server.route("/save_audio_recording", methods=["POST"])
def save_audio_recording():
    """
    Save the audio that the user has recorded so that it can be sent
    to OpenAI's Whisper-1 API.
    """
    try:
        data = request.get_json()
        audio_data = data["audio_data"]
        # Decode the Base64 audio data
        audio_bytes = base64.b64decode(audio_data)

        # Save the audio recording
        with io.BytesIO(audio_bytes) as f:
            with open("audio_recording.wav", "wb") as audio_file:
                audio_file.write(f.read())

        return "Audio data received successfully", 200

    except Exception:
        return "An error occurred", 500


if __name__ == "__main__":
    app.run_server(debug=True, port=8080)
