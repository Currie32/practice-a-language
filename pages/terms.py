from dash import html, register_page


register_page(__name__, path="/terms")

layout = html.Div(
    id="content",
    children=[
        html.H3("TERMS AND CONDITIONS"),
        html.P(
            'These terms and conditions (the "Terms and Conditions") govern the user of www.practicealanguage.xyz (the "Site"). This Site is owned and operated by David Currie Software Development Ltd.. This Site is for helps its users to practice a language by writing and speaking.'
        ),
        html.P(
            "By using this Site, you indicate that you have read and understand these Terms and Conditions and agree to abide by them at all times."
        ),
        html.H4("Intellectual Property"),
        html.P(
            "All content published and made available on our Site is the property of David Currie Software Development Ltd. and the Site's creators. This includes, but is not limited to images, text, logos, documents, and anything that contributes to the composition of our Site."
        ),
        html.H4("Links to Other Websites"),
        html.P(
            "Our Site contains links to third party websites or services that we do not own or control. We are not responsible for the content, policies, or practices of any third party website or service linked to on our Site. It is your responsibility to read the terms and conditions and privacy policies of these third party websites before using these sites."
        ),
        html.H4("Limitation of Liability"),
        html.P(
            "David Currie Software Development Ltd. and our directors, employees, and affiliates will not be liable for any actions, claims, losses, damages, liabilities and expenses including legal fees from your use of the Site."
        ),
        html.H4("Indemnity"),
        html.P(
            "Except where prohibited by law, by using this Site you indemnify and hold harmless David Currie Software Development Ltd. and our directors, employees, and affiliates from any actions, claims, losses, damages, liabilities, and expenses including legal fees arising out of your use of our Site or your violation of these Terms and Conditions."
        ),
        html.H4("Applicable Law"),
        html.P(
            "These Terms and Conditions are governed by the laws of the Province of British Columbia."
        ),
        html.H4("Severability"),
        html.P(
            "If at any time any of the provisions set forth in these Terms and Conditions are found to be inconsistent or invalid under applicable laws, those provisions will be deemed void and will be removed from these Terms and Conditions. All other provisions will not be affected by the removal and the rest of these Terms and Conditions will still be considered valid."
        ),
        html.H4("Changes"),
        html.P(
            "These Terms and Conditions may be amended from time to time in order to maintain compliance with the law and to reflect any changes to the way we operate our Site and the way we expect users to behave on our Site."
        ),
        html.H4("Contact Details"),
        html.P(
            "Please contact us if you have any questions or concerns at: david.currie32@gmail.com"
        ),
    ],
)
