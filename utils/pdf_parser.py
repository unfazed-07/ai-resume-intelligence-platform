import os
import PyPDF2
import io


def extract_text_with_azure(file_bytes: bytes, filename: str) -> str:
    """
    Extract text from a resume PDF using Azure AI Document Intelligence.
    Falls back to PyPDF2 if Azure credentials are not configured.
    """
    azure_key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")
    azure_endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "")

    if azure_key and azure_endpoint:
        return _extract_with_azure(file_bytes, azure_key, azure_endpoint)
    else:
        print("[INFO] Azure credentials not found. Using PyPDF2 fallback.")
        return _extract_with_pypdf2(file_bytes)


def _extract_with_azure(file_bytes: bytes, key: str, endpoint: str) -> str:
    """Use Azure AI Document Intelligence for high-quality OCR + layout extraction."""
    try:
        from azure.ai.documentintelligence import DocumentIntelligenceClient
        from azure.core.credentials import AzureKeyCredential

        client = DocumentIntelligenceClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key)
        )

        poller = client.begin_analyze_document(
            model_id="prebuilt-layout",
            body=file_bytes,
            content_type="application/pdf"
        )
        result = poller.result()

        extracted_text = []
        for page in result.pages:
            for line in page.lines:
                extracted_text.append(line.content)

        return "\n".join(extracted_text)

    except ImportError:
        print("[WARNING] azure-ai-documentintelligence not installed. Using PyPDF2.")
        return _extract_with_pypdf2(file_bytes)
    except Exception as e:
        print(f"[ERROR] Azure extraction failed: {e}. Falling back to PyPDF2.")
        return _extract_with_pypdf2(file_bytes)


def _extract_with_pypdf2(file_bytes: bytes) -> str:
    """Fallback PDF text extraction using PyPDF2."""
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text_parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
        return "\n".join(text_parts)
    except Exception as e:
        return f"[ERROR] Could not extract text from PDF: {e}"


def extract_multiple_resumes(uploaded_files: list) -> dict:
    """
    Extract text from multiple uploaded resume files.
    Returns a dict: {filename: extracted_text}
    """
    results = {}
    for uploaded_file in uploaded_files:
        file_bytes = uploaded_file.read()
        text = extract_text_with_azure(file_bytes, uploaded_file.name)
        results[uploaded_file.name] = text
        uploaded_file.seek(0)  # Reset file pointer
    return results
