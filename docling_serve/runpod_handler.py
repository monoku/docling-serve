import logging
import tempfile
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Union

import runpod
from docling.datamodel.base_models import DocumentStream, InputFormat
from docling.document_converter import DocumentConverter
from docling_serve.docling_conversion import (
    ConvertDocumentsOptions,
    convert_documents,
    converters,
    get_pdf_pipeline_opts,
)
from docling_serve.response_preparation import process_results
from docling_serve.settings import docling_serve_settings


# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:\t%(asctime)s - %(name)s - %(message)s",
    datefmt="%H:%M:%S",
)
_log = logging.getLogger(__name__)

# Inicialización de conversores al iniciar el contenedor
pdf_format_option, options_hash = get_pdf_pipeline_opts(ConvertDocumentsOptions())
converters[options_hash] = DocumentConverter(
    format_options={InputFormat.PDF: pdf_format_option, InputFormat.IMAGE: pdf_format_option}
)
converters[options_hash].initialize_pipeline(InputFormat.PDF)


# -------------------
# RUNPOD HANDLER
# -------------------

def handler(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler de RunPod para procesar solicitudes de conversión de documentos.
    """

    _log.info(f"Recibido evento: {event}")

    # Verifica si se envió un archivo en Base64 o una URL
    sources: List[Union[str, DocumentStream]] = []
    request_options = ConvertDocumentsOptions()

    if "files" in event:
        file_sources = []
        for file_data in event["files"]:
            file_name = file_data.get("name", "document.pdf")
            file_bytes = BytesIO(bytes(file_data["content"], encoding="utf-8"))
            file_sources.append(DocumentStream(name=file_name, stream=file_bytes))

        sources.extend(file_sources)

    if "urls" in event:
        sources.extend(event["urls"])

    if not sources:
        return {"error": "No se proporcionaron archivos o URLs para la conversión."}

    results = convert_documents(sources=sources, options=request_options)
    response = process_results(conversion_options=request_options, conv_results=results)

    return response


# -------------------
# INICIALIZAR RUNPOD
# -------------------
runpod.serverless.start({"handler": handler})
