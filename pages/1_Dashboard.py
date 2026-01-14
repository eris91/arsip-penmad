import streamlit as st
from components.sidebar import render_sidebar
from components.cards import render_cards

from services.gdrive import get_service, list_children, count_items_in_subfolder
from services.utils import is_year_folder

st.set_page_config(page_title="PENMADARC - Dashboard", layout="wide")

with open("style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_sidebar()

st.title("Dashboard")
st.caption("Ringkasan aplikasi arsip Penmad.")

# === Ambil data ringkas dari Drive (Shared Drive) ===
service = get_service()
ROOT = st.secrets["FOLDER_ID"]

children = list_children(service, ROOT, only_folders=True)
years = [(f["name"], f["id"]) for f in children if is_year_folder(f["name"])]
years.sort(key=lambda x: x[0], reverse=True)

total_arsip = 0
total_foto = 0
arsip_tahun_ini = 0

for year_name, year_id in years:
    kegiatan_folders = list_children(service, year_id, only_folders=True)
    total_arsip += len(kegiatan_folders)

    for k in kegiatan_folders:
        total_foto += count_items_in_subfolder(service, k["id"], "FOTO")

if years:
    newest_year_id = years[0][1]
    arsip_tahun_ini = len(list_children(service, newest_year_id, only_folders=True))

render_cards(
    total_arsip=total_arsip,
    arsip_tahun_ini=arsip_tahun_ini,
    total_foto=total_foto
)

st.subheader("Grafik (opsional)")
st.info("Nanti bisa ditambahkan grafik Arsip per Tahun / Jenis.")
