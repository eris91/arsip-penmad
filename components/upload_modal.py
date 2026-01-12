import streamlit as st
from datetime import date
from services.gdrive import (
    get_service, get_or_create_folder, upload_file, upload_text
)
from services.utils import make_activity_folder_name, safe_text

def ensure_upload_state():
    if "open_upload" not in st.session_state:
        st.session_state.open_upload = False

def open_upload_modal_button():
    ensure_upload_state()
    if st.button("➕ Tambah Arsip", type="primary", use_container_width=True):
        st.session_state.open_upload = True
        st.rerun()

def render_upload_modal():
    ensure_upload_state()
    if not st.session_state.open_upload:
        return

    @st.dialog("Tambah Arsip")
    def modal():
        cA, cB = st.columns(2)
        with cA:
            tgl = st.date_input("TANGGAL", value=date.today())
        with cB:
            pic = st.text_input("PIC", value="Eris", help="Bisa otomatis dari login (nanti).")

        nama_kegiatan = st.text_input("NAMA KEGIATAN", placeholder="Judul kegiatan")
        deskripsi = st.text_area("DESKRIPSI KEGIATAN (Opsional)", placeholder="Keterangan singkat...")
        link_video = st.text_input("LINK VIDEO (YouTube/Drive)", placeholder="https://...")

        u1, u2 = st.columns(2)
        with u1:
            foto_files = st.file_uploader("UPLOAD FOTO", type=["jpg","jpeg","png"], accept_multiple_files=True)
        with u2:
            dok_files = st.file_uploader("UPLOAD DOKUMEN", type=["pdf","docx","xlsx","zip","rar"], accept_multiple_files=True)

        col1, col2 = st.columns([3, 1])
        simpan = col1.button("SIMPAN ARSIP SEKARANG", type="primary", use_container_width=True)
        tutup = col2.button("Tutup", use_container_width=True)

        if tutup:
            st.session_state.open_upload = False
            st.rerun()

        if simpan:
            nama_kegiatan = safe_text(nama_kegiatan)
            pic = safe_text(pic)
            deskripsi = safe_text(deskripsi)
            link_video = safe_text(link_video)

            if not nama_kegiatan:
                st.error("Nama kegiatan wajib diisi.")
                return

            if (not foto_files) and (not dok_files) and (not link_video):
                st.error("Minimal upload foto/dokumen atau isi link video.")
                return

            try:
                service = get_service()
                ROOT = st.secrets["FOLDER_ID"]

                # 1) folder tahun
                tahun_name = str(tgl.year)
                tahun_folder_id = get_or_create_folder(service, ROOT, tahun_name)

                # 2) folder kegiatan di bawah tahun
                folder_kegiatan_name = make_activity_folder_name(tgl, nama_kegiatan, pic)
                kegiatan_folder_id = get_or_create_folder(service, tahun_folder_id, folder_kegiatan_name)

                # 3) subfolder
                foto_folder_id = get_or_create_folder(service, kegiatan_folder_id, "FOTO")
                dok_folder_id  = get_or_create_folder(service, kegiatan_folder_id, "DOKUMEN")

                # upload foto
                if foto_files:
                    for f in foto_files:
                        upload_file(service, foto_folder_id, f, f.name)

                # upload dokumen
                if dok_files:
                    for f in dok_files:
                        upload_file(service, dok_folder_id, f, f.name)

                # metadata txt
                meta_txt = (
                    f"Tanggal: {tgl.isoformat()}\n"
                    f"PIC: {pic}\n"
                    f"Kegiatan: {nama_kegiatan}\n\n"
                    f"Deskripsi:\n{deskripsi}\n\n"
                    f"Link Video:\n{link_video}\n"
                )
                upload_text(service, kegiatan_folder_id, "metadata.txt", meta_txt)

                st.success("✅ Arsip berhasil disimpan ke Google Drive")
                st.caption(f"Folder: {tahun_name} / {folder_kegiatan_name}")

                st.session_state.open_upload = False
                st.rerun()

            except Exception as e:
                st.error("Gagal menyimpan arsip. Cek secrets, izin folder, dan Drive API.")
                st.exception(e)

    modal()
