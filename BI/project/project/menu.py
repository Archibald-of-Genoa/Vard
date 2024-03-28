from sso import *
from mysql_conn import *
from httpx_oauth.clients.google import GoogleOAuth2
import streamlit as st

REDIRECT_URI = os.environ['REDIRECT_URI']


def authenticated_menu():
    # Show a navigation menu for authenticated users
    if st.session_state['loggedIn']:
        st.sidebar.page_link("menuentry.py", label="Switch accounts")
        st.sidebar.page_link("pages/dash.py", label="Dashboard")
        if st.session_state.role in ["admin", "super-admin"]:
            st.sidebar.page_link("pages/admin.py", label="Manage users")
            st.sidebar.page_link(
                "pages/super-admin.py",
                label="Manage admin access",
                disabled=st.session_state.role != "super-admin",
            )


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    client: GoogleOAuth2 = GoogleOAuth2(CLIENT_ID, CLIENT_SECRET)
    code = st.query_params.get_all('code')
    googletoken = get_access_token(client, REDIRECT_URI, code)
    if googletoken:
        st.session_state['loggedIn'] = True
        authenticated_menu()
    st.sidebar.page_link("menuentry.py", label="Log in")
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
            authenticated_menu()
        else:
            st.warning("Incorrect username or password")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "role" not in st.session_state or st.session_state.role is None or not st.session_state['loggedIn']:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        st.switch_page("menuentry.py")
    menu()
