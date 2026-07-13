from enum import Enum


class DocumentType(str, Enum):
    CONTRACT = "contract"
    SPECIFICATION = "specification"
    INVOICE = "invoice"
    ACT = "act"
    UNKNOWN = "unknown"