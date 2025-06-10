
import streamlit as st
st.set_page_config(
    page_title="College Dropout",
    layout="wide"
)
hide_deploy_button = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_deploy_button, unsafe_allow_html=True)
pg = st.navigation([st.Page("page1.py", title="College Dropout Prediction", default=True),])
pg.run()
