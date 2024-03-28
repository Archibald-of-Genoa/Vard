import mysql.connector
import streamlit

loginconn = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    passwd="",
    db="user_accounts")

conn = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    passwd="",
    db="mock")

c = conn.cursor()


def view_all_data():
    c.execute('SELECT * FROM my_dataset1')
    data = c.fetchall()
    return data


def view_all_departments():
    c.execute('SELECT rating FROM my_dataset1')
    data = c.fetchmany
    return data
