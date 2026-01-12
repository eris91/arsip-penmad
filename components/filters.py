import streamlit as st

def ensure_filter_state():
    if "filters" not in st.session_state:
        st.session_state.filters = {
            "tahun": "Semua Tahun",
            "jenis": "Semua Jenis",
            "q": ""
        }

def render_filters(year_options: list[str]):
    """
    year_options: ["Semua Tahun", "2026", "2025", ...]
    """
    ensure_filter_state()

    jenis_opsi = ["Semua Jenis", "Foto", "Dokumen"]

    # Biar mirip UI, kita bungkus dengan container CSS
    st.markdown('<div class="filter-wrap">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1.2, 1.6, 6, 1.5])

    with c1:
        tahun = st.selectbox("", year_options, label_visibility="collapsed",
                             index=year_options.index(st.session_state.filters["tahun"]) if st.session_state.filters["tahun"] in year_options else 0)

    with c2:
        jenis = st.selectbox("", jenis_opsi, label_visibility="collapsed",
                             index=jenis_opsi.index(st.session_state.filters["jenis"]) if st.session_state.filters["jenis"] in jenis_opsi else 0)

    with c3:
        q = st.text_input("", placeholder="🔍 Cari kegiatan...", label_visibility="collapsed",
                          value=st.session_state.filters["q"])

    with c4:
        apply = st.button("🔎 Terapkan", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if apply:
        st.session_state.filters = {"tahun": tahun, "jenis": jenis, "q": q}
        st.rerun()

    return st.session_state.filters
