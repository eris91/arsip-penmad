import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/716/716784.png", width=70)
        st.markdown("## ADP")
        st.caption("Arsip Digital Penmad")

        st.divider()

        # Streamlit multipage otomatis sudah ada di sidebar,
        # tombol manual di sini opsional saja.
        st.markdown("### Menu")
        st.page_link("pages/1_Dashboard.py", label="🏠 Dashboard")
        st.page_link("pages/2_Arsip.py", label="🗂️ Arsip")
        st.page_link("pages/3_Laporan.py", label="📊 Laporan")
        st.page_link("pages/4_Admin.py", label="⚙️ Admin")

        st.divider()

        if st.button("🔴 Logout"):
            # Placeholder (untuk nanti kalau ada auth)
            st.warning("Logout (demo).")
            st.stop()


