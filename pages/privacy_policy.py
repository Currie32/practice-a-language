from dash import html, register_page


register_page(__name__, path="/privacy_policy")

layout = html.Div(
    id="content",
    children=[
        html.H3("Practice a Language Privacy Policy"),
        html.P("Type of website: Practice a language by speaking and writing"),
        html.P("Effective date: November 14th, 2023"),
        html.P(
            'www.practicealanguage.xyz (the "Site") is owned and operated by David Currie Software Development Ltd.. David Currie Software Development Ltd. is the data controller and can be contacted at: david.currie32@gmail.com'
        ),
        html.H4("Purpose"),
        html.P(
            'The purpose of this privacy policy (this "Privacy Policy") is to inform users of our Site of the following:'
        ),
        html.P("1. The personal data we will collect;"),
        html.P("2. Use of collected data;"),
        html.P("3. Who has access to the data collected;"),
        html.P("4. The rights of Site users; and"),
        html.P("5. The Site's cookie policy."),
        html.P(
            "This Privacy Policy applies in addition to the terms and conditions of our Site."
        ),
        html.H4("GDPR"),
        html.P(
            'For users in the European Union, we adhere to the Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016, known as the General Data Protection Regulation (the "GDPR"). For users in the United Kingdom, we adhere to the GDPR as enshrined in the Data Protection Act 2018.'
        ),
        html.H4("Constent"),
        html.P("By using our Site users agree that they consent to:"),
        html.P("1. The conditions set out in this Privacy Policy."),
        html.P(
            "When the legal basis for us processing your personal data is that you have provided your consent to that processing, you may withdraw your consent at any time. If you withdraw your consent, it will not make processing which we completed before you withdrew your consent unlawful."
        ),
        html.P(
            "You can withdraw your consent by emailing us at david.currie32@gmail.com."
        ),
        html.H4("Legal Basis for Processing"),
        html.P(
            "We collect and process personal data about users in the EU only when we have a legal basis for doing so under Article 6 of the GDPR."
        ),
        html.P(
            "We rely on the following legal basis to collect and process the personal data of users in the EU:"
        ),
        html.P(
            "1. Users have provided their consent to the processing of their data for one or more specific purposes."
        ),
        html.H4("Personal Data We Collect"),
        html.P(
            "We only collect data that helps us achieve the purpose set out in this Privacy Policy. We will not collect any additional data beyond the data listed below without notifying you first."
        ),
        html.H4("Data Collected Automatically"),
        html.P(
            "When you visit and use our Site, we may automatically collect and store the following information:"
        ),
        html.P("1. IP address;"),
        html.P("2. Location"),
        html.P("3. Hardware and software details; and"),
        html.P("4. Clicked links."),
        html.H4("Data Collected in a Non-Automatic Way"),
        html.P(
            "We may also collect the following data when you perform certain functions on our Site:"
        ),
        html.P("1. Choose a conversation setting for practicing."),
        html.P("This data may be collected using the following methods:"),
        html.P("1. With an API call, then stored in our database."),
        html.H4("How We Use Personal Data"),
        html.P(
            "Data collected on our Site will only be used for the purposes specified in this Privacy Policy or indicated on the relevant pages of our Site. We will not use your data beyond what we disclose in this Privacy Policy."
        ),
        html.P("The data we collect automatically is used for the following purposes:"),
        html.P("1. Providing more relevant ads using Google Adsense."),
        html.P(
            "The data we collect when the user performs certain functions may be used for the following purposes:"
        ),
        html.P("1. To add more default conversation settings to the Site."),
        html.H4("Who We Share Personal Data With"),
        html.H5("Employees"),
        html.P(
            "We may disclose user data to any member of our organization who reasonably needs access to user data to achieve the purposes set out in this Privacy Policy."
        ),
        html.H5("Third Parties"),
        html.P("We may share user data with the following third parties:"),
        html.P("1. Google Adsense."),
        html.P("We may share the follwoing user data with third parties:"),
        html.P(
            "1. User IP addresses, browsing histories, website preferences, device location and device preferences."
        ),
        html.P("We may share user data with third parties for the following purposes:"),
        html.P("1. Targeted advertising."),
        html.P(
            "Third parties will not be able to access user data beyond what is reasonably necessary to achieve the given purpose."
        ),
        html.H5("Other Disclosures"),
        html.P(
            "We will not sell or share your data with other third parties, except in the following cases:"
        ),
        html.P("1. If the law requries it;"),
        html.P("2. If it is required for any legal proceeding;"),
        html.P("3. To prove or protect our legal rights; and"),
        html.P(
            "4. To buyers or potential buyers of this company in the event that we seek to sell the company."
        ),
        html.P(
            "If you follow hyperlinks from our Site to another site, please note that we are not responsible for and have no control over their privacy policies and practices."
        ),
        html.H4("How Long We Store Personal Data"),
        html.P(
            "User data will be stored until the purpose the data was collected for has been achieved."
        ),
        html.P(
            "You will be notified if your data is kept for longer than this period."
        ),
        html.H4("How We Protect Your Personal Data"),
        html.P(
            "The company will use products developed and provided by Google to store personal data."
        ),
        html.P(
            "While we take all reasonable precautions to ensure that user data is secure and that users are protected, there always remains the risk of harm. The Internet as a whole can be insecure at times and therefore we are unable to guarantee the security of user data beyond what is reasonably practical."
        ),
        html.H4("Your Rights as a User"),
        html.P("Under the GDPR, you have the following rights:"),
        html.P("1. Right to be informed;"),
        html.P("2. Right of access;"),
        html.P("3. Right to rectification;"),
        html.P("4. Right to erasure;"),
        html.P("5. Right to restrict processing;"),
        html.P("6. Right to data protability; and"),
        html.P("7. Right to object."),
        html.H4("Children"),
        html.P(
            "We do not knowingly collect or use personal data from children under 16 years of age. If we learn that we have collected personal data from a child under 16 years of age, the personal data will be deleted as soon as possible. If a child under 16 years of age has provided us with personal data their parent or guardian may contact the company."
        ),
        html.H4("How to Access, Modify, Delete, or Challenge the Data Collected"),
        html.P(
            "If you would like to know if we have collected your personal data, how we have used your personal data, if we have disclosed your personal data and to who we disclosed your personal data, if you would like your data to be deleted or modified in any way, or if you would like to exercise any of your other rights under the GDPR, please contact us at: david.currie32@gmail.com"
        ),
        html.H4("How to Opt-Out of Data Collection, Use or Disclosure"),
        html.P(
            "In addition to the method(s) described in the How to Access, Modify, Delete, or Challenge the Data Collected section, we provide the following specific opt-out methods for the forms of collection, use, or disclosure of your personal data:"
        ),
        html.P(
            "1. All collected data. You can opt-out by selecting that they do not consent to their data being collected."
        ),
        html.H4("Cookie Policy"),
        html.P(
            "A cookie is a small file, stored on a user's hard drive by a website. Its purpose is to collect data relating to the user's browsing habits. You can choose to be notified each time a cookie is transmitted. You can also choose to disable cookies entirely in your internet browser, but this may decrease the quality of your user experience."
        ),
        html.P("We use the following types of cookies on our Site:"),
        html.H5("1. Third-Party Cookies"),
        html.P(
            "Third-party cookies are created by a website other than ours. We may use third-party cookies to achieve the following purposes:"
        ),
        html.P(
            "1. Monitor user preferences to tailor advertisements around their interests."
        ),
        html.H4("Modifications"),
        html.P(
            'This Privacy Policy may be amended from time to time in order to maintain compliance with the law and to reflect any changes to our data collection process. When we amend this Privacy Policy we will update the "Effective Date" at the top of this Privacy Policy. We recommend that our users periodically review our Privacy Policy to ensure that they are notified of any updates. If necessary, we may notify users by email of changes to this Privacy Policy.'
        ),
        html.H4("Complaints"),
        html.P(
            "If you have any complaints about how we process your personal data, please contact us through the contact methods listed in the Contact Information section so that we can, where possible, resolve the issue. If you feel we have not addressed your concern in a satisfactory manner you may contact a supervisory authority. You also have the right to directly make a complaint to a supervisory authority. You can lodge a complaint with a supervisory authority by contacting the Information Commissioner's Office in the UK, Data Protection Commission in Ireland."
        ),
        html.H4("Contact Information"),
        html.P(
            "If you have any questions, concerns, or complaints, you can contact us at: david.currie32@gmail.com"
        ),
    ],
)
