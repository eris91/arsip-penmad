import streamlit as st
from components.sidebar import render_sidebar

st.set_page_config(page_title="PENMADARC - Admin", layout="wide")

with open("style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_sidebar()

st.title("Admin")
st.caption("Halaman admin (placeholder).")

st.info("Nanti bisa ditambahkan: manajemen user/operator, role, pengaturan folder, dsb.")

with st.expander("Pengaturan"):
    st.text_input("Nama Instansi", "Kemenag Kab. Tasikmalaya")
    st.text_input("Unit", "Seksi Penmad")
    st.selectbox("Mode", ["Produksi", "Uji Coba"])
    st.button("Simpan")
