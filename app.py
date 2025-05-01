
import streamlit as st 


reg_page = st.Page("./pgs/registration.py", title="register", icon=":material/thumb_up:")
signin_page = st.Page("./pgs/signin.py", title="sign in", icon=":material/thumb_down:")
get_doc_page = st.Page("./pgs/get_doc.py", title="file upload", icon=":material/content_copy:")
# hub_page = st.Page("./pgs/hub.py", title="hub", icon=":material/query_stats:")
chatbot_page = st.Page("./pgs/chatbot.py", title="chatbot", icon=":material/chat:")



pg = st.navigation([reg_page, signin_page, get_doc_page, chatbot_page])



st.set_page_config(
    page_title="Ask Wakili",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.echominds.africa',
        'Report a bug': "https://www.echominds.africa",
        'About': "# Driving Impact Through Communication \nTry *Ask Wakili* and experience reality!"
    }
)


pg.run()



