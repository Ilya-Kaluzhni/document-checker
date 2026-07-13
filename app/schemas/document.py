from pydantic import BaseModel

from app.enums.document_type import DocumentType


class DocumentResponse(BaseModel):

    name: str
    detected_type: DocumentType
    size_kb: int