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
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-THNE3MSS49"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());

            gtag('config', 'G-THNE3MSS49');
        </script>
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
                page_container,
                footer,
            ],
        )
    ],
)


@server.route("/save_audio_recording", methods=["POST"])
def save_audio_recording():
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
