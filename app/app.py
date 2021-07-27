import streamlit as st
st.set_page_config(layout="wide")
from multiapp import MultiApp
from apps import annotations, ratings_app
app = MultiApp()

app.add_app("Rating", ratings_app.app)
app.add_app("Annotations", annotations.app)

#app.add_app("Model", model.app)
app.run()
