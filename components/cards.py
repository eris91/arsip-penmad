import streamlit as st

def render_cards(total_arsip: int, arsip_tahun_ini: int, total_foto: int):
    st.markdown(f"""
    <div class="card-container">
        <div class="metric-card">
            <h5>Total Arsip</h5>
            <h2>{total_arsip}</h2>
            <p>Jumlah folder kegiatan terarsip</p>
        </div>
        <div class="metric-card">
            <h5>Arsip Tahun Ini</h5>
            <h2>{arsip_tahun_ini}</h2>
            <p>Folder kegiatan pada tahun terpilih</p>
        </div>
        <div class="metric-card">
            <h5>Foto</h5>
            <h2>{total_foto}</h2>
            <p>Total file foto (perkiraan)</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

