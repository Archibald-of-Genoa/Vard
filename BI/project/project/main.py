from pages.user import login
from sso import *
from mysql_conn import *
import streamlit as st

headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
logOutSection = st.container()


def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False


def show_logout_page():
    loginSection.empty()
    with logOutSection:
        st.button("Log Out", key="logout", on_click=LoggedOut_Clicked)


def LoggedIn_Clicked(userName, password):
    if login(userName, password):
        st.session_state['loggedIn'] = True
    else:
        st.session_state['loggedIn'] = False
        st.error("Invalid user name or password")


def show_login_page():
    with loginSection:
        if not st.session_state['loggedIn']:
            st.title("Войти через Google профиль:")
            st.write(get_login_str(), unsafe_allow_html=True)
            if st.button("Текущий профиль"):
                display_user()
            st.title("Войти через почту:")
            username = st.text_input("Enter your user name")
            password = st.text_input("Enter password", type="password")
            if st.button("Login"):
                cursor = loginconn.cursor()
                query = "SELECT * FROM users WHERE username = %s AND password = %s"
                values = (username, password)
                cursor.execute(query, values)
                record = cursor.fetchone()
                if record:
                    st.success("Logged in as {}".format(username))
                    st.session_state['loggedIn'] = True
                else:
                    st.warning("Incorrect username or password")


with headerSection:
    st.title("VARD-BI")
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        show_login_page()
    else:
        if st.session_state['loggedIn']:
            show_logout_page()
        else:
            show_login_page()
