import pytest

from app.enums.document_type import DocumentType
from app.services.document_detector import DocumentDetector


@pytest.mark.parametrize(
    "filename, expected",
    [
        ("договор.pdf", DocumentType.CONTRACT),
        ("contract_47.docx", DocumentType.CONTRACT),
        ("спецификация.pdf", DocumentType.SPECIFICATION),
        ("invoice_001.pdf", DocumentType.INVOICE),
        ("акт_приема.pdf", DocumentType.ACT),
        ("упд.docx", DocumentType.ACT),
        ("scan_0041.jpg", DocumentType.UNKNOWN),
    ],
)
def test_document_detection(filename, expected):
    assert DocumentDetector.detect(filename) == expected