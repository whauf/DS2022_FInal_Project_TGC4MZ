# app/azure_blob.py
import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

_conn = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
_container = os.getenv("AZURE_CONTAINER")

_client = BlobServiceClient.from_connection_string(_conn) if _conn else None


def download_text_if_exists(blob_name: str):
    """Download text from Azure Blob if it exists."""
    if not _client:
        return None
    bc = _client.get_blob_client(_container, blob_name)
    if not bc.exists():
        return None
    return bc.download_blob().readall().decode()


def upload_text(blob_name: str, text: str):
    """Upload text to Azure Blob (overwrites existing)."""
    if not _client:
        return False
    bc = _client.get_blob_client(_container, blob_name)
    bc.upload_blob(text, overwrite=True)
    return True
