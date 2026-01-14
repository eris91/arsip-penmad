import streamlit as st
import re

from components.sidebar import render_sidebar
from components.filters import render_filters
from components.table import render_table
from components.upload_modal import open_upload_modal_button, render_upload_modal

from services.gdrive import (
    get_service, list_children, count_items_in_subfolder
)
from services.utils import is_year_folder

st.set_page_config(page_title="PENMADARC - Arsip", layout="wide")

with open("style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_sidebar()

st.title("Arsip / Semua Kegiatan")
st.caption("Struktur Drive: Tahun → Kegiatan → (FOTO, DOKUMEN)")

# tombol tambah arsip
top1, top2 = st.columns([7, 2])
with top2:
    open_upload_modal_button()

# render modal upload bila terbuka
render_upload_modal()

# --- load data drive (Service Account + Shared Drive) ---
service = get_service()
ROOT = st.secrets["FOLDER_ID"]  # folder root DI DALAM SHARED DRIVE

# list folder tahun
children = list_children(service, ROOT, only_folders=True)
years = [(f["name"], f["id"]) for f in children if is_year_folder(f["name"])]
years.sort(key=lambda x: x[0], reverse=True)

year_options = ["Semua Tahun"] + [y[0] for y in years]

# filter bar
filters = render_filters(year_options)

# tentukan tahun folder target
targets = []
if filters["tahun"] == "Semua Tahun":
    targets = years
else:
    year_map = dict(years)
    if filters["tahun"] in year_map:
        targets = [(filters["tahun"], year_map[filters["tahun"]])]

# kumpulkan baris tabel dari folder kegiatan
rows = []



q = (filters.get("q") or "").strip().lower()
jenis = filters.get("jenis")

for year_name, year_id in targets:
    # folder kegiatan dalam tahun
    kegiatan_folders = list_children(service, year_id, only_folders=True)

    # arsip_tahun_ini:
    # - kalau user pilih tahun tertentu: jumlah kegiatan di tahun itu
    # - kalau semua tahun: nanti kita set ke tahun terbaru (di bawah)
    if filters["tahun"] != "Semua Tahun":
        arsip_tahun_ini = len(kegiatan_folders)

    for k in kegiatan_folders:
        total_arsip += 1

        folder_name = k["name"]
        parts = [p.strip() for p in folder_name.split(" - ")]

        tgl_txt = parts[0] if len(parts) > 0 else ""
        kegiatan = parts[1] if len(parts) > 1 else folder_name
        pic = parts[2] if len(parts) > 2 else ""

        # hitung lampiran
        foto_count = count_items_in_subfolder(service, k["id"], "FOTO")
        dok_count  = count_items_in_subfolder(service, k["id"], "DOKUMEN")
        total_foto += foto_count
        total_lampiran = foto_count + dok_count

        # filter jenis
        if jenis == "Foto" and foto_count == 0:
            continue
        if jenis == "Dokumen" and dok_count == 0:
            continue

        # filter search
        if q:
            if q not in kegiatan.lower() and q not in pic.lower() and q not in folder_name.lower():
                continue

        rows.append({
            "TANGGAL": tgl_txt,
            "KEGIATAN": kegiatan,
            "PIC": pic,
            "LAMPIRAN": f"📎 {total_lampiran}" if total_lampiran else "—",
            "AKSI": f"https://drive.google.com/drive/folders/{k['id']}"
        })

# cards (tampilkan ringkasan)
selected_year = filters["tahun"]
if selected_year == "Semua Tahun":
    # kalau semua tahun, arsip_tahun_ini = jumlah kegiatan di tahun terbaru (jika ada)
    if years:
        newest_year_id = years[0][1]
        arsip_tahun_ini = len(list_children(service, newest_year_id, only_folders=True))


# table
render_table(rows)

