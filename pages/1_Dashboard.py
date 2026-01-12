import streamlit as st
from components.sidebar import render_sidebar

st.set_page_config(page_title="PENMADARC - Dashboard", layout="wide")

# CSS global (opsional di setiap page)
with open("style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_sidebar()

st.title("Dashboard")
st.caption("Ringkasan aplikasi arsip Penmad.")

st.info("Buka menu **Arsip** untuk upload dan melihat data.")
