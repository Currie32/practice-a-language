from dash import html, register_page


register_page(__name__, path="/about")

meta_tags = [
    {
        "name": "description",
        "content": "Practice A Language - Learn and practice languages through conversations.",
    },
]

layout = html.Div(
    id="content",
    children=[
        html.H1("About Practice a Language"),
        html.P(
            "Welcome to Practice A Language, a website to help you practice a language by having conversations. This website started from wanting to make it easier to learn a language before going on trips abroad. I became annoyed with the over-repetition of apps like Duolingo and losing track of how many times I translated “Juan come manzanas”."
        ),
        html.H2("Learn what you want faster"),
        html.P(
            "Unlike other tools that force you to learn according to their lesson plans, you can practice the conversation topics and phrases that you want, whenever you want. This control should help you to be ready for your next trip abroad much faster."
        ),
        html.H2("Practice at your level"),
        html.P(
            "You chat in either the language you’re learning or your native language. This allows experienced speakers to practice their vocabulary and grammar, while beginners can write in their native language and it will automatically be translated into the language they are learning."
        ),
        html.H2("Practice writing and speaking"),
        html.P(
            "You have the choice to practice your new language by either writing your response or recording your voice. If you record your voice, it will be transcribed so that you can see what was understood. If you want to make a change, then you can edit the text or rerecord yourself."
        ),
        html.H2("Learn from your mistakes"),
        html.P(
            "When speaking or writing in your new language, your responses are always analyzed for mistakes and will be automatically corrected. This quick feedback will help you to learn more from each conversation."
        ),
    ],
)
