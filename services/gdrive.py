import io
import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/drive"]

def get_service():
    info = st.secrets["gcp_service_account"]
    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    return build("drive", "v3", credentials=creds, cache_discovery=False)

def list_children(service, parent_id: str, only_folders: bool = False):
    q = f"'{parent_id}' in parents and trashed=false"
    if only_folders:
        q += " and mimeType='application/vnd.google-apps.folder'"
    res = service.files().list(
        q=q,
        fields="files(id,name,mimeType,createdTime,webViewLink,parents)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True,
    ).execute()
    return res.get("files", [])

def _escape_drive_query_value(value: str) -> str:
    # Escape single quote for Drive query string
    return value.replace("'", "\\'")

def find_folder(service, parent_id: str, name: str):
    safe_name = _escape_drive_query_value(name)
    q = (
        "mimeType='application/vnd.google-apps.folder' "
        f"and name='{safe_name}' and '{parent_id}' in parents and trashed=false"
    )
    res = service.files().list(
        q=q,
        fields="files(id,name)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True,
    ).execute()
    files = res.get("files", [])
    return files[0]["id"] if files else None

def create_folder(service, parent_id: str, name: str):
    meta = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }
    out = service.files().create(
        body=meta,
        fields="id",
        supportsAllDrives=True,
    ).execute()
    return out["id"]

def get_or_create_folder(service, parent_id: str, name: str):
    existing = find_folder(service, parent_id, name)
    return existing if existing else create_folder(service, parent_id, name)

def upload_file(service, parent_id: str, uploaded_file, filename: str):
    media = MediaIoBaseUpload(
        io.BytesIO(uploaded_file.getbuffer()),
        mimetype=uploaded_file.type,
        resumable=True,
    )
    meta = {"name": filename, "parents": [parent_id]}
    return service.files().create(
        body=meta,
        media_body=media,
        fields="id,webViewLink,name",
        supportsAllDrives=True,
    ).execute()

def upload_text(service, parent_id: str, filename: str, text: str):
    bio = io.BytesIO(text.encode("utf-8"))
    media = MediaIoBaseUpload(bio, mimetype="text/plain", resumable=False)
    meta = {"name": filename, "parents": [parent_id]}
    return service.files().create(
        body=meta,
        media_body=media,
        fields="id",
        supportsAllDrives=True,
    ).execute()

def count_items_in_subfolder(service, parent_folder_id: str, subfolder_name: str) -> int:
    sub_id = find_folder(service, parent_folder_id, subfolder_name)
    if not sub_id:
        return 0
    res = service.files().list(
        q=f"'{sub_id}' in parents and trashed=false",
        fields="files(id)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True,
    ).execute()
    return len(res.get("files", []))
