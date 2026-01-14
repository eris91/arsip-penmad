import streamlit as st

st.set_page_config(page_title="Arsip Penmad", layout="wide")

# === Sidebar Menu ===
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/716/716784.png", width=80)
    st.markdown("## PENMADARC")
    st.caption("Arsip Digital Seksi Penmad")
    st.write("---")

    st.page_link("app.py", label="🏠 Dashboard")
    st.page_link("pages/Arsip.py", label="📁 Arsip")  # sesuaikan nama file
    st.page_link("pages/Laporan.py", label="📊 Laporan", disabled=True)  # opsional
    st.page_link("pages/Admin.py", label="⚙️ Admin", disabled=True)      # opsional

    st.write("---")
    st.button("🔴 Logout")

# === Konten Dashboard ===
st.title("Dashboard")
st.caption("Ringkasan Arsip Penmad")

c1, c2, c3 = st.columns(3)
c1.metric("Total Arsip", "—")
c2.metric("Arsip Tahun Ini", "—")
c3.metric("Foto", "—")

st.info("Untuk melihat detail arsip kegiatan, silakan buka menu **Arsip**.")
if st.button("➡️ Buka Arsip"):
    st.switch_page("pages/Arsip.py")
