import io
import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

# Scope:
# - drive.file: aman & cukup untuk upload arsip yang dibuat app
# - drive: akses penuh (lebih luas)
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

def _client_config():
    cfg = st.secrets["google_oauth"]
    return {
        "web": {
            "client_id": cfg["client_id"],
            "client_secret": cfg["client_secret"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [cfg["redirect_uri"]],
        }
    }

def get_service():
    """
    Return service Drive v3 menggunakan OAuth.
    Kalau belum login:
      - set st.session_state["google_auth_url"]
      - raise RuntimeError agar UI bisa menampilkan tombol login
    """
    client_config = _client_config()
    redirect_uri = st.secrets["google_oauth"]["redirect_uri"]

    # 1) sudah ada creds di session
    if "google_creds" in st.session_state:
        creds = Credentials.from_authorized_user_info(st.session_state["google_creds"], scopes=SCOPES)
        return build("drive", "v3", credentials=creds, cache_discovery=False)

    # 2) callback OAuth (ada code)
    qp = st.query_params
    if "code" in qp:
        flow = Flow.from_client_config(client_config, scopes=SCOPES, redirect_uri=redirect_uri)
        flow.fetch_token(code=qp["code"])
        creds = flow.credentials

        st.session_state["google_creds"] = {
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": creds.token_uri,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "scopes": creds.scopes,
        }

        # bersihkan param agar tidak fetch ulang
        st.query_params.clear()
        return build("drive", "v3", credentials=creds, cache_discovery=False)

    # 3) belum login -> buat URL login
    flow = Flow.from_client_config(client_config, scopes=SCOPES, redirect_uri=redirect_uri)
    auth_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    st.session_state["google_auth_url"] = auth_url
    raise RuntimeError("NOT_AUTHENTICATED_OAUTH")

def logout():
    st.session_state.pop("google_creds", None)
    st.session_state.pop("google_auth_url", None)

def list_children(service, parent_id: str, only_folders: bool = False):
    q = f"'{parent_id}' in parents and trashed=false"
    if only_folders:
        q += " and mimeType='application/vnd.google-apps.folder'"
    res = service.files().list(
        q=q,
        fields="files(id,name,mimeType,createdTime,webViewLink,parents)"
    ).execute()
    return res.get("files", [])

def find_folder(service, parent_id: str, name: str):
    # NOTE: name='...' raw bisa bermasalah kalau ada apostrof.
    # untuk aman, idealnya escape. sementara cukup untuk nama standar.
    q = (
        "mimeType='application/vnd.google-apps.folder' "
        f"and name='{name}' and '{parent_id}' in parents and trashed=false"
    )
    res = service.files().list(q=q, fields="files(id,name)").execute()
    files = res.get("files", [])
    return files[0]["id"] if files else None

def create_folder(service, parent_id: str, name: str):
    meta = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }
    out = service.files().create(body=meta, fields="id").execute()
    return out["id"]

def get_or_create_folder(service, parent_id: str, name: str):
    existing = find_folder(service, parent_id, name)
    return existing if existing else create_folder(service, parent_id, name)

def upload_file(service, parent_id: str, uploaded_file, filename: str):
    media = MediaIoBaseUpload(
        io.BytesIO(uploaded_file.getbuffer()),
        mimetype=uploaded_file.type,
        resumable=True
    )
    meta = {"name": filename, "parents": [parent_id]}
    return service.files().create(body=meta, media_body=media, fields="id,webViewLink,name").execute()

def upload_text(service, parent_id: str, filename: str, text: str):
    bio = io.BytesIO(text.encode("utf-8"))
    media = MediaIoBaseUpload(bio, mimetype="text/plain", resumable=False)
    meta = {"name": filename, "parents": [parent_id]}
    return service.files().create(body=meta, media_body=media, fields="id").execute()

def count_items_in_subfolder(service, parent_folder_id: str, subfolder_name: str) -> int:
    sub_id = find_folder(service, parent_folder_id, subfolder_name)
    if not sub_id:
        return 0
    res = service.files().list(
        q=f"'{sub_id}' in parents and trashed=false",
        fields="files(id)"
    ).execute()
    return len(res.get("files", []))
