from dash import dcc, html


footer = html.Div(id='footer', children=[
    html.P("Practice a Language. All rights reserved."),
    html.Div("|", className="footer-pipe"),
    dcc.Link("About", href="/about"),
    html.Div("|", className="footer-pipe"),
    html.A("We're open source!", target="_blank", href="https://github.com/Currie32/practice-a-language"),
    html.Div("|", className="footer-pipe"),
    html.A(
        html.Img(src='assets/buyMeACoffee.png', alt='Link to Currie32 Buy me a Coffee page.', id="buy-me-a-coffee-logo"),
        target="_blank",
        href="https://www.buymeacoffee.com/Currie32",
    ),
    html.Div("|", className="footer-pipe"),
    html.P("david.currie32@gmail.com"),
    html.Div("|", className="footer-pipe"),
    dcc.Link("Terms", href="/terms"),
    html.Div("|", className="footer-pipe"),
    dcc.Link("Privacy Policy", href="/privacy_policy"),
])
