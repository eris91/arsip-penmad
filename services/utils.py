import re
from datetime import date

def is_year_folder(name: str) -> bool:
    return bool(re.fullmatch(r"\d{4}", str(name).strip()))

def safe_text(s: str) -> str:
    return str(s or "").strip()

def make_activity_folder_name(tgl: date, kegiatan: str, pic: str) -> str:
    # Format folder kegiatan: YYYY-MM-DD - NAMA - PIC
    kegiatan = safe_text(kegiatan)
    pic = safe_text(pic)
    return f"{tgl.isoformat()} - {kegiatan} - {pic}"
