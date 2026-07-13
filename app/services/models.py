from dataclasses import dataclass

from app.enums.document_type import DocumentType


@dataclass
class FileInfo:
    filename: str
    detected_type: DocumentType
    size: int          # размер в байтах
    extension: str