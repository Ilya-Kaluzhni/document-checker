from app.enums.document_type import DocumentType


class DocumentDetector:
    PATTERNS = {
        DocumentType.CONTRACT: [
            "договор",
            "contract",
            "dogovor",
        ],
        DocumentType.SPECIFICATION: [
            "спецификация",
            "specification",
            "spec",
        ],
        DocumentType.INVOICE: [
            "счет",
            "счёт",
            "invoice",
        ],
        DocumentType.ACT: [
            "акт",
            "упд",
            "act",
        ],
    }

    @classmethod
    def detect(cls, filename: str) -> DocumentType:
        filename = filename.lower()

        for document_type, patterns in cls.PATTERNS.items():
            if any(pattern in filename for pattern in patterns):
                return document_type

        return DocumentType.UNKNOWN