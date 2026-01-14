import streamlit as st
import pandas as pd

st.set_page_config(page_title="Arsip Penmad Dashboard", layout="wide")

# Load CSS
try:
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Sidebar (pakai navigation sederhana)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/716/716784.png", width=80)
    st.title("ARSIP PENMAD")
    st.write("---")

    st.page_link("app.py", label="🏠 Dashboard")
    st.page_link("pages/arsip.py", label="📁 Arsip")      # sesuaikan nama file page kamu
    st.page_link("pages/laporan.py", label="📊 Laporan")  # kalau ada
    st.page_link("pages/admin.py", label="⚙️ Admin")      # kalau ada

    st.write("---")
    if st.button("🔴 Logout"):
        st.stop()

# Header
st.write("MENU UTAMA")
st.title("Dashboard / Semua Arsip")

# Dashboard stat (sementara)
col1, col2, col3 = st.columns(3)
col1.metric("Total Arsip", "—")
col2.metric("Arsip Tahun Ini", "—")
col3.metric("Foto & Dokumen", "—")

st.info("Silakan buka menu **Arsip** untuk melihat daftar arsip dan file.")

