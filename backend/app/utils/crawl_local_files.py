import io
from typing import List, Dict
from fastapi import UploadFile
from PyPDF2 import PdfReader

async def extract_file_content(files: List[UploadFile]) -> Dict[str, str]:
    """
    Extract content from uploaded files and return as a dictionary with filename as key.

    Args:
        files (List[UploadFile]): List of uploaded files.

    Returns:
        Dict[str, str]: Dictionary with filename as key and file content as value.
    """
    file_content_dict = {}

    for upload in files:
        try:
            data = await upload.read()

            # Handle PDFs
            if upload.filename.lower().endswith(".pdf"):
                try:
                    reader = PdfReader(io.BytesIO(data))
                    pages = [page.extract_text() or "" for page in reader.pages]
                    content = "\n\n".join(pages)
                except Exception as e:
                    print(f"Error reading PDF {upload.filename}: {e}")
                    content = ""
            
            # Handle Text Files
            else:
                try:
                    content = data.decode("utf-8", errors="ignore")
                except Exception as e:
                    print(f"Error reading file {upload.filename}: {e}")
                    content = ""

            # Store content in dictionary
            file_content_dict[upload.filename] = content

        except Exception as e:
            print(f"Error processing file {upload.filename}: {e}")

    return file_content_dict
