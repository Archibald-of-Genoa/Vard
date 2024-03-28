import streamlit as st
from sso import *

if __name__ == '__main__':
    st.title("Войти через Google профиль")
    st.write(get_login_str(), unsafe_allow_html=True)

    if st.button("Текущий профиль"):
        display_user()
