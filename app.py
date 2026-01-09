import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account

# --- KONFIGURASI ---
st.set_page_config(page_title="PENMADARC Dashboard", layout="wide")

# Load CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- FUNGSI GOOGLE DRIVE ---
def get_gdrive_service():
    info = st.secrets["gcp_service_account"]
    creds = service_account.Credentials.from_service_account_info(info)
    return build('drive', 'v3', credentials=creds)

def list_files(folder_id):
    service = get_gdrive_service()
    query = f"'{folder_id}' in parents and trashed = false"
    results = service.files().list(q=query, fields="files(id, name, createdTime, size, webViewLink)").execute()
    return results.get('files', [])

# --- HEADER (Mirip Laravel) ---
col_logo, col_title = st.columns([1, 8])
with col_title:
    st.write("MENU UTAMA")
    st.title("Dashboard / Semua Arsip")

# --- STATS CARDS (Mirip Gambar 2 Laravel Anda) ---
files = list_files("ID_FOLDER_DRIVE_ANDA")
total_arsip = len(files)
# Contoh filter sederhana untuk kategori
total_foto = sum(1 for f in files if f['name'].lower().endswith(('.png', '.jpg', '.jpeg')))

# Menampilkan Kartu Statistik secara Horizontal
st.markdown(f"""
<div class="card-container">
    <div class="metric-card">
        <h5>Total Arsip</h5>
        <h2>{total_arsip}</h2>
    </div>
    <div class="metric-card">
        <h5>Arsip Tahun Ini</h5>
        <h2>{total_arsip}</h2>
    </div>
    <div class="metric-card">
        <h5>Foto & Dokumen</h5>
        <h2>{total_foto}</h2>
    </div>
</div>
""", unsafe_allow_html=True)

# --- TOOLS (Pencarian & Tombol Tambah) ---
c1, c2, c3 = st.columns([3, 1, 1])
with c1:
    search = st.text_input("", placeholder="🔍 Cari kegiatan atau dokumen...")
with c3:
    st.write("##") # Spasi
    if st.button("➕ Tambah Arsip"):
        st.info("Fitur upload bisa ditaruh di Sidebar atau Pop-up")

# --- TABEL ARSIP (Mirip Laravel) ---
if files:
    df_data = []
    for f in files:
        df_data.append({
            "TANGGAL": f['createdTime'][:10],
            "KEGIATAN": f['name'].upper(),
            "PIC": "PETUGAS", # Bisa disesuaikan
            "AKSI": f['webViewLink']
        })
    
    df = pd.DataFrame(df_data)
    
    # Filter Pencarian
    if search:
        df = df[df['KEGIATAN'].str.contains(search.upper())]

    # Menampilkan Tabel bergaya Modern
    st.data_editor(
        df,
        column_config={
            "AKSI": st.column_config.LinkColumn("LIHAT", display_text="👁️ Lihat")
        },
        hide_index=True,
        use_container_width=True,
        disabled=True
    )
