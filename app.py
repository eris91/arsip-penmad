import streamlit as st
import os
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

# --- PENGATURAN HALAMAN ---
st.set_page_config(page_title="PENMADARC Cloud", layout="wide", page_icon="📂")

# --- KONEKSI GOOGLE DRIVE ---
def get_gdrive_service():
    # Mengambil rahasia dari Streamlit Secrets (untuk Online)
    # Jika di Localhost, Anda bisa ganti dengan path file JSON Anda
    info = st.secrets["gcp_service_account"]
    creds = service_account.Credentials.from_service_account_info(info)
    return build('drive', 'v3', credentials=creds)

# --- FUNGSI AMBIL DAFTAR FILE ---
def list_files(folder_id):
    service = get_gdrive_service()
    query = f"'{folder_id}' in parents and trashed = false"
    results = service.files().list(
        q=query, fields="files(id, name, createdTime, webViewLink)").execute()
    return results.get('files', [])

# --- FUNGSI UPLOAD ---
def upload_to_drive(file, folder_id):
    service = get_gdrive_service()
    temp_path = file.name
    with open(temp_path, "wb") as f:
        f.write(file.getbuffer())

    file_metadata = {'name': file.name, 'parents': [folder_id]}
    media = MediaFileUpload(temp_path, resumable=True)
    uploaded_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    
    os.remove(temp_path) # Hapus file sementara setelah upload
    return uploaded_file.get('id')

# --- STYLE CSS ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fc; }
    .stButton>button { background-color: #4e73df; color: white; border-radius: 8px; }
    .card {
        background: white; padding: 20px; border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- KONFIGURASI ID FOLDER ---
# Ganti dengan ID folder Google Drive Anda
FOLDER_ID = "MASUKKAN_ID_FOLDER_DRIVE_ANDA_DI_SINI"

# --- TAMPILAN DASHBOARD ---
st.title("📂 PENMADARC")
st.write("Sistem Pengarsipan Digital Internal")
st.divider()

# --- INPUT UPLOAD ---
st.subheader("📤 Unggah Arsip Baru")
with st.container():
    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded_file = st.file_uploader("Pilih dokumen (PDF/JPG/PNG)", type=['pdf', 'jpg', 'png', 'docx'])
    with col2:
        st.write("##") # Spasi
        if st.button("🚀 Simpan ke Cloud"):
            if uploaded_file:
                with st.spinner('Mengunggah...'):
                    upload_to_drive(uploaded_file, FOLDER_ID)
                    st.success("File berhasil diarsip!")
                    st.rerun() # Refresh halaman agar tabel terupdate
            else:
                st.warning("Pilih file dulu!")

st.divider()

# --- TABEL DAFTAR ARSIP ---
st.subheader("📜 Daftar Arsip di Google Drive")

files = list_files(FOLDER_ID)

if files:
    # Ubah data ke format Tabel (Pandas DataFrame)
    df_data = []
    for f in files:
        df_data.append({
            "Nama Dokumen": f['name'],
            "Tanggal Upload": f['createdTime'][:10], # Ambil tanggal saja
            "Link Drive": f['webViewLink']
        })
    
    df = pd.DataFrame(df_data)
    
    # Tampilkan tabel yang bisa diklik
    st.dataframe(df, use_container_width=True)
    
    st.info(f"Total terdapat {len(files)} dokumen tersimpan.")
else:
    st.write("Belum ada dokumen di folder ini.")