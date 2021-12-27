import streamlit as st
import requests
import pandas as pd
import altair as alt
import numpy as np
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import locale
from locale import atof, setlocale, LC_NUMERIC
import pymongo
URI = "mongodb+srv://admin:admin@covidapp.j3vg0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(URI)

db = client["covid-database"]
df = db.Iris
df = pd.DataFrame(list(df.find()))


df.drop('_id', inplace=True, axis=1)
df2 = df.set_index('Countries')
df2.index.names = [None]

st.markdown("""
    <style>
    .reportview-container {
        background: url("https://www.youngmoorelaw.com/wp-content/uploads/2020/04/Covid-4shutterstock_1654034092.jpg")
    }
   .sidebar .sidebar-content {
        background: url("")
    }
    </style>
    """,
            unsafe_allow_html=True
            )

add_selectbox = st.sidebar.selectbox(
    'Select what to view',
    ('Welcome', 'Raw data', 'Plots', 'Maps')
)

if add_selectbox == 'Welcome':
    st.title("WELCOME TO Covid bot tracker")

if add_selectbox == 'Raw data':
    st.title("Raw DataFrame")
    st.text("dataframe head")
    st.dataframe(df2.head())
    user_input = st.text_input("Search a specific Country", "")
    if st.button("Search"):
        st.dataframe(df.loc[df['Countries'] == user_input])

    if st.button("Show All countries"):
        st.dataframe(df2)

if add_selectbox == 'Plots':
    st.title("Plots")
    st.bar_chart(df2.head())
    c = alt.Chart(df.head()).mark_bar().encode(
        x='Countries',
        y='Total Cases',

    )
    st.altair_chart(c, use_container_width=True)

    st.markdown("""
    <iframe style="background: #21313C;border: none;border-radius: 2px;box-shadow: 0 2px 10px 0 rgba(70, 76, 79, .2);" width="640" height="480" src="https://charts.mongodb.com/charts-e-shop-mhnfu/embed/charts?id=15800df9-8c31-40b7-85c4-be096152776f&maxDataAge=3600&theme=dark&autoRefresh=true">
    </iframe>
    """, unsafe_allow_html=True)

    st.markdown("""
    <iframe style="background: #21313C;border: none;border-radius: 2px;box-shadow: 0 2px 10px 0 rgba(70, 76, 79, .2);" width="640" height="480" src="https://charts.mongodb.com/charts-e-shop-mhnfu/embed/charts?id=26af633d-2d92-42f2-899f-66979962693d&maxDataAge=3600&theme=dark&autoRefresh=true">
    </iframe>
    """, unsafe_allow_html=True)

if add_selectbox == 'Maps':
    st.title("Maps")
    st.markdown("""
        <iframe style="background: #21313C;border: none;border-radius: 2px;box-shadow: 0 2px 10px 0 rgba(70, 76, 79, .2);" width="640" height="480" src="https://charts.mongodb.com/charts-e-shop-mhnfu/embed/charts?id=fe31b2f8-39cf-4886-8761-6768dd1dc0e2&maxDataAge=3600&theme=dark&autoRefresh=true">
        </iframe>
        """, unsafe_allow_html=True)