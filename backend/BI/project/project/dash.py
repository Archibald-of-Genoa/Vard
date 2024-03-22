import streamlit as st
import plotly.express as px
import plotly.subplots as sp
from mysql_conn import *
import pandas

# set page

st.set_page_config(page_title="Аналитический сервис VARD", layout="wide")
st.subheader("VARD-BI")

result = view_all_data()
df = pandas.DataFrame(result, columns=[
    "isUser", "Rating", "Name"
])

st.dataframe(df)

st.sidebar.header("Фильтры")
rating = st.sidebar.multiselect(
    "по Рейтингу:",
    options=df["Rating"].unique(),
    default=df["Rating"].unique(),
)

isuser = st.sidebar.multiselect(
    "по Статусу:",
    options=df["isUser"].unique(),
    default=df["isUser"].unique(),
)

df_filter = df.query(
    "Rating==@rating & isUser==@isuser"
)


def metrics():
    from streamlit_extras.metric_cards import style_metric_cards
    col1, col2 = st.columns(2)
    col1.metric(label="Всего пользователей:", value=df_filter.Name.count(), delta="Всего пользователей")
    col2.metric(label="Всего зарегистрировано:", value=df_filter.isUser.count(), delta="All users")
    style_metric_cards(background_color="#ffffff", border_left_color="#1f66bd")


metrics()

div1, div2 = st.columns(2)

theme_plotly = None
df = df.groupby(by=["isUser"]).size().reset_index(name="counts")
fig = px.bar(data_frame=df, x="isUser", y="counts", barmode="group")
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
