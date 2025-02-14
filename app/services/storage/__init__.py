from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from app.config import settings

credential = DefaultAzureCredential()
blob_service_client = BlobServiceClient(
    account_url=settings.AZURE_STORAGE, credential=credential
)


def upload_file(file: bytes, file_name: str, overwrite=True) -> dict:
    """Upload a file to Azure Blob Storage.

    Args:
        file (bytes): File to upload.
        file_name (str): Name of the file.
        overwrite (bool, optional): Overwrite if file already exists. Defaults to True.

    Returns:
        dict: Upload response from Azure.
    """
    blob_client = blob_service_client.get_blob_client(
        container=settings.AZURE_PUBLIC_CONTAINER, blob=file_name
    )
    return blob_client.upload_blob(file, overwrite=overwrite)


def delete_file(file_name: str) -> None:
    """Delete a file from Azure Blob Storage.

    Args:
        file_name (str): Name of the file.
    """
    blob_client = blob_service_client.get_blob_client(
        container=settings.AZURE_PUBLIC_CONTAINER, blob=file_name
    )
    blob_client.delete_blob()
