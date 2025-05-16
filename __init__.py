import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv()

conection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("CONTAINER")


def upload_blob(blob_name, alien_number, case_type): 
    
    metadata = {"AlienNumber": alien_number, "CaseType": case_type} 

    blob_service_client = BlobServiceClient.from_connection_string(conection_string)

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    blob_client.set_blob_metadata(metadata)
    print(f"Blob {blob_name} metadata set to {metadata}")

if __name__ == "__main__":
    blob_name = "ABEL EDUARDO CALVILLO SERNA-Appointment (1).pdf"
    upload_blob(blob_name, "123456789", "example_case")