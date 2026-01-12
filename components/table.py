import streamlit as st
import pandas as pd

def render_table(rows: list[dict]):
    """
    rows: list of dict with keys:
    TANGGAL, KEGIATAN, PIC, LAMPIRAN, AKSI
    """
    if not rows:
        st.info("Belum ada arsip untuk filter yang dipilih.")
        return

    df = pd.DataFrame(rows)

    # sort by TANGGAL desc if possible
    if "TANGGAL" in df.columns:
        df = df.sort_values(by="TANGGAL", ascending=False)

    st.data_editor(
        df,
        column_config={
            "AKSI": st.column_config.LinkColumn("AKSI", display_text="👁️ Lihat"),
        },
        hide_index=True,
        use_container_width=True,
        disabled=True
    )
