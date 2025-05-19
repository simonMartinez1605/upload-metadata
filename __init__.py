import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        blob_name = req.params.get('blob_name')
        alien_number = req.params.get('alien_number')
        case_type = req.params.get('case_type')
    except AttributeError:
        return func.HttpResponse(
             "Por favor, pasa los parámetros 'blob_name', 'alien_number' y 'case_type' en la URL.",
             status_code=400
        )

    if not all([blob_name, alien_number, case_type]):
        return func.HttpResponse(
             "Por favor, proporciona valores para 'blob_name', 'alien_number' y 'case_type'.",
             status_code=400
        )

    connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.environ.get("CONTAINER")

    if not connection_string or not container_name:
        logging.error("Las variables de entorno AZURE_STORAGE_CONNECTION_STRING o CONTAINER no están configuradas.")
        return func.HttpResponse(
             "Error de configuración de la función.",
             status_code=500
        )

    metadata = {"AlienNumber": alien_number, "CaseType": case_type}

    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.set_blob_metadata(metadata)
        logging.info(f"Blob {blob_name} metadata set to {metadata}")
        return func.HttpResponse(
             f"Metadatos del blob {blob_name} establecidos correctamente.",
             status_code=200
        )
    except Exception as e:
        logging.error(f"Error al establecer los metadatos del blob: {e}")
        return func.HttpResponse(
             f"Error al establecer los metadatos del blob: {e}",
             status_code=500
        )

if __name__ == "__main__":
    # Este bloque no se ejecutará en Azure Functions
    pass