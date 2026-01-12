import streamlit as st
import pandas as pd
from components.sidebar import render_sidebar

st.set_page_config(page_title="PENMADARC - Laporan", layout="wide")

with open("style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_sidebar()

st.title("Laporan")
st.caption("Contoh laporan sederhana. Nanti bisa ditarik dari Drive/Sheets.")

df = pd.DataFrame({
    "Jenis": ["Arsip Kegiatan", "Foto", "Dokumen"],
    "Jumlah": [0, 0, 0],
})

st.dataframe(df, use_container_width=True)

st.download_button(
    "Download CSV",
    df.to_csv(index=False).encode("utf-8"),
    file_name="laporan_penmadarc.csv",
    mime="text/csv"
)
